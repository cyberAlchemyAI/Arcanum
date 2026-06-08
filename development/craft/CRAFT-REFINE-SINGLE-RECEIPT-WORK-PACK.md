# WORK-PACK: Craft Refine Single Receipt

## Purpose

Continue the current Craft Refine validation route while treating `refine` as
one receipt-bearing capability instead of requiring a separate receipt for each
internal Refine stage.

## Decision Source

| Field | Value |
| --- | --- |
| decision gate | `docs/decisions/craft-distill-receipt-route.md` |
| selected route | single Refine receipt |
| operator decision | continue this, but treat refine as just 1 receipt |
| status | ready |

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | medium |
| outputMode | single |
| lastUpdatedAt | 2026-06-07 |
| readinessProfile | local-skill-refine-aggregate-receipt |

## Current State

The historical stage-receipt model advanced the run to:

```text
Interrogation refine-review: pass, evidence_kind=receipt
Distill: block, missing owner-stage pass evidence
```

The selected decision changes the active continuation route:

```text
Refine: one aggregate receipt
Distill: internal Refine evidence, not a standalone receipt gate
```

Existing stage-level receipts remain valid historical evidence:

```text
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/01-context-builder.json
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/02-invoke-define.json
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/03-interrogation-refine-review.json
```

## Task Status Board

| Task ID | Goal | Layer | Complexity | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRAFT-REFINE-SINGLE-RECEIPT-001 | Define and produce or block one aggregate Refine receipt for the current run. | L0 | medium | decision gate, current run evidence | pass | completed |

## Task: CRAFT-REFINE-SINGLE-RECEIPT-001

### Objective

Create one Refine-level receipt for the current Craft Refine run, using the
existing stage evidence as inputs without requiring each remaining internal
stage to produce its own receipt.

### Source Contracts

- `docs/decisions/craft-distill-receipt-route.md`
- `development/craft/CRAFT-MISSING-WORK-LIVE-TEST.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RESULT.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RUN-MANIFEST.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-DISPATCH.json`

### Write Scope

- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-RECEIPT.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RESULT.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/RUN-MANIFEST.md`
- `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/evidence-index.json`
- `development/craft/README.md`
- `development/craft/SESSION-LEDGER.md`
- task-session evidence under `development/craft/task-sessions/`

### Aggregate Receipt Shape

The Refine receipt should include:

- `receipt_id`
- `run_id`
- `capability`: `refine`
- `status`: `pass`, `block`, `flag`, `interrupted`, or `timeout`
- `evidence_kind`: `receipt`
- `target_artifact`
- `dispatch_path`
- `historical_stage_receipts`
- `internal_stage_summary`
- `artifact_paths`
- `validation`
- `blockers`
- `created_at`
- `worker`

### Implementation

1. Read the current run result, manifest, evidence index, and dispatch.
2. Summarize internal Refine stages as internal evidence, not independent active receipt gates.
3. Create `REFINE-RECEIPT.md` as the human-readable owner artifact.
4. Write `receipts/refine-run.json`.
5. Sync run/package state so the active blocker is the Refine aggregate receipt result, not a missing Distill stage receipt.
6. Preserve promotion deferral and command-surface historical-only boundary.

### Done Criteria

- `receipts/refine-run.json` parses with `jq`.
- The receipt cites existing stage receipts as historical inputs.
- The receipt honestly reports `pass`, `block`, or `flag` at the Refine level.
- Evidence sync no longer names a standalone Distill receipt as the active next route.
- README and SESSION-LEDGER name the single-Refine-receipt route.
- Promotion remains deferred.

### Validation

```text
jq empty development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json
rg -n "single Refine receipt|aggregate Refine receipt|Distill.*internal|promotion.*defer|Current Next Move" development/craft/README.md development/craft/SESSION-LEDGER.md development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof
```

### Completion Evidence

Status: `completed`

Produced:

```text
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-RECEIPT.md
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json
development/craft/task-sessions/20260607T175719Z-CRAFT-REFINE-SINGLE-RECEIPT-001-CONTEXT.md
development/craft/task-sessions/20260607T175719Z-CRAFT-REFINE-SINGLE-RECEIPT-001-RESULT.md
```

Observed aggregate state:

```text
Refine aggregate receipt: block, evidence_kind=receipt
Distill: internal Refine evidence, not a standalone receipt gate
```

## Recommended Next Execution

This work-pack task is complete. Continue internal Refine work under the
aggregate receipt model.

```text
next route: continue the current Refine run and update the aggregate Refine receipt
```
