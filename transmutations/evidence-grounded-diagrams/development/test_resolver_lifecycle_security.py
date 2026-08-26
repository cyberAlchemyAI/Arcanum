#!/usr/bin/env python3
"""Negative probes for resolver lifecycle and role-aware member closure."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path

import yaml

from test_bundle_contract import persist, run, write_staging, write_yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from list_diagram_bundles import apply_effective_lifecycle, resolve_current  # noqa: E402


VALIDATE = SCRIPTS / "validate_diagram_bundle.py"
LIST = SCRIPTS / "list_diagram_bundles.py"


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected YAML object: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expect(condition: bool, message: str, result=None) -> None:
    if condition:
        return
    details = "" if result is None else f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    raise AssertionError(message + details)


def persisted_bundle(temp: Path, diagram_id: str) -> tuple[Path, Path]:
    stage = write_staging(temp / f"stage-{diagram_id}", diagram_id=diagram_id)
    output = temp / f"output-{diagram_id}"
    result = persist(stage, output)
    expect(result.returncode == 0, f"baseline persistence failed for {diagram_id}", result)
    return output, output / diagram_id / "r0001"


def reseal_manifest(bundle: Path, output: Path) -> None:
    """Update external byte bindings after an adversarial manifest mutation."""
    manifest_digest = digest(bundle / "diagram.meta.yml")
    receipt_path = bundle / "validation.receipt.yml"
    receipt = load_yaml(receipt_path)
    receipt["observed_manifest_sha256"] = manifest_digest
    write_yaml(receipt_path, receipt)
    marker_path = (
        output
        / ".evidence-grounded-diagrams"
        / "commits"
        / bundle.parent.name
        / f"{bundle.name}.yml"
    )
    marker = load_yaml(marker_path)
    marker["manifest_sha256"] = manifest_digest
    write_yaml(marker_path, marker)


def lifecycle_resolution_probes() -> None:
    records = [
        {
            "diagram_id": "governed",
            "revision": "r0001",
            "lifecycle": "validated",
            "declared_lifecycle": "validated",
            "supersedes_revision": None,
        },
        {
            "diagram_id": "governed",
            "revision": "r0002",
            "lifecycle": "draft",
            "declared_lifecycle": "draft",
            "supersedes_revision": "r0001",
        },
    ]
    apply_effective_lifecycle(records)
    expect(
        records[0]["lifecycle"] == "validated",
        "a newer DRAFT incorrectly derived superseded for a validated ancestor",
    )
    current = resolve_current(records)
    expect(
        len(current) == 1 and current[0]["revision"] == "r0001",
        "a newer DRAFT displaced the validated current revision",
    )

    draft_only = [
        {
            "diagram_id": "draft-only",
            "revision": revision,
            "lifecycle": "draft",
            "declared_lifecycle": "draft",
            "supersedes_revision": prior,
        }
        for revision, prior in (("r0001", None), ("r0002", "r0001"))
    ]
    apply_effective_lifecycle(draft_only)
    expect(
        resolve_current(draft_only)[0]["revision"] == "r0002",
        "draft-only history did not expose its latest working revision",
    )


def main() -> int:
    lifecycle_resolution_probes()
    with tempfile.TemporaryDirectory(prefix="egd-resolver-security-") as temporary:
        temp = Path(temporary)

        output, bundle = persisted_bundle(temp, "validated-draft")
        manifest_path = bundle / "diagram.meta.yml"
        manifest = load_yaml(manifest_path)
        manifest["lifecycle_status"] = "validated"
        manifest["tags"]["lifecycle"] = "validated"
        write_yaml(manifest_path, manifest)
        reseal_manifest(bundle, output)
        validated_draft = run(sys.executable, str(VALIDATE), str(bundle))
        expect(
            validated_draft.returncode != 0
            and "validated bundle requires overall receipt PASS" in validated_draft.stdout,
            "validated lifecycle exited successfully with an overall DRAFT receipt",
            validated_draft,
        )
        hidden_validated_draft = run(sys.executable, str(LIST), str(output), "--json")
        expect(
            hidden_validated_draft.returncode == 0
            and json.loads(hidden_validated_draft.stdout) == [],
            "discovery exposed a validated declaration backed only by DRAFT validation",
            hidden_validated_draft,
        )

        alias_output, alias_bundle = persisted_bundle(temp, "member-alias")
        alias_manifest_path = alias_bundle / "diagram.meta.yml"
        alias_manifest = load_yaml(alias_manifest_path)
        alias_manifest["members"]["textual_equivalent"] = copy.deepcopy(
            alias_manifest["members"]["source"]
        )
        write_yaml(alias_manifest_path, alias_manifest)
        aliased = run(sys.executable, str(VALIDATE), str(alias_bundle), "--write-receipt")
        expect(
            aliased.returncode != 0 and "member path alias" in aliased.stdout,
            "two semantic roles were allowed to alias one normalized member path",
            aliased,
        )

        missing_output, missing_bundle = persisted_bundle(temp, "memberless-forgery")
        missing_manifest_path = missing_bundle / "diagram.meta.yml"
        missing_manifest = load_yaml(missing_manifest_path)
        missing_manifest["members"].pop("source")
        write_yaml(missing_manifest_path, missing_manifest)
        missing_receipt_path = missing_bundle / "validation.receipt.yml"
        missing_receipt = load_yaml(missing_receipt_path)
        missing_receipt["observed_members"] = [
            item
            for item in missing_receipt["observed_members"]
            if item["path"] != "diagram.mmd"
        ]
        write_yaml(missing_receipt_path, missing_receipt)
        reseal_manifest(missing_bundle, missing_output)
        missing_list = run(sys.executable, str(LIST), str(missing_output), "--json")
        expect(
            missing_list.returncode == 0 and json.loads(missing_list.stdout) == [],
            "schema-invalid memberless bundle entered discovery",
            missing_list,
        )

        promotion_output, promotion_bundle = persisted_bundle(temp, "promotion-forgery")
        promotion_manifest_path = promotion_bundle / "diagram.meta.yml"
        promotion_manifest = load_yaml(promotion_manifest_path)
        promotion_manifest["promotion_status"] = "promoted"
        promotion_manifest["promotion_evidence"] = {
            "decision_id": "unverified-decision",
            "decided_at": "2026-08-25T00:00:00Z",
            "subject": {
                "diagram_id": "promotion-forgery",
                "revision": "r0001",
                "pre_promotion_manifest_sha256": "b" * 64,
            },
            "authority": {
                "identity": "self-asserted authority",
                "basis": "Unverified provenance used by a negative test.",
            },
            "attestation": {
                "kind": "external-attestation",
                "path": "../missing-promotion-attestation.yml",
                "media_type": "application/yaml",
                "sha256": "a" * 64,
            },
        }
        write_yaml(promotion_manifest_path, promotion_manifest)
        reseal_manifest(promotion_bundle, promotion_output)
        promotion_validation = run(
            sys.executable, str(VALIDATE), str(promotion_bundle)
        )
        expect(
            promotion_validation.returncode != 0
            and "promotion attestation does not exist" in promotion_validation.stdout,
            "promoted metadata passed without its declared external attestation",
            promotion_validation,
        )
        promotion_list = run(sys.executable, str(LIST), str(promotion_output), "--json")
        expect(
            promotion_list.returncode == 0 and json.loads(promotion_list.stdout) == [],
            "discovery admitted promoted metadata without verifiable provenance",
            promotion_list,
        )

        forged_output, forged_bundle = persisted_bundle(temp, "published-forgery")
        render_path = forged_bundle / "diagram.svg"
        render_path.write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>\n", encoding="utf-8")
        forged_manifest_path = forged_bundle / "diagram.meta.yml"
        forged_manifest = load_yaml(forged_manifest_path)
        forged_manifest["lifecycle_status"] = "published"
        forged_manifest["tags"]["lifecycle"] = "published"
        forged_manifest["publication"] = {
            "destination": "forged-official-destination",
            "official": True,
            "readiness": "ready",
        }
        forged_manifest["members"]["render"] = {
            "path": "diagram.svg",
            "media_type": "image/svg+xml",
            "sha256": digest(render_path),
        }
        write_yaml(forged_manifest_path, forged_manifest)
        forged_receipt_path = forged_bundle / "validation.receipt.yml"
        forged_receipt = load_yaml(forged_receipt_path)
        forged_receipt["observed_members"].append(
            {"path": "diagram.svg", "sha256": digest(render_path)}
        )
        for check in forged_receipt["checks"].values():
            check.update(
                {
                    "status": "PASS",
                    "assessor": "self-forged",
                    "evidence": "Untrusted receipt edit.",
                    "limitations": [],
                }
            )
        forged_receipt["overall"] = "PASS"
        forged_receipt["blockers"] = []
        write_yaml(forged_receipt_path, forged_receipt)
        reseal_manifest(forged_bundle, forged_output)
        forged_list = run(sys.executable, str(LIST), str(forged_output), "--json")
        expect(
            forged_list.returncode == 0 and json.loads(forged_list.stdout) == [],
            "forged published bundle entered discovery",
            forged_list,
        )

    print("RESOLVER_LIFECYCLE_SECURITY_TESTS=pass")
    print(
        "CASES=draft-does-not-supersede,validated-plus-draft,draft-fallback,"
        "validated-requires-pass,member-alias,memberless-discovery,"
        "promotion-evidence-verification,forged-published-discovery"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print("RESOLVER_LIFECYCLE_SECURITY_TESTS=block")
        print(f"BLOCK: {exc}")
        raise SystemExit(1)
