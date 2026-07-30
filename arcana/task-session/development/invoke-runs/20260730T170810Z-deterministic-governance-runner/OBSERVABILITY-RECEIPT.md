# Observability Receipt

## Distill child

- result: recorded
- ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`
- line: 439
- run ID: `distill-20260730T170810Z-task-session-runner-plan`
- parent: `invoke-20260730T170810Z-deterministic-governance-runner`
- dedupe key:
  `distill-20260730T170810Z-task-session-runner-plan:signal-observer:0.1.0`
- reflection trigger calculated by observer: `output-threshold`
- recommendation: `reflect-now`

## Invoke parent

- result: recorded
- ledger: `.arcanum/observability/signals/sigil-invocations.jsonl`
- line: 440
- run ID: `invoke-20260730T170810Z-deterministic-governance-runner`
- dedupe key:
  `invoke-20260730T170810Z-deterministic-governance-runner:signal-observer:0.1.0`
- reflection trigger: `manual`
- recommendation: `targeted-update`

## Authority

Telemetry is non-authoritative and does not alter the Distill verdict, plan gate,
implementation authorization, or lifecycle owner. Reflection was recommended but
not executed by this Invoke planning request.

Replaying both envelopes returned `OBSERVATION=skipped` with
`REASON=duplicate observer emission`, confirming the idempotency keys.
