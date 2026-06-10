---
name: Invoke Result - MOGT Module Formulae Model
description: Invoke-authored Module Formulae model for MOGT rule, workflow, and operation contracts.
created: 2026-06-07
mode: define-design
status: pass
---

# Invoke Result

## Summary

Mode: define/design hybrid.

Template family: Module Formulae.

Selected templates:

- `module-spec.md`
- `concept-model.md`
- `operations.md`
- `flows-policies.md`

Target artifact: MOGT research evidence model under
`research/mogt-agentic-conversation/module-formulae/`.

## Outputs

- `module-spec.md`
- `concept-model.md`
- `operations.md`
- `flows-policies.md`
- `formal-runtime-definition.md`
- `runtime-decision-receipt.md`
- `objective-estimator-contract.md`
- `../experiments/schema/mogt-runtime-decision-receipt.schema.json`

## Template Selection Evidence

The user requested Module Formulae modeling using rule, workflow, and operation.
The Module Formulae template pack maps these to:

- rule and policy contracts: `flows-policies.md`;
- workflow contracts: `flows-policies.md`;
- operation/action contracts: `operations.md`;
- structural concepts: `concept-model.md`;
- navigation and ownership: `module-spec.md`.

## Source Evidence

- `../definitions/DEFINITIONS.md`
- `../claims/CLAIMS.md`
- `../experiments/E1-tradeoff-traceability-baseline/protocol.md`
- `../experiments/E2-pareto-arbitration-quality/protocol.md`
- `../experiments/schema/mogt-run.schema.json`
- `../tools/validate-mogt-run-jsonl.py`
- `../development/TASK-MOGT-HARNESS-001-RESULT.md`
- `formal-runtime-definition.md`

## Decisions

1. Model MOGT as a research evidence module, not as canonical Arcanum ontology.
2. Treat fixture validation as schema readiness only.
3. Keep policy-regime comparison as a workflow for later SWUs, not live execution.
4. Use `EvidenceStatusBoundaryPolicy` to prevent fixture data from upgrading claims.
5. Add a formal/runtime definition because the project needed an operational
   account of how MOGT actually selects conversation actions.
6. Refresh the model with a concrete runtime receipt contract so the formal
   definition can be instantiated by fixtures and later runtime adapters.

## Unresolved Gaps

Resolved since the 2026-06-08 refresh (reconciled 2026-06-10):

- `SWU-MOGT-HARNESS-002` runtime-receipt fixtures are complete (`TASK-MOGT-HARNESS-002-RESULT.md`, `development/fixtures/mogt-runtime-decision-receipts.jsonl`).
- `SWU-MOGT-HARNESS-003` objective-vector and Pareto/frontier calculator is complete (`TASK-MOGT-HARNESS-003-RESULT.md`, `tools/calculate-pareto-frontier.py`).

Still open:

- `runtime-decision-receipt.md` shape table lists `decision_state` as required while its minimal JSON example omits it; the receipt contract still needs to reconcile table vs example.
- The objective estimator contract is now authored (`objective-estimator-contract.md`) but has no executable estimator implementation.
- The runtime receipt JSON Schema (`../experiments/schema/mogt-runtime-decision-receipt.schema.json`) is not yet wired into `tools/validate-mogt-run-jsonl.py` as a receipt-specific validation pass.
- Live experiment approval remains blocked until dry-run fixture validation matures.

## Next Route

`task-session` for `SWU-MOGT-HARNESS-006` (wire the receipt schema into a receipt-specific validation pass).
