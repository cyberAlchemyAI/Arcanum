#!/usr/bin/env python3
"""Deterministic lifecycle tests for evidence-grounded diagram bundles."""

from __future__ import annotations

import json
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates"
PERSIST = ROOT / "scripts" / "persist_diagram_bundle.py"
VALIDATE = ROOT / "scripts" / "validate_diagram_bundle.py"
LIST = ROOT / "scripts" / "list_diagram_bundles.py"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def run(*args: str | Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *map(str, args)],
        check=False,
        capture_output=True,
        text=True,
    )


def make_stage(
    parent: Path,
    diagram_id: str,
    revision: str = "r0001",
    supersedes: dict[str, str] | None = None,
    target_bundle: Path | None = None,
) -> Path:
    stage = parent / f"stage-{diagram_id}-{revision}"
    stage.mkdir()
    for name in (
        "diagram.model.yml",
        "diagram.meta.yml",
        "diagram.request.yml",
        "textual-equivalent.md",
        "validation.receipt.yml",
    ):
        shutil.copy2(TEMPLATES / name, stage / name)
    (stage / "diagram.mmd").write_text(
        "flowchart LR\n  A[Draft] -->|directly supported flow| B[Review]\n",
        encoding="utf-8",
    )
    model = load_yaml(stage / "diagram.model.yml")
    manifest = load_yaml(stage / "diagram.meta.yml")
    receipt = load_yaml(stage / "validation.receipt.yml")
    request = load_yaml(stage / "diagram.request.yml")
    for value in (model, manifest, receipt):
        value["diagram_id"] = diagram_id
        value["revision"] = revision
    manifest["supersedes"] = supersedes
    if revision != "r0001":
        if target_bundle is None or supersedes is None:
            raise ValueError("revised stage requires target bundle and lineage")
        request["mode"] = "revise"
        request["mutation_authorized"] = True
        request["target"] = {
            "kind": "bundle",
            "diagram_id": diagram_id,
            "revision": supersedes["revision"],
            "bundle_path": str(target_bundle),
            "manifest_digest": supersedes["manifest_digest"],
        }
    manifest["owner"] = "lifecycle-test"
    write_yaml(stage / "diagram.model.yml", model)
    write_yaml(stage / "diagram.meta.yml", manifest)
    write_yaml(stage / "validation.receipt.yml", receipt)
    write_yaml(stage / "diagram.request.yml", request)
    return stage


def digest_map(bundle: Path) -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(bundle.iterdir())
        if path.is_file()
    }


def require(condition: bool, message: str, result: subprocess.CompletedProcess[str] | None = None) -> None:
    if condition:
        return
    details = ""
    if result is not None:
        details = f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    raise AssertionError(message + details)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="egd-lifecycle-") as temporary:
        temp = Path(temporary)
        output_root = temp / "artifacts"

        valid_stage = make_stage(temp, "valid-diagram")
        persisted = run(
            PERSIST,
            "--staging-dir",
            valid_stage,
            "--output-root",
            output_root,
        )
        require(persisted.returncode == 0, "valid draft did not persist", persisted)
        bundle = output_root / "valid-diagram" / "r0001"
        require(bundle.is_dir(), "persisted bundle directory is missing")
        verified = run(VALIDATE, bundle)
        require(verified.returncode == 0, "persisted draft did not validate", verified)
        require("BUNDLE_VALIDATION=draft" in verified.stdout, "draft verdict was not preserved", verified)

        listed = run(LIST, output_root, "--current", "--json")
        require(listed.returncode == 0, "bundle resolver failed", listed)
        records = json.loads(listed.stdout)
        require(len(records) == 1 and records[0]["diagram_id"] == "valid-diagram", "resolver missed bundle", listed)

        prior_manifest = bundle / "diagram.meta.yml"
        prior_digests = digest_map(bundle)
        prior_digest = prior_digests["diagram.meta.yml"]
        revision_stage = make_stage(
            temp,
            "valid-diagram",
            "r0002",
            {"revision": "r0001", "manifest_digest": prior_digest},
            bundle,
        )
        revised = run(
            PERSIST,
            "--staging-dir",
            revision_stage,
            "--output-root",
            output_root,
        )
        require(revised.returncode == 0, "valid revision lineage did not persist", revised)
        require(
            digest_map(bundle) == prior_digests,
            "new revision mutated at least one prior bundle member",
        )
        current_after_revision = run(LIST, output_root, "--current", "--json")
        current_records = json.loads(current_after_revision.stdout)
        require(
            len(current_records) == 1 and current_records[0]["revision"] == "r0002",
            "resolver did not select the newer draft revision",
            current_after_revision,
        )
        all_revisions = run(LIST, output_root, "--json")
        all_records = json.loads(all_revisions.stdout)
        prior_record = next(item for item in all_records if item["revision"] == "r0001")
        require(
            prior_record["lifecycle"] == "draft",
            "newer DRAFT incorrectly superseded the prior revision",
        )

        receipt_path = bundle / "validation.receipt.yml"
        honest_receipt = load_yaml(receipt_path)
        contradictory_receipt = dict(honest_receipt)
        contradictory_receipt["overall"] = "PASS"
        contradictory_receipt["blockers"] = []
        write_yaml(receipt_path, contradictory_receipt)
        contradicted = run(VALIDATE, bundle)
        require(contradicted.returncode != 0, "contradictory PASS receipt was accepted", contradicted)
        require("checks require 'DRAFT'" in contradicted.stdout, "receipt contradiction was not diagnosed", contradicted)
        write_yaml(receipt_path, honest_receipt)

        overwrite = run(
            PERSIST,
            "--staging-dir",
            valid_stage,
            "--output-root",
            output_root,
        )
        require(overwrite.returncode != 0, "existing revision was overwritten", overwrite)

        (bundle / "diagram.mmd").write_text("tampered", encoding="utf-8")
        tampered = run(VALIDATE, bundle)
        require(tampered.returncode != 0, "tampered source passed validation", tampered)
        require("digest mismatch" in tampered.stdout, "tamper failure lacked digest evidence", tampered)
        after_tamper = run(LIST, output_root, "--json")
        tamper_records = json.loads(after_tamper.stdout)
        require(
            all(item["revision"] != "r0001" for item in tamper_records),
            "tampered revision remained resolvable",
            after_tamper,
        )

        coverage_stage = make_stage(temp, "missing-coverage")
        coverage_model = load_yaml(coverage_stage / "diagram.model.yml")
        coverage_model["textual_equivalent_coverage"] = []
        write_yaml(coverage_stage / "diagram.model.yml", coverage_model)
        coverage = run(
            PERSIST,
            "--staging-dir",
            coverage_stage,
            "--output-root",
            output_root,
        )
        require(coverage.returncode != 0, "missing textual coverage passed", coverage)
        require("missing textual-equivalent coverage" in coverage.stdout, "coverage failure was not specific", coverage)

        unsafe_stage = make_stage(temp, "unsafe-path")
        unsafe_manifest = load_yaml(unsafe_stage / "diagram.meta.yml")
        unsafe_manifest["members"]["source"]["path"] = "../diagram.mmd"
        write_yaml(unsafe_stage / "diagram.meta.yml", unsafe_manifest)
        unsafe = run(
            PERSIST,
            "--staging-dir",
            unsafe_stage,
            "--output-root",
            output_root,
        )
        require(unsafe.returncode != 0, "path traversal passed persistence", unsafe)

    print("BUNDLE_LIFECYCLE_TESTS=pass")
    print("CASES=valid-draft,index-resolution,lineage,immutable-prior,draft-does-not-supersede,no-overwrite,receipt-consistency,tamper-exclusion,coverage,path-traversal")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
