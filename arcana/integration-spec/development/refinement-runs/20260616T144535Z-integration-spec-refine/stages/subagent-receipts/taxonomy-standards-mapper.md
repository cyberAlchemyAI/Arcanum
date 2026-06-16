# Subagent Receipt: Taxonomy Standards Mapper

Agent ID: `019ed0ed-96d5-7a63-96fe-0e97119322ae`
Role ID: `taxonomy-standards-mapper`
Status: pass-readonly
Spawn status: spawned
Join status: completed
Close status: closed

## Artifacts Considered

- `arcanum/definitions/TAXONOMY.md`
- `arcanum/definitions/DEFINITIONS.md`
- `arcanum/definitions/RELATIONSHIPS.md`
- `arcanum/spells/invoke/templates/domainspec-spec/README.md`
- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`

## Reuse Map

DomainSpec meta-types to reuse:

- `Interface`: HTTP/RPC/module/API boundaries.
- `Mapping`: field, payload, DTO, envelope, and provider-response transformations.
- `Event`: domain facts crossing async boundaries.
- `Policy`: retry, timeout, fallback, routing, consistency, idempotency, cache, and reconciliation decisions.
- `Operation` and `Query`: application-layer use cases that depend on integration ports.
- `Workflow` and `Saga`: multi-step integration orchestration.
- `Rule`, `State Machine`, `Enum / Type`: eligibility, failure states, circuit-breaker states, sync lifecycles, and allowed strategy families.

Strained gaps:

- No canonical edge for `Port -> Adapter implements`.
- No canonical edge for `Adapter -> External Resource uses/connects-to`.
- No canonical edge for `Evidence -> Decision proves`.
- No canonical cache/source-of-truth edge.
- UI edges `fetches`, `mutates`, `contracts`, and `mirrors` are useful analogies, but should not be overloaded for non-UI application ports.

## External Standards Reuse

| Source | IntegrationSpec use |
| --- | --- |
| OpenAPI | HTTP API description and tooling surface. |
| AsyncAPI | Message-driven API contracts and protocol bindings. |
| CloudEvents | Portable event envelope metadata. |
| Ports and adapters | Application-owned ports and external-system adapters. |
| Cache guidance | Cache source of truth, TTL, invalidation, stale-data, local/shared cache, and sensitivity decisions. |
| Data-store guidance | Data format, access pattern, consistency, schema flexibility, latency, throughput, lifecycle, cost, governance, security, and store family choice. |

## Package-Local Vocabulary

Keep these local unless definitions-governance promotes them:

- `Integration Port`
- `Integration Adapter`
- `Integration Resource`
- `Integration Decision`
- `Integration Policy`
- `Integration Evidence`
- `Cache Strategy`
- `Data Store Selection Record`
- `External API Contract`
- `Provider Boundary`
- `Idempotency Contract`
- `Consistency Contract`
- `Adapter Test Matrix`

## Owner-Boundary Warnings

- Do not mutate `arcanum/definitions/*` from this run.
- Do not treat external standards as Arcanum canon.
- Do not put private parent-workspace, client, implementation, or validation examples into public `arcanum`.
- Do not widen DomainSpec by accident.
- Do not let `Adapter` silently shift from UI `Adapter` to backend integration adapter without a local vocabulary boundary.
