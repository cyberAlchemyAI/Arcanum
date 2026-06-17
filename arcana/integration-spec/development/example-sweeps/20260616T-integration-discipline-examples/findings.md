# Integration Discipline Example Sweep Findings

Dispatch ID: `2026-06-16-integration-discipline-example-sweep`
Exit recommendation: `resolved`

## One-Line Answer

Before constructing `INTEGRATION-BOUNDARY-DISCIPLINE.md`, use a matrix of owned precedents: external API authority, callback/webhook directionality, provider trust and idempotency policy, event envelope/delivery residue, derived-resource authority, cache/search/read-model freshness, and migration operability gates. The discipline should compose these owned precedents; it should not claim novelty for their individual semantics.

## Dispatch Record

| Field | Value |
| --- | --- |
| Dispatch type | `research` |
| Working folder | `arcanum/arcana/integration-spec/development/example-sweeps/20260616T-integration-discipline-examples/` |
| Explorer group | API contracts, event/messaging, data/cache/resources, migration operability |
| Reviewer group | precedent, non-vacuity, definitional-soundness |
| Final approver | parent |
| Gate outcome | pass after repairs |

## Verdict Matrix

| Candidate | Owner / Source | Verdict | Use Mode | IntegrationSpec Residue | DomainSpec Reuse | Smallest Fixture |
| --- | --- | --- | --- | --- | --- | --- |
| Provider contract authority and version pinning | OpenAPI and provider docs; GitHub is deployed provider example. Evidence: [research.md §Agent 1](research.md#agent-1-external-api-contract-explorer). | GO | `build-from-owned`; `already-deployed` only for named provider examples | `provider_spec_source`, version pinning, provider/product variant, breaking-change tracking | `Interface`, `Operation`, `Policy` | One provider operation with spec source and required version header. Pass: pinned. Flag: acknowledged but unpinned. Block: unversioned behavior assumed. |
| Callback vs webhook directionality | OpenAPI callback/webhook shape. Evidence: [research.md §Agent 1](research.md#agent-1-external-api-contract-explorer). | GO | `build-from-owned` | callback URL origin, provider-initiated request, registration origin, ack surface, event family, delivery direction | `Event`, `Interface`, `Operation`, `Policy`, `Workflow` | Two tiny contracts: caller-supplied callback URL and provider-initiated webhook, each with registration and ack. |
| Provider trust checks | GitHub auth/signature validation and provider security docs. Evidence: [research.md §Agent 1](research.md#agent-1-external-api-contract-explorer). | GO | `already-deployed` for named providers; otherwise `build-from-owned` | credential kind, permissions/scopes, webhook secret, signature validation, replay stance | `Policy`, `Interface`, `Event`, `Operation` | Signed webhook trust check. Pass: signature checked. Flag: generic trust wording. Block: unsigned payload processed. |
| Idempotent mutating writes | Stripe idempotency docs and comparable provider write policies. Evidence: [research.md §Agent 1](research.md#agent-1-external-api-contract-explorer). | GO | `already-deployed` for Stripe; otherwise `build-from-owned` | idempotency key, scope, retry policy, parameter match rule, duplicate-write behavior | `Policy`, `Operation`, `Interface` | Mutating write with retry key. Pass: duplicate retry has one effect. Flag: retries without key. Block: duplicate-prone write path. |
| Async request/reply and message envelope | AsyncAPI request/reply and message-envelope docs. Evidence: [research.md §Agent 2](research.md#agent-2-event-message-explorer). | GO with wording repair | `build-from-owned` | reply address source, channel binding, payload/header split, transport metadata obligations | `Operation`, `Interface`, `Mapping`, `Policy`, `Event` | Request message with `replyTo`, declared reply channel, payload schema, and header schema. Do not claim delivery guarantees. |
| CloudEvents-style event identity and filterable context | CloudEvents format/envelope precedent. Evidence: [research.md §Agent 2](research.md#agent-2-event-message-explorer). | GO with wording repair | `build-from-owned` | event identity, replay/dedupe key material, routing context, context-vs-data boundary | `Event`, `Mapping`, `Policy` | Event with `id`, `source`, `type`, `subject`, and `data`. Block duplicate-sensitive flow with no stable identity. |
| At-least-once delivery, outbox, and idempotent receiver | Transactional Outbox and Idempotent Consumer pattern docs. Evidence: [research.md §Agent 2](research.md#agent-2-event-message-explorer). | GO | `build-from-owned` | atomic publish boundary, outbox store, relay owner, duplicate-delivery residue, consumer receipt store | `Policy`, `Event`, `Workflow` | DB write plus outbox row atomicity, relay may duplicate, receiver dedupes. Do not claim exactly-once delivery. |
| Saga compensation | Saga pattern docs. Evidence: [research.md §Agent 2](research.md#agent-2-event-message-explorer). | REROUTE to DomainSpec-first | `build-from-owned` | only boundary-trigger evidence and external participant references stay local | `Saga`, `Workflow`, `Event`, `Policy` | Failed step triggers named compensation. The compensation model itself is DomainSpec reuse, not a new IntegrationSpec primitive. |
| Delivery ordering and resequencing | EIP Message Sequence and Resequencer. Evidence: [research.md §Agent 2](research.md#agent-2-event-message-explorer). | GO after split from saga | `build-from-owned` | `sequence_id`, ordering key, resequence policy, lateness/window policy | `Event`, `Policy`, `Workflow` | Out-of-order messages require sequence key and resequence policy. Flag ordering required but no key. |
| Source-of-truth vs derived resource authority | AWS/Azure operational stores plus local database-selection refine pressure. Evidence: [research.md §Agent 3](research.md#agent-3-data-resource-cache-explorer). | GO with wording repair | `build-from-owned`; deployed examples only where named | authority boundary, freshness, failover, derived-consumer non-authority | `Operation`, `Query`, `Policy`, `Event`, `Workflow` | Operational source plus derived consumer. Pass: SoT named. Block: derived view is authority. |
| Cache-aside and stale-read handling | AWS ElastiCache and Azure Cache-Aside. Evidence: [research.md §Agent 3](research.md#agent-3-data-resource-cache-explorer). | GO / REPAIR wording | `build-from-owned` | stale-read fixture, fallback-to-SoT, invalidation/TTL evidence | `Policy`, `Query`, optional `Event` | Cache miss or stale read falls back to SoT. Flag missing TTL. Block cache as SoT. |
| Search/vector/read-model projection | OpenSearch, Azure AI Search, Redshift materialized views, Cosmos change feed. Evidence: [research.md §Agent 3](research.md#agent-3-data-resource-cache-explorer). | GO / REPAIR wording | `build-from-owned` | lineage anchor, rebuild owner, refresh/fallback/privacy propagation, non-authority constraint | `Query`, `Mapping`, `Policy`, `Workflow`, `Event` | Projection with `derived_from`, refresh/rebuild owner, lineage, and fallback. Block projection claimed as canonical source. |
| Migration command taxonomy and environment split | Prisma, Flyway, Liquibase, GitLab. Evidence: [research.md §Agent 4](research.md#agent-4-migration-operability-explorer). | GO | `build-from-owned` | command class, environment, drift precheck, lock/repair/destructive gates, operator runbook | mostly `Policy`; `Query` for readiness/status | Command matrix with `apply/status/repair/destructive`, dev/prod environment, block `reset/clean/drop` in production. |
| Expand/contract, backfill, and deploy-safe migration | GitLab strongest; Alembic and Django support schema/data split and reversibility pressure. Evidence: [research.md §Agent 4](research.md#agent-4-migration-operability-explorer). | GO / REPAIR wording | `build-from-owned`; GitLab staged migrations are deployed precedent | deploy-safe staging, backfill evidence, irreversible-change gate, forward recovery | `Workflow`, `Mapping`, `Policy` | Column or field rename: expand, staged read/write, background backfill, contract, forward recovery. |
| Combined L0 synthesis seed | Local refine outputs plus owned external precedents. Evidence: [research.md §Agent 2](research.md#agent-2-event-message-explorer), [§Agent 3](research.md#agent-3-data-resource-cache-explorer), [§Agent 4](research.md#agent-4-migration-operability-explorer). | HOLD, not L0 proof | `build-from-owned composite` | cross-boundary fixture composition and evidence anchors | all listed DomainSpec concepts | Keep only as a later composition-smoke candidate. It is too broad to be the discipline's first non-vacuity anchor. |

## Reviewer Corrections Applied

- Precedent gate: no candidate claims a new discipline. The matrix composes owned precedents into local examples.
- Non-vacuity gate: auth/signature and idempotent writes are split; saga compensation and ordering recovery are split; combined L0 synthesis is demoted to later composition smoke.
- Definitional-soundness gate: saga compensation stays DomainSpec-first; IntegrationSpec-local residue is boundary authority, directionality, trust, delivery semantics, derived-resource authority, and migration operability evidence.

## Recommended Input To Discipline Construction

Build the discipline around small fixtures first:

1. provider contract authority and version pinning;
2. callback vs webhook directionality;
3. signed webhook trust check;
4. idempotent mutating write;
5. async request/reply envelope;
6. CloudEvents-style event identity;
7. outbox plus idempotent receiver;
8. delivery ordering and resequencing;
9. source-of-truth vs derived resource authority;
10. cache-aside stale-read handling;
11. search/vector/read-model projection lineage;
12. migration command taxonomy and environment gates;
13. expand/contract plus backfill proof.

The payment/database composition should come later, after the narrow fixtures exist.

## Closeout

The dispatch resolved with repairs. `INTEGRATION-BOUNDARY-DISCIPLINE.md` should not be constructed from a single giant scenario; it should be constructed from the narrow, owner-backed fixture families above.
