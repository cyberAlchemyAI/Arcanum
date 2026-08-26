#!/usr/bin/env python3
"""Focused negative tests for promotion and persistence publication boundaries."""

from __future__ import annotations

import copy
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from test_bundle_contract import persist, write_staging, write_yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = ROOT / "schemas" / "diagram-bundle-manifest.schema.yml"


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def expect(
    condition: bool,
    message: str,
    result: subprocess.CompletedProcess[str] | None = None,
) -> None:
    if condition:
        return
    details = "" if result is None else f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    raise AssertionError(message + details)


def promotion_evidence() -> dict:
    return {
        "decision_id": "external-decision-001",
        "decided_at": "2026-08-25T00:00:00Z",
        "subject": {
            "diagram_id": "promotion-boundary",
            "revision": "r0001",
            "pre_promotion_manifest_sha256": "b" * 64,
        },
        "authority": {
            "identity": "external-governance-authority",
            "basis": "Authority is asserted as provenance; trust is decided outside this schema.",
        },
        "attestation": {
            "kind": "external-attestation",
            "path": "../external/promotion-attestation.yml",
            "media_type": "application/yaml",
            "sha256": "a" * 64,
        },
    }


def make_directory_redirect(link: Path, target: Path) -> tuple[bool, str]:
    try:
        os.symlink(target, link, target_is_directory=True)
        return True, "os.symlink"
    except OSError as symlink_error:
        if os.name != "nt":
            return False, f"os.symlink unavailable: {symlink_error}"
        junction = subprocess.run(
            ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
            check=False,
            capture_output=True,
            text=True,
        )
        if junction.returncode == 0:
            return True, "Windows junction"
        return False, (
            f"os.symlink unavailable: {symlink_error}; "
            f"junction unavailable: {junction.stderr.strip() or junction.stdout.strip()}"
        )


def main() -> int:
    schema = load_yaml(MANIFEST_SCHEMA)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    with tempfile.TemporaryDirectory(prefix="egd-persistence-boundary-") as temporary:
        temp = Path(temporary)

        ordinary_stage = write_staging(temp / "ordinary", diagram_id="promotion-boundary")
        ordinary_manifest = load_yaml(ordinary_stage / "diagram.meta.yml")
        expect(not list(validator.iter_errors(ordinary_manifest)), "ordinary manifest is invalid")

        promoted_without_evidence = copy.deepcopy(ordinary_manifest)
        promoted_without_evidence["promotion_status"] = "promoted"
        expect(
            bool(list(validator.iter_errors(promoted_without_evidence))),
            "schema accepted promoted status without external promotion evidence",
        )

        promoted_manifest = copy.deepcopy(ordinary_manifest)
        promoted_manifest["promotion_status"] = "promoted"
        promoted_manifest["promotion_evidence"] = promotion_evidence()
        expect(
            not list(validator.iter_errors(promoted_manifest)),
            "schema rejected a structurally complete external promotion evidence record",
        )
        write_yaml(ordinary_stage / "diagram.meta.yml", promoted_manifest)
        promoted_output = temp / "promoted-output"
        promoted_result = persist(ordinary_stage, promoted_output)
        expect(promoted_result.returncode != 0, "initial persistence accepted promoted draft", promoted_result)
        expect(
            not (promoted_output / "promotion-boundary" / "r0001").exists(),
            "rejected promoted draft created a final revision",
        )

        malformed_stage = write_staging(temp / "malformed", diagram_id="malformed-index")
        malformed_output = temp / "malformed-output"
        malformed_output.mkdir()
        index_path = malformed_output / "index.yml"
        original_index = b"entries: definitely-not-a-list\n"
        index_path.write_bytes(original_index)
        malformed_result = persist(malformed_stage, malformed_output)
        expect(malformed_result.returncode != 0, "malformed index unexpectedly persisted", malformed_result)
        expect(index_path.read_bytes() == original_index, "index rollback did not preserve original bytes")
        expect(
            not (malformed_output / "malformed-index" / "r0001").exists(),
            "post-rename index failure left an orphan at the final revision path",
        )
        expect(
            bool(list((malformed_output / ".quarantine" / "malformed-index").glob("r0001-*"))),
            "post-rename index failure did not quarantine the incomplete bundle",
        )

        redirect_stage = write_staging(temp / "redirect", diagram_id="redirected")
        redirect_output = temp / "redirect-output"
        outside = temp / "outside-output-root"
        redirect_output.mkdir()
        outside.mkdir()
        redirect = redirect_output / "redirected"
        created, method = make_directory_redirect(redirect, outside)
        if created:
            redirect_result = persist(redirect_stage, redirect_output)
            expect(
                redirect_result.returncode != 0,
                f"persistence traversed a destination {method}",
                redirect_result,
            )
            expect(
                not (outside / "r0001").exists(),
                f"destination {method} escaped the output root",
            )
            if os.path.lexists(redirect):
                if redirect.is_symlink():
                    redirect.unlink()
                else:
                    os.rmdir(redirect)
            confinement_status = f"pass ({method})"
        else:
            confinement_status = f"SKIP with evidence ({method})"

    print("PERSISTENCE_BOUNDARY_TESTS=pass")
    print(f"CONFINEMENT_PROBE={confinement_status}")
    print("CASES=promotion-evidence-schema,initial-promotion-rejection,index-rollback,post-rename-quarantine,reparse-confinement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
