# Context Pack — SWU-NDR-010R

Evidence class: Task Session context; not canonical source

- Task: `TASK-NDR-004 / SWU-NDR-010R`
- Mode: standard, strict
- Built: `2026-07-22T23:34:10Z`
- Selected files: 14
- Obligation coverage: 12/12 (100%)
- Runtime handoff: none; execution is local and deterministic
- Write scope: `runtime/orchestrate/schemas/run-event.schema.json`, `runtime/orchestrate/scripts/validate_run_evidence.py`, `runtime/orchestrate/tests/evidence-order/`, and this session-evidence directory

## Controlling constraints

1. Preserve the SWU-NDR-010 PASS receipt and the blocked SWU-NDR-011 attempt unchanged.
2. Add all five lifecycle kinds declared by the canonical Orchestrate native join contract.
3. Validate registration, wait, terminal-close, timeout-interrupt, receipt join, and gate order without inferring absent events.
4. Cover both valid branches and every illegal ordering named by SWU-NDR-010R with stable error codes.
5. Keep all earlier evidence-order and runtime tests passing.
6. Validate the preserved eight-event failure stream read-only after the repair.
7. Do not unlock SWU-NDR-012; a passing SWU-NDR-010R unlocks only the append-only SWU-NDR-011 retry.

## Obligation matrix

| ID | Obligation | Evidence selector | Status |
| --- | --- | --- | --- |
| O1 | Dependency SWU-NDR-010 is PASS | `work-pack/swu-manifest.json` and `session-evidence/SWU-NDR-010/receipt.json` | covered |
| O2 | Schema admits five lifecycle kinds with correct identities | `runtime/orchestrate/SKILL.md#native_join_contract`; `run-event.schema.json` | covered |
| O3 | Registration follows matching successful host return and is unique | `TASK-NDR-004.md#SWU-NDR-010R`, ordered rule 1 | covered |
| O4 | Wait follows full registration for the known wave | ordered rule 2 | covered |
| O5 | Terminal follows wait and close follows terminal exactly once | ordered rule 3 | covered |
| O6 | Timeout follows wait and interrupt follows timeout at most once | ordered rule 4 | covered |
| O7 | Receipt join follows terminal-close or timeout-interrupt | ordered rule 5 | covered |
| O8 | Gate follows every required joined receipt | ordered rule 6 and existing SWU-NDR-010 validator | covered |
| O9 | Nine illegal orderings fail with exact codes | `TASK-NDR-004.md`, failure cases | covered |
| O10 | Both valid branches and all earlier cases pass | done criteria and existing evidence-order matrix | covered |
| O11 | Preserved failure stream validates without mutation | failure `run/events.jsonl` plus its blocked validator receipt | covered |
| O12 | Emit receipts, regression count, hashes, and public-boundary result | acceptance evidence and work-pack rule 6 | covered |

## Selected evidence

- `WORK-PACK.md` — status, authority, W2/W3 gates, and first handoff — O1, O7, O12.
- `work-pack/tasks/TASK-NDR-004.md` — complete SWU contract, write scope, rules, failures, done criteria — O2–O12.
- `work-pack/swu-manifest.json` — dependency and current status truth — O1, O12.
- `work-pack/waves/W2.md` — both branch exit condition — O5, O6, O10.
- `work-pack/shared/cross-task-gaps.md` — active vocabulary blocker and retry route — O11, O12.
- `work-pack/shared/traceability.md` — NDR-R7/R8 ownership — O2, O7, O8.
- `runtime/orchestrate/SKILL.md` — canonical five-event native join contract — O2–O7.
- `runtime/orchestrate/schemas/run-event.schema.json` — current six-event schema gap — O2.
- `runtime/orchestrate/scripts/validate_run_evidence.py` — current causal state and exact-code surface — O3–O10.
- `runtime/orchestrate/tests/evidence-order/test_evidence_order.py` — deterministic schema/receipt/CLI checks — O9, O10.
- `runtime/orchestrate/tests/evidence-order/fixture-matrix.json` — existing regression matrix — O9, O10.
- failure `run/events.jsonl` — preserved real terminal-close branch — O3–O5, O7, O8, O11.
- failure `run/evidence-validation-receipt.json` — exact pre-repair mismatch — O2, O11.
- `session-evidence/SWU-NDR-010/receipt.json` — dependency proof and earlier regression baseline — O1, O10.

## Decisions and assumptions

- Use one per-action lifecycle state keyed by the persisted action identity; agent identity must match the successful host return.
- Treat `wait_attempted` as a wave-level event with null action and agent identities.
- Treat timeout and interrupt as per-action events so cleanup is causally attributable.
- Preserve existing error behavior, adding one stable code per new illegal-order class.
- No blocker-level decision remains: these choices are direct consequences of the checked-in contract.

## Excluded candidates

- Architecture-wide prose: excluded because the task-owned runtime contract is more specific.
- Generated installed runtimes: excluded from mutation; regeneration belongs to the canary retry.
- Other test families: excluded from context selection, but included in regression execution after the bounded repair.

## Gate verdict

PASS to local implementation. Dependency, source contract, write scope, validation path, preservation boundary, and synchronization target are all explicit.
