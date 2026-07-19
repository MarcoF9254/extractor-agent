"""Synthetic ZIP fixture builder for Pilot A tests."""

from __future__ import annotations

import io
import json
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED


def build_zip(
    manifest: Optional[Dict[str, Any]] = None,
    shards: Optional[Dict[str, List[Dict[str, Any]]]] = None,
    add_asset_file_names: Optional[Dict[str, Any]] = None,
    add_library_files: Optional[Any] = None,
    asset_files: Optional[List[str]] = None,
    extra_files: Optional[Dict[str, bytes]] = None,
) -> bytes:
    """Build a synthetic ChatGPT export ZIP in memory.

    Returns the ZIP as ``bytes`` suitable for writing to a temp file.
    Every conversation ID is deterministic for reproducible output.
    """
    buf = io.BytesIO()
    # Disallow Zip64 for smaller, simpler files; 65535 entries is more than enough.
    with ZipFile(buf, "w", ZIP_DEFLATED, allowZip64=False) as zf:

        # -- Manifest -----------------------------------------------------------
        if manifest is None:
            manifest = {
                "version": 1,
                "logical_files": {
                    "conversations.json": {
                        "files": ["conversations-000.json"],
                        "shard_count": 1,
                        "sharded": True,
                    }
                },
                "export_files": [
                    {"path": "conversations-000.json", "size_bytes": 1000},
                ],
            }
        zf.writestr("export_manifest.json", json.dumps(manifest, sort_keys=True, indent=2))

        # -- Shards -------------------------------------------------------------
        if shards is None:
            shards = {}

        for shard_name, conversations in shards.items():
            zf.writestr(
                shard_name,
                json.dumps(conversations, sort_keys=True, indent=2),
            )

        # -- Optional asset-name index ------------------------------------------
        if add_asset_file_names is not None:
            zf.writestr(
                "conversation_asset_file_names.json",
                json.dumps(add_asset_file_names, sort_keys=True, indent=2),
            )

        # -- Optional library metadata ------------------------------------------
        if add_library_files is not None:
            zf.writestr(
                "library_files.json",
                json.dumps(add_library_files, sort_keys=True, indent=2),
            )

        # -- Asset .dat files ---------------------------------------------------
        if asset_files:
            for fname in asset_files:
                zf.writestr(fname, b"<binary asset data>")

        # -- Extra files --------------------------------------------------------
        if extra_files:
            for fname, data in extra_files.items():
                zf.writestr(fname, data)

    return buf.getvalue()


def make_conv_id(seed: int) -> str:
    """Deterministic conversation ID for testing."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"test-conversation-{seed}"))


def make_node_id(seed: int) -> str:
    """Deterministic mapping node ID for testing."""
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"test-node-{seed}"))


def make_message(
    role: str = "user",
    content_type: str = "text",
    parts: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a synthetic message dict.

    Content is generic and contains no real personal data.
    """
    if parts is None:
        parts = ["This is a synthetic test message. No real conversation content."]

    msg: Dict[str, Any] = {
        "author": {"role": role},
        "content": {"content_type": content_type, "parts": parts},
        "create_time": 1_700_000_000.0,
        "status": "finished_successfully",
        "end_turn": True,
        "weight": 1.0,
    }
    return msg


def make_conversation(
    conv_id_seed: int,
    node_seeds: Optional[List[Tuple[int, Optional[Dict[str, Any]]]]] = None,
) -> Dict[str, Any]:
    """Build a synthetic conversation dict.

    Parameters
    ----------
    conv_id_seed:
        Deterministic seed for the conversation ID.
    node_seeds:
        List of (seed, message-or-None) tuples describing mapping nodes.
        If ``None``, produces one node with a null message.
    """
    if node_seeds is None:
        node_seeds = [(0, None)]

    mapping: Dict[str, Any] = {}
    for seed, msg in node_seeds:
        nid = make_node_id(seed)
        node: Dict[str, Any] = {"id": nid}

        if msg is not None:
            node["message"] = msg
            node["parent"] = None if seed == 0 else make_node_id(node_seeds[0][0])
            node["children"] = []
        else:
            node["message"] = None
            node["parent"] = None
            node["children"] = []

        mapping[nid] = node

    return {
        "conversation_id": make_conv_id(conv_id_seed),
        "title": f"Synthetic Test Conversation {conv_id_seed}",
        "create_time": 1_700_000_000.0,
        "mapping": mapping,
    }


def deterministic_json(inventory: Dict[str, Any]) -> str:
    """Serialize an inventory dict to deterministic (field-ordered) JSON.

    This function is used by tests to get stable output for byte-level
    comparison. The inventory dict should already have field-order
    guarantees from ``build_inventory``.
    """
    return json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False)
