#!/usr/bin/env python3
"""Adversarial probes for persistence, receipts, request binding, and telemetry."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from test_bundle_contract import persist, run, write_staging, write_yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
TEMPLATES = ROOT / "templates"
VALIDATE = ROOT / "scripts" / "validate_diagram_bundle.py"
VALIDATE_REVIEW = ROOT / "scripts" / "validate_review_receipt.py"
LIST = ROOT / "scripts" / "list_diagram_bundles.py"
TELEMETRY = ROOT / "scripts" / "record_usage_event.py"


def expect(condition: bool, message: str, result: subprocess.CompletedProcess[str] | None = None) -> None:
    if condition:
        return
    details = "" if result is None else f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    raise AssertionError(message + details)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="egd-security-") as temporary:
        temp = Path(temporary)

        request_schema = load_yaml(SCHEMAS / "diagram-request.schema.yml")
        inline_request = load_yaml(TEMPLATES / "diagram-request.yml")
        source = "flowchart LR\n  A --> B"
        inline_request["mode"] = "review"
        inline_request["mutation_authorized"] = False
        inline_request["target"] = {
            "kind": "source",
            "source_path": None,
            "inline_content": source,
            "normalization": "UTF-8, LF line endings, no trailing newline",
            "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(),
        }
        inline_errors = list(
            Draft202012Validator(
                request_schema, format_checker=FormatChecker()
            ).iter_errors(inline_request)
        )
        expect(not inline_errors, f"inline review request is not schema-valid: {inline_errors}")

        valid_stage = write_staging(temp / "valid")
        output = temp / "valid-output"
        created = persist(valid_stage, output)
        expect(created.returncode == 0, "security baseline did not persist", created)
        bundle = output / "reviewer-action" / "r0001"
        receipt_path = bundle / "validation.receipt.yml"
        honest_receipt = load_yaml(receipt_path)

        subset_receipt = copy.deepcopy(honest_receipt)
        subset_receipt["observed_members"] = []
        write_yaml(receipt_path, subset_receipt)
        listed_subset = run(sys.executable, str(LIST), str(output), "--json")
        expect(json.loads(listed_subset.stdout) == [], "resolver accepted receipt-selected empty coverage", listed_subset)
        write_yaml(receipt_path, honest_receipt)

        forged = copy.deepcopy(honest_receipt)
        for name in (
            "evidence_adequacy", "source_validation", "render_inspection",
            "semantic_reconciliation", "accessibility",
        ):
            forged["checks"][name] = {
                "status": "PASS",
                "assessor": "self-forged",
                "evidence": "Untrusted receipt edit.",
                "limitations": [],
            }
        forged["overall"] = "PASS"
        forged["blockers"] = []
        write_yaml(receipt_path, forged)
        forged_result = run(sys.executable, str(VALIDATE), str(bundle))
        expect(forged_result.returncode != 0, "self-forged manual PASS was accepted", forged_result)
        write_yaml(receipt_path, honest_receipt)

        review_receipt = load_yaml(TEMPLATES / "review.receipt.yml")
        review_receipt["target"] = {
            "kind": "bundle",
            "diagram_id": "reviewer-action",
            "revision": "r0001",
            "bundle_path": str(bundle),
            "normalization": "not applicable",
            "observed_members": [
                {"role": "manifest", "path": "diagram.meta.yml", "sha256": digest(bundle / "diagram.meta.yml")}
            ],
            "render_inspected": False,
        }
        review_path = temp / "partial-review.yml"
        write_yaml(review_path, review_receipt)
        partial_review = run(
            sys.executable, str(VALIDATE_REVIEW), str(review_path), "--bundle-root", str(bundle)
        )
        expect(partial_review.returncode != 0, "partial bundle review receipt passed", partial_review)

        role_paths = {
            "manifest": "diagram.meta.yml",
            "request": "diagram.request.yml",
            "source": "diagram.mmd",
            "semantic-model": "diagram.model.yml",
            "textual-equivalent": "textual-equivalent.md",
            "validation-receipt": "validation.receipt.yml",
        }
        review_receipt["target"]["observed_members"] = [
            {"role": role, "path": relative, "sha256": digest(bundle / relative)}
            for role, relative in role_paths.items()
        ]
        complete_review_path = temp / "complete-review.yml"
        write_yaml(complete_review_path, review_receipt)
        complete_review = run(
            sys.executable,
            str(VALIDATE_REVIEW),
            str(complete_review_path),
            "--bundle-root",
            str(bundle),
        )
        expect(complete_review.returncode == 0, "complete bundle review receipt failed", complete_review)

        attestation = load_yaml(TEMPLATES / "manual-attestation.yml")
        attestation["observed_manifest_sha256"] = digest(bundle / "diagram.meta.yml")
        attestation["observed_members"] = copy.deepcopy(honest_receipt["observed_members"])
        attestation["checks"]["render_inspection"] = {
            "status": "N/A",
            "evidence": "The tested bundle has no render member.",
            "limitations": ["This attestation does not approve official publication."],
        }
        attestation_path = temp / "manual-attestation.yml"
        write_yaml(attestation_path, attestation)
        attested = run(
            sys.executable,
            str(VALIDATE),
            str(bundle),
            "--manual-attestation",
            str(attestation_path),
            "--write-receipt",
        )
        expect(attested.returncode == 0, "explicit bound attestation failed", attested)
        attested_receipt = load_yaml(receipt_path)
        expect(
            attested_receipt["manual_attestation"]["sha256"] == digest(attestation_path),
            "attestation provenance was not recorded",
        )
        expect(
            attested_receipt["overall"] == "DRAFT",
            "caller-authored external attestation minted authoritative PASS",
        )
        for name in (
            "evidence_adequacy", "source_validation", "render_inspection",
            "semantic_reconciliation", "accessibility",
        ):
            expect(
                any(
                    "no configured attestor trust anchor" in limitation
                    for limitation in attested_receipt["checks"][name]["limitations"]
                ),
                f"manual check {name} omitted the advisory trust boundary",
            )
        untrusted_recheck = run(sys.executable, str(VALIDATE), str(bundle))
        expect(
            untrusted_recheck.returncode != 0,
            "manual PASS survived without the explicit external attestation",
            untrusted_recheck,
        )
        trusted_recheck = run(
            sys.executable,
            str(VALIDATE),
            str(bundle),
            "--manual-attestation",
            str(attestation_path),
        )
        expect(trusted_recheck.returncode == 0, "bound attestation did not revalidate", trusted_recheck)

        drift_stage = write_staging(temp / "evidence-drift", diagram_id="evidence-drift")
        drift_request = load_yaml(drift_stage / "diagram.request.yml")
        drift_request["evidence_set"]["sources"][0]["location"] = "substituted/source"
        write_yaml(drift_stage / "diagram.request.yml", drift_request)
        drift = persist(drift_stage, temp / "drift-output")
        expect(drift.returncode != 0, "evidence-set substitution passed", drift)

        malformed_stage = write_staging(temp / "index-failure", diagram_id="index-failure")
        malformed_output = temp / "malformed-output"
        malformed_output.mkdir()
        (malformed_output / "index.yml").write_text("entries: not-a-list\n", encoding="utf-8")
        malformed = persist(malformed_stage, malformed_output)
        expect(malformed.returncode != 0, "malformed index unexpectedly persisted", malformed)
        expect(
            not (malformed_output / "index-failure" / "r0001").exists(),
            "index failure left a half-committed final revision",
        )
        quarantine_entries = list(
            (malformed_output / ".quarantine" / "index-failure").glob("r0001-*")
        )
        expect(
            bool(quarantine_entries),
            "index failure was not quarantined; tree="
            + repr([str(path.relative_to(malformed_output)) for path in malformed_output.rglob("*")]),
            malformed,
        )

        recovery_stage = write_staging(temp / "orphan-recovery", diagram_id="orphan-recovery")
        recovery_output = temp / "recovery-output"
        orphan = recovery_output / "orphan-recovery" / "r0001"
        orphan.mkdir(parents=True)
        (orphan / "incomplete.txt").write_text("simulated crash residue", encoding="utf-8")
        recovered = persist(recovery_stage, recovery_output)
        expect(recovered.returncode == 0, "retry did not recover an orphaned final revision", recovered)
        expect(
            "RECOVERED_ORPHAN_TO_QUARANTINE=" in recovered.stderr,
            "orphan recovery was not reported",
            recovered,
        )
        expect((recovery_output / "orphan-recovery" / "r0001" / "diagram.meta.yml").is_file(), "recovered retry did not persist the new revision")

        finalize_stage = write_staging(temp / "unmarked-final", diagram_id="unmarked-final")
        finalize_output = temp / "unmarked-final-output"
        finalized_once = persist(finalize_stage, finalize_output)
        expect(finalized_once.returncode == 0, "unmarked-final baseline did not persist", finalized_once)
        finalize_bundle = finalize_output / "unmarked-final" / "r0001"
        finalize_marker = (
            finalize_output / ".evidence-grounded-diagrams" / "commits"
            / "unmarked-final" / "r0001.yml"
        )
        before_finalize = {
            path.name: digest(path) for path in finalize_bundle.iterdir() if path.is_file()
        }
        finalize_marker.unlink()
        invisible = run(sys.executable, str(LIST), str(finalize_output), "--json")
        expect(json.loads(invisible.stdout) == [], "resolver exposed an unmarked transaction", invisible)
        finalized_retry = persist(finalize_stage, finalize_output)
        expect(finalized_retry.returncode == 0, "valid unmarked transaction did not finalize", finalized_retry)
        expect(
            "FINALIZED_UNMARKED_COMMIT=" in finalized_retry.stderr,
            "idempotent unmarked finalization was not reported",
            finalized_retry,
        )
        expect(finalize_marker.is_file(), "retry did not restore the commit marker")
        after_finalize = {
            path.name: digest(path) for path in finalize_bundle.iterdir() if path.is_file()
        }
        expect(before_finalize == after_finalize, "unmarked finalization rewrote bundle bytes")

        replay_stage = write_staging(temp / "committed-replay", diagram_id="committed-replay")
        replay_output = temp / "committed-replay-output"
        first_commit = persist(replay_stage, replay_output)
        expect(first_commit.returncode == 0, "committed-replay baseline did not persist", first_commit)
        replay_bundle = replay_output / "committed-replay" / "r0001"
        replay_marker = (
            replay_output / ".evidence-grounded-diagrams" / "commits"
            / "committed-replay" / "r0001.yml"
        )
        expect(replay_marker.is_file(), "successful persistence omitted its commit marker")
        replay_source = replay_bundle / "diagram.mmd"
        replay_source.write_text("tampered committed history", encoding="utf-8")
        tampered_digest = digest(replay_source)
        replay_attempt = persist(replay_stage, replay_output)
        expect(
            replay_attempt.returncode != 0,
            "tampered committed revision identity was quarantined and reused",
            replay_attempt,
        )
        expect(
            replay_source.is_file() and digest(replay_source) == tampered_digest,
            "blocked replay changed the committed historical path",
        )
        expect(
            not list((replay_output / ".quarantine" / "committed-replay").glob("r0001-*")),
            "committed tamper was misclassified as recoverable crash residue",
        )

        concurrent_output = temp / "concurrent-output"
        stages = [
            write_staging(temp / "concurrent-a", diagram_id="concurrent-a"),
            write_staging(temp / "concurrent-b", diagram_id="concurrent-b"),
        ]
        processes = [
            subprocess.Popen(
                [sys.executable, str(ROOT / "scripts" / "persist_diagram_bundle.py"), "--staging-dir", str(stage), "--output-root", str(concurrent_output)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for stage in stages
        ]
        outcomes = [process.communicate(timeout=45) + (process.returncode,) for process in processes]
        expect(all(item[2] == 0 for item in outcomes), f"concurrent persistence failed: {outcomes}")
        concurrent_list = run(sys.executable, str(LIST), str(concurrent_output), "--json")
        expect(len(json.loads(concurrent_list.stdout)) == 2, "concurrent index update lost an entry", concurrent_list)

        event = json.loads((TEMPLATES / "usage-event.json").read_text(encoding="utf-8"))
        event["timestamp"] = "2026-08-25T20:00:00Z"
        event_paths: list[Path] = []
        for index in range(2):
            candidate = copy.deepcopy(event)
            candidate["diagram_id"] = f"telemetry-{index}"
            path = temp / f"event-{index}.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            event_paths.append(path)
        ledger = temp / "usage-events.jsonl"
        telemetry_processes = [
            subprocess.Popen(
                [sys.executable, str(TELEMETRY), "--event", str(path), "--ledger", str(ledger)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for path in event_paths
        ]
        telemetry_outcomes = [process.communicate(timeout=20) + (process.returncode,) for process in telemetry_processes]
        expect(all(item[2] == 0 for item in telemetry_outcomes), f"concurrent telemetry append failed: {telemetry_outcomes}")
        lines = ledger.read_text(encoding="utf-8").splitlines()
        expect(len(lines) == 2 and all(isinstance(json.loads(line), dict) for line in lines), "telemetry ledger was truncated or interleaved")

    print("SECURITY_CONTRACT_TESTS=pass")
    print("CASES=inline-review-request,receipt-exact-coverage,manual-pass-forgery,review-bundle-binding,external-attestation-advisory,evidence-set-binding,index-failure-rollback,crash-orphan-recovery,unmarked-invisible-idempotent-finalize,committed-revision-no-reuse,concurrent-index,concurrent-telemetry")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print("SECURITY_CONTRACT_TESTS=block")
        print(f"BLOCK: {exc}")
        raise SystemExit(1)
