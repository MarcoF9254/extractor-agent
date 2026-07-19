"""Custom exceptions for the export inventory reader."""


class InventoryError(Exception):
    """Base exception for all export inventory errors."""


class SecurityError(InventoryError):
    """Security violation detected in the archive."""


class ZipIntegrityError(InventoryError):
    """ZIP integrity validation failed."""


class ManifestError(InventoryError):
    """Export manifest is missing, malformed, or incomplete."""


class ShardError(InventoryError):
    """Conversation shard validation or counting failed."""


class DuplicateConversationError(InventoryError):
    """Duplicate conversation IDs detected across shards."""


class LimitExceededError(InventoryError):
    """A configurable resource limit was exceeded."""
