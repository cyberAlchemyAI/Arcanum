---
name: invoke
description: "Use when: turning development intent into governed define, design, plan, handoff, or refresh artifacts before lifecycle execution."
argument-hint: "<define|design|plan|handoff|refresh|full|validate> <target-or-intent> [--output <path>] [--dry-run]"
tier: spells
domain: lifecycle-authoring
version: 0.2.0
origin: canonical Arcanum spell for intent-to-artifact authoring
allowed-tools: Read, Write, Glob, Grep, Bash, AskQuestions, Task
---

# Invoke

## Identity

- Canonical ID: `invoke`
- Aliases: none
- Scope: library

## Purpose

Invoke turns vague development intent into governed authoring artifacts. The root spell file stays intentionally compact and delegates mode behavior to per-mode contracts under `spells/invoke/`.

Invoke is an authoring front door, not the lifecycle owner for every artifact it can describe. It discovers intent, shapes definitions, designs, and plans, then hands off to the capability that owns the target lifecycle.

Invoke does not require deprecated command files, slash commands, or command-resolution bridges as authoring readiness evidence. When an Invoke-authored plan prepares later execution, it should name native capability handles, expected receipts, validation surfaces, and subagent/local fallback boundaries. Legacy command adapters may remain as explicit example-runner compatibility only.

## Trigger Conditions

- The user has something to build but the authoring baseline is missing or inconsistent.
- A reusable spec and glossary are needed before architecture or execution planning.
- The workflow needs one-question clarification, explicit approvals, and auditable outputs.

## Mode Contracts

| Mode       | Status           | Contract File                              | Notes                                                  |
| ---------- | ---------------- | ------------------------------------------ | ------------------------------------------------------ |
| `define`   | implemented (L0) | [define.md](./define.md)     | Active authoring baseline mode with the DomainSpec template (`templates/domainspec-spec/`), standalone companions, and dedicated candidate family scaffolds. |
| `design`   | implemented (L1 contract) | [design.md](./design.md)     | Converts approved define outputs into governed architecture/design artifacts; validation examples still gate promotion. |
| `plan`     | implemented (L2 contract) | [plan.md](./plan.md)         | Converts approved design outputs into implementation plans, layering artifacts, and work-packs. |
| `handoff`  | implemented (L2 companion contract) | [handoff.md](./handoff.md) | Creates a new session/thread handoff from a prompt, source session reference, and Context Builder selection. |
| `refresh`  | implemented (L2 refresh contract) | [refresh.md](./refresh.md) | Updates existing invoke-authored workflow artifacts from new session evidence through typed deltas. |
| `full`     | deferred         | [full.md](./full.md)         | Composite execution mode, pending L2 and L3 readiness. |
| `validate` | deferred         | [validate.md](./validate.md) | Lifecycle validation mode, pending L3.                 |

## Core Required Sigils

| Sigil                       | Role In Spell                                                         | Required Mode  |
| --------------------------- | --------------------------------------------------------------------- | -------------- |
| `structured-interview-kits` | Clarify missing context one question at a time and capture approvals. | mode-dependent |
| `inventory`                 | Resolve local templates and record template usage evidence.           | mode-dependent |
| `context-builder`           | Build bounded context for invoke inputs and artifact linking.         | mode-dependent |
| `dispatch-spec`             | Select and validate the Dispatch Spec technique trace that shapes each invoke route. | technique trace or dispatch validation |

## Core Optional Sigils

| Sigil                            | Use When                                                             | Notes                                                                              |
| -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `decision-gate`                  | A blocker-level decision cannot be resolved from available evidence. | Route only consequential unresolved choices.                                       |
| `spellcraft`                     | Approved invoke output targets spell authoring or spell revision.    | Invoke prepares handoff context only; Spellcraft owns spell lifecycle mutation, validation, install, observation, and reflection. |
| `sigil-development`              | Approved invoke output targets sigil authoring or sigil revision.    | Invoke prepares handoff context only; Sigil Development owns sigil lifecycle mutation, validation, observability, reflection, and promotion readiness. |
| `architecture-pattern-inventory` | Design-stage work needs reusable pattern evidence or alternatives.    | Optional design-mode evidence source; does not override design gates.              |
| `task-session`                   | Plan output is ready for bounded execution.                          | Invoke emits handoff context; Task Session owns execution.                         |
| `distill`                        | A broad output needs smallest coherent unit validation, scope reduction, or gap discovery. | Required as automatic validate pass for `plan`, `full`, and `validate`; triggered for other modes when scope is broad or overbuilt. |

## Lifecycle Authority Chain

Use this chain to avoid responsibility overlap:

1. `invoke` owns intent-to-artifact authoring: define, design, plan, work-pack creation, and handoff context.
2. `sigil-development` owns sigil lifecycle: create, revise, validate, observe, reflect, iterate, and prepare promotion evidence.
3. `spellcraft` owns spell lifecycle: compose sigils, define phases and gates, install/adapt spells, validate, observe, reflect, and revise.
4. `task-session` owns bounded execution from an approved work-pack task or SWU.

Invoke may write handoff artifacts inside a target capability's `development/` folder, but it must not claim the target lifecycle is complete. The handoff route becomes the next owner.

### Chaining Workflow

For a new sigil:

```text
invoke define/design/plan -> sigil-development --new/--update -> task-session when implementation work-pack tasks are ready
```

For a new spell:

```text
invoke define/design/plan -> spellcraft design/install/validate -> task-session when implementation work-pack tasks are ready
```

For an ordinary feature or module:

```text
invoke define/design/plan -> task-session to WORK-PACK.md
```

For a new thread split from the current session:

```text
invoke handoff -> workflow-reflect | invoke define/design/full | research | task-session
```

For artifact refresh after a session result:

```text
invoke refresh -> proposal-only refresh report -> task-session | workflow-reflect | deferred
```

When a target is already clearly a sigil or spell, Invoke should produce a compact handoff packet and route early instead of expanding into lifecycle execution.

## Cross-Cutting Transmutations

| Transmutation | Role In Spell | Application Rule |
| --- | --- | --- |
| `implementation-layering` | Keeps plan/full/validate outputs bounded by explicit layer decisions and promotion evidence. | Optional seed in `define` and `design`; required companion artifact in `plan`, `full`, and `validate`. |

## Dispatch Technique Discipline

Every invoke mode must record a Dispatch Spec technique trace before it returns a pass or flag result. The trace selects only techniques from `formulae/dispatch-spec/TECHNIQUE-CATALOG.md` or explicitly names a local-extension source, then connects each selected technique to a mode phase, output artifact, gate, evidence expectation, or unresolved gap.

Minimum trace fields:

- selected technique ids,
- activation trigger,
- affected phase or artifact,
- validation expectation,
- skipped technique reasons when an obvious technique was considered and rejected,
- whether a full dispatch JSON was needed and, if so, the validation result.

Common invoke techniques include `sequence`, `frame_handoff`, `handle_handoff`, `residue_ledger`, `owner_boundary_check`, `artifact_contract_bridge`, `validation_loop`, `concrete_path_evidence`, and `observability_grouping`. Plan, full, and validate modes additionally consider `scu_swu_reduction`, `recomposition_proof`, `execution_receipt_handoff`, and `authority_split_gate`.

Do not list techniques as decoration. A technique citation that does not affect a phase, output, gate, evidence check, or gap route is a flag. When the invoke route crosses multiple capabilities, delegates work, defines subagent strategy, creates a reusable route artifact, or carries protected/private context, create a dispatch document and validate it with `formulae/dispatch-spec/scripts/validate-dispatch.py`.

## Distill Validation

Plan, full, and validate must run automatic Distill validation against the draft implementation plan, layering artifact, work-pack, and handoff route before reporting mutation-capable readiness. Distill validation checks whether the selected unit is small enough to execute, large enough to preserve meaning, recomposes into the approved design, exposes hidden gaps, and avoids overbuilt or vague task structure.

Distill verdict handling:

- `pass`: the output may route to its next owner if all other gates pass.
- `flag`: the output may route only when the gap ledger names each Distill gap, owner, and repair path.
- `block`: the output must not route to mutation-capable execution until the smallest coherent unit, SWU boundary, recomposition proof, or acceptance-critical gap is repaired.

Define, design, handoff, and refresh should run Distill when the requested output is broad, ambiguous, overbuilt, or likely to hide lifecycle gaps, but they may record a skipped reason when the output is already narrow and locally bounded.

## Prerequisites

- Repository root is known.
- Development pack context is available under `spells/invoke/development/`.
- Local template inventory is available, or candidate-template creation is allowed by user approval.
- Current prebuilt template inventory is rooted at `arcanum/spells/invoke/templates/` and includes the DomainSpec template family (`domainspec-spec/` — define baseline `SPEC.md` + aspect docs, design-stage `architecture-bundle.md`, plan-stage `execution-pack.md`), standalone companion templates, and dedicated candidate family scaffolds. The legacy `module-formulae/` family is deprecated and retained only for the invoke validation fixtures and the `mogt` research project; physical removal is gated on regenerating those (see `templates/module-formulae/README.md`).
- Implementation layering transmutation is available at `arcanum/transmutations/implementation-layering/`.
- Implementation-layering template is available at `arcanum/spells/invoke/templates/implementation-layering.md`.
- Work-pack template is available at `arcanum/spells/invoke/templates/work-pack.md`.
- Necronomicon concept sources are reachable when glossary linking is requested.

## Shared State

| State                       | Owner | Updated By                                      | Consumed By                           |
| --------------------------- | ----- | ----------------------------------------------- | ------------------------------------- |
| define intent record        | spell | `structured-interview-kits` and `invoke define` | define synthesis, decision routing    |
| template selection record   | spell | `inventory` and `invoke define`                 | define synthesis, validation, handoff |
| spec artifact               | spell | `invoke define`                                 | downstream design or plan routing     |
| glossary artifact           | spell | `invoke define`                                 | downstream design or plan routing     |
| design artifact             | spell | `invoke design`                                 | downstream plan routing and validation |
| glossary consistency report | spell | `invoke design`                                 | design validation and gap routing     |
| implementation layering artifact | spell | `invoke design`, `invoke plan`, and `invoke full` | plan validation, execution handoff, and release checks |
| implementation plan artifact | spell | `invoke plan` and `invoke full` | work-pack mapping, validation strategy, and execution handoff |
| work-pack artifact          | spell | `invoke plan` and `invoke full`                 | stable planning manifest and execution handoff |
| session handoff artifact    | spell | `invoke handoff`                                | new session/thread start, reflection, research, or continuation route |
| refresh report              | spell | `invoke refresh`                                | evidence-backed artifact deltas, proposals, no-op decisions, and next route |
| define transport report     | spell | `invoke define`                                 | Necronomicon context          |
| design transport report     | spell | `invoke design`                                 | Necronomicon context          |
| plan transport report       | spell | `invoke plan`                                   | Necronomicon context          |
| unresolved gap ledger entry | spell | `invoke define`, `invoke design`, and optional `decision-gate` | follow-up routing                     |

## Mode Router

1. Resolve requested mode and load the corresponding mode contract.
2. Select a Dispatch Spec technique trace for the mode route and determine whether a full dispatch document is required.
3. Execute the mode contract phases and collect mode outputs.
4. Run automatic Distill validation when required by mode or triggered by broad/ambiguous output shape.
5. Apply global gates, observability, and handoff policy from this root contract.

## Target Artifact Provenance

Invoke may author artifacts for another capability, module, spell, sigil, or repository feature. In those cases, invoke remains the observed authoring capability, but the produced artifact belongs to the target development cycle.

Every invoke run that targets another artifact should record:

- observed capability: always `invoke`,
- invoke mode: `define`, `design`, `plan`, `handoff`, `refresh`, `full`, `validate`, or a composed mode,
- target artifact name and type,
- target artifact owner or lifecycle cycle,
- output paths owned by the target artifact,
- invoke-specific gaps,
- target-artifact gaps,
- recommended next route for the target artifact.

Reflection and telemetry from such a run should preserve both layers. If the gap is caused by invoke behavior, template routing, output contract drift, or missing invoke guidance, route the follow-up through the invoke development cycle. If the gap is in the authored subject matter, state schema, design, plan, or implementation readiness of the target artifact, route the follow-up through the target artifact's development cycle.

## Global Handoff Artifacts

- define context summary
- target artifact name, type, owner, and lifecycle cycle
- source session reference and new-session prompt when mode is `handoff`
- handoff type and Context Builder coverage status when mode is `handoff`
- source signals, target artifact inventory, mutation mode, and delta summary when mode is `refresh`
- mode artifact paths
- design artifact paths and six-view coverage
- glossary consistency report
- mode selection evidence
- implementation plan artifact path
- implementation layering artifact path and layer decision snapshot
- per-layer planning slice coverage when complexity is medium or high
- work-pack artifact path and output mode (single-file or split)
- Dispatch Spec technique trace and dispatch validation result when a full dispatch document is required
- Distill validation verdict, gap summary, and recomposition proof status when run
- unresolved gaps and blocker decisions
- Necronomicon transport report
- recommended next route (`task-session`, `full`, `spellcraft`, `sigil-development`, or deferred follow-up)

## Global Gates

- One-question interview cadence when context is missing in interactive mode.
- Template or recipe selection must show eligibility evidence and explicit user choice on ties.
- Every mode must include a Dispatch Spec technique trace; missing trace blocks pass-ready output, and unused technique citations flag.
- `plan`, `full`, and `validate` must include an implementation-layering artifact; `define` and `design` may emit a seed or explicit gap.
- `plan`, `full`, and `validate` must include a work-pack artifact mapped from implementation-plan tasks and layer decisions.
- `plan`, `full`, and `validate` must include a validation strategy for every delivery slice.
- `plan`, `full`, and `validate` must run automatic Distill validation and report pass, flag, or block before mutation-capable handoff.
- Medium/high complexity plans must include explicit L0-L3 per-layer planning slices; low complexity plans may keep compact layer mapping in the single-file work-pack.
- Medium/high complexity plans must include implementation-detail specs for execution tasks, and algorithmic or domain-logic tasks must document inputs, outputs, ordered rules or pseudocode, edge cases, failure modes, and validation evidence.
- Medium/high complexity work-packs must include Smallest Working Units: a shared SWU manifest, task-local SWU lists, one parent task per SWU, write scope, acceptance evidence, and verification command or reviewable check.
- Vague task labels such as "implement this bundle" are not execution-ready unless backed by implementation-detail specs.
- Layer promotion requires evidence from the previous layer, not preference alone.
- Candidate glossary or registry promotion is never automatic.
- No silent upstream mutation; direct upstream edits require explicit approval.
- Stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Reflection provenance must distinguish invoke telemetry ownership from target artifact ownership.
- Session/thread handoffs must select context from the referenced session through Context Builder and must not substitute a whole-session transcript for obligation-linked context.
- Handoff mode must preserve the user's split reason: workflow gap, new lifecycle idea, research direction, execution continuation, or generic continuation.
- Refresh mode must map every proposed or applied artifact update to a typed source signal and must default to proposal-only.
- Refresh mode must treat no-op as a valid outcome when latest evidence is already represented.

## Global Failure Policy

- Return `block` when blocker ambiguity, missing mandatory inputs, or governance violations prevent safe mode output.
- Return `flag` when mode output is usable but includes unresolved non-blocker gaps.
- Stop at the first blocked gate and return remediation guidance rather than silently switching modes.

## Local Customization

- Spell root: `.arcanum/spells/` for local adaptations, `spells/` for this reusable library spell.
- Local paths: output paths come from selected templates and local project conventions.
- Gate strictness: standard for authoring modes; blocker decisions remain strict.
- Interaction mode: interactive one-question clarification by default.

## Observability

When `.arcanum/observability/` exists, record:

- spell name and mode,
- phases attempted,
- sigils invoked,
- gates passed, flagged, or blocked,
- artifact paths produced,
- unresolved gaps and blocker decisions,
- handoff target recommendation,
- handoff type and source session reference when mode is `handoff`,
- refresh source signal count, delta classes, mutation mode, and no-op rationale when mode is `refresh`,
- target artifact name, type, owner, and lifecycle cycle,
- gap ownership split between invoke-specific gaps and target-artifact gaps,
- referenced mode contract,
- selected Dispatch Spec techniques and dispatch validation status,
- Distill validation verdict and gap count,
- design view coverage and glossary consistency status,
- plan complexity and output mode,
- implementation layer coverage and per-layer planning slice status,
- implementation-detail coverage status,
- SWU coverage status,
- validation and follow-up action.

## Root Output Contract

Return:

```markdown
## Invoke Result

- Mode: <define | design | plan | handoff | refresh | full | validate>
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: <path>
- Outputs: <mode output paths>
- Design views: <coverage summary | n/a>
- Glossary consistency: <pass | flag | block | n/a>
- Dispatch techniques: <ids selected, validation status, full dispatch path | n/a>
- Distill validation: <pass | flag | block | skipped with reason | n/a>
- Implementation layering: <artifact path | seed emitted | gap recorded>
- Work-pack: <artifact path | single-file | split>
- Complexity: <low | medium | high | n/a>
- Per-layer planning: <compact | L0, L1, L2, L3 | blocked | n/a>
- Implementation detail: <inline | task specs complete | detail gaps recorded | blocked | n/a>
- Smallest working units: <n/a | complete | gaps recorded | blocked>
- Refresh: <n/a | report path and delta summary | no-op | blocked>
- Target artifact: <name, type, owner/cycle>
- Template or recipe selection: <summary>
- Decisions: <summary>
- Unresolved gaps: <invoke gaps; target artifact gaps>
- Next route: task-session | workflow-reflect | full | spellcraft | sigil-development | deferred
```

Mode-specific execution phases and mode-level output contracts are defined in [define.md](./define.md), [design.md](./design.md), [plan.md](./plan.md), [handoff.md](./handoff.md), [refresh.md](./refresh.md), [full.md](./full.md), and [validate.md](./validate.md).
