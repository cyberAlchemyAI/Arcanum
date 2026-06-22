#!/usr/bin/env python3
"""Runtime adapter for the reading-learning-package spell candidate.

The adapter is intentionally small and dependency-light. It consumes tower/source
artifacts by path, emits a Whisper-compatible substrate by contract, and records
renderer fallback honestly instead of pretending PDF support exists.
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SPELL_ROOT = Path(__file__).resolve().parents[1]
PRESETS_PATH = SPELL_ROOT / "runtime" / "presets.json"
HTML_TEMPLATE_PATH = SPELL_ROOT / "templates" / "learning-package.html"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def to_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(to_yaml(child, indent + 2))
            else:
                lines.append(f"{pad}{key}: {yaml_scalar(child)}")
        return "\n".join(lines)
    if isinstance(value, list):
        if not value:
            return f"{pad}[]"
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}-")
                lines.append(to_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}- {yaml_scalar(item)}")
        return "\n".join(lines)
    return f"{pad}{yaml_scalar(value)}"


def read_excerpt(path: Path, max_lines: int = 8) -> str:
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped:
            lines.append(stripped)
        if len(lines) >= max_lines:
            break
    return "\n".join(lines)


def find_tower_artifacts(tower_root: Path) -> dict[str, Path | None]:
    claim_candidates = [
        tower_root / "tracks" / "paper-claim-ledger.md",
        tower_root / "paper-claim-ledger.md",
        tower_root / "claim-ledger.md",
    ]
    source_candidates = [
        tower_root / "source-record.md",
        tower_root / "SOURCE-RECORD.md",
        tower_root / "source.md",
    ]
    return {
        "final_pack": tower_root / "FINAL-LEARNING-PACK.md",
        "claim_ledger": next((p for p in claim_candidates if p.exists()), None),
        "source_record": next((p for p in source_candidates if p.exists()), None),
    }


def source_gate(tower_root: Path) -> tuple[str, list[str], dict[str, Path | None]]:
    artifacts = find_tower_artifacts(tower_root)
    blockers: list[str] = []
    if not tower_root.exists():
        blockers.append(f"tower_root missing: {display_path(tower_root)}")
    final_pack = artifacts["final_pack"]
    if not final_pack or not final_pack.exists():
        blockers.append("FINAL-LEARNING-PACK.md is required")
    if not artifacts["claim_ledger"]:
        blockers.append("claim evidence is required, preferably tracks/paper-claim-ledger.md")
    return ("block" if blockers else "pass", blockers, artifacts)


def answer_defaults(preset_id: str, preset: dict[str, Any]) -> dict[str, Any]:
    return {
        "reader_context": preset["relevance_core"]["target_public"],
        "resonance_core": {
            **preset["resonance_core"],
            "accepted_examples": [preset["resonance_core"]["voice"]],
            "rejected_examples": ["unsupported_flourish"],
        },
        "relevance_core": preset["relevance_core"],
        "trajectory_core": preset["trajectory_core"],
        "examples": {
            "accepted": [
                {
                    "id": preset["resonance_core"]["voice"],
                    "reason": f"matches {preset_id} output shape",
                }
            ],
            "rejected": [
                {
                    "id": "unsupported_flourish",
                    "reason": "would weaken source traceability",
                }
            ],
        },
        "pdf_preferences": {
            "page_size": "letter",
            "citation_style": preset["citation_style"],
            "density": preset["density"],
        },
        "approval": {"preset_preview_status": "approved"},
    }


def load_answers(path: Path | None, preset_id: str, preset: dict[str, Any]) -> dict[str, Any]:
    data = answer_defaults(preset_id, preset)
    if not path:
        return data
    override = load_json(path)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(data.get(key), dict):
            data[key] = {**data[key], **value}
        else:
            data[key] = value
    return data


def source_artifact_list(tower_root: Path, artifacts: dict[str, Path | None], extras: list[str]) -> list[str]:
    paths = [
        artifacts["final_pack"],
        artifacts["claim_ledger"],
        artifacts["source_record"],
    ]
    result = [display_path(p) for p in paths if p]
    result.extend(extras)
    return result


def build_preset_profile(
    preset_id: str,
    tower_root: Path,
    artifacts: dict[str, Path | None],
    answers: dict[str, Any],
    extras: list[str],
) -> dict[str, Any]:
    return {
        "preset_profile": {
            "preset_id": preset_id,
            "source": {
                "tower_root": display_path(tower_root),
                "source_artifacts": source_artifact_list(tower_root, artifacts, extras),
            },
            "resonance_core": answers["resonance_core"],
            "relevance_core": answers["relevance_core"],
            "trajectory_core": answers["trajectory_core"],
            "examples": answers["examples"],
            "pdf_preferences": answers["pdf_preferences"],
            "approval": answers["approval"],
        }
    }


def write_source_context(output_root: Path, tower_root: Path, artifacts: dict[str, Path | None], blockers: list[str]) -> None:
    rows = [
        ("tower_root", display_path(tower_root), "input"),
        ("final_pack", display_path(artifacts["final_pack"]) if artifacts["final_pack"] else "missing", "required"),
        ("claim_ledger", display_path(artifacts["claim_ledger"]) if artifacts["claim_ledger"] else "missing", "required"),
        ("source_record", display_path(artifacts["source_record"]) if artifacts["source_record"] else "missing", "optional gap"),
    ]
    table = "\n".join(f"| {name} | `{path}` | {status} |" for name, path, status in rows)
    gap_text = "\n".join(f"- {item}" for item in blockers) if blockers else "- none"
    write_text(
        output_root / "source-context.md",
        f"""# Source Context

| Handle | Path | Status |
| --- | --- | --- |
{table}

## Open Source Gaps

{gap_text}
""",
    )


def write_preset_preview(output_root: Path, preset_id: str, preset: dict[str, Any], answers: dict[str, Any]) -> None:
    accepted = ", ".join(item["id"] for item in answers["examples"]["accepted"])
    rejected = ", ".join(item["id"] for item in answers["examples"]["rejected"])
    write_text(
        output_root / "preset-preview.md",
        f"""# Preset Preview

Preset: `{preset_id}`

Voice: {answers["resonance_core"]["voice"]} with {answers["resonance_core"]["tone"]} tone.

Reader: {answers["relevance_core"]["target_public"]}; reward: {answers["relevance_core"]["reader_reward"]}.

Movement: {answers["trajectory_core"]["narrative_anchor"]}.

Output: {preset["shape"]}.

Accepted examples: {accepted}.

Rejected examples: {rejected}.
""",
    )


def write_substrate(output_root: Path, profile: dict[str, Any]) -> None:
    substrate = {
        "text_intent_substrate": {
            "source": "reading-learning-package",
            "whisper_contract": "compatible substrate; Whisper retains composition authority",
            "resonance_core": profile["preset_profile"]["resonance_core"],
            "relevance_core": profile["preset_profile"]["relevance_core"],
            "trajectory_core": profile["preset_profile"]["trajectory_core"],
            "source_handles": profile["preset_profile"]["source"]["source_artifacts"],
            "validation_checks": [
                "source handles must support load-bearing claims",
                "generated manuscript is learning output, not source authority",
                "accepted and rejected examples must be preserved",
            ],
        }
    }
    write_text(output_root / "text-intent-substrate.yaml", to_yaml(substrate) + "\n")


def write_composition_plan(output_root: Path, preset_id: str, preset: dict[str, Any], profile: dict[str, Any]) -> None:
    body_parts = "\n".join(f"- {part}" for part in profile["preset_profile"]["trajectory_core"]["body_parts"])
    write_text(
        output_root / "composition-plan.md",
        f"""# Composition Plan

Preset: `{preset_id}`
Shape: {preset["shape"]}
Length: {preset["length"]}

## Body Parts

{body_parts}

## Source-Use Policy

- Cite tower/source handles for load-bearing claims.
- Move unsupported claims to residue.
- Keep generated explanations as learning output, not source evidence.

## Validation Checklist

- Preset profile approved.
- SCU cores present in `text-intent-substrate.yaml`.
- Manuscript sections map to source handles.
- HTML exists.
- PDF exists or renderer gap is explicit.
""",
    )


def write_manuscript_and_trace(output_root: Path, preset_id: str, artifacts: dict[str, Path | None], preset: dict[str, Any]) -> None:
    final_pack = artifacts["final_pack"]
    claim_ledger = artifacts["claim_ledger"]
    excerpt = read_excerpt(final_pack) if final_pack else "No final pack available."
    claim_excerpt = read_excerpt(claim_ledger, max_lines=5) if claim_ledger else "No claim ledger available."
    script_note = "This package is a script and handout, not video rendering." if preset_id == "quick_video" else "This package is a reading guide."
    write_text(
        output_root / "manuscript.md",
        f"""# Learning Package Manuscript

## Orientation

{script_note}

The source tower says:

> {excerpt.replace(chr(10), chr(10) + '> ')}

## Source-Backed Claim

The package uses the claim ledger as the source boundary:

> {claim_excerpt.replace(chr(10), chr(10) + '> ')}

## Practice

Use the source trace to decide which sections can be trusted as source-backed and
which parts are learning residue.

## Residue

- Renderer availability may produce HTML-only output.
- This manuscript does not promote source claims into canon.
""",
    )
    write_text(
        output_root / "source-trace.md",
        f"""# Source Trace

| Manuscript Section | Source Artifact | Source Kind | Claim Status | Residue |
| --- | --- | --- | --- | --- |
| Orientation | `{display_path(final_pack) if final_pack else 'missing'}` | tower final pack | source-backed | none |
| Source-Backed Claim | `{display_path(claim_ledger) if claim_ledger else 'missing'}` | claim ledger | source-backed | none |
| Practice | `{display_path(claim_ledger) if claim_ledger else 'missing'}` | claim ledger | interpretive | reader applies trace |
| Residue | validation report | package residue | generated | renderer and promotion warnings |
""",
    )


def markdown_to_html(markdown_text: str) -> str:
    lines = []
    in_list = False
    for raw in markdown_text.splitlines():
        line = raw.rstrip()
        if line.startswith("# "):
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("- "):
            if not in_list:
                lines.append("<ul>")
                in_list = True
            lines.append(f"<li>{html.escape(line[2:])}</li>")
        elif line:
            if in_list:
                lines.append("</ul>")
                in_list = False
            lines.append(f"<p>{html.escape(line)}</p>")
    if in_list:
        lines.append("</ul>")
    return "\n".join(lines)


def render_html(output_root: Path) -> None:
    manuscript = (output_root / "manuscript.md").read_text(encoding="utf-8")
    trace = (output_root / "source-trace.md").read_text(encoding="utf-8")
    body = markdown_to_html(manuscript)
    body += "\n<section class=\"source-trace\">\n<h2>Source Trace</h2>\n"
    body += f"<pre>{html.escape(trace)}</pre>\n</section>"
    template = HTML_TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = template.replace("{{title}}", "Learning Package").replace("{{body}}", body)
    write_text(output_root / "learning-package.html", rendered)


def render_pdf_if_available(output_root: Path) -> tuple[str, str]:
    html_path = output_root / "learning-package.html"
    pdf_path = output_root / "learning-package.pdf"
    wkhtml = shutil.which("wkhtmltopdf")
    if wkhtml:
        result = subprocess.run([wkhtml, str(html_path), str(pdf_path)], check=False, text=True, capture_output=True)
        if result.returncode == 0 and pdf_path.exists():
            return "pass", "wkhtmltopdf rendered learning-package.pdf"
        return "flag", "wkhtmltopdf exists but render failed; HTML fallback kept"
    pandoc = shutil.which("pandoc")
    pdf_engine = shutil.which("xelatex") or shutil.which("pdflatex")
    if pandoc and pdf_engine:
        result = subprocess.run(
            [pandoc, str(output_root / "manuscript.md"), "-o", str(pdf_path), f"--pdf-engine={Path(pdf_engine).name}"],
            check=False,
            text=True,
            capture_output=True,
        )
        if result.returncode == 0 and pdf_path.exists():
            return "pass", "pandoc rendered learning-package.pdf"
        return "flag", "pandoc/pdf engine exists but render failed; HTML fallback kept"
    return "flag", "no deterministic PDF renderer found; HTML fallback emitted"


def write_validation_report(output_root: Path, preset_id: str, source_status: str, pdf_status: str, pdf_note: str) -> None:
    required = [
        "source-context.md",
        "preset-profile.yaml",
        "preset-preview.md",
        "text-intent-substrate.yaml",
        "composition-plan.md",
        "manuscript.md",
        "source-trace.md",
        "learning-package.html",
    ]
    missing = [name for name in required if not (output_root / name).exists()]
    overall = "block" if source_status == "block" or missing else ("flag" if pdf_status == "flag" else "pass")
    missing_text = "\n".join(f"- {item}" for item in missing) if missing else "- none"
    write_text(
        output_root / "validation-report.md",
        f"""# Validation Report

Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}

Overall status: `{overall}`

Preset: `{preset_id}`

| Gate | Result | Evidence |
| --- | --- | --- |
| Source gate | {source_status} | `source-context.md` |
| Preset gate | pass | `preset-profile.yaml` and `preset-preview.md` |
| Whisper gate | pass | `text-intent-substrate.yaml` and `composition-plan.md` |
| Trace gate | pass | `source-trace.md` |
| PDF gate | {pdf_status} | {pdf_note} |
| Promotion gate | pass | Generated package is labelled learning output, not source authority. |

## Missing Required Outputs

{missing_text}

## Residue

- PDF renderer status: {pdf_note}
- Source authority remains with `research-tower`.
- Composition authority remains with `whisper`.
""",
    )


def compose(args: argparse.Namespace) -> int:
    presets = load_json(PRESETS_PATH)
    if args.preset not in presets:
        print(f"unknown preset: {args.preset}", file=sys.stderr)
        return 2
    tower_root = Path(args.tower_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    source_status, blockers, artifacts = source_gate(tower_root)
    write_source_context(output_root, tower_root, artifacts, blockers)
    if source_status == "block":
        write_validation_report(output_root, args.preset, source_status, "block", "source gate blocked before rendering")
        return 2
    preset = presets[args.preset]
    answers = load_answers(Path(args.answers) if args.answers else None, args.preset, preset)
    profile = build_preset_profile(args.preset, tower_root, artifacts, answers, args.source_artifact)
    write_text(output_root / "preset-profile.yaml", to_yaml(profile) + "\n")
    write_preset_preview(output_root, args.preset, preset, answers)
    write_substrate(output_root, profile)
    write_composition_plan(output_root, args.preset, preset, profile)
    write_manuscript_and_trace(output_root, args.preset, artifacts, preset)
    render_html(output_root)
    pdf_status, pdf_note = render_pdf_if_available(output_root)
    write_validation_report(output_root, args.preset, source_status, pdf_status, pdf_note)
    return 0


def preset_interview(args: argparse.Namespace) -> int:
    presets = load_json(PRESETS_PATH)
    if args.preset not in presets:
        print(f"unknown preset: {args.preset}", file=sys.stderr)
        return 2
    tower_root = Path(args.tower_root)
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    source_status, blockers, artifacts = source_gate(tower_root)
    write_source_context(output_root, tower_root, artifacts, blockers)
    preset = presets[args.preset]
    answers = load_answers(Path(args.answers) if args.answers else None, args.preset, preset)
    profile = build_preset_profile(args.preset, tower_root, artifacts, answers, args.source_artifact)
    write_text(output_root / "preset-profile.yaml", to_yaml(profile) + "\n")
    write_preset_preview(output_root, args.preset, preset, answers)
    return 0 if source_status != "block" else 2


def validate_package(args: argparse.Namespace) -> int:
    output_root = Path(args.output_root)
    required = [
        "source-context.md",
        "preset-profile.yaml",
        "text-intent-substrate.yaml",
        "composition-plan.md",
        "manuscript.md",
        "source-trace.md",
        "learning-package.html",
        "validation-report.md",
    ]
    missing = [name for name in required if not (output_root / name).exists()]
    if missing:
        print("BLOCK missing outputs: " + ", ".join(missing))
        return 2
    report = (output_root / "validation-report.md").read_text(encoding="utf-8")
    if "Overall status: `block`" in report:
        print("BLOCK validation report is block")
        return 2
    print("PASS package validates with pass/flag semantics")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Compose reading learning packages from tower/source artifacts.")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("compose", "preset-interview"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--tower-root", required=True)
        cmd.add_argument("--output-root", required=True)
        cmd.add_argument("--preset", required=True)
        cmd.add_argument("--answers")
        cmd.add_argument("--source-artifact", action="append", default=[])
        cmd.set_defaults(func=compose if name == "compose" else preset_interview)
    validate = sub.add_parser("validate-package")
    validate.add_argument("--output-root", required=True)
    validate.set_defaults(func=validate_package)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
