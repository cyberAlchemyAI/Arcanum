# Invoke Design Mode

## Identity

- Spell: `invoke`
- Mode: `design`
- Status: implemented (L1 contract with deterministic selection validation)

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
- a closed `DesignScopeManifest` bound to exact target and source selectors,
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
- exact target footprint, declared field classes, exclusions, and author
  identity for `DesignScopeManifest`,
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
| `ux-plan` family | A natural person reads, decides, acts, recovers, navigates, or performs assistive operation through a new or changed rendered semantic contract. | UX plan and handoff boundaries. Backend files, APIs, receipts, or style-only changes do not select UX by themselves. |
| `spell` family | Target artifact is a spell. | spellcraft handoff context only. |
| `sigil` family | Target artifact is a sigil. | sigil-development handoff context only. |

The six required design views are:

1. Context view.
2. High-level structure view.
3. Low-level components view.
4. Workflow process view.
5. Decision flow view.
6. Dependency interface view.

## Design Selection Protocol

The six views remain mandatory navigation, but they are not a completeness
proof. Normal Design validation uses three versioned public contracts:

1. the Design author closes `DesignScopeManifest`, including every declared
   field class, exact selectors and digests, evidence-backed exclusions, an
   empty `unknowns` set, and an author identity distinct from the detector;
2. `invoke-design-scope-extractor` inspects only those exact selectors and
   emits `DesignDenominatorReceipt`; it cannot select companions or validate
   its own receipt;
3. `invoke-design-selection-validator` unions authored concerns with extracted
   signals, binds every signal to one primary concern, resolves all ownership
   roles, assigns one of four dispositions, and emits
   `DesignSelectionResult`;
4. selection repeats once from the same immutable manifest and denominator.
   Any changed concern, owner, disposition, output, diagnostic, or digest
   blocks with `CHANGED_PASS_TWO`; there is no implicit third pass.

The four dispositions are `required`, `recommended`,
`not-applicable-with-rationale`, and `block`. Only `required` selects an output.
N/A requires detector-negative evidence selectors. Missing input, unknown
scope, stale/self-issued receipt, unbound signal, unresolved owner, illegal
selection, or a changed second pass blocks.

Evidence states are separate:

- `authored-complete` means the Design and planned witness contracts exist;
- `design-validator-pass` means exact manifest, denominator, ownership,
  selection, and fixed-point checks passed;
- `plan-evidence-pending|pass|fail` belongs to Plan receipts and is never a
  `DesignSelectionResult` value.

An `authored-complete` Design may route only to a remediation Plan whose
declared purpose is to materialize the missing Design validator or fixtures.
Normal implementation planning requires `design-validator-pass`, begins at
`plan-evidence-pending`, and validates its own runnable witnesses.

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| --- | --- | --- | --- | --- | --- |
| 1 | `context-builder` | approved define outputs, constraints, existing artifacts | bounded design context | mandatory design inputs are identified | block on contradictory scope or missing core goal |
| 2 | `structured-interview-kits` | bounded design context | approved design intent and missing-input decisions | one-question cadence and explicit approvals captured | block on unresolved blocker ambiguity |
| 3 | `inventory` | approved design intent and local template inventory | architecture profile/template selection record | eligibility evidence is explicit and tie cases request user choice | flag when candidate template is usable but not promoted |
| 4 | optional `architecture-pattern-inventory` | design intent, source contracts, pattern question | pattern evidence and alternatives | evidence is cited and alternatives are bounded | flag when pattern evidence is unavailable but local design can proceed |
| 5 | optional `research` companion | evidence gap or contradiction | research brief and claim status | research question and source scope are present | block when evidence gap affects required design decision |
| 6 | Design scope extractor | closed `DesignScopeManifest` and repository root | current `DesignDenominatorReceipt` | every selector is in-root, readable, digest-matched, and independently detected | block with exact missing/stale/self-issued/unbound diagnostic |
| 7 | Design selection validator | manifest, denominator, authored concerns, predicate config, planned witness contracts | two-pass `DesignSelectionResult` | total binding, exact owners, legal dispositions/outputs, and fixed point pass | block without partial pass; preserve `authored-complete` |
| 8 | optional `ux-plan` companion | validator-selected `ux-plan`, actor, and changed semantic surface | UX plan and handoff boundaries | natural-person plus changed-semantic-contract predicate is true | block when selected UX inputs are incomplete; do not select from keywords |
| 9 | `invoke design` | approved intent, template/profile record, selection receipt, companion evidence | architecture bundle, optional architecture plan, glossary consistency report, risks, decisions, dependency/interface map, planning handoff notes, optional layering seed or gap, design transport report | six views, selection receipt, glossary consistency, no-silent-upstream-mutation, and transport rules are satisfied | block on violated governance rule; otherwise return partial with unresolved gaps |
| 10 | optional `decision-gate` | unresolved consequential design blocker | decision record and next route | blocker resolved or explicitly deferred | keep blocker in gap ledger with recommended next action |
| 11 | optional handoff (`spellcraft`, `sigil-development`, or `plan`) | approved design outputs and selection result | lifecycle-authoring, remediation-Plan, or normal Plan context | normal Plan requires `design-validator-pass`; remediation Plan is explicitly bounded | defer or block when evidence state and route disagree |

## Mode Gates

- Normal design blocks without approved define outputs unless discovery mode is explicitly approved.
- Source contracts are required unless discovery mode is approved.
- Template/profile selection must include eligibility evidence and explicit user choice on tie cases.
- The design output must include the six required design views or block.
- `DesignScopeManifest` must be schema-valid, digest-current, selector-closed,
  authored independently from the detector, and have no unknowns.
- A normal Plan handoff requires a passing `DesignDenominatorReceipt`, total
  `DesignSelectionResult`, and unchanged pass-one/pass-two digests.
- Every concern must name accountable, contributing, artifact, and validator
  owners and use exactly one of the four dispositions.
- Only `required` concerns may appear in `selected_outputs`; false N/A,
  selected recommendations, or unresolved owners block.
- Planned fixtures and validator contracts remain Design artifacts. They never
  count as executed Plan evidence.
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
- Design scope manifest, denominator receipt, and selection result paths,
- Design evidence state and exact evidence ceiling,
- planned fixture and validator contracts, explicitly marked unexecuted,
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
- Design selection receipt path, evidence state, selected output IDs, and
  blocking diagnostics,
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
- Design selection receipt: <DesignSelectionResult path | blocked reason>
- Design evidence state: authored-complete | design-validator-pass
- Evidence ceiling: Design validation only; Plan evidence is separate
- Plan evidence: plan-evidence-pending | n/a for blocked/remediation route
- Template/profile selection: <selected profile and companion templates>
- Dispatch techniques: <technique ids and rationale>
- Distill validation: pass | flag | block | not applicable; <rationale>
- Implementation layering: <seed path | gap recorded | n/a>
- Work-pack: n/a
- Decisions: <summary>
- Unresolved gaps: <summary>
- Next route: plan | define | spellcraft | sigil-development | deferred
```

## Evidence Capability Contract

Active design output must carry `execution_path`, `dispatch_trace`, `source_contracts`,
`template_selection`, `result`, and `next_route` evidence. A conditional Distill skip requires a
rationale. The validator result, not an authored handoff label, controls mutation readiness.
