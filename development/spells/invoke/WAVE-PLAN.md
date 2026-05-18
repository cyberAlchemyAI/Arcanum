# Invoke Spell Wave Plan

## Purpose

Define an implementation-ready plan for one reusable Arcanum library spell: `invoke`.

`invoke` should convert vague development intent into governed artifacts through one unified flow:

1. intent to spec and glossary,
2. spec/glossary to architecture/design bundle,
3. approved spec/design to executable work-pack.

## Scope

- Build one reusable library spell under `arcanum/spells/invoke.md`.
- Keep the active development pack under `arcanum/development/spells/invoke/` until Spellcraft validation and release approval promote the canonical spell file.
- Register `invoke` in `arcanum/registry/SPELLS.md` after validation.
- Keep feature-spec authorship in the dedicated feature-spec commands.
- Keep Spellcraft and Sigil Development as lifecycle authorities for spell and sigil authoring handoffs.
- Allow Necronomicon route presets to call `invoke` after release.
- Treat `invoke` as a baseline Necronomicon route for implementation-research handoffs and define/design/plan lifecycle requests once released.
- Maintain an `invoke`-owned glossary used as the system and business ontology for generated artifacts.
- Apply Necronomicon-first linking for glossary terms: always try to link to already defined Necronomicon concepts before creating new terms.
- After each approved `invoke` stage, transport approved definitions and context deltas into Necronomicon context.

## Non-Goals

- No direct code implementation.
- No full local CLI runtime in the first pass.
- No replacement of existing specialist commands.
- No replacement of `spellcraft` or `sigil-development` lifecycle ownership.

## Design Principles

1. Keep wording generic and plain-language.
2. Do not require specialized graph vocabulary.
3. Ask one focused interview question at a time when context is missing.
4. Prefer local repository templates as canonical.
5. Keep each stage auditable with explicit outputs and gates.
6. Do not silently edit upstream artifacts.
7. Reuse existing Necronomicon concepts before introducing new glossary concepts.
8. After each approved stage, complement Necronomicon context with approved outputs.

## Decided Outcomes

1. Template set is broad and generic:
    - Top-level template inventory is implemented at `arcanum/spells/invoke/templates/README.md`.
    - Module Formulae composable starter bundle is implemented at `arcanum/spells/invoke/templates/module-formulae/`.
    - Standalone invoke implementation-layering template is implemented at `arcanum/spells/invoke/templates/implementation-layering.md`.
    - Standalone invoke work-pack template is implemented at `arcanum/spells/invoke/templates/work-pack.md`.
    - Dedicated candidate family scaffolds are implemented under `arcanum/spells/invoke/templates/` for `generic`, `research`, `architecture`, `implementation-plan`, `spell`, `sigil`, and `ux-plan`.
    - Composable profile routing is defined by `bundle-profile.md` across discovery, architecture, implementation, and full profiles.
2. Template authority is local-first:
   - active canonical templates live in local inventory,
   - library templates are starters/examples.
3. No-model behavior:
   - `invoke` runs structured interview,
   - proposes artifact bundle options,
   - requires approval,
   - creates local template candidate,
   - candidate remains non-canonical until promoted.
4. Architecture gate:
   - prefer approved spec,
   - allow discovery mode for vague goals,
   - route missing spec needs back into define stage.
5. Plan mode output:
   - low complexity: single-file work-pack,
   - medium/high complexity: split work-pack.
6. Mutation governance:
   - downstream stages emit patch requests,
   - direct upstream edits require explicit approval.
7. Required architecture views:
   - context,
   - high-level structure,
   - low-level components,
   - workflow/process,
   - decision flow,
   - dependency/interface map.
8. Glossary ownership:
   - `invoke` maintains its own glossary,
   - glossary terms are used as the system and business ontology baseline,
   - spec, design, and work-pack outputs must align to glossary terminology,
   - glossary creation follows Necronomicon-first concept linking.
9. Stage-to-Necronomicon transport:
   - after any approved stage (`define`, `design`, `plan`), `invoke` transports approved definitions into Necronomicon context,
   - transport should append or complement existing Necronomicon context by default,
   - transport actions should emit per-stage reports.
10. Necronomicon baseline linkage:

- after release, `necronomicon` should route `implementation-research` handoffs and lifecycle authoring requests (`define`, `design`, `plan`, `full`, `validate`) through `invoke` when installed,
- missing `invoke` should be surfaced as a capability gap with installation guidance.

11. Default Necronomicon transport policy:

- approved `invoke` stages append structured transport reports under `.arcanum/necronomicon/sessions/<session-id>/invoke-transports/`,
- active session summaries or memory files are complemented only when a matching section already exists,
- transports do not overwrite existing context or promote authoritative concepts without explicit approval.

12. Default glossary linking heuristic:

- normalize term labels and known aliases before matching,
- mark a term `linked` only when it exactly matches an existing Necronomicon canonical concept or alias,
- mark a term `partial` only when explicit evidence references an existing concept but the label or alias does not exactly match,
- otherwise mark the term `no-match` and record the rationale.

13. Glossary candidate promotion authority:

- `invoke` records candidate terms, partial matches, conflicts, evidence, and recommended next action,
- canonical promotion requires explicit approval through `decision-gate` or the relevant `ontology-vault` promotion flow,
- unresolved conflicts do not silently block artifact generation unless they affect acceptance criteria or traceability labels.

14. Default Necronomicon lifecycle route preset:

- route preset ID is `lifecycle-authoring`,
- selected route target is `invoke`,
- trigger phrases cover `define`, `design`, `plan`, `full`, `validate`, implementation planning, architecture planning, work-pack creation, artifact validation, and implementation-research handoffs,
- when `invoke` is missing, the preset reports a capability gap and installation guidance instead of routing to an ad hoc lifecycle handler.

15. Default plan complexity threshold:

- low complexity requires 5 or fewer tasks, 2 or fewer output artifacts, no cross-repository changes, no runtime or durable-state migration, and no unresolved blocker gates,
- any scope exceeding one or more low-complexity limits is medium or high complexity and uses a split work-pack,
- high complexity is flagged when medium-complexity work also has cross-team ownership, irreversible migration risk, or multiple unresolved gate dependencies.

16. Local template promotion rule:

- candidate templates become canonical only after validation passes, at least one example exists, required inputs and outputs are documented, and the candidate has either been used in an approved stage or reviewed as equivalent to an approved-stage need,
- promotion still requires explicit approval and a recorded decision snapshot,
- failed validation or missing examples keep the template in candidate status.

17. Template recommendation policy:

- `invoke` first filters templates by mode/profile applicability, required input availability, output contract coverage, and authority status,
- if exactly one eligible template remains, select it and record the eligibility evidence,
- if multiple eligible templates remain, ask the user to choose instead of using a hidden weighted score,
- if no eligible template exists, propose a local candidate template with required evidence and validation gaps.

18. Initial template validation example coverage:

- each initial template needs one passing example,
- each profile family needs one missing-input negative example,
- registry release remains blocked when required validation examples are missing.

## Spell Overview

| Spell    | Core Outcome                                                           | Primary Inputs                                                          | Primary Outputs                                                                                                      |
| -------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `invoke` | Produce spec + glossary + design + work-pack through one governed flow | goal, constraints, evidence, optional existing artifacts, selected mode | spec artifact, glossary artifact, design bundle, work-pack, decisions, unresolved gaps, Necronomicon context updates |

## Compose Map

### Required Capabilities

- `structured-interview-kits`
- `inventory`
- `context-builder`
- `decision-gate`
- `implementation-readiness`

### Conditional Capabilities

- `architecture-pattern-inventory` when design bundle is requested.
- `task-session` when handoff needs bounded execution planning.
- `spellcraft` when the generated work-pack targets reusable or local spell creation, revision, validation, observation, or reflection.
- `sigil-development` when the generated work-pack targets sigil creation, revision, observability, or reflection.

## Authoring Handoff Policy

`invoke` owns the lifecycle authoring setup: it can define the goal, glossary, design bundle, work-pack, decisions, gates, and Necronomicon context transport for a requested artifact.

`invoke` does not own spell or sigil lifecycle execution. When the target artifact is a spell, the next route is `spellcraft` with the `invoke` outputs as handoff context. When the target artifact is a sigil, the next route is `sigil-development`, optionally preceded by `skill-decomposer` or `skill-transcriptor` when source material needs decomposition or conversion.

This keeps `invoke` generic while preserving existing Arcanum lifecycle authorities:

- `invoke`: define/design/plan/validate artifact intent and handoff context,
- `spellcraft`: design, install, validate, observe, reflect, and revise spells,
- `sigil-development`: create, update, observe, reflect, and iterate sigils.

## Shared Artifact Contracts

### 1. Spec Contract

Every generated spec should include:

- objective,
- scope,
- out-of-scope,
- actors,
- core workflows,
- constraints,
- acceptance criteria,
- assumptions,
- unresolved questions,
- evidence references,
- decision snapshots.

### 2. Template Entry Contract (Local Inventory)

Each template entry should include:

- `template_id`,
- `template_type`,
- `applies_to`,
- `required_inputs`,
- `optional_inputs`,
- `output_files`,
- `version`,
- `status` (`candidate` or `canonical`),
- `authority_level`,
- `promotion_evidence`,
- `promotion_decision`,
- `examples`,
- `validation_rules`,
- `validation_examples`,
- `selection_evidence`,
- `created_at`,
- `updated_at`.

### 3. Glossary Contract (System and Business Ontology)

The glossary should include:

- `term`,
- `category` (`business`, `system`, or `shared`),
- `definition`,
- `source_or_rationale`,
- `linked_necronomicon_concepts`,
- `link_status` (`linked`, `partial`, or `no-match`),
- `no_match_reason` (required when `link_status = no-match`),
- `usage_references` (spec/design/work-pack sections),
- `status` (`candidate` or `canonical`),
- `promotion_gate` (`not-required`, `decision-gate`, or `ontology-vault`),
- `conflict_status` (`none`, `suspected`, or `confirmed`),
- `created_at`,
- `updated_at`.

Glossary linking order should be deterministic:

1. Normalize the proposed term label and available Necronomicon canonical labels and aliases.
2. If an exact canonical-label or alias match exists, set `link_status = linked` and reuse that concept language.
3. If explicit cited evidence points to an existing concept but the label or alias does not exactly match, set `link_status = partial` and record the evidence reference.
4. If no exact or evidence-backed partial match exists, create a candidate term, set `link_status = no-match`, and record `no_match_reason`.
5. If promotion or conflict resolution is needed, set `promotion_gate` to `decision-gate` or `ontology-vault`; do not promote the term to canonical inside `invoke` without that explicit approval.

### 4. Architecture Bundle Contract

Every design bundle should include:

- required view set,
- assumptions,
- open design risks,
- unresolved decisions,
- downstream planning notes.

### 5. Work-Pack Contract

Every work-pack should include:

- objective,
- complexity,
- complexity factors and threshold result,
- selected output mode,
- tasks and/or waves,
- traceability links,
- gate checks,
- blockers,
- closure strategy.

### 6. Necronomicon Context Transport Contract

Every approved stage transport should include:

- `stage_id`,
- `approval_reference`,
- `definitions_transported`,
- `context_paths_updated`,
- `merge_mode` (`append` or `complement`),
- `transport_status`,
- `transport_timestamp`,
- `unresolved_transport_gaps`.

Default transport paths and merge rules:

- append stage reports to `.arcanum/necronomicon/sessions/<session-id>/invoke-transports/<stage-id>.md`,
- complement matching sections in `.arcanum/necronomicon/sessions/<session-id>/SESSION.md` or `memory.md` only when those sections already exist,
- record any missing matching section as an unresolved transport gap instead of creating or overwriting upstream context silently.

## Invoke Contract

## Identity

- Canonical ID: `invoke`
- Scope: library spell
- Purpose: unify define, design, and planning workflows behind one generic contract.

## Trigger Conditions

- User has something to build but needs structure before implementation.
- Existing artifacts are incomplete, inconsistent, or missing.

## Modes

- `define`: produce or update spec artifact.
- `design`: produce architecture/design bundle.
- `plan`: produce executable work-pack.
- `full`: run `define`, `design`, and `plan` in sequence with gates.
- `validate`: validate existing artifacts and report gaps.

## Input Contract

`invoke` accepts:

- goal,
- optional mode,
- optional existing artifacts,
- constraints,
- required output depth,
- approval preferences.

## Phase Contract

### Phase 0 - Baseline Check

- detect existing local templates,
- detect existing spec/glossary/design/work-pack artifacts,
- load existing Necronomicon concept sources for term matching,
- detect missing mandatory inputs for selected mode.

### Phase 1 - Clarify Intent

- if context is missing, run one-question-at-a-time interview,
- generate recommended artifact bundle,
- capture approval decision.

### Phase 2 - Define (Spec)

- select local canonical template or create candidate,
- generate spec artifact,
- generate or update glossary artifact,
- for each glossary term, run Necronomicon-first concept linking,
- record assumptions and unresolved gaps,
- write template usage to inventory,
- after define-stage approval, transport approved spec and glossary definitions to Necronomicon context.

### Phase 3 - Design (Architecture)

- use approved spec when available,
- enforce glossary term consistency for system and business language,
- in discovery mode, produce design brief and spec gap requests,
- generate six required views,
- record architecture gaps,
- after design-stage approval, transport approved design context to Necronomicon.

### Phase 4 - Plan (Work-Pack)

- determine complexity using the default low/medium/high threshold rubric,
- select single or split mode,
- preserve upstream implementation-research handoff references when plan mode is entered from Necronomicon,
- use glossary terms for task naming and traceability labels,
- build tasks/waves and gate checks,
- route unresolved blockers to decision-gate,
- after plan-stage approval, transport approved work-pack context to Necronomicon.

### Phase 5 - Finalize

- publish outputs,
- write decision snapshots,
- write glossary candidate and conflict notes,
- write unresolved Necronomicon no-match terms for later promotion review,
- reconcile per-stage Necronomicon transport reports,
- write unresolved gap ledger,
- return next recommended route.

## Output Contract

`invoke` returns:

- artifact paths by mode,
- selected templates and status,
- glossary path and term updates,
- design views generated,
- work-pack mode and gate status,
- decisions recorded,
- Necronomicon transport report by stage,
- Necronomicon context paths updated,
- unresolved gaps,
- next route recommendation.

## Governance Rules

1. No silent upstream mutation.
2. Direct edits to upstream artifacts require explicit approval.
3. Candidate templates cannot auto-promote to canonical.
4. `full` mode stops on blocked gates and returns remediation guidance.
5. Glossary is the terminology source for system and business ontology in all `invoke` outputs.
6. Glossary terms must always attempt Necronomicon-first linking before creating new candidate concepts.
7. Candidate glossary terms and conflicts require `decision-gate` or `ontology-vault` approval before canonical promotion.
8. Any approved stage must transport approved definitions/context into Necronomicon.
9. Stage transport should append or complement existing Necronomicon context unless explicit overwrite approval is provided.
10. `invoke` must remain discoverable as a baseline Necronomicon route for implementation-research handoff and lifecycle authoring requests.
11. Spell and sigil authoring handoffs must route to `spellcraft` or `sigil-development`; `invoke` must not copy or redefine their internal contracts.

## Interrogation Decisions

| Decision                                    | Selected Option                                                                                                                                                                                                        | Rejected Alternatives                                                                                                                            | Rationale                                                                                                       | Plan Impact                                                                                                                                                                     |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Default Necronomicon transport policy       | Session-scoped append plus summary complement. Approved `invoke` stages append structured reports under the active Necronomicon and complement matching session summaries only when a matching section exists. | Central invoke context ledger; artifact-local transport reports only; deferring transport defaults to Wave 5 validation.                         | This keeps approved stage transport auditable while preserving the no-silent-upstream-mutation rule.            | Waves 2, 3, 4, and 5 must emit per-stage transport reports under `.arcanum/necronomicon/sessions/<session-id>/invoke-transports/` and report missing matching sections as gaps. |
| Default glossary linking heuristic          | Conservative exact-or-alias first. Normalized exact canonical-label or alias matches become `linked`; evidence-backed non-exact matches become `partial`; all other terms become `no-match` with rationale.            | Tiered lexical plus definition overlap; ontology-vault delegated matching for all ambiguity; deferring the heuristic to a later validation wave. | This avoids weak automatic links while still allowing explicitly evidenced partial matches.                     | Wave 2 must implement deterministic term normalization, exact-or-alias matching, partial evidence recording, and no-match rationale output.                                     |
| Glossary candidate promotion authority      | Record only with explicit promotion gate. `invoke` records candidates, conflicts, evidence, and next action; canonical promotion requires `decision-gate` or `ontology-vault` approval.                                | Promote after stage approval; promote after repeated approved use; defer promotion rules.                                                        | This keeps terminology evidence useful without letting approved stage artifacts silently canonize new concepts. | Wave 2 must write promotion gate and conflict status fields, and Phase 5 must preserve unresolved promotion actions in the gap ledger.                                          |
| Default Necronomicon lifecycle route preset | Single `lifecycle-authoring` preset targeting `invoke` for define/design/plan/full/validate requests and implementation-research handoffs.                                                                             | One preset per invoke mode; implementation-research only first; defer route preset naming.                                                       | A single preset keeps lifecycle authoring discoverable while preserving explicit mode dispatch inside `invoke`. | Wave 6 must register examples against `lifecycle-authoring`, and validation must cover missing-`invoke` capability gap behavior.                                                |
| Default plan complexity threshold           | Conservative low-complexity rubric. Single-file work-packs require 5 or fewer tasks, 2 or fewer artifacts, no cross-repository changes, no runtime or durable-state migration, and no unresolved blocker gates.        | Task-count only threshold; always split unless explicitly trivial; defer complexity thresholds.                                                  | This keeps compact work-packs available without hiding coordination or migration risk.                          | Wave 4 must emit complexity factors, threshold result, and selected output mode for every plan run.                                                                             |
| Local template promotion rule               | Explicit approval after validation evidence. A candidate needs passing validation, at least one example, documented inputs/outputs, approved-stage use or equivalent review, and an explicit promotion decision.       | Promote after first approved use; promote after repeated approved use; defer promotion rules.                                                    | This preserves local template authority without letting candidates linger without a path to reuse.              | Wave 2 must record promotion evidence and promotion decision fields in template inventory entries.                                                                              |
| Template recommendation policy              | Eligibility filter with user choice on ties. `invoke` selects a single eligible template only when the evidence leaves exactly one match; otherwise it asks the user to choose among eligible templates.               | Weighted rubric with deterministic tie-breakers; strict rule cascade; defer scoring model.                                                       | This avoids false precision when multiple templates legitimately fit the request.                               | Wave 2 must emit eligibility evidence, option cards for multiple matches, and candidate-template gaps when no match exists.                                                     |
| Initial template validation examples        | Per-template passing example plus per-profile negative example. Every initial template has one passing example, and each profile family has one missing-input negative example.                                        | Profile-level examples only; Module Formulae examples only; defer validation examples.                                                           | This gives validation enough behavioral coverage without overbuilding the first release.                        | Wave 7 must fail registry release when required validation examples are missing.                                                                                                |

## Remaining Release Gates

- No template-family scaffold gaps remain relative to the declared invoke taxonomy.
- Dedicated family scaffolds remain candidate templates until validation evidence and explicit promotion approval are recorded.
- Registry release remains blocked until required validation examples pass for each required initial template or profile family.

## Implementation Waves

### Wave 0 - Baseline Audit

- inspect existing templates and work-pack examples,
- map overlaps with current capabilities.

### Wave 1 - Spell Contract Finalization

- finalize `invoke` identity, modes, phase contract, gates, and output contract.

### Wave 2 - Template and Spec Stage

- implement `define` stage contract,
- implement local template retrieval and candidate creation policy,
- validate Module Formulae starter bundle defaults under `arcanum/spells/invoke/templates/module-formulae/`,
- validate standalone implementation-layering defaults under `arcanum/spells/invoke/templates/implementation-layering.md` and standalone work-pack defaults under `arcanum/spells/invoke/templates/work-pack.md`,
- validate dedicated family scaffolds under `arcanum/spells/invoke/templates/generic/`, `arcanum/spells/invoke/templates/research/`, `arcanum/spells/invoke/templates/architecture/`, `arcanum/spells/invoke/templates/implementation-plan/`, `arcanum/spells/invoke/templates/spell/`, `arcanum/spells/invoke/templates/sigil/`, and `arcanum/spells/invoke/templates/ux-plan/`,
- validate composition mapping from implementation profile outputs,
- validate composable profile mapping in `bundle-profile.md` for define/design/plan/full/validate modes,
- implement define-stage approved transport to Necronomicon.

### Wave 3 - Design Stage

- implement `design` stage contract in `arcanum/spells/invoke/design.md`,
- consume approved define outputs: spec artifact, glossary artifact, template selection evidence, decisions, unresolved gaps, optional layering seed/gap, and define transport report,
- use Module Formulae `architecture` profile as the normal design bundle route,
- enforce six required architecture views: context, high-level structure, low-level components, workflow/process, decision flow, and dependency/interface map,
- compose the dedicated `architecture` family when source contracts, dependency/interface rules, decision log, risks, and design transport notes need fuller structure,
- compose the `research` family before final design when evidence is absent, contradictory, or insufficient for an architecture decision,
- compose the `ux-plan` family when workflow, surface, state, content, accessibility, or interaction risk materially affects architecture,
- emit spellcraft or sigil-development handoff context when the target artifact is a spell or sigil, without taking lifecycle ownership,
- implement discovery-mode design brief behavior only after explicit approval, and route missing spec work back to `define`,
- emit glossary consistency report and route conflicts without silent glossary promotion,
- seed or gap-record implementation layering while keeping full layering required only for `plan`, `full`, and `validate`,
- emit source design refs for `implementation-plan` without creating work-pack tasks,
- implement design-stage approved transport to Necronomicon.

### Wave 4 - Plan Stage

- implement `plan` stage contract,
- implement adaptive output mode,
- implement blocker routing,
- implement plan-stage approved transport to Necronomicon.

### Wave 5 - Full and Validate Modes

- implement `full` orchestration,
- implement `validate` mode reporting,
- verify stage gates and stop conditions,
- verify per-stage transport reporting and merge behavior.

### Wave 6 - Registry and Examples

- register `invoke` in spell registry,
- add examples for each mode.

### Wave 7 - Validation

- run spell contract validation,
- run markdown link checks,
- run schema checks,
- validate one passing example per initial template,
- validate one missing-input negative example per profile family,
- execute representative scenarios.

## Validation Matrix

| Check                                                    | Expected Result                                                                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `invoke define` from vague goal                          | interview runs, template selected or candidate created, governed spec emitted                                                         |
| Module Formulae template bundle availability             | local inventory can resolve defaults from `arcanum/spells/invoke/templates/module-formulae/`, resolve standalone implementation-layering from `arcanum/spells/invoke/templates/implementation-layering.md`, resolve standalone work-pack from `arcanum/spells/invoke/templates/work-pack.md`, and map terms via `vocabulary-map.md`                  |
| Dedicated invoke family scaffolds                        | local inventory can resolve `generic`, `research`, `architecture`, `implementation-plan`, `spell`, `sigil`, and `ux-plan` families with primary templates and passing/missing-input examples |
| Module Formulae composable profiles                      | `bundle-profile.md` maps invoke modes to discovery/architecture/implementation/full bundles with deterministic selection rules        |
| Initial template validation examples                     | every initial template has one passing example and each profile family has one missing-input negative example before registry release |
| `invoke define` glossary output                          | glossary is created/updated and includes business + system terms with status and references                                           |
| Necronomicon-first glossary linking                      | each glossary term links to an existing Necronomicon concept when available; no-match terms include rationale                         |
| `invoke define` transport                                | after define approval, approved spec/glossary definitions are transported to Necronomicon context                                     |
| `invoke design` from approved spec                       | six required views emitted, architecture gaps recorded                                                                                |
| `invoke design` missing source contracts                 | blocks unless discovery mode is explicitly approved                                                                                   |
| Glossary consistency in design                           | design bundle uses glossary terminology and reports term conflicts                                                                    |
| `invoke design` with evidence ambiguity                  | composes research companion and carries claim status into design decisions                                                            |
| `invoke design` with workflow or surface risk            | composes UX-plan companion and records handoff boundaries                                                                             |
| `invoke design` for spell or sigil target                | emits handoff context and routes lifecycle execution to `spellcraft` or `sigil-development`                                           |
| `invoke design` transport                                | after design approval, approved design context is transported and complemented in Necronomicon                                        |
| `invoke design` from vague goal                          | discovery brief emitted, spec gap requests recorded                                                                                   |
| `invoke plan` low complexity                             | single-file work-pack emitted                                                                                                         |
| `invoke plan` medium/high complexity                     | split work-pack emitted with waves/tasks/shared context                                                                               |
| Glossary consistency in work-pack                        | task labels and traceability names align with glossary terms                                                                          |
| `invoke plan` transport                                  | after plan approval, approved work-pack context is transported and complemented in Necronomicon                                       |
| Necronomicon implementation-research handoff to `invoke` | when installed, handoff routes to `invoke` as baseline authoring spell; when missing, capability gap and install path are reported    |
| Transport merge policy                                   | stage transports append/complement existing Necronomicon context and do not overwrite without explicit approval                       |
| `invoke full` with blocker                               | execution stops at gate and returns remediation guidance                                                                              |
| Upstream mutation policy                                 | no silent edits; explicit approval required for upstream changes                                                                      |
| Local template authority                                 | local inventory resolves canonical active templates                                                                                   |

## Acceptance Criteria

1. One spell (`invoke`) covers define/design/plan lifecycle with explicit modes.
2. Generic contract avoids specialized graph-vocabulary dependencies.
3. Shared artifact schemas are documented and testable.
4. Stage handoffs are deterministic and auditable.
5. No direct implementation mutation occurs.
6. Glossary is generated and used as system/business ontology across outputs.
7. Necronomicon-first linking is enforced for glossary terms, with explicit no-match rationale when needed.
8. Any approved `invoke` stage transports approved definitions/context into Necronomicon with per-stage reports.
9. Module Formulae starter template bundle and standalone implementation-layering/work-pack templates are available and resolvable for default `invoke` template selection.
10. Dedicated candidate family scaffolds exist for generic, research, architecture, implementation-plan, spell, sigil, and ux-plan routes.
11. Registry entry is added only after validation passes.
12. After release, `invoke` is treated as the baseline Necronomicon route for implementation-research handoffs and lifecycle authoring requests.
13. Design mode is implemented as an L1 contract that emits six-view architecture artifacts, glossary consistency status, and plan-ready source design refs without creating work-pack tasks.
