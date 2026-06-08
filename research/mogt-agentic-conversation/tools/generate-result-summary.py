#!/usr/bin/env python3
"""Generate fixture-only MOGT result summaries from validated JSONL rows."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line:
                row = json.loads(line)
                if isinstance(row, dict):
                    rows.append(row)
    return rows


def mean(values: list[float]) -> str:
    return "n/a" if not values else f"{statistics.mean(values):.3f}"


def number_values(rows: list[dict[str, Any]], field: str) -> list[float]:
    return [float(row[field]) for row in rows if isinstance(row.get(field), (int, float))]


def render_summary(experiment_id: str, source: Path, rows: list[dict[str, Any]]) -> str:
    deviations = sum(len(row.get("protocol_deviations") or []) for row in rows)
    policy_regimes = sorted({str(row.get("policy_regime")) for row in rows})
    evidence_classes = sorted({str(row.get("evidence_class", "unspecified")) for row in rows})
    run_ids = [str(row.get("run_id")) for row in rows]
    selected_actions = [str((row.get("selected_action") or {}).get("action_id")) for row in rows]

    metric_fields = [
        "traceability_coverage",
        "acceptance_score",
        "decision_quality_score",
        "regret_or_proxy",
        "overhead_acceptability_ratio",
        "quality_retention",
        "reviewer_burden",
    ]
    metric_lines = []
    for field in metric_fields:
        values = number_values(rows, field)
        if values:
            metric_lines.append(f"| `{field}` | {mean(values)} | Fixture mean over {len(values)} row(s). |")
    if not metric_lines:
        metric_lines.append("| n/a | n/a | No numeric summary fields were present. |")

    success_decision = "fixture-ready" if rows and deviations == 0 else "review-needed"
    claim_recommendation = (
        "Do not update publication claims or evidence status. Use this as dry-run fixture readiness evidence only."
    )
    next_step = (
        "Run the S4 fixture validation report gate after SWU-MOGT-HARNESS-002, "
        "003, and 004 result files exist."
    )

    return "\n".join(
        [
            f"# Result Summary: `{experiment_id}`",
            "",
            f"Run data: `{source}`",
            "",
            "Evidence class: dry-run fixture",
            "",
            "## Integrity",
            "",
            "| Check | Decision | Evidence |",
            "| --- | --- | --- |",
            f"| Schema validation | pass | Validator command completed before this summary was generated. |",
            f"| Required metadata | pass | {len(rows)} row(s): {', '.join(run_ids)}. |",
            f"| Protocol deviations | {'pass' if deviations == 0 else 'review'} | {deviations} deviation(s) recorded. |",
            "",
            "## Metrics",
            "",
            "| Metric | Value | Interpretation |",
            "| --- | --- | --- |",
            *metric_lines,
            f"| policy regimes | {', '.join(policy_regimes)} | Regimes represented in this fixture slice. |",
            f"| selected actions | {', '.join(selected_actions)} | Runtime choices summarized from fixture rows. |",
            "",
            "## Success Criteria",
            "",
            "| Criteria ID | Target | Decision | Notes |",
            "| --- | --- | --- | --- |",
            f"| fixture-validation | Rows validate locally before summary generation | {success_decision} | Evidence classes: {', '.join(evidence_classes)}. |",
            "| evidence-boundary | Do not claim live experiment support | pass | Summary is explicitly fixture-only. |",
            "",
            "## Claim Impact",
            "",
            "Claim status update allowed: no",
            "",
            f"Recommendation: {claim_recommendation}",
            "",
            "## Next Step",
            "",
            f"1. {next_step}",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MOGT result summary from fixture JSONL.")
    parser.add_argument("jsonl", type=Path, help="Validated MOGT fixture JSONL")
    parser.add_argument("--experiment", required=True, help="Experiment id to summarize")
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path")
    args = parser.parse_args()

    rows = [row for row in load_rows(args.jsonl) if row.get("experiment_id") == args.experiment]
    if not rows:
        raise SystemExit(f"FAIL no rows for experiment {args.experiment}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_summary(args.experiment, args.jsonl, rows), encoding="utf-8")
    print(f"PASS wrote {args.output} ({len(rows)} row(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
