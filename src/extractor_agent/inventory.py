"""
Pilot A — Deterministic, read-only ChatGPT export ZIP inventory reader.

This module inspects a ChatGPT data-export ZIP container and produces
structural inventory metadata only. It does not extract or reproduce
conversation text, titles, user information, attachment names, message
content, or other personal data.

This output shape is Pilot A provisional, not a ratified cross-stage
contract.
"""

from __future__ import annotations

import json
import re
from pathlib import PurePosixPath
from typing import Any, Dict, List, Optional
from zipfile import ZipFile, ZipInfo

from .constants import (
    DEFAULT_LIMITS,
    MANIFEST_NAME,
    ASSET_FILE_NAMES_NAME,
    LIBRARY_FILES_NAME,
    SHARD_PREFIX,
    SHARD_LIST_FIELDS,
)
from .exceptions import (
    DuplicateConversationError,
    InventoryError,
    LimitExceededError,
    ManifestError,
    SecurityError,
    ShardError,
    ZipIntegrityError,
)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_inventory(
    zip_path: str,
    limits: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a structural inventory of a ChatGPT export ZIP.

    Parameters
    ----------
    zip_path:
        Local filesystem path to the ChatGPT data-export ZIP.
    limits:
        Optional overrides for configuration limits. See ``constants.DEFAULT_LIMITS``.

    Returns
    -------
    Dict[str, Any]
        A deterministic JSON-serialisable inventory dictionary (Pilot A provisional).

    Raises
    ------
    InventoryError
        Every fail-closed condition raises a subclass of ``InventoryError``.
    """
    effective_limits = {**DEFAULT_LIMITS, **(limits or {})}

    # -- Open ZIP read-only -------------------------------------------------
    try:
        zf = ZipFile(zip_path, "r")
    except (FileNotFoundError, OSError) as exc:
        raise ZipIntegrityError(f"Input is not a readable ZIP: {exc}")
    except Exception as exc:
        raise ZipIntegrityError(f"Failed to open ZIP: {exc}")

    try:
        return _build_inventory_inner(zf, effective_limits)
    finally:
        zf.close()


# ---------------------------------------------------------------------------
# Internal implementation
# ---------------------------------------------------------------------------


def _build_inventory_inner(
    zf: ZipFile,
    limits: Dict[str, Any],
) -> Dict[str, Any]:
    # -- Collect & validate members -----------------------------------------
    infos = zf.infolist()

    if len(infos) > limits["max_archive_entries"]:
        raise LimitExceededError(
            f"Archive entry count {len(infos)} exceeds "
            f"limit {limits['max_archive_entries']}"
        )

    # Validate ZIP integrity (detect CRC / truncated-member errors).
    bad = zf.testzip()
    if bad is not None:
        raise ZipIntegrityError(f"ZIP integrity check failed on member: {bad}")

    # Build a checked name -> ZipInfo index.
    name_index: Dict[str, ZipInfo] = {}
    total_uncompressed_json = 0

    for info in infos:
        _check_member(info, limits, name_index)

        norm = _norm_name(info.filename)
        name_index[norm] = info

        if norm.endswith(".json"):
            total_uncompressed_json += info.file_size

    if total_uncompressed_json > limits["max_total_json_uncompressed_bytes"]:
        raise LimitExceededError(
            f"Total JSON uncompressed size {total_uncompressed_json} exceeds "
            f"limit {limits['max_total_json_uncompressed_bytes']}"
        )

    # -- Read & validate export manifest -------------------------------------
    if MANIFEST_NAME not in name_index:
        raise ManifestError(f"{MANIFEST_NAME} is missing from archive")
    if MANIFEST_NAME not in name_index:
        raise ManifestError(f"{MANIFEST_NAME} is missing from archive")

    manifest_raw = _read_json_member(zf, name_index[MANIFEST_NAME], limits)
    if not isinstance(manifest_raw, dict):
        raise ManifestError(f"{MANIFEST_NAME} root is not a JSON object")

    export_manifest_version = manifest_raw.get("export_manifest_version")
    if not isinstance(export_manifest_version, int):
        raise ManifestError(
            "export_manifest_version is missing or not an integer"
        )

    # -- Discover conversation shards ---------------------------------------
    shards = _discover_shards(manifest_raw, name_index)
    if not shards:
        raise ManifestError("No conversation shard is discoverable")

    for s in shards:
        if s not in name_index:
            raise ShardError(f"Declared shard missing from archive: {s}")

    # -- Process each shard --------------------------------------------------
    total_conversations = 0
    total_mapping_nodes = 0
    total_message_nodes = 0
    total_null_message_nodes = 0
    role_counts: Dict[str, int] = {}
    content_type_counts: Dict[str, int] = {}
    seen_ids: set = set()
    warnings: List[str] = []

    for shard_name in shards:
        shard_data = _read_json_member(zf, name_index[shard_name], limits)

        if not isinstance(shard_data, list):
            raise ShardError(
                f"Shard {shard_name} top-level is not an array; "
                f"got {type(shard_data).__name__}"
            )

        for conv in shard_data:
            if not isinstance(conv, dict):
                raise ShardError(
                    f"Conversation in {shard_name} is not an object; "
                    f"got {type(conv).__name__}"
                )

            conv_id = conv.get("conversation_id")
            if not isinstance(conv_id, str) or conv_id == "":
                raise ShardError(
                    f"Conversation in {shard_name} lacks a usable unique ID"
                )

            if conv_id in seen_ids:
                raise DuplicateConversationError(
                    f"Duplicate conversation ID across shards: {conv_id}"
                )
            seen_ids.add(conv_id)
            total_conversations += 1

            if total_conversations > limits["max_conversation_count"]:
                raise LimitExceededError(
                    f"Conversation count {total_conversations} exceeds "
                    f"limit {limits['max_conversation_count']}"
                )

            mapping = conv.get("mapping")
            if not isinstance(mapping, dict):
                raise ShardError(
                    f"Conversation {conv_id} has absent or non-dict mapping"
                )

            for node_id, node in mapping.items():
                if not isinstance(node, dict):
                    raise ShardError(
                        f"Invalid mapping node type in conversation {conv_id}; "
                        f"got {type(node).__name__}"
                    )
                total_mapping_nodes += 1

                if total_mapping_nodes > limits["max_mapping_node_count"]:
                    raise LimitExceededError(
                        f"Mapping-node count {total_mapping_nodes} exceeds "
                        f"limit {limits['max_mapping_node_count']}"
                    )

                msg = node.get("message")
                if msg is None:
                    total_null_message_nodes += 1
                elif isinstance(msg, dict):
                    total_message_nodes += 1

                    # -- Author role counting ---------------------------------
                    author = msg.get("author")
                    if isinstance(author, dict):
                        role = author.get("role", "unknown")
                    else:
                        role = "unknown"
                    role_counts[role] = role_counts.get(role, 0) + 1

                    # -- Content type counting --------------------------------
                    content = msg.get("content")
                    if isinstance(content, dict):
                        ct = content.get("content_type", "unknown")
                    else:
                        ct = "unknown"
                    content_type_counts[ct] = content_type_counts.get(ct, 0) + 1
                else:
                    raise ShardError(
                        f"Message field has unsupported type (not null, not dict) "
                        f"in conversation {conv_id}, node {node_id}: "
                        f"{type(msg).__name__}"
                    )

    # -- Count asset files (top-level .dat) -----------------------------------
    asset_file_count = sum(
        1
        for norm in name_index
        if "/" not in norm and norm.endswith(".dat")
    )

    # -- Count conversation_asset_file_names.json entries --------------------
    conv_asset_entry_count = 0
    if ASSET_FILE_NAMES_NAME in name_index:
        asset_name_data = _read_json_member(
            zf, name_index[ASSET_FILE_NAMES_NAME], limits
        )
        if isinstance(asset_name_data, dict):
            conv_asset_entry_count = len(asset_name_data)
        elif isinstance(asset_name_data, list):
            conv_asset_entry_count = len(asset_name_data)
        else:
            warnings.append(
                f"{ASSET_FILE_NAMES_NAME} has unexpected root type; "
                f"counted as 0"
            )

    # -- Count library_files.json records ------------------------------------
    lib_file_record_count = 0
    if LIBRARY_FILES_NAME in name_index:
        lib_data = _read_json_member(
            zf, name_index[LIBRARY_FILES_NAME], limits
        )
        if isinstance(lib_data, list):
            lib_file_record_count = len(lib_data)
        elif isinstance(lib_data, dict):
            # Two plausible shapes: {"files": [...]} or flat key->value map.
            files_array = lib_data.get("files") or lib_data.get("entries")
            if isinstance(files_array, list):
                lib_file_record_count = len(files_array)
            else:
                lib_file_record_count = len(lib_data)
        else:
            warnings.append(
                f"{LIBRARY_FILES_NAME} has unexpected root type; "
                f"counted as 0"
            )

    # -- Assemble deterministic output ---------------------------------------
    inventory: Dict[str, Any] = {
        "inventory_schema_version": "0.1",
        "export_manifest_version": export_manifest_version,
        "conversation_shards": sorted(shards),
        "conversation_count": total_conversations,
        "conversation_node_count": total_mapping_nodes,
        "message_node_count": total_message_nodes,
        "null_message_node_count": total_null_message_nodes,
        "role_counts": dict(sorted(role_counts.items())),
        "content_type_counts": dict(sorted(content_type_counts.items())),
        "asset_file_count": asset_file_count,
        "conversation_asset_name_entry_count": conv_asset_entry_count,
        "library_file_record_count": lib_file_record_count,
        "warnings": sorted(set(warnings)),
        # Label this output shape explicitly.
        "_pilot_a_provisional": True,
        "_note": (
            "This output shape is Pilot A provisional, "
            "not a ratified cross-stage contract."
        ),
    }

    return inventory


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _norm_name(name: str) -> str:
    """Normalise a ZIP member name to forward-slash form.

    This avoids platform-dependent path separators in comparison keys.
    """
    return name.replace("\\", "/")


def _check_member(
    info: ZipInfo,
    limits: Dict[str, Any],
    seen: Dict[str, ZipInfo],
) -> None:
    """Run all per-member security checks."""
    norm = _norm_name(info.filename)

    # -- Path traversal ----------------------------------------------------
    if info.filename.startswith("/") or info.filename.startswith("\\"):
        raise SecurityError(f"Absolute-path ZIP member: {info.filename}")
    if info.filename.startswith("../") or "/../" in norm or "\\..\\" in norm:
        raise SecurityError(f"Path-traversal ZIP member: {info.filename}")
    try:
        parts = PurePosixPath(norm).parts
        if ".." in parts:
            raise SecurityError(f"Path-traversal ZIP member: {info.filename}")
    except (ValueError, TypeError):
        raise SecurityError(f"Unusable ZIP member name: {info.filename}")

    # -- Duplicate names ---------------------------------------------------
    if norm in seen:
        raise SecurityError(f"Duplicate ZIP member name: {info.filename}")

    # -- Encrypted members -------------------------------------------------
    if info.flag_bits & 0x01:
        raise SecurityError(f"Encrypted ZIP member: {info.filename}")

    # -- Unsupported compression type --------------------------------------
    if info.compress_type not in (0, 8):  # 0=stored, 8=deflated
        raise SecurityError(
            f"Unsupported compression type {info.compress_type} "
            f"for member: {info.filename}"
        )

    # -- Compression-ratio bomb --------------------------------------------
    if info.compress_size > 0 and info.file_size > 0:
        ratio = info.file_size / info.compress_size
        if ratio > limits["max_compression_ratio"]:
            raise SecurityError(
                f"Compression ratio {ratio:.2f} exceeds "
                f"limit {limits['max_compression_ratio']} "
                f"for member: {info.filename}"
            )


def _read_json_member(
    zf: ZipFile,
    info: ZipInfo,
    limits: Dict[str, Any],
) -> Any:
    """Read a ZIP member, check size, parse as JSON.

    Raises ``LimitExceededError`` or ``ShardError`` on failure.
    """
    if info.file_size > limits["max_json_uncompressed_bytes"]:
        raise LimitExceededError(
            f"Uncompressed size {info.file_size} of {info.filename} exceeds "
            f"limit {limits['max_json_uncompressed_bytes']}"
        )

    if info.compress_size > limits["max_json_uncompressed_bytes"]:
        raise LimitExceededError(
            f"Compressed size {info.compress_size} of {info.filename} exceeds "
            f"limit {limits['max_json_uncompressed_bytes']}"
        )

    try:
        raw = zf.read(info)
    except Exception as exc:
        raise ShardError(
            f"Failed to read ZIP member {info.filename}: {exc}"
        )

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ShardError(
            f"Invalid JSON in ZIP member {info.filename}: {exc}"
        )


_SHARD_RE = re.compile(rf"^{re.escape(SHARD_PREFIX)}\d{{3}}\.json$")


def _discover_shards(
    manifest: Dict[str, Any],
    name_index: Dict[str, ZipInfo],
) -> List[str]:
    """Discover conversation shard filenames from the manifest.

    Preference order:
    1. Explicit array in manifest (field names from SHARD_LIST_FIELDS).
    2. Pattern-based fallback scanning ``conversations-NNN.json`` in the index.
    """
    # Try explicit fields.
    for field in SHARD_LIST_FIELDS:
        raw = manifest.get(field)
        if isinstance(raw, list) and len(raw) > 0:
            shards: List[str] = []
            for entry in raw:
                if isinstance(entry, str):
                    shards.append(entry)
                elif isinstance(entry, dict):
                    # Some manifests list dicts with a "file_name" field.
                    fn = entry.get("file_name") or entry.get("filename")
                    if isinstance(fn, str):
                        shards.append(fn)
            if shards:
                return shards

    # Fallback: scan name_index for shard-pattern files.
    pattern_shards = sorted(
        norm for norm in name_index if _SHARD_RE.match(norm)
    )
    return pattern_shards
