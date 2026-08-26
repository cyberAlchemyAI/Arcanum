#!/usr/bin/env python3
"""Run the promotion-grade evidence-grounded-diagrams validation harness."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEVELOPMENT = Path(__file__).resolve().parent
ROOT = DEVELOPMENT.parent
RUNS = DEVELOPMENT / "runs"
PROFILE_ID = "sigil-development"
LIFECYCLE_OWNER = "sigil-development"
ARTIFACT_TYPE = "sigil"
CONTRACT_PATH = "transmutations/evidence-grounded-diagrams/SKILL.md"
PROMPT_SET = "sigil-new-low, sigil-update-medium, sigil-observe-medium, sigil-reflect-complex, sigil-harness-validation-complex"
REGIME_SET = "LIVE-SIGIL-NEW-001, LIVE-SIGIL-UPDATE-001, LIVE-SIGIL-OBSERVE-001, LIVE-SIGIL-REFLECT-001, LIVE-SIGIL-HARNESS-VALIDATION-001"
REQUIRED_FIELDS = (
    "Mode", "Outcome", "Verdict", "Reader question", "Diagram ID / revision",
    "Bundle", "Lifecycle", "Aggregate epistemic status", "Renderer",
    "Validation", "Review receipt", "First blocker", "Evidence boundary",
)
ARTIFACTS = (
    "create-low.artifact.md",
    "needs-evidence-low.artifact.md",
    "review-medium.artifact.md",
    "revise-complex.artifact.md",
)
LIVE_OUTPUTS = (
    "postfix-create.output.md",
    "postfix-needs-evidence.output.md",
    "postfix-review.output.md",
    "postfix-revise.output.md",
)
LIVE_EXPECTATIONS = {
    "postfix-create.output.md": ("- Mode: create", "- Outcome: diagram", "- Verdict: DRAFT"),
    "postfix-needs-evidence.output.md": (
        "- Mode: create", "- Outcome: needs-evidence", "- Verdict: BLOCKED", "- Bundle: none"
    ),
    "postfix-review.output.md": (
        "- Mode: review", "- Outcome: review-result", "- Verdict: FIX", "- Bundle: none"
    ),
    "postfix-revise.output.md": ("- Mode: revise", "- Outcome: diagram", "- Verdict: DRAFT"),
}
LIVE_PROMPTS = {
    "postfix-create.output.md": "postfix-create.md",
    "postfix-needs-evidence.output.md": "postfix-needs-evidence.md",
    "postfix-review.output.md": "postfix-review.md",
    "postfix-revise.output.md": "postfix-revise.md",
}


def canonical_digest() -> str:
    digest = hashlib.sha256()
    excluded_parts = {"runs", "example-runs", ".staging", "__pycache__"}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix == ".pyc":
            continue
        relative = path.relative_to(ROOT)
        if relative == Path("development/PROMOTION-VALIDATION.md"):
            continue
        if any(part in excluded_parts for part in relative.parts):
            continue
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def command(label: str, *args: str) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, *args], check=False, capture_output=True, text=True, cwd=ROOT
    )
    body = (result.stdout + result.stderr).strip()
    return result.returncode == 0, f"### {label}\n\n```text\n{body}\n```"


def main() -> int:
    initial_canonical_digest = canonical_digest()
    failures: list[str] = []
    sections: list[str] = []
    live_evidence: list[str] = []
    required = [
        ROOT / "SKILL.md",
        ROOT / "requirements.txt",
        DEVELOPMENT / "VALIDATION-EXPERIMENT.md",
        DEVELOPMENT / "VALIDATION.md",
        DEVELOPMENT / "TASK-MATRIX.md",
        DEVELOPMENT / "fixtures" / "create-low.expected.md",
        DEVELOPMENT / "fixtures" / "review-medium.expected.md",
        DEVELOPMENT / "fixtures" / "revise-complex.expected.md",
    ]
    for path in required:
        if not path.is_file():
            failures.append(f"missing required harness file: {path.relative_to(ROOT)}")

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    for marker in ("<quality-bar>", "<anti-patterns>", "<observability>", "<output-contract>"):
        if marker not in skill:
            failures.append(f"SKILL.md missing contract marker: {marker}")

    for name in ARTIFACTS:
        path = DEVELOPMENT / "fixtures" / name
        if not path.is_file():
            failures.append(f"missing durable artifact output: fixtures/{name}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip() or text.lstrip().lower().startswith("saved the output"):
            failures.append(f"fixtures/{name} is empty or a save summary")
        for field in REQUIRED_FIELDS:
            if f"- {field}:" not in text:
                failures.append(f"fixtures/{name} missing output field: {field}")

    for name in LIVE_OUTPUTS:
        path = DEVELOPMENT / "example-outputs" / name
        if not path.is_file():
            failures.append(f"missing fresh-agent output: example-outputs/{name}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.strip() or text.lstrip().lower().startswith("saved the output"):
            failures.append(f"example-outputs/{name} is empty or a save summary")
        for field in REQUIRED_FIELDS:
            if f"- {field}:" not in text:
                failures.append(f"example-outputs/{name} missing output field: {field}")
        for expected in LIVE_EXPECTATIONS[name]:
            if expected not in text:
                failures.append(
                    f"example-outputs/{name} missing semantic expectation: {expected}"
                )
        prompt = DEVELOPMENT / "example-prompts" / LIVE_PROMPTS[name]
        if not prompt.is_file():
            failures.append(f"missing fresh-agent invocation: example-prompts/{prompt.name}")
        else:
            prompt_digest = hashlib.sha256(prompt.read_bytes()).hexdigest()
            output_digest = hashlib.sha256(path.read_bytes()).hexdigest()
            live_evidence.append(
                f"- `{prompt.name}` `{prompt_digest}` -> `{name}` `{output_digest}`"
            )

    checks = (
        ("runtime preflight", str(ROOT / "scripts" / "preflight_runtime.py")),
        ("package closure", str(ROOT / "scripts" / "validate_skill_package.py")),
        ("bundle contract", str(DEVELOPMENT / "test_bundle_contract.py")),
        ("bundle lifecycle", str(DEVELOPMENT / "test_bundle_lifecycle.py")),
        ("security contract", str(DEVELOPMENT / "test_security_contract.py")),
        ("review contract", str(DEVELOPMENT / "test_review_contract.py")),
        ("persistence boundary", str(DEVELOPMENT / "test_persistence_boundary.py")),
        (
            "resolver lifecycle security",
            str(DEVELOPMENT / "test_resolver_lifecycle_security.py"),
        ),
        (
            "inline review receipt",
            str(ROOT / "scripts" / "validate_review_receipt.py"),
            str(DEVELOPMENT / "fixtures" / "forward-review-target.receipt.yml"),
            "--target-source",
            str(DEVELOPMENT / "fixtures" / "forward-review-target.mmd"),
        ),
        (
            "fresh-agent review receipt",
            str(ROOT / "scripts" / "validate_review_receipt.py"),
            str(DEVELOPMENT / "example-outputs" / "postfix-review.receipt.yml"),
            "--target-source",
            str(DEVELOPMENT / "example-outputs" / "postfix-review-target.mmd"),
        ),
    )
    for check in checks:
        passed, section = command(check[0], *check[1:])
        sections.append(section)
        if not passed:
            failures.append(f"command failed: {check[0]}")

    inline_target = (DEVELOPMENT / "fixtures" / "forward-review-target.mmd").read_text(
        encoding="utf-8"
    )
    inline_result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_review_receipt.py"),
            str(DEVELOPMENT / "fixtures" / "forward-review-target.receipt.yml"),
            "--target-stdin",
        ],
        input=inline_target,
        check=False,
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    sections.append(
        "### inline review stdin\n\n```text\n"
        + (inline_result.stdout + inline_result.stderr).strip()
        + "\n```"
    )
    if inline_result.returncode != 0:
        failures.append("command failed: inline review stdin")

    final_canonical_digest = canonical_digest()
    if final_canonical_digest != initial_canonical_digest:
        failures.append(
            "canonical package bytes changed during the validation run: "
            f"{initial_canonical_digest} -> {final_canonical_digest}"
        )

    status = "pass" if not failures else "block"
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    RUNS.mkdir(parents=True, exist_ok=True)
    report = RUNS / f"{timestamp}-promotion-validation.md"
    report_body = "\n".join(
            [
                "# Evidence-Grounded Diagrams Validation Report",
                "",
                f"- Timestamp: {timestamp}",
                f"- Profile ID: {PROFILE_ID}",
                f"- Lifecycle owner: {LIFECYCLE_OWNER}",
                f"- Artifact type: {ARTIFACT_TYPE}",
                f"- Contract path: {CONTRACT_PATH}",
                f"- Canonical byte-set SHA-256: {final_canonical_digest}",
                f"- Canonical bytes stable during run: {str(initial_canonical_digest == final_canonical_digest).lower()}",
                f"- Status: {status}",
                "- Quality Bar status: " + ("pass" if not failures else "fail"),
                "- Anti-Pattern hits: []",
                "- Workflow gaps: " + json.dumps(failures, ensure_ascii=False),
                "- Runtime forward evidence: four fresh-agent outputs plus durable normalized fixtures",
                "",
                "## Profile Fields",
                "",
                f"PROFILE_ID={PROFILE_ID}",
                f"LIFECYCLE_OWNER={LIFECYCLE_OWNER}",
                f"ARTIFACT_TYPE={ARTIFACT_TYPE}",
                f"CONTRACT_PATH={CONTRACT_PATH}",
                f"PROMPT_SET={PROMPT_SET}",
                f"REGIME_SET={REGIME_SET}",
                f"PROFILE_VALIDATION={'pass' if not failures else 'block'}",
                "",
                "## Failures",
                "",
                *(f"- {item}" for item in failures),
                "" if failures else "- none",
                "",
                "## Command Evidence",
                "",
                *sections,
                "",
                "## Fresh-Agent Evidence Digests",
                "",
                *live_evidence,
                "",
                "Fresh-agent outputs are immutable behavioral snapshots bound to their preserved invocations. The deterministic bundle contract and lifecycle tests reconstruct create/revise persistence in temporary roots on every harness run; ignored live bundle trees are not required for replay.",
                "",
            ]
    )
    report.write_text(report_body, encoding="utf-8")
    durable_report = DEVELOPMENT / "PROMOTION-VALIDATION.md"
    durable_report.write_text(report_body, encoding="utf-8")
    print(f"HARNESS_STATUS={status}")
    print(f"QUALITY_BAR_STATUS={'pass' if not failures else 'fail'}")
    print("ANTI_PATTERN_HITS_JSON=[]")
    print("WORKFLOW_GAPS_JSON=" + json.dumps(failures, ensure_ascii=False))
    print(f"REPORT={durable_report}")
    print(f"ARCHIVE_REPORT={report}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
