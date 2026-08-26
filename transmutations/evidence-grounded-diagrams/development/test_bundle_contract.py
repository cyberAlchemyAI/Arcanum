#!/usr/bin/env python3
"""Deterministic positive and negative probes for the staged bundle contract."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PERSIST = ROOT / "scripts" / "persist_diagram_bundle.py"
VALIDATE = ROOT / "scripts" / "validate_diagram_bundle.py"
PACKAGE = ROOT / "scripts" / "validate_skill_package.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=False)


def write_yaml(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def initial_receipt(diagram_id: str = "reviewer-action") -> dict:
    def pending(name: str) -> dict:
        return {
            "status": "NOT_RUN",
            "assessor": "pending",
            "evidence": "",
            "limitations": [f"{name} has not run."],
        }

    return {
        "contract_version": "2.0.0",
        "diagram_id": diagram_id,
        "revision": "r0001",
        "validated_at": "2026-08-25T00:00:00Z",
        "validator": {"name": "pending", "version": "0.0.0"},
        "observed_manifest_sha256": "0" * 64,
        "observed_members": [],
        "manual_attestation": None,
        "checks": {name: pending(name) for name in (
            "schema_shape", "referential_integrity", "evidence_adequacy",
            "source_validation", "render_inspection", "semantic_reconciliation",
            "accessibility", "persistence",
        )},
        "overall": "DRAFT",
        "blockers": [],
    }


def write_staging(
    base: Path,
    *,
    diagram_id: str = "reviewer-action",
    broken_reference: bool = False,
    invalid_tag: bool = False,
) -> Path:
    staging = base / "staging"
    staging.mkdir(parents=True)
    (staging / "diagram.mmd").write_text(
        "flowchart LR\n  A[Draft received] --> B{Reviewer action}\n",
        encoding="utf-8",
    )
    (staging / "textual-equivalent.md").write_text(
        "# Textual Equivalent\n\nThe reviewer receives a draft and selects a documented action.\n",
        encoding="utf-8",
    )
    support_source = "MISSING" if broken_reference else "POL-12"
    model = {
        "contract_version": "2.0.0",
        "diagram_id": diagram_id,
        "revision": "r0001",
        "request_binding": {
            "request_id": f"request.{diagram_id}",
            "evidence_set_id": "POL-12",
            "request_sha256": "0" * 64,
            "evidence_snapshot_digest": None,
        },
        "reader_question": "What can the reviewer do after receiving a draft?",
        "caption": "Documented reviewer action after draft receipt.",
        "rationale": "A branch makes the documented alternatives easier to inspect.",
        "scope": {"coverage": "POL-12 sections 3-4", "completeness": "partial", "exclusions": ["Publication"]},
        "sources": [{
            "source_id": "POL-12",
            "source_type": "document",
            "location": "POL-12",
            "authority_role": "governing",
            "content_digest": None,
            "locators": [{"locator_id": "S3", "selector": "section 3", "excerpt": "Reviewer may approve or request changes."}],
        }],
        "claims": [{
            "claim_id": "C-1",
            "exact_meaning": "The reviewer receives a draft.",
            "relation_kind": "flow",
            "status": "evidence-backed",
            "support": [{"source_id": support_source, "locator_id": "S3", "support_kind": "direct"}],
            "qualification": "Within the documented review step.",
            "load_bearing": True,
            "included": True,
        }],
        "elements": [{"element_id": "E-1", "element_type": "node", "label": "Draft received", "selector": "A", "claim_ids": ["C-1"]}],
        "encodings": [],
        "textual_equivalent_coverage": ["C-1"],
        "aggregate_status": "evidence-backed",
        "residue": [],
    }
    write_yaml(staging / "diagram.model.yml", model)
    request = {
        "contract_version": "2.0.0",
        "request_id": f"request.{diagram_id}",
        "mode": "create",
        "reader_question": model["reader_question"],
        "resolution": "Reviewer actions at policy-section resolution.",
        "evidence_set": {
            "evidence_set_id": "POL-12",
            "snapshot_digest": None,
            "sources": model["sources"],
        },
        "publication": {"destination": "draft workspace artifact", "official": False, "requested_readiness": "draft"},
        "output": {"representation_format": "mermaid", "target_renderer": None, "result_encoding": "markdown"},
        "storage": {"output_root": None, "allow_draft_fallback": True},
    }
    write_yaml(staging / "diagram.request.yml", request)
    topic = "Bad Tag" if invalid_tag else "review"
    manifest = {
        "contract_version": "2.0.0",
        "diagram_id": diagram_id,
        "revision": "r0001",
        "owner": "evidence-grounded-diagrams",
        "request_binding": model["request_binding"],
        "reader_question": model["reader_question"],
        "created_at": "2026-08-25T00:00:00Z",
        "lifecycle_status": "draft",
        "retention_class": "generated",
        "promotion_status": "not-promoted",
        "promotion_evidence": None,
        "aggregate_status": "evidence-backed",
        "supersedes": None,
        "tags": {
            "diagram_kind": "flowchart",
            "lifecycle": "draft",
            "epistemic": "evidence-backed",
            "scope": "partial",
            "topics": [topic],
            "extensions": [],
        },
        "members": {
            "request": {"path": "diagram.request.yml", "media_type": "application/yaml", "sha256": "0" * 64},
            "source": {"path": "diagram.mmd", "media_type": "text/vnd.mermaid", "sha256": "0" * 64},
            "render": None,
            "semantic_model": {"path": "diagram.model.yml", "media_type": "application/yaml", "sha256": "0" * 64},
            "textual_equivalent": {"path": "textual-equivalent.md", "media_type": "text/markdown", "sha256": "0" * 64},
            "validation_receipt": {"path": "validation.receipt.yml", "media_type": "application/yaml"},
        },
        "renderer": None,
        "persistence": {"state": "saved", "output_root": "pending", "bundle_path": "pending", "index_path": "pending"},
        "publication": {"destination": "draft workspace artifact", "official": False, "readiness": "draft"},
    }
    write_yaml(staging / "diagram.meta.yml", manifest)
    write_yaml(staging / "validation.receipt.yml", initial_receipt(diagram_id))
    return staging


def persist(staging: Path, output: Path) -> subprocess.CompletedProcess[str]:
    return run(
        sys.executable,
        str(PERSIST),
        "--staging-dir",
        str(staging),
        "--output-root",
        str(output),
    )


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    package = run(sys.executable, str(PACKAGE))
    expect(package.returncode == 0, package.stdout + package.stderr)
    with tempfile.TemporaryDirectory(prefix="egd-contract-") as temporary:
        base = Path(temporary)
        staging = write_staging(base / "valid")
        output = base / "artifacts"
        created = persist(staging, output)
        expect(created.returncode == 0, created.stdout + created.stderr)
        bundle = output / "reviewer-action" / "r0001"
        expect(bundle.is_dir(), "valid bundle was not persisted")
        receipt = yaml.safe_load((bundle / "validation.receipt.yml").read_text(encoding="utf-8"))
        expect(receipt["overall"] == "DRAFT", "source-only draft must remain DRAFT")
        expect(receipt["checks"]["persistence"]["status"] == "PASS", "persistence check did not pass")
        validated = run(sys.executable, str(VALIDATE), str(bundle))
        expect(validated.returncode == 0, validated.stdout + validated.stderr)

        duplicate = persist(staging, output)
        expect(duplicate.returncode != 0 and "overwrite existing revision" in (duplicate.stdout + duplicate.stderr), "duplicate revision was not blocked")

        invalid_staging = write_staging(base / "invalid-tag", invalid_tag=True)
        invalid_tag = persist(invalid_staging, base / "invalid-tag-artifacts")
        expect(invalid_tag.returncode != 0 and "Bad Tag" in (invalid_tag.stdout + invalid_tag.stderr), "invalid tag was not blocked")

        broken_staging = write_staging(base / "broken-reference", broken_reference=True)
        broken = persist(broken_staging, base / "broken-artifacts")
        expect(broken.returncode != 0 and "support does not resolve" in (broken.stdout + broken.stderr), "broken source reference was not blocked")

        (bundle / "diagram.mmd").write_text("flowchart LR\n  X --> Y\n", encoding="utf-8")
        stale = run(sys.executable, str(VALIDATE), str(bundle))
        expect(stale.returncode != 0 and "digest mismatch" in stale.stdout, "stale member digest was not blocked")

        manifest_path = bundle / "diagram.meta.yml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        manifest["publication"] = {"destination": "official-manual", "official": True, "readiness": "ready"}
        manifest["lifecycle_status"] = "published"
        manifest["tags"]["lifecycle"] = "published"
        write_yaml(manifest_path, manifest)
        false_ready = run(sys.executable, str(VALIDATE), str(bundle), "--write-receipt")
        expect(false_ready.returncode != 0 and "requires a render" in false_ready.stdout, "false official readiness was not blocked")

    print("BUNDLE_CONTRACT_TEST=pass")
    print("PROBES=package,valid-draft,duplicate-revision,invalid-tag,broken-reference,stale-digest,false-ready")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print("BUNDLE_CONTRACT_TEST=block")
        print(f"BLOCK: {exc}")
        raise SystemExit(1)
