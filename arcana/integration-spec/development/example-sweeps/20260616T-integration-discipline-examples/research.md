# Integration Discipline Example Sweep Research

Dispatch ID: `2026-06-16-integration-discipline-example-sweep`
Status: collected explorer returns

Note: returns are preserved as collected, with absolute local checkout paths normalized to repo-relative public artifact paths.

## Agent 1: External API Contract Explorer

I read the three local refine results first. The pressure is consistent: host-owned port, explicit external boundary, provider auth/rate-limit/idempotency policy, async callback/webhook shape, failure contract, and evidence anchors. Based on that, here is the compact precedent sweep.

| Owned example | Owner / source | IntegrationSpec field pressure | DomainSpec reuse | L0 fixture candidate | Use-mode | Risks / residue |
|---|---|---|---|---|---|---|
| OpenAPI callback registration with caller-supplied `callbackUrl` and provider callback path expansion | OpenAPI Initiative callback example: https://learn.openapis.org/examples/v3.0/callback-example.html | `host_port`, `callback_registration`, `callback_url_origin`, `event_payload_contract`, `ack_response`, `failure_contract` | `Interface`, `Operation`, `Event`, `Mapping`, `Policy` | Pass: registration op plus callback contract. Flag: callback URL accepted but not modeled. Block: callback behavior only in prose. | `build-from-owned` | Good precedent for modeling out-of-band provider calls, but it is a spec example, not proof of one provider's operational behavior. |
| OpenAPI webhooks as first-class provider-initiated requests, distinct from callbacks | OpenAPI 3.2 spec `webhooks`: https://spec.openapis.org/oas/v3.2.0.html and guide: https://learn.openapis.org/specification/webhooks.html | `webhook_contract`, `provider_initiated_request`, `consumer_ack`, `out_of_band_registration`, `event_family` | `Event`, `Interface`, `Policy`, `Workflow` | Pass: separate webhook template section. Flag: webhook described but registration missing. Block: webhook collapsed into ordinary response docs. | `build-from-owned` | Strong shape precedent. Residue: OAS 3.2 is newer than many deployed provider descriptions, so adoption choice should be explicit. |
| OpenAPI links and runtime expressions for response-to-next-operation wiring | OpenAPI 3.1.1 `operationRef` guidance: https://spec.openapis.org/oas/v3.1.1.html and link example: https://learn.openapis.org/examples/v3.0/link-example.html | `follow_on_operation`, `response_binding`, `runtime_expression`, `operation_ref`, `multi_step_flow` | `Workflow`, `Saga`, `Operation`, `Mapping` | Pass: response field bound to next call input. Flag: sequence exists only narratively. Block: hidden coupling between calls with no declared link. | `build-from-owned` | Useful for L0 examples where one provider response drives another step; still HTTP-description-centric, not full orchestration proof. |
| OpenAPI security schemes plus per-operation override | OpenAPI security guide: https://learn.openapis.org/specification/security.html | `auth_scheme`, `auth_location`, `global_vs_operation_override`, `scopes_or_permissions`, `optional_auth` | `Policy`, `Interface`, `Operation` | Pass: explicit scheme plus operation overrides. Flag: auth mentioned but not machine-readable. Block: secrets/auth mechanism implied only by examples. | `build-from-owned` | Excellent for contract clarity; does not itself model provider key rotation, quota, or tenancy behavior. |
| OpenAPI examples as contract fixtures, not just docs | OpenAPI docs/examples guide: https://learn.openapis.org/specification/docs.html | `example_request`, `example_response`, `negative_fixture`, `mockability`, `evidence_anchor` | `Mapping`, `Interface`, `Operation` | Pass: request/response examples per operation. Flag: happy-path only. Block: no concrete examples for high-risk boundary cases. | `build-from-owned` | Strong L0 fixture pattern. Residue: examples can drift unless tied to validation or recorded receipts. |
| GitHub REST API published as versioned OpenAPI descriptions | GitHub OpenAPI description: https://docs.github.com/en/rest/about-the-rest-api/about-the-openapi-description-for-the-rest-api and API versions: https://docs.github.com/rest/overview/api-versions | `provider_openapi_source`, `api_version_header`, `deployment_variant`, `breaking_change_surface`, `product_variant` | `Interface`, `Operation`, `Policy` | Pass: provider spec source plus required version header. Flag: provider versioning acknowledged but not pinned. Block: integration assumes unversioned provider behavior. | `already-deployed` | Very good precedent for external source authority. Residue: version cadence and product variants must be tracked outside pure schema shape. |
| GitHub repository webhooks with fine-grained token permissions and signature validation | Webhook endpoints: https://docs.github.com/en/rest/repos/webhooks ; validation: https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries | `webhook_registration`, `provider_permissions`, `webhook_secret`, `signature_validation`, `delivery_authenticity`, `replay_handling` | `Event`, `Policy`, `Interface` | Pass: registration plus secret plus signature validation. Flag: webhook exists but trust check omitted. Block: webhook consumer processes unsigned payloads. | `already-deployed` | Strong operational precedent. Residue: delivery retry/redelivery semantics should be modeled separately if they matter to reconciliation. |
| GitHub auth and categorized rate limits | Auth: https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api ; rate limits: https://docs.github.com/en/rest/rate-limit/rate-limit | `credential_kind`, `required_permissions`, `authorization_header`, `rate_limit_category`, `quota_probe`, `backoff_policy` | `Policy`, `Operation` | Pass: token type plus permission mapping plus quota check. Flag: generic auth only. Block: no explicit rate-limit handling for polling/search-heavy paths. | `already-deployed` | Good precedent for policy fields that are provider-specific but stable. Residue: docs show categories and auth shape, not the app's retry budget decisions. |
| Stripe API key auth plus idempotent write contract | Auth: https://docs.stripe.com/api/authentication ; idempotency: https://docs.stripe.com/api/idempotent_requests | `auth_scheme`, `secret_handling`, `idempotency_key`, `idempotency_scope`, `parameter_match_rule`, `retry_policy` | `Policy`, `Operation`, `Interface` | Pass: mutating call includes idempotency strategy. Flag: retries exist but key strategy absent. Block: duplicate-prone create/update flow with no idempotency field. | `already-deployed` | One of the clearest owned precedents for write-side idempotency. Residue: exact semantics are Stripe-specific, so copy field shape, not the whole behavioral claim. |
| Stripe webhook endpoint plus documented provider limits | Webhooks: https://docs.stripe.com/webhooks ; rate limits: https://docs.stripe.com/rate-limits | `async_event_contract`, `secure_endpoint`, `event_destination`, `provider_limit_budget`, `burst_handling`, `fetch_after_event_policy` | `Event`, `Policy`, `Workflow` | Pass: webhook handler plus secure endpoint plus quota-aware follow-up calls. Flag: webhook modeled but no throughput budget. Block: event-driven flow that ignores provider request ceilings. | `already-deployed` | Strong precedent for pairing async delivery with quota policy. Residue: docs are broad; exact per-flow saturation behavior still needs local fixture design. |
| Google/gRPC HTTP transcoding and metadata-based auth boundary | AIP-127: https://google.aip.dev/127 ; Cloud Endpoints transcoding: https://docs.cloud.google.com/endpoints/docs/grpc/transcoding ; gRPC auth/metadata: https://grpc.io/docs/guides/auth/ and https://grpc.io/docs/guides/metadata/ | `rpc_to_http_mapping`, `resource_path_template`, `transcoding_rule`, `channel_security`, `metadata_contract`, `streaming_exception` | `Interface`, `Operation`, `Mapping`, `Policy` | Pass: explicit RPC plus HTTP mapping. Flag: REST facade over gRPC with no declared transcoding rule. Block: bidi-streaming dependency with no HTTP-safe alternative. | `already-deployed` | Best precedent for REST/gRPC boundary discipline. Residue: once streaming enters, HTTP parity becomes partial by design. |

L0 takeaways:

1. Treat provider contract authority as layered, not singular: provider OpenAPI/proto, provider auth docs, provider webhook docs, provider rate-limit docs.
2. Separate `callback` from `webhook`: callback is operation-tied and caller-parameterized; webhook is provider-initiated from prior registration or configuration.
3. Make `Policy` carry provider-specific operational rules explicitly: auth kind, permissions/scopes, idempotency, quota category, backoff, signature validation, replay stance.
4. Require at least one fixture per risky boundary class: auth failure, quota/429, duplicate delivery, invalid signature, stale follow-up read, idempotent retry, version-header omission, transcoding mismatch.

Most reusable pressure for DomainSpec is still `Interface`, `Operation`, `Mapping`, `Policy`, `Event`, and `Workflow`/`Saga`. The part that still wants IntegrationSpec-local handling is boundary machinery itself: provider contract source, registration surface, callback/webhook directionality, trust checks, version pinning, rate-limit/idempotency rules, and evidence anchors.

## Agent 2: Event Message Explorer

Here is a compact event/message precedent sweep for the Integration Boundary Discipline pass. I am treating the three refine outputs as local pressure, and everything else below as owner-run source material to borrow from carefully rather than as proof of local deployment.

| Owned example | Owner/source URL or local path | IntegrationSpec field pressure | DomainSpec reuse | L0 fixture candidate | Use-mode | Risks/residue |
|---|---|---|---|---|---|---|
| AsyncAPI request/reply `ping` to `pong`, with operation bound to channel and optional dynamic `replyTo` | AsyncAPI docs: https://www.asyncapi.com/docs/tutorials/getting-started/request-reply and spec ref https://www.asyncapi.com/docs/reference/specification/v3.1.0 | `operation_kind`, `channel_address`, `message_ref`, `reply_channel`, `reply_address_source`, `header_contract` | `Operation`, `Interface`, `Mapping`, `Policy` | Pass: request message carries `replyTo`, responder sends on declared reply channel. Flag: reply channel exists but address source undocumented. Block: runtime reply address with no modeled source/header. | build-from-owned | Good for contract shape; does not itself solve delivery guarantees, retries, or dedupe. |
| AsyncAPI message = payload plus metadata/headers | AsyncAPI message docs: https://www.asyncapi.com/docs/concepts/message | `payload_schema`, `header_schema`, `message_role` (event/command/query), `transport_metadata` | `Event`, `Operation`, `Mapping` | Pass: same payload under different header contracts. Flag: payload modeled but headers omitted. | build-from-owned | Helpful for envelope discipline, but AsyncAPI alone does not tell you which metadata must be business vs transport vs evidence. |
| CloudEvents context attributes separated from event `data`; `source` plus `id` unique per distinct event; `subject` useful for middleware filtering | CloudEvents spec: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md and primer: https://github.com/cloudevents/spec/blob/main/cloudevents/primer.md | `event_context`, `event_data`, `event_id`, `event_source`, `event_type`, `subject/filter_key`, `dataschema`, `datacontenttype` | `Event`, `Mapping`, `Policy` | Pass: filter/routing can inspect `subject` without deserializing payload. Flag: identifier lives only in payload. Block: no stable event identity for replay/duplicate detection. | build-from-owned | Strong envelope precedent, but CloudEvents is event-format guidance, not a whole integration operating model. |
| EIP Envelope Wrapper | Enterprise Integration Patterns: https://www.enterpriseintegrationpatterns.com/patterns/messaging/EnvelopeWrapper.html | `envelope_contract`, `wrapped_payload`, `transport_headers`, `unwrap_policy`, `compatibility_mode` | `Mapping`, `Policy`, `Interface` | Pass: domain payload wrapped to satisfy broker/webhook constraints. Flag: wrapper exists but unwrap/validation owner unclear. | build-from-owned | Useful when infra demands extra headers/signature fields; easy to over-wrap and hide domain meaning. |
| EIP Idempotent Receiver | Enterprise Integration Patterns: https://www.enterpriseintegrationpatterns.com/patterns/messaging/IdempotentReceiver.html | `dedupe_strategy`, `idempotency_key`, `receiver_effect_model`, `replay_behavior` | `Policy`, `Event`, `Operation` | Pass: same message twice, same effect once. Flag: handler is retry-safe but no explicit key source. Block: non-idempotent side effects behind at-least-once delivery. | build-from-owned | Pattern says what property you need, not which storage/key/window to use. |
| Transactional Outbox: write business state and outbox in one transaction; relay may publish twice; ordering preserved from app to broker | Microservices.io: https://microservices.io/patterns/data/transactional-outbox.html | `publish_atomicity_mode`, `outbox_store`, `relay_owner`, `ordering_scope`, `duplicate_delivery_residue`, `consumer_idempotency_requirement` | `Policy`, `Event`, `Workflow` | Pass: DB commit produces exactly one outbox record and relay emits in app order. Flag: outbox exists but relay duplication residue undocumented. Block: direct publish plus DB write with no atomicity story. | build-from-owned | Gives a concrete answer for atomic publish, but explicitly leaves duplicate delivery residue for consumers. |
| Idempotent Consumer under at-least-once delivery | Microservices.io: https://microservices.io/patterns/communication-style/idempotent-consumer.html | `delivery_semantics`, `consumer_dedupe_store`, `processed_message_record`, `retry_contract` | `Policy`, `Event`, `Workflow` | Pass: repeated broker delivery does not duplicate effects. Flag: at-least-once assumed but no consumer receipt store. | build-from-owned | Complements outbox well; still leaves retention/window questions open. |
| Saga with compensating transactions; choreography or orchestration | Microservices.io: https://microservices.io/patterns/data/saga.html | `saga_steps`, `coordination_mode`, `compensation_steps`, `failure_trigger`, `terminal_states` | `Workflow`, `Saga`, `Event`, `Policy` | Pass: failing step triggers named compensation path. Flag: multi-step workflow exists but undo path unspecified. Block: distributed transaction implied with no local-step/compensation model. | build-from-owned | Strong precedent for long-running consistency, but compensation semantics remain domain-specific. |
| Ordering recovery via sequence tagging plus resequencing | EIP Message Sequence plus Resequencer: https://www.enterpriseintegrationpatterns.com/patterns/messaging/MessageSequence.html and https://www.enterpriseintegrationpatterns.com/patterns/messaging/Resequencer.html | `sequence_id`, `position`, `ordering_key`, `resequence_policy`, `lateness/window_policy` | `Event`, `Policy`, `Workflow` | Pass: out-of-order messages can be reassembled by sequence metadata. Flag: ordering required but no ordering key. | build-from-owned | Only needed where order matters; adds state, buffering, and latency. |
| Cross-source synthesis from local refine runs: boundary record plus message/event policy plus evidence anchors | Local: `arcanum/arcana/integration-spec/development/refinement-runs/20260616T144535Z-integration-spec-refine/RESULT.md`, `arcanum/arcana/integration-spec/development/refinement-runs/20260616T203246Z-openclaw-sdk-integration-refine/RESULT.md`, `arcanum/arcana/integration-spec/development/refinement-runs/20260616T204823Z-database-selection-migration-commands-refine/RESULT.md` | At minimum: `boundary_kind`, `resource_or_channel`, `message/event contract`, `policy surface`, `failure contract`, `evidence anchors` | `Operation`, `Interface`, `Mapping`, `Event`, `Policy`, `Workflow`, `Saga`, `Query` | Payment-style fixture: API call writes state, outbox emits event, webhook/event may duplicate, consumer dedupes, stale cache reconciles, failed downstream step compensates. | novel-attempt | This is the likely L0 discipline shape, but it is still synthesis, not an owned standard by itself. |

Takeaways:

- `AsyncAPI` pressures channel/operation/reply/header contract fields.
- `CloudEvents` pressures context-vs-data and stable event identity/filtering fields.
- `EIP` pressures envelope, dedupe, and resequencing tactics.
- `Transactional outbox` and `idempotent consumer` pressure atomic publish, duplicate-delivery residue, and receiver-side safety.
- `Saga` pressures explicit compensation and terminal failure handling.

I do not have proof from the supplied local materials that one single combined event discipline is already deployed locally. The safe reading is: the local refine work asks for a discipline that borrows these precedents, not one that claims one already exists.

## Agent 3: Data Resource Cache Explorer

Below is a compact sweep. I am only making claims the owner docs or the three local refine outputs directly support; the `DomainSpec reuse` column is the inference layer.

Local pressure from the refine inputs:

- `integration-spec-refine/RESULT.md` says the L0 envelope has to cover cache-aside stale reads, duplicate delivery, idempotency, reconciliation, and proof/evidence without mutating taxonomy yet.
- `database-selection-migration-commands-refine/RESULT.md` explicitly pressures `resource_role`, `resource_family`, `source_of_truth_role`, `consistency_model`, `retention_lifecycle`, `failure_modes`, `evidence_anchors`, plus extra fields for cache/search/vector/analytics: freshness, rebuild, lineage, privacy propagation, fallback.
- `openclaw-sdk-integration-refine/RESULT.md` adds the discipline that evidence anchors and failure fixtures matter, but runtime receipts do not become canonical truth.

| Owned example | Owner/source | IntegrationSpec field pressure | DomainSpec reuse | L0 fixture candidate | Use-mode | Risks / residue |
|---|---|---|---|---|---|---|
| Amazon DynamoDB as operational store | AWS DynamoDB: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html | `resource_role=operational_source`; `resource_family=key-value/document`; consistency plus ACID scope plus CDC plus backup/restore plus multi-region/failover semantics | `Operation`/`Query` for access intent; `Policy` for consistency, backup, failover; `Event`/`Workflow` for Streams consumers | `pass`: SoT named, CDC consumers non-authoritative. `block`: cache/search/read-model presented as authority over DynamoDB | already-deployed | Global tables are multi-active, so primary language can become misleading; zero-ETL/search adjacencies are derived, not SoT |
| Azure SQL Database as relational SoT | Azure SQL Database: https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview?view=azuresql | `resource_family=relational`; HA/SLA, backups, PITR, read-heavy replica use, workload tiering | `Operation`/`Query`; `Policy` for backup, restore, retention, read-offload; `Mapping` for schema/query shape | `pass`: write authority and restore policy explicit. `flag`: read replicas used without freshness statement | already-deployed | Good operational authority precedent, but read replicas and analytical offload still need explicit freshness/non-authority language |
| ElastiCache lazy loading / write-through / TTL | AWS ElastiCache strategies: https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html | `resource_role=cache`; freshness, TTL, invalidation, empty-node behavior, fallback-to-database, cache churn | `Policy` dominates; `Query` for read path; `Event` only if invalidation is evented | `block`: cache marked SoT or no fallback path. `flag`: no TTL / stale-read handling | build-from-owned | AWS docs are explicit that lazy loading can go stale; write-through helps freshness but still has empty-node gaps |
| Azure Managed Redis with cache-aside | Azure Managed Redis overview: https://learn.microsoft.com/en-us/azure/redis/overview, Azure Cache-Aside pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside | `resource_role=cache`; expiration/eviction, consistency gap, shared-vs-local cache, HA mode, clustering compatibility if relevant | `Policy` for expiration/eviction/HA; `Query` for miss path; `Interface` if multiple app instances share cache | `block`: cache has no invalidation/expiration or is treated as authority. `flag`: local cache used without multi-instance consistency note | build-from-owned | Microsoft's current direction is Azure Managed Redis; cache-aside explicitly does not guarantee consistency |
| Amazon OpenSearch vector search | Amazon OpenSearch vector search: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/vector-search.html | `resource_role=search/vector`; embedding provenance, index refresh/rebuild owner, query mode, fallback when index is cold/stale | `Query` for retrieval intent; `Mapping` for source-to-index transforms; `Policy` for rebuild and stale results | `block`: vector index declared canonical source. `flag`: no rebuild path from owned corpus | already-deployed | Direct proof supports semantic retrieval, not source-of-truth authority; discipline should force lineage back to owned source data |
| Azure AI Search vector plus hybrid search | Azure AI Search vector search: https://learn.microsoft.com/en-us/azure/search/vector-search-overview | `resource_role=search/vector`; integrated-vs-external vectorization, hybrid retrieval, source connectors/indexers, service-version capability | `Query`; `Mapping`; `Policy` for embedding generation, reindex, and fallback to keyword/operational source | `block`: no source corpus lineage or no reindex plan. `flag`: old service assumed vector-capable without evidence | already-deployed | Docs support hybrid/vector retrieval and integrated vectorization, but still as an index layer, not the operational authority |
| Amazon Redshift materialized view as read-model / analytics projection | Redshift materialized views overview: https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-overview.html, refresh behavior: https://docs.aws.amazon.com/redshift/latest/dg/materialized-view-refresh.html | `resource_role=analytics/read_model`; freshness SLA, manual/incremental/full refresh, lineage to base tables, nested refresh ordering | `Query`; `Mapping`; `Workflow`/`Event` if refresh is orchestrated | `block`: MV treated as always-current without refresh policy. `flag`: nested MV with no cascade owner | already-deployed | Redshift docs are clear that contents stay unchanged until refresh; good precedent for derived, fast, non-authoritative unless refreshed |
| Azure Cosmos DB change feed plus analytical store / materialized view pattern | Cosmos DB overview: https://learn.microsoft.com/en-us/azure/cosmos-db/overview, change feed design patterns: https://learn.microsoft.com/en-us/azure/cosmos-db/change-feed-design-patterns, CQRS pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs | `resource_role=projection/search/cache/analytics feeder`; lineage, near-real-time not exact-current, change-feed consumer ownership, isolated analytical store, fallback to operational container | `Event`; `Workflow`; `Query`; `Policy` for projection freshness and privacy propagation | `pass`: change feed updates cache/search/warehouse as derived targets. `block`: analytical store or projection claimed as the write authority | build-from-owned | Strong precedent for rebuildable projections. Current Cosmos overview also says OLAP is a poor fit for the operational store itself, so authority should stay with the operational container, not the analytical projection |

What this most strongly suggests for Integration Boundary Discipline L0:

1. Make `source_of_truth_role` mandatory and require every cache/search/vector/analytics resource to say `derived_from`.
2. Add mandatory derived-resource fields: `freshness_policy`, `rebuild_owner`, `lineage_anchor`, `fallback_behavior`, `privacy_propagation`.
3. Treat cache/search/vector/read-model resources as fast views by default; they only stop being just a view if the spec proves write authority explicitly.
4. Add explicit fixtures for cache marked authoritative, vector/search index with no source lineage, read-model with no refresh contract, analytics store used as operational truth, and fallback omitted on cache/search/vector miss or staleness.

## Agent 4: Migration Operability Explorer

Compact sweep, scoped to owner docs and the local owned refine results.

1. GitLab: regular vs post-deploy vs batched background.

- Owned example: three migration classes with timing and feature-flag guidance.
- Source: GitLab migration style guide: https://docs.gitlab.com/development/migration_style_guide/
- IntegrationSpec field pressure: `command_class`, `apply_policy`, `environment`, `expand_contract_stage`, `backfill_plan`, `evidence_fixtures`.
- DomainSpec reuse: `Policy` for deploy gating and timing; `Workflow/Event` for scheduled background execution.
- L0 fixture candidate: `flag` if a long-running critical change lacks `post_deploy + feature_flag`; `block` if background migration changes schema.
- Use-mode: `build-from-owned`.
- Risks/residue: GitLab's class split is Rails/Sidekiq-specific; reuse the discipline, not the exact runtime labels.

2. GitLab: zero-downtime rename / expand-contract by milestone.

- Owned example: column rename uses a regular migration, ignore rule, post-deploy cleanup, then later removal; large tables escalate to batched background migrations across milestones.
- Source: https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/ and https://docs.gitlab.com/development/database/post_deployment_migrations/
- IntegrationSpec field pressure: `expand_contract_stage`, `destructive_gate`, `rollback_or_roll_forward_policy`, `backfill_plan`, `approval_record`.
- DomainSpec reuse: `Mapping` for old/new field duality; `Policy` for deprecation and removal windows.
- L0 fixture candidate: payment-table rename with `expand`, `dual-write/dual-read`, `background backfill`, `contract`.
- Use-mode: `already-deployed`.
- Risks/residue: proof is strong for staged removal; less direct for non-relational resources.

3. GitLab: operability before upgrade.

- Owned example: upgrades require batched background migrations to be `Finished`; docs provide UI/SQL status checks, pause/resume, retry.
- Source: https://docs.gitlab.com/update/background_migrations/ and https://docs.gitlab.com/update/zero_downtime/
- IntegrationSpec field pressure: `drift_precheck`, `evidence_fixtures`, `operator_runbook`, `environment_policy`.
- DomainSpec reuse: `Query` for readiness/status checks; `Policy` for upgrade preconditions.
- L0 fixture candidate: `block` production upgrade when migration-status proof is missing or incomplete.
- Use-mode: `build-from-owned`.
- Risks/residue: strongly supports no deploy without readiness proof; less about generic rollback semantics.

4. Prisma: explicit env split plus expand/contract.

- Owned example: `migrate dev` and `reset` for development, `deploy/status/resolve` for production; official expand/contract walkthrough; advisory locking on production commands.
- Source: https://www.prisma.io/docs/cli/migrate , https://www.prisma.io/docs/cli/migrate/deploy , https://www.prisma.io/docs/cli/migrate/status , https://www.prisma.io/docs/cli/migrate/resolve , https://www.prisma.io/docs/orm/prisma-migrate/workflows/customizing-migrations , https://www.prisma.io/docs/orm/prisma-migrate/workflows/development-and-production
- IntegrationSpec field pressure: `environment`, `command_class`, `drift_precheck`, `lock_policy`, `rollback_or_roll_forward_policy`, `expand_contract_stage`.
- DomainSpec reuse: `Policy` for environment separation and hotfix repair; `Mapping` for copy/backfill semantics.
- L0 fixture candidate: `block` `reset` in production; `flag` when a hotfix/failed migration lacks `resolve` evidence.
- Use-mode: `build-from-owned`.
- Risks/residue: Prisma supports reconcile/repair of migration history, but that is not proof that arbitrary data rollback is safe.

5. Flyway: strong command taxonomy, destructive gates, drift/repair.

- Owned example: command catalog (`migrate`, `info`, `validate`, `repair`, `baseline`, `clean`); `validate` checks checksum/name/type drift; `repair` mutates schema history; `clean` is explicitly unsafe for production; migrations-based deploys lock the schema history table.
- Source: https://documentation.red-gate.com/flyway/reference/commands , https://documentation.red-gate.com/fd/validate-277578898.html , https://documentation.red-gate.com/fd/repair-277578892.html , https://documentation.red-gate.com/fd/clean-277578871.html , https://documentation.red-gate.com/flyway/deploying-database-changes-using-flyway/rolling-out-updates-from-a-single-schema-to-multiple-production-databases
- IntegrationSpec field pressure: `command_class`, `schema_history_resource`, `drift_precheck`, `lock_policy`, `destructive_gate`, `repair_gate`.
- DomainSpec reuse: `Policy` only; history table and repair semantics are integration-boundary machinery, not domain meaning.
- L0 fixture candidate: `block` `clean`; `flag` `repair` unless same-locations proof and operator approval exist.
- Use-mode: `build-from-owned`.
- Risks/residue: Flyway's history-table model fits SQL engines well; less portable to systems without an equivalent ledger.

6. Liquibase: single-run lock, status/diff/update/rollback, explicit lock release.

- Owned example: `update`, `validate`, `status`, `diff`, `rollback`, `release-locks`; `DATABASECHANGELOGLOCK` enforces one runner at a time; poll/wait params are documented.
- Source: https://docs.liquibase.com/secure/reference-guide-5-1-1/init-update-and-rollback-commands/update , https://docs.liquibase.com/secure/reference-guide-5-2/database-inspection-change-tracking-and-utility-commands/validate , https://docs.liquibase.com/secure/reference-guide-5-1-1/database-inspection-change-tracking-and-utility-commands/status , https://docs.liquibase.com/secure/reference-guide-5-1-1/database-inspection-change-tracking-and-utility-commands/diff , https://docs.liquibase.com/secure/reference-guide-5-1-1/init-update-and-rollback-commands/rollback , https://docs.liquibase.com/secure/reference-guide-5-1-1/database-inspection-change-tracking-and-utility-commands/release-locks , https://docs.liquibase.com/secure/user-guide-5-2/what-is-the-database-changelog-lock-table
- IntegrationSpec field pressure: `lock_policy`, `lock_release_policy`, `drift_precheck`, `rollback_or_roll_forward_policy`, `command_class`, `operator_runbook`.
- DomainSpec reuse: `Policy` for concurrency and approval; `Query` for status/diff checks.
- L0 fixture candidate: `flag` stale lock with no release procedure; `block` rollback command use without tag/target proof.
- Use-mode: `build-from-owned`.
- Risks/residue: Liquibase has richer rollback surfaces than some tools, but rollback safety still depends on change type and data semantics.

7. Alembic: schema-first, data migration skepticism, separate script option.

- Owned example: docs say Alembic is designed for schema migrations; data migrations often should be separate; online migration means dual-version schema plus background copy; `check` and `stamp` exist; custom commands are supported.
- Source: https://alembic.sqlalchemy.org/en/latest/cookbook.html , https://alembic.sqlalchemy.org/en/latest/api/commands.html
- IntegrationSpec field pressure: `command_class`, `backfill_plan`, `expand_contract_stage`, `rollback_or_roll_forward_policy`, `custom_command_surface`.
- DomainSpec reuse: `Workflow` for staged schema-to-script-to-constraint flow; `Policy` for when data migration must leave the core migration tool.
- L0 fixture candidate: `flag` if a large data rewrite is embedded as if it were ordinary schema migration.
- Use-mode: `build-from-owned`.
- Risks/residue: good precedent for keeping schema versioning and data backfill distinct; weaker as a full operability model by itself.

8. Django: versioned migration files, reversible/unreversible, non-atomic batch backfill.

- Owned example: command set (`makemigrations`, `migrate`, `sqlmigrate`, `showmigrations`); `migrate --fake-initial`; explicit reversal and `IrreversibleError`; non-atomic migrations with chunked `RunPython`.
- Source: https://docs.djangoproject.com/en/6.0/topics/migrations/ , https://docs.djangoproject.com/en/6.0/ref/django-admin/ , https://docs.djangoproject.com/en/6.0/howto/writing-migrations/
- IntegrationSpec field pressure: `command_class`, `baseline_or_stamp_policy`, `rollback_or_roll_forward_policy`, `backfill_plan`, `transaction_policy`.
- DomainSpec reuse: `Policy` for reversible vs irreversible operations; `Workflow` for staged application/backfill.
- L0 fixture candidate: `flag` irreversible migration without explicit forward-recovery plan; `flag` large backfill left atomic.
- Use-mode: `build-from-owned`.
- Risks/residue: Django proves need for irreversibility classification, but command shapes are framework-specific.

9. Local owned seed: Integration Boundary Discipline refine outputs.

- Owned example: local refine already asks for `Database Migration Command Profile`, `lock_policy`, `drift_precheck`, `destructive_gate`, `rollback_or_roll_forward_policy`, `backfill_plan`.
- Source: `arcanum/arcana/integration-spec/development/refinement-runs/20260616T204823Z-database-selection-migration-commands-refine/RESULT.md`, plus companion refine results.
- IntegrationSpec field pressure: confirms external precedents are converging on the same L0 field set.
- DomainSpec reuse: `Operation`, `Query`, `Mapping`, `Policy`, `Workflow`, `Saga`, `Event` remain reuse surface; command machinery stays local to the discipline.
- L0 fixture candidate: one matrix with `pass/flag/block` for `reset/clean/drop`, `repair/release-locks/resolve/stamp/fake`, missing drift proof, and missing backfill proof.
- Use-mode: `novel-attempt`.
- Risks/residue: this is still a design seed, not deployed proof.

Small synthesis:

The strongest owned precedent is not one migration command model, but a consistent split:

1. normal apply commands
2. readiness/drift/status commands
3. repair/reconcile commands
4. destructive commands
5. long-running backfill paths
6. environment-specific policy

That looks like the right spine for Integration Boundary Discipline L0.
