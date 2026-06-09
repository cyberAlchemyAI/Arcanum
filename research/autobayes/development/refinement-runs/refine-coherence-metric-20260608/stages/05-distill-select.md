---
stage: 5
name: Distill (select coherent unit and signal set)
capability: distill
mode: standard
status: pass
dispatch_id: refine-coherence-metric-20260608
---

# Distill — selected unit and signal set (grounded in real telemetry)

## Real distribution (n=398, arcanum/.arcanum/observability/signals/sigil-invocations.jsonl)

- `execution.status`: completed 327, failed 24, pass 26, partial 8, blocked 5, + enum drift
  (`pass`/`flag`/`block`/`completed_with_block`/None) — **the status enum is itself inconsistent**
  (a data-quality residue worth flagging to observability owners).
- `quality_bar_status`: pass 360, partial 33, not_checked 2 — **heavily ceiling-skewed**.
- Records with `workflow_gaps`: 22/398; `output_contract_drift` true: 1/398.
- `files_changed` length: 0 → 317, 1–3 → 33, 4–10 → 31, 11+ → 17.
- Top sigils: invoke 98, task-session 85, context-builder 55, interview-kits 50, refine 35.

## Selected unit

> **One sigil invocation in an execution-bearing mode** (mode ∈ new/update/execute, or
> `files_changed` non-empty), with residue read from the objective signals first.

## Repairs folded in (from refine-review)

- **Anti-gaming:** rank objective signals (`execution.status`, `output_contract_drift`,
  downstream reopen of same `target_artifact`) above self-reported `workflow_gaps`; flag
  zero-variance "suspiciously clean" sigils separately.
- **Difficulty:** normalize per obligation; read DCI as a per-sigil trend, not a cross-sigil
  ranking.
- **Ceiling effect (new, from data):** because ~90% are clean, DCI is near-100 for most
  units — it behaves as an **anomaly/residue detector**, not a smooth gauge. The backtest must
  measure discrimination on the *execution-bearing* subset, not the whole store.
- **Status enum drift:** normalize statuses into {ok, partial, fail/blocked} before scoring.

## Unit-size proxy

`len(files_changed)` — but **only meaningful on the ~81 non-zero-file records**; observe-mode
zero-file invocations are excluded from the DCI-vs-size curve.

## Rejected alternatives

- Whole-store scoring — rejected: dominated by zero-file observe invocations, no signal.
- Self-reported `quality_bar_status` as sole input — rejected: gameable + ceiling-skewed.
- Absolute cross-sigil DCI ranking — rejected: conflates difficulty with coherence.

## Recomposition path

unit + signal set → metric tournament (3 candidate DCIs) → pareto → backtest on the
execution-bearing subset → workflow-reflect lens + the Craft redefinition that DCI grounds.
