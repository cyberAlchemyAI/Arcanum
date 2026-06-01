# Craft Architecture Inputs

## Purpose

This register converts remaining Craft gaps into explicit inputs for the next Craft method architecture package.

It does not solve the architecture. It tells the architecture pass what it must decide, what evidence it must use, and which concerns are deferred or owned by side threads.

## Current Status

| Field | Value |
| --- | --- |
| Status | architecture-input-register |
| Created by | `CRAFT-GAP-002` |
| Prerequisite closed | `CRAFT-GLOSSARY.md` exists and closes the pre-architecture vocabulary blocker. |
| Expected next architecture route | `invoke design`-style Craft method architecture package |
| Candidate next artifacts | `CRAFT-ARCHITECTURE.md`, `CRAFT-LIFECYCLE.md`, `CRAFT-ROUTE-MAP.md`, `CRAFT-VALIDATION.md` |

## Classification Rule

Remaining gaps must be one of:

| Class | Meaning |
| --- | --- |
| `architecture-owned input` | Must be decided or shaped by the next Craft architecture package. |
| `deferred implementation concern` | Should remain out of the architecture acceptance gate until architecture and examples justify implementation. |
| `side-thread dependency` | Related work with a separate owner thread; architecture may reference it but must not claim it is solved. |
| `closed evidence` | Already proven by the recursive-ledger MVP or gap-closure wave. |

## Architecture-Owned Inputs

| Input ID | Input | Why Architecture Owns It | Required Source Evidence | Acceptance Question |
| --- | --- | --- | --- | --- |
| ARCH-IN-001 | Craft method architecture package | The initial definition is strong conceptually, but Craft still needs an auditable operational contract that organizes lifecycle, artifacts, route boundaries, validation, and recomposition. | `CRAFT-INITIAL-DEFINITION.md`, `CRAFT-GLOSSARY.md`, `LEDGER.md`, `LEDGER-VALIDATION.md`, `CRAFT-GAP-CLOSURE-WORK-PACK.md` | Does the architecture define Craft as a candidate method with clear lifecycle, artifact boundaries, authority limits, and recomposition rules without promoting it canonically? |
| ARCH-IN-002 | Route integration contract | Craft must clarify when it routes to existing Arcanum sigils/spells instead of taking their authority. This is architectural because it governs responsibility boundaries across capabilities. | `SESSION-LEDGER.md` decision ledger, `CRAFT-GLOSSARY.md` route/handoff terms, `refinement-runs/20260529T105556Z-close-gaps/RESULT.md` | Can a user or agent tell which route owns define, design, plan, refine, task execution, decision gates, validation, reflection, and runtime handoff? |
| ARCH-IN-003 | Validation example-suite shape | Craft needs examples to prove SCU selection, residue classification, recomposition, and architecture route behavior. Architecture must define the example categories before implementation creates fixtures. | `CRAFT-INITIAL-DEFINITION.md` SCU/residue sections, `LEDGER-VALIDATION.md`, `CRAFT-GLOSSARY.md`, `CRAFT-LEDGER-TYPE-EXAMPLES.md` | Does the architecture name the minimum example suite required to validate Craft method claims without prematurely building the suite? |
| ARCH-IN-004 | Promotion decision path | Craft remains candidate. Architecture must define what evidence would be required before deciding whether Craft becomes a sigil, spell, framework method, mixed package, or stays local. | `SESSION-LEDGER.md` decisions and candidate seeds, `CRAFT-GLOSSARY.md` promotion term, `LEDGER-VALIDATION.md` pass evidence | Does the architecture provide a promotion checklist and decision route without promoting Craft automatically? |
| ARCH-IN-005 | Type-to-lane-to-role automation evidence | The recursive-ledger MVP validates type/lane representation, but automation needs more examples and authority. Architecture must define what evidence is required before delegation rules become executable. | `CRAFT-LEDGER-TYPE-SYSTEM.md`, `CRAFT-GLOSSARY.md`, `LEDGER.md`, `LEDGER-VALIDATION.md` | Does the architecture keep role delegation manual until examples prove reliable mappings and owner authority? |

## Deferred Implementation Concerns

| Concern | Why Deferred | Required Future Evidence | Current Boundary |
| --- | --- | --- | --- |
| Priority scoring | Scoring depends on multiple valid ledger states and stable relationship semantics. | Several validated ledgers with different blocker/enabler/readiness profiles. | Do not include scoring in architecture acceptance criteria beyond naming the future seam. |
| Generated ledger index | A machine-readable index is useful only after repeated query or automation needs appear. | Query patterns, index consumers, and validation rules for generated state. | Keep `ledger-index.json` deferred. |
| Role delegation automation | Type plus lane can suggest role hints, but automated delegation requires examples, confidence rules, and route authority. | Example suite covering business, tech, qa, validator, auditor, governance, planner, operations, and integrator lanes. | Architecture may define requirements, not implement automation. |
| Runtime execution integration | Runtime adapter and command-route gaps are real but owned by separate runtime/interface work. | Completed runtime strategy or interface thread artifacts. | Architecture may reference as external dependency only. |

## Side-Thread Dependencies

| Dependency | Owner Artifact | Architecture Treatment |
| --- | --- | --- |
| Refine runtime strategy | `CRAFT-REFINE-RUNTIME-STRATEGY.md` | Reference as a side-thread. Do not make canonical refine mutation part of Craft architecture acceptance. |
| Arcanum skill runtime interface | `ARCANUM-SKILL-RUNTIME-HANDOFF.md` | Reference as a separate lifecycle thread. Do not require completion before Craft method architecture. |
| Missing `dispatch-spec` and `runtime-handoff` command routes | `refinement-runs/20260529T105556Z-close-gaps/RESULT.md` | Treat as runtime-command surface gap, not Craft architecture blocker. |

## Runtime Boundary Contract

Craft architecture may mention runtime/interface work only as an external dependency or future integration seam.

| Boundary | Rule | Owner Evidence | Craft Architecture Impact |
| --- | --- | --- | --- |
| Refine runtime topology | The orchestrator/stage-worker strategy is a candidate refine runtime strategy, not a Craft architecture acceptance criterion. | `CRAFT-REFINE-RUNTIME-STRATEGY.md` | Architecture can reference the need for stage-aware routes, but cannot claim canonical refine runtime mutation is complete. |
| Skill runtime interface | The cross-runtime skill invocation interface belongs to a separate Arcanum runtime lifecycle thread. | `ARCANUM-SKILL-RUNTIME-HANDOFF.md` | Architecture can require compatibility with a future interface, but must not block on that interface being designed or implemented. |
| Command route availability | Missing `dispatch-spec` and `runtime-handoff` command routes block canonical Refine v0.2.0 execution, not Craft method architecture. | `refinement-runs/20260529T105556Z-close-gaps/RESULT.md` | Architecture should preserve this as runtime-command evidence and avoid treating it as a Craft-local blocker. |
| Runtime mutation authority | Runtime adapters, command surfaces, skill wrappers, sigils, spells, registries, and observation plumbing are outside this architecture pass. | Craft package guardrails and gap-closure work-pack gates. | Any mutation must route through the runtime/interface or refine-runtime owner thread. |

## Non-Blocking Runtime Statement

Craft method architecture can continue when the runtime/interface items above remain open, provided the architecture:

1. cites their owner artifacts,
2. labels them external or deferred,
3. does not list them as Craft-local blockers,
4. does not claim they are solved,
5. does not mutate command, runtime, registry, sigil, spell, or skill surfaces.

## Closed Evidence Feeding Architecture

| Evidence | What It Proves | Source |
| --- | --- | --- |
| Recursive-ledger MVP package sync | Craft can represent nested contexts, artifacts, relations, typed items, decisions, blockers, gates, enablers, and deferred future work. | `LEDGER.md`, `LEDGER-VALIDATION.md` |
| Blocker refinement and waiver behavior | Raw blockers cannot resolve directly; refined, resolved, and waived blockers can be represented with evidence. | `LEDGER.md`, `LEDGER-VALIDATION.md` |
| Craft glossary | Base vocabulary is stable enough for architecture planning. | `CRAFT-GLOSSARY.md` |

## Architecture Acceptance Gate

The next architecture package should pass only if it answers:

1. What is Craft's lifecycle from intent through recomposition?
2. Which artifacts does Craft own, and which artifacts remain owned by existing Arcanum capabilities?
3. Which routes does Craft call instead of replacing?
4. Which validation examples are required before promotion or automation?
5. What evidence is required before priority scoring, generated indexes, or role delegation automation can start?
6. What is explicitly side-threaded and non-blocking for Craft architecture?

## Non-Goals For The Architecture Pass

The architecture pass should not:

- mutate canonical Arcanum registries,
- install or alter runtime commands,
- promote Craft into a sigil, spell, or framework method,
- implement scoring, generated indexes, or role delegation automation,
- claim runtime interface side-thread work is solved.

## Next Route

After the gap-closure wave completes:

```text
invoke design development/craft/CRAFT-ARCHITECTURE.md
```

The design should consume this register as its architecture input map.
