# Pre-Execution Owner Prerequisite Fast Path

Status: Invoke-authored development package; implementation not started.

This package repairs the plan-to-execution handoff that can make Task Session spend substantial effort proving a prerequisite already declared by the selected work pack. The target behavior is simple:

1. prefer the existing `selected-unit-at-task-session` plan-once route, which needs no expected pre-execution Invoke Refresh;
2. when a legacy or drifted plan genuinely requires an owner prerequisite, classify it before Context Builder;
3. either join one exactly authorized owner hop or return the exact missing route immediately;
4. enter normal Task Session context, admission, mutation, and validation only after the prerequisite is satisfied.

The package is public and product-neutral. The originating consuming-project incident is represented only as a generic workflow signal; no private project prose or ontology material is copied here.

## Start here

- Definition: [`SPEC.md`](SPEC.md)
- Design: [`architecture-bundle.md`](architecture-bundle.md)
- Plan: [`IMPLEMENTATION-PLAN.md`](IMPLEMENTATION-PLAN.md)
- Executable decomposition: [`WORK-PACK.md`](WORK-PACK.md)
- Lifecycle route: [`execution.dispatch.json`](execution.dispatch.json)
- Open decisions and blindspots: [`RESIDUE.md`](RESIDUE.md)
- Observability receipt: [`OBSERVABILITY-RESULT.md`](OBSERVABILITY-RESULT.md)

## Claim ceiling

The package proves an authored, validated plan boundary only. It does not prove canonical implementation, generated-package parity, lifecycle promotion, publication, release, or a live consuming-project repair.
