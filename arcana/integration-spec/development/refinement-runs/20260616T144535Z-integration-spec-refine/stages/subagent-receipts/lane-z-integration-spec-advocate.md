# Subagent Receipt: Lane Z IntegrationSpec Advocate

Agent ID: `019ed0ed-949b-7b63-a637-21fb4c7ef231`
Role ID: `lane-z-integration-spec-advocate`
Status: pass_with_residue
Spawn status: spawned
Join status: completed
Close status: closed

## Artifacts Considered

- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `RUN-MANIFEST.md`
- `RUNTIME-HANDOFF.md`
- `evidence-index.json`
- `RESULT.md`
- `arcanum/definitions/DEFINITIONS.md`
- `arcanum/definitions/TAXONOMY.md`
- `arcanum/definitions/RELATIONSHIPS.md`
- `arcanum/spells/invoke/templates/domainspec-spec/`
- `arcanum/formulae/dispatch-spec/development/TANDEM-INTEGRATION-OPTIONS.md`

## Receipt

Lane Z built the strongest new-package hypothesis: `integration-spec` should be a public Arcanum arcana package only if it owns coordination across multiple integration concerns: ports, adapters, external resources, decisions, policies, mappings, evidence, and repair loops.

Minimum artifact family:

- `INTEGRATION-SPEC.md`
- `ports.md`
- `adapters.md`
- `resources.md`
- `decisions.md`
- `policies.md`
- `mappings.md`
- `evidence.md`
- optional `standards-crosswalk.md`

Application-layer model:

```text
application use case -> integration port -> adapter -> external resource -> policy -> mapping -> evidence
```

Counterexample:

A payment provider integration returns synchronously from `CreatePayment`, later sends webhook callbacks, uses a cache projection for local reads, may deliver duplicate webhooks, and can disagree with local state. A weak spec becomes OpenAPI-only, cache-only, or provider prose. It misses idempotency, stale read policy, event ordering, reconciliation, and domain ownership.

Zig-zag repair:

IntegrationSpec must not describe every API shape itself. It should govern the application-layer decision and evidence envelope around integrations, then delegate formal wire contracts to OpenAPI, AsyncAPI, CloudEvents, and domain semantics to DomainSpec.

## Residue

- Tier remains conditional.
- Taxonomy promotion is blocked until definitions-governance.
- If the final route selects a new package, it should go through `sigil-development` for a minimal public proof first.
