# Craft Current Architecture

This pack captures the current canonical Craft architecture. It is a comparison
baseline for proposed changes, not a proposal for new behavior.

Use it before mutating Craft runtime contracts, schemas, generated views,
projection surfaces, scripts, or tools. A proposal should state what changes
relative to this baseline, what remains unchanged, and which validation proves
the difference.

## Scope

Craft is an Arcana sigil for project-local recursive ledgers. It keeps durable
state for nested development contexts, blockers, enablers, decisions, gaps,
definitions, next moves, route evidence, artifacts, validation, and
recomposition.

Current Craft architecture is intentionally small. It defines the operating
method, storage contract, schema contract, linked human-view expectations, and
example ledgers. It does not yet ship a command runner, automated renderer,
projection generator, or row update tool.

## Source Authority

The current canonical Craft package is rooted here:

```text
arcana/craft/
  SKILL.md
  README.md
  ARCHITECTURE.md
  templates/ledger.schema.yml
  templates/schemas/
    ledger-core.schema.yml
    index.schema.yml
  examples/
```

Current authority is split by concern:

| Surface | Authority |
| --- | --- |
| `SKILL.md` | Executable operating contract for agents using Craft. |
| `README.md` | Package overview, storage model, and canonical file index. |
| `ARCHITECTURE.md` | Current architecture baseline for comparing proposed changes. |
| `templates/ledger.schema.yml` | Compatibility entrypoint for the Craft schema stack. |
| `templates/schemas/ledger-core.schema.yml` | Source ledger row-family, ID, link, enum, and reference contract. |
| `templates/schemas/index.schema.yml` | Embedded index and generated `.craft/index.json` contract. |
| `examples/*.yml` | Concrete ledger examples that exercise the schema. |
| `examples/*-CRAFT.md` | Linked human-view examples derived from ledger state. |

Historical material under `development/craft/` is promotion evidence and working
material. It is not the runtime contract for Craft.

## Current Architecture At A Glance

```text
Craft operator or agent
      |
      v
SKILL.md operating contract
      |
      v
workspace resolution
      |
      v
.craft/ledger.yml              templates/ledger.schema.yml
source of truth  <-----------> schema-stack entrypoint
      |
      +--> .craft/index.json    optional generated lookup surface
      |
      +--> CRAFT.md             linked human-readable view
      |
      +--> .craft/artifacts/    receipts, handoffs, evidence, reports
```

The ledger is the only project-local source of truth. Human views and machine
indexes are derived from it. Craft can record route memory and receipt evidence,
but called capabilities own their native artifacts and verdicts.

## 1. Context View

Craft sits between an operator and a project-local state ledger.

```text
human or agent intent
  start, state, describe, blocker, decision, gap, next, validate, recompose
      |
      v
Craft method
  resolve workspace
  read or update ledger state
  preserve links and indexes
  record residue and next move
      |
      v
project-local Craft state
  .craft/ledger.yml
  CRAFT.md
  .craft/index.json
  .craft/artifacts/
```

Craft is not a global definition authority and not a generic task executor. It
coordinates local project memory and keeps recursive work visible across
sessions.

## 2. High-Level Structure View

```text
package boundary
  SKILL.md
  README.md
  ARCHITECTURE.md
  templates/ledger.schema.yml
  examples/
      |
      v
runtime workspace boundary
  .craft/ledger.yml
  .craft/index.json
  .craft/artifacts/
  CRAFT.md
      |
      v
operation boundary
  workspace resolution
  ledger read or explicit row update
  index refresh
  human view export
  validation and residue reporting
```

The package boundary defines how Craft should behave. The runtime workspace
boundary contains per-project state. The operation boundary is currently a
method contract, not a packaged script interface.

## 3. Low-Level Components View

| Component | Current Form | Responsibility |
| --- | --- | --- |
| Workspace resolver | `SKILL.md` process contract | Discover existing `.craft/ledger.yml` files, disambiguate scope, and bind before acting. |
| Ledger source | `.craft/ledger.yml` | Own project-local structured state. |
| Ledger schema stack | `templates/ledger.schema.yml`, `templates/schemas/ledger-core.schema.yml`, `templates/schemas/index.schema.yml` | Define source-ledger rows, required fields, enums, ID patterns, references, link shape, embedded indexes, and generated index freshness. |
| Human view | `CRAFT.md` | Render linked status and rows for people without becoming source authority. |
| Machine index | `.craft/index.json` | Optional rebuildable lookup data derived from the ledger. |
| Artifact store | `.craft/artifacts/` | Hold receipts, handoffs, validation evidence, reports, and supporting material. |
| Examples | `examples/` | Demonstrate small and larger ledger/view shapes. |

The current schema row families are:

| Row Family | ID Field | Purpose |
| --- | --- | --- |
| `contexts` | `context_id` | Recursive project-like units. |
| `artifacts` | `artifact_id` | Files, records, work-packs, validations, handoffs, and receipts. |
| `descriptions` | `description_id` | Versioned working descriptions for Craft contexts. |
| `definitions` | `definition_id` | Local candidate definitions scoped to a Craft context or artifact. |
| `gaps` | `gap_id` | Missing, deferred, weak, or unresolved areas that remain visible. |
| `relations` | `relation_id` | Typed links between contexts, artifacts, decisions, and other rows. |
| `typed_items` | `item_id` | Blockers, gates, enablers, and related typed state. |
| `decisions` | `decision_id` | Open, closed, blocking, waiver, selection, approval, and deferral decisions. |
| `recomposition` | child/parent context pair | Evidence that a child context has been recomposed into a parent. |

The required ledger indexes are `by_id`, `open_decisions`,
`blocking_decisions`, `active_blockers`, `active_gaps`, `next_moves`, and
`artifacts_by_path`.

### Current Schema Stack Boundaries

The current P0 schema stack covers source-ledger rows and index contracts. It
formalizes the example-backed `descriptions`, `definitions`, `gaps`, and
`recomposition` sections, and it defines the required embedded/generated index
shape without implementing a generator.

Route handoffs, receipts, route events, human interface output, projections,
row-update plans, validation reports, and artifact manifests remain deferred
schema layers. A proposal that edits those layers must either create the
matching schema slice first or explicitly treat the behavior as candidate-local.
For a deterministic row update planner, the first safe fixture scope should stay
inside source-ledger and index schemas until projection and row-update schemas
exist.

## 4. Workflow Process View

Current Craft operations follow this shape:

```text
1. Resolve the owning Craft workspace.
2. Read the authoritative ledger when one exists.
3. Perform one explicit operation:
      start_project
      state
      describe
      add_blocker
      refine_blocker
      add_enabler
      next
      open_decision
      decide
      add_gap
      add_definition
      open_child_context
      link
      validate
      recompose
      export_ledger
4. Preserve stable IDs and links.
5. Refresh ledger indexes after meaningful mutation.
6. Export or update CRAFT.md only as a linked view.
7. Record residue and next move.
```

Repository-wide status is read-only. It must discover every Craft space and
show pending work by node, including active blockers, blocking decisions, open
decisions, active gaps, pending artifacts, recomposition residue, and the
current next move.

## 5. Decision Flow View

| Decision Point | Current Behavior | Reason |
| --- | --- | --- |
| Source of truth | `.craft/ledger.yml` | Keeps project state machine-readable and durable. |
| Human view authority | Derived only | Prevents Markdown drift from replacing structured state. |
| Generated index authority | Derived only | Keeps lookup surfaces rebuildable. |
| Workspace selection | Discover and disambiguate before acting | Prevents writing to the wrong Craft scope. |
| Raw blockers | Cannot be directly resolved | Blockers need refinement and closure criteria first. |
| Child context closure | Requires recomposition evidence | Prevents local work from vanishing without parent fit. |
| Route results | Recorded as evidence, not rewritten | Called capabilities own native results. |
| Canonical surface mutation | Only by explicit maintenance or promotion task | Protects Craft from accidental self-modification. |

## 6. Dependency Interface View

| Dependency | Current Interface | Contract |
| --- | --- | --- |
| Agent runtime | `SKILL.md` | Supplies the executable Craft method. |
| Ledger schema stack | `templates/ledger.schema.yml`, `templates/schemas/ledger-core.schema.yml`, `templates/schemas/index.schema.yml` | Supplies source row, enum, reference, ID, link, embedded index, generated index, and freshness rules. |
| Project filesystem | `.craft/` and `CRAFT.md` | Stores project-local state and derived views. |
| Native capabilities | Their own artifacts and receipts | Craft records handoffs, results, residue, and next moves. |
| Examples | `examples/` | Provide regression-readable shapes for ledgers and human views. |

Craft currently depends on disciplined file editing and validation by the
operator or calling lifecycle. It does not expose a stable public CLI, library,
or generated adapter inside this package.

## Explicitly Absent Today

These capabilities are not part of the current architecture:

| Capability | Current Status |
| --- | --- |
| Deterministic row update planner | Not present. |
| CSV projection import or writeback | Not present. |
| Projection metadata contract under `.craft/projections/` | Not present. |
| Route-exchange schema for handoffs, receipts, and route events | Not present. |
| Interface schema for `CRAFT.md`, `state all`, and `Craft Result` | Not present. |
| Automated YAML patch application | Not present. |
| Public Craft CLI | Not present. |
| Packaged ledger renderer | Not present. |
| Generated machine index builder | Not present as a shipped tool; schema exists. |
| Fixture suite for row update behavior | Not present. |
| Direct mutation from derived `CRAFT.md` | Prohibited. |

## Comparison Checklist For Proposed Changes

Every proposed Craft architecture change should answer:

1. Which current authority surface changes: `SKILL.md`, `README.md`,
   `ARCHITECTURE.md`, schema stack, examples, scripts, fixtures, or generated mirrors?
2. Does `.craft/ledger.yml` remain the source of truth?
3. Are derived views still rebuildable and non-authoritative?
4. Does the change introduce a new runtime surface, command, script, fixture,
   projection, or schema field?
5. Does the change preserve stable row IDs, required indexes, and link shape?
6. Does it add mutation behavior, or only dry-run planning/reporting?
7. What pass, flag, block, and no-op cases prove the new behavior?
8. What stays explicitly absent after the change?

For the row update planner proposal, the current baseline is: no planner, no CSV
writeback, no projection directory contract, no apply mode, and no shipped tool.
Any implementation should first explain how it adds a deterministic dry-run
planner while keeping ledger authority, derived-view boundaries, and stable row
identity intact.

## Change Classification

Use this guide when deciding how much governance a Craft change needs:

| Change Type | Examples | Expected Governance |
| --- | --- | --- |
| Documentation-only clarification | README wording, architecture comparison note | Diff check and source-authority review. |
| Contract clarification | `SKILL.md` behavior, output contract, non-use rule | Explicit rationale and examples if behavior changes. |
| Schema change | New field, enum, index, row family, or reference rule | Schema validation, example update, and compatibility notes. |
| Runtime surface | Script, CLI, generated adapter, projection, renderer | Design bundle, fixtures, dry-run proof, and task-session execution. |
| Mutation primitive | YAML patching, row updater, import writeback | Deterministic fixtures, stale-source handling, no-op behavior, block cases, and explicit apply boundary. |

## Current Risks

| Risk | Current Mitigation |
| --- | --- |
| Human view drift | `CRAFT.md` is derived and never source of truth. |
| Wrong workspace mutation | Workspace resolution must discover and disambiguate. |
| Hidden pending work | All-status must report pending items by node. |
| Unowned route evidence | Craft records handoffs and receipts while native routes own verdicts. |
| Accidental Craft self-mutation | Canonical surfaces require explicit maintenance or promotion scope. |

## Maintenance Rule

Update this file when the current Craft architecture changes, not for every
proposal. Proposal bundles should link here and describe their delta from this
baseline.
