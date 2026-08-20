"""Typed application configuration loaded from the process environment."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATA_DIR = Path("~/.local/share/ai-mix")
DEFAULT_LOG_LEVEL = "INFO"
_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


class ConfigurationError(ValueError):
    """Raised when an environment value cannot form a safe application config."""


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Resolved paths and runtime settings used by the composition root."""

    data_dir: Path
    database_path: Path
    log_level: str = DEFAULT_LOG_LEVEL
    busy_timeout_ms: int = 5000

    def __post_init__(self) -> None:
        data_dir = _resolve_path(self.data_dir, "data directory")
        database_path = _resolve_path(self.database_path, "database path")
        level = self.log_level.upper().strip()
        if level not in _LOG_LEVELS:
            raise ConfigurationError(
                f"AI_MIX_LOG_LEVEL must be one of {', '.join(sorted(_LOG_LEVELS))}"
            )
        if self.busy_timeout_ms <= 0:
            raise ConfigurationError("busy timeout must be a positive integer")
        object.__setattr__(self, "data_dir", data_dir)
        object.__setattr__(self, "database_path", database_path)
        object.__setattr__(self, "log_level", level)

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> AppConfig:
        """Build a config once from environment values and resolve all paths."""

        values = os.environ if environ is None else environ
        raw_data_dir = values.get("AI_MIX_DATA_DIR", str(DEFAULT_DATA_DIR)).strip()
        if not raw_data_dir:
            raise ConfigurationError("AI_MIX_DATA_DIR must not be empty")
        data_dir = _resolve_path(raw_data_dir, "data directory")
        raw_database = values.get("AI_MIX_DATABASE_PATH", "").strip()
        database_path = (
            _resolve_path(raw_database, "database path")
            if raw_database
            else data_dir / "state.sqlite3"
        )
        log_level = values.get("AI_MIX_LOG_LEVEL", DEFAULT_LOG_LEVEL).strip()
        if not log_level:
            raise ConfigurationError("AI_MIX_LOG_LEVEL must not be empty")
        raw_timeout = values.get("AI_MIX_BUSY_TIMEOUT_MS", "5000").strip()
        try:
            timeout = int(raw_timeout)
        except ValueError as exc:
            raise ConfigurationError("AI_MIX_BUSY_TIMEOUT_MS must be an integer") from exc
        return cls(data_dir, database_path, log_level, timeout)


def _resolve_path(value: str | Path, label: str) -> Path:
    try:
        path = Path(value).expanduser()
    except (TypeError, ValueError) as exc:
        raise ConfigurationError(f"{label} is invalid") from exc
    if not str(path):
        raise ConfigurationError(f"{label} must not be empty")
    return path.resolve(strict=False)
