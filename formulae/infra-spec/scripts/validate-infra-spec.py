#!/usr/bin/env python3
"""Validate Arcanum infra-spec CANDIDATE documents.

Two-layer validator (mirrors dispatch-spec):
  - shape layer:      JSON Schema (infra-spec.schema.json) checks structure.
  - governance layer: this script checks the infra-spec discipline rules that
    a schema cannot express (evidence != authority, reversal obligations, etc).

Output contract (parity with validate-dispatch.py):
  prints VALIDATION=pass|flag|block, then BLOCK:/FLAG: lines.
  exit 0 for pass/flag, exit 1 for block, exit 2 for tooling-blocked.

Status: CANDIDATE. Not promotion authority. See ../README.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    print("VALIDATION=blocked")
    print(f"BLOCKED: missing jsonschema dependency: {exc}", file=sys.stderr)
    raise SystemExit(2)

SCRIPT_DIR = Path(__file__).resolve().parent
PACKAGE = SCRIPT_DIR.parent
SCHEMA_PATH = PACKAGE / "infra-spec.schema.json"

# stages at or beyond which evidence is required (index = floor level)
STAGE_ORDER = ["specified", "implemented", "deployed", "observed", "validated", "reflected", "promoted"]
# borrowed-register vocabulary that must be analogy-labelled if used as an obligation
ANALOGY_TERMS = re.compile(
    r"\b(reflection tower|fixed point|functor|adjunction|kan extension|"
    r"entropy|noether|lawvere|isomorphism|same object|fractal)\b",
    re.IGNORECASE,
)


def stage_index(stage: str) -> int:
    return STAGE_ORDER.index(stage) if stage in STAGE_ORDER else -1


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def governance_checks(doc: dict[str, Any], blocks: list[str], flags: list[str]) -> None:
    services = doc.get("services", []) or []
    boundaries = doc.get("boundaries", []) or []
    gates = doc.get("gates", []) or []
    receipts = doc.get("receipts", []) or []
    observability = doc.get("observability", {}) or {}
    state_namespaces = doc.get("state_namespaces", []) or []
    promotion_status = doc.get("promotion_status", {}) or {}
    environments = doc.get("environments", []) or []
    stage = str(promotion_status.get("stage", ""))
    sidx = stage_index(stage)
    has_production_env = any(str(e.get("name", "")).lower() == "production" for e in environments)

    # Rule 1 - fail-closed gates: promotion_guardrail gates and secret/data_store boundaries must block.
    for g in gates:
        if g.get("kind") == "promotion_guardrail" and g.get("on_fail") != "block":
            blocks.append(f"rule1-fail-closed: gate '{g.get('gate_id')}' is a promotion_guardrail but on_fail='{g.get('on_fail')}' (must be 'block')")
    for b in boundaries:
        if b.get("kind") in {"secret", "data_store"} and b.get("on_violation") != "block":
            blocks.append(f"rule1-fail-closed: {b.get('kind')} boundary '{b.get('boundary_id')}' on_violation='{b.get('on_violation')}' (must be 'block')")

    # Rule 2 - status floor: deployed+ needs a receipt; validated+ needs observability/SLO evidence.
    if sidx >= stage_index("deployed") and not receipts:
        blocks.append(f"rule2-status-floor: stage '{stage}' requires at least one receipt but none declared")
    if sidx >= stage_index("validated"):
        has_obs = bool(observability.get("signal_refs") or observability.get("slo_refs") or observability.get("scrape_targets"))
        if not has_obs:
            blocks.append(f"rule2-status-floor: stage '{stage}' requires observability/SLO evidence but none declared")

    # Rule 3 - reversal obligations.
    needs_rollback = stage == "promoted" or has_production_env
    if needs_rollback:
        for s in services:
            rev = s.get("reversal", {}) or {}
            if not (rev.get("rollback")):
                blocks.append(f"rule3-reversal: service '{s.get('name')}' reaches promoted/production but has no reversal.rollback")
    for b in boundaries:
        if b.get("kind") == "data_store":
            rev = b.get("reversal", {}) or {}
            if not rev.get("backup"):
                blocks.append(f"rule3-reversal: data_store boundary '{b.get('boundary_id')}' has no reversal.backup")
    for s in services:
        mig = (s.get("reversal", {}) or {}).get("migration", {}) or {}
        if mig.get("forward") and not mig.get("reverse"):
            blocks.append(f"rule3-reversal: service '{s.get('name')}' migration has 'forward' but no 'reverse'")

    # Rule 4 - unowned state: every data_store boundary must map to a state_namespace with exactly one owner.
    ns_owners: dict[str, set] = {}
    for ns in state_namespaces:
        ns_owners.setdefault(ns.get("namespace", ""), set()).add(ns.get("owner", ""))
    for b in boundaries:
        if b.get("kind") == "data_store":
            owners = ns_owners.get("runtime", set()) | ns_owners.get("evidence", set()) | ns_owners.get("generated", set())
            if not owners:
                blocks.append(f"rule4-unowned-state: data_store boundary '{b.get('boundary_id')}' has no owning state_namespace")
    for nsname, owners in ns_owners.items():
        if len(owners) > 1:
            blocks.append(f"rule4-unowned-state: state_namespace '{nsname}' has multiple owners {sorted(owners)} (must be exactly one)")

    # Rule 5 - analogy labelling: borrowed-register vocab in obligations needs an analogy_labels entry.
    labelled = {str(a.get("claim", "")).lower() for a in (doc.get("analogy_labels", []) or [])}
    obligation_text: list[tuple[str, str]] = []
    for b in boundaries:
        obligation_text.append((f"boundary:{b.get('boundary_id')}", str(b.get("contract", ""))))
    for g in gates:
        obligation_text.append((f"gate:{g.get('gate_id')}", str(g.get("condition", ""))))
    for r in (doc.get("residue", []) or []):
        obligation_text.append(("residue", str(r.get("summary", ""))))
    for where, text in obligation_text:
        if ANALOGY_TERMS.search(text) and not any(text.lower() in c or c in text.lower() for c in labelled):
            flags.append(f"rule5-analogy: {where} uses borrowed-register vocabulary without an analogy_labels entry: '{text[:60]}'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an infra-spec candidate document.")
    parser.add_argument("doc", type=Path, help="Path to infra-spec instance JSON")
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    args = parser.parse_args()

    try:
        schema = load_json(args.schema)
        doc = load_json(args.doc)
    except (OSError, json.JSONDecodeError) as exc:
        print("VALIDATION=blocked")
        print(f"BLOCKED: cannot load inputs: {exc}", file=sys.stderr)
        return 2

    blocks: list[str] = []
    flags: list[str] = []

    # shape layer
    shape_errors = sorted(Draft202012Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    for e in shape_errors:
        loc = "/".join(str(p) for p in e.path) or "<root>"
        blocks.append(f"shape: {loc}: {e.message}")

    # governance layer (only meaningful if shape is broadly intact; still run for coverage)
    governance_checks(doc, blocks, flags)

    verdict = "block" if blocks else ("flag" if flags else "pass")
    print(f"VALIDATION={verdict}")
    print(f"DOC={args.doc}")
    for b in blocks:
        print(f"BLOCK: {b}")
    for f in flags:
        print(f"FLAG: {f}")
    return 1 if blocks else 0


if __name__ == "__main__":
    raise SystemExit(main())
