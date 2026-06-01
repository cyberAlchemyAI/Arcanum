# Craft Development Package

This package is the active development space for `Craft`, a candidate Arcanum/CyberAlchemy method primitive for turning intention into stable artifacts through schema/data translation, residue handling, SCU/SWU selection, validation, reflection, and recomposition.

Craft is not canonical authority yet. This package is checkpoint-first: it preserves evidence, session state, candidate decisions, and future work boundaries before any registry, runtime, sigil, spell, or framework promotion.

## Start Here

1. [DURABLE-SESSION-CONTEXT.md](DURABLE-SESSION-CONTEXT.md)
2. [SESSION-LEDGER.md](SESSION-LEDGER.md)
3. [CRAFT-INITIAL-DEFINITION.md](CRAFT-INITIAL-DEFINITION.md)

## Current Verdict

`refine-validation-stage-receipt-blocked-promotion-deferred`

The recursive-ledger MVP is validated, the pre-architecture gap-closure wave is complete, and the broader Craft method architecture has passed design and plan hardening. Craft now has a candidate validation example suite, validation/recomposition guide, promotion readiness review, and a cleared runtime command-surface smoke for the previously missing `dispatch-spec` and `runtime-handoff` routes. Native Refine evidence classification has been repaired: handoff stubs are no longer counted as completed owner-stage artifacts. The latest Refine validation now blocks honestly because the Context Builder stage has only a prepared runtime-native handoff and still needs an owner-stage execution receipt. Promotion is deferred until repeated local use and receipt-backed validation produce stronger evidence.

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
Run:    development/craft/development/refinement-runs/20260601T015552Z-craft-validation-md
Result: block
Dispatch validation: pass
Reason: Context Builder evidence baseline is `flag` with `evidence_kind=handoff_prepared`; no owner-stage execution receipt exists yet.
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

## Current Next Move

```text
Create the parent-native stage execution receipt path before treating Craft Refine validation as complete.
```

Recommended route:

```text
$task-session development/craft/CRAFT-NATIVE-STAGE-EXECUTION-RECEIPTS-WORK-PACK.md --task CRAFT-NATIVE-RECEIPT-001
```

Why this route:

```text
The parent-native receipt bridge has been planned. The next executable step is
to define the local stage receipt contract before mutating native Refine
receipt ingestion.
```

Use [CRAFT-VALIDATION.md](CRAFT-VALIDATION.md) as the review surface. Promotion remains deferred by [CRAFT-PROMOTION-READINESS.md](CRAFT-PROMOTION-READINESS.md).

## Guardrail

Craft development stays in `development/craft/` until a later, explicit promotion route says otherwise. In this phase, Craft may describe how it composes Arcanum capabilities, but it should not silently replace or mutate them.
