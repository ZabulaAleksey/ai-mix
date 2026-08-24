import sqlite3
from pathlib import Path

import pytest

from ai_mix_assistant.adapters.storage.sqlite import SQLiteStateStore
from ai_mix_assistant.application.ports import StorageError


def test_sqlite_migration_is_idempotent_and_only_metadata(tmp_path: Path) -> None:
    database = tmp_path / "state.sqlite3"
    store = SQLiteStateStore(database)

    before = store.schema_info()
    first = store.initialize()
    second = store.initialize()

    assert before.initialized is False
    assert first.current_version == second.current_version == 1
    assert first.applied_versions == second.applied_versions == (1,)
    with sqlite3.connect(database) as connection:
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }
    assert tables == {"schema_migrations"}


def test_sqlite_health_check_is_repeatable(tmp_path: Path) -> None:
    store = SQLiteStateStore(tmp_path / "state.sqlite3", busy_timeout_ms=3210)

    store.initialize()
    first = store.check()
    second = store.check()

    assert first == second == {"sqlite": True, "foreign_keys": True, "busy_timeout": True}


def test_sqlite_initialization_reports_invalid_parent(tmp_path: Path) -> None:
    parent_file = tmp_path / "not-a-directory"
    parent_file.write_text("occupied", encoding="utf-8")
    store = SQLiteStateStore(parent_file / "state.sqlite3")

    with pytest.raises(StorageError):
        store.initialize()


def test_sqlite_rejects_an_unknown_future_schema(tmp_path: Path) -> None:
    database = tmp_path / "state.sqlite3"
    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)"
        )
        connection.execute(
            "INSERT INTO schema_migrations(version, applied_at) VALUES (99, 'future')"
        )

    store = SQLiteStateStore(database)
    with pytest.raises(StorageError, match="unsupported sqlite schema versions: 99"):
        store.initialize()
