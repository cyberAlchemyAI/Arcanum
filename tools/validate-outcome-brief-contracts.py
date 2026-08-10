#!/usr/bin/env python3
"""Validate the Outcome Brief pilot contracts and generated projections."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


OUTCOME = "## Outcome Brief"
BOUNDARY = "## Boundary and Next Decision"
TECHNICAL = "## Technical Details"
OUTCOME_FIELDS = ("- Objective:", "- Result:", "- Why it matters:")
BOUNDARY_FIELDS = (
    "- Changed:",
    "- Unchanged:",
    "- Open questions:",
    "- User decision:",
    "- Next action:",
)


@dataclass(frozen=True)
class ContractCheck:
    path: str
    detail_headings: tuple[str, ...]
    expected_sequences: int = 1


CANONICAL_CHECKS = (
    ContractCheck("spells/invoke/README.md", ("## Invoke Result",)),
    ContractCheck("spells/invoke/define.md", ("## Invoke Result",)),
    ContractCheck("spells/invoke/design.md", ("## Invoke Result",)),
    ContractCheck("spells/invoke/plan.md", ("## Invoke Result",)),
    ContractCheck("spells/invoke/handoff.md", ("## Invoke Validation Fixture Result",)),
    ContractCheck("spells/invoke/refresh.md", ("## Invoke Validation Fixture Result",)),
    ContractCheck(
        "arcana/refine/SKILL.md",
        ("## Refine Run Strategy Proposal", "## Refine Result"),
        expected_sequences=2,
    ),
    ContractCheck("arcana/refine/templates/result.md", ("# Refine Result",)),
    ContractCheck("arcana/task-session/SKILL.md", ("## Task Session Result",)),
)


GENERATED_CHECKS = (
    ContractCheck(".agents/skills/invoke/SKILL.md", ("## Invoke Result",)),
    ContractCheck(".agents/skills/invoke/define.md", ("## Invoke Result",)),
    ContractCheck(".agents/skills/invoke/design.md", ("## Invoke Result",)),
    ContractCheck(".agents/skills/invoke/plan.md", ("## Invoke Result",)),
    ContractCheck(
        ".agents/skills/invoke/handoff.md", ("## Invoke Validation Fixture Result",)
    ),
    ContractCheck(
        ".agents/skills/invoke/refresh.md", ("## Invoke Validation Fixture Result",)
    ),
    ContractCheck(
        ".agents/skills/refine/SKILL.md",
        ("## Refine Run Strategy Proposal", "## Refine Result"),
        expected_sequences=2,
    ),
    ContractCheck(".agents/skills/refine/templates/result.md", ("# Refine Result",)),
    ContractCheck(".agents/skills/task-session/SKILL.md", ("## Task Session Result",)),
    ContractCheck(".claude/skills/invoke/SKILL.md", ("## Invoke Result",)),
    ContractCheck(".claude/skills/invoke/define.md", ("## Invoke Result",)),
    ContractCheck(".claude/skills/invoke/design.md", ("## Invoke Result",)),
    ContractCheck(".claude/skills/invoke/plan.md", ("## Invoke Result",)),
    ContractCheck(
        ".claude/skills/invoke/handoff.md", ("## Invoke Validation Fixture Result",)
    ),
    ContractCheck(
        ".claude/skills/invoke/refresh.md", ("## Invoke Validation Fixture Result",)
    ),
    ContractCheck(
        ".claude/skills/refine/SKILL.md",
        ("## Refine Run Strategy Proposal", "## Refine Result"),
        expected_sequences=2,
    ),
    ContractCheck(".claude/skills/refine/templates/result.md", ("# Refine Result",)),
    ContractCheck(".claude/skills/task-session/SKILL.md", ("## Task Session Result",)),
)


def occurrences(text: str, needle: str) -> list[int]:
    positions: list[int] = []
    start = 0
    while True:
        index = text.find(needle, start)
        if index < 0:
            return positions
        positions.append(index)
        start = index + len(needle)


def validate_contract(path: Path, check: ContractCheck) -> list[str]:
    if not path.is_file():
        return [f"{check.path}: missing file"]

    text = path.read_text(encoding="utf-8")
    outcome_positions = occurrences(text, OUTCOME)
    errors: list[str] = []

    if len(outcome_positions) != check.expected_sequences:
        errors.append(
            f"{check.path}: expected {check.expected_sequences} Outcome Brief "
            f"sequence(s), found {len(outcome_positions)}"
        )
        return errors

    if len(check.detail_headings) != check.expected_sequences:
        errors.append(f"{check.path}: validator configuration has mismatched headings")
        return errors

    for index, (outcome_at, detail_heading) in enumerate(
        zip(outcome_positions, check.detail_headings), start=1
    ):
        next_outcome = (
            outcome_positions[index] if index < len(outcome_positions) else len(text)
        )
        boundary_at = text.find(BOUNDARY, outcome_at + len(OUTCOME), next_outcome)
        technical_at = text.find(
            TECHNICAL,
            boundary_at + len(BOUNDARY) if boundary_at >= 0 else outcome_at,
            next_outcome,
        )
        detail_at = text.find(
            detail_heading,
            technical_at + len(TECHNICAL) if technical_at >= 0 else outcome_at,
            next_outcome,
        )

        prefix = f"{check.path}: sequence {index}"
        if boundary_at < 0:
            errors.append(f"{prefix}: missing Boundary and Next Decision")
            continue
        if technical_at < 0:
            errors.append(f"{prefix}: missing Technical Details")
            continue
        if detail_at < 0:
            errors.append(f"{prefix}: missing preserved heading {detail_heading!r}")
            continue
        if not outcome_at < boundary_at < technical_at < detail_at:
            errors.append(f"{prefix}: required section order is not preserved")
            continue

        outcome_segment = text[outcome_at:boundary_at]
        boundary_segment = text[boundary_at:technical_at]
        for field in OUTCOME_FIELDS:
            if field not in outcome_segment:
                errors.append(f"{prefix}: missing outcome field {field!r}")
        for field in BOUNDARY_FIELDS:
            if field not in boundary_segment:
                errors.append(f"{prefix}: missing boundary field {field!r}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--arcanum-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="canonical Arcanum repository root",
    )
    parser.add_argument(
        "--consumer-root",
        type=Path,
        default=None,
        help="consuming repository root containing .agents and .claude projections",
    )
    parser.add_argument(
        "--canonical-only",
        action="store_true",
        help="skip generated projection checks",
    )
    args = parser.parse_args()

    arcanum_root = args.arcanum_root.resolve()
    consumer_root = (
        args.consumer_root.resolve()
        if args.consumer_root is not None
        else arcanum_root.parent
    )

    errors: list[str] = []
    framework_contract = arcanum_root / "framework/OUTCOME-BRIEF-CONTRACT.md"
    framework_index = arcanum_root / "framework/README.md"
    if not framework_contract.is_file():
        errors.append("framework/OUTCOME-BRIEF-CONTRACT.md: missing file")
    if not framework_index.is_file() or "OUTCOME-BRIEF-CONTRACT.md" not in framework_index.read_text(
        encoding="utf-8"
    ):
        errors.append("framework/README.md: missing Outcome Brief Contract index entry")

    for check in CANONICAL_CHECKS:
        errors.extend(validate_contract(arcanum_root / check.path, check))

    if not args.canonical_only:
        for check in GENERATED_CHECKS:
            errors.extend(validate_contract(consumer_root / check.path, check))

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        print(f"Outcome Brief contract validation: block ({len(errors)} error(s))")
        return 1

    checked = len(CANONICAL_CHECKS)
    if not args.canonical_only:
        checked += len(GENERATED_CHECKS)
    print(f"Outcome Brief contract validation: pass ({checked} contract files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
