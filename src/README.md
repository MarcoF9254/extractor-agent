# Implementation

## Pilot A — ChatGPT Export ZIP Inventory Reader

The `extractor_agent.inventory` module provides a deterministic, read-only
inventory scanner for ChatGPT data-export ZIP archives.

### Status

**Pilot A — Provisional.** This output shape is not a ratified cross-stage
contract. See the `_pilot_a_provisional` and `_note` fields in the output.

### Quick start

```python
from extractor_agent import build_inventory

result = build_inventory("/path/to/chatgpt-export.zip")
print(result["conversation_count"])      # 230
print(result["role_counts"]["user"])     # 1820
print(result["content_type_counts"]["text"])  # 3946
```

### CLI usage

```bash
python -m extractor_agent.inventory /path/to/export.zip
```

### Output shape

The returned dictionary has these fields (all deterministic, no runtime
timestamps, no absolute paths):

| Field | Type | Description |
|---|---|---|
| `inventory_schema_version` | `str` | `"0.1"` |
| `export_manifest_version` | `int` | From ZIP manifest ``"version"`` field (provisional output name) |
| `conversation_shards` | `list[str]` | Sorted shard filenames |
| `conversation_count` | `int` | Total conversations |
| `conversation_node_count` | `int` | Total mapping nodes |
| `message_node_count` | `int` | Nodes with non-null message |
| `null_message_node_count` | `int` | Nodes with null message |
| `role_counts` | `dict` | Message count by author role |
| `content_type_counts` | `dict` | Message count by content type |
| `asset_file_count` | `int` | Top-level .dat files |
| `conversation_asset_name_entry_count` | `int` | Entries in optional index |
| `library_file_record_count` | `int` | Records in optional metadata |
| `warnings` | `list[str]` | Non-critical observations |

### Fail-closed behaviour

Raises an `InventoryError` subclass (never returns a partial/incomplete
inventory) for: invalid ZIP, missing/corrupt manifest, missing/corrupt shard,
duplicate conversation IDs, absent conversation IDs, invalid mapping structure,
malformed JSON, non-array shard roots, resource limit exceedance, and security
violations.

### Security

The reader enforces:

- **ZIP integrity validation** via `testzip()`
- **No path traversal** — rejects `../` and absolute member names
- **No encrypted members**
- **No unsupported compression** (only stored and deflated)
- **Decompression bomb detection** via configurable compression-ratio limit
- **Size limits** on per-member and total uncompressed JSON
- **Entry-count limits** on the archive
- **Conversation and node-count limits**

All limits are configurable via the `limits` parameter. Defaults are
documented in `constants.py` as Pilot A implementation limits.

### Testing

```bash
git clone https://github.com/MarcoF9254/extractor-agent.git
cd extractor-agent
uv pip install -e ".[dev]"
pytest tests/test_inventory.py -v
```

All tests use **synthetic fixtures only** — no real ChatGPT export data.

### Configuration limits

The reader enforces configurable resource limits (Pilot A provisional values):

| Limit | Default | Notes |
|---|---|---|
| `max_archive_entries` | 2,000 | Maximum ZIP member count |
| `max_member_uncompressed_bytes` | 500 MB | Per-member uncompressed size |
| `max_total_uncompressed_bytes` | 3 GB | Total archive uncompressed size |
| `max_conversation_count` | 10,000 | Conversations across all shards |
| `max_mapping_node_count` | 500,000 | Total mapping nodes |
| `max_compression_ratio` | 100 | Compression ratio bomb threshold |

These are implementation limits, not governance decisions. Callers may override
via the ``limits`` parameter, but doing so relaxes admission protections.
The CLI always uses the safe defaults above.
