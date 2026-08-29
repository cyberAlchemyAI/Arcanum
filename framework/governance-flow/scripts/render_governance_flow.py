#!/usr/bin/env python3
"""Render a deterministic human view from a validated governance-flow graph."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from compile_governance_flow import GovernanceFlowError, verify_graph


SCRIPT_PATH = Path(__file__).resolve()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def renderer_digest() -> str:
    return sha256_bytes(SCRIPT_PATH.read_bytes())


def _display(value: Any) -> str:
    if isinstance(value, bool):
        return "allowed" if value else "denied"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "none"
    return str(value)


def _cell(value: Any) -> str:
    return _display(value).replace("|", "\\|").replace("\n", "<br>")


def render_graph(graph: dict[str, Any], *, exact_renderer_digest: str | None = None) -> str:
    verify_graph(graph)
    envelope = graph["decision_envelope"]
    authority = envelope["authority"]
    executable = envelope["executable"]
    terminal = envelope["terminal_outcome"]
    render_digest = exact_renderer_digest or renderer_digest()

    lines = [
        "# Governance Flow Decision View",
        "",
        "> Deterministically derived from the schema-valid machine graph. This view is non-authoritative and cannot widen its source.",
        "",
        "## Digest Bindings",
        "",
        f"- Source SHA-256: `{graph['source_digest']}`",
        f"- Decision graph SHA-256: `{graph['decision_graph_digest']}`",
        f"- Renderer SHA-256: `{render_digest}`",
        "",
        "## Decision Identity",
        "",
        f"- Flow: `{graph['flow_id']}`",
        f"- Owner: `{envelope['owner']['owner_id']}`",
        f"- Lifecycle route: `{envelope['owner']['lifecycle_route']}`",
        f"- Request budget: `{envelope['request_budget']}`",
        "",
        "## Exact Targets",
        "",
        "| Path | Baseline SHA-256 | Postimage SHA-256 | Visibility |",
        "| --- | --- | --- | --- |",
    ]
    for target in envelope["targets"]:
        lines.append(
            "| `{}` | `{}` | `{}` | `{}` |".format(
                _cell(target["path"]),
                target["baseline_sha256"],
                target["postimage_sha256"],
                target["visibility"],
            )
        )

    lines.extend(["", "## Authority and Risk", ""])
    for key in (
        "write_paths",
        "execution",
        "publication",
        "git",
        "deployment",
        "credentials",
        "destructive_actions",
        "external_effects",
        "successor_execution",
        "selection_required",
        "admission_required",
    ):
        lines.append(f"- {key.replace('_', ' ').title()}: `{_display(authority[key])}`")
    lines.extend(
        [
            f"- Risk class: `{envelope['risk']['class']}`",
            f"- Risk reasons: `{_display(envelope['risk']['reasons'])}`",
            "",
            "## Authority-Bearing Executable",
            "",
            f"- Path: `{executable['path']}`",
            f"- SHA-256: `{executable['sha256']}`",
            f"- Mode: `{executable['mode']}`",
            f"- Arguments: `{json.dumps(executable['argv'], separators=(',', ':'))}`",
            f"- Working directory: `{executable['cwd']}`",
            f"- Environment allowlist: `{_display(executable['environment_allowlist'])}`",
            "",
            "## Independent Review",
            "",
            f"- Required: `{_display(envelope['independent_review']['required'])}`",
            f"- Reviewer: `{envelope['independent_review']['reviewer_id']}`",
            f"- Reviewer role: `{envelope['independent_review']['reviewer_role']}`",
            "",
            "## Terminal Outcome",
            "",
            f"- Promised boundary: `{terminal['promised_boundary_id']}`",
            f"- Required effects: `{_display(terminal['required_effects'])}`",
            f"- Prohibited effects: `{_display(terminal['prohibited_effects'])}`",
            f"- Completion predicate: `{terminal['completion_predicate']}`",
            f"- Terminal observer: `{terminal['terminal_observer']['observer_id']}`",
            "",
            "## Mode Boundary",
            "",
            "1. Preacceptance collects every reachable no-effect blocker and preserves the first nonzero.",
            "2. Human-decision mode emits at most one idempotent request for this frozen graph and stops.",
            "3. Effectful execution requires exact acceptance, selection, and admission, then fails fast to the promised terminal boundary.",
            "",
            "Preparation, rehearsal, freeze, review, and request emission grant no execution, publication, Git, deployment, credential, destructive-action, external-effect, or successor authority.",
            "",
            "## Metric Targets",
            "",
            "| Metric | Event | Target |",
            "| --- | --- | --- |",
        ]
    )
    for metric in envelope["metrics"]:
        lines.append(
            f"| `{metric['metric_id']}` | `{metric['event']}` | `{metric['target']}` |"
        )
    lines.extend(
        [
            "",
            "Aggregate completion remains false until the exact terminal receipt satisfies the frozen terminal predicate; component PASS is not terminal completion.",
            "",
        ]
    )
    return "\n".join(lines)


def verify_human_view(graph: dict[str, Any], human_view: str) -> None:
    expected = render_graph(graph)
    if human_view != expected:
        raise GovernanceFlowError("human view bytes or digest bindings are stale")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    graph = json.loads(args.graph.read_text(encoding="utf-8"))
    rendered = render_graph(graph)
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            raise GovernanceFlowError("human view differs from deterministic rendering")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
