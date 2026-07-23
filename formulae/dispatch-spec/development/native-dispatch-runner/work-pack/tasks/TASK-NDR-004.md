# TASK-NDR-004 — Failure and Evidence Hardening

Owner: Task Session

Objective: make native execution fail closed and make its causal event chain mechanically checkable.

## SWU-NDR-008 — Withhold dependents on invalid required receipts

- Behavior: reject a required receipt that is missing, malformed, identity-mismatched, timed out, or non-pass and emit a blocking gate with zero dependent actions.
- Split analysis: all listed cases are variants of one receipt-admission behavior; partial spawn reconciliation and event-order proof remain separate.
- Dependencies: `SWU-NDR-005` pass receipt.
- Source anchors: `native-dispatch-runner.contract.json` invariants/receipt requirements; `ARCHITECTURE.json` failure rule.
- Related context: `work-pack/shared/traceability.md` NDR-R5/R6.
- Write scope: `runtime/orchestrate/scripts/`, `runtime/orchestrate/schemas/`, `runtime/orchestrate/tests/receipt-admission/`.
- Done criteria: every invalid class produces `gate_block`; the next action set is empty; the receipt rejection names the exact violated binding.
- Acceptance evidence: receipt-admission matrix, gate decisions, zero-dependent-action assertions.
- Validation: deterministic parameterized fixture suite.
- Handoff: pass unlocks `SWU-NDR-009` and is required by failure canary.

## SWU-NDR-009 — Reconcile a partially spawned wave

- Behavior: after one spawn succeeds and a sibling spawn fails, stop new actions, wait/interrupt every known agent, persist residue, and close the run blocked.
- Split analysis: partial-wave recovery changes host state and is separately acceptable from receipt admission.
- Dependencies: `SWU-NDR-008` pass receipt.
- Source anchors: `EXECUTION-PACK.md` recovery; `DESIGN.md` risks and controls.
- Related context: `work-pack/shared/cross-task-gaps.md`.
- Write scope: `runtime/orchestrate/SKILL.md`, `runtime/orchestrate/hosts/codex-native.md`, `runtime/orchestrate/tests/partial-wave/`.
- Done criteria: no additional role is spawned after the failure; every known agent has a terminal join/interrupt event; result is blocked with residue and no dependent actions.
- Acceptance evidence: ordered host-call trace, terminal agent states, residue receipt, blocked result.
- Validation: native or host-stub partial-wave fixture with exact call counts.
- Handoff: pass unlocks `SWU-NDR-010`.

## SWU-NDR-010 — Validate causal event ordering

- Behavior: validate that action-attempt, host-result, join, gate, and dependent-action events occur in legal order and reject post-hoc or missing evidence.
- Split analysis: this verifies evidence integrity without changing dispatch decisions.
- Dependencies: `SWU-NDR-009` pass receipt.
- Source anchors: `DESIGN.md` data/evidence view; `native-dispatch-runner.contract.json` live evidence invariant.
- Related context: `work-pack/shared/traceability.md` NDR-R7.
- Write scope: `runtime/orchestrate/scripts/validate_run_evidence.py`, `runtime/orchestrate/schemas/`, `runtime/orchestrate/tests/evidence-order/`.
- Done criteria: valid ordered streams pass; dependent spawn before gate, missing attempt, duplicated host result, and synthesized terminal-only streams fail.
- Acceptance evidence: evidence validator receipt and fixture matrix.
- Validation: deterministic evidence-order fixture suite.
- Handoff: pass establishes the L2 gate for `TASK-NDR-005`.

## SWU-NDR-010R — Reconcile the complete native join lifecycle vocabulary

- Behavior: admit and causally validate `agent_wait_registered`, `wait_attempted`, `agent_closed`, `wait_timed_out`, and `agent_interrupted` as the complete lifecycle extension required by the native join contract.
- Split analysis: terminal-close and timeout-interrupt are two branches of one lifecycle state machine. Splitting them would leave the declared Orchestrate contract partially unverifiable and force another canary loop.
- Dependencies: `SWU-NDR-010` pass receipt; blocked SWU-NDR-011 attempt 1 is source evidence, not a dependency edge.
- Source anchors: `runtime/orchestrate/SKILL.md` native join contract; blocked failure canary result and evidence-validation receipt.
- Related context: `work-pack/shared/traceability.md` NDR-R7/R8; `work-pack/shared/cross-task-gaps.md` lifecycle-event vocabulary blocker.
- Write scope: `runtime/orchestrate/schemas/run-event.schema.json`, `runtime/orchestrate/scripts/validate_run_evidence.py`, `runtime/orchestrate/tests/evidence-order/`, and `work-pack/session-evidence/SWU-NDR-010R/`.
- Ordered rules:
  1. `agent_wait_registered` follows a successful `host_spawn_returned` for the same action and agent and occurs once per known agent.
  2. `wait_attempted` occurs only after every known agent in the wave is registered.
  3. Terminal branch: `agent_terminal` follows a wait observation; `agent_closed` follows terminal and occurs once.
  4. Timeout branch: `wait_timed_out` follows a wait attempt; `agent_interrupted` follows timeout and occurs at most once.
  5. `receipt_joined` follows a valid terminal-close or timeout-interrupt branch.
  6. `gate_decided` follows every required joined receipt.
- Failure cases: registration before host return, wait before full registration, terminal without wait, close before terminal, duplicate close, interrupt without timeout, duplicate interrupt, joined receipt before terminal cleanup, and gate before required join.
- Done criteria: terminal-close and timeout-interrupt fixtures pass; every illegal ordering fails with an exact code; all earlier event-order and runtime tests pass; the preserved blocked canary stream validates through the repaired validator without editing that stream.
- Acceptance evidence: expanded fixture matrix, validation receipt for the preserved eight-event stream, complete regression count, and public-boundary scan.
- Validation: deterministic evidence-order suite plus read-only validation of the preserved failure stream.
- Handoff: pass unlocks a retry of `SWU-NDR-011`; it does not unlock `SWU-NDR-012` directly.
