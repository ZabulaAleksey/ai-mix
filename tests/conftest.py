"""Pytest runtime isolation for the workspace sandbox."""

import os
import shutil
from pathlib import Path
from uuid import uuid4

import pytest

_BASE_TEMP: Path | None = None


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Give every invocation an isolated, repository-local temporary directory."""
    global _BASE_TEMP
    basetemp = Path.cwd() / f".pytest_tmp-{os.getpid()}-{uuid4().hex}"
    _BASE_TEMP = basetemp
    config.option.basetemp = str(basetemp)


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config: pytest.Config) -> None:
    """Remove this invocation's temporary directory after plugins release files."""
    del config
    if _BASE_TEMP is not None:
        shutil.rmtree(_BASE_TEMP, ignore_errors=True)
