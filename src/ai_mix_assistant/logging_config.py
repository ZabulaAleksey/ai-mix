"""Logging setup kept at the composition root."""

from __future__ import annotations

import logging
import sys
from typing import TextIO


def configure_logging(level: str = "INFO", stream: TextIO | None = None) -> None:
    """Configure concise stderr logging without media payloads or tracebacks."""

    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"unknown log level: {level}")
    logging.basicConfig(
        level=numeric_level,
        format="%(levelname)s %(name)s: %(message)s",
        stream=stream or sys.stderr,
        force=True,
    )
