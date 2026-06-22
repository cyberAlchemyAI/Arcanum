#!/usr/bin/env python3
"""Run reading-learning-package public-safe fixtures."""

from __future__ import annotations

import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SPELL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SPELL_ROOT.parents[2]
RUNTIME = SPELL_ROOT / "runtime" / "reading_learning_package.py"
RESULTS = SPELL_ROOT / "validation" / "results"
DEMO_TOWER = SPELL_ROOT / "fixtures" / "demo-tower"
MISSING_TOWER = SPELL_ROOT / "fixtures" / "missing-tower"
PRESET_ANSWERS = SPELL_ROOT / "fixtures" / "preset-answers"
PRESETS = ["deep_voice_reading", "quick_video", "medium_explanation"]


def rel(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)


def assert_contains(path: Path, text: str, failures: list[str]) -> None:
    content = path.read_text(encoding="utf-8")
    if text not in content:
        failures.append(f"{rel(path)} missing expected text: {text}")


def validate_preset(preset: str, rows: list[tuple[str, str, str]], failures: list[str]) -> None:
    output = RESULTS / "outputs" / preset
    cmd = [
        sys.executable,
        rel(RUNTIME),
        "compose",
        "--tower-root",
        rel(DEMO_TOWER),
        "--output-root",
        rel(output),
        "--preset",
        preset,
        "--answers",
        rel(PRESET_ANSWERS / f"{preset}.json"),
    ]
    result = run(cmd)
    rows.append((preset, "compose", "pass" if result.returncode == 0 else "block"))
    if result.returncode != 0:
        failures.append(f"{preset} compose failed: {result.stderr or result.stdout}")
        return

    required = [
        "source-context.md",
        "preset-profile.yaml",
        "preset-preview.md",
        "text-intent-substrate.yaml",
        "composition-plan.md",
        "manuscript.md",
        "source-trace.md",
        "learning-package.html",
        "validation-report.md",
    ]
    for name in required:
        if not (output / name).exists():
            failures.append(f"{preset} missing {name}")
    assert_contains(output / "preset-profile.yaml", f'preset_id: "{preset}"', failures)
    assert_contains(output / "preset-profile.yaml", "accepted:", failures)
    assert_contains(output / "preset-profile.yaml", "rejected:", failures)
    assert_contains(output / "text-intent-substrate.yaml", "resonance_core:", failures)
    assert_contains(output / "text-intent-substrate.yaml", "relevance_core:", failures)
    assert_contains(output / "text-intent-substrate.yaml", "trajectory_core:", failures)
    assert_contains(output / "source-trace.md", "FINAL-LEARNING-PACK.md", failures)
    assert_contains(output / "source-trace.md", "paper-claim-ledger.md", failures)
    assert_contains(output / "validation-report.md", "Promotion gate", failures)
    if not (output / "learning-package.pdf").exists():
        assert_contains(output / "validation-report.md", "renderer", failures)

    validate = run([sys.executable, rel(RUNTIME), "validate-package", "--output-root", rel(output)])
    rows.append((preset, "validate-package", "pass" if validate.returncode == 0 else "block"))
    if validate.returncode != 0:
        failures.append(f"{preset} validate-package failed: {validate.stderr or validate.stdout}")


def validate_missing_source(rows: list[tuple[str, str, str]], failures: list[str]) -> None:
    output = RESULTS / "outputs" / "missing-source"
    result = run(
        [
            sys.executable,
            rel(RUNTIME),
            "compose",
            "--tower-root",
            rel(MISSING_TOWER),
            "--output-root",
            rel(output),
            "--preset",
            "medium_explanation",
        ]
    )
    status = "pass" if result.returncode != 0 else "block"
    rows.append(("missing-source", "source gate blocks", status))
    if result.returncode == 0:
        failures.append("missing-source fixture unexpectedly composed")
    report = output / "validation-report.md"
    if not report.exists():
        failures.append("missing-source fixture did not emit validation-report.md")
    else:
        assert_contains(report, "Overall status: `block`", failures)


def write_report(rows: list[tuple[str, str, str]], failures: list[str]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    table = "\n".join(f"| {name} | {check} | {status} |" for name, check, status in rows)
    failure_text = "\n".join(f"- {item}" for item in failures) if failures else "- none"
    overall = "pass" if not failures else "block"
    (RESULTS / "fixture-report.md").write_text(
        f"""# Reading Learning Package Fixture Report

Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}

Overall status: `{overall}`

| Fixture | Check | Result |
| --- | --- | --- |
{table}

## Evidence

- Preset variants: `deep_voice_reading`, `quick_video`, `medium_explanation`.
- Valid tower fixture: `{rel(DEMO_TOWER)}`.
- Missing-source fixture: `{rel(MISSING_TOWER)}`.
- Output root: `{rel(RESULTS / 'outputs')}`.
- HTML/PDF fallback: validation reports flag renderer gaps when no deterministic renderer is available.
- No-promotion boundary: validation reports keep generated learning output separate from source authority.

## Failures

{failure_text}
""",
        encoding="utf-8",
    )


def main() -> int:
    if (RESULTS / "outputs").exists():
        shutil.rmtree(RESULTS / "outputs")
    if (RESULTS / "fixture-report.md").exists():
        (RESULTS / "fixture-report.md").unlink()
    RESULTS.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, str, str]] = []
    failures: list[str] = []
    for preset in PRESETS:
        validate_preset(preset, rows, failures)
    validate_missing_source(rows, failures)
    write_report(rows, failures)
    print(rel(RESULTS / "fixture-report.md"))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
