#!/usr/bin/env python3
"""Check runtime prerequisites before invoking diagram package scripts."""

from __future__ import annotations

import importlib
import sys
from importlib import metadata


REQUIREMENTS = {
    "yaml": ("PyYAML", (6, 0)),
    "jsonschema": ("jsonschema", (4, 18)),
}


def version_tuple(value: str) -> tuple[int, ...]:
    parts: list[int] = []
    for token in value.split("."):
        digits = "".join(character for character in token if character.isdigit())
        if not digits:
            break
        parts.append(int(digits))
    return tuple(parts)


def main() -> int:
    failures: list[str] = []
    if sys.version_info < (3, 10):
        failures.append(f"Python 3.10+ required; found {sys.version.split()[0]}")
    for module_name, (distribution, minimum) in REQUIREMENTS.items():
        try:
            importlib.import_module(module_name)
            installed = metadata.version(distribution)
        except (ImportError, metadata.PackageNotFoundError):
            failures.append(f"missing Python dependency: {distribution}")
            continue
        if version_tuple(installed) < minimum:
            expected = ".".join(map(str, minimum))
            failures.append(f"{distribution}>={expected} required; found {installed}")
    if failures:
        print("RUNTIME_PREFLIGHT=block")
        for failure in failures:
            print(f"BLOCK: {failure}")
        print("FIX: python -m pip install -r requirements.txt")
        return 1
    print("RUNTIME_PREFLIGHT=pass")
    print(f"PYTHON={sys.version.split()[0]}")
    for _, (distribution, _) in REQUIREMENTS.items():
        print(f"{distribution}={metadata.version(distribution)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
