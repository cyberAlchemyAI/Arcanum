# Subagent Receipt: Migration Command Governor

role_id: migration-command-governor
agent_id: 019ed231-90c7-78d2-80d1-0441c8163af5
dispatch_id: refine-20260616T204823Z-database-selection-migration-commands
status: pass
spawn_status: spawned
join_status: completed
close_status: closed

## Sources Considered

- Prior public IntegrationSpec gap review and OpenClaw refine result.
- DomainSpec taxonomy and definitions.
- Official Flyway, Liquibase, Prisma, Alembic, and Django migration documentation.

## Findings

- Migration commands are operability machinery for data resources, not canonical DomainSpec vocabulary.
- Required command classes: `author_generate`, `review_dry_run`, `validate_status`, `drift_check`, `apply_deploy`, `history_state_management`, `lock_management`, `rollback_downgrade_undo`, `roll_forward_fix`, `data_backfill`, and `destructive_reset_clean_drop`.
- Dev commands may generate/apply/reset against disposable targets; staging/prod should deploy reviewed artifacts only, with reset/clean/drop blocked.
- Schema history/checksum state, drift detection, locks, dry-run artifacts, expand-contract stages, backfills, and destructive-change gates are first-class evidence obligations.

## Recommended Model

Add an IntegrationSpec-local `Database Migration Command Profile` with fields for tool, environment, target database, command class, command, migration artifacts, schema history, checksum policy, drift precheck, lock policy, dry-run artifact, apply policy, rollback/roll-forward policy, expand-contract stage, backfill plan, destructive gate, approval record, and evidence fixtures.

## Boundary Warnings

- Do not promote `DatabaseMigration`, `MigrationRunner`, `SchemaHistory`, or `BackfillJob` into DomainSpec canon.
- Repair, baseline, stamp, fake, resolve, and lock release commands mutate migration truth and require exceptional gates.

## Residue

Tool-specific profiles should be authored later for Flyway, Liquibase, Prisma, Alembic, Django, and project-local runners.
