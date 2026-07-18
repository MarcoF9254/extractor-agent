"""
Pilot A implementation limits — safe provisional defaults.

These are NOT governance decisions. They are implementation-time
bounds chosen to prevent resource abuse during ZIP inventory scanning.
"""

from typing import Dict, Any

DEFAULT_LIMITS: Dict[str, Any] = {
    # Maximum number of entries in the ZIP archive.
    "max_archive_entries": 2_000,
    # Maximum uncompressed size of a single JSON member (bytes).
    # 500 MB allows large conversation exports without unbounded memory.
    "max_json_uncompressed_bytes": 500 * 1024 * 1024,
    # Maximum total uncompressed JSON size across all relevant members (bytes).
    "max_total_json_uncompressed_bytes": 2 * 1024 * 1024 * 1024,
    # Maximum conversation count across all shards.
    "max_conversation_count": 10_000,
    # Maximum mapping-node count across all conversations.
    "max_mapping_node_count": 500_000,
    # Maximum compression ratio (uncompressed / compressed).
    # A ratio above 100× is almost certainly a decompression bomb.
    "max_compression_ratio": 100,
}

# Canonical ZIP member names for the ChatGPT export format.
MANIFEST_NAME = "export_manifest.json"
SHARD_PREFIX = "conversations-"
ASSET_FILE_NAMES_NAME = "conversation_asset_file_names.json"
LIBRARY_FILES_NAME = "library_files.json"

# Known manifest fields that may list conversation shard filenames.
SHARD_LIST_FIELDS = (
    "conversation_shards",
    "file_names",
    "conversations",
)
