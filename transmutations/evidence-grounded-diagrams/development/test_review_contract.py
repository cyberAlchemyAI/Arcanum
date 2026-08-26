#!/usr/bin/env python3
"""Focused adversarial tests for review requests and review receipts."""

from __future__ import annotations

import copy
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
REQUEST_SCHEMA = ROOT / "schemas" / "diagram-request.schema.yml"
REVIEW_SCHEMA = ROOT / "schemas" / "diagram-review-receipt.schema.yml"
VALIDATOR = ROOT / "scripts" / "validate_review_receipt.py"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schema_errors(instance: dict[str, Any], schema_path: Path) -> list[str]:
    validator = Draft202012Validator(load_yaml(schema_path), format_checker=FormatChecker())
    return [error.message for error in validator.iter_errors(instance)]


def run_receipt(
    receipt_path: Path,
    *arguments: str,
    stdin: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(receipt_path), *arguments],
        input=stdin,
        capture_output=True,
        text=True,
        check=False,
    )


def expect(condition: bool, message: str, result: subprocess.CompletedProcess[str] | None = None) -> None:
    if condition:
        return
    detail = "" if result is None else f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    raise AssertionError(message + detail)


def major_fix_source_receipt(source: str) -> dict[str, Any]:
    return {
        "contract_version": "1.0.0",
        "review_id": "major-only-fix",
        "reviewed_at": "2026-08-25T00:00:00Z",
        "reviewer": "review-contract-test",
        "reader_question": "What does the exact source claim?",
        "target": {
            "kind": "source",
            "normalization": "UTF-8, LF line endings, no trailing newline",
            "observed_members": [{
                "role": "source",
                "path": None,
                "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
            }],
            "render_inspected": False,
        },
        "evidence_boundary": [{"source_id": "SRC-1", "locators": ["line-1"]}],
        "verdict": "FIX",
        "findings": [{
            "finding_id": "F-001",
            "severity": "major",
            "visual_claim": "A directly causes B.",
            "status": "unsupported",
            "evidence": "SRC-1 does not license a causal edge.",
            "smallest_correction": "Replace the causal edge with an untyped relation.",
        }],
    }


def create_bundle(root: Path) -> Path:
    bundle = root / "diagram-under-review" / "r0001"
    bundle.mkdir(parents=True)
    contents = {
        "diagram.request.yml": "request: exact\n",
        "diagram.mmd": "flowchart LR\n  A --> B\n",
        "diagram.model.yml": "model: exact\n",
        "textual-equivalent.md": "A points to B.\n",
        "validation.receipt.yml": "overall: DRAFT\n",
    }
    for name, value in contents.items():
        (bundle / name).write_text(value, encoding="utf-8")
    manifest = {
        "contract_version": "2.0.0",
        "diagram_id": "diagram-under-review",
        "revision": "r0001",
        "owner": "review-contract-test",
        "request_binding": {
            "request_id": "review-contract-test",
            "evidence_set_id": "SRC-1",
            "request_sha256": digest(bundle / "diagram.request.yml"),
            "evidence_snapshot_digest": None,
        },
        "reader_question": "What relation is asserted?",
        "created_at": "2026-08-25T00:00:00Z",
        "lifecycle_status": "draft",
        "retention_class": "generated",
        "promotion_status": "not-promoted",
        "promotion_evidence": None,
        "aggregate_status": "unknown",
        "supersedes": None,
        "tags": {
            "diagram_kind": "flowchart",
            "lifecycle": "draft",
            "epistemic": "unknown",
            "scope": "partial",
            "topics": ["review-contract"],
            "extensions": [],
        },
        "members": {
            "request": {
                "path": "diagram.request.yml",
                "media_type": "application/yaml",
                "sha256": digest(bundle / "diagram.request.yml"),
            },
            "source": {
                "path": "diagram.mmd",
                "media_type": "text/vnd.mermaid",
                "sha256": digest(bundle / "diagram.mmd"),
            },
            "render": None,
            "semantic_model": {
                "path": "diagram.model.yml",
                "media_type": "application/yaml",
                "sha256": digest(bundle / "diagram.model.yml"),
            },
            "textual_equivalent": {
                "path": "textual-equivalent.md",
                "media_type": "text/markdown",
                "sha256": digest(bundle / "textual-equivalent.md"),
            },
            "validation_receipt": {
                "path": "validation.receipt.yml",
                "media_type": "application/yaml",
            },
        },
        "renderer": None,
        "persistence": {
            "state": "saved",
            "output_root": str(root),
            "bundle_path": str(bundle),
            "index_path": str(root / "index.yml"),
        },
        "publication": {"destination": None, "official": False, "readiness": "draft"},
    }
    write_yaml(bundle / "diagram.meta.yml", manifest)
    return bundle


def bundle_receipt(bundle: Path) -> dict[str, Any]:
    role_paths = {
        "manifest": "diagram.meta.yml",
        "request": "diagram.request.yml",
        "source": "diagram.mmd",
        "semantic-model": "diagram.model.yml",
        "textual-equivalent": "textual-equivalent.md",
        "validation-receipt": "validation.receipt.yml",
    }
    receipt = major_fix_source_receipt("unused")
    receipt["review_id"] = "complete-bundle-review"
    receipt["target"] = {
        "kind": "bundle",
        "diagram_id": "diagram-under-review",
        "revision": "r0001",
        "bundle_path": str(bundle),
        "normalization": "raw bytes",
        "observed_members": [
            {"role": role, "path": relative, "sha256": digest(bundle / relative)}
            for role, relative in role_paths.items()
        ],
        "render_inspected": False,
    }
    return receipt


def main() -> int:
    source = "flowchart LR\n  A --> B"
    request = load_yaml(ROOT / "templates" / "diagram-request.yml")
    request["mode"] = "review"
    request["mutation_authorized"] = False
    request["target"] = {
        "kind": "source",
        "source_path": None,
        "inline_content": source,
        "normalization": "UTF-8, LF line endings, no trailing newline",
        "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
    }
    expect(not schema_errors(request, REQUEST_SCHEMA), "inline source review request must be valid")

    invented_source_identity = copy.deepcopy(request)
    invented_source_identity["target"]["diagram_id"] = "invented"
    expect(
        bool(schema_errors(invented_source_identity, REQUEST_SCHEMA)),
        "source review request accepted invented bundle identity",
    )

    revise_source = copy.deepcopy(request)
    revise_source["mode"] = "revise"
    revise_source["mutation_authorized"] = True
    expect(bool(schema_errors(revise_source, REQUEST_SCHEMA)), "revise accepted a source target")

    revise_bundle = copy.deepcopy(request)
    revise_bundle["mode"] = "revise"
    revise_bundle["target"] = {
        "kind": "bundle",
        "diagram_id": "diagram-under-review",
        "revision": "r0001",
        "bundle_path": "output/diagram-under-review/r0001",
        "manifest_digest": None,
    }
    revise_bundle.pop("mutation_authorized")
    expect(bool(schema_errors(revise_bundle, REQUEST_SCHEMA)), "revise omitted mutation authorization")
    revise_bundle["mutation_authorized"] = True
    expect(not schema_errors(revise_bundle, REQUEST_SCHEMA), "authorized bundle revise must be valid")

    with tempfile.TemporaryDirectory(prefix="egd-review-contract-") as temporary:
        temp = Path(temporary)
        major_receipt = major_fix_source_receipt(source)
        major_path = temp / "major-fix.yml"
        write_yaml(major_path, major_receipt)
        major_result = run_receipt(major_path, "--target-stdin", stdin=source)
        expect(major_result.returncode == 0, "major-only FIX receipt must be valid", major_result)

        invented_receipt_identity = copy.deepcopy(major_receipt)
        invented_receipt_identity["target"]["diagram_id"] = "invented"
        expect(
            bool(schema_errors(invented_receipt_identity, REVIEW_SCHEMA)),
            "source review receipt accepted invented bundle identity",
        )

        forged_first = copy.deepcopy(major_receipt)
        forged_first["first_blocker"] = "F-001"
        forged_first_path = temp / "forged-first-blocker.yml"
        write_yaml(forged_first_path, forged_first)
        forged_first_result = run_receipt(forged_first_path, "--target-stdin", stdin=source)
        expect(forged_first_result.returncode != 0, "major finding was accepted as first_blocker", forged_first_result)

        blocker_without_first = copy.deepcopy(major_receipt)
        blocker_without_first["findings"][0]["severity"] = "blocker"
        blocker_path = temp / "blocker-without-first.yml"
        write_yaml(blocker_path, blocker_without_first)
        blocker_result = run_receipt(blocker_path, "--target-stdin", stdin=source)
        expect(blocker_result.returncode != 0, "material blocker passed without first_blocker", blocker_result)

        wrong_digest = copy.deepcopy(major_receipt)
        wrong_digest["target"]["observed_members"][0]["sha256"] = "0" * 64
        wrong_digest_path = temp / "wrong-source-digest.yml"
        write_yaml(wrong_digest_path, wrong_digest)
        wrong_digest_result = run_receipt(wrong_digest_path, "--target-stdin", stdin=source)
        expect(wrong_digest_result.returncode != 0, "wrong normalized source digest passed", wrong_digest_result)

        bundle = create_bundle(temp / "bundles")
        complete = bundle_receipt(bundle)
        complete_path = temp / "complete-bundle.yml"
        write_yaml(complete_path, complete)
        complete_result = run_receipt(complete_path, "--bundle-root", str(bundle))
        expect(complete_result.returncode == 0, "complete exact bundle receipt must pass", complete_result)

        one_member = copy.deepcopy(complete)
        one_member["target"]["observed_members"] = one_member["target"]["observed_members"][:1]
        one_member_path = temp / "one-member.yml"
        write_yaml(one_member_path, one_member)
        one_member_result = run_receipt(one_member_path, "--bundle-root", str(bundle))
        expect(one_member_result.returncode != 0, "one-member bundle receipt passed", one_member_result)

        forged_identity = copy.deepcopy(complete)
        forged_identity["target"]["diagram_id"] = "forged-id"
        forged_identity_path = temp / "forged-identity.yml"
        write_yaml(forged_identity_path, forged_identity)
        forged_identity_result = run_receipt(forged_identity_path, "--bundle-root", str(bundle))
        expect(forged_identity_result.returncode != 0, "forged bundle identity passed", forged_identity_result)

        forged_path = copy.deepcopy(complete)
        forged_path["target"]["bundle_path"] = str(temp / "elsewhere")
        forged_path_file = temp / "forged-path.yml"
        write_yaml(forged_path_file, forged_path)
        forged_path_result = run_receipt(forged_path_file, "--bundle-root", str(bundle))
        expect(forged_path_result.returncode != 0, "forged bundle path passed", forged_path_result)

        duplicate_role = copy.deepcopy(complete)
        duplicate_role["target"]["observed_members"][-1]["role"] = "source"
        duplicate_path = temp / "duplicate-role.yml"
        write_yaml(duplicate_path, duplicate_role)
        duplicate_result = run_receipt(duplicate_path, "--bundle-root", str(bundle))
        expect(duplicate_result.returncode != 0, "duplicate bundle role passed", duplicate_result)

        forged_manifest_digest = load_yaml(bundle / "diagram.meta.yml")
        forged_manifest_digest["members"]["source"]["sha256"] = "0" * 64
        write_yaml(bundle / "diagram.meta.yml", forged_manifest_digest)
        digest_mismatch = bundle_receipt(bundle)
        digest_mismatch_path = temp / "manifest-member-digest-mismatch.yml"
        write_yaml(digest_mismatch_path, digest_mismatch)
        digest_mismatch_result = run_receipt(
            digest_mismatch_path, "--bundle-root", str(bundle)
        )
        expect(
            digest_mismatch_result.returncode != 0,
            "receipt passed when member bytes disagreed with manifest digest",
            digest_mismatch_result,
        )

    print("REVIEW_CONTRACT_TESTS=pass")
    print(
        "CASES=request-target-discrimination,revise-bundle-authorization,"
        "major-only-fix,conditional-first-blocker,source-digest-binding,"
        "bundle-identity-path-binding,exact-member-coverage,unique-roles,"
        "manifest-member-digest-binding"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print("REVIEW_CONTRACT_TESTS=block")
        print(f"BLOCK: {exc}")
        raise SystemExit(1)
