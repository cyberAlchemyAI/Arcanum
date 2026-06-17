# Invoke Define: Data Resource And Migration Boundary

Status: pass
Owner capability: invoke
Mode: define

## Definition

Database selection is an IntegrationSpec-local resource decision: choose a data resource family and concrete technology from workload access patterns, source-of-truth authority, consistency needs, operational constraints, and evidence.

Migration commands are an IntegrationSpec-local command surface: define which commands may create, validate, preview, apply, repair, roll back, or destroy database state in each environment, and what evidence must exist before and after each command.

## Minimum Components

| Component | Description |
| --- | --- |
| Host data need | DomainSpec operation/query/workflow/state that needs persistence, projection, cache, search, analytics, vector, or archive support. |
| Data resource decision record | Workload-led choice of resource family, source of truth, access patterns, consistency, lifecycle, governance, and evidence. |
| Migration command profile | Tool/environment/command policy that covers generate, dry-run, validate, status, deploy, drift, rollback, repair, baseline, and destructive commands. |
| Evidence anchors | Selection rationale, status output, diff/dry-run SQL, lock/drift evidence, backfill progress, rollback/roll-forward proof. |

## Non-Goals

- Do not introduce canonical `DatabaseResource`, `MigrationCommand`, or `SchemaHistory` types into DomainSpec.
- Do not execute migrations.
- Do not claim a validator proves architecture correctness or production safety.
