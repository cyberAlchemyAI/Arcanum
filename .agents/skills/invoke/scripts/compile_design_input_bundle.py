#!/usr/bin/env python3
"""Compile one approved Design input closure into an atomic W1 bundle."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator, RefResolver


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from design_scope_extractor import ExtractionFailure, extract_denominator  # noqa: E402
from design_selection_validator import validate_selection  # noqa: E402
from project_design_scope_manifest import (  # noqa: E402
    ProjectionFailure,
    project_scope_manifest,
)
from validate_design_input_closure import (  # noqa: E402
    exact_ref as repository_exact_ref,
    load_json,
    resolve_inside,
    validate_input_closure,
)


IDENTITY = "invoke.compile-design-input-bundle.v1"
OWNER = "invoke-design-input-producer"
PRODUCER_PATH = "arcanum/spells/invoke/scripts/compile_design_input_bundle.py"
OUTPUT_CONTRACTS = (
    ("input-closure-receipt", "DESIGN-INPUT-CLOSURE-RECEIPT.json"),
    ("scope-manifest", "DESIGN-SCOPE-MANIFEST.json"),
    ("denominator-receipt", "DESIGN-DENOMINATOR-RECEIPT.json"),
    ("selection-result", "DESIGN-SELECTION-RESULT.json"),
)
SUCCESS_RECEIPT = "DESIGN-INPUT-PRODUCTION-RECEIPT.json"
STAGE_IDS = (
    "input-closure-validation",
    "scope-projection",
    "denominator-extraction",
    "selection",
)


class GovernedBlock(ValueError):
    def __init__(
        self,
        code: str,
        message: str,
        stage_index: int,
        selector: str | None = None,
        closure_receipt: dict[str, Any] | None = None,
        blockers: list[dict[str, Any]] | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.stage_index = stage_index
        self.selector = selector
        self.closure_receipt = closure_receipt
        self.blockers = blockers


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest_without(document: dict[str, Any], field: str) -> str:
    return hashlib.sha256(
        canonical_bytes({key: value for key, value in document.items() if key != field})
    ).hexdigest()


def exact_ref(path: Path, label: str) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "path": label,
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
    }


def schema_errors(
    document: dict[str, Any],
    schema: dict[str, Any],
    store: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    resolver = RefResolver.from_schema(schema, store=store or {})
    return [
        f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema, resolver=resolver).iter_errors(document),
            key=lambda item: list(item.absolute_path),
        )
    ]


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def atomic_write_json(path: Path, document: dict[str, Any]) -> None:
    if path.exists():
        raise ValueError(f"attempt receipt already exists: {path}")
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(document, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        Path(temporary).unlink(missing_ok=True)
        raise


def source_binding(source_path: Path, repository_root: Path) -> dict[str, Any]:
    lexical = Path(os.path.abspath(source_path))
    root = repository_root.resolve()
    try:
        relative = lexical.relative_to(root).as_posix()
    except ValueError as error:
        raise ValueError("Design input closure must be inside --repo-root") from error
    resolved = resolve_inside(root, relative)
    if not resolved.is_file() or resolved.is_symlink():
        raise ValueError("Design input closure must be one regular file")
    return repository_exact_ref(resolved, root)


def make_blocker(
    code: str, message: str, selector: str | None = None
) -> dict[str, Any]:
    return {
        "blocker_id": f"w1-blocker:{code.lower()}",
        "code": code,
        "message": message,
        "selector": selector,
        "owner": "design-input-owner",
        "repair_route": "Repair the named W1 binding and restart from the Design input closure.",
    }


def stage_results(
    failed_index: int | None, blocker_ids: list[str]
) -> list[dict[str, Any]]:
    results = []
    for index, stage_id in enumerate(STAGE_IDS):
        if failed_index is None or index < failed_index:
            status = "pass"
            causal: list[str] = []
        elif index == failed_index:
            status = "block"
            causal = blocker_ids
        else:
            status = "not_evaluable"
            causal = blocker_ids
        results.append(
            {"stage_id": stage_id, "status": status, "causal_blocker_ids": causal}
        )
    return results


def evidence_ceiling(passed_stages: int) -> dict[str, bool]:
    return {
        "boundary_relative_input_closure": passed_stages >= 1,
        "manifest_projection": passed_stages >= 2,
        "denominator_compatibility": passed_stages >= 3,
        "selection_fixed_point": passed_stages >= 4,
        "artifact_authored": False,
        "plan_evidence": False,
        "acceptance": False,
        "execution": False,
        "publication": False,
        "deployment": False,
        "external_effect": False,
    }


def build_production_receipt(
    source_ref: dict[str, Any],
    closure_receipt: dict[str, Any],
    producer_digest: str,
    result: str,
    outputs: list[dict[str, Any]],
    failed_index: int | None = None,
    blockers: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    receipt_blockers = copy.deepcopy(blockers or [])
    blocker_ids = [item["blocker_id"] for item in receipt_blockers]
    passed_stages = 4 if failed_index is None else failed_index
    activation_kind = closure_receipt.get("activation_kind", "invalid")
    if activation_kind not in {"normal", "discovery"}:
        activation_kind = "invalid"
    receipt: dict[str, Any] = {
        "$schema": "https://arcanum.dev/schemas/invoke/design-input-production-receipt/v1",
        "schema_version": "invoke.design-input-production-receipt.v1",
        "receipt_id": f"design-w1:{source_ref['sha256'][:24]}",
        "producer": {
            "identity": IDENTITY,
            "owner": OWNER,
            "path": PRODUCER_PATH,
            "sha256": producer_digest,
        },
        "source_ref": source_ref,
        "activation_kind": activation_kind,
        "input_closure_receipt": copy.deepcopy(closure_receipt),
        "stage_results": stage_results(failed_index, blocker_ids),
        "outputs": outputs,
        "result": result,
        "next_route": (
            "design-authoring"
            if result == "pass" and activation_kind == "normal"
            else "input-review"
            if result == "pass" and activation_kind == "discovery"
            else "repair-input"
        ),
        "blockers": receipt_blockers,
        "evidence_ceiling": evidence_ceiling(passed_stages),
        "authority_effect": "none",
        "receipt_digest": "0" * 64,
    }
    receipt["receipt_digest"] = digest_without(receipt, "receipt_digest")
    return receipt


def validate_production_receipt(
    receipt: dict[str, Any], schemas: dict[str, dict[str, Any]]
) -> None:
    closure_schema = schemas["closure_receipt"]
    errors = schema_errors(
        receipt,
        schemas["production_receipt"],
        {closure_schema["$id"]: closure_schema},
    )
    if errors:
        raise ValueError("production receipt schema invalid: " + "; ".join(errors))
    if digest_without(receipt, "receipt_digest") != receipt["receipt_digest"]:
        raise ValueError("production receipt digest is stale")


def assert_predicates(
    closure: dict[str, Any], selection_result: dict[str, Any]
) -> None:
    authored = {
        item["concern_id"]: item
        for item in closure["selection_inputs"]["authored_concerns"]
    }
    final = {item["primary_class"]: item for item in selection_result["concerns"]}
    for predicate in closure["selection_inputs"]["predicate_inputs"]:
        concern = authored[predicate["concern_id"]]
        selected = final.get(concern["primary_class"])
        if selected is None:
            raise GovernedBlock(
                "PREDICATE_ASSERTION_MISMATCH",
                f"selection omitted predicate concern: {predicate['concern_id']}",
                3,
                predicate["concern_id"],
            )
        final_value = selected["predicate_evidence"]["required_predicate"]
        if (
            predicate["expected"] != concern["required_predicate"]
            or predicate["expected"] != final_value
        ):
            raise GovernedBlock(
                "PREDICATE_ASSERTION_MISMATCH",
                f"predicate assertion changed for concern: {predicate['concern_id']}",
                3,
                predicate["concern_id"],
            )


def compile_bundle(
    source_path: Path,
    repository_root: Path,
    output_dir: Path,
    attempt_receipt: Path,
    schema_dir: Path,
    late_validator: Callable[[Path], None] | None = None,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    output_dir = Path(os.path.abspath(output_dir))
    attempt_receipt = Path(os.path.abspath(attempt_receipt))
    schema_dir = schema_dir.resolve()
    if not repository_root.is_dir():
        raise ValueError("--repo-root must be an existing directory")
    if not schema_dir.is_dir():
        raise ValueError("--schema-dir must be an existing directory")
    if (
        output_dir.exists()
        or output_dir.is_symlink()
        or attempt_receipt.exists()
        or attempt_receipt.is_symlink()
    ):
        raise ValueError("output directory and attempt receipt must both be absent")
    if not output_dir.parent.is_dir() or not attempt_receipt.parent.is_dir():
        raise ValueError("output and attempt receipt parents must already exist")
    if output_dir == attempt_receipt or output_dir in attempt_receipt.parents:
        raise ValueError("attempt receipt must be outside the output directory")

    source_ref = source_binding(source_path, repository_root)
    source_path = resolve_inside(repository_root, source_ref["path"])
    producer_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    required_schema_names = {
        "manifest": "design-scope-manifest.schema.json",
        "denominator": "design-denominator-receipt.schema.json",
        "selection": "design-selection-result.schema.json",
        "closure_receipt": "design-input-closure-receipt-v1.schema.json",
        "production_receipt": "design-input-production-receipt-v1.schema.json",
    }
    schemas = {
        key: load_json(schema_dir / filename)
        for key, filename in required_schema_names.items()
    }
    for schema in schemas.values():
        Draft202012Validator.check_schema(schema)

    closure = load_json(source_path)
    closure_receipt: dict[str, Any] | None = None
    stage: Path | None = None
    try:
        closure_receipt = validate_input_closure(
            closure, source_path, repository_root, schema_dir
        )
        if closure_receipt["verdict"] != "pass":
            raise GovernedBlock(
                closure_receipt["blockers"][0]["code"],
                "Design input closure validation blocked",
                0,
                closure_receipt["blockers"][0]["selector"],
                closure_receipt=closure_receipt,
                blockers=closure_receipt["blockers"],
            )

        stage = Path(
            tempfile.mkdtemp(prefix=f".{output_dir.name}.", dir=output_dir.parent)
        )
        write_json(stage / OUTPUT_CONTRACTS[0][1], closure_receipt)

        try:
            manifest = project_scope_manifest(
                closure,
                closure_receipt,
                repository_root,
                schemas["manifest"],
            )
        except (OSError, ProjectionFailure, ValueError) as error:
            raise GovernedBlock(
                "MANIFEST_PROJECTION_MISMATCH", str(error), 1, "scope_signals"
            ) from error
        write_json(stage / OUTPUT_CONTRACTS[1][1], manifest)

        authored_concerns = copy.deepcopy(
            closure["selection_inputs"]["authored_concerns"]
        )
        authored_ids = [item["concern_id"] for item in authored_concerns]
        try:
            denominator = extract_denominator(
                manifest,
                repository_root,
                schemas["manifest"],
                authored_ids,
            )
        except (ExtractionFailure, OSError, ValueError) as error:
            raise GovernedBlock(
                "DENOMINATOR_BLOCKED", str(error), 2, "DESIGN-SCOPE-MANIFEST.json"
            ) from error
        denominator_errors = schema_errors(denominator, schemas["denominator"])
        if denominator_errors or denominator.get("verdict") != "pass":
            raise GovernedBlock(
                "DENOMINATOR_BLOCKED",
                "; ".join(denominator_errors) or "denominator receipt did not pass",
                2,
                "DESIGN-DENOMINATOR-RECEIPT.json",
            )
        write_json(stage / OUTPUT_CONTRACTS[2][1], denominator)

        selection = validate_selection(
            manifest,
            denominator,
            authored_concerns,
            copy.deepcopy(
                closure["selection_inputs"]["planned_witness_requirements"]
            ),
            {
                "manifest": schemas["manifest"],
                "receipt": schemas["denominator"],
                "result": schemas["selection"],
            },
        )
        selection_errors = schema_errors(selection, schemas["selection"])
        if selection_errors or selection.get("verdict") != "pass":
            raise GovernedBlock(
                "SELECTION_BLOCKED",
                "; ".join(selection_errors)
                or "; ".join(item["message"] for item in selection["diagnostics"])
                or "selection did not pass",
                3,
                "DESIGN-SELECTION-RESULT.json",
            )
        assert_predicates(closure, selection)
        write_json(stage / OUTPUT_CONTRACTS[3][1], selection)

        outputs = [
            {"kind": kind, **exact_ref(stage / filename, filename)}
            for kind, filename in OUTPUT_CONTRACTS
        ]
        success_receipt = build_production_receipt(
            source_ref,
            closure_receipt,
            producer_digest,
            "pass",
            outputs,
        )
        validate_production_receipt(success_receipt, schemas)
        write_json(stage / SUCCESS_RECEIPT, success_receipt)

        expected_files = {filename for _, filename in OUTPUT_CONTRACTS} | {
            SUCCESS_RECEIPT
        }
        actual_files = {
            path.name for path in stage.iterdir() if path.is_file() and not path.is_symlink()
        }
        if actual_files != expected_files or any(path.is_symlink() for path in stage.iterdir()):
            raise GovernedBlock(
                "OUTPUT_INVENTORY_MISMATCH",
                "staged W1 output inventory differs from the fixed five-file contract",
                3,
                stage.as_posix(),
            )
        for output in success_receipt["outputs"]:
            current = {
                "kind": output["kind"],
                **exact_ref(stage / output["path"], output["path"]),
            }
            if current != output:
                raise GovernedBlock(
                    "OUTPUT_INVENTORY_MISMATCH",
                    f"staged output drifted after receipt closure: {output['path']}",
                    3,
                    output["path"],
                )
        validate_production_receipt(load_json(stage / SUCCESS_RECEIPT), schemas)
        if late_validator is not None:
            try:
                late_validator(stage)
            except Exception as error:
                raise GovernedBlock(
                    "LATE_VALIDATION_FAILED", str(error), 3, stage.as_posix()
                ) from error
        final_files = {
            path.name
            for path in stage.iterdir()
            if path.is_file() and not path.is_symlink()
        }
        if final_files != expected_files or any(
            path.is_symlink() or not path.is_file() for path in stage.iterdir()
        ):
            raise GovernedBlock(
                "OUTPUT_INVENTORY_MISMATCH",
                "late validation changed the fixed five-file W1 output inventory",
                3,
                stage.as_posix(),
            )
        for output in success_receipt["outputs"]:
            current = {
                "kind": output["kind"],
                **exact_ref(stage / output["path"], output["path"]),
            }
            if current != output:
                raise GovernedBlock(
                    "OUTPUT_INVENTORY_MISMATCH",
                    f"late validation changed a receipted output: {output['path']}",
                    3,
                    output["path"],
                )
        os.replace(stage, output_dir)
        stage = None
        return success_receipt
    except GovernedBlock as error:
        if stage is not None:
            shutil.rmtree(stage, ignore_errors=True)
            stage = None
        bound_closure_receipt = error.closure_receipt or closure_receipt
        if bound_closure_receipt is None:
            raise ValueError("no schema-valid closure receipt is available") from error
        blockers = error.blockers or [
            make_blocker(error.code, str(error), error.selector)
        ]
        block_receipt = build_production_receipt(
            source_ref,
            bound_closure_receipt,
            producer_digest,
            "block",
            [],
            failed_index=error.stage_index,
            blockers=blockers,
        )
        validate_production_receipt(block_receipt, schemas)
        atomic_write_json(attempt_receipt, block_receipt)
        return block_receipt
    finally:
        if stage is not None:
            shutil.rmtree(stage, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("closure", type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--attempt-receipt", required=True, type=Path)
    parser.add_argument("--schema-dir", type=Path)
    args = parser.parse_args()
    schema_dir = args.schema_dir or SCRIPT_DIR.parent / "schemas"
    try:
        receipt = compile_bundle(
            args.closure,
            args.repo_root,
            args.output_dir,
            args.attempt_receipt,
            schema_dir,
        )
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    print(json.dumps(receipt, sort_keys=True))
    return 0 if receipt["result"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
