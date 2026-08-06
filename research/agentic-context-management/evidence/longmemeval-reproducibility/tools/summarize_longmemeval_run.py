#!/usr/bin/env python3
"""Render a deterministic Markdown summary from validated ACM OR1 JSONL data."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from validate_longmemeval_jsonl import CATEGORY_ORDER, validate_file


def render(path: Path) -> str:
    rows, errors = validate_file(path)
    if errors:
        details = "\n".join(f"  - {error}" for error in errors)
        raise ValueError(f"input failed validation:\n{details}")
    manifest = rows[0]
    summary = rows[-1]
    evidence_class = manifest["evidence_class"]
    deviations = sum(len(row["protocol_deviations"]) for row in rows)
    lines = [
        "# Result Summary: `ACM-OR1-LME-REPRO`",
        "",
        f"Run data: `{path.as_posix()}`",
        "",
        f"Evidence class: `{evidence_class}`",
        "",
        "## Integrity",
        "",
        "| Check | Decision | Evidence |",
        "| --- | --- | --- |",
        f"| Schema and cross-row validation | pass | {len(rows)} contiguous rows validated. |",
        f"| Required metadata | pass | Run `{manifest['run_id']}` has one manifest and one summary. |",
        f"| Protocol deviations | {'pass' if deviations == 0 else 'flag'} | {deviations} deviation(s) recorded. |",
        "| Append-only shape | pass | One run, contiguous indices, unique question IDs, summary last. |",
        "",
        "## Metrics",
        "",
        "| Metric | Value | Interpretation |",
        "| --- | --- | --- |",
        f"| question count | {summary['question_count']} | Validated question-result rows. |",
        f"| correct count | {summary['correct_count']} | Rows whose binary judge verdict is `CORRECT`. |",
        f"| overall accuracy | {summary['accuracy']:.3f} | Fixture arithmetic only. |",
    ]
    for category in CATEGORY_ORDER:
        result = summary["category_results"].get(category)
        if result:
            lines.append(
                f"| `{category}` | {result['correct_count']}/{result['question_count']} ({result['accuracy']:.3f}) | Category fixture slice. |"
            )
    lines.extend(
        [
            "",
            "## Success Criteria",
            "",
            "| Criteria ID | Target | Decision | Notes |",
            "| --- | --- | --- | --- |",
            "| fixture-positive | Passing fixture validates | pass | Schema, metadata, sequence, and metrics accepted. |",
            "| evidence-boundary | Raw or fixture evidence cannot update claim status | pass | Every row has `claim_status_update_allowed=false`. |",
            "| live-adjudication | 500 official questions plus resolved published-run pin | blocked | Synthetic fixture intentionally does not satisfy live requirements. |",
            "",
            "## Claim Impact",
            "",
            "Claim status update allowed: no",
            "",
            "Recommendation: Do not update C10 or the tower's evidence status. Use this summary only as dry-run fixture-readiness evidence.",
            "",
            "## Remaining Blockers",
            "",
            "- exact published-run harness revision;",
            "- reconciliation of the public 50-versus-500 question mismatch;",
            "- original or independently generated per-question artifacts;",
            "- live credentials, cost authorization, and an admitted execution unit.",
            "",
            "## Next Step",
            "",
            "1. Defer live execution until an approved task-session owns the pinned protocol, credentials, cost, and raw-artifact capture.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args()
    try:
        sys.stdout.write(render(args.jsonl))
    except (OSError, ValueError) as exc:
        print(f"FAIL {args.jsonl}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
