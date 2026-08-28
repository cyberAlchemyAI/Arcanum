#!/usr/bin/env python3
"""Project one Design source into the deterministic W2 candidate artifact."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, RefResolver


PROCESS_PATH = "arcanum/spells/invoke/development/whole-invoke-repair-plan/design-process/DESIGN-PRODUCTION-PROCESS.json"
PROFILE_PATH = "arcanum/spells/invoke/development/whole-invoke-repair-plan/design-process/DESIGN-PROFILE.json"
POLICY_PATH = "arcanum/spells/invoke/development/whole-invoke-repair-plan/design-process/DESIGN-COHERENCE-POLICY.json"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest_without(document: dict[str, Any], field: str) -> str:
    return hashlib.sha256(canonical_bytes({k: v for k, v in document.items() if k != field})).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def exact_ref(path: Path, root: Path) -> dict[str, Any]:
    lexical = Path(os.path.abspath(path))
    try:
        label = lexical.relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise ValueError(f"path outside repository: {path}") from error
    current = root.resolve()
    for part in Path(label).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"symlink path component is forbidden: {label}")
    if not lexical.is_file():
        raise ValueError(f"expected regular non-symlink file: {label}")
    data = lexical.read_bytes()
    return {"path": label, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def sorted_copy(items: list[dict[str, Any]], *keys: str) -> list[dict[str, Any]]:
    return sorted(copy.deepcopy(items), key=lambda item: tuple(str(item[key]) for key in keys))


SET_ARRAY_KEYS = {"fact_ids", "requirement_refs", "evidence_refs", "na_evidence_refs", "signal_ids", "surfaces", "data_classes", "writers", "producers", "consumers", "targets", "contract_ids", "next_step_ids", "allowed_next_state_ids", "techniques", "target_fact_ids", "unmapped_terms", "deltas"}


def normalize_sets(value: Any, key: str | None = None) -> Any:
    if isinstance(value, dict):
        return {item_key: normalize_sets(item, item_key) for item_key, item in value.items()}
    if isinstance(value, list):
        normalized = [normalize_sets(item) for item in value]
        return sorted(normalized, key=canonical_bytes) if key in SET_ARRAY_KEYS else normalized
    return value


def project_design_artifact(
    source: dict[str, Any],
    source_ref: dict[str, Any],
    process_ref: dict[str, Any],
    profile_ref: dict[str, Any],
    policy_ref: dict[str, Any],
    selection: dict[str, Any],
) -> dict[str, Any]:
    applications = sorted_copy(source["applications"], "subject_kind", "subject_id")
    pairs = [(item["subject_kind"], item["subject_id"]) for item in applications]
    if len(pairs) != len(set(pairs)):
        raise ValueError("duplicate typed application pairs are not projectable")
    applications = normalize_sets(applications)
    application_by_pair = {(item["subject_kind"], item["subject_id"]): item for item in applications}
    concern_trace = []
    for concern in sorted(selection["concerns"], key=lambda item: item["concern_id"]):
        application = application_by_pair[("selection-concern", concern["concern_id"])]
        concern_trace.append({
            "concern_id": concern["concern_id"],
            "primary_class": concern["primary_class"],
            "disposition": concern["disposition"],
            "signal_ids": sorted(concern["signal_ids"]),
            "application_ref": {"subject_kind": "selection-concern", "subject_id": concern["concern_id"]},
            "fact_ids": sorted(application["fact_ids"]),
            "selected_output_id": concern["output_id"] if concern["selected"] else None,
        })

    views = copy.deepcopy(source["views"])
    for view in views.values():
        view["fact_ids"] = sorted(view["fact_ids"])
        view["na_evidence_refs"] = sorted(view["na_evidence_refs"], key=lambda item: (item["path"], item["sha256"], item["size"]))

    artifact: dict[str, Any] = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-artifact/v1",
        "schema_version": "invoke.design-artifact.v1",
        "artifact_id": f"{source['source_id']}:candidate:v1",
        "artifact_status": "candidate",
        "owner_route": "invoke-design-candidate-producer",
        "target_id": source["target_id"],
        "activation_kind": source["activation_kind"],
        "profile_id": source["profile_binding"]["profile_id"],
        "design_kind": normalize_sets(copy.deepcopy(source["design_kind"])),
        "evidence_bindings": {
            "process_ref": copy.deepcopy(process_ref),
            "profile_ref": copy.deepcopy(profile_ref),
            "coherence_policy_ref": copy.deepcopy(policy_ref),
            "design_input_production_receipt_ref": copy.deepcopy(source["upstream_bindings"]["design_input_production_receipt_ref"]),
            "design_input_closure_ref": copy.deepcopy(source["upstream_bindings"]["design_input_closure_ref"]),
            "design_input_closure_receipt_ref": copy.deepcopy(source["upstream_bindings"]["design_input_closure_receipt_ref"]),
            "scope_manifest_ref": copy.deepcopy(source["upstream_bindings"]["scope_manifest_ref"]),
            "denominator_receipt_ref": copy.deepcopy(source["upstream_bindings"]["denominator_receipt_ref"]),
            "selection_result_ref": copy.deepcopy(source["upstream_bindings"]["selection_result_ref"]),
            "design_source_ref": copy.deepcopy(source_ref),
        },
        "applications": applications,
        "facts": normalize_sets(sorted_copy(source["facts"], "fact_id")),
        "views": views,
        "selected_outputs": sorted(source["selected_outputs"]),
        "selected_companions": normalize_sets(sorted_copy(source["selected_companions"], "output_id")),
        "concern_trace": concern_trace,
        "glossary_application": copy.deepcopy(source["glossary_application"]),
        "planned_witnesses": normalize_sets(sorted_copy(source["planned_witnesses"], "witness_id")),
        "unresolved_gaps": sorted_copy(source["unresolved_gaps"], "gap_id"),
        "layering": copy.deepcopy(source["layering"]),
        "template_selection": copy.deepcopy(source["template_selection"]),
        "dispatch_trace": normalize_sets(copy.deepcopy(source["dispatch_trace"])),
        "distill_contract": copy.deepcopy(source["distill_contract"]),
        "transport_policy": copy.deepcopy(source["transport_policy"]),
        "selection_evidence_state": "design-validator-pass",
        "coherence_evidence_state": "pending-independent-receipt",
        "plan_evidence_state": "plan-evidence-pending",
        "next_route": "design-bundle-production",
        "evidence_ceiling": "w2-candidate-coherence-only",
        "authority_effect": "none",
        "artifact_digest": "0" * 64,
    }
    artifact["glossary_application"]["mappings"] = normalize_sets(sorted_copy(artifact["glossary_application"]["mappings"], "term"))
    artifact["glossary_application"]["unmapped_terms"] = sorted(artifact["glossary_application"]["unmapped_terms"])
    artifact["artifact_digest"] = digest_without(artifact, "artifact_digest")
    return artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--schema-dir")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    source_path = Path(args.source)
    source = load_json(source_path)
    selection_path = root / source["upstream_bindings"]["selection_result_ref"]["path"]
    if source.get("source_digest") != digest_without(source, "source_digest"):
        raise SystemExit("source self digest mismatch")
    if exact_ref(selection_path, root) != source["upstream_bindings"]["selection_result_ref"]:
        raise SystemExit("selection result binding mismatch")
    selection = load_json(selection_path)
    if selection.get("result_digest") != digest_without(selection, "result_digest") or selection.get("verdict") != "pass":
        raise SystemExit("selection result is not self-digested PASS")
    artifact = project_design_artifact(
        source,
        exact_ref(source_path, root),
        exact_ref(root / PROCESS_PATH, root),
        exact_ref(root / PROFILE_PATH, root),
        exact_ref(root / POLICY_PATH, root),
        selection,
    )
    output = Path(args.output)
    schema_dir = Path(args.schema_dir) if args.schema_dir else root / "arcanum/spells/invoke/schemas"
    store = {}
    for path in schema_dir.glob("*.schema.json"):
        schema = load_json(path)
        if "$id" in schema:
            store[schema["$id"]] = schema
    artifact_schema = store.get("https://arcanum.dev/schemas/invoke/design-artifact/v1")
    if artifact_schema is None:
        raise SystemExit("artifact schema unavailable")
    errors = list(Draft202012Validator(artifact_schema, resolver=RefResolver.from_schema(artifact_schema, store=store)).iter_errors(artifact))
    if errors:
        raise SystemExit(f"projected artifact schema invalid: {errors[0].message}")
    if not output.is_absolute() or output.exists() or output.is_symlink() or not output.parent.is_dir() or output.parent.is_symlink():
        raise SystemExit("output must be an absolute absent path with an existing safe parent")
    try:
        output.relative_to(root)
    except ValueError as error:
        raise SystemExit("output must remain inside --repo-root") from error
    fd, temporary = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(artifact, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, output)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
