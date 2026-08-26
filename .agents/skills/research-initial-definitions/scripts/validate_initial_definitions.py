#!/usr/bin/env python3
"""Validate the structural contract of research-initial-definitions.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Context",
    "Purpose",
    "Research Question (Can be refined)",
    "Confirmed Product Constraints",
    "Current Evidence Baseline",
    "Known Gaps",
]


def resolve_artifact(raw: str) -> Path:
    candidate = Path(raw)
    if candidate.is_dir() or candidate.name != "research-initial-definitions.md":
        candidate = candidate / "research-initial-definitions.md"
    return candidate.resolve()


def resolve_layout(path: Path, repo_root: Path) -> tuple[Path | None, Path | None, list[str]]:
    errors: list[str] = []
    working_folder = path.parent.resolve()
    repository_root = repo_root.resolve()

    if not repository_root.is_dir():
        errors.append(f"repository root is not a directory: {repository_root}")
        return None, None, errors

    try:
        relative = working_folder.relative_to(repository_root)
    except ValueError:
        errors.append("working folder must be inside repository root")
        return None, None, errors

    research_positions = [
        index for index, part in enumerate(relative.parts) if part == "research"
    ]
    if not research_positions:
        errors.append("working folder must be beneath a directory literally named 'research'")
        return working_folder, None, errors

    position = research_positions[-1]
    research_root = repository_root.joinpath(*relative.parts[: position + 1])
    if position == len(relative.parts) - 1:
        errors.append("working folder must identify one research beneath the shared research directory")

    return working_folder, research_root, errors


def validate(path: Path, repo_root: Path) -> dict[str, object]:
    errors: list[str] = []
    repository_root = repo_root.resolve()
    working_folder, research_root, location_errors = resolve_layout(path, repository_root)
    errors.extend(location_errors)

    if not path.is_file():
        return {
            "status": "block",
            "repository_root": str(repository_root),
            "research_root": str(research_root) if research_root else None,
            "working_folder": str(working_folder) if working_folder else str(path.parent.resolve()),
            "artifact": str(path),
            "sha256": None,
            "sections": [],
            "errors": [*errors, "missing research-initial-definitions.md"],
        }

    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "status": "block",
            "repository_root": str(repository_root),
            "research_root": str(research_root) if research_root else None,
            "working_folder": str(working_folder) if working_folder else str(path.parent.resolve()),
            "artifact": str(path),
            "sha256": None,
            "sections": [],
            "errors": [*errors, f"cannot read UTF-8 artifact: {exc}"],
        }

    h1 = re.findall(r"^#\s+(.+?)\s*$", text, flags=re.MULTILINE)
    if len(h1) != 1 or not h1[0].startswith("Research Initial Definitions"):
        errors.append("expected one H1 beginning with 'Research Initial Definitions'")

    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    sections = [match.group(1) for match in matches]
    if sections != REQUIRED_SECTIONS:
        errors.append(
            "level-two sections must be exactly, once, and in order: "
            + " | ".join(REQUIRED_SECTIONS)
        )

    if sections == REQUIRED_SECTIONS:
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            if not text[start:end].strip():
                errors.append(f"section is empty: {sections[index]}")

    return {
        "status": "pass" if not errors else "block",
        "repository_root": str(repository_root),
        "research_root": str(research_root) if research_root else None,
        "working_folder": str(working_folder) if working_folder else str(path.parent.resolve()),
        "artifact": str(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sections": sections,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Research folder or research-initial-definitions.md")
    parser.add_argument(
        "--repo-root",
        required=True,
        help="Absolute or relative root of the repository containing the research tree",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    result = validate(resolve_artifact(args.path), Path(args.repo_root))
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result["status"] == "pass":
        print(f"PASS {result['artifact']} sha256={result['sha256']}")
    else:
        print(f"BLOCK {result['artifact']}", file=sys.stderr)
        for error in result["errors"]:
            print(f"- {error}", file=sys.stderr)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
