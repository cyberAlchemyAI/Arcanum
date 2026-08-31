#!/usr/bin/env python3
"""Run the deterministic Define intent-completeness causal matrix twice."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from validate_semantic_intent import (
    build_complete_artifact,
    canonical_bytes,
    evaluate_artifact,
    load_object,
)


FIXTURE_DIR = Path(__file__).resolve().parent
ARCANUM_ROOT = FIXTURE_DIR.parents[4]
MATRIX_PATH = FIXTURE_DIR / "fixture-matrix.json"
INCIDENT_PATH = FIXTURE_DIR / "incident-manifest.json"
EXPECTED_JSON = FIXTURE_DIR / "results" / "latest-summary.json"
EXPECTED_MARKDOWN = FIXTURE_DIR / "results" / "latest-summary.md"


def semantic_id(key: str) -> str:
    suffix = key.split(":", 1)[-1]
    return (
        f"authority-definition:{suffix}"
        if key.startswith("external:")
        else f"definition:{suffix}"
    )


def apply_fault(artifact: dict[str, Any], oracle: dict[str, Any], fault: str) -> None:
    if fault.startswith("remove-concept:"):
        obligation_id = fault.removeprefix("remove-concept:")
        definition_id = semantic_id(obligation_id)
        artifact["definitions"] = [
            item for item in artifact["definitions"] if item["definition_id"] != definition_id
        ]
        artifact["probes"] = [
            item for item in artifact["probes"] if item.get("definition_id") != definition_id
        ]
        return
    if fault.startswith("remove-relation:"):
        obligation_id = fault.removeprefix("remove-relation:")
        relationship = next(
            item for item in oracle["relationships"] if item["obligation_id"] == obligation_id
        )
        subject_id = semantic_id(relationship["subject"])
        target_id = semantic_id(relationship["object"])
        for definition in artifact["definitions"]:
            if definition["definition_id"] == subject_id:
                definition["relations"] = [
                    item
                    for item in definition["relations"]
                    if item
                    != {"type": relationship["type"], "target_id": target_id}
                ]
        return
    if fault == "historical-discard":
        for source in artifact["evidence_sources"]:
            if source["source_class"] == "historical":
                source["semantic_disposition"] = "discard"
                source["authority_disposition"] = "historical-only"
        return
    if fault.startswith("unassess-facet:"):
        facet_id = fault.removeprefix("unassess-facet:")
        for facet in artifact["facets"]:
            if facet["facet_id"] == facet_id:
                facet["status"] = "unassessed"
        return
    if fault.startswith("uncover:"):
        artifact["declared_uncovered"].append(fault.removeprefix("uncover:"))
        return
    if fault == "add-orphan-probe":
        artifact["probes"].append(
            {
                "probe_id": "probe:orphan",
                "term": "Orphan shell label",
                "definition_id": "definition:not-in-oracle",
                "authority_binding_id": None,
            }
        )
        return
    if fault == "empty-consumer-denominator":
        artifact["consumer_topology"] = {
            "configured_roots": [],
            "enumerated_consumers": [],
            "declared_consumers": [],
            "no_consumers_evidence": "The author asserted that no consumers exist.",
        }
        return
    raise ValueError(f"unknown fixture fault: {fault}")


def execute_case(case: dict[str, Any], oracle: dict[str, Any]) -> dict[str, Any]:
    included = case["include_concepts"]
    include_set = None if included == "all" else set(included)
    artifact = build_complete_artifact(oracle, include_set)
    for fault in case["pre_closure_faults"]:
        apply_fault(artifact, oracle, fault)
    closure_receipt = evaluate_artifact(oracle, artifact)
    artifact["closure_snapshot"] = {
        "coverage_digest": closure_receipt["coverage_digest"]
    }
    for fault in case["post_closure_faults"]:
        apply_fault(artifact, oracle, fault)
    return evaluate_artifact(oracle, artifact)


def verify_incident(manifest: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for item in [
        *manifest["thin_attempt"],
        *manifest["expanded_attempt"],
        *manifest.get("v1_contracts", []),
    ]:
        path = ARCANUM_ROOT / item["path"]
        if not path.is_file():
            failures.append(f"incident path missing: {item['path']}")
            continue
        data = path.read_bytes()
        observed = hashlib.sha256(data).hexdigest()
        if len(data) != item["size"] or observed != item["sha256"]:
            failures.append(f"incident identity drift: {item['path']}")
    return failures


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Define Intent Coverage Fixture Summary",
        "",
        f"- Result: `{summary['result']}`",
        f"- Matrix digest: `{summary['matrix_digest']}`",
        f"- Cases: {summary['case_count']}",
        f"- Deterministic two-run cases: {summary['deterministic_case_count']}",
        f"- Incident identities checked: {summary['incident_identity_count']}",
        f"- Frozen v1 contract identities checked: {summary['v1_contract_identity_count']}",
        f"- Failures: {len(summary['failures'])}",
        "",
        "| Case | Expected | Observed | Deterministic | Codes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in summary["cases"]:
        codes = ", ".join(item["diagnostic_codes"]) or "-"
        lines.append(
            f"| {item['case_id']} | {item['expected_result']} | {item['actual_result']} | "
            f"{str(item['deterministic']).lower()} | {codes} |"
        )
    return "\n".join(lines) + "\n"


def build_summary() -> dict[str, Any]:
    matrix = load_object(MATRIX_PATH)
    incident = load_object(INCIDENT_PATH)
    failures = verify_incident(incident)
    results: list[dict[str, Any]] = []
    for case in matrix["cases"]:
        oracle = matrix["targets"][case["target"]]
        first = execute_case(copy.deepcopy(case), copy.deepcopy(oracle))
        second = execute_case(copy.deepcopy(case), copy.deepcopy(oracle))
        deterministic = canonical_bytes(first) == canonical_bytes(second)
        codes = sorted({item["code"] for item in first["diagnostics"]})
        expected_codes = set(case["expected_codes"])
        case_errors = []
        if first["result"] != case["expected_result"]:
            case_errors.append(
                f"expected result {case['expected_result']}, observed {first['result']}"
            )
        if not expected_codes.issubset(codes):
            case_errors.append(
                f"missing expected codes {sorted(expected_codes - set(codes))}"
            )
        if case["expected_result"] == "pass" and codes:
            case_errors.append(f"passing case emitted diagnostics {codes}")
        if not deterministic:
            case_errors.append("two receipts differ byte-for-byte")
        failures.extend(f"{case['case_id']}: {error}" for error in case_errors)
        results.append(
            {
                "case_id": case["case_id"],
                "target": case["target"],
                "expected_result": case["expected_result"],
                "actual_result": first["result"],
                "diagnostic_codes": codes,
                "deterministic": deterministic,
                "receipt_digest": first["receipt_digest"],
                "status": "pass" if not case_errors else "fail",
            }
        )
    return {
        "schema_version": "invoke.define-intent-fixture-summary.v1",
        "matrix_digest": hashlib.sha256(MATRIX_PATH.read_bytes()).hexdigest(),
        "incident_manifest_digest": hashlib.sha256(INCIDENT_PATH.read_bytes()).hexdigest(),
        "incident_identity_count": len(incident["thin_attempt"]) + len(incident["expanded_attempt"]),
        "v1_contract_identity_count": len(incident.get("v1_contracts", [])),
        "case_count": len(results),
        "deterministic_case_count": sum(item["deterministic"] for item in results),
        "cases": results,
        "failures": failures,
        "result": "pass" if not failures else "block",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-check",
        action="store_true",
        help="Print current deterministic results without comparing checked summaries.",
    )
    args = parser.parse_args()
    summary = build_summary()
    markdown = render_markdown(summary)
    checked_failures: list[str] = []
    if not args.no_check:
        if not EXPECTED_JSON.is_file() or EXPECTED_JSON.read_bytes() != canonical_bytes(summary):
            checked_failures.append("checked JSON summary differs or is missing")
        if not EXPECTED_MARKDOWN.is_file() or EXPECTED_MARKDOWN.read_text(encoding="utf-8") != markdown:
            checked_failures.append("checked Markdown summary differs or is missing")
    print(canonical_bytes(summary).decode("utf-8"), end="")
    for failure in checked_failures:
        print(f"CHECKED-SUMMARY-BLOCK: {failure}")
    return 0 if summary["result"] == "pass" and not checked_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
