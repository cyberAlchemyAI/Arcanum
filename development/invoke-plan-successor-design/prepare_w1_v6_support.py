#!/usr/bin/env python3
"""Create V6 owner-decision and no-prior records from the approved boundary."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


EPOCH = "2026-08-28-plan-successor-design-boundary-v6-evidence-repair"
TARGET = "invoke:plan-successor:definition-target"
OWNER = "owner:user"


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()


def write_absent(path: Path, document: dict[str, Any], digest_key: str) -> None:
    if path.exists() or path.is_symlink():
        raise ValueError(f"output must be absent: {path}")
    document[digest_key] = digest(document)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--approval", required=True, type=Path)
    parser.add_argument("--decision-output", required=True, type=Path)
    parser.add_argument("--no-prior-output", required=True, type=Path)
    args = parser.parse_args()

    approval = json.loads(args.approval.read_text(encoding="utf-8"))
    if (
        approval.get("target_id") != TARGET
        or approval.get("approved_by") != OWNER
        or approval.get("observation_epoch") != EPOCH
        or approval.get("authority_effect") != "none"
    ):
        raise ValueError("approval does not bind the exact V6 target, owner, and epoch")

    decision = {
        "schema_version": "invoke.plan-successor-design-owner-decision.v1",
        "decision_id": "decision:plan-successor-design-boundary-v6-evidence-repair",
        "target_id": TARGET,
        "owner": OWNER,
        "observation_epoch": EPOCH,
        "decisions": {
            "plan_source_authority": "One canonical JSON Plan authoring source owns the meaning-bearing Plan content.",
            "work_pack_role": "WORK-PACK.md is a deterministic coordinator view generated from the canonical JSON Plan source.",
            "work_pack_reader_contract": "The generated WORK-PACK.md is a changed human navigation surface for plan coordinators and requires an explicit UX contract and validation witness.",
            "legacy_plan_material": "Existing Plan prose that calls WORK-PACK.md the source of truth is migration evidence eligible for supersession, not successor authority.",
            "distill_contract": "Design evidence is pinned to the four public Distill v1 schemas under arcanum/spells/invoke/schemas; concurrent Distill v2 material is outside this boundary.",
            "design_kind": "No admitted Design predecessor exists for this exact target, so W1 proceeds as greenfield Design.",
            "evidence_filter": "Generated Python bytecode, __pycache__ contents, and the derived latest-run summary are not architecture evidence and are absent from the selected snapshot.",
            "observability_gap": "Signal Observer README and skill prose state a conditional integration requirement but do not prove a machine schema, projector, validator, fixture, or admission closure.",
            "native_context_version": "Select native-context 1.2.0 when no transient outputs are declared and 1.3.0 when the declared transient-output set is nonempty.",
            "evidence_closure": "Every selected file is frozen with its original path, digest, discovery rule, and input class; every catalog entry must participate in a typed Design obligation.",
            "snapshot_boundary": "The approved boundary consumes the independently verified selected-file snapshot and current Define refresh, so unrelated live repository writes cannot change its material digest.",
        },
        "claim_ceiling": "This decision records W1 input meaning, evidence classification, and conflict ownership only. It does not admit a Design, close the Signal Observer machine gap, accept a Plan, authorize implementation, or mutate product code.",
        "authority_effect": "none",
    }
    no_prior = {
        "schema_version": "invoke.design-no-prior-determination.v1",
        "target_id": TARGET,
        "observation_epoch": EPOCH,
        "applicable_prior_design_paths": [],
        "determined_by": OWNER,
        "authority_effect": "none",
    }
    write_absent(args.decision_output, decision, "decision_digest")
    write_absent(args.no_prior_output, no_prior, "determination_digest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
