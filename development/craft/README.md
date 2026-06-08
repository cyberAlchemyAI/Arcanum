# Craft Development Package

This package is the active development space for `Craft`, a candidate Arcanum/CyberAlchemy method primitive for turning intention into stable artifacts through schema/data translation, residue handling, SCU/SWU selection, validation, reflection, and recomposition.

Craft is not canonical authority yet. This package is checkpoint-first: it preserves evidence, session state, candidate decisions, and future work boundaries before any registry, runtime, sigil, spell, or framework promotion.

## Start Here

1. [DURABLE-SESSION-CONTEXT.md](DURABLE-SESSION-CONTEXT.md)
2. [SESSION-LEDGER.md](SESSION-LEDGER.md)
3. [CRAFT-INITIAL-DEFINITION.md](CRAFT-INITIAL-DEFINITION.md)

## Current Verdict

`refine-validation-aggregate-refine-receipt-block-promotion-deferred`

The recursive-ledger MVP is validated, the pre-architecture gap-closure wave is complete, and the broader Craft method architecture has passed design and plan hardening. Craft now has a candidate validation example suite, validation/recomposition guide, promotion readiness review, and historical runtime command-surface smoke for the previously missing `dispatch-spec` and `runtime-handoff` routes. Refine evidence classification has been repaired, Context Builder, Invoke Define, and Interrogation refine-review now have receipt-backed pass evidence. The single aggregate Refine receipt now exists and reports `block`: `Distill` remains important internal Refine evidence, but it is no longer the active standalone receipt gate. Promotion is deferred until repeated local use and receipt-backed validation produce stronger evidence.

Current operational MVP focus:

```text
Craft recursive ledger: a YAML-backed local ledger for nested development
contexts, their artifacts, lifecycle states, blockers, enablers, and
cross-context relations.
Blockers, gates, and enablers now have candidate condition types and
operational lanes such as tech, business, QA, validator, and auditor,
so the ledger can later map type + lane -> role for delegation.
```

Current MVP artifacts:

```text
Schema authority: CRAFT-LEDGER-SCHEMA.yml
Ledger fixture:   LEDGER.md
Validation:       LEDGER-VALIDATION.md
Result:           pass
```

Gap-closure artifacts:

```text
Glossary:           CRAFT-GLOSSARY.md
Architecture inputs: CRAFT-ARCHITECTURE-INPUTS.md
Wave work-pack:      CRAFT-GAP-CLOSURE-WORK-PACK.md
Result:              pass
```

Architecture-hardening artifacts:

```text
Architecture:       CRAFT-ARCHITECTURE.md
Plan work-pack:     CRAFT-ARCHITECTURE-WORK-PACK.md
Examples:           CRAFT-VALIDATION-EXAMPLES.yml
Validation guide:   CRAFT-VALIDATION.md
Readiness review:   CRAFT-PROMOTION-READINESS.md
Recommendation:     defer promotion
Result:             pass
```

Runtime command-surface artifacts:

```text
dispatch-spec route:    .codex/commands/dispatch-spec.md
runtime-handoff route:  .codex/commands/runtime-handoff.md
Smoke evidence:         development/craft/task-sessions/CRAFT-RUNTIME-003.md
Result:                 pass
```

Latest Refine validation attempt:

```text
Run:    development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof
Result: block
Dispatch validation: pass
Receipt-backed stages: Context Builder, Invoke Define, and Interrogation refine-review are `pass` with `evidence_kind=receipt`.
Historical stage-model reason: Distill is the first remaining `block`; it has not produced owner-stage pass evidence.
Active decision: continue with one aggregate Refine receipt instead of one receipt per internal Refine stage.
Aggregate receipt: receipts/refine-run.json reports `block` because internal Refine work remains incomplete.
```

Invoke Define receipt plan:

```text
Layering:  CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md
Work-pack: CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md
Execution: CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md
Transport: CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-PLAN-TRANSPORT.md
Result:    pass
```

Local skill-surface refresh:

```text
Report:    CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-REFRESH-REPORT.md
JSON:      CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-refresh-report.json
Result:    active route refreshed
Boundary:  historical command-surface evidence retained; current execution uses local skill contracts
```

Refine missing-work strategy:

```text
Strategy:  CRAFT-REFINE-MISSING-STRATEGY.md
Dispatch:  CRAFT-REFINE-MISSING-STRATEGY-DISPATCH.json
Live test: CRAFT-MISSING-WORK-LIVE-TEST.md
Result:    dispatch validation pass; first live test advanced blocker to Distill
Boundary:  full Refine run and subagent fanout require operator approval
```

Single Refine receipt decision:

```text
Decision: docs/decisions/craft-distill-receipt-route.md
Work-pack: CRAFT-REFINE-SINGLE-RECEIPT-WORK-PACK.md
Selected route: treat Refine as one receipt-bearing capability
Receipt: development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json
Result: block; internal Refine work remains incomplete
Boundary: existing stage receipts are historical evidence; current execution uses local skill contracts
```

## Files

| File | Purpose | Status |
| --- | --- | --- |
| [DURABLE-SESSION-CONTEXT.md](DURABLE-SESSION-CONTEXT.md) | Durable scope boundary, source context, operating rules, and resume prompt. | active |
| [SESSION-LEDGER.md](SESSION-LEDGER.md) | Artifact, decision, gap, and candidate task ledger. | active |
| [CRAFT-INITIAL-DEFINITION.md](CRAFT-INITIAL-DEFINITION.md) | Initial Craft definition, research synthesis, vocabulary, lifecycle, residue model, and formal model. | source-baseline |
| [CRAFT-INITIAL-DEFINITION.html](CRAFT-INITIAL-DEFINITION.html) | Rendered companion for the initial definition. | source-baseline |
| [CRAFT-RECURSIVE-LEDGER-DEFINE.md](CRAFT-RECURSIVE-LEDGER-DEFINE.md) | Define baseline for the first operational Craft MVP. | active |
| [CRAFT-RECURSIVE-LEDGER-GLOSSARY.md](CRAFT-RECURSIVE-LEDGER-GLOSSARY.md) | Candidate glossary for recursive ledger terms. | active |
| [CRAFT-LEDGER-TYPE-SYSTEM.md](CRAFT-LEDGER-TYPE-SYSTEM.md) | Candidate condition type and operational lane system for blockers, gates, enablers, and future role mapping. | active |
| [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Minimal L0-L1 layer boundary for the next refinement slice. | active |
| [WORK-PACK.md](WORK-PACK.md) | Minimal work-pack for refining examples and schema. | active |
| [CRAFT-LEDGER-TYPE-EXAMPLES.md](CRAFT-LEDGER-TYPE-EXAMPLES.md) | Refined examples for typed ledger rows. | active |
| [CRAFT-RECURSIVE-LEDGER-DESIGN.md](CRAFT-RECURSIVE-LEDGER-DESIGN.md) | Minimal recursive ledger schema. | active |
| [CRAFT-LEDGER-SCHEMA.yml](CRAFT-LEDGER-SCHEMA.yml) | YAML schema contract for the recursive ledger MVP. | active |
| [CRAFT-MVP-DEFINE.md](CRAFT-MVP-DEFINE.md) | Invoke define artifact for the file-backed recursive-ledger MVP. | active |
| [CRAFT-MVP-DESIGN.md](CRAFT-MVP-DESIGN.md) | Invoke design artifact with six-view MVP design and plan handoff notes. | active |
| [CRAFT-MVP-DESIGN.html](CRAFT-MVP-DESIGN.html) | Visual HTML companion for the Craft MVP architecture. | active |
| [CRAFT-MVP-IMPLEMENTATION-LAYERING.md](CRAFT-MVP-IMPLEMENTATION-LAYERING.md) | L0-L2 layer boundary for the first file-backed recursive-ledger MVP. | active |
| [CRAFT-MVP-WORK-PACK.md](CRAFT-MVP-WORK-PACK.md) | Invoke plan work-pack for creating `LEDGER.md` and validating blocker refinement behavior. | active |
| [LEDGER.md](LEDGER.md) | Validated recursive-ledger MVP fixture. | active |
| [LEDGER-VALIDATION.md](LEDGER-VALIDATION.md) | Manual validation report for schema rules and blocker lifecycle behavior. | pass |
| [CRAFT-GAP-CLOSURE-IMPLEMENTATION-LAYERING.md](CRAFT-GAP-CLOSURE-IMPLEMENTATION-LAYERING.md) | L0-L3 layer boundary for removing pre-architecture blockers and routing remaining gaps. | active |
| [CRAFT-GAP-CLOSURE-WORK-PACK.md](CRAFT-GAP-CLOSURE-WORK-PACK.md) | Invoke plan work-pack for the pre-architecture gap-closure wave. | active |
| [CRAFT-GLOSSARY.md](CRAFT-GLOSSARY.md) | Candidate Craft method glossary that closes the pre-architecture vocabulary blocker. | active |
| [CRAFT-ARCHITECTURE-INPUTS.md](CRAFT-ARCHITECTURE-INPUTS.md) | Architecture-owned input register for route integration, validation examples, promotion path, deferred automation, and runtime side-thread boundaries. | active |
| [CRAFT-ARCHITECTURE.md](CRAFT-ARCHITECTURE.md) | Six-view Craft method architecture, route integration contract, validation example-suite shape, and promotion path. | pass |
| [CRAFT-ARCHITECTURE-GLOSSARY-CONSISTENCY.md](CRAFT-ARCHITECTURE-GLOSSARY-CONSISTENCY.md) | Glossary consistency report for the architecture design pass. | pass |
| [CRAFT-ARCHITECTURE-DESIGN-TRANSPORT.md](CRAFT-ARCHITECTURE-DESIGN-TRANSPORT.md) | Design transport/provenance report for the architecture pass. | active |
| [CRAFT-ARCHITECTURE-IMPLEMENTATION-LAYERING.md](CRAFT-ARCHITECTURE-IMPLEMENTATION-LAYERING.md) | L0-L3 layer boundary for architecture hardening and validation evidence. | active |
| [CRAFT-ARCHITECTURE-WORK-PACK.md](CRAFT-ARCHITECTURE-WORK-PACK.md) | Completed work-pack for validation examples, validation guide, readiness review, and package sync. | pass |
| [CRAFT-ARCHITECTURE-EXECUTION-PACK.md](CRAFT-ARCHITECTURE-EXECUTION-PACK.md) | Wave sequencing for architecture hardening. | active |
| [CRAFT-VALIDATION-EXAMPLES.yml](CRAFT-VALIDATION-EXAMPLES.yml) | Structured candidate example suite for Craft method claims. | pass |
| [CRAFT-VALIDATION-EXAMPLES.md](CRAFT-VALIDATION-EXAMPLES.md) | Human-readable walkthrough of the validation example suite. | pass |
| [CRAFT-VALIDATION.md](CRAFT-VALIDATION.md) | Manual validation and recomposition guide for Craft examples and future task-session runs. | pass |
| [CRAFT-PROMOTION-READINESS.md](CRAFT-PROMOTION-READINESS.md) | Promotion readiness review; recommendation is `defer`. | active |
| [CRAFT-REFINE-RUNTIME-STRATEGY.md](CRAFT-REFINE-RUNTIME-STRATEGY.md) | Candidate strategy for replacing recursive command-backed refine with orchestrator plus stage workers/subagents. | candidate |
| [ARCANUM-SKILL-RUNTIME-HANDOFF.md](ARCANUM-SKILL-RUNTIME-HANDOFF.md) | New-thread handoff for designing an Arcanum skill runtime interface with observation envelope capture. | active |
| [CRAFT-MISSING-ARTIFACTS.md](CRAFT-MISSING-ARTIFACTS.md) | Missing-artifact audit for the Craft runtime command-surface blocker. | pass |
| [CRAFT-RUNTIME-DEFINE.md](CRAFT-RUNTIME-DEFINE.md) | Invoke define artifact for resolving missing `dispatch-spec` and `runtime-handoff` command routes. | active |
| [CRAFT-RUNTIME-GLOSSARY.md](CRAFT-RUNTIME-GLOSSARY.md) | Runtime command-surface vocabulary needed by the Craft validation blocker. | active |
| [CRAFT-RUNTIME-DESIGN.md](CRAFT-RUNTIME-DESIGN.md) | Six-view design for repairing the bare command routes without changing canonical capability authority. | pass |
| [CRAFT-RUNTIME-WORK-PACK.md](CRAFT-RUNTIME-WORK-PACK.md) | Completed work-pack for clearing Craft's runtime command-surface blocker. | pass |
| [CRAFT-RUNTIME-EXECUTION-PACK.md](CRAFT-RUNTIME-EXECUTION-PACK.md) | Wave sequencing for the runtime command-surface work-pack. | active |
| [CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-IMPLEMENTATION-LAYERING.md](CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-IMPLEMENTATION-LAYERING.md) | L0-L3 layer boundary for repairing native Refine stage receipt semantics. | active |
| [CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-WORK-PACK.md](CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-WORK-PACK.md) | Executable work-pack for preventing handoff stubs from being counted as owner-stage pass evidence. | active |
| [CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-EXECUTION-PACK.md](CRAFT-REFINE-RUNTIME-STAGE-RECEIPTS-EXECUTION-PACK.md) | Wave sequencing for the stage receipt repair work. | active |
| [CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-IMPLEMENTATION-LAYERING.md](CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-IMPLEMENTATION-LAYERING.md) | L0-L3 layer boundary for creating parent-native owner-stage receipt evidence. | active |
| [CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md](CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md) | Invoke plan work-pack for the native Refine stage receipt bridge. | active |
| [CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-EXECUTION-PACK.md](CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-EXECUTION-PACK.md) | Wave sequencing for the native stage receipt bridge. | active |
| [CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-PLAN-TRANSPORT.md](CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-PLAN-TRANSPORT.md) | Plan transport/provenance report for the native stage receipt bridge. | active |
| [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-HANDOFF.md) | Continuation handoff for the current `Invoke Define` owner-stage receipt blocker. | active |
| [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-IMPLEMENTATION-LAYERING.md) | L0-L3 layer boundary for the `Invoke Define` receipt plan. | active |
| [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-WORK-PACK.md) | Invoke plan work-pack for producing and ingesting the `Invoke Define` receipt. | pass |
| [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-EXECUTION-PACK.md) | Wave sequencing for the `Invoke Define` receipt plan. | active |
| [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-PLAN-TRANSPORT.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-PLAN-TRANSPORT.md) | Plan transport/provenance report for the `Invoke Define` receipt plan. | active |
| [CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-REFRESH-REPORT.md](CRAFT-INVOKE-DEFINE-STAGE-RECEIPT-REFRESH-REPORT.md) | Invoke refresh report that retires command-surface routing for the active Craft receipt workflow. | active |
| [CRAFT-REFINE-MISSING-STRATEGY.md](CRAFT-REFINE-MISSING-STRATEGY.md) | Dispatch-backed strategy for refining all remaining Craft blockers and gaps before build/live test. | active |
| [CRAFT-REFINE-MISSING-STRATEGY-DISPATCH.json](CRAFT-REFINE-MISSING-STRATEGY-DISPATCH.json) | Validator-backed dispatch route for the Craft missing-work strategy. | pass |
| [CRAFT-REFINE-MISSING-LIVE-TEST.md](CRAFT-REFINE-MISSING-LIVE-TEST.md) | First bounded live test for the strategy dispatch and pre-execution evidence baseline. | pass |
| [CRAFT-REFINE-MISSING-APPROVED-RUN.md](CRAFT-REFINE-MISSING-APPROVED-RUN.md) | Approved subagent strategy run synthesis and first live-test decision. | pass |
| [CRAFT-MISSING-BLOCKERS-AND-GAPS.md](CRAFT-MISSING-BLOCKERS-AND-GAPS.md) | Consolidated blockers, deferred gaps, and boundary risks found by the approved strategy run. | active |
| [CRAFT-MISSING-WORK-DESIGN.md](CRAFT-MISSING-WORK-DESIGN.md) | Missing-work design for converting the first remaining blocker into a receipt task. | pass |
| [CRAFT-MISSING-WORK-DESIGN-REVIEW.md](CRAFT-MISSING-WORK-DESIGN-REVIEW.md) | Review of the missing-work design before execution. | pass |
| [CRAFT-MISSING-WORK-EXECUTION-PACK.md](CRAFT-MISSING-WORK-EXECUTION-PACK.md) | Execution sequencing for the first missing-work live-test task. | pass |
| [CRAFT-MISSING-WORK-WORK-PACK.md](CRAFT-MISSING-WORK-WORK-PACK.md) | Completed work-pack for producing the Interrogation refine-review receipt. | pass |
| [CRAFT-MISSING-WORK-LIVE-TEST.md](CRAFT-MISSING-WORK-LIVE-TEST.md) | Current live-test result: Interrogation receipt passed; Distill is next blocker. | pass |
| [CRAFT-REFINE-SINGLE-RECEIPT-WORK-PACK.md](CRAFT-REFINE-SINGLE-RECEIPT-WORK-PACK.md) | Completed work-pack for producing one aggregate Refine receipt for the current run. | pass |

## Current Next Move

```text
Continue the current Refine run under the aggregate receipt model.
```

Recommended route:

```text
Use `receipts/refine-run.json` as the single Refine receipt and update it when internal Refine evidence is completed or intentionally blocked.
```

Why this route:

```text
The aggregate Refine receipt exists and reports `block` because internal Refine
work remains incomplete. Distill and later stages should stay internal Refine
evidence rather than becoming standalone receipt gates.
```

Use [CRAFT-VALIDATION.md](CRAFT-VALIDATION.md) as the review surface. Promotion remains deferred by [CRAFT-PROMOTION-READINESS.md](CRAFT-PROMOTION-READINESS.md).

## Guardrail

Craft development stays in `development/craft/` until a later, explicit promotion route says otherwise. In this phase, Craft may describe how it composes Arcanum capabilities, but it should not silently replace or mutate them.
