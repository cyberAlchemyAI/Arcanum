#!/usr/bin/env python3
"""Validate development fixtures for the branch-aware ontology schema candidate.

This is a development-only validator for schema pressure tests. It is not a
canonical Ontology Vault runtime contract.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"

REQUIRED_TOP_LEVEL = {
    "id",
    "title",
    "entry_type",
    "record_kind",
    "lifecycle_status",
    "claim_role",
    "governance_outcome",
    "bridge_outcome",
    "owner",
    "updated_at",
    "branch_context",
    "scope",
    "content",
    "evidence",
    "confidence",
    "edges",
    "governance",
}

ENUMS = {
    "record_kind": {
        "ontology_entry",
        "promotion_record",
        "evidence_input",
        "bridge_validation",
    },
    "lifecycle_status": {
        "raw",
        "catalogedEvidence",
        "reviewableSignal",
        "promotionRecordDraft",
        "candidate",
        "premise",
        "reviewed",
        "promoted",
        "contradicted",
        "retired",
        "rejected",
        "deferred",
    },
    "claim_role": {
        "hypothesis",
        "observation",
        "evidence",
        "premise",
        "principle",
        "policy",
        "constraint",
        "invariant",
        "contradiction",
        "retirement",
        "other",
    },
    "governance_outcome": {"none", "policy", "constitution", "axiom"},
    "bridge_outcome": {
        "aligned",
        "partial",
        "drift",
        "insufficient",
        "contradicted",
        "not_applicable",
        "unknown",
    },
    "branch_context.primary": {"meaning", "system", "operational", "bridge"},
    "branch_context.local_alias": {
        None,
        "business",
        "domain",
        "intent",
        "proposition",
        "philosophy",
    },
    "branch_context.role_family": {
        "meaning",
        "mechanism",
        "context",
        "relation",
        "evidence",
        "governance",
        "other",
    },
    "confidence.evidence": {"low", "medium", "high", "unknown"},
    "confidence.commitment": {"low", "medium", "high", "unknown"},
    "confidence.bridge_alignment": {
        "low",
        "medium",
        "high",
        "not_applicable",
        "unknown",
    },
    "confidence.scope": {"low", "medium", "high", "unknown"},
    "governance.promotion_state": {
        "hypothesis",
        "candidate",
        "reviewed",
        "promoted",
        "contradicted",
        "retired",
        "rejected",
        "deferred",
    },
    "governance.next_gate": {
        "none",
        "evidence-review",
        "premise-review",
        "bridge-validation",
        "decision-gate",
        "convention-update",
        "lifecycle-owner-review",
    },
    "governance.circular_authority_check": {
        "pass",
        "flag",
        "block",
        "not_applicable",
    },
}

EDGE_TYPES = {
    "realized_by",
    "depends_on",
    "constrained_by",
    "observed_by",
    "tested_by",
    "drifts_from",
    "traced_to",
    "operationalizes",
    "contradicted_by",
    "promotes_to",
    "specializes",
    "generalizes_to",
    "supersedes",
    "related_to",
}


@dataclass(frozen=True)
class Finding:
    rule: str
    message: str


def value_at(entry: dict[str, Any], dotted: str) -> Any:
    current: Any = entry
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def add(findings: list[Finding], rule: str, message: str) -> None:
    findings.append(Finding(rule, message))


def validate_entry(entry: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    missing = sorted(REQUIRED_TOP_LEVEL - set(entry))
    for field in missing:
        add(findings, "required", f"missing top-level field: {field}")

    if "status" in entry:
        add(findings, "V11", "top-level status is not allowed; use lifecycle_status")

    for field, allowed in ENUMS.items():
        value = value_at(entry, field)
        if value not in allowed:
            rule = "V12" if field == "record_kind" else "enum"
            add(findings, rule, f"{field} has invalid value: {value!r}")

    confidence = entry.get("confidence")
    if not isinstance(confidence, dict):
        add(findings, "required", "confidence must be an object")
    else:
        for field in ("evidence", "commitment"):
            if field not in confidence:
                add(findings, "V8", f"confidence.{field} is required")

    governance = entry.get("governance")
    if not isinstance(governance, dict):
        add(findings, "required", "governance must be an object")
    else:
        if governance.get("mutation_allowed") is not False:
            add(findings, "boundary", "governance.mutation_allowed must be false")
        if not isinstance(governance.get("promotion_blockers"), list):
            add(findings, "required", "governance.promotion_blockers must be a list")

    evidence = entry.get("evidence")
    if not isinstance(evidence, dict):
        add(findings, "required", "evidence must be an object")
    else:
        for item in evidence.get("inventory_refs", []):
            if item.get("non_authority_notice") is not True:
                add(findings, "V5", "inventory_refs[] must set non_authority_notice: true")

    branch_context = entry.get("branch_context")
    if not isinstance(branch_context, dict):
        add(findings, "required", "branch_context must be an object")
    else:
        primary = branch_context.get("primary")
        if primary == "operational" and not branch_context.get("operating_context"):
            add(findings, "V3", "operational entries require operating_context")
        if primary == "bridge":
            if not branch_context.get("bridge_scope"):
                add(findings, "V4", "bridge entries require bridge_scope")
            if not entry.get("edges") and branch_context.get("local_role") != "evidence-gap":
                add(findings, "V4", "bridge entries require edges or local_role evidence-gap")

    edges = entry.get("edges")
    if not isinstance(edges, list):
        add(findings, "required", "edges must be a list")
    else:
        for index, edge in enumerate(edges):
            if not isinstance(edge, dict):
                add(findings, "required", f"edges[{index}] must be an object")
                continue
            if edge.get("type") not in EDGE_TYPES:
                add(findings, "enum", f"edges[{index}].type has invalid value: {edge.get('type')!r}")
            if edge.get("target_branch") not in {"meaning", "system", "operational", "bridge", "unknown"}:
                add(findings, "enum", f"edges[{index}].target_branch is invalid")
            if edge.get("lifecycle_status") not in {
                "raw",
                "candidate",
                "reviewed",
                "promoted",
                "contradicted",
                "retired",
                "rejected",
                "deferred",
            }:
                add(findings, "enum", f"edges[{index}].lifecycle_status is invalid")
            if edge.get("bridge_outcome") not in ENUMS["bridge_outcome"]:
                add(findings, "enum", f"edges[{index}].bridge_outcome is invalid")

    if entry.get("claim_role") == "candidate":
        add(findings, "V11", "claim_role candidate is invalid; candidate is a lifecycle status")

    if entry.get("record_kind") == "promotion_record":
        if entry.get("entry_type") != "PromotionRecord":
            add(findings, "V13", "promotion_record entries should use entry_type PromotionRecord")
        if not entry.get("edges"):
            add(findings, "V13", "promotion_record entries require at least one target relation")
        if not isinstance(evidence, dict) or not (
            evidence.get("raw_sources") or evidence.get("validation_refs") or evidence.get("inventory_refs")
        ):
            add(findings, "V13", "promotion_record entries require at least one evidence pointer")
        if not isinstance(governance, dict) or governance.get("next_gate") == "none":
            add(findings, "V13", "promotion_record entries require a review or validation gate")
        if isinstance(governance, dict) and not governance.get("contradiction_path"):
            add(findings, "V13", "promotion_record entries require a contradiction path")

    if entry.get("record_kind") == "ontology_entry" and entry.get("entry_type") == "PromotionRecord":
        add(findings, "V13", "ontology_entry must not use entry_type PromotionRecord")

    if entry.get("record_kind") == "bridge_validation":
        if not isinstance(branch_context, dict) or branch_context.get("primary") != "bridge":
            add(findings, "V13", "bridge_validation entries require branch_context.primary bridge")
        if not isinstance(branch_context, dict) or not branch_context.get("bridge_scope"):
            add(findings, "V13", "bridge_validation entries require bridge_scope")
        if value_at(entry, "confidence.bridge_alignment") in {None, "not_applicable"}:
            add(findings, "V13", "bridge_validation entries require bridge alignment confidence")
        if not entry.get("edges") and (
            not isinstance(branch_context, dict) or branch_context.get("local_role") != "evidence-gap"
        ):
            add(findings, "V13", "bridge_validation entries require edges or local_role evidence-gap")

    if entry.get("record_kind") == "evidence_input":
        if entry.get("lifecycle_status") == "promoted" or (
            isinstance(governance, dict) and governance.get("promotion_state") == "promoted"
        ):
            add(findings, "V13", "evidence_input must not claim promoted ontology authority")
        if entry.get("governance_outcome") != "none":
            add(findings, "V13", "evidence_input must not carry governance_outcome")
        if entry.get("claim_role") not in {"evidence", "observation"}:
            add(findings, "V13", "evidence_input claim_role must be evidence or observation")
        if value_at(entry, "confidence.commitment") not in {"low", "unknown"}:
            add(findings, "V13", "evidence_input commitment must be low or unknown")
        if not isinstance(evidence, dict) or not (
            evidence.get("raw_sources") or evidence.get("validation_refs") or evidence.get("inventory_refs")
        ):
            add(findings, "V13", "evidence_input requires at least one evidence pointer")

    if entry.get("lifecycle_status") == "promoted":
        if not isinstance(governance, dict) or governance.get("promotion_state") != "promoted":
            add(findings, "V9", "promoted entries require governance.promotion_state promoted")
        if isinstance(governance, dict) and governance.get("promotion_blockers"):
            add(findings, "V9", "promoted entries cannot have open promotion blockers")
        evidence_refs = []
        if isinstance(evidence, dict):
            evidence_refs.extend(evidence.get("raw_sources", []))
            evidence_refs.extend(evidence.get("validation_refs", []))
        if not evidence_refs:
            add(findings, "V9", "promoted entries require reviewed evidence or decision record")

    if entry.get("bridge_outcome") == "contradicted":
        raw_sources = evidence.get("raw_sources", []) if isinstance(evidence, dict) else []
        has_counterevidence = any(item.get("role") == "counterevidence" for item in raw_sources if isinstance(item, dict))
        if not has_counterevidence:
            add(findings, "V11", "contradicted bridge_outcome requires counterevidence")

    return findings


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def expected_invalid_rules() -> dict[str, str]:
    index_path = FIXTURES / "invalid" / "index.json"
    if not index_path.exists():
        return {}
    index = load_json(index_path)
    return {item["path"]: item["expected_rule"] for item in index.get("fixtures", [])}


def run() -> int:
    failures: list[str] = []

    for path in sorted((FIXTURES / "valid").glob("*.json")):
        if path.name == "index.json":
            continue
        findings = validate_entry(load_json(path))
        if findings:
            details = "; ".join(f"{finding.rule}: {finding.message}" for finding in findings)
            failures.append(f"VALID fixture failed {path.name}: {details}")

    invalid_rules = expected_invalid_rules()
    for path in sorted((FIXTURES / "invalid").glob("*.json")):
        if path.name == "index.json":
            continue
        findings = validate_entry(load_json(path))
        if not findings:
            failures.append(f"INVALID fixture unexpectedly passed {path.name}")
            continue
        expected = invalid_rules.get(path.name)
        if expected and expected not in {finding.rule for finding in findings}:
            details = ", ".join(finding.rule for finding in findings)
            failures.append(f"INVALID fixture {path.name} missed expected {expected}; got {details}")

    if failures:
        print("branch-schema-fixtures: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("branch-schema-fixtures: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(run())
