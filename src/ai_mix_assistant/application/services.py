"""Application services for status and health checks."""

from __future__ import annotations

import platform
import sys
from collections.abc import Mapping
from dataclasses import dataclass

from ai_mix_assistant import __version__

from .config import AppConfig
from .ports import SchemaInfo, StateStore


@dataclass(frozen=True, slots=True)
class HealthReport:
    ok: bool
    checks: Mapping[str, object]
    schema: SchemaInfo

    def as_dict(self) -> dict[str, object]:
        return {
            "status": "ok" if self.ok else "error",
            "checks": dict(self.checks),
            "schema": self.schema.as_dict(),
        }


class SystemStatusService:
    """Coordinates read-only info and initializing health use cases."""

    def __init__(self, config: AppConfig, store: StateStore) -> None:
        self._config = config
        self._store = store

    def info(self) -> dict[str, object]:
        schema = self._store.schema_info()
        return {
            "status": "ok",
            "application": {"name": "ai-mix-assistant", "version": __version__},
            "python": {
                "version": platform.python_version(),
                "implementation": sys.implementation.name,
            },
            "backend": {
                "kind": "sqlite",
                "database_path": str(self._config.database_path),
                "data_dir": str(self._config.data_dir),
                "log_level": self._config.log_level,
            },
            "schema": schema.as_dict(),
        }

    def health(self) -> HealthReport:
        schema = self._store.initialize()
        checks = dict(self._store.check())
        ok = all(value is True for value in checks.values())
        return HealthReport(ok=ok, checks=checks, schema=schema)
