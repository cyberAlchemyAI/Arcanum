#!/usr/bin/env python3
"""Shared validation for current and historical Invoke Plan receipts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def digest_without(document: dict[str, Any], field: str) -> str:
    projection = {key: value for key, value in document.items() if key != field}
    return hashlib.sha256(json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def canonical_file_bytes(document: Any) -> bytes:
    return (json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def schema_errors(document: Any, path: Path, label: str) -> list[str]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    return [f"{label} schema invalid at /{'/'.join(map(str, error.absolute_path))}: {error.message}" for error in sorted(Draft202012Validator(schema).iter_errors(document), key=lambda item: (list(item.absolute_path), item.message))]


def validate_stage_receipt(receipt: Any, repo_root: Path, schema_dir: Path) -> list[str]:
    if not isinstance(receipt, dict): return ["Plan PASS requires an exact v2 producer receipt"]
    version = receipt.get("schema_version")
    if version == "invoke.plan-stage-receipt.v1": return ["invoke.plan-stage-receipt.v1 is historical/read-only"]
    if version != "invoke.plan-stage-receipt.v2": return [f"unsupported Plan producer receipt version: {version!r}"]
    errors = schema_errors(receipt, schema_dir / "plan-stage-receipt-v2.schema.json", "Plan producer receipt")
    if errors: return errors
    if receipt["receipt_digest"] != digest_without(receipt, "receipt_digest"): errors.append("Plan producer receipt digest mismatch")
    producer_candidates = [repo_root / "arcanum/spells/invoke/scripts/compile_plan_bundle_v2.py", repo_root / ".agents/skills/invoke/scripts/compile_plan_bundle_v2.py", repo_root / ".claude/skills/invoke/scripts/compile_plan_bundle_v2.py"]
    producers = [path for path in producer_candidates if path.is_file()]
    if not producers or receipt["producer"]["sha256"] not in {hashlib.sha256(path.read_bytes()).hexdigest() for path in producers}: errors.append("Plan producer identity digest mismatch")
    expected_consumers = ["wpra", "implementation-readiness", "task-session", "context-builder", "dispatch-spec", "goal", "signal-observer"]
    if [row.get("consumer") for row in receipt["consumer_results"]] != expected_consumers: errors.append("Plan consumer result inventory mismatch")
    if any(row.get("result") not in {"pass", "negative_evidence"} for row in receipt["consumer_results"]): errors.append("Plan producer contains a blocked consumer")
    return errors


def validate_admission_receipt(admission: Any, producer: Any, repo_root: Path, schema_dir: Path) -> list[str]:
    if not isinstance(admission, dict): return ["Plan PASS requires an independent bundle admission receipt"]
    if not isinstance(producer, dict): return ["Plan admission cannot be evaluated without its producer receipt"]
    errors = schema_errors(admission, schema_dir / "plan-bundle-admission-receipt-v1.schema.json", "Plan admission receipt")
    if errors: return errors
    if admission["receipt_digest"] != digest_without(admission, "receipt_digest"): errors.append("Plan admission receipt digest mismatch")
    validator_candidates = [repo_root / "arcanum/spells/invoke/scripts/validate_plan_bundle_admission.py", repo_root / ".agents/skills/invoke/scripts/validate_plan_bundle_admission.py", repo_root / ".claude/skills/invoke/scripts/validate_plan_bundle_admission.py"]
    validators = [path for path in validator_candidates if path.is_file()]
    if not validators or admission.get("validator", {}).get("sha256") not in {hashlib.sha256(path.read_bytes()).hexdigest() for path in validators}: errors.append("Plan admission validator identity digest mismatch")
    producer_bytes = canonical_file_bytes(producer)
    stage_ref = admission.get("stage_receipt_ref", {})
    if Path(stage_ref.get("path", "")).name != "PLAN-STAGE-RECEIPT.json" or stage_ref.get("sha256") != hashlib.sha256(producer_bytes).hexdigest() or stage_ref.get("size") != len(producer_bytes): errors.append("Plan producer/admission stage binding mismatch")
    if admission.get("bundle_inventory") != admission.get("replay_inventory"): errors.append("Plan admission replay inventory mismatch")
    if admission.get("result") != "pass" or admission.get("blockers") or admission.get("authority_effect") != "none": errors.append("Plan admission is not a clean no-authority PASS")
    if admission.get("consumer_results") != producer.get("consumer_results"): errors.append("Plan producer/admission consumer results mismatch")
    return errors
