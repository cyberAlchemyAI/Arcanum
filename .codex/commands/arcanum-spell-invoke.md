# Arcanum Spell: invoke

<!-- arcanum:capability-id invoke -->
<!-- arcanum:capability-kind spell -->
<!-- arcanum:capability-tier spell -->
<!-- arcanum:command arcanum-spell-invoke -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-arcanum-spell-invoke-<UTC timestamp>`.
- `capability.id`: `invoke`
- `capability.kind`: `spell`
- `capability.tier`: `spell`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum spell `invoke` using the canonical spell snapshot embedded below.

## Process

1. Use the embedded canonical spell snapshot as the execution contract.
2. Execute only this installed spell unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected spell's process, quality bar, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `invoke`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical Spell Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/spells/invoke/README.md

````markdown
# Invoke

## Identity

- Canonical ID: `invoke`
- Aliases: none
- Scope: library

## Purpose

Invoke turns vague development intent into governed authoring artifacts. The root spell file stays intentionally compact and delegates mode behavior to per-mode contracts under `spells/invoke/`.

## Trigger Conditions

- The user has something to build but the authoring baseline is missing or inconsistent.
- A reusable spec and glossary are needed before architecture or execution planning.
- The workflow needs one-question clarification, explicit approvals, and auditable outputs.

## Mode Contracts

| Mode       | Status           | Contract File                              | Notes                                                  |
| ---------- | ---------------- | ------------------------------------------ | ------------------------------------------------------ |
| `define`   | implemented (L0) | [define.md](./define.md)     | Active authoring baseline mode with Module Formulae baseline coverage, standalone companions, and candidate family scaffolds. |
| `design`   | implemented (L1 contract) | [design.md](./design.md)     | Converts approved define outputs into governed architecture/design artifacts; validation examples still gate promotion. |
| `plan`     | implemented (L2 contract) | [plan.md](./plan.md)         | Converts approved design outputs into implementation plans, layering artifacts, and work-packs. |
| `full`     | deferred         | [full.md](./full.md)         | Composite execution mode, pending L2 and L3 readiness. |
| `validate` | deferred         | [validate.md](./validate.md) | Lifecycle validation mode, pending L3.                 |

## Core Required Sigils

| Sigil                       | Role In Spell                                                         | Required Mode  |
| --------------------------- | --------------------------------------------------------------------- | -------------- |
| `structured-interview-kits` | Clarify missing context one question at a time and capture approvals. | mode-dependent |
| `inventory`                 | Resolve local templates and record template usage evidence.           | mode-dependent |
| `context-builder`           | Build bounded context for invoke inputs and artifact linking.         | mode-dependent |

## Core Optional Sigils

| Sigil                            | Use When                                                             | Notes                                                                              |
| -------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `decision-gate`                  | A blocker-level decision cannot be resolved from available evidence. | Route only consequential unresolved choices.                                       |
| `spellcraft`                     | Approved invoke output targets spell authoring or spell revision.    | Invoke prepares handoff context; Spellcraft owns spell lifecycle execution.        |
| `sigil-development`              | Approved invoke output targets sigil authoring or sigil revision.    | Invoke prepares handoff context; Sigil Development owns sigil lifecycle execution. |
| `architecture-pattern-inventory` | Design-stage work needs reusable pattern evidence or alternatives.    | Optional design-mode evidence source; does not override design gates.              |
| `task-session`                   | Plan output is ready for bounded execution.                          | Invoke emits handoff context; Task Session owns execution.                         |

## Cross-Cutting Transmutations

| Transmutation | Role In Spell | Application Rule |
| --- | --- | --- |
| `implementation-layering` | Keeps plan/full/validate outputs bounded by explicit layer decisions and promotion evidence. | Optional seed in `define` and `design`; required companion artifact in `plan`, `full`, and `validate`. |

## Prerequisites

- Repository root is known.
- Development pack context is available under `spells/invoke/development/`.
- Local template inventory is available, or candidate-template creation is allowed by user approval.
- Current prebuilt template inventory is rooted at `arcanum/spells/invoke/templates/` and includes Module Formulae, standalone companion templates, and dedicated candidate family scaffolds.
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
| define transport report     | spell | `invoke define`                                 | Necronomicon context          |
| design transport report     | spell | `invoke design`                                 | Necronomicon context          |
| plan transport report       | spell | `invoke plan`                                   | Necronomicon context          |
| unresolved gap ledger entry | spell | `invoke define`, `invoke design`, and optional `decision-gate` | follow-up routing                     |

## Mode Router

1. Resolve requested mode and load the corresponding mode contract.
2. Execute the mode contract phases and collect mode outputs.
3. Apply global gates, observability, and handoff policy from this root contract.

## Target Artifact Provenance

Invoke may author artifacts for another capability, module, spell, sigil, or repository feature. In those cases, invoke remains the observed authoring capability, but the produced artifact belongs to the target development cycle.

Every invoke run that targets another artifact should record:

- observed capability: always `invoke`,
- invoke mode: `define`, `design`, `plan`, `full`, `validate`, or a composed mode,
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
- mode artifact paths
- design artifact paths and six-view coverage
- glossary consistency report
- mode selection evidence
- implementation plan artifact path
- implementation layering artifact path and layer decision snapshot
- per-layer planning slice coverage when complexity is medium or high
- work-pack artifact path and output mode (single-file or split)
- unresolved gaps and blocker decisions
- Necronomicon transport report
- recommended next route (`task-session`, `full`, `spellcraft`, `sigil-development`, or deferred follow-up)

## Global Gates

- One-question interview cadence when context is missing in interactive mode.
- Template or recipe selection must show eligibility evidence and explicit user choice on ties.
- `plan`, `full`, and `validate` must include an implementation-layering artifact; `define` and `design` may emit a seed or explicit gap.
- `plan`, `full`, and `validate` must include a work-pack artifact mapped from implementation-plan tasks and layer decisions.
- `plan`, `full`, and `validate` must include a validation strategy for every delivery slice.
- Medium/high complexity plans must include explicit L0-L3 per-layer planning slices; low complexity plans may keep compact layer mapping in the single-file work-pack.
- Medium/high complexity plans must include implementation-detail specs for execution tasks, and algorithmic or domain-logic tasks must document inputs, outputs, ordered rules or pseudocode, edge cases, failure modes, and validation evidence.
- Medium/high complexity work-packs must include Smallest Working Units: a shared SWU manifest, task-local SWU lists, one parent task per SWU, write scope, acceptance evidence, and verification command or reviewable check.
- Vague task labels such as "implement this bundle" are not execution-ready unless backed by implementation-detail specs.
- Layer promotion requires evidence from the previous layer, not preference alone.
- Candidate glossary or registry promotion is never automatic.
- No silent upstream mutation; direct upstream edits require explicit approval.
- Stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Reflection provenance must distinguish invoke telemetry ownership from target artifact ownership.

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
- target artifact name, type, owner, and lifecycle cycle,
- gap ownership split between invoke-specific gaps and target-artifact gaps,
- referenced mode contract,
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

- Mode: <define | design | plan | full | validate>
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: <path>
- Outputs: <mode output paths>
- Design views: <coverage summary | n/a>
- Glossary consistency: <pass | flag | block | n/a>
- Implementation layering: <artifact path | seed emitted | gap recorded>
- Work-pack: <artifact path | single-file | split>
- Complexity: <low | medium | high | n/a>
- Per-layer planning: <compact | L0, L1, L2, L3 | blocked | n/a>
- Implementation detail: <inline | task specs complete | detail gaps recorded | blocked | n/a>
- Smallest working units: <n/a | complete | gaps recorded | blocked>
- Target artifact: <name, type, owner/cycle>
- Template or recipe selection: <summary>
- Decisions: <summary>
- Unresolved gaps: <invoke gaps; target artifact gaps>
- Next route: task-session | full | spellcraft | sigil-development | deferred
```

Mode-specific execution phases and mode-level output contracts are defined in [define.md](./define.md), [design.md](./design.md), [plan.md](./plan.md), [full.md](./full.md), and [validate.md](./validate.md).

````
