#!/usr/bin/env python3
"""Validate Task Session decision/completion policy, fixtures, and mirrors."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_automatic_choice(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    required = policy["automatic_choice"]["required_classification"]
    admitted = all(fixture_input.get(key) == value for key, value in required.items())
    outcome_key = "admitted_outcome" if admitted else "rejected_outcome"
    return str(policy["automatic_choice"][outcome_key])


def evaluate_series_intent(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    series = policy["series_intent"]
    request = str(fixture_input.get("request", "")).casefold()
    detected = any(term.casefold() in request for term in series["explicit_terms"])
    outcome_key = "detected_outcome" if detected else "not_detected_outcome"
    return str(series[outcome_key])


def evaluate_closeout_preflight(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    preflight = policy["closeout_preflight"]
    if fixture_input.get("sync_expected") is False:
        return str(preflight["no_sync_outcome"])

    for field in preflight["required_inputs"]:
        value = fixture_input.get(field)
        if value is None or value == "" or value == [] or value == {}:
            return str(preflight["rejected_outcome"])

    delta_classes = fixture_input.get("allowed_delta_classes")
    if not isinstance(delta_classes, list) or not delta_classes:
        return str(preflight["rejected_outcome"])
    if any(item not in preflight["admitted_delta_classes"] for item in delta_classes):
        return str(preflight["rejected_outcome"])

    successor = fixture_input.get("successor_selection", {})
    if successor.get("requested") is True and preflight[
        "unique_declared_successor_only"
    ]:
        if not (
            successor.get("declared") is True
            and successor.get("dependency_ready") is True
            and successor.get("candidate_count") == 1
        ):
            return str(preflight["rejected_outcome"])

    return str(preflight["admitted_outcome"])


def accepted_equivalent_passes(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> bool:
    equivalent = fixture_input.get("accepted_equivalent")
    if not isinstance(equivalent, dict):
        return False
    equivalent_policy = policy["validation"]["accepted_equivalent"]
    if equivalent_policy["must_be_named_and_accepted"] and not (
        equivalent.get("named") is True and equivalent.get("accepted") is True
    ):
        return False
    if equivalent_policy["must_pass"]:
        return equivalent.get("result") == policy["validation"]["passing_result"]
    return True


def evaluate_validation(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    validation = policy["validation"]
    result = fixture_input.get("result")
    if result == validation["passing_result"] or accepted_equivalent_passes(
        policy, fixture_input
    ):
        return "PASS"

    criticality = fixture_input.get(
        "criticality", validation["default_criticality"]
    )
    if criticality not in validation["criticality_values"]:
        return "BLOCK"
    if criticality == "acceptance-critical":
        return str(validation["acceptance_critical_unmet_outcome"])

    residue = fixture_input.get("residue")
    residue_policy = validation["noncritical_residue"]
    admitted = isinstance(residue, dict)
    if admitted and residue_policy["must_be_named"]:
        admitted = residue.get("named") is True
    if admitted and residue_policy["must_not_falsify_done_criterion"]:
        admitted = residue.get("can_falsify_done_criterion") is False
    outcome_key = "admitted_outcome" if admitted else "rejected_outcome"
    return str(residue_policy[outcome_key])


def evaluate_closeout_sync(
    policy: dict[str, Any], fixture_input: dict[str, Any]
) -> str:
    closeout = policy["closeout_sync"]
    if fixture_input.get("sync_required") is False:
        return str(closeout["no_op_outcome"])

    if fixture_input.get("route_tuple") != closeout["route_tuple"]:
        return str(closeout["rejected_outcome"])
    for field in closeout["required_inputs"]:
        value = fixture_input.get(field)
        if value is None or value == "" or value == []:
            return str(closeout["rejected_outcome"])

    delta_classes = fixture_input.get("delta_classes")
    if not isinstance(delta_classes, list) or not delta_classes:
        return str(closeout["rejected_outcome"])
    if any(item not in closeout["allowed_delta_classes"] for item in delta_classes):
        return str(closeout["rejected_outcome"])

    scopes = fixture_input.get("scopes", [])
    if not isinstance(scopes, list):
        return str(closeout["rejected_outcome"])
    if any(item in closeout["forbidden_scopes"] for item in scopes):
        return str(closeout["rejected_outcome"])

    successor = fixture_input.get("successor_selection", {})
    if successor.get("requested") is True and closeout[
        "unique_declared_successor_only"
    ]:
        if not (
            successor.get("declared") is True
            and successor.get("dependency_ready") is True
            and successor.get("candidate_count") == 1
        ):
            return str(closeout["rejected_outcome"])

    owner_receipt = fixture_input.get("owner_receipt")
    if not isinstance(owner_receipt, dict) or owner_receipt.get("joined") is not True:
        return str(closeout["rejected_outcome"])
    if owner_receipt.get("result") not in closeout["passing_owner_results"]:
        return str(closeout["rejected_outcome"])
    return str(closeout["admitted_outcome"])


def split_contract(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"{path}: incomplete YAML frontmatter")
    return parts[1], parts[2]


def validate_contracts(repo_root: Path, canonical_dir: Path) -> list[str]:
    errors: list[str] = []
    canonical_path = canonical_dir / "SKILL.md"
    canonical_frontmatter, canonical_body = split_contract(canonical_path)
    required_clauses = (
        "With no positional target or selector, enter `resume-nearest` mode",
        "Visible current-session context means the active prompt/session evidence",
        "never claim access to lost",
        "global-latest telemetry, fuzzy relevance, and cross-project inference",
        "emit or\n    update one repository-local Task Session continuity cursor",
        "explicitly classified both nonconsequential and reversible",
        "Unclassified done criteria and validation obligations are",
        "return `BLOCK`; recording a substitute does not",
        "Return `FLAG` only for named noncritical residue",
        "do not ask for a",
        "second user approval",
        "return but never execute the next task/SWU selected by closeout",
        "`task-session-until-blocker` spell",
        "closeout prerequisite preflight before mutation admission",
        "## Step 5A - Verify Routed Mutation Admission",
        "`scripts/verify-mutation-readiness.py`",
        "`not-applicable` is valid only for `standalone-nonmutating`",
    )
    forbidden_clauses = (
        "or where a recommendation is clearly safe",
    )

    for clause in required_clauses:
        if clause not in canonical_body:
            errors.append(f"canonical contract missing clause: {clause}")
    for clause in forbidden_clauses:
        if clause in canonical_body:
            errors.append(f"canonical contract retains forbidden clause: {clause}")
    if "version: 0.8.0" not in canonical_frontmatter:
        errors.append("canonical contract version is not 0.8.0")

    support_paths = (
        Path("README.md"),
        Path("decision-validation-policy.json"),
        Path("continuity.schema.json"),
        Path("schemas/mutation-admission-request.schema.json"),
        Path("schemas/mutation-admission-receipt.schema.json"),
        Path("scripts/resolve-nearest-swu.py"),
        Path("scripts/verify-mutation-readiness.py"),
    )
    runtime_targets = (
        repo_root / ".agents/skills/task-session",
        repo_root / ".claude/skills/task-session",
    )
    for runtime_dir in runtime_targets:
        skill_path = runtime_dir / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"generated contract missing: {skill_path}")
            continue
        _, runtime_body = split_contract(skill_path)
        if runtime_body != canonical_body:
            errors.append(f"generated contract body drift: {skill_path}")
        for support_path in support_paths:
            canonical_support = canonical_dir / support_path
            runtime_support = runtime_dir / support_path
            if not runtime_support.is_file():
                errors.append(f"generated support missing: {runtime_support}")
            elif runtime_support.read_bytes() != canonical_support.read_bytes():
                errors.append(f"generated support drift: {runtime_support}")
    return errors


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "usage: validate-decision-validation-policy.py "
            "<repository-root> <canonical-task-session-dir>",
            file=sys.stderr,
        )
        return 2

    repo_root = Path(sys.argv[1]).resolve()
    canonical_dir = Path(sys.argv[2]).resolve()
    policy = load_json(canonical_dir / "decision-validation-policy.json")
    zero_argument = policy.get("zero_argument_resolution", {})
    expected_priority = [
        "explicit-source",
        "visible-session-context",
        "exact-session-cursor",
        "cwd-ancestor-work-pack",
        "scope-matched-continuity",
    ]
    if zero_argument.get("source_priority") != expected_priority:
        errors = ["zero-argument source priority drift"]
    else:
        errors = []
    if zero_argument.get("execution_limit") != 1:
        errors.append("zero-argument execution limit is not one")
    if zero_argument.get("live_revalidation_required") is not True:
        errors.append("zero-argument resolution does not require live revalidation")
    forbidden_sources = set(zero_argument.get("forbidden_sources", []))
    if forbidden_sources != {
        "global-latest-observability",
        "unscoped-transcript-search",
        "fuzzy-relevance",
    }:
        errors.append("zero-argument forbidden source set drift")
    fixtures = load_json(
        canonical_dir / "development/fixtures/decision-validation-cases.json"
    )
    passed = 0

    for case in fixtures["cases"]:
        kind = case["kind"]
        if kind == "series-intent":
            actual = evaluate_series_intent(policy, case["input"])
        elif kind == "closeout-preflight":
            actual = evaluate_closeout_preflight(policy, case["input"])
        elif kind == "automatic-choice":
            actual = evaluate_automatic_choice(policy, case["input"])
        elif kind == "validation":
            actual = evaluate_validation(policy, case["input"])
        elif kind == "closeout-sync":
            actual = evaluate_closeout_sync(policy, case["input"])
        else:
            errors.append(f"{case['id']}: unknown fixture kind {kind}")
            continue
        if actual != case["expected"]:
            errors.append(
                f"{case['id']}: expected {case['expected']}, received {actual}"
            )
        else:
            passed += 1

    errors.extend(validate_contracts(repo_root, canonical_dir))
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        print(f"RESULT passed={passed} failed={len(errors)}")
        return 1

    print(f"RESULT passed={passed} failed=0")
    print("PARITY canonical=.agents=.claude policy-and-contract-body")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
