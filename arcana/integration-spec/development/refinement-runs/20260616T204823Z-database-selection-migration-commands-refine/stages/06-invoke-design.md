# Invoke Design: Database Selection And Migration Commands L0

Status: pass
Owner capability: invoke
Mode: design

## Integration Data Resource Decision Record

Required fields:

| Field | Meaning |
| --- | --- |
| `resource_role` | What the store does for the application: primary OLTP, projection, cache, search, vector index, analytics sink, archive, etc. |
| `resource_family` | Relational, document, key-value/cache, wide-column, graph, time-series, object/file/lake, stream/log, search/index, vector, analytics/warehouse, ledger, external SaaS/API store, ephemeral/session. |
| `source_of_truth_role` | External authority, local authority, replicated projection, materialized view, cache, search index, analytics sink, vector index, archive, transient state. |
| `workload_access_patterns` | Key lookup, range scan, join, aggregate, full-text, graph traversal, temporal query, similarity search, streaming ingest. |
| `data_shape` | Structured relational, document, key-value, binary object, event/log, graph, vector embedding, time-series, analytical fact. |
| `consistency_model` | ACID, eventual, session, read-your-writes, monotonic reads, tunable, or custom. |
| `atomicity_scope` | Single row/document/key, multi-row transaction, cross-resource saga, batch job, stream offset. |
| `latency_throughput_targets` | Expected p95/p99 latency, throughput, burst, geographic placement, partitioning/sharding. |
| `volume_growth` | Current size, growth pattern, retention, hot/cold tiering. |
| `retention_lifecycle` | TTL, archive, legal hold, deletion, backup/restore, rebuild. |
| `migration_backfill_plan` | Schema evolution, data movement, backfill, reindex, rebuild, dual-write/read. |
| `security_governance` | PII, encryption, access control, audit, data residency, compliance. |
| `failure_modes` | Outage, stale projection, cache stampede, index lag, migration failure, restore failure. |
| `alternatives_rejected` | Store families or providers rejected with trade-offs. |
| `evidence_anchors` | Benchmarks, query examples, load tests, restore test, migration dry-run, fixture results. |

Specialized resource roles require extra fields:

- Cache: strategy, TTL, invalidation trigger, stale-read policy, sensitivity constraints, reconciliation.
- Search/vector: derivation source, refresh/rebuild path, lag tolerance, deletion/privacy propagation, fallback behavior.
- Analytics/lake: lineage, freshness, partitioning, privacy propagation, cost/governance.

## Database Migration Command Profile

Required fields:

| Field | Meaning |
| --- | --- |
| `tool` | Flyway, Liquibase, Prisma, Alembic, Django, Rails, custom SQL runner, managed provider migration. |
| `environment` | Development, test, staging, production, disposable preview, shadow database. |
| `target_database` | Logical resource target; no secrets or connection strings in public spec. |
| `command_class` | `author_generate`, `review_dry_run`, `validate_status`, `drift_check`, `apply_deploy`, `history_state_management`, `lock_management`, `rollback_downgrade_undo`, `roll_forward_fix`, `data_backfill`, `destructive_reset_clean_drop`. |
| `command` | Tool command or abstract action, with secrets redacted. |
| `migration_artifacts` | Migration files, changelog, schema model, generated SQL, ORM model, snapshot, diff artifact. |
| `schema_history_resource` | Migration table/changelog/version table and identity/checksum policy. |
| `drift_precheck` | Whether drift/status/diff is required before apply. |
| `lock_policy` | Lock acquisition, timeout, owner, stuck lock inspection, manual release gate. |
| `dry_run_artifact` | Generated SQL, plan, diff, report, operation list, approval record. |
| `apply_policy` | Who can apply, when, with what backup/restore and observability. |
| `rollback_or_roll_forward_policy` | Default prod recovery path; rollback only with reversible logic and data recovery limits. |
| `expand_contract_stage` | Additive change, compatibility period, backfill, read/write switch, constraint/drop cleanup. |
| `backfill_plan` | Idempotency, batching, resumability, transaction scope, routing, progress evidence, failure recovery. |
| `destructive_gate` | Required approvals and evidence for reset/clean/drop/destructive DDL. |
| `evidence_fixtures` | Pass/flag/block fixtures attached to the command profile. |

## Local Relations

- `operation_uses_data_resource`
- `resource_governed_by_decision`
- `migration_targets_resource`
- `migration_command_uses_artifact`
- `command_requires_environment_policy`
- `evidence_anchor_covers_obligation`

These are IntegrationSpec-local and must not be added to DS-D2 in this run.
