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
import stat
from pathlib import PurePosixPath
from typing import Any, Dict, List, Optional
from zipfile import ZipFile, ZipInfo

from .constants import (
    DEFAULT_LIMITS,
    MANIFEST_NAME,
    ASSET_FILE_NAMES_NAME,
    LIBRARY_FILES_NAME,
    SHARD_PREFIX,
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
    # -- Phase 1: Archive entry count ---------------------------------------
    infos = zf.infolist()

    if len(infos) > limits["max_archive_entries"]:
        raise LimitExceededError(
            f"Archive entry count {len(infos)} exceeds "
            f"limit {limits['max_archive_entries']}"
        )

    # -- Phase 2: Metadata-only admission (no reading / decompression) ------
    seen_names: Dict[str, ZipInfo] = {}
    total_uncompressed = 0
    total_json_uncompressed = 0
    limit_member = limits["max_member_uncompressed_bytes"]
    limit_total = limits["max_total_uncompressed_bytes"]

    for info in infos:
        _check_member_name(info.filename, seen_names)
        _check_encrypted(info)
        _check_compression(info)
        _check_special_entry(info)
        _check_ratio(info, limits)

        norm = _norm_name(info.filename)

        # Individual member uncompressed size limit (metadata check).
        if info.file_size > limit_member:
            raise LimitExceededError(
                f"Uncompressed size {info.file_size} of {norm} "
                f"exceeds limit {limit_member}"
            )

        total_uncompressed += info.file_size
        if norm.endswith(".json"):
            total_json_uncompressed += info.file_size

        seen_names[norm] = info

    # Total archive uncompressed size limit.
    if total_uncompressed > limit_total:
        raise LimitExceededError(
            f"Total uncompressed size {total_uncompressed} "
            f"exceeds limit {limit_total}"
        )

    # -- Phase 3: Integrity validation (after all metadata checks) ----------
    # testzip() performs CRC / truncated-member verification by reading and
    # decompressing — it is safe to call now because every member has been
    # admitted on metadata alone.
    bad = zf.testzip()
    if bad is not None:
        raise ZipIntegrityError(f"ZIP integrity check failed on member: {bad}")

    # -- Phase 4: Build name_index (safe to read now) -----------------------
    name_index = dict(seen_names)

    # -- Phase 5: Read & validate export manifest --------------------------
    if MANIFEST_NAME not in name_index:
        raise ManifestError(f"{MANIFEST_NAME} is missing from archive")

    manifest_raw = _read_json_member(zf, name_index[MANIFEST_NAME], limits)
    if not isinstance(manifest_raw, dict):
        raise ManifestError(f"{MANIFEST_NAME} root is not a JSON object")

    # Read the real "version" field from the ChatGPT export manifest.
    # Reject the invented legacy field "export_manifest_version" when
    # "version" is absent (fail-closed — do not treat an invented
    # fixture-only schema as canonical).
    version = manifest_raw.get("version")
    if not isinstance(version, int):
        raise ManifestError(
            'Manifest field "version" is missing or not an integer'
        )

    # The output preserves the provisional field name.
    export_manifest_version = version

    # -- Discover conversation shards via logical_files ---------------------
    shards = _validate_logical_files(manifest_raw, name_index)

    # -- Cross-check declared shards against export_files -------------------
    _validate_export_files_cross_check(manifest_raw, shards)

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


def _check_member_name(
    name: str,
    seen: Dict[str, ZipInfo],
) -> None:
    """Check path traversal, absolute paths, and duplicate names.

    Operates on metadata only — does not read any member data.
    """
    if name.startswith("/") or name.startswith("\\"):
        raise SecurityError(f"Absolute-path ZIP member: {name}")

    norm = _norm_name(name)

    if name.startswith("../") or "/../" in norm or "\\..\\" in norm:
        raise SecurityError(f"Path-traversal ZIP member: {name}")
    try:
        parts = PurePosixPath(norm).parts
        if ".." in parts:
            raise SecurityError(f"Path-traversal ZIP member: {name}")
    except (ValueError, TypeError):
        raise SecurityError(f"Unusable ZIP member name: {name}")

    if norm in seen:
        raise SecurityError(f"Duplicate ZIP member name: {name}")


def _check_encrypted(info: ZipInfo) -> None:
    """Reject members with the encryption flag set (metadata-only)."""
    if info.flag_bits & 0x01:
        raise SecurityError(f"Encrypted ZIP member")


def _check_compression(info: ZipInfo) -> None:
    """Reject unsupported compression types (metadata-only)."""
    if info.compress_type not in (0, 8):  # 0=stored, 8=deflated
        raise SecurityError(
            f"Unsupported compression type {info.compress_type}"
        )


def _check_special_entry(info: ZipInfo) -> None:
    """Reject symlinks, device nodes, FIFOs, and sockets.

    Checks Unix mode bits from ``external_attr`` (high 16 bits).
    When no Unix mode is present (e.g. Windows-origin archives),
    external_attr >> 16 is 0 and no special entry is detected.
    """
    mode = info.external_attr >> 16
    if mode:
        if (
            stat.S_ISLNK(mode)
            or stat.S_ISBLK(mode)
            or stat.S_ISCHR(mode)
            or stat.S_ISFIFO(mode)
            or stat.S_ISSOCK(mode)
        ):
            raise SecurityError(f"Unsupported special-file ZIP entry")


def _check_ratio(info: ZipInfo, limits: Dict[str, Any]) -> None:
    """Reject decompression bombs based on compression ratio.

    Operates on metadata only — only info.file_size and
    info.compress_size are consulted.
    """
    if info.compress_size > 0 and info.file_size > 0:
        ratio = info.file_size / info.compress_size
        if ratio > limits["max_compression_ratio"]:
            raise SecurityError(
                f"Compression ratio {ratio:.2f} exceeds "
                f"limit {limits['max_compression_ratio']}"
            )


def _read_json_member(
    zf: ZipFile,
    info: ZipInfo,
    limits: Dict[str, Any],
) -> Any:
    """Read a ZIP member, check size, parse as JSON.

    Raises ``LimitExceededError`` or ``ShardError`` on failure.
    """
    # Defensive check — per-member limit was already enforced in Phase 2.
    if info.file_size > limits["max_member_uncompressed_bytes"]:
        raise LimitExceededError(
            f"Uncompressed size {info.file_size} of {info.filename} exceeds "
            f"limit {limits['max_member_uncompressed_bytes']}"
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


def _validate_logical_files(
    manifest: Dict[str, Any],
    name_index: Dict[str, ZipInfo],
) -> List[str]:
    """Validate ``logical_files`` and return the authoritative shard list.

    The real ChatGPT export manifest declares shards at::

        logical_files["conversations.json"]["files"]

    Every fail-closed condition enumerated in Pilot A is checked here.

    Returns
    -------
    List[str]
        Sorted list of declared shard filenames that exist in the archive.

    Raises
    ------
    ManifestError
        For any missing, malformed, or inconsistent logical_files entry.
    ShardError
        For a declared shard that is missing from the ZIP.
    """
    logical_files = manifest.get("logical_files")
    if not isinstance(logical_files, dict):
        raise ManifestError(
            '"logical_files" is missing or not an object'
        )

    conv_entry = logical_files.get("conversations.json")
    if not isinstance(conv_entry, dict):
        raise ManifestError(
            '"logical_files" has no "conversations.json" entry '
            "or it is not an object"
        )

    files = conv_entry.get("files")
    if not isinstance(files, list) or len(files) == 0:
        raise ManifestError(
            '"conversations.json" "files" is missing, not an array, '
            "or empty"
        )

    shard_count = conv_entry.get("shard_count")
    if not isinstance(shard_count, int):
        raise ManifestError(
            '"shard_count" is missing or not an integer'
        )

    if conv_entry.get("sharded") is not True:
        raise ManifestError(
            '"sharded" must be true for the logical_files shard path'
        )

    if shard_count != len(files):
        raise ManifestError(
            f'"shard_count" ({shard_count}) does not match '
            f'"files" count ({len(files)})'
        )

    seen: set = set()
    shards: List[str] = []
    for fname in files:
        if not isinstance(fname, str) or fname == "":
            raise ManifestError(
                'Non-string or empty filename in "files" list'
            )
        if not _SHARD_RE.match(fname):
            raise ManifestError(
                f'Declared shard "{fname}" does not match expected '
                f'pattern "{SHARD_PREFIX}NNN.json"'
            )
        if fname in seen:
            raise ManifestError(
                f'Duplicate shard filename in "files": {fname}'
            )
        seen.add(fname)
        if fname not in name_index:
            raise ShardError(
                f'Declared shard missing from archive: {fname}'
            )
        shards.append(fname)

    # Reject any top-level conversations-NNN.json outside the declared list.
    for norm in name_index:
        if _SHARD_RE.match(norm) and norm not in seen:
            raise ManifestError(
                f"Undeclared conversation shard in archive: {norm}"
            )

    return sorted(shards)


def _validate_export_files_cross_check(
    manifest: Dict[str, Any],
    shards: List[str],
) -> None:
    """Cross-check every declared shard against ``export_files`` entries.

    Every conversation shard declared via ``logical_files`` must have a
    corresponding ``export_files`` entry with a matching ``path``.

    Raises
    ------
    ManifestError
        For missing, duplicate, or malformed export_files entries.
    """
    export_files = manifest.get("export_files")
    if not isinstance(export_files, list):
        raise ManifestError('"export_files" is missing or not an array')

    seen_paths: set = set()
    exported_shards: set = set()

    for entry in export_files:
        if not isinstance(entry, dict):
            raise ManifestError("Non-object entry in \"export_files\"")
        path = entry.get("path")
        if not isinstance(path, str) or path == "":
            raise ManifestError(
                '"export_files" entry missing valid "path" field'
            )
        if path in seen_paths:
            raise ManifestError(
                f'Duplicate "export_files" path: {path}'
            )
        seen_paths.add(path)

        if _SHARD_RE.match(path):
            exported_shards.add(path)

    for s in shards:
        if s not in exported_shards:
            raise ManifestError(
                f'Declared shard "{s}" is missing from "export_files"'
            )


# ---------------------------------------------------------------------------
# Module CLI — python -m extractor_agent.inventory INPUT_ZIP
# ---------------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    import argparse
    import json
    import sys

    from .exceptions import InventoryError

    parser = argparse.ArgumentParser(
        description="ChatGPT export ZIP structural inventory (Pilot A)"
    )
    parser.add_argument(
        "input_zip",
        help="Path to a ChatGPT data-export ZIP file",
    )
    args = parser.parse_args()

    try:
        inventory = build_inventory(args.input_zip)
        json.dump(
            inventory,
            sys.stdout,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ": "),
        )
        sys.stdout.write("\n")
    except InventoryError as exc:
        # Sanitize: emit only the exception type; do not leak
        # absolute paths, conversation IDs, or message content.
        print(
            f"Error: {type(exc).__name__}",
            file=sys.stderr,
        )
        sys.exit(1)
