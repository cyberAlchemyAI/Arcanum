# Refine Seed Proposal: Integration Spec

Status: strategy-proposal
Run ID: 20260616T144535Z-integration-spec-refine
Dispatch ID: refine-20260616T144535Z-integration-spec
Target: `arcanum/arcana/integration-spec`
Preset: full
Research mode: bounded-research
Operator intent: Create an Arcanum `integration-spec` that is like DomainSpec, but focused on integrations and application-layer decisions for databases, external APIs, cache, and system boundaries.

## Target Resolution

The target package does not yet exist. This run creates the target-local refinement evidence folder only:

`arcanum/arcana/integration-spec/development/refinement-runs/20260616T144535Z-integration-spec-refine/`

The proposed future package should be public-safe because it lives inside the public `arcanum` submodule. It must not contain private parent-workspace, client, implementation, or validation details.

## Underlying Problem

Teams need a system-agnostic way to choose, describe, test, and govern integration boundaries between application use cases and external systems without collapsing domain modeling, infrastructure vendor choices, runtime execution evidence, and application-layer contracts into one blurry artifact.

## Starting Hypothesis

Create `integration-spec` as an Arcanum arcana package that turns integration concerns into a governed spec surface:

- application-layer ports and use-case dependency contracts;
- adapter contracts for databases, external APIs, caches, queues, webhooks, files, and identity providers;
- selection records for data stores, cache strategies, and external API protocols;
- mapping, retry, idempotency, consistency, error, observability, and test obligations;
- links to existing standards such as OpenAPI, AsyncAPI, CloudEvents, and cloud architecture decision guides without replacing them.

## Local Evidence

- `arcanum/definitions/TAXONOMY.md` already names connective DomainSpec types: `Interface`, `Event`, `Mapping`, plus UI `Binding` and `Adapter`.
- `arcanum/definitions/RELATIONSHIPS.md` already covers `exposes`, `maps`, `fetches`, `mutates`, `contracts`, and `mirrors`.
- `arcanum/definitions/DEFINITIONS.md` fixes the canonical 25 meta-type and 29 edge vocabulary. New integration vocabulary should not silently mutate that canon.
- `arcanum/spells/invoke/templates/domainspec-spec/` provides the closest existing DomainSpec template family.
- `arcanum/formulae/dispatch-spec/development/TANDEM-INTEGRATION-OPTIONS.md` contains prior integration-adapter thinking, but it is specific to Tandem and Task Session runtime evidence, not a general IntegrationSpec package.
- The operator-supplied Two-Lane Discipline requires two research lanes: Lane Z builds the hypothesis through critique; Lane A challenges the underlying problem with a genuinely different solution.

## Bounded External Research Baseline

This is strategy evidence, not the canonical research stage result. The confirmed refine run should still produce a stage-owned research artifact.

| Source | Useful finding | IntegrationSpec implication |
| --- | --- | --- |
| OpenAPI Initiative, `https://www.openapis.org/` | OpenAPI is a formal standard for describing HTTP APIs and supports code generation, tests, documentation, and design standards. | Reuse OpenAPI for HTTP contract shape; IntegrationSpec should decide when an HTTP boundary needs OpenAPI and how it maps to ports, adapters, auth, errors, idempotency, and tests. |
| AsyncAPI Initiative, `https://www.asyncapi.com/` and docs | AsyncAPI targets event-driven APIs and treats the document as a communication contract between senders and receivers. | Reuse AsyncAPI for pub/sub or message channels; IntegrationSpec should govern event source/sink ownership, consumer obligations, retries, ordering, and dead-letter behavior. |
| CloudEvents, `https://cloudevents.io/` | CloudEvents standardizes event data metadata across services, platforms, and systems. | Reuse CloudEvents for event envelopes when interoperability matters; IntegrationSpec should say when CloudEvents is required and how domain events map into it. |
| Alistair Cockburn, Hexagonal Architecture, `https://alistair.cockburn.us/hexagonal-architecture` | Ports and adapters frame an inside application communicating over ports with outside actors/systems. | IntegrationSpec should guide the application layer through named ports and driven/driving adapters rather than vendor objects leaking inward. |
| Azure Architecture Center, Cache-Aside, `https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside` | Cache-aside loads data on demand from a data store and has consistency concerns. | IntegrationSpec needs cache strategy records: key ownership, source of truth, TTL, invalidation, consistency, stampede behavior, and test evidence. |
| Azure Architecture Center, choose data stores, `https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-stores-getting-started` | Data store choice should evaluate functional, performance, cost, and security requirements. | IntegrationSpec needs database selection records grounded in workload access patterns, consistency, query shape, latency, scaling, security, migrations, and operational ownership. |
| AWS Well-Architected database guidance | Purpose-built stores include relational, key-value, document, in-memory, graph, time-series, and ledger choices. | IntegrationSpec should record why a store family was selected and what compromise was accepted, not merely name the chosen technology. |
| Google Cloud Application Integration overview | Integration platforms connect applications, APIs, data sources, and third-party services for business operations. | IntegrationSpec should include an integration-workflow escape hatch, but keep lifecycle and domain authority in Arcanum rather than in a low-code/iPaaS platform. |

## Candidate Relationship To DomainSpec

IntegrationSpec should borrow the DomainSpec concept-graph discipline but not become a bigger DomainSpec taxonomy by accident.

Likely reuse:

- `Interface`: the boundary exposed to or consumed from another system.
- `Mapping`: transformations across boundary shapes.
- `Event`: integration facts or notifications crossing async boundaries.
- `Policy`: retry, routing, fallback, storage, cache, and reconciliation decisions.
- `Operation` and `Query`: application-layer use cases that depend on integration ports.
- `Workflow` and `Saga`: orchestration surfaces when multiple integration steps must be coordinated.
- `Binding` and `Adapter`: useful cross-layer vocabulary, but IntegrationSpec should generalize adapter obligations beyond UI boundaries.

Likely new local vocabulary, kept package-local until promoted:

- `Integration Port`: application-owned boundary contract.
- `Integration Adapter`: external-system implementation of a port.
- `Integration Resource`: external system capability or data source used by an adapter.
- `Integration Decision`: selection and trade-off record for protocol, data store, cache, queue, provider, or SDK.
- `Integration Policy`: retry, timeout, circuit breaker, idempotency, consistency, auth, rate-limit, cache, and reconciliation behavior.
- `Integration Evidence`: contract tests, schema validation, emulator tests, sandbox receipts, migration checks, and observability proof.

## Lane Z: Build The Hypothesis

Lane Z should build an IntegrationSpec shape with:

- package identity, objective, and public-safe scope;
- artifact family such as `INTEGRATION-SPEC.md`, `ports.md`, `adapters.md`, `resources.md`, `decisions.md`, `policies.md`, `mappings.md`, `evidence.md`;
- a minimum component catalog for database, API, cache, queue/event, file/blob, and identity integrations;
- examples showing application use case -> port -> adapter -> resource -> policy -> evidence;
- a counterexample, such as "cache-only read path with stale data" or "third-party API with webhook callback and idempotency key".

## Lane A: Challenge The Framing

Lane A must hold the underlying problem fixed and propose a different solution, such as:

- do not create a new arcana package; instead extend DomainSpec templates with an `integrations.md` aspect;
- create a formula-level `integration-contract` validator rather than an arcana sigil;
- treat integration work as `implementation-layering` or `task-session` adapter guidance;
- rely on OpenAPI/AsyncAPI/CloudEvents plus Architecture Decision Records and only add Arcanum crosswalk templates.

Lane A should reject any alternative that is only a renamed IntegrationSpec.

## Desired Output After Confirmed Run

A final `RESULT.md` that recommends one of:

1. `integration-spec` as a new arcana package;
2. a smaller transmutation/formula package;
3. a DomainSpec template extension;
4. no new package, only crosswalk guidance to existing standards.

The result must include:

- proposed package tier and owner;
- spec artifact family;
- local vocabulary and which terms stay unpromoted;
- DomainSpec taxonomy reuse map;
- external standard reuse map;
- application-layer guidance surface;
- validation and test evidence surface;
- non-executed implementation plan or follow-up route.

## Write Scope

Allowed now:

- refine evidence under `arcanum/arcana/integration-spec/development/refinement-runs/20260616T144535Z-integration-spec-refine/`.

Deferred until confirmed route or a later task session:

- creating `arcanum/arcana/integration-spec/SKILL.md`;
- changing `arcanum/definitions/DEFINITIONS.md`;
- changing `arcanum/definitions/TAXONOMY.md`;
- changing DomainSpec templates;
- generating native runtime skill mirrors.

## Done Criteria For This Proposal Step

- Seed proposal is written.
- Dispatch route is written and validator-checked.
- Runtime handoff records that execution and subagents require user confirmation.
- Manifest and evidence index exist.
- Response asks for confirmation before running native stages or spawning subagents.
