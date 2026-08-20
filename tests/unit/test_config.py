from pathlib import Path

import pytest

from ai_mix_assistant.application.config import AppConfig, ConfigurationError


def test_config_resolves_paths_and_defaults_database_under_data_dir(tmp_path: Path) -> None:
    config = AppConfig.from_env({"AI_MIX_DATA_DIR": str(tmp_path / "data")})
    assert config.data_dir == (tmp_path / "data").resolve()
    assert config.database_path == (tmp_path / "data" / "state.sqlite3").resolve()
    assert config.log_level == "INFO"


@pytest.mark.parametrize(
    "environment",
    [
        {"AI_MIX_DATA_DIR": ""},
        {"AI_MIX_LOG_LEVEL": "verbose"},
        {"AI_MIX_BUSY_TIMEOUT_MS": "zero"},
        {"AI_MIX_BUSY_TIMEOUT_MS": "0"},
    ],
)
def test_config_rejects_invalid_environment(environment: dict[str, str]) -> None:
    with pytest.raises(ConfigurationError):
        AppConfig.from_env(environment)
