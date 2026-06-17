# Refine Seed Proposal: Database Selection And Migration Commands

Status: execution-approved
Run ID: 20260616T204823Z-database-selection-migration-commands-refine
Dispatch ID: refine-20260616T204823Z-database-selection-migration-commands
Target: `arcanum/arcana/integration-spec`
Preset: full
Research mode: bounded-research

## Operator Intent

Run the same full refinement pattern used for OpenClaw integration modeling, now focused on database selection and migration commands.

The concrete question is:

> How should IntegrationSpec model database selection and migration commands so DomainSpec can guide application-layer work without absorbing infrastructure vocabulary into its canon?

## Target Resolution

This run is scoped as an Integration Boundary Discipline refinement, not an implementation.

Allowed now:

- Create refinement evidence under this run folder.
- Model database/data-store selection as an Integration Resource and Decision Record problem.
- Model migration commands as an Integration Command Surface with safety gates and evidence obligations.
- Reuse prior IntegrationSpec findings and DomainSpec taxonomy boundaries.

Deferred:

- Mutating `arcanum/definitions/*`.
- Creating production migration scripts.
- Running database migration commands against any live database.
- Adding a final `integrations.md` aspect before L0 fields stabilize.
- Creating a formula validator before examples and fixtures exist.

## Local Evidence

- Prior IntegrationSpec review selected **Integration Boundary Discipline first**.
- The IntegrationSpec gap review found DomainSpec does not currently model provider/resource topology, data-store selection, cache/source-of-truth, or evidence/proof relationships as canonical graph vocabulary.
- The OpenClaw integration refine proved a useful pattern: host-owned port first, external resource second, decision record plus evidence anchors third.
- Operator instruction requested the same pattern with subagent fanout and full refine evidence.

## Bounded External Research Baseline

- AWS Well-Architected says data storage should be selected so querying, scaling, and storage characteristics support workload data requirements.
- Azure Architecture Center says teams should identify data storage and access requirements for each application or service, then use policies to control allowed resource types.
- Azure data model guidance says a single data store rarely satisfies all access patterns efficiently and lists relational, key-value, document, graph, time-series, object, search, vector, and analytical models.
- Flyway migration guidance centers on versioned/repeatable migrations, schema history, `migrate`, `validate`, `repair`, checksums, and known baselines.
- Liquibase frames database change management around update, rollback, snapshot, diff, and status command families.
- Prisma Migrate separates development and production commands and uses advisory locking for migration commands.
- Alembic and Django show that migration generators create candidate/schema-change artifacts, but generated migration output still needs review.

## Provisional Model

Do not model database selection as merely a field under DomainSpec `State` or `Repository`.

Model it as:

```text
DomainSpec Operation/Query/Workflow
  -> Integration Boundary: Data Resource Boundary
  -> Integration Port: Read/Write/Query/Transaction/Projection/Cache/Analytics need
  -> Integration Resource: selected data-store family and concrete provider
  -> Integration Decision Record: workload, access, consistency, lifecycle, source-of-truth, migration, evidence
  -> Migration Command Surface: generate/diff/validate/apply/status/rollback/repair/baseline
  -> Policies + Mappings: transaction, retry, idempotency, retention, privacy, backfill, observability
  -> Evidence Anchors: selection rationale, migration dry-run, drift check, rollback/roll-forward plan, fixture results
```

## DomainSpec Reuse

Use DomainSpec for the host application semantics:

- `Operation`: write behavior or business action that depends on a data store.
- `Query`: read behavior, projections, reports, or lookup needs.
- `State`: domain/application state that must be persisted or derived.
- `Mapping`: DTO/entity/schema transformations and external query shape mappings.
- `Policy`: consistency, transaction, retry, timeout, retention, privacy, and operational constraints.
- `Workflow` / `Saga`: multi-step behavior with persistence and compensation.
- `Event`: emitted or consumed facts that drive projections or reconciliation.

Keep local to Integration Boundary Discipline:

- Data resource family.
- Source of truth.
- Access pattern profile.
- Consistency model.
- Migration command surface.
- Schema history / changelog / migration table.
- Drift detection.
- Backfill plan.
- Rollback or roll-forward plan.
- Migration evidence anchors.

## Candidate Decision Record Fields

For database selection, require:

| Field | Why it matters |
| --- | --- |
| Workload role | OLTP, OLAP, cache, search, vector, time-series, document, graph, object, queue/event store, ledger, or hybrid. |
| Source of truth | Declares whether this store is authoritative, derived, cached, indexed, or archival. |
| Access patterns | Key lookups, range scans, joins, graph traversals, full-text search, aggregates, temporal queries, similarity search, streaming ingest. |
| Consistency and transactions | ACID, eventual consistency, session consistency, read-your-writes, multi-row/multi-entity transaction needs. |
| Scale and latency | Data volume, growth, throughput, p95/p99 latency, geographic placement, partitioning. |
| Schema evolution | Migration tool, command surface, drift detection, compatibility plan, expand/contract plan. |
| Operational ownership | Managed service vs self-managed, backups, restores, patching, monitoring, access control. |
| Governance | PII, encryption, audit, retention, deletion, data residency, compliance boundaries. |
| Failure modes | Outage, partial migration, lock timeout, drift, destructive migration, rollback failure, stale cache/index. |
| Alternatives rejected | Why other store families or migration approaches were not selected. |
| Evidence anchors | Load/latency evidence, migration dry-run, rollback/roll-forward proof, fixture results, observability. |

For migration commands, require:

| Field | Why it matters |
| --- | --- |
| Command class | generate/diff, validate, apply, status, rollback, repair, baseline, snapshot, reset. |
| Environment policy | Development, test, staging, production; which commands are allowed where. |
| Artifact authority | Migration file, changelog, schema model, generated SQL, ORM model, or live database snapshot. |
| Ordering and identity | Version, timestamp, checksum, author/id/path, schema-history row, migration table state. |
| Locking/concurrency | Advisory lock, migration lock table, deployment serialization, timeout behavior. |
| Safety gate | Dry-run, SQL review, destructive-change check, expand/contract compatibility, backup/restore point. |
| Failure handling | Failed migration, partial apply, checksum mismatch, drift, repair, resolve, rollback, roll-forward. |
| Evidence | Status output, validation output, diff output, generated SQL, applied version, migration logs. |

## Done Criteria

- Seed proposal is written.
- Dispatch route is written and validator-checked.
- Three subagent receipts are collected and closed.
- Ten-stage Refine evidence is written.
- Result explains the database selection and migration-command model.
- No canonical DomainSpec definitions are mutated.
- Public-boundary scan, JSON validation, dispatch validation, and markdown link checks pass.
