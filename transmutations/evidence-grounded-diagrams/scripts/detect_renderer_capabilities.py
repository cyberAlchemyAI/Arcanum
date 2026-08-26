#!/usr/bin/env python3
"""Report local structural-diagram renderer capabilities without substitution."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from typing import Any


TOOLS = {
    "mermaid": ("mmdc", ["--version"]),
    "graphviz": ("dot", ["-V"]),
    "plantuml": ("plantuml", ["-version"]),
}


def inspect(executable: str, version_args: list[str]) -> dict[str, Any]:
    path = shutil.which(executable)
    if path is None:
        return {"available": False, "executable": executable, "path": None, "version": None}
    version: str | None = None
    try:
        result = subprocess.run(
            [path, *version_args],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
        version = (result.stdout or result.stderr).strip().splitlines()[0] or None
    except (OSError, subprocess.SubprocessError, IndexError):
        version = None
    return {"available": True, "executable": executable, "path": path, "version": version}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    capabilities = {
        name: inspect(executable, version_args)
        for name, (executable, version_args) in TOOLS.items()
    }
    if args.json:
        print(json.dumps(capabilities, indent=2, ensure_ascii=False))
    else:
        for name, record in capabilities.items():
            state = "available" if record["available"] else "unavailable"
            detail = f" ({record['version']})" if record["version"] else ""
            print(f"{name}: {state}{detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
