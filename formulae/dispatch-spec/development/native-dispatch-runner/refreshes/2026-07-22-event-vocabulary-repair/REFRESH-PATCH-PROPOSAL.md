# Refresh Patch Proposal — Native Lifecycle Event Vocabulary Repair

Mutation mode: proposal-only

No target artifact is modified by this proposal. Apply requires explicit approval.

## 1. Add one repair SWU to TASK-NDR-004

Append `SWU-NDR-010R — Reconcile the complete native join lifecycle vocabulary` after SWU-NDR-010.

- Behavior: admit and causally validate all five join-lifecycle kinds missing from the current event model: `agent_wait_registered`, `wait_attempted`, `agent_closed`, `wait_timed_out`, and `agent_interrupted`.
- Split analysis: terminal-close and timeout-interrupt are two branches of one lifecycle state machine. Splitting them would leave the declared Orchestrate contract partially unverifiable and force another canary loop.
- Dependencies: SWU-NDR-010 pass receipt plus the blocked SWU-NDR-011 evidence.
- Write scope: `runtime/orchestrate/schemas/run-event.schema.json`, `runtime/orchestrate/scripts/validate_run_evidence.py`, `runtime/orchestrate/tests/evidence-order/`, and SWU-NDR-010R Task Session evidence.
- Ordered rules:
  1. `agent_wait_registered` requires an earlier successful `host_spawn_returned` for the same action/agent and occurs once per known agent.
  2. `wait_attempted` occurs only after every known agent in the wave is registered.
  3. Terminal branch: `agent_terminal` follows a wait observation; `agent_closed` follows terminal and occurs once.
  4. Timeout branch: `wait_timed_out` follows a wait attempt; `agent_interrupted` follows timeout and occurs at most once.
  5. `receipt_joined` follows a valid terminal-close or timeout-interrupt branch.
  6. `gate_decided` follows every required joined receipt.
- Failure cases: registration before host return, wait before full registration, terminal without wait, close before terminal, duplicate close, interrupt without timeout, duplicate interrupt, joined receipt before terminal cleanup, and gate before required join.
- Done criteria: both branch fixtures pass; every illegal ordering fails with an exact code; all earlier event-order and runtime tests pass; the preserved blocked canary stream validates when read through the repaired validator without editing that stream.
- Acceptance evidence: expanded fixture matrix, validation receipt for the preserved eight-event stream, regression count, and public-boundary scan.
- Handoff: pass unlocks a retry of SWU-NDR-011; it does not unlock SWU-NDR-012 directly.

## 2. Make SWU-NDR-011 retry semantics append-only

Update TASK-NDR-005 SWU-NDR-011:

- Add SWU-NDR-010R to dependencies.
- Record the root `failure/` evidence as blocked attempt 1 and preserve it byte-for-byte.
- Set the next attempt write scope to `formulae/dispatch-spec/development/runtime-integration/native-dispatch-runner-canary/failure/retry-001/` only.
- Require the isolated runtime to regenerate from the repaired canonical source.
- Preserve existing done criteria and add: full terminal lifecycle events validate; retry evidence links the blocked attempt instead of replacing it.
- Keep the handoff rule: only a pass retry unlocks SWU-NDR-012.

SWU-NDR-012 remains unchanged except for an explicit dependency note that a blocked or absent SWU-NDR-011 retry receipt forbids execution.

## 3. Refresh the SWU manifest

Insert after SWU-NDR-010:

```json
{
  "id": "SWU-NDR-010R",
  "task": "TASK-NDR-004",
  "wave": "W2",
  "depends_on": ["SWU-NDR-010"],
  "behavior": "validate the complete native join lifecycle event vocabulary"
}
```

Refresh SWU-NDR-011 to preserve current truth:

```json
{
  "id": "SWU-NDR-011",
  "task": "TASK-NDR-005",
  "wave": "W3",
  "depends_on": ["SWU-NDR-007", "SWU-NDR-008", "SWU-NDR-010", "SWU-NDR-010R"],
  "behavior": "run failure-withholding canary",
  "status": "block",
  "receipt": "formulae/dispatch-spec/development/runtime-integration/native-dispatch-runner-canary/failure/receipt.json",
  "validation_result": "block",
  "retry_scope": "formulae/dispatch-spec/development/runtime-integration/native-dispatch-runner-canary/failure/retry-001/"
}
```

Task Session may select SWU-NDR-010R next. It may select SWU-NDR-011 again only after SWU-NDR-010R returns PASS; the retry replaces the manifest's current status/receipt but never rewrites attempt 1.

## 4. Refresh traceability and the gap ledger

Update `work-pack/shared/traceability.md`:

- NDR-R7 live action evidence: `004, 010, 010R, 011`.
- NDR-R8 validated closeout: `010R, 011, 012, VERIFY`.

Add this blocking gap to `work-pack/shared/cross-task-gaps.md`:

| Gap | State | Owner/route | Blocking this pack |
| --- | --- | --- | --- |
| Canonical run evidence omits five declared native join lifecycle kinds. | active blocker proven by SWU-NDR-011 attempt 1 | SWU-NDR-010R, then SWU-NDR-011 retry | yes for W3 and closeout |

Keep the historical-manual-canary truthfulness gap open for SWU-NDR-013.

## 5. Refresh W2, W3, WORK-PACK, and execution dispatch

- W2 adds SWU-NDR-010R; its exit gate becomes contract-complete lifecycle evidence validation.
- W3 entry requires SWU-NDR-010R PASS and an append-only SWU-NDR-011 retry.
- WORK-PACK task table changes TASK-NDR-004 coverage from `008–010` to `008–010R` and names the repair in W2.
- `execution.dispatch.json` S4 consumes the blocked canary receipt as repair evidence and emits an L2 receipt covering SWU-NDR-010R.
- G3 requires receipt admission, partial recovery, original event-order cases, and complete terminal/timeout lifecycle cases.
- S5/G4 remain blocked until SWU-NDR-011 retry passes.

## 6. Apply validation

After approval and patching:

1. Parse `swu-manifest.json` and verify every dependency refers to a known SWU.
2. Run the canonical Dispatch Spec validator on `execution.dispatch.json`.
3. Confirm TASK-NDR-004, TASK-NDR-005, manifest, W2/W3, traceability, gaps, WORK-PACK, and execution dispatch all name the same repair/retry order.
4. Confirm no target file claims SWU-NDR-011 or SWU-NDR-012 PASS.
5. Confirm the blocked canary files retain their pre-apply hashes.
6. Run public-boundary and trailing-whitespace scans.

## Handoff after apply

Next owner: Task Session

First executable unit: `TASK-NDR-004 / SWU-NDR-010R`

Then: retry `TASK-NDR-005 / SWU-NDR-011` under `failure/retry-001/`.

Only after that retry passes: execute SWU-NDR-012.
