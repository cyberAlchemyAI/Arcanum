# Invoke Design: Integration Boundary Discipline

Status: pass
Mode: design
Capability: `invoke`

## Context View

The design problem sits between DomainSpec and implementation/runtime evidence.

DomainSpec owns domain concepts and feature graph vocabulary. External standards own protocol and wire shapes. Task Session owns bounded execution receipts. Integration Boundary Discipline owns the rule that these surfaces must remain connected without collapsing authority.

## High-Level Structure View

```text
Integration Boundary Discipline
  -> minimum component catalog
  -> DomainSpec integration aspect proposal
  -> formula validator proposal
  -> evidence and receipt boundary
  -> future IntegrationSpec package decision gate
```

## Low-Level Components

| Component | Purpose |
| --- | --- |
| Integration Boundary | Names the system boundary and application use case it serves. |
| Integration Port | Package-local label for application-owned dependency contract. |
| Integration Adapter | Package-local label for external-system implementation of a port. |
| Integration Resource | External database, API, cache, queue, webhook, file store, identity provider, or iPaaS host. |
| Integration Decision | Trade-off record for protocol, store family, cache strategy, provider, SDK, or platform. |
| Integration Policy | Retry, timeout, idempotency, consistency, auth, rate-limit, cache, circuit-breaker, and reconciliation behavior. |
| Integration Mapping | Domain/external shape transformation, delegating to DomainSpec `Mapping` where possible. |
| Integration Evidence | Tests, schemas, emulator/sandbox receipts, migrations, observability, and reconciliation checks. |

## Workflow Process View

1. Start from an application `Operation` or `Query`.
2. Name the integration boundary and port.
3. Select external resource family through a decision record.
4. Attach or reference the standard contract: OpenAPI, AsyncAPI, CloudEvents, SQL/schema, SDK, or provider docs.
5. Define policies and mappings.
6. Define evidence: contract tests, mapping tests, emulator/sandbox checks, migration checks, cache consistency checks, and observability.
7. Validate completeness through a formula contract.
8. Route implementation through Task Session only after a work-pack exists.

## Decision Flow View

```text
Does an existing DomainSpec Interface/Mapping/Event cover it?
  yes -> extend through integration aspect and evidence
  no -> keep local Integration Boundary term, do not promote canon

Does an external standard own the wire/protocol shape?
  yes -> reference it and record crosswalk obligations
  no -> document local contract and evidence requirements

Is coordination repeated enough to need autonomous lifecycle?
  yes -> future sigil-development for integration-spec
  no -> discipline + template + formula route
```

## Dependency Interface View

| Owner | Boundary |
| --- | --- |
| DomainSpec definitions | Canonical meta-types and edges remain unchanged. |
| DomainSpec templates | Future `integrations.md` aspect is a candidate output, not created here. |
| Dispatch Spec | Validates route shape, receipts, subagent lifecycle, and owner boundaries. |
| Formula validator | Candidate owner for integration contract completeness. |
| Task Session | Candidate owner for execution evidence. |
| External standards | Own wire/protocol contracts. |

## Design Decision

Select discipline-first hardening as the immediate route. Preserve `integration-spec` as a future package candidate after proof.
