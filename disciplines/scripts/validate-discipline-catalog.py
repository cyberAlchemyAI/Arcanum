#!/usr/bin/env python3
"""Validate the discipline catalog's basic structure and local links."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "disciplines" / "DISCIPLINES.md"
REQUIRED_COLUMNS = ["ID", "Discipline", "Status", "Steward", "Evidence", "Next hardening move"]
VALID_STATUSES = {"candidate", "active-pattern", "implemented", "canonical", "deprecated"}


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_links(cell: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", cell)


def resolve_link(markdown_path: Path, link: str) -> Path:
    base = link.split("#", 1)[0]
    return (markdown_path.parent / base).resolve()


def main() -> int:
    text = CATALOG.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    try:
        header_index = next(
            idx for idx, line in enumerate(lines) if line.startswith("| ID | Discipline |")
        )
    except StopIteration:
        print("VALIDATION=block")
        print("BLOCK: catalog table header not found")
        return 1

    header = split_row(lines[header_index])
    if header != REQUIRED_COLUMNS:
        errors.append(f"catalog columns must be: {', '.join(REQUIRED_COLUMNS)}")

    row_count = 0
    seen_ids: set[str] = set()
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        cells = split_row(line)
        if len(cells) != len(REQUIRED_COLUMNS):
            errors.append(f"row has wrong column count: {line}")
            continue
        row_count += 1
        discipline_id = cells[0].strip("`")
        status = cells[2]
        evidence = cells[4]
        if not re.match(r"^[a-z][a-z0-9-]*$", discipline_id):
            errors.append(f"invalid discipline id: {discipline_id}")
        if discipline_id in seen_ids:
            errors.append(f"duplicate discipline id: {discipline_id}")
        seen_ids.add(discipline_id)
        if status not in VALID_STATUSES:
            errors.append(f"{discipline_id}: invalid status: {status}")
        links = extract_links(evidence)
        if not links:
            errors.append(f"{discipline_id}: evidence cell must include a local Markdown link")
        for link in links:
            if link.startswith(("http://", "https://", "mailto:")):
                errors.append(f"{discipline_id}: evidence link must be local: {link}")
                continue
            target = resolve_link(CATALOG, link)
            if not target.exists():
                errors.append(f"{discipline_id}: missing evidence target: {link}")

    if row_count == 0:
        errors.append("catalog table has no rows")

    if errors:
        print("VALIDATION=block")
        for error in errors:
            print(f"BLOCK: {error}")
        return 1

    print("VALIDATION=pass")
    print(f"CATALOG={CATALOG.relative_to(ROOT)}")
    print(f"DISCIPLINE_COUNT={row_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
