import json
from pathlib import Path

from ai_mix_assistant.adapters.cli import main


def test_info_json_is_read_only(tmp_path: Path, monkeypatch, capsys) -> None:
    database = tmp_path / "state.sqlite3"
    monkeypatch.setenv("AI_MIX_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AI_MIX_DATABASE_PATH", str(database))

    assert main(["info", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert payload["schema"]["initialized"] is False
    assert not database.exists()


def test_info_text_contract_is_read_only(tmp_path: Path, monkeypatch, capsys) -> None:
    database = tmp_path / "state.sqlite3"
    monkeypatch.setenv("AI_MIX_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AI_MIX_DATABASE_PATH", str(database))

    assert main(["info"]) == 0
    captured = capsys.readouterr()
    assert "application: ai-mix-assistant 0.1.0" in captured.out
    assert "backend: sqlite" in captured.out
    assert "schema: uninitialized" in captured.out
    assert captured.err == ""
    assert not database.exists()


def test_health_json_initializes_and_is_idempotent(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.setenv("AI_MIX_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AI_MIX_DATABASE_PATH", str(tmp_path / "data" / "state.sqlite3"))

    assert main(["health", "--json"]) == 0
    first = json.loads(capsys.readouterr().out)
    assert main(["health", "--json"]) == 0
    second = json.loads(capsys.readouterr().out)
    assert first["status"] == second["status"] == "ok"
    assert first["schema"]["applied_versions"] == second["schema"]["applied_versions"] == [1]


def test_cli_text_contract_and_configuration_exit_code(monkeypatch, capsys) -> None:
    monkeypatch.setenv("AI_MIX_DATA_DIR", "")
    assert main(["health"]) == 2
    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "Traceback" not in captured.err


def test_runtime_error_does_not_expose_traceback_in_debug_mode(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    database_directory = tmp_path / "database-directory"
    database_directory.mkdir()
    monkeypatch.setenv("AI_MIX_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.setenv("AI_MIX_DATABASE_PATH", str(database_directory))
    monkeypatch.setenv("AI_MIX_LOG_LEVEL", "DEBUG")

    assert main(["health"]) == 1
    captured = capsys.readouterr()
    assert "error:" in captured.err
    assert "Traceback" not in captured.err
