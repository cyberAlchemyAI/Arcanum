# Context Pack — SWU-NDR-010

Task: `TASK-NDR-004 / SWU-NDR-010`

## Objective

Make persisted native-run evidence mechanically prove its own causal order. A valid stream must connect an action attempt to exactly one host result, a joined receipt, a gate decision, and only then any gate-dependent action.

## Covered obligations

1. Validate one strict, contiguous event sequence.
2. Bind every host result to an earlier action attempt.
3. Admit at most one host result per action.
4. Bind joined receipts to successful host results.
5. Require every gate input to have an attempt, host result, and joined receipt.
6. Require `gate_pass` before a dependent action attempt.
7. Reject terminal-only evidence that reconstructs no causal action chain.
8. Return a deterministic machine receipt with exact violations.
9. Preserve the public boundary and record generated-package drift introduced by canonical runtime files.

## Selected evidence

- `work-pack/tasks/TASK-NDR-004.md` — exact behavior, cases, scope, and done criteria.
- `work-pack/session-evidence/SWU-NDR-009/receipt.json` — dependency PASS.
- `DESIGN.md` — live evidence rule and data/evidence view.
- `native-dispatch-runner.contract.json` — attempted-not-reconstructed invariant.
- `work-pack/shared/traceability.md` — NDR-R7 mapping.
- `runtime/orchestrate/tests/partial-wave/fixtures/expected-unresolved-trace.json` — current spawn/failure ordering vocabulary.
- `runtime/orchestrate/tests/native-join/fixtures/expected-all-pass-events.json` — current join ordering vocabulary.
- `runtime/orchestrate/generation-manifest.json` — canonical scripts and schemas are generated support.

## Decisions

- Use one shared run-event schema and one validator-receipt schema.
- Express join evidence as `receipt_joined`, distinct from the optional host lifecycle event `agent_terminal`.
- Put `required_action_ids` on `gate_decided` so a stream proves which completed actions authorized the gate.
- Put `depends_on_gate_id` on dependent `action_attempted` events so premature execution is locally checkable.
- Treat new canonical scripts/schemas as deliberate generation drift until the installed packages are mechanically refreshed before native canaries.

## Write boundary

- `runtime/orchestrate/scripts/validate_run_evidence.py`
- `runtime/orchestrate/schemas/`
- `runtime/orchestrate/tests/evidence-order/`
- `work-pack/session-evidence/SWU-NDR-010/`
- `work-pack/swu-manifest.json`

No subagent or host-native mutation is required for this deterministic SWU.
