# Arcanum Migration

## Objective

This analysis area exists to map the principal concepts, capabilities,
services, artifacts, ownership boundaries, and runtime relations that currently
exist in Arcanum, then use that evidence to prepare a migration plan for a new
Git branch.

The migration is not assumed to be a clean rewrite. Its purpose is to preserve
useful behavior and accumulated evidence, expose contradictions and incomplete
integrations, and move the system incrementally toward clearer contracts and
operable boundaries.

## Current position

Arcanum does not currently behave as one universal linear pipeline. The
repository supports multiple caller- and owner-bound compositions mediated by
artifacts, dispatches, receipts, approvals, and explicit state operations.
Documented contracts, implemented bindings, and observed executions are uneven
and must remain distinguishable.

The existing Craft, Task Session, and Decision Gate explanation is retained as
a minimum product model. It is not treated as the complete migration inventory.

## Craft write-back boundary

Craft is the semantic owner and source of truth for the selected Craft ledger,
not for every artifact or state family in Arcanum. Invoke, Task Session,
Decision Gate, Goal, delegated capabilities, and observability retain ownership
of their native artifacts, receipts, verdicts, and telemetry.

An external result can inform a Craft update, but the result does not mutate the
ledger merely by existing. A caller must determine that Craft-owned state is
affected and invoke a scoped Craft operation that preserves Craft validation
and ownership.

No generic, packaged mechanism has yet been established that automatically:

1. observes every relevant external capability result;
2. determines that a Craft ledger row is implicated;
3. translates the result into a typed Craft operation;
4. invokes the correct Craft workspace; and
5. records the owner receipt and resulting ledger transition.

Some bounded or historical flows coordinate proposals or approved writes. They
are evidence for those exact flows, not proof of a universal automatic
write-back service.

## Mapping views

The analysis will keep three views separate.

### 1. Minimum product model

- **Craft** — durable state for one selected Craft ledger scope.
- **Task Session** — bounded execution and validation of one unit of work.
- **Decision Gate** — explicit resolution of consequential choices.

This view is intended for product orientation, not exhaustive architecture.

### 2. Current evidenced inventory

The migration inventory must at least examine:

- the skill, sigil, and spell capability model;
- Invoke lifecycle authoring and refresh;
- Dispatch Spec route representation and validation;
- Orchestrate native execution, joins, gates, and evidence;
- Task Session bounded execution and owner hooks;
- Craft ledger ownership and write-back;
- Decision Gate authority and decision records;
- Continuation Router and Goal progression models;
- Context Builder, Implementation Readiness, and readiness audits;
- observability, experiment evidence, and artifact production;
- registries, installers, generated host projections, overlays, and
  compatibility surfaces such as `tools/arcanum`;
- capability development, promotion, and source-precedence rules.

Every inventory entry should state:

- owner and canonical source;
- responsibility and non-responsibility;
- inputs, outputs, schemas, and write scopes;
- upstream and downstream consumers;
- evidence status: `documented`, `implemented`, or `observed`;
- contradictions, missing bindings, and compatibility obligations;
- provisional migration disposition: preserve, repair, adapt, merge, retire, or
  unresolved.

The executable inventory is one JSON mapping package at
`mapping/current-system-map.json`. Its
[`current-system-map.schema.json`](contracts/current-system-map.schema.json)
contract and deterministic validator make relation identity, discovery
coverage, baseline binding, unresolved items, and decision readiness
checkable. The file is not created until the mapping pass has a reproducible
baseline and real records to place in it.

### 3. Candidate migration workstreams

Candidate target-architecture work remains proposed until separately decided
and proved. Current candidates include:

- a governed lifecycle boundary for generated execution artifacts;
- a typed and owner-preserving Craft write-back path;
- a clearer relationship between Dispatch Spec, Orchestrate, host profiles,
  projections, and compatibility resolvers;
- a unified capability model, if authority, identity, precedence, and
  path-compatibility research supports it;
- parity and freshness checks for generated host skill packages.

Listing a candidate here does not establish that the service already exists or
that its target design has been accepted.

## Runtime relationship

The runtime should not be described as one linear sequence of every related
surface:

- **Dispatch Spec** validates the shape, dependencies, boundaries, and
  authorization representation of a proposed dispatch.
- **Orchestrate** consumes an admitted dispatch and owns native execution
  preflight, scheduling, joins, gates, and closeout.
- **Host profiles and generated projections** make capabilities and native
  operations available to a host; they are inputs to deployment and execution,
  not outputs of Orchestrate.
- **`tools/arcanum`** should remain a deterministic resolver and compatibility
  surface. It should not become a second owner of orchestration semantics.

## Migration approach

1. Complete the current-system inventory and classify evidence without changing
   canonical paths.
2. Identify artifact producers, consumers, write locations, authority
   boundaries, and path-dependent consumers.
3. Convert unresolved architecture questions into explicit decisions with
   acceptance criteria and compatibility obligations.
4. Establish a reproducible migration baseline. Use a resolvable clean commit
   or preserve a retrievable content-addressed bundle of the required dirty
   state; a list of hashes without the corresponding bytes is not a baseline.
5. Create the migration branch from the selected baseline.
6. Migrate one bounded vertical slice at a time, retain compatibility adapters,
   and require evidence before expanding the slice.

The first vertical slice is not selected by this README. Existing evidence
suggests Task Session to Invoke Refresh as a strong candidate for an
artifact-lifecycle proof, while Dispatch Spec and Orchestrate are candidates for
the runtime spine. The choice requires an explicit migration decision.

## Non-goals

This folder does not yet:

- approve a clean rewrite or successor repository;
- authorize moving or deleting `formulae/`, `transmutations/`, or `arcana/`;
- define the final skill identity or schema;
- claim that proposed artifact or write-back services are implemented;
- promote historical fixtures into evidence of universal runtime behavior;
- perform the migration itself.

## Artifacts

- [`analysis.md`](analysis.md) — reader-facing explanation and eventual
  evidence-backed migration analysis.
- [`contracts/current-system-map.schema.json`](contracts/current-system-map.schema.json)
  — executable contract for relation records, discovery coverage, baselines,
  open items, and completion.
- [`contracts/current-system-map.example.json`](contracts/current-system-map.example.json)
  — minimal conforming example of that contract.
- [`scripts/validate_mapping.py`](scripts/validate_mapping.py) — read-only
  schema, relation, coverage, baseline, and readiness validator.
- [`requirements.txt`](requirements.txt) — validator dependency boundary.
- [`research/arcanum-composition/research-initial-definitions.md`](research/arcanum-composition/research-initial-definitions.md)
  — informational research baseline.
- [`research/arcanum-composition/findings.md`](research/arcanum-composition/findings.md)
  — current composition findings and evidence ceilings.
- [`research/arcanum-composition/initial-definitions-review.md`](research/arcanum-composition/initial-definitions-review.md)
  — preserved review of the research initial definitions.

## Status

Current phase: **mapping and migration preparation**.

No target architecture, migration branch, or repository-wide move is approved
by this README alone.
