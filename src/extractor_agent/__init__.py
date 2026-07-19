"""Extractor Agent — Pilot A: ChatGPT export ZIP inventory reader."""

from .exceptions import (
    InventoryError,
    SecurityError,
    ZipIntegrityError,
    ManifestError,
    ShardError,
    DuplicateConversationError,
    LimitExceededError,
)


def __getattr__(name):
    """Lazy-import build_inventory to avoid a runpy warning when
    the inventory module is invoked via ``python -m`` (which would
    otherwise import inventory.py before __main__ execution)."""
    if name == "build_inventory":
        from .inventory import build_inventory

        return build_inventory
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "build_inventory",
    "InventoryError",
    "SecurityError",
    "ZipIntegrityError",
    "ManifestError",
    "ShardError",
    "DuplicateConversationError",
    "LimitExceededError",
]
