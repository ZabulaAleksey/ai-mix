"""SQLite implementation of the local state store."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

from ai_mix_assistant.application.ports import SchemaInfo, StorageError

CURRENT_SCHEMA_VERSION = 1


class SQLiteStateStore:
    """A connection-per-operation SQLite store with deterministic migrations."""

    def __init__(self, database_path: Path | str, busy_timeout_ms: int = 5000) -> None:
        path = Path(database_path).expanduser().resolve(strict=False)
        if busy_timeout_ms <= 0:
            raise ValueError("busy_timeout_ms must be positive")
        self.database_path = path
        self.busy_timeout_ms = busy_timeout_ms

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(
                self.database_path,
                timeout=self.busy_timeout_ms / 1000,
            )
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            connection.execute(f"PRAGMA busy_timeout = {self.busy_timeout_ms}")
            yield connection
        except sqlite3.Error as exc:
            raise StorageError(f"sqlite operation failed: {exc}") from exc
        finally:
            if connection is not None:
                connection.close()

    def initialize(self) -> SchemaInfo:
        """Create the migration table and apply all pending migrations atomically."""

        try:
            self.database_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connection() as connection:
                connection.execute("BEGIN IMMEDIATE")
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        version INTEGER PRIMARY KEY,
                        applied_at TEXT NOT NULL
                    )
                    """
                )
                applied = {
                    int(row[0])
                    for row in connection.execute("SELECT version FROM schema_migrations")
                }
                migrations: tuple[tuple[int, Callable[[sqlite3.Connection], None]], ...] = (
                    (1, _migration_one),
                )
                known_versions = tuple(version for version, _ in migrations)
                _validate_applied_versions(applied, known_versions)
                for version, migration in migrations:
                    if version not in applied:
                        migration(connection)
                        connection.execute(
                            "INSERT INTO schema_migrations(version, applied_at) "
                            "VALUES (?, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))",
                            (version,),
                        )
                connection.commit()
                return self._schema_info_from_connection(connection)
        except StorageError:
            raise
        except (OSError, sqlite3.Error) as exc:
            raise StorageError(f"could not initialize sqlite store: {exc}") from exc

    def schema_info(self) -> SchemaInfo:
        """Read schema metadata without creating a database file."""

        if not self.database_path.exists():
            return SchemaInfo(False, 0, (), self.database_path)
        with self._connection() as connection:
            return self._schema_info_from_connection(connection)

    def check(self) -> dict[str, object]:
        """Verify SQLite responds and has the required connection pragmas."""

        with self._connection() as connection:
            sqlite_ok = connection.execute("SELECT 1").fetchone()[0] == 1
            foreign_keys = int(connection.execute("PRAGMA foreign_keys").fetchone()[0]) == 1
            busy_timeout = int(connection.execute("PRAGMA busy_timeout").fetchone()[0])
            return {
                "sqlite": sqlite_ok,
                "foreign_keys": foreign_keys,
                "busy_timeout": busy_timeout == self.busy_timeout_ms,
            }

    def _schema_info_from_connection(self, connection: sqlite3.Connection) -> SchemaInfo:
        exists = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'schema_migrations'"
        ).fetchone()
        if exists is None:
            return SchemaInfo(False, 0, (), self.database_path)
        rows = connection.execute(
            "SELECT version FROM schema_migrations ORDER BY version"
        ).fetchall()
        versions = tuple(int(row[0]) for row in rows)
        return SchemaInfo(
            bool(versions), versions[-1] if versions else 0, versions, self.database_path
        )


def _migration_one(connection: sqlite3.Connection) -> None:
    """Stage 01 intentionally has no domain tables."""


def _validate_applied_versions(applied: set[int], known_versions: tuple[int, ...]) -> None:
    ordered_applied = tuple(sorted(applied))
    expected_prefix = known_versions[: len(ordered_applied)]
    if ordered_applied != expected_prefix:
        versions = ", ".join(str(version) for version in ordered_applied) or "none"
        raise StorageError(f"unsupported sqlite schema versions: {versions}")


__all__ = ["CURRENT_SCHEMA_VERSION", "SQLiteStateStore"]
