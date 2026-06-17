# X-Ray: Data Resource And Migration Command Surface

Status: pass

```text
Host Operation/Query/Workflow
  -> data access need
  -> Integration Data Resource Decision Record
  -> selected Data Resource
  -> Migration Command Profile
  -> Evidence Anchors and Failure Fixtures
```

## Layers

| Layer | Owner | Notes |
| --- | --- | --- |
| Host behavior | DomainSpec | Business operations, queries, workflows, events, mappings, policies. |
| Data resource decision | IntegrationSpec L0 | Store family, source of truth, access patterns, consistency, lifecycle, governance. |
| Migration command profile | IntegrationSpec L0 | Command class, environment policy, history/checksum/lock/drift/safety gates. |
| Runtime state | Database or migration tool | Live schema, schema-history rows, locks, checksums, logs, snapshots. |
| Evidence | Task-session or CI route | Status/diff/dry-run/apply evidence, not canonical taxonomy. |

## Key Boundary Decision

The host application should depend on a named data access port or policy, not on a database engine, ORM migration command, or production schema-history table.
