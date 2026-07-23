#!/usr/bin/env python3
"""Exercise Task Session mutation admission against the live Invoke contract."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def exact_ref(root: Path, relative_path: str) -> dict[str, Any]:
    content = (root / relative_path).read_bytes()
    return {
        "path": relative_path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "sizeBytes": len(content),
    }


def producer_ref(root: Path, relative_path: str) -> dict[str, Any]:
    reference = exact_ref(root, relative_path)
    return {
        "path": reference["path"],
        "sha256": reference["sha256"],
        "size_bytes": reference["sizeBytes"],
    }


def build_valid_case(
    case_root: Path,
    producer: Any,
    package_schema: dict[str, Any],
    producer_receipt_schema: dict[str, Any],
    producer_receipt_schema_path: Path,
) -> dict[str, Any]:
    (case_root / "controls").mkdir(parents=True)
    (case_root / "dependencies").mkdir(parents=True)
    (case_root / "staged").mkdir(parents=True)
    (case_root / "schemas").mkdir(parents=True)

    (case_root / "controls/task.md").write_text(
        "# TASK-WFE-005\n", encoding="utf-8"
    )
    (case_root / "controls/work-pack.md").write_text(
        "# Work Pack\n\nSelected: SWU-WFE-005\n", encoding="utf-8"
    )
    write_json(
        case_root / "controls/context-pack.json",
        {
            "task_id": "TASK-WFE-005",
            "swu_id": "SWU-WFE-005",
            "strict_coverage": True,
        },
    )
    (case_root / "dependencies/invoke-receipt.json").write_text(
        '{"result":"pass"}\n', encoding="utf-8"
    )
    (case_root / "staged/generated.txt").write_text(
        "generated runtime\n", encoding="utf-8"
    )
    shutil.copyfile(
        producer_receipt_schema_path,
        case_root / "schemas/material-package-receipt.schema.json",
    )

    control_specs = [
        ("controls/task.md", "task-contract"),
        ("controls/work-pack.md", "work-pack"),
        ("controls/context-pack.json", "context-pack"),
    ]
    controls = [
        {
            **exact_ref(case_root, path),
            "role": role,
            "authorityClass": "public",
        }
        for path, role in control_specs
    ]
    dependencies = [
        {
            "dependencyId": "invoke-material-receipt",
            "artifactRef": exact_ref(
                case_root, "dependencies/invoke-receipt.json"
            ),
        }
    ]
    package = {
        "schema_version": "1.0.0",
        "package_id": "task-session:TASK-WFE-005:SWU-WFE-005",
        "mutation_mode": "apply-approved",
        "mutation_state": "materialized",
        "lifecycle_owner": "sigil-development",
        "authority_class": "public",
        "publication_class": "public",
        "source_artifacts": [
            {
                "path": item["path"],
                "sha256": item["sha256"],
                "size_bytes": item["sizeBytes"],
                "authority_class": item["authorityClass"],
            }
            for item in controls
        ],
        "changes": [
            {
                "target_path": "runtime/generated.txt",
                "operation": "update",
                "output_ref": producer_ref(
                    case_root, "staged/generated.txt"
                ),
            }
        ],
        "target_inventory": [
            {
                "target_path": "runtime/generated.txt",
                "lifecycle_owner": "sigil-development",
                "authority_class": "public",
                "publication_class": "public",
                "dependency_ids": ["invoke-material-receipt"],
            }
        ],
        "dependencies": [
            {
                "dependency_id": item["dependencyId"],
                "artifact_ref": {
                    "path": item["artifactRef"]["path"],
                    "sha256": item["artifactRef"]["sha256"],
                    "size_bytes": item["artifactRef"]["sizeBytes"],
                },
            }
            for item in dependencies
        ],
        "mirror_groups": [],
        "approval": {
            "class": "explicit-apply",
            "owner": "sigil-development",
            "scope_paths": ["runtime/generated.txt"],
            "authority_classes": ["public"],
            "publication_classes": ["public"],
        },
        "validation_commands": ["bash verify-generated-runtime.sh"],
    }
    receipt = producer.validate_material_package(
        package,
        case_root,
        package_schema,
        producer_receipt_schema,
    )
    if receipt["patchVerdict"] != "pass":
        raise RuntimeError(f"producer fixture failed: {receipt['reasons']}")
    write_json(case_root / "material-package.json", package)
    write_json(case_root / "material-receipt.json", receipt)

    return {
        "schemaVersion": "1.0.0",
        "executionMode": "routed-mutation",
        "taskId": "TASK-WFE-005",
        "swuId": "SWU-WFE-005",
        "controlArtifacts": controls,
        "dependencyFrontier": dependencies,
        "materialPackage": exact_ref(case_root, "material-package.json"),
        "materialReceipt": exact_ref(case_root, "material-receipt.json"),
        "producerReceiptSchema": exact_ref(
            case_root, "schemas/material-package-receipt.schema.json"
        ),
        "allowedWrites": ["runtime/generated.txt"],
        "validationCommands": ["bash verify-generated-runtime.sh"],
        "lifecycleOwner": "sigil-development",
        "authorityClass": "public",
        "publicationClass": "public",
    }


def apply_mutation(case_root: Path, request: dict[str, Any], mutation: str) -> None:
    if mutation == "none":
        return
    if mutation == "remove-receipt":
        (case_root / "material-receipt.json").unlink()
        return
    if mutation == "invalidate-receipt-schema":
        receipt = load_json(case_root / "material-receipt.json")
        del receipt["authorityClass"]
        write_json(case_root / "material-receipt.json", receipt)
        request["materialReceipt"] = exact_ref(
            case_root, "material-receipt.json"
        )
        return
    if mutation == "change-control":
        with (case_root / "controls/task.md").open("a", encoding="utf-8") as handle:
            handle.write("changed\n")
        return
    if mutation == "change-task-id":
        request["taskId"] = "TASK-WFE-OTHER"
        return
    if mutation == "change-dependency":
        with (
            case_root / "dependencies/invoke-receipt.json"
        ).open("a", encoding="utf-8") as handle:
            handle.write("changed\n")
        return
    if mutation == "expand-request-write-scope":
        request["allowedWrites"].append("runtime/extra.txt")
        return
    if mutation == "remove-authority-class":
        del request["authorityClass"]
        return
    if mutation == "standalone":
        request.clear()
        request.update(
            {
                "schemaVersion": "1.0.0",
                "executionMode": "standalone-nonmutating",
            }
        )
        return
    raise ValueError(f"unknown fixture mutation: {mutation}")


def main() -> int:
    canonical_dir = Path(__file__).resolve().parents[1]
    arcanum_root = canonical_dir.parents[1]
    invoke_dir = arcanum_root / "spells/invoke"
    consumer = load_module(
        "task_session_mutation_admission",
        canonical_dir / "scripts/verify-mutation-readiness.py",
    )
    producer = load_module(
        "invoke_material_package_validator",
        invoke_dir / "scripts/material_package_validator.py",
    )

    request_schema = load_json(
        canonical_dir / "schemas/mutation-admission-request.schema.json"
    )
    admission_receipt_schema = load_json(
        canonical_dir / "schemas/mutation-admission-receipt.schema.json"
    )
    package_schema = load_json(
        invoke_dir / "schemas/material-package.schema.json"
    )
    producer_receipt_schema_path = (
        invoke_dir / "schemas/material-package-receipt.schema.json"
    )
    producer_receipt_schema = load_json(producer_receipt_schema_path)
    cases = load_json(
        canonical_dir / "development/fixtures/mutation-admission-cases.json"
    )

    passed = 0
    with tempfile.TemporaryDirectory(
        prefix="task-session-mutation-admission-"
    ) as temporary:
        fixture_root = Path(temporary)
        for fixture in cases:
            case_root = fixture_root / fixture["id"]
            case_root.mkdir()
            request = build_valid_case(
                case_root,
                producer,
                package_schema,
                producer_receipt_schema,
                producer_receipt_schema_path,
            )
            apply_mutation(case_root, request, fixture["mutation"])
            result = consumer.resolve_mutation_admission(
                copy.deepcopy(request), case_root, request_schema
            )
            errors = list(
                Draft202012Validator(admission_receipt_schema).iter_errors(
                    result
                )
            )
            reason_text = " | ".join(result["reasons"])
            expected_reason = fixture["expectedReason"]
            ok = (
                not errors
                and result["admissionVerdict"]
                == fixture["expectedVerdict"]
                and (
                    expected_reason is None
                    or expected_reason in reason_text
                )
            )
            if fixture["expectedVerdict"] == "admit":
                ok = (
                    ok
                    and result["mutationReady"] is True
                    and result["liveValidationRequired"] is True
                    and result["validationCommands"]
                    == ["bash verify-generated-runtime.sh"]
                )
            if fixture["expectedVerdict"] == "not-applicable":
                ok = (
                    ok
                    and result["mutationReady"] is False
                    and result["liveValidationRequired"] is False
                )
            if not ok:
                print(
                    f"FAIL {fixture['id']}: "
                    f"{json.dumps(result, sort_keys=True)}"
                )
                return 1
            passed += 1
            print(
                f"PASS {fixture['id']}: "
                f"{result['admissionVerdict']}"
            )

    producer_schema_digest = hashlib.sha256(
        producer_receipt_schema_path.read_bytes()
    ).hexdigest()
    print(
        "PASS producer-owned receipt schema consumed by exact digest: "
        f"{producer_schema_digest}"
    )
    print(f"PASS mutation admission fixtures: {passed}/{len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
