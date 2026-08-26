#!/usr/bin/env python3
"""Validate and append one usage event to a JSONL observability ledger."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "usage-event.schema.yml"


def load_event(path: str) -> dict[str, Any]:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("usage event must be a JSON object")
    return value


@contextmanager
def ledger_lock(ledger: Path, timeout_seconds: float = 10.0):
    lock_path = ledger.with_suffix(ledger.suffix + ".lock")
    handle = lock_path.open("a+b")
    if lock_path.stat().st_size == 0:
        handle.write(b"0")
        handle.flush()
    deadline = time.monotonic() + timeout_seconds
    acquired = False
    try:
        while not acquired:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"timed out acquiring telemetry lock: {lock_path}")
                time.sleep(0.05)
        yield
    finally:
        if acquired:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def append_all(ledger: Path, line: bytes) -> None:
    with ledger_lock(ledger):
        descriptor = os.open(ledger, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            written = 0
            while written < len(line):
                count = os.write(descriptor, line[written:])
                if count <= 0:
                    raise OSError("telemetry append made no progress")
                written += count
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--event", required=True, help="JSON event path, or - for stdin")
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    try:
        event = load_event(args.event)
        schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
        errors = sorted(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(event),
            key=lambda item: list(item.absolute_path),
        )
        if errors:
            for error in errors:
                locator = ".".join(str(item) for item in error.absolute_path) or "<root>"
                print(f"USAGE_EVENT=block\nERROR: {locator}: {error.message}")
            return 1
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        line = (json.dumps(event, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
        append_all(args.ledger, line)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        print(f"USAGE_EVENT=block\nERROR: {exc}")
        return 1
    print("USAGE_EVENT=appended")
    print(f"LEDGER={args.ledger.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
