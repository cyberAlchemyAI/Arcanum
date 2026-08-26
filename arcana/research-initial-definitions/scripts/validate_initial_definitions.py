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
    "Research Questions (Can be refined)",
    "Confirmed Product Constraints",
    "Current Evidence Baseline",
    "Known Gaps",
]

FENCE_START = re.compile(r"^[ ]{0,3}(`{3,}|~{3,}).*$")
PROGRAM_QUESTION = re.compile(r"^\*\*(RQ-00)\.\*\*\s+(.+\?)\s*$")
SUPPORTING_QUESTION = re.compile(
    r"^(\d+)\.\s+\*\*(RQ-(\d{2,}))\.\*\*\s+(.+\?)\s*$"
)


def mask_fenced_code_blocks(text: str) -> str:
    """Replace fenced code with spaces while preserving offsets and line endings."""
    output: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        ending = line[len(content) :]

        if fence_character is None:
            opening = FENCE_START.match(content)
            if opening:
                marker = opening.group(1)
                fence_character = marker[0]
                fence_length = len(marker)
                output.append(" " * len(content) + ending)
            else:
                output.append(line)
            continue

        closing = re.match(
            rf"^[ ]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
            content,
        )
        output.append(" " * len(content) + ending)
        if closing:
            fence_character = None
            fence_length = 0

    return "".join(output)


def validate_research_questions(section: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    identifiers: list[str] = []
    headings = list(re.finditer(r"^###\s+(.+?)\s*$", section, flags=re.MULTILINE))
    titles = [heading.group(1) for heading in headings]

    if titles.count("Program question") != 1:
        errors.append("Research Questions must contain exactly one '### Program question'")
    if not titles or titles[0] != "Program question":
        errors.append("'### Program question' must be the first level-three heading")
    if len(headings) < 2:
        errors.append("Research Questions must contain at least one thematic heading")
        return errors, identifiers
    if len(set(titles[1:])) != len(titles[1:]):
        errors.append("thematic headings in Research Questions must be unique")

    program_region = section[headings[0].end() : headings[1].start()]
    program_lines = [line.strip() for line in program_region.splitlines() if line.strip()]
    if len(program_lines) != 1:
        errors.append("Program question must contain exactly one non-empty question line")
    else:
        program_match = PROGRAM_QUESTION.fullmatch(program_lines[0])
        if not program_match:
            errors.append("Program question must use '**RQ-00.** <question ending in ?>'")
        else:
            identifiers.append(program_match.group(1))

    supporting: list[tuple[int, str, int]] = []
    for index, heading in enumerate(headings[1:], start=1):
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(section)
        lines = [line.strip() for line in section[start:end].splitlines() if line.strip()]
        if not lines:
            errors.append(f"thematic heading has no supporting questions: {titles[index]}")
            continue
        for line in lines:
            match = SUPPORTING_QUESTION.fullmatch(line)
            if not match:
                errors.append(
                    "supporting questions must use "
                    "'<n>. **RQ-<nn>.** <question ending in ?>'"
                )
                continue
            supporting.append((int(match.group(1)), match.group(2), int(match.group(3))))

    for expected, (list_number, identifier, suffix) in enumerate(supporting, start=1):
        if list_number != expected or suffix != expected:
            errors.append(
                "supporting question numbers and RQ suffixes must be continuous and matching"
            )
            break
        identifiers.append(identifier)

    if len(identifiers) != len(set(identifiers)):
        errors.append("research question identifiers must be unique")

    return errors, identifiers


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
            "question_ids": [],
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
            "question_ids": [],
            "errors": [*errors, f"cannot read UTF-8 artifact: {exc}"],
        }

    visible_text = mask_fenced_code_blocks(text)
    h1 = re.findall(r"^#\s+(.+?)\s*$", visible_text, flags=re.MULTILINE)
    if len(h1) != 1 or not h1[0].startswith("Research Initial Definitions"):
        errors.append("expected one H1 beginning with 'Research Initial Definitions'")

    matches = list(re.finditer(r"^##\s+(.+?)\s*$", visible_text, flags=re.MULTILINE))
    sections = [match.group(1) for match in matches]
    if sections != REQUIRED_SECTIONS:
        errors.append(
            "level-two sections must be exactly, once, and in order: "
            + " | ".join(REQUIRED_SECTIONS)
        )

    if sections == REQUIRED_SECTIONS:
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(visible_text)
            if not visible_text[start:end].strip():
                errors.append(f"section is empty: {sections[index]}")

    question_ids: list[str] = []
    if sections == REQUIRED_SECTIONS:
        question_index = REQUIRED_SECTIONS.index("Research Questions (Can be refined)")
        question_start = matches[question_index].end()
        question_end = matches[question_index + 1].start()
        question_errors, question_ids = validate_research_questions(
            visible_text[question_start:question_end]
        )
        errors.extend(question_errors)

    return {
        "status": "pass" if not errors else "block",
        "repository_root": str(repository_root),
        "research_root": str(research_root) if research_root else None,
        "working_folder": str(working_folder) if working_folder else str(path.parent.resolve()),
        "artifact": str(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "sections": sections,
        "question_ids": question_ids,
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
