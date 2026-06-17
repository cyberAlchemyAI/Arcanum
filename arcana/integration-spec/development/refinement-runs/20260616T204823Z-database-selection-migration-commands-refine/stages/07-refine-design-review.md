# Interrogation Design Review

Status: pass-with-residue
Owner capability: interrogation
Mode: refine-design-review

## Verdict

The design gives IntegrationSpec a concrete way to guide database selection and migration commands without pretending DomainSpec already owns those mechanics.

## Pass Conditions Met

- Selection starts with workload/access/source-of-truth requirements.
- Resource families and roles stay local.
- Cache/search/vector/analytics roles require authority and rebuild/freshness fields.
- Migration command profile separates dev/test/staging/prod permissions.
- Drift/status/lock/checksum/dry-run/destructive gates are explicit.
- Validator scope remains structural.

## Flags

- `DatabaseResource` and `SchemaHistoryResource` should remain labels until L0 examples prove stable naming.
- Tool-specific profiles are still needed for Flyway, Liquibase, Prisma, Alembic, Django, and any project-local runner.
- No live database migration proof was executed.
