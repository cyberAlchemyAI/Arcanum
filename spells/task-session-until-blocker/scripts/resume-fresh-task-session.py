#!/usr/bin/env python3
"""Admit a fresh Task Session from one prerequisite-resume request."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from fresh_session_resume import admit_fresh_task_session


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--repository-root", default=Path.cwd(), type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    request = json.loads(arguments.input.read_text(encoding="utf-8"))
    receipt = admit_fresh_task_session(request, arguments.repository_root)
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["decision"] == "start-fresh-session" else 2


if __name__ == "__main__":
    raise SystemExit(main())
