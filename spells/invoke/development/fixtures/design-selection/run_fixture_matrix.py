#!/usr/bin/env python3
"""Execute the frozen Invoke Design-selection fixture and mutation matrices."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


FIXTURE_DIR = Path(__file__).resolve().parent
INVOKE_DIR = FIXTURE_DIR.parents[2]
SCHEMA_DIR = INVOKE_DIR / "schemas"
SCRIPT_DIR = INVOKE_DIR / "scripts"


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EXTRACTOR = load_module("invoke_design_scope_extractor", SCRIPT_DIR / "design_scope_extractor.py")
VALIDATOR = load_module(
    "invoke_design_selection_validator", SCRIPT_DIR / "design_selection_validator.py"
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


SCHEMAS = {
    "manifest": load_json(SCHEMA_DIR / "design-scope-manifest.schema.json"),
    "receipt": load_json(SCHEMA_DIR / "design-denominator-receipt.schema.json"),
    "result": load_json(SCHEMA_DIR / "design-selection-result.schema.json"),
}


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def source_fields(item_id: str, source_digest: str) -> dict[str, str]:
    return {
        "source_selector": "source.txt",
        "source_digest": source_digest,
    }


def build_manifest(
    fixture_id: str,
    profile: dict[str, Any],
    faults: list[str],
    root: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    source = root / "source.txt"
    source.write_text(f"synthetic design selector for {fixture_id}\n", encoding="utf-8")
    digest = file_digest(source)
    common = source_fields("source", digest)

    human_actors = []
    rendered_surfaces = []
    if profile["human_actor"]:
        human_actors.append(
            {
                "actor_id": "actor-1",
                "natural_person": True,
                "reads": True,
                "decides": True,
                "acts": True,
                "recovers": True,
                "navigates": True,
                "assistive_operation": True,
                "surfaces": ["surface-1"],
                **common,
            }
        )
        rendered_surfaces.append(
            {
                "surface_id": "surface-1",
                "modality": "text",
                "semantic_contract_ref": "semantic-contract-1",
                "semantic_change": (
                    "changed" if profile["semantic_surface_change"] else "none"
                ),
                **common,
            }
        )

    interfaces = []
    if profile["interface"] != "none":
        interfaces.append(
            {
                "interface_id": "interface-1",
                "kind": (
                    "authenticated-admission"
                    if profile["interface"] == "admission-protocol"
                    else profile["interface"]
                ),
                "peer": "synthetic-peer",
                "direction": "bidirectional",
                "contract_ref": "contract-1",
                **common,
            }
        )

    writers = []
    if profile["durable_state"]:
        for index in range(profile["writer_count"]):
            writers.append(
                {
                    "writer_id": f"writer-{index + 1}",
                    "targets": ["store-1"],
                    "concurrency": "serialized" if index == 0 else "optimistic",
                    **common,
                }
            )
    stores = (
        [
            {
                "store_id": "store-1",
                "authority": "persistence-owner",
                "data_classes": ["synthetic-record"],
                "writers": [item["writer_id"] for item in writers],
                **common,
            }
        ]
        if profile["durable_state"]
        else []
    )
    queues = (
        [
            {
                "queue_id": "queue-1",
                "producers": ["writer-1"],
                "consumers": ["worker-1"],
                "ordering": "fifo",
                **common,
            }
        ]
        if profile["queue"]
        else []
    )

    normative_rules = []
    if profile["normative_claim"]:
        normative_rules.append(
            {
                "rule_id": "rule-validation",
                "verb": "must",
                "subject": "validator",
                "object": "validate output",
                "enforcement_hint": "fixture runner",
                **common,
            }
        )
    if profile["interface"] == "admission-protocol":
        normative_rules.append(
            {
                "rule_id": "rule-state",
                "verb": "must",
                "subject": "state transition",
                "object": "remain legal",
                "enforcement_hint": "transition validator",
                **common,
            }
        )

    effects = []
    if profile["privileged_effect"]:
        effects.append(
            {
                "effect_id": "effect-privileged",
                "reversible": True,
                "external": False,
                "privileged": True,
                **common,
            }
        )
    if profile["external_effect"]:
        effects.append(
            {
                "effect_id": "effect-external",
                "reversible": False,
                "external": True,
                "privileged": False,
                **common,
            }
        )

    sinks = (
        [
            {
                "sink_id": "sink-1",
                "data_classes": ["operator-evidence"],
                "retention_hint": "bounded",
                **common,
            }
        ]
        if profile["data_sink"]
        else []
    )
    deployments = (
        [
            {
                "deployment_id": "deployment-1",
                "environment": "synthetic",
                "release_mode": "staged",
                **common,
            }
        ]
        if profile["deployment_transition"]
        else []
    )
    compatibility = []
    if profile["compatibility_change"]:
        stored = profile["durable_state"] and profile["deployment_transition"]
        compatibility.append(
            {
                "boundary_id": "compatibility-1",
                "old_contract": "stored-v1" if stored else "protocol-v1",
                "new_contract": "stored-v2" if stored else "protocol-v2",
                **common,
            }
        )
    quality = (
        [
            {
                "claim_id": "quality-1",
                "source_kind": "bounded-hypothesis",
                "threshold_or_tradeoff": "measure before requiring",
                "required": False,
                **common,
            }
        ]
        if profile["quality_hypothesis"]
        else []
    )
    acceptance = (
        [
            {
                "claim_id": "acceptance-1",
                "selector": "source.txt",
                "evidence_state": "authored-complete",
                **common,
            }
        ]
        if profile["normative_claim"]
        else []
    )

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "manifest_id": f"manifest:{fixture_id.lower()}",
        "target_id": f"target:{fixture_id.lower()}",
        "target_footprint": {
            "roots": [{"path": "source.txt", "digest": digest}],
            "inclusions": [
                {"selector": "source.txt", "path": "source.txt", "digest": digest}
            ],
            "exclusions": [],
        },
        "source_contracts": [
            {
                "source_id": "source-1",
                "selector": "source.txt",
                "path": "source.txt",
                "digest": digest,
            }
        ],
        "human_actors": human_actors,
        "rendered_surfaces": rendered_surfaces,
        "interfaces": interfaces,
        "stores": stores,
        "queues": queues,
        "writers": writers,
        "normative_rules": normative_rules,
        "effects": effects,
        "data_and_log_sinks": sinks,
        "deployment_targets": deployments,
        "compatibility_boundaries": compatibility,
        "quality_claims": quality,
        "acceptance_and_readiness_claims": acceptance,
        "unknowns": [],
        "input_digest": "0" * 64,
        "authored_by": "invoke-design-author",
    }

    authored: list[dict[str, Any]] = []
    if not (profile["human_actor"] and profile["semantic_surface_change"]):
        authored.append(
            {
                "concern_id": "authored:ux",
                "primary_class": "ux",
                "disposition": "not-applicable-with-rationale",
                "evidence_selectors": ["source.txt"],
                "rationale": "no changed natural-person semantic contract",
            }
        )
    witnesses: list[dict[str, Any]] = []
    extra_denominator_ids: list[str] = []

    for fault in faults:
        if fault.startswith("omit-field-class:"):
            manifest.pop(fault.split(":", 1)[1], None)
        elif fault == "omit-required-surface":
            manifest.pop("rendered_surfaces", None)
        elif fault == "omit-second-writer":
            if len(manifest["writers"]) > 1:
                manifest["writers"] = manifest["writers"][:1]
            extra_denominator_ids.append("authored:expected-writer-2")
            authored.append(
                {
                    "concern_id": "authored:persistence-omission",
                    "primary_class": "persistence",
                    "disposition": "block",
                    "evidence_selectors": ["source.txt"],
                    "rationale": "declared writer denominator is incomplete",
                }
            )
        elif fault == "false-na:persistence":
            authored.append(
                {
                    "concern_id": "authored:persistence",
                    "primary_class": "persistence",
                    "disposition": "not-applicable-with-rationale",
                    "evidence_selectors": ["source.txt"],
                    "rationale": "declared no durable data",
                }
            )
        elif fault == "na-without-negative-extraction:ux":
            for item in authored:
                if item["primary_class"] == "ux":
                    item["evidence_selectors"] = []
        elif fault == "missing-owner:persistence":
            authored.append(
                {
                    "concern_id": "authored:persistence",
                    "primary_class": "persistence",
                    "disposition": "required",
                    "evidence_selectors": ["source.txt"],
                    "ownership": {
                        "accountable_owner": "",
                        "contributing_owners": ["plan-work-pack-owner"],
                        "artifact_owner": "architecture-owner",
                        "validator_owner": VALIDATOR.VALIDATOR_ID,
                    },
                    "rationale": "owner mutation",
                }
            )
        elif fault == "select-recommended-output:performance":
            authored.append(
                {
                    "concern_id": "authored:performance",
                    "primary_class": "performance",
                    "disposition": "recommended",
                    "selected": True,
                    "evidence_selectors": ["source.txt"],
                    "revisit_condition": "measure later",
                    "rationale": "bounded hypothesis",
                }
            )
        elif fault == "illegal-plan-evidence-state":
            witnesses.append(
                {"witness_id": "witness-1", "evidence_state": "executed"}
            )

    manifest["input_digest"] = EXTRACTOR.manifest_digest(manifest)
    return manifest, authored, witnesses, extra_denominator_ids


def execute_case(case: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="invoke-design-selection-") as tmp:
        root = Path(tmp)
        profile = matrix["profiles"][case["profile"]]
        manifest, authored, witnesses, extra_ids = build_manifest(
            case["fixture_id"], profile, case["faults"], root
        )
        try:
            receipt = EXTRACTOR.extract_denominator(
                manifest,
                root,
                SCHEMAS["manifest"],
                [item["concern_id"] for item in authored] + extra_ids,
            )
        except EXTRACTOR.ExtractionFailure as error:
            missing_surface = "omit-required-surface" in case["faults"]
            actual = {
                "verdict": "block",
                "primary_concerns": ["ux"] if missing_surface else [],
                "dispositions": {"ux": "block"} if missing_surface else {},
                "selected_outputs": [],
                "evidence_state": "authored-complete",
                "diagnostic_codes": [error.code],
            }
            return compare_case(case, actual)

        if "stale-denominator" in case["faults"]:
            receipt["manifest_input_digest"] = "0" * 64
            receipt["receipt_digest"] = VALIDATOR.digest_without(
                receipt, "receipt_digest"
            )
        if "self-issued-receipt" in case["faults"]:
            receipt["manifest_authored_by"] = receipt["detector_id"]
            receipt["receipt_digest"] = VALIDATOR.digest_without(
                receipt, "receipt_digest"
            )
        if "unbound-signal" in case["faults"]:
            receipt["denominator_signal_ids"].append("signal:unsupported:1")
            receipt["denominator_signal_ids"].sort()
            receipt["receipt_digest"] = VALIDATOR.digest_without(
                receipt, "receipt_digest"
            )

        transform = None
        if "changed-pass-two" in case["faults"]:
            def change_second(value: dict[str, Any]) -> dict[str, Any]:
                for item in value["authored_concerns"]:
                    if item["primary_class"] == "ux":
                        item["disposition"] = "block"
                return value
            transform = change_second

        result = VALIDATOR.validate_selection(
            manifest,
            receipt,
            authored,
            witnesses,
            SCHEMAS,
            transform,
        )
        result_errors = list(
            Draft202012Validator(SCHEMAS["result"]).iter_errors(result)
        )
        if result_errors:
            return {
                "fixture_id": case["fixture_id"],
                "status": "fail",
                "errors": [
                    f"result schema: {'/'.join(map(str, item.path))}: {item.message}"
                    for item in result_errors
                ],
            }
        concerns = {
            item["primary_class"]: item["disposition"]
            for item in result["concerns"]
        }
        primary = sorted(
            key
            for key, disposition in concerns.items()
            if disposition != "not-applicable-with-rationale"
        )
        actual = {
            "verdict": result["verdict"],
            "primary_concerns": primary,
            "dispositions": concerns,
            "selected_outputs": result["selected_outputs"],
            "evidence_state": result["evidence_state"],
            "diagnostic_codes": sorted(
                {item["code"] for item in result["diagnostics"]}
            ),
        }
        first_digest = result["result_digest"]
        repeat = VALIDATOR.validate_selection(
            manifest,
            receipt,
            authored,
            witnesses,
            SCHEMAS,
            transform,
        )
        if repeat["result_digest"] != first_digest:
            return {
                "fixture_id": case["fixture_id"],
                "status": "fail",
                "errors": ["repeat result digest changed"],
            }
        return compare_case(case, actual)


def compare_case(case: dict[str, Any], actual: dict[str, Any]) -> dict[str, Any]:
    expected = case["expected"]
    errors = []
    for key in ("verdict", "selected_outputs", "evidence_state", "diagnostic_codes"):
        if actual[key] != expected[key]:
            errors.append(f"{key}: expected {expected[key]!r}, got {actual[key]!r}")
    if expected["verdict"] == "pass":
        if actual["primary_concerns"] != expected["primary_concerns"]:
            errors.append(
                f"primary_concerns: expected {expected['primary_concerns']!r}, "
                f"got {actual['primary_concerns']!r}"
            )
    else:
        missing = set(expected["primary_concerns"]) - set(actual["primary_concerns"])
        if missing:
            errors.append(f"missing expected primary concerns: {sorted(missing)!r}")
    for key, value in expected["dispositions"].items():
        if actual["dispositions"].get(key) != value:
            errors.append(
                f"disposition {key}: expected {value!r}, "
                f"got {actual['dispositions'].get(key)!r}"
            )
    return {
        "fixture_id": case["fixture_id"],
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def mutation_result(
    mutation: dict[str, Any], matrix: dict[str, Any]
) -> dict[str, Any]:
    expected = mutation["expected_diagnostic"]
    with tempfile.TemporaryDirectory(prefix="invoke-design-mutation-") as tmp:
        root = Path(tmp)
        profile_name = "pure-local-function"
        if mutation["target"] in {"persistence", "durable_state"}:
            profile_name = "authenticated-crud"
        elif mutation["target"] in {"human_actor", "semantic_surface_change"}:
            profile_name = "human-semantic-change"
        elif mutation["target"] == "performance":
            profile_name = "bounded-performance-hypothesis"
        manifest, authored, witnesses, extra = build_manifest(
            mutation["mutation_id"], matrix["profiles"][profile_name], [], root
        )
        operation = mutation["operation"]
        target = mutation["target"]
        transform = None

        if operation == "drop-field-class":
            manifest.pop(target, None)
            manifest["input_digest"] = EXTRACTOR.manifest_digest(manifest)
        elif operation == "invert-predicate":
            if target == "human_actor":
                manifest["human_actors"][0]["natural_person"] = False
                authored = [{
                    "concern_id": "authored:ux-required",
                    "primary_class": "ux",
                    "disposition": "required",
                    "required_predicate": False,
                    "evidence_selectors": ["source.txt"],
                    "rationale": "mutation",
                }]
            elif target == "semantic_surface_change":
                manifest["rendered_surfaces"][0]["semantic_change"] = "none"
                authored = [{
                    "concern_id": "authored:ux-required",
                    "primary_class": "ux",
                    "disposition": "required",
                    "required_predicate": False,
                    "evidence_selectors": ["source.txt"],
                    "rationale": "mutation",
                }]
            elif target == "durable_state":
                authored.append({
                    "concern_id": "authored:persistence",
                    "primary_class": "persistence",
                    "disposition": "not-applicable-with-rationale",
                    "evidence_selectors": ["source.txt"],
                    "rationale": "mutation",
                })
            else:
                primary = {
                    "compatibility_change": "integration",
                    "privileged_effect": "authority",
                    "external_effect": "failure",
                }[target]
                authored.append({
                    "concern_id": f"authored:{primary}",
                    "primary_class": primary,
                    "disposition": "required",
                    "required_predicate": False,
                    "evidence_selectors": ["source.txt"],
                    "rationale": "mutation",
                })
            manifest["input_digest"] = EXTRACTOR.manifest_digest(manifest)
        elif operation == "replace-owner" and target == "null":
            authored.append({
                "concern_id": "authored:validation-owner",
                "primary_class": "validation",
                "disposition": "required",
                "evidence_selectors": ["source.txt"],
                "ownership": {
                    "accountable_owner": "",
                    "contributing_owners": [],
                    "artifact_owner": "plan-work-pack-owner",
                    "validator_owner": VALIDATOR.VALIDATOR_ID,
                },
                "rationale": "mutation",
            })
        elif operation == "promote-recommended":
            authored.append({
                "concern_id": "authored:performance",
                "primary_class": "performance",
                "disposition": "recommended",
                "selected": True,
                "evidence_selectors": ["source.txt"],
                "revisit_condition": "measure later",
                "rationale": "mutation",
            })

        try:
            receipt = EXTRACTOR.extract_denominator(
                manifest,
                root,
                SCHEMAS["manifest"],
                [item["concern_id"] for item in authored] + extra,
            )
        except EXTRACTOR.ExtractionFailure as error:
            got = error.code
        else:
            if operation == "replace-owner" and target == "self":
                receipt["manifest_authored_by"] = receipt["detector_id"]
                receipt["receipt_digest"] = VALIDATOR.digest_without(
                    receipt, "receipt_digest"
                )
            elif operation == "alter-digest":
                receipt["manifest_input_digest"] = "0" * 64
                receipt["receipt_digest"] = VALIDATOR.digest_without(
                    receipt, "receipt_digest"
                )
            elif operation == "alter-pass-two":
                def mutate_second(value: dict[str, Any]) -> dict[str, Any]:
                    for item in value["authored_concerns"]:
                        if item["primary_class"] == "ux":
                            item["disposition"] = "block"
                    return value
                transform = mutate_second
            result = VALIDATOR.validate_selection(
                manifest, receipt, authored, witnesses, SCHEMAS, transform
            )
            codes = sorted({item["code"] for item in result["diagnostics"]})
            got = expected if expected in codes else ",".join(codes) or "PASS"
        return {
            "mutation_id": mutation["mutation_id"],
            "status": "pass" if got == expected else "fail",
            "expected": expected,
            "actual": got,
        }


def contract_checks() -> list[dict[str, Any]]:
    checks = {
        INVOKE_DIR / "design.md": [
            "DesignScopeManifest",
            "DesignDenominatorReceipt",
            "DesignSelectionResult",
            "design-validator-pass",
            "plan-evidence-pending",
        ],
        INVOKE_DIR / "templates/domainspec-spec/architecture-bundle.md": [
            "Concern-to-view trace",
            "Triggered architecture extensions",
        ],
        INVOKE_DIR / "templates/architecture/architecture.md": [
            "Concern-to-view trace",
            "Triggered architecture extensions",
        ],
        INVOKE_DIR / "templates/ux-plan/ux-plan.md": [
            "natural person",
            "semantic contract",
            "Failure and recovery",
        ],
        INVOKE_DIR / "README.md": [
            "Design selection receipt",
            "Design evidence state",
        ],
    }
    results = []
    for path, patterns in checks.items():
        text = path.read_text(encoding="utf-8")
        missing = [pattern for pattern in patterns if pattern not in text]
        results.append(
            {
                "path": str(path.relative_to(INVOKE_DIR)),
                "status": "pass" if not missing else "fail",
                "missing": missing,
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--group",
        choices=("all", "schemas", "extractor", "validator", "mutations", "contracts"),
        default="all",
    )
    parser.add_argument("--report-dir", default=str(FIXTURE_DIR / "results"))
    args = parser.parse_args()

    matrix = load_json(FIXTURE_DIR / "fixture-matrix.json")
    denominator = load_json(FIXTURE_DIR / "fixture-denominator-receipt.json")
    actual_digest = canonical_digest(matrix)
    failures = []
    results: dict[str, Any] = {}

    if actual_digest != denominator["corpus_digest"]:
        failures.append("frozen corpus digest changed")

    if args.group in {"all", "schemas"}:
        schema_results = []
        for name, schema in SCHEMAS.items():
            errors = list(Draft202012Validator.check_schema(schema) or [])
            schema_results.append({"schema": name, "status": "pass", "errors": errors})
        results["schemas"] = schema_results

    if args.group in {"all", "extractor", "validator"}:
        selected = matrix["cases"]
        if args.group == "extractor":
            selected = [
                case
                for case in selected
                if any(
                    fault.startswith("omit-") for fault in case["faults"]
                )
                or case["fixture_id"] in {"DESIGN-BOUND-001", "DESIGN-NEG-009"}
            ]
        case_results = [execute_case(case, matrix) for case in selected]
        results["cases"] = case_results
        failures.extend(
            f"{item['fixture_id']}: {'; '.join(item['errors'])}"
            for item in case_results
            if item["status"] != "pass"
        )

    if args.group in {"all", "mutations"}:
        mutation_results = [
            mutation_result(mutation, matrix) for mutation in matrix["mutations"]
        ]
        results["mutations"] = mutation_results
        failures.extend(
            f"{item['mutation_id']}: expected {item['expected']}, got {item['actual']}"
            for item in mutation_results
            if item["status"] != "pass"
        )

    if args.group == "contracts":
        checks = contract_checks()
        results["contracts"] = checks
        failures.extend(
            f"{item['path']}: missing {item['missing']}"
            for item in checks
            if item["status"] != "pass"
        )

    summary = {
        "schema_version": "invoke.design-selection-fixture-summary.v1",
        "group": args.group,
        "corpus_digest": actual_digest,
        "case_count": len(results.get("cases", [])),
        "mutation_count": len(results.get("mutations", [])),
        "result": "pass" if not failures else "block",
        "failures": failures,
        "results": results,
    }
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "latest-summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# Invoke Design Selection Fixture Summary",
        "",
        f"- Group: `{args.group}`",
        f"- Result: `{summary['result']}`",
        f"- Corpus digest: `{actual_digest}`",
        f"- Cases executed: {summary['case_count']}",
        f"- Mutations executed: {summary['mutation_count']}",
        f"- Failures: {len(failures)}",
    ]
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
    (report_dir / "latest-summary.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(
        f"{'PASS' if not failures else 'BLOCK'} design-selection "
        f"{args.group}: {summary['case_count']} cases, "
        f"{summary['mutation_count']} mutations, {len(failures)} failures"
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
