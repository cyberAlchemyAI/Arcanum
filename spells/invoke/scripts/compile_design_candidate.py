#!/usr/bin/env python3
"""Compile one normal W1-bound Design source into an atomic W2 candidate bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from jsonschema import Draft202012Validator, RefResolver

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from project_design_artifact import (  # noqa: E402
    POLICY_PATH,
    PROCESS_PATH,
    PROFILE_PATH,
    digest_without,
    exact_ref,
    load_json,
    project_design_artifact,
)
from validate_design_coherence import (  # noqa: E402
    ContractFailure,
    safe_path,
    schema_errors,
    schema_store,
    validate_design_coherence,
    verify_ref,
)


IDENTITY = "invoke.compile-design-candidate.v1"
OWNER = "invoke-design-candidate-producer"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_candidate.py"
STAGE_IDS = ("source-validation", "artifact-projection", "coherence-validation", "candidate-output-closure")
ARTIFACT_NAME = "DESIGN.json"
COHERENCE_NAME = "DESIGN-COHERENCE-RECEIPT.json"
RECEIPT_NAME = "DESIGN-CANDIDATE-PRODUCTION-RECEIPT.json"


class GovernedBlock(ValueError):
    def __init__(self, code: str, message: str, stage_index: int, selector: str | None = None, route: str = "repair-design-source", coherence_receipt: dict[str, Any] | None = None):
        super().__init__(message)
        self.code, self.stage_index, self.selector, self.route = code, stage_index, selector, route
        self.coherence_receipt = coherence_receipt


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def atomic_write_json(path: Path, document: dict[str, Any]) -> None:
    if path.exists():
        raise ValueError(f"attempt receipt already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def output_ref(path: Path, kind: str) -> dict[str, Any]:
    data = path.read_bytes()
    return {"kind": kind, "path": path.name, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def blocker(code: str, message: str, selector: str | None, route: str) -> dict[str, Any]:
    owner = "design-input-owner" if route == "repair-w1-input" else "invoke-contract-owner" if route == "repair-installed-contract" else "design-author"
    return {"blocker_id": f"w2-blocker:{code.lower()}", "code": code, "message": message, "selector": selector, "owner": owner, "repair_route": route}


def stages(failed_index: int | None, blocker_ids: list[str]) -> list[dict[str, Any]]:
    result = []
    for index, stage_id in enumerate(STAGE_IDS):
        if failed_index is None or index < failed_index:
            status, causal = "pass", []
        elif index == failed_index:
            status, causal = "block", blocker_ids
        else:
            status, causal = "not_evaluable", blocker_ids
        result.append({"stage_id": stage_id, "status": status, "causal_blocker_ids": causal})
    return result


def make_receipt(source_ref: dict[str, Any], w1_ref: dict[str, Any], bindings: dict[str, Any], producer_digest: str, result: str, outputs: list[dict[str, Any]], failed_index: int | None = None, blockers: list[dict[str, Any]] | None = None, route: str = "repair-design-source", coherence_block_receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    blocker_values = copy.deepcopy(blockers or [])
    passed = 4 if failed_index is None else failed_index
    receipt = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1",
        "schema_version": "invoke.design-candidate-production-receipt.v1",
        "receipt_id": f"design-w2:{source_ref['sha256'][:24]}",
        "producer": {"identity": IDENTITY, "owner": OWNER, "path": PRODUCER_PATH, "sha256": producer_digest},
        "bindings": copy.deepcopy(bindings), "source_ref": copy.deepcopy(source_ref),
        "w1_production_receipt_ref": copy.deepcopy(w1_ref),
        "coherence_block_receipt": copy.deepcopy(coherence_block_receipt),
        "stage_results": stages(failed_index, [item["blocker_id"] for item in blocker_values]),
        "outputs": copy.deepcopy(outputs), "result": result,
        "next_route": "design-bundle-production" if result == "pass" else route,
        "blockers": blocker_values,
        "evidence_ceiling": {
            "normal_w1_bound": passed >= 1, "source_complete": passed >= 1,
            "candidate_projected": passed >= 2, "coherence_validated": passed >= 3,
            "human_views_produced": False, "design_stage_pass": False, "plan_evidence": False,
            "acceptance": False, "execution": False, "publication": False, "deployment": False, "external_effect": False,
        },
        "authority_effect": "none", "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    return receipt


def safe_absent_destination(path: Path, root: Path | None = None) -> Path:
    if not path.is_absolute():
        raise ValueError("destination paths must be absolute")
    lexical = Path(os.path.abspath(path))
    if lexical.exists() or lexical.is_symlink():
        raise ValueError(f"destination must be absent and not a symlink: {lexical}")
    parent = lexical.parent
    if not parent.is_dir() or parent.is_symlink():
        raise ValueError(f"destination parent must be an existing non-symlink directory: {parent}")
    current = Path(lexical.anchor)
    for part in parent.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"destination parent contains a symlink: {current}")
    if root is not None:
        try:
            lexical.relative_to(root.resolve())
        except ValueError as error:
            raise ValueError("output directory must be inside --repo-root") from error
    return lexical


def preflight_w1(source: dict[str, Any], root: Path, store: dict[str, dict[str, Any]]) -> dict[str, Any]:
    refs = source["upstream_bindings"]
    w1_ref = refs["design_input_production_receipt_ref"]
    w1_path = verify_ref(root, w1_ref)
    required_schema_ids = ["https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1", "https://arcanum.dev/schemas/invoke/design-input-closure/v1", "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1", "https://arcanum.dev/schemas/invoke/design-scope-manifest/1-0-0", "https://arcanum.dev/schemas/invoke/design-denominator-receipt/1-0-0", "https://arcanum.dev/schemas/invoke/design-selection-result/1-0-0"]
    missing = [item for item in required_schema_ids if item not in store]
    if missing:
        raise GovernedBlock("PROFILE_INVALID", f"installed W1 schemas unavailable: {missing}", 0, None, "repair-installed-contract")
    try:
        w1 = load_json(w1_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise GovernedBlock("W1_RECEIPT_INVALID", f"W1 receipt is unreadable: {error}", 0, w1_ref["path"], "repair-w1-input") from error
    errors = schema_errors(w1, store["https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1"], store)
    if errors or w1.get("result") != "pass" or w1.get("activation_kind") != "normal" or w1.get("next_route") != "design-authoring" or w1.get("receipt_digest") != digest_without(w1, "receipt_digest"):
        raise GovernedBlock("W1_RECEIPT_INVALID", "; ".join(errors[:5]) or "W1 receipt is not current normal PASS", 0, w1_ref["path"], "repair-w1-input")
    installed_w1_digest = exact_ref(root / "arcanum/spells/invoke/scripts/compile_design_input_bundle.py", root)["sha256"]
    if w1["producer"]["sha256"] != installed_w1_digest:
        raise GovernedBlock("W1_RECEIPT_INVALID", "W1 producer digest differs from the installed producer", 0, w1_ref["path"], "repair-w1-input")
    expected_names = ["DESIGN-INPUT-CLOSURE-RECEIPT.json", "DESIGN-SCOPE-MANIFEST.json", "DESIGN-DENOMINATOR-RECEIPT.json", "DESIGN-SELECTION-RESULT.json"]
    if [item["path"] for item in w1["outputs"]] != expected_names:
        raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", "W1 output inventory is not exact", 0, w1_ref["path"], "repair-w1-input")
    keys = ["design_input_closure_receipt_ref", "scope_manifest_ref", "denominator_receipt_ref", "selection_result_ref"]
    parent = PurePosixPath(w1_ref["path"]).parent
    for key, output in zip(keys, w1["outputs"]):
        verify_ref(root, refs[key])
        if refs[key] != {"path": (parent / output["path"]).as_posix(), "sha256": output["sha256"], "size": output["size"]}:
            raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", f"W1 output binding mismatch: {key}", 0, key, "repair-w1-input")
    verify_ref(root, refs["design_input_closure_ref"])
    if refs["design_input_closure_ref"] != w1["source_ref"]:
        raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", "W1 source binding mismatch", 0, "design_input_closure_ref", "repair-w1-input")
    document_specs = [("design_input_closure_ref", "https://arcanum.dev/schemas/invoke/design-input-closure/v1", "closure_digest"), ("design_input_closure_receipt_ref", "https://arcanum.dev/schemas/invoke/design-input-closure-receipt/v1", "receipt_digest"), ("scope_manifest_ref", "https://arcanum.dev/schemas/invoke/design-scope-manifest/1-0-0", "input_digest"), ("denominator_receipt_ref", "https://arcanum.dev/schemas/invoke/design-denominator-receipt/1-0-0", "receipt_digest"), ("selection_result_ref", "https://arcanum.dev/schemas/invoke/design-selection-result/1-0-0", "result_digest")]
    try:
        documents = [(load_json(root / refs[key]["path"]), schema_id, digest_field) for key, schema_id, digest_field in document_specs]
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", f"W1 payload is unreadable: {error}", 0, None, "repair-w1-input") from error
    for document, schema_id, digest_field in documents:
        errors = schema_errors(document, store[schema_id], store)
        if errors or document.get(digest_field) != digest_without(document, digest_field):
            raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", f"live W1 payload invalid: {schema_id}: {'; '.join(errors[:5])}", 0, schema_id, "repair-w1-input")
    closure, closure_receipt, manifest, denominator, selection = [item[0] for item in documents]
    if w1["input_closure_receipt"] != closure_receipt or closure_receipt.get("activation_kind") != "normal" or closure_receipt.get("verdict") != "pass":
        raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", "W1 closure receipt is not exact normal PASS", 0, "design_input_closure_receipt_ref", "repair-w1-input")
    if denominator.get("verdict") != "pass" or denominator.get("manifest_id") != manifest.get("manifest_id") or denominator.get("manifest_input_digest") != manifest.get("input_digest"):
        raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", "W1 denominator is not PASS for the exact manifest", 0, "denominator_receipt_ref", "repair-w1-input")
    if selection.get("verdict") != "pass" or not selection.get("fixed_point") or selection.get("evidence_state") != "design-validator-pass" or selection.get("manifest_id") != manifest.get("manifest_id") or selection.get("manifest_input_digest") != manifest.get("input_digest") or selection.get("denominator_receipt_digest") != denominator.get("receipt_digest") or selection.get("pass_1_digest") != selection.get("pass_2_digest"):
        raise GovernedBlock("W1_OUTPUT_BINDING_MISMATCH", "W1 selection is not exact fixed-point PASS", 0, "selection_result_ref", "repair-w1-input")
    if source["target_id"] != closure["target"]["id"] or manifest["target_id"] != source["target_id"]:
        raise GovernedBlock("TARGET_BINDING_MISMATCH", "W1 and W2 target identities differ", 0, "target_id", "repair-w1-input")
    return selection


def validate_staging(staging: Path, store: dict[str, dict[str, Any]]) -> None:
    paths = {item.name: item for item in staging.iterdir()}
    if set(paths) != {ARTIFACT_NAME, COHERENCE_NAME, RECEIPT_NAME} or any(not item.is_file() or item.is_symlink() for item in paths.values()):
        raise GovernedBlock("OUTPUT_INVENTORY_MISMATCH", "staged W2 inventory is not exactly three regular files", 3, str(staging))
    try:
        artifact, coherence, receipt = (load_json(paths[name]) for name in [ARTIFACT_NAME, COHERENCE_NAME, RECEIPT_NAME])
    except (OSError, ValueError, json.JSONDecodeError) as error:
        raise GovernedBlock("LATE_VALIDATION_FAILED", f"staged JSON became unreadable: {error}", 3, str(staging)) from error
    for document, field, schema_id in [
        (artifact, "artifact_digest", "https://arcanum.dev/schemas/invoke/design-artifact/v1"),
        (coherence, "receipt_digest", "https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1"),
        (receipt, "receipt_digest", "https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1"),
    ]:
        errors = schema_errors(document, store[schema_id], store)
        if errors or document.get(field) != digest_without(document, field):
            raise GovernedBlock("LATE_VALIDATION_FAILED", f"late validation failed for {schema_id}: {'; '.join(errors[:5])}", 3, schema_id, "repair-installed-contract")
    observed = [output_ref(paths[ARTIFACT_NAME], "design-artifact"), output_ref(paths[COHERENCE_NAME], "coherence-receipt")]
    if receipt["outputs"] != observed:
        raise GovernedBlock("OUTPUT_INVENTORY_MISMATCH", "production receipt output hashes/sizes differ from staged bytes", 3, RECEIPT_NAME)


def validate_final_staging(
    staging: Path,
    source_path: Path,
    source_ref: dict[str, Any],
    artifact_label: str,
    root: Path,
    schema_dir: Path,
    store: dict[str, dict[str, Any]],
    w1_ref: dict[str, Any],
    bindings: dict[str, Any],
    producer_digest: str,
) -> None:
    """Re-run every acceptance-critical consumer on the final staged bytes."""
    validate_staging(staging, store)
    try:
        live_source_path = safe_path(root, source_ref["path"])
        live_source_ref = exact_ref(live_source_path, root)
        live_bindings = {
            "process": exact_ref(safe_path(root, PROCESS_PATH), root),
            "profile": exact_ref(safe_path(root, PROFILE_PATH), root),
            "policy": exact_ref(safe_path(root, POLICY_PATH), root),
        }
        live_producer_digest = exact_ref(safe_path(root, PRODUCER_PATH), root)["sha256"]
    except (OSError, ValueError) as error:
        raise GovernedBlock("LATE_VALIDATION_FAILED", f"validated source or installed W2 contracts became unavailable: {error}", 3, PRODUCER_PATH) from error
    if live_source_ref != source_ref:
        raise GovernedBlock("LATE_VALIDATION_FAILED", "Design source changed after the validated projection epoch", 3, source_ref["path"])
    if live_bindings != bindings or live_producer_digest != producer_digest:
        raise GovernedBlock("LATE_VALIDATION_FAILED", "installed W2 producer or static contract bytes changed during staging", 3, PRODUCER_PATH, "repair-installed-contract")

    artifact_path = staging / ARTIFACT_NAME
    artifact_data = artifact_path.read_bytes()
    final_artifact_ref = {
        "path": artifact_label,
        "sha256": hashlib.sha256(artifact_data).hexdigest(),
        "size": len(artifact_data),
    }
    try:
        expected_coherence = validate_design_coherence(source_path, artifact_path, final_artifact_ref, root, schema_dir)
    except ContractFailure as error:
        raise GovernedBlock("LATE_VALIDATION_FAILED", f"final staged bytes failed independent coherence: {error}", 3, error.selector, error.route) from error
    if expected_coherence["verdict"] != "pass":
        raise GovernedBlock("LATE_VALIDATION_FAILED", "final staged artifact is not independently coherent", 3, COHERENCE_NAME, coherence_receipt=expected_coherence)
    staged_coherence = load_json(staging / COHERENCE_NAME)
    if staged_coherence != expected_coherence:
        raise GovernedBlock("LATE_VALIDATION_FAILED", "staged coherence receipt differs from fresh independent validation", 3, COHERENCE_NAME)

    outputs = [
        output_ref(staging / ARTIFACT_NAME, "design-artifact"),
        output_ref(staging / COHERENCE_NAME, "coherence-receipt"),
    ]
    expected_receipt = make_receipt(source_ref, w1_ref, bindings, producer_digest, "pass", outputs)
    if load_json(staging / RECEIPT_NAME) != expected_receipt:
        raise GovernedBlock("OUTPUT_INVENTORY_MISMATCH", "staged production receipt differs from fresh producer closure", 3, RECEIPT_NAME)


def compile_candidate(source_path: Path, root: Path, output_dir: Path, attempt_receipt: Path, schema_dir: Path, late_validation_hook: Callable[[Path], None] | None = None) -> int:
    root = root.resolve()
    output_dir = safe_absent_destination(output_dir, root)
    attempt_receipt = safe_absent_destination(attempt_receipt)
    if attempt_receipt == output_dir or output_dir in attempt_receipt.parents:
        raise ValueError("--attempt-receipt must be distinct from and outside --output-dir")
    output_parent = output_dir.parent
    source_lexical = Path(os.path.abspath(source_path))
    try:
        source_label = source_lexical.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError("DESIGN-SOURCE.json must be inside --repo-root") from error
    source_path = safe_path(root, source_label)
    if not source_path.is_file():
        raise ValueError("DESIGN-SOURCE.json must be one regular non-symlink file")
    source_ref = exact_ref(source_path, root)
    producer_digest = exact_ref(root / PRODUCER_PATH, root)["sha256"]
    process_ref, profile_ref, policy_ref = exact_ref(root / PROCESS_PATH, root), exact_ref(root / PROFILE_PATH, root), exact_ref(root / POLICY_PATH, root)
    bindings = {"process": process_ref, "profile": profile_ref, "policy": policy_ref}
    source: dict[str, Any] | None = None
    w1_ref: dict[str, Any] | None = None
    staging: Path | None = None
    try:
        try:
            source = load_json(source_path)
        except (ValueError, json.JSONDecodeError) as error:
            raise ValueError("malformed source cannot bind a schema-valid attempt receipt") from error
        w1_ref = source.get("upstream_bindings", {}).get("design_input_production_receipt_ref")
        if not isinstance(w1_ref, dict) or not {"path", "sha256", "size"} <= w1_ref.keys():
            raise ValueError("source lacks a usable W1 production receipt binding; no schema-valid attempt receipt can be issued")
        w1_ref = {key: w1_ref[key] for key in ["path", "sha256", "size"]}
        store = schema_store(schema_dir)
        source_schema = store.get("https://arcanum.dev/schemas/invoke/design-source/v1")
        receipt_schema = store.get("https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1")
        artifact_schema = store.get("https://arcanum.dev/schemas/invoke/design-artifact/v1")
        coherence_schema = store.get("https://arcanum.dev/schemas/invoke/design-coherence-receipt/v1")
        if not all([source_schema, receipt_schema, artifact_schema, coherence_schema]):
            raise ValueError("required W2 schemas are unavailable")
        errors = schema_errors(source, source_schema, store)
        if errors:
            raise GovernedBlock("SOURCE_SCHEMA_INVALID", "; ".join(errors[:8]), 0, source_label)
        if source["source_digest"] != digest_without(source, "source_digest"):
            raise GovernedBlock("SOURCE_DIGEST_MISMATCH", "source self digest mismatch", 0, "source_digest")
        try:
            selection = preflight_w1(source, root, store)
        except ContractFailure as error:
            raise GovernedBlock(error.code, str(error), 0, error.selector, error.route) from error

        staging = Path(tempfile.mkdtemp(prefix=f".{output_dir.name}.stage-", dir=output_parent))
        try:
            artifact = project_design_artifact(source, source_ref, process_ref, profile_ref, policy_ref, selection)
        except (KeyError, TypeError, ValueError) as error:
            raise GovernedBlock("ARTIFACT_PROJECTION_FAILED", str(error), 1, source_label) from error
        artifact_path = staging / ARTIFACT_NAME
        write_json(artifact_path, artifact)
        artifact_label = (output_dir / ARTIFACT_NAME).relative_to(root).as_posix()
        artifact_data = artifact_path.read_bytes()
        artifact_ref = {"path": artifact_label, "sha256": hashlib.sha256(artifact_data).hexdigest(), "size": len(artifact_data)}
        try:
            coherence = validate_design_coherence(source_path, artifact_path, artifact_ref, root, schema_dir)
        except ContractFailure as error:
            code = error.code if error.code in {"SOURCE_SCHEMA_INVALID", "SOURCE_DIGEST_MISMATCH", "W1_RECEIPT_INVALID", "W1_RECEIPT_NOT_NORMAL", "W1_OUTPUT_BINDING_MISMATCH", "TARGET_BINDING_MISMATCH", "PROFILE_INVALID", "PROFILE_BINDING_MISMATCH", "APPLICATION_DENOMINATOR_MISMATCH", "APPLICATION_INVALID", "FACT_REGISTRY_INVALID", "VIEW_PROJECTION_INVALID", "SELECTION_CLOSURE_INVALID", "EVOLUTION_INVALID", "GOVERNANCE_OVERCLAIM"} else "COHERENCE_BLOCKED"
            raise GovernedBlock(code, str(error), 2, error.selector, error.route) from error
        coherence_path = staging / COHERENCE_NAME
        write_json(coherence_path, coherence)
        if coherence["verdict"] != "pass":
            raise GovernedBlock("COHERENCE_BLOCKED", "independent coherence validator returned BLOCK with complete embedded receipt", 2, "DESIGN-COHERENCE-RECEIPT.json", coherence_receipt=coherence)
        outputs = [output_ref(artifact_path, "design-artifact"), output_ref(coherence_path, "coherence-receipt")]
        receipt = make_receipt(source_ref, w1_ref, bindings, producer_digest, "pass", outputs)
        receipt_path = staging / RECEIPT_NAME
        write_json(receipt_path, receipt)
        validate_staging(staging, store)
        if late_validation_hook:
            try:
                late_validation_hook(staging)
            except Exception as error:
                raise GovernedBlock("LATE_VALIDATION_FAILED", f"late validation hook failed: {error}", 3, str(staging)) from error
        validate_final_staging(
            staging, source_path, source_ref, artifact_label, root, schema_dir,
            store, w1_ref, bindings, producer_digest,
        )
        os.replace(staging, output_dir)
        staging = None
        return 0
    except GovernedBlock as error:
        if output_dir.exists():
            raise RuntimeError("governed BLOCK must not leave a final output directory")
        assert w1_ref is not None
        item = blocker(error.code, str(error), error.selector, error.route)
        receipt = make_receipt(source_ref, w1_ref, bindings, producer_digest, "block", [], error.stage_index, [item], error.route, error.coherence_receipt)
        store = schema_store(schema_dir)
        receipt_schema = store.get("https://arcanum.dev/schemas/invoke/design-candidate-production-receipt/v1")
        if receipt_schema is None or schema_errors(receipt, receipt_schema, store):
            raise ValueError("cannot issue a schema-valid W2 attempt receipt")
        atomic_write_json(attempt_receipt, receipt)
        return 1
    finally:
        if staging is not None:
            shutil.rmtree(staging, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--attempt-receipt", required=True)
    parser.add_argument("--schema-dir")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    try:
        return compile_candidate(Path(args.source), root, Path(args.output_dir), Path(args.attempt_receipt), Path(args.schema_dir) if args.schema_dir else root / "arcanum/spells/invoke/schemas")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
