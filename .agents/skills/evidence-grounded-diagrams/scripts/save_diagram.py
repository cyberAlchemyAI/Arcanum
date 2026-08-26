#!/usr/bin/env python3
"""Validate and save one minimal Mermaid diagram."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


SKILL_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_ROOT / "schemas" / "diagram.schema.json"
MERMAID_CLI_PACKAGE = "@mermaid-js/mermaid-cli@11.12.0"


def load_metadata(path: Path) -> dict[str, object]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("diagram.yml must contain a YAML object")
    return value


def validate_metadata(metadata: dict[str, object]) -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(metadata), key=lambda item: list(item.absolute_path))
    ]

    diagram_id = metadata.get("id")
    created_at = metadata.get("created_at")
    if isinstance(diagram_id, str) and isinstance(created_at, str):
        if diagram_id[:8] != created_at.replace("-", ""):
            errors.append("id date prefix must match created_at")
    return errors


def render_mermaid(source: Path, output: Path) -> None:
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if npx is None:
        raise RuntimeError("npx is required to render diagram.png")
    result = subprocess.run(
        [
            npx,
            "--yes",
            MERMAID_CLI_PACKAGE,
            "-i",
            str(source),
            "-o",
            str(output),
            "-b",
            "white",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"Mermaid rendering failed: {detail}")
    payload = output.read_bytes() if output.is_file() else b""
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError("Mermaid renderer did not produce a valid PNG")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata", type=Path, help="Path to the draft diagram.yml")
    parser.add_argument("source", type=Path, help="Path to the draft diagram.mmd")
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=Path.cwd(),
        help="Workspace containing output/diagrams (default: current directory)",
    )
    args = parser.parse_args()

    try:
        metadata_path = args.metadata.resolve(strict=True)
        source_path = args.source.resolve(strict=True)
        metadata = load_metadata(metadata_path)
        errors = validate_metadata(metadata)
        source = source_path.read_text(encoding="utf-8")
        if not source.strip():
            errors.append("diagram.mmd must not be empty")
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1

        workspace_root = args.workspace_root.resolve(strict=True)
        output_root = workspace_root / "output" / "diagrams"
        output_root.mkdir(parents=True, exist_ok=True)
        destination = output_root / str(metadata["id"])
        if destination.exists():
            print(f"ERROR: destination already exists: {destination}", file=sys.stderr)
            return 1

        staging = Path(tempfile.mkdtemp(prefix=".saving-", dir=output_root))
        try:
            shutil.copyfile(metadata_path, staging / "diagram.yml")
            shutil.copyfile(source_path, staging / "diagram.mmd")
            render_mermaid(staging / "diagram.mmd", staging / "diagram.png")
            staging.rename(destination)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise

        print(f"DIAGRAM_SAVED={destination}")
        return 0
    except (OSError, UnicodeError, ValueError, RuntimeError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
