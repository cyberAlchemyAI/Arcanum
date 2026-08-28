#!/usr/bin/env python3
"""Shared validation for the current Invoke Design v3 stage and v2 admission."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver


OUTPUTS = (
    ("design-artifact", "DESIGN.json"),
    ("architecture", "ARCHITECTURE.md"),
    ("selected-companions", "SELECTED-COMPANIONS.md"),
    ("glossary-consistency", "GLOSSARY-CONSISTENCY-REPORT.json"),
    ("planned-witnesses", "PLANNED-WITNESS-CONTRACTS.json"),
    ("layering", "IMPLEMENTATION-LAYERING.md"),
    ("template-selection", "TEMPLATE-SELECTION-RECEIPT.json"),
    ("dispatch-trace", "DISPATCH-TRACE.json"),
    ("distill", "DISTILL-RECEIPT.json"),
    ("scope-manifest", "DESIGN-SCOPE-MANIFEST.json"),
    ("denominator-receipt", "DESIGN-DENOMINATOR-RECEIPT.json"),
    ("selection-result", "DESIGN-SELECTION-RESULT.json"),
    ("coherence-receipt", "DESIGN-COHERENCE-RECEIPT.json"),
    ("transport", "DESIGN-TRANSPORT-REPORT.json"),
)
STAGE_NAME = "INVOKE-DESIGN-STAGE-RECEIPT.json"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_source_v3.py"
ADMISSION_PATH = "arcanum/spells/invoke/scripts/validate_design_bundle_admission_v2.py"


def digest_without(document: dict[str, Any], field: str) -> str:
    value = copy.deepcopy(document)
    value.pop(field, None)
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def file_ref(path: Path, label: str) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": label, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def _schema_store(schema_dir: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in schema_dir.glob("*.schema.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(value, dict) and isinstance(value.get("$id"), str):
            result[value["$id"]] = value
    return result


def schema_diagnostics(
    document: Any, schema: dict[str, Any], label: str, store: dict[str, dict[str, Any]]
) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store)
    return [
        f"{label} schema invalid at {'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, resolver=resolver).iter_errors(document),
            key=lambda item: list(item.path),
        )
    ]


def validate_stage_receipt(
    receipt: Any,
    repo_root: Path,
    schema_dir: Path,
    bundle_dir: Path | None = None,
) -> list[str]:
    if not isinstance(receipt, dict):
        return ["Design PASS requires an exact v3 producer receipt"]
    version = receipt.get("schema_version")
    if version in {"invoke.design-stage-receipt.v1", "invoke.design-stage-receipt.v2"}:
        return [f"{version} is historical/read-only and cannot establish a new PASS"]
    if version != "invoke.design-stage-receipt.v3":
        return [f"unsupported Design producer receipt version: {version!r}"]
    diagnostics: list[str] = []
    store = _schema_store(schema_dir)
    schema = store.get("https://arcanum.dev/schemas/invoke/design-result/v3")
    if schema is None:
        return ["current Design stage schema is unavailable"]
    diagnostics.extend(schema_diagnostics(receipt, schema, "Design producer receipt", store))
    if diagnostics:
        return diagnostics
    if receipt["receipt_digest"] != digest_without(receipt, "receipt_digest"):
        diagnostics.append("Design producer receipt digest mismatch")
    producer_path = repo_root / PRODUCER_PATH
    if (
        not producer_path.is_file()
        or receipt["producer"]["sha256"] != hashlib.sha256(producer_path.read_bytes()).hexdigest()
    ):
        diagnostics.append("Design producer identity digest mismatch")
    if [(item["kind"], item["path"]) for item in receipt["outputs"]] != list(OUTPUTS):
        diagnostics.append("Design producer ordered output inventory mismatch")
    if (
        receipt.get("result") != "pass"
        or receipt.get("distill_state") != "pass"
        or receipt.get("authority_effect") != "none"
    ):
        diagnostics.append("Design producer receipt is not a no-effect PASS")
    if bundle_dir is not None:
        expected_names = {name for _, name in OUTPUTS} | {STAGE_NAME}
        try:
            entries = {item.name: item for item in bundle_dir.iterdir()}
        except OSError as error:
            return diagnostics + [f"Design bundle cannot be read: {error}"]
        if set(entries) != expected_names or any(
            not item.is_file() or item.is_symlink() for item in entries.values()
        ):
            diagnostics.append("Design bundle inventory is not exactly fifteen regular files")
        else:
            for item, (kind, name) in zip(receipt["outputs"], OUTPUTS, strict=True):
                if item != {"kind": kind, **file_ref(entries[name], name)}:
                    diagnostics.append(f"Design stage output binding mismatch: {name}")
                    break
    return diagnostics


def validate_admission_receipt(
    admission: Any,
    producer: Any,
    repo_root: Path,
    schema_dir: Path,
) -> list[str]:
    if not isinstance(admission, dict):
        return ["Design PASS requires an independent v2 bundle admission receipt"]
    if not isinstance(producer, dict):
        return ["Design admission cannot be evaluated without its stage receipt"]
    version = admission.get("schema_version")
    if version == "invoke.design-bundle-admission-receipt.v1":
        return ["invoke.design-bundle-admission-receipt.v1 is historical/read-only"]
    if version != "invoke.design-bundle-admission-receipt.v2":
        return [f"unsupported Design admission receipt version: {version!r}"]
    diagnostics: list[str] = []
    store = _schema_store(schema_dir)
    schema = store.get("https://arcanum.dev/schemas/invoke/design-bundle-admission-receipt/v2")
    if schema is None:
        return ["current Design admission schema is unavailable"]
    diagnostics.extend(schema_diagnostics(admission, schema, "Design admission receipt", store))
    if diagnostics:
        return diagnostics
    if admission["receipt_digest"] != digest_without(admission, "receipt_digest"):
        diagnostics.append("Design admission receipt digest mismatch")
    validator_path = repo_root / ADMISSION_PATH
    if (
        not validator_path.is_file()
        or admission["validator"]["sha256"] != hashlib.sha256(validator_path.read_bytes()).hexdigest()
    ):
        diagnostics.append("Design admission validator identity digest mismatch")
    expected_binding = {
        "receipt_id": producer.get("receipt_id"),
        "receipt_digest": producer.get("receipt_digest"),
        "profile_id": producer.get("profile_id"),
        "producer": producer.get("producer"),
    }
    if admission["producer_binding"] != expected_binding:
        diagnostics.append("Design producer/admission binding mismatch")
    if admission["replay"]["bundle_closure_ref"] != producer.get("bindings", {}).get("bundle_closure_ref"):
        diagnostics.append("Design admission bundle-closure replay binding mismatch")
    if admission["replay"]["candidate_receipt_ref"] != producer.get("bindings", {}).get("candidate_production_receipt_ref"):
        diagnostics.append("Design admission candidate replay binding mismatch")
    if len(admission["output_inventory"]) != 15:
        diagnostics.append("Design admission inventory must contain fifteen entries")
    else:
        for produced, admitted in zip(producer.get("outputs", []), admission["output_inventory"][:14], strict=False):
            if (
                produced.get("kind") != admitted.get("kind")
                or Path(produced.get("path", "")).name != Path(admitted.get("path", "")).name
                or produced.get("sha256") != admitted.get("sha256")
                or produced.get("size") != admitted.get("size")
            ):
                diagnostics.append("Design stage/admission output inventory mismatch")
                break
        terminal = admission["output_inventory"][-1]
        terminal_ref = {key: terminal[key] for key in ("path", "sha256", "size")}
        if terminal.get("kind") != "stage-receipt" or terminal_ref != admission["stage_receipt_ref"]:
            diagnostics.append("Design admission terminal stage receipt binding mismatch")
    inventory_digest = hashlib.sha256(
        json.dumps(admission["output_inventory"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if admission["replay"]["output_inventory_digest"] != inventory_digest:
        diagnostics.append("Design admission output inventory digest mismatch")
    if (
        admission["result"] != "pass"
        or admission["blockers"]
        or admission["replay"]["comparison"] != "pass"
        or admission["replay"]["differences"]
        or any(item["status"] != "pass" for item in admission["checks"])
        or admission["authority_effect"] != "none"
    ):
        diagnostics.append("Design admission is not a clean replay PASS")
    return diagnostics
