#!/usr/bin/env python3
"""Validate deterministic, total, two-pass Invoke Design output selection."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator


VALIDATOR_ID = "invoke-design-selection-validator"
VALIDATOR_VERSION = "1.0.0"

PRIMARY_PRECEDENCE = (
    "authority",
    "security",
    "state-event",
    "persistence",
    "failure",
    "reliability",
    "integration",
    "migration",
    "rollout",
    "privacy-data",
    "performance",
    "ux",
    "validation",
)

OUTPUT_BY_CLASS = {
    "authority": "architecture:authority-trust",
    "security": "architecture:security-abuse",
    "state-event": "architecture:state-event",
    "persistence": "architecture:persistence-concurrency",
    "failure": "architecture:failure-compensation",
    "reliability": "architecture:quality",
    "integration": "architecture:integration-versioning",
    "migration": "architecture:migration-rollout",
    "rollout": "architecture:migration-rollout",
    "privacy-data": "architecture:data-lifecycle",
    "performance": "architecture:quality",
    "ux": "ux-plan",
    "validation": "validation-contracts",
}

ACCOUNTABLE_OWNER = {
    "authority": "authority-owner",
    "security": "security-risk-owner",
    "state-event": "workflow-owner",
    "persistence": "persistence-owner",
    "failure": "workflow-owner",
    "reliability": "service-owner",
    "integration": "interface-owner",
    "migration": "migration-owner",
    "rollout": "release-owner",
    "privacy-data": "data-owner",
    "performance": "service-owner",
    "ux": "ux-plan-owner",
    "validation": "design-owner",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def digest_without(document: dict[str, Any], key: str) -> str:
    return canonical_digest({k: v for k, v in document.items() if k != key})


def schema_errors(
    document: dict[str, Any], schema: dict[str, Any], label: str
) -> list[str]:
    return [
        f"{label} schema invalid at "
        f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def diagnostic(
    code: str,
    message: str,
    selector: str | None = None,
    owner: str | None = None,
) -> dict[str, Any]:
    repairs = {
        "MANIFEST_NOT_CLOSED": "close the manifest and recompute its digest",
        "MISSING_DETECTOR_INPUT": "repair the missing detector input and rerun",
        "STALE_DENOMINATOR_RECEIPT": "rerun extraction against the current manifest",
        "SELF_ISSUED_RECEIPT": "use an independent detector identity",
        "UNBOUND_SIGNAL": "bind every denominator signal to one primary concern",
        "OWNER_UNRESOLVED": "name all four required ownership roles",
        "FALSE_NA": "supply detector-negative selectors or mark the concern required",
        "ILLEGAL_SELECTION": "select only outputs whose disposition is required",
        "CHANGED_PASS_TWO": "supersede changed inputs and restart at pass one",
        "ILLEGAL_EVIDENCE_STATE": "keep Plan evidence outside the Design result",
    }
    return {
        "code": code,
        "message": message,
        "selector": selector,
        "owner": owner,
        "repair": repairs[code],
    }


def classify_signal(signal: dict[str, Any]) -> str:
    signal_class = signal["signal_class"]
    attrs = signal.get("attributes", {})
    if signal_class == "human-actor":
        return "ux"
    if signal_class == "rendered-surface":
        return "ux"
    if signal_class == "interface":
        kind = str(attrs.get("kind", "")).lower()
        if "authenticated" in kind:
            return "security"
        if "operator" in kind:
            return "state-event"
        return "integration"
    if signal_class in {"store", "queue", "writer"}:
        return "persistence"
    if signal_class == "normative-rule":
        text = " ".join(
            str(attrs.get(key, "")) for key in ("verb", "subject", "object")
        ).lower()
        if any(word in text for word in ("admit", "authorize", "approve")):
            return "authority"
        if any(word in text for word in ("state", "transition", "terminal")):
            return "state-event"
        return "validation"
    if signal_class == "effect":
        if attrs.get("privileged") is True:
            return "authority"
        if attrs.get("external") is True or attrs.get("reversible") is False:
            return "failure"
        return "validation"
    if signal_class == "data-log-sink":
        return "privacy-data"
    if signal_class == "deployment":
        return "rollout"
    if signal_class == "compatibility":
        old = str(attrs.get("old_contract", "")).lower()
        new = str(attrs.get("new_contract", "")).lower()
        if "stored" in old or "stored" in new:
            return "migration"
        return "integration"
    if signal_class == "quality-claim":
        return "performance"
    if signal_class == "acceptance-readiness-claim":
        return "validation"
    raise ValueError(f"unsupported signal class: {signal_class}")


def required_predicate(
    primary_class: str,
    signals: list[dict[str, Any]],
    authored: dict[str, Any] | None,
) -> bool:
    if primary_class == "ux":
        actors = [
            signal
            for signal in signals
            if signal["signal_class"] == "human-actor"
            and signal.get("attributes", {}).get("natural_person") is True
            and any(
                signal.get("attributes", {}).get(action) is True
                for action in (
                    "reads",
                    "decides",
                    "acts",
                    "recovers",
                    "navigates",
                    "assistive_operation",
                )
            )
        ]
        surfaces = [
            signal
            for signal in signals
            if signal["signal_class"] == "rendered-surface"
            and signal.get("attributes", {}).get("semantic_change") in {"new", "changed"}
        ]
        return bool(actors and surfaces)
    if primary_class == "performance":
        return any(
            signal.get("attributes", {}).get("required") is True for signal in signals
        )
    if authored and authored.get("required_predicate") is not None:
        return bool(authored["required_predicate"])
    return bool(signals)


def default_ownership(primary_class: str) -> dict[str, Any]:
    artifact_owner = "ux-plan-owner" if primary_class == "ux" else "architecture-owner"
    if primary_class == "validation":
        artifact_owner = "plan-work-pack-owner"
    return {
        "accountable_owner": ACCOUNTABLE_OWNER[primary_class],
        "contributing_owners": ["architecture-owner", "plan-work-pack-owner"],
        "artifact_owner": artifact_owner,
        "validator_owner": VALIDATOR_ID,
    }


def ownership_valid(ownership: dict[str, Any]) -> bool:
    return (
        isinstance(ownership.get("accountable_owner"), str)
        and bool(ownership["accountable_owner"])
        and isinstance(ownership.get("artifact_owner"), str)
        and bool(ownership["artifact_owner"])
        and ownership.get("validator_owner") == VALIDATOR_ID
        and isinstance(ownership.get("contributing_owners"), list)
        and all(isinstance(item, str) and item for item in ownership["contributing_owners"])
    )


def normalized_block_ownership(ownership: dict[str, Any]) -> dict[str, Any]:
    contributing = [
        item
        for item in ownership.get("contributing_owners", [])
        if isinstance(item, str) and item
    ]
    return {
        "accountable_owner": ownership.get("accountable_owner")
        if isinstance(ownership.get("accountable_owner"), str)
        and ownership["accountable_owner"]
        else "unresolved-owner",
        "contributing_owners": contributing or ["unresolved-owner"],
        "artifact_owner": ownership.get("artifact_owner")
        if isinstance(ownership.get("artifact_owner"), str)
        and ownership["artifact_owner"]
        else "unresolved-owner",
        "validator_owner": VALIDATOR_ID,
    }


def build_pass(
    receipt: dict[str, Any],
    authored_concerns: list[dict[str, Any]],
    planned_witnesses: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    diagnostics: list[dict[str, Any]] = []
    signals = receipt["extracted_signals"]
    authored_by_id = {
        item["concern_id"]: item
        for item in authored_concerns
        if isinstance(item, dict) and isinstance(item.get("concern_id"), str)
    }
    signal_by_id = {item["signal_id"]: item for item in signals}
    bindings: dict[str, list[str]] = {}
    for signal in signals:
        try:
            primary = classify_signal(signal)
        except ValueError as error:
            diagnostics.append(
                diagnostic(
                    "UNBOUND_SIGNAL",
                    str(error),
                    signal.get("source_selector"),
                )
            )
            continue
        bindings.setdefault(primary, []).append(signal["signal_id"])

    for authored_id, authored in authored_by_id.items():
        primary = authored.get("primary_class")
        if primary not in PRIMARY_PRECEDENCE:
            diagnostics.append(
                diagnostic(
                    "UNBOUND_SIGNAL",
                    f"authored concern has unsupported primary class: {authored_id}",
                    authored_id,
                )
            )
            continue
        bindings.setdefault(primary, []).append(authored_id)

    bound_ids = {
        signal_id for signal_ids in bindings.values() for signal_id in signal_ids
    }
    expected_ids = set(receipt["denominator_signal_ids"])
    for missing_id in sorted(expected_ids - bound_ids):
        diagnostics.append(
            diagnostic(
                "UNBOUND_SIGNAL",
                f"denominator signal is unbound: {missing_id}",
                missing_id,
            )
        )
    for extra_id in sorted(bound_ids - expected_ids):
        diagnostics.append(
            diagnostic(
                "UNBOUND_SIGNAL",
                f"binding is not in denominator: {extra_id}",
                extra_id,
            )
        )

    illegal_witness = False
    for witness in planned_witnesses:
        if witness.get("evidence_state") in {
            "plan-evidence-pending",
            "plan-evidence-pass",
            "plan-evidence-fail",
            "executed",
        }:
            illegal_witness = True
            diagnostics.append(
                diagnostic(
                    "ILLEGAL_EVIDENCE_STATE",
                    "planned witness claims Plan or executed evidence inside Design",
                    witness.get("witness_id"),
                )
            )

    concerns = []
    selected_outputs = {"architecture"}
    for primary in PRIMARY_PRECEDENCE:
        signal_ids = sorted(set(bindings.get(primary, [])))
        if not signal_ids:
            continue
        authored_candidates = [
            authored_by_id[item]
            for item in signal_ids
            if item in authored_by_id
        ]
        authored = authored_candidates[0] if authored_candidates else None
        class_signals = [
            signal_by_id[item] for item in signal_ids if item in signal_by_id
        ]
        required = required_predicate(primary, class_signals, authored)
        detector_negative = not required
        evidence_selectors = sorted(
            {
                signal["source_selector"]
                for signal in class_signals
                if signal.get("source_selector")
            }
            | set((authored or {}).get("evidence_selectors", []))
        )
        requested = (authored or {}).get("disposition")
        if requested == "required" and not required:
            disposition = "block"
            diagnostics.append(
                diagnostic(
                    "ILLEGAL_SELECTION",
                    f"required disposition has a false predicate for {primary}",
                    signal_ids[0],
                )
            )
        elif requested == "not-applicable-with-rationale" and required:
            disposition = "block"
            diagnostics.append(
                diagnostic(
                    "FALSE_NA",
                    f"negative disposition contradicts extracted {primary} signal",
                    signal_ids[0],
                )
            )
        elif requested == "not-applicable-with-rationale" and not evidence_selectors:
            disposition = "block"
            diagnostics.append(
                diagnostic(
                    "FALSE_NA",
                    f"negative disposition lacks detector evidence for {primary}",
                    signal_ids[0],
                )
            )
        elif requested in {
            "required",
            "recommended",
            "not-applicable-with-rationale",
            "block",
        }:
            disposition = requested
        elif required:
            disposition = "required"
        elif primary == "performance":
            disposition = "recommended"
        else:
            disposition = "not-applicable-with-rationale"

        ownership = copy.deepcopy(
            (authored or {}).get("ownership") or default_ownership(primary)
        )
        if not ownership_valid(ownership):
            disposition = "block"
            diagnostics.append(
                diagnostic(
                    "OWNER_UNRESOLVED",
                    f"ownership is incomplete for {primary}",
                    signal_ids[0],
                    ownership.get("accountable_owner"),
                )
            )
            ownership = normalized_block_ownership(ownership)

        output_id = OUTPUT_BY_CLASS[primary]
        if primary == "validation" and illegal_witness:
            disposition = "block"
        selected = disposition == "required"
        if (authored or {}).get("selected") is True and disposition != "required":
            diagnostics.append(
                diagnostic(
                    "ILLEGAL_SELECTION",
                    f"non-required {primary} output was selected",
                    signal_ids[0],
                )
            )
            selected = False
        if selected:
            selected_outputs.add(output_id)
        concerns.append(
            {
                "concern_id": f"concern:{primary}",
                "signal_ids": signal_ids,
                "primary_class": primary,
                "ownership": ownership,
                "disposition": disposition,
                "predicate_evidence": {
                    "required_predicate": required,
                    "detector_negative": detector_negative,
                    "evidence_selectors": evidence_selectors,
                },
                "output_id": output_id if disposition in {"required", "recommended"} else None,
                "selected": selected,
                "rationale": (authored or {}).get(
                    "rationale",
                    f"{primary} disposition follows normalized extracted signals",
                ),
                "revisit_condition": (
                    (authored or {}).get("revisit_condition")
                    if disposition == "recommended"
                    else None
                )
                or ("re-evaluate when the bounded hypothesis changes" if disposition == "recommended" else None),
            }
        )

    pass_value = {
        "concerns": concerns,
        "selected_outputs": sorted(selected_outputs),
        "diagnostics": sorted(
            diagnostics,
            key=lambda item: (
                item["code"],
                item["selector"] or "",
                item["message"],
            ),
        ),
    }
    return pass_value, pass_value["diagnostics"]


def blocking_result(
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    diagnostics: list[dict[str, Any]],
    pass_1: dict[str, Any] | None = None,
    pass_2: dict[str, Any] | None = None,
) -> dict[str, Any]:
    pass_1 = pass_1 or {"concerns": [], "selected_outputs": [], "diagnostics": diagnostics}
    pass_2 = pass_2 or pass_1
    result = {
        "schema_version": "1.0.0",
        "manifest_id": manifest.get("manifest_id", "invalid-manifest"),
        "manifest_input_digest": manifest.get("input_digest", "0" * 64),
        "denominator_receipt_digest": receipt.get("receipt_digest", "0" * 64),
        "concerns": pass_1.get("concerns", []),
        "selected_outputs": [],
        "pass_1_digest": canonical_digest(pass_1),
        "pass_2_digest": canonical_digest(pass_2),
        "fixed_point": False,
        "evidence_state": "authored-complete",
        "verdict": "block",
        "diagnostics": sorted(
            diagnostics,
            key=lambda item: (
                item["code"],
                item["selector"] or "",
                item["message"],
            ),
        ),
        "result_digest": "0" * 64,
    }
    result["result_digest"] = digest_without(result, "result_digest")
    return result


def validate_selection(
    manifest: dict[str, Any],
    receipt: dict[str, Any],
    authored_concerns: list[dict[str, Any]],
    planned_witnesses: list[dict[str, Any]],
    schemas: dict[str, dict[str, Any]],
    pass_two_transform: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    early: list[dict[str, Any]] = []
    manifest_errors = schema_errors(manifest, schemas["manifest"], "manifest")
    if manifest_errors:
        early.append(diagnostic("MANIFEST_NOT_CLOSED", "; ".join(manifest_errors)))
    receipt_errors = schema_errors(receipt, schemas["receipt"], "denominator receipt")
    if receipt_errors:
        code = (
            "SELF_ISSUED_RECEIPT"
            if receipt.get("manifest_authored_by") == receipt.get("detector_id")
            else "MISSING_DETECTOR_INPUT"
        )
        early.append(diagnostic(code, "; ".join(receipt_errors)))
    if early:
        return blocking_result(manifest, receipt, early)

    manifest_material = {key: value for key, value in manifest.items() if key != "input_digest"}
    if canonical_digest(manifest_material) != manifest["input_digest"]:
        early.append(diagnostic("MANIFEST_NOT_CLOSED", "manifest input digest is stale"))
    if receipt["manifest_id"] != manifest["manifest_id"]:
        early.append(
            diagnostic("STALE_DENOMINATOR_RECEIPT", "receipt manifest id mismatch")
        )
    if receipt["manifest_input_digest"] != manifest["input_digest"]:
        early.append(
            diagnostic("STALE_DENOMINATOR_RECEIPT", "receipt manifest digest mismatch")
        )
    if receipt["manifest_authored_by"] == receipt["detector_id"]:
        early.append(
            diagnostic("SELF_ISSUED_RECEIPT", "manifest author equals detector identity")
        )
    if digest_without(receipt, "receipt_digest") != receipt["receipt_digest"]:
        early.append(
            diagnostic("STALE_DENOMINATOR_RECEIPT", "receipt digest mismatch")
        )
    if receipt["verdict"] != "pass" or receipt["missing_detector_inputs"]:
        early.append(
            diagnostic("MISSING_DETECTOR_INPUT", "denominator receipt is not complete")
        )
    if receipt["unbound_signal_ids"]:
        early.append(
            diagnostic(
                "UNBOUND_SIGNAL",
                "denominator receipt contains unbound signals",
                receipt["unbound_signal_ids"][0],
            )
        )
    if early:
        return blocking_result(manifest, receipt, early)

    pass_1, diagnostics_1 = build_pass(
        receipt, copy.deepcopy(authored_concerns), copy.deepcopy(planned_witnesses)
    )
    second_authored = copy.deepcopy(authored_concerns)
    if pass_two_transform is not None:
        transformed = pass_two_transform({"authored_concerns": second_authored})
        second_authored = transformed.get("authored_concerns", second_authored)
    pass_2, diagnostics_2 = build_pass(
        receipt, second_authored, copy.deepcopy(planned_witnesses)
    )
    pass_1_digest = canonical_digest(pass_1)
    pass_2_digest = canonical_digest(pass_2)
    diagnostics = diagnostics_1
    if pass_1_digest != pass_2_digest:
        diagnostics = diagnostics + [
            diagnostic(
                "CHANGED_PASS_TWO",
                "pass two changed concerns, ownership, disposition, output, or diagnostics",
            )
        ]
    if diagnostics or diagnostics_2:
        return blocking_result(
            manifest,
            receipt,
            diagnostics + [item for item in diagnostics_2 if item not in diagnostics],
            pass_1,
            pass_2,
        )

    result = {
        "schema_version": "1.0.0",
        "manifest_id": manifest["manifest_id"],
        "manifest_input_digest": manifest["input_digest"],
        "denominator_receipt_digest": receipt["receipt_digest"],
        "concerns": pass_1["concerns"],
        "selected_outputs": pass_1["selected_outputs"],
        "pass_1_digest": pass_1_digest,
        "pass_2_digest": pass_2_digest,
        "fixed_point": True,
        "evidence_state": "design-validator-pass",
        "verdict": "pass",
        "diagnostics": [],
        "result_digest": "0" * 64,
    }
    result["result_digest"] = digest_without(result, "result_digest")
    result_errors = schema_errors(result, schemas["result"], "selection result")
    if result_errors:
        return blocking_result(
            manifest,
            receipt,
            [diagnostic("ILLEGAL_SELECTION", "; ".join(result_errors))],
            pass_1,
            pass_2,
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("denominator_receipt")
    parser.add_argument("--authored-concerns", required=True)
    parser.add_argument("--planned-witnesses", required=True)
    parser.add_argument("--schema-dir")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    schema_dir = (
        Path(args.schema_dir)
        if args.schema_dir
        else Path(__file__).resolve().parent.parent / "schemas"
    )
    authored_doc = load_json(Path(args.authored_concerns))
    witnesses_doc = load_json(Path(args.planned_witnesses))
    result = validate_selection(
        load_json(Path(args.manifest)),
        load_json(Path(args.denominator_receipt)),
        authored_doc.get("concerns", []),
        witnesses_doc.get("witnesses", []),
        {
            "manifest": load_json(schema_dir / "design-scope-manifest.schema.json"),
            "receipt": load_json(
                schema_dir / "design-denominator-receipt.schema.json"
            ),
            "result": load_json(schema_dir / "design-selection-result.schema.json"),
        },
    )
    Path(args.output).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
