"""Ports implemented by infrastructure adapters."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class StorageError(RuntimeError):
    """A local state store operation failed."""


@dataclass(frozen=True, slots=True)
class SchemaInfo:
    initialized: bool
    current_version: int
    applied_versions: tuple[int, ...]
    database_path: Path

    def as_dict(self) -> dict[str, object]:
        return {
            "initialized": self.initialized,
            "current_version": self.current_version,
            "applied_versions": list(self.applied_versions),
            "database_path": str(self.database_path),
        }


class StateStore(Protocol):
    """Minimal application-facing state store contract."""

    def initialize(self) -> SchemaInfo:
        """Apply pending migrations and return resulting schema information."""

    def schema_info(self) -> SchemaInfo:
        """Read schema state without initializing or mutating it."""

    def check(self) -> Mapping[str, object]:
        """Run a lightweight storage health check."""
