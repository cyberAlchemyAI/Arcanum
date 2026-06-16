# Invoke Define: Integration Boundary Capability

Status: pass
Mode: define
Capability: `invoke`

## Defined Intent

Create a public-safe integration-boundary capability for Arcanum that helps teams decide, document, test, and govern how application use cases interact with external systems.

The capability must guide what clean architecture would call the application layer: the use case names what it needs, a port expresses the dependency, an adapter satisfies the port, and external systems remain outside the core.

## Scope

In scope:

- database selection and handling;
- external API contracts and provider boundaries;
- cache strategy and stale-data behavior;
- events, webhooks, queues, and async contracts;
- mappings between domain and external shapes;
- retry, timeout, idempotency, rate-limit, circuit-breaker, consistency, and reconciliation policies;
- test and evidence obligations.

Out of scope for this run:

- implementing a new package;
- changing canonical definitions;
- replacing OpenAPI, AsyncAPI, CloudEvents, or existing DomainSpec templates.

## Candidate Output Family

The new-package hypothesis would use:

- `INTEGRATION-SPEC.md`
- `ports.md`
- `adapters.md`
- `resources.md`
- `decisions.md`
- `policies.md`
- `mappings.md`
- `evidence.md`
- `standards-crosswalk.md`

The alternative route would split this into:

- an Integration Boundary Discipline card;
- a DomainSpec `integrations.md` aspect;
- a formula-level integration contract validator;
- a standards crosswalk.

## Template Selection

No existing template family fully owns this. DomainSpec templates cover feature specs, interfaces, mappings, and concept registries, but not provider/resource selection, cache/source-of-truth decisions, or evidence/proof relationships.

Verdict: candidate family required.

## Unresolved Gaps

- Whether the owner should be a new arcana sigil, discipline-governance, a DomainSpec template extension, or a formula validator.
- Whether package-local terms such as `Integration Port` and `Integration Evidence` eventually deserve canonical definition promotion.
