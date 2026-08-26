# Research Initial Definitions — Craft Ledger Integrity

## Context

Arcanum's Craft capability provides a project-local recursive ledger for keeping
development state explicit and navigable across contexts, artifacts, blockers,
enablers, decisions, gaps, definitions, next moves, validation, and
recomposition. Its canonical package treats `.craft/ledger.yml` as the local
source of truth. That file contains both source rows and required embedded
lookup indexes under `.craft/ledger.yml#indexes`; the indexes are logically
derived from the rows but remain co-located inside the authoritative file. The
optional generated machine index `.craft/index.json` and the human view
`CRAFT.md` are separate, derived, and non-authoritative surfaces. Capabilities
called from Craft retain ownership of their native artifacts and verdicts.

The local problem is that a ledger can describe the right kinds of state and
still cease to correspond to the work it is meant to track. Source rows,
embedded indexes, the generated machine index, the human view, recorded
artifacts, route results, closure state, and next moves may not change together
or may preserve incompatible accounts of the same project state. Resolving this
matters because Craft is useful only when operators and later agents can rely on
its current state without silently promoting route shape, stale projections, or
manually integrated evidence into stronger conclusions.

## Purpose

This document establishes the informational starting point for research into
the integrity of Craft ledger state. The later research will inform a decision
about whether Craft's current contracts are sufficient to keep authoritative
state and derived views aligned, and whether any later contract, validation, or
runtime change is warranted. It does not select a mechanism, prescribe a schema,
authorize implementation, or change Craft's canonical surfaces.

## Research Question (Can be refined)

In which Craft state transitions can source rows and embedded indexes within
the authoritative `.craft/ledger.yml` diverge; when can that ledger diverge from
the optional generated `.craft/index.json`, the derived `CRAFT.md`, or the
native results of called capabilities; which of those divergences belong to
Craft's current responsibility; and what minimum integrity properties must hold
for the recorded state to remain safe to navigate and use?

## Confirmed Product Constraints

- `.craft/ledger.yml` remains the project-local source of truth for Craft state.
  Its required embedded indexes remain lookup data derived from source rows and
  do not independently redefine those rows. The optional `.craft/index.json`
  and `CRAFT.md` remain separate, derived, and non-authoritative surfaces.
- Called capabilities retain ownership of their native artifacts, validation,
  and verdicts. Craft may record their handoffs, receipts, evidence, residue,
  and consequences without silently replacing that authority.
- Route-shape validation is not execution evidence, and neither one alone
  licenses a stronger closure or readiness claim than its recorded predicate
  supports.
- Stable row identity, navigable links, required embedded indexes, explicit
  pending state, and recomposition evidence remain part of the current Craft
  contract.
- This research concerns ledger integrity and currency. The separate question
  of whether Craft should gain new claim–evidence concepts remains outside this
  research scope.
- Research claims must remain no stronger than the inspected ledger, schema,
  artifact, receipt, validation, or repository evidence.
- This research is diagnostic. It does not authorize mutation of existing
  ledgers, canonical Craft contracts, schemas, examples, or runtime surfaces.

## Current Evidence Baseline

- `arcana/craft/SKILL.md` defines Craft as a file-backed recursive ledger and
  requires meaningful mutations to preserve links, embedded indexes, pending
  state, evidence boundaries, and recomposition discipline.
- `arcana/craft/ARCHITECTURE.md` records `.craft/ledger.yml` as authoritative and
  explicitly states that Craft does not currently ship a command runner,
  packaged renderer, generated-index builder, deterministic row updater, or
  automated YAML mutation surface.
- `arcana/craft/templates/schemas/ledger-core.schema.yml` defines canonical row
  families, lifecycle enums, references, and validation rules for source-ledger
  state. `arcana/craft/templates/schemas/index.schema.yml` separately defines
  the required embedded-index shape and the larger generated-index contract.
  The formal `active_blockers` filter for `kind=blocker,status=active` appears in
  the generated-index lookup groups; the embedded-index contract requires the
  key but does not separately restate that filter.
- `development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md`
  records an adjacent-workspace use in which produced artifacts, embedded
  indexes, and next moves required manual integration and two manual edits
  temporarily broke YAML parsing. It describes proposed mechanisms, but those
  proposals are not implemented canonical behavior.
- `spells/goal/.craft/ledger.yml` records `BLK-GOAL-SUBMODULE-001` with
  `status: closed`; `closed` is not a canonical typed-item status. This is an
  unequivocal lifecycle-enum violation. The same row remains in the embedded
  `indexes.active_blockers`, so the row lifecycle and embedded lookup disagree
  about whether the blocker is active; the exact normative relationship between
  embedded and generated active-blocker filters remains unresolved. The ledger
  also contains gap rows without the status required by the canonical gap
  contract. These observations establish local inconsistency in that ledger;
  they do not establish its cause or repository-wide prevalence.

### Evidence snapshot

The mutable local evidence above was observed at
`2026-08-25T12:18:36-03:00` against repository commit
`b07a03d95e4c8bd4d98c05a8eb2916ad7f8341d9`. Every source in this table was
tracked and clean at observation time; the baseline itself had not yet been
committed.

| Artifact | Stable selector | Version | SHA-256 |
| --- | --- | --- | --- |
| `arcana/craft/SKILL.md` | `<storage-contract>`, `<linking-and-indexing-contract>`, `<interaction-boundary>`, `<process>` | package contract | `6edb22bd4caa7ff6c8058b8e836817cfa0841522e6f042068d11cca47d075451` |
| `arcana/craft/ARCHITECTURE.md` | `Source Authority`, `Current Schema Stack Boundaries`, `Explicitly Absent Today` | architecture baseline | `f81cca917fe51a2525948a46bcc81be77ccf02fbad2eab8c47be98b2667a8623` |
| `arcana/craft/templates/ledger.schema.yml` | `schema_stack`, `source_of_truth_policy`, `index_contract` | `0.3.0` | `b086fb4b23026a4ce5d5932a4561b65d420d40416bc346028784c12a4e7b7034` |
| `arcana/craft/templates/schemas/ledger-core.schema.yml` | `typed_item_status`, `gap_status`, `row_families.gaps` | `0.3.0` | `23ba19aa30ed787d6a4b506e359bfb074a0ed0a71a93c7cf269283c533ae9646` |
| `arcana/craft/templates/schemas/index.schema.yml` | `source_of_truth_policy`, `embedded_index_contract`, `generated_index_contract` | `0.3.0` | `a686a37bdeae5811069d6e2a654d8e4d190cb7cbd567029edbc5e21cf78f7872` |
| `spells/goal/.craft/ledger.yml` | `BLK-GOAL-SUBMODULE-001`, `indexes.active_blockers`, `gaps` | `0.2.0` | `0274d2f90aff9b5d02a94d31cf4a8b7088b7730c68ce18230a81b6920766e462` |
| `development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md` | `What went wrong`, `Proposed Craft behavior` | historical handoff | `e8a2a2cda95cc13aaaa711cba1aa79b6f55754bf2602b1d3c7861f23ed9f38ae` |

The closed initial corpus for prior mechanisms and deferred layers is:

- `arcana/craft/ARCHITECTURE.md` — canonical deferral record for generated
  indexes, projections, row-update plans, validation reports, and mutation
  tooling;
- `development/craft/CRAFT-HANDOFF-AUTO-ARTIFACT-LIFECYCLE-2026-06-13.md`
  — historical witness and proposal for receipt application and deterministic
  reindexing;
- `arcana/craft/development/invoke-runs/20260615T123257Z-craft-index-improvements/INVOKE-DESIGN-ARCHITECTURE.md`
  — candidate-local generated-index and projection proposal;
- `arcana/craft/development/invoke-runs/20260615T152120Z-craft-row-update-planner-architecture/INVOKE-DESIGN-ARCHITECTURE.md`
  — candidate-local deterministic row-update planning proposal; and
- `arcana/craft/development/invoke-runs/20260615T161047Z-craft-canonical-schema-stack/INVOKE-DESIGN-SCHEMA-STACK.md`
  — candidate-local schema-layer proposal covering projection, row-update, and
  validation-report deferrals.

This list is exhaustive for the initial baseline, not for all historical Craft
development material. The existence of these proposals and deferrals does not
establish that any one of them is the required solution.

## Known Gaps

- The complete set of current Craft state transitions and mutation entry points
  has not been established against the canonical package and live usage.
- It is not known which recorded inconsistencies are isolated historical drift,
  which remain reproducible, and which arise from ambiguous contracts rather
  than missing enforcement.
- The exact responsibility boundary between applying a native capability result
  to Craft state and preserving that result as externally owned evidence remains
  unresolved for each transition type.
- It is not established which source-row changes require corresponding changes
  to embedded indexes, regeneration or invalidation of `.craft/index.json`,
  refresh of `CRAFT.md`, artifact records, next moves, blockers, decisions,
  gaps, or recomposition state.
- The minimum integrity meaning of freshness, atomicity, idempotence,
  reconstructibility, stale-state detection, and failed mutation has not been
  established for Craft.
- It is unclear which integrity properties belong in canonical schema rules,
  validation behavior, runtime behavior, generated surfaces, or operator
  discipline.
- Compatibility requirements for existing ledgers with divergent formatting,
  missing fields, stale embedded indexes, stale generated indexes, or older
  lifecycle values have not been determined.
- The current validation boundary does not yet establish whether a ledger that
  parses and satisfies row-shape checks also has semantically current embedded
  indexes, whether a generated `.craft/index.json` is fresh and complete,
  whether `CRAFT.md` reflects the ledger, or whether evidence applications and
  next moves remain current.
