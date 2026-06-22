# Invoke Design Mode

## Identity

- Spell: `invoke`
- Mode: `design`
- Status: implemented (L1 contract, validation examples pending)

## Purpose

Design mode converts approved define outputs into a governed architecture/design bundle with explicit source contracts, glossary consistency checks, design decisions, risks, dependency/interface notes, and plan-ready handoff context.

Design mode is non-mutating: it does not silently edit upstream spec, glossary, or Necronomicon context. Upstream corrections become patch requests, blocker decisions, or explicit gap-ledger entries.

## Implementation Coverage

- The L1 design contract is implemented as a mode-level governance contract.
- The authoritative six-view design baseline is the DomainSpec architecture profile and [templates/domainspec-spec/architecture-bundle.md](templates/domainspec-spec/architecture-bundle.md).
- Dedicated candidate family scaffolds for `architecture`, `research`, `ux-plan`, `spell`, and `sigil` are available as design companions.
- Runtime execution, registry release, and canonical template promotion remain gated by validation evidence and explicit approval.

## Activation Gate

Normal design mode requires:

- approved and stable define outputs,
- explicit design-stage constraints,
- source contracts or approved discovery mode,
- lifecycle owner approval for L1 design work,
- template/profile selection evidence.

Discovery-mode design is allowed only when the user explicitly approves a limited architecture brief without approved define outputs.

## Required Sigils

| Sigil | Role In Mode | Required Mode |
| --- | --- | --- |
| `context-builder` | Build bounded design context from define outputs, constraints, and existing artifacts. | lean or standard |
| `structured-interview-kits` | Clarify missing design inputs one question at a time and capture approvals. | gap-check or equivalent one-question interview mode |
| `inventory` | Resolve architecture profile/templates and record selection evidence. | lookup, ingest, validate |

## Optional Sigils

| Sigil | Use When | Notes |
| --- | --- | --- |
| `architecture-pattern-inventory` | Existing patterns, reusable architectures, or design alternatives need lookup. | Supplies evidence; does not override design gates. |
| `decision-gate` | A blocker-level design decision cannot be resolved from available evidence. | Route only consequential unresolved choices. |
| `distill` | A draft design needs unit-size validation, split pressure analysis, or gap discovery before plan handoff. | Run a design-unit check and record `pass`, `flag`, or `block` unless design blocks before material exists. |
| `spellcraft` | Approved design output targets spell authoring or spell revision. | Invoke emits handoff context; Spellcraft owns spell lifecycle mutation, validation, install/adaptation, observation, and reflection. |
| `sigil-development` | Approved design output targets sigil authoring or sigil revision. | Invoke emits handoff context; Sigil Development owns sigil lifecycle mutation, validation, observability, reflection, and promotion readiness. |

## Inputs

Normal design inputs:

- approved spec artifact path,
- approved glossary artifact path,
- define context summary,
- template selection evidence,
- define decision and gap ledger,
- design constraints,
- source contracts,
- optional existing implementation-layering seed or gap.

Discovery-mode inputs:

- user goal and scope hints,
- explicit discovery-mode approval,
- source evidence boundary,
- known constraints,
- required output depth.

Optional companion inputs:

- research question and source scope,
- user goals, workflow scope, and target actors,
- existing interfaces,
- target artifact type (`spell`, `sigil`, or neutral),
- Necronomicon concept sources for glossary consistency checks.

## Template And Profile Selection

| Selection | Use When | Required Output |
| --- | --- | --- |
| DomainSpec architecture profile | Normal design from approved define outputs. | architecture bundle with the six required views. |
| `architecture` family | Design needs source contracts, dependency/interface rules, decision log, risks, and design transport notes. | architecture plan artifact. |
| `research` family | Evidence is absent, contradictory, or insufficient for an architecture decision. | research brief with claim status and unresolved gaps. |
| `ux-plan` family | User workflow, surfaces, states, content, accessibility, or interaction risk materially affect architecture. | UX plan and handoff boundaries. |
| `spell` family | Target artifact is a spell. | spellcraft handoff context only. |
| `sigil` family | Target artifact is a sigil. | sigil-development handoff context only. |

The six required design views are:

1. Context view.
2. High-level structure view.
3. Low-level components view.
4. Workflow process view.
5. Decision flow view.
6. Dependency interface view.

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1 | `context-builder` | approved define outputs, constraints, existing artifacts | bounded design context | mandatory design inputs are identified | block on contradictory scope or missing core goal |
| 2 | `structured-interview-kits` | bounded design context | approved design intent and missing-input decisions | one-question cadence and explicit approvals captured | block on unresolved blocker ambiguity |
| 3 | `inventory` | approved design intent and local template inventory | architecture profile/template selection record | eligibility evidence is explicit and tie cases request user choice | flag when candidate template is usable but not promoted |
| 4 | optional `architecture-pattern-inventory` | design intent, source contracts, pattern question | pattern evidence and alternatives | evidence is cited and alternatives are bounded | flag when pattern evidence is unavailable but local design can proceed |
| 5 | optional `research` companion | evidence gap or contradiction | research brief and claim status | research question and source scope are present | block when evidence gap affects required design decision |
| 6 | optional `ux-plan` companion | workflow, actor, surface, or accessibility risk | UX plan and handoff boundaries | workflow scope and target actors are present or inferable | flag on non-blocker UX gaps; block on unknown core actor/workflow |
| 7 | `invoke design` | approved intent, template/profile record, companion evidence | architecture bundle, optional architecture plan, glossary consistency report, risks, decisions, dependency/interface map, planning handoff notes, optional layering seed or gap, design transport report | six views, glossary consistency, no-silent-upstream-mutation, and transport rules are satisfied | block on violated governance rule; otherwise return partial with unresolved gaps |
| 8 | optional `decision-gate` | unresolved design blocker | decision record and next route | blocker resolved or explicitly deferred | keep blocker in gap ledger with recommended next action |
| 9 | optional handoff (`spellcraft`, `sigil-development`, or `plan`) | approved design outputs | lifecycle-authoring or plan-mode handoff context | target route is explicit and accepted | defer handoff if target authority is unavailable |

## Mode Gates

- Normal design blocks without approved define outputs unless discovery mode is explicitly approved.
- Source contracts are required unless discovery mode is approved.
- Template/profile selection must include eligibility evidence and explicit user choice on tie cases.
- The design output must include the six required design views or block.
- Glossary consistency must be checked against define glossary terms; conflicts are recorded and routed instead of silently promoted.
- Design mode may emit an implementation-layering seed or record a layering gap; full layering artifacts remain required only for `plan`, `full`, and `validate`.
- Design mode must not create work-pack tasks, execution-pack waves, or mutation-ready implementation steps.
- Candidate templates, glossary terms, registry entries, and Necronomicon concepts are never promoted automatically.
- Design-stage transport appends stage reports and complements matching Necronomicon sections only when they already exist.
- Spell and sigil lifecycle work routes to `spellcraft` or `sigil-development`; design only prepares handoff context.
- Design mode must record a Dispatch Spec technique trace that names the techniques used to justify profile/template selection, companion evidence, owner boundaries, and next route.
- Design mode must run a design-unit Distill check unless it blocks before design material exists; the result must identify the coherent unit, split pressure, and any gaps that affect plan readiness.
- A `flag` or `block` Distill result routes to `define`, design follow-up, or deferred follow-up; it must not silently advance to `plan`.

## Handoff Artifacts

- design context summary,
- architecture bundle path,
- optional architecture plan path,
- glossary consistency report,
- source contract list,
- dependency/interface map,
- design decision log,
- risk and unresolved gap ledger entries,
- Dispatch Spec technique trace,
- Distill validation status and rationale,
- optional research brief path,
- optional UX plan path,
- implementation-layering seed path or explicit layering gap,
- design transport report,
- source design refs for implementation-plan,
- context-builder-readiness notes for downstream plan when runtime handoff may be used,
- recommended next route (`plan`, `define`, `spellcraft`, `sigil-development`, or deferred follow-up).

## Observability

When `.arcanum/observability/` exists, record:

- spell name and mode,
- phases attempted,
- sigils invoked,
- selected profile/templates,
- six-view coverage status,
- glossary consistency status,
- gates passed, flagged, or blocked,
- artifact paths produced,
- transport status,
- unresolved gaps and blocker decisions,
- next route recommendation.

## Mode Output Contract

Return:

```markdown
## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: spells/invoke/design.md
- Outputs: <architecture bundle path>, <architecture plan path | n/a>, <glossary consistency report path>, <transport report path>
- Design views: context | high-level structure | low-level components | workflow process | decision flow | dependency interface
- Template/profile selection: <selected profile and companion templates>
- Dispatch techniques: <technique ids and rationale>
- Distill validation: pass | flag | block | not applicable; <rationale>
- Implementation layering: <seed path | gap recorded | n/a>
- Work-pack: n/a
- Decisions: <summary>
- Unresolved gaps: <summary>
- Next route: plan | define | spellcraft | sigil-development | deferred
```
