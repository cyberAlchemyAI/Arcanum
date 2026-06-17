# Subagent Receipt: DomainSpec Data Boundary Guardian

role_id: domainspec-data-boundary-guardian
agent_id: 019ed231-b2de-7383-913a-97bf523c9faa
dispatch_id: refine-20260616T204823Z-database-selection-migration-commands
status: pass-with-boundary-warnings
spawn_status: spawned
join_status: completed
close_status: closed

## Sources Considered

- DomainSpec taxonomy and definitions.
- Prior public IntegrationSpec refinement and gap review.
- Prior OpenClaw integration refine result.

## Findings

- DomainSpec canon is closed around existing meta-types and edges; database resources, migration tools, ports, connectors, evidence, and decision records are not canonical DomainSpec vocabulary.
- Reuse DomainSpec for application meaning: `Operation`, `Query`, `Interface`, `Mapping`, `Policy`, `Workflow`, `Saga`, and `Event`.
- Put database selection and migration commands in local IntegrationSpec/tooling vocabulary.

## Recommended Model

Layer 1: DomainSpec anchor layer for host intent and domain behavior.

Layer 2: IntegrationSpec L0 local machinery for `IntegrationBoundary`, `IntegrationPort`, `Connector`, `ExternalResource` or `DatabaseResource` label, `IntegrationDecisionRecord`, `MigrationCommandRecord`, `EvidenceAnchor`, and failure fixtures.

## Boundary Warnings

- Do not use canonical `Adapter` for provider/database connectors.
- Migration logs and runtime receipts are task evidence, not canonical spec truth.
- Keep local relations outside DS-D2.

## Handoff

DomainSpec names the business meaning; IntegrationSpec owns the resource, tool, migration, and evidence machinery until governance promotes anything deliberately.
