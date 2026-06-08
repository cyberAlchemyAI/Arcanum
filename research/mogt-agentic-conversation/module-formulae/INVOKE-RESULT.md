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

- `SWU-MOGT-HARNESS-002` still needs concrete scenario and policy-regime fixture formats that instantiate `RuntimeDecisionReceipt`.
- `SWU-MOGT-HARNESS-003` still needs objective-vector and Pareto/frontier calculator implementation.
- Live experiment approval remains blocked until dry-run fixture validation matures.

## Next Route

`task-session` or native Codex Goal for `SWU-MOGT-HARNESS-002`.
