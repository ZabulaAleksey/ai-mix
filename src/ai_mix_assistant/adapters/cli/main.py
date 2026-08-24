"""The small, stable command-line interface for stage 01."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Sequence
from typing import Any

from ai_mix_assistant.application.config import AppConfig, ConfigurationError
from ai_mix_assistant.application.ports import StorageError
from ai_mix_assistant.application.services import SystemStatusService
from ai_mix_assistant.logging_config import configure_logging

from ..storage.sqlite import SQLiteStateStore

EXIT_OK = 0
EXIT_RUNTIME_ERROR = 1
EXIT_USAGE_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-mix", description="AI Mix Assistant local status checks"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("info", "health"):
        subparser = subparsers.add_parser(command, help=f"show {command} information")
        subparser.add_argument("--json", action="store_true", dest="as_json", help="emit JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        # argparse already printed a useful usage message. Preserve its conventional code.
        return exc.code if isinstance(exc.code, int) else EXIT_USAGE_ERROR

    try:
        config = AppConfig.from_env()
        configure_logging(config.log_level)
        store = SQLiteStateStore(config.database_path, config.busy_timeout_ms)
        service = SystemStatusService(config, store)
        if args.command == "info":
            payload: dict[str, Any] = service.info()
            exit_code = EXIT_OK
        else:
            report = service.health()
            payload = report.as_dict()
            exit_code = EXIT_OK if report.ok else EXIT_RUNTIME_ERROR
    except ConfigurationError as exc:
        payload = {"status": "error", "error": {"type": "configuration", "message": str(exc)}}
        exit_code = EXIT_USAGE_ERROR
    except (StorageError, OSError) as exc:
        logging.getLogger(__name__).debug("local state operation failed")
        payload = {"status": "error", "error": {"type": "runtime", "message": str(exc)}}
        exit_code = EXIT_RUNTIME_ERROR

    if args.as_json:
        print(json.dumps(payload, sort_keys=True, ensure_ascii=True))
    else:
        _print_text(args.command, payload)
    return exit_code


def _print_text(command: str, payload: dict[str, Any]) -> None:
    if payload.get("status") == "error":
        error = payload.get("error", {})
        print(f"error: {error.get('message', 'unknown error')}", file=sys.stderr)
        return
    if command == "info":
        application = payload["application"]
        backend = payload["backend"]
        schema = payload["schema"]
        print(f"application: {application['name']} {application['version']}")
        print(f"python: {payload['python']['version']}")
        print(f"backend: {backend['kind']}")
        print(f"database: {backend['database_path']}")
        print(f"schema: {'initialized' if schema['initialized'] else 'uninitialized'}")
        return
    print(f"health: {payload.get('status', 'error')}")
    checks = payload.get("checks", {})
    for name, value in checks.items():
        print(f"{name}: {'ok' if value is True else 'failed'}")
