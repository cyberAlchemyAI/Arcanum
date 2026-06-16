# Interrogation: Refine Review

Status: pass
Mode: refine-review
Capability: `interrogation`

## Highest-Discrimination Question

Does the problem require a new autonomous arcana package, or only a governed integration-boundary discipline that routes into existing template, formula, and task-session owners?

## Evidence

- DomainSpec already has connective concepts: `Interface`, `Event`, `Mapping`, plus `Policy`, `Workflow`, `Saga`, `Operation`, and `Query`.
- DomainSpec definitions explicitly block unapproved larger vocabulary extensions.
- Existing templates include interfaces and mappings, but not a complete selection/evidence envelope for databases, caches, providers, and integration policies.
- Lane Z found a real counterexample that exceeds simple API shape documentation.
- Lane A found a smaller route that may answer the same underlying problem with less lifecycle weight.

## Review Verdict

The new IntegrationSpec idea is meaningful, but immediate package creation is not yet proven as the smallest responsible unit.

Proceed through bounded research and distill. Require final synthesis to choose between:

1. new arcana package;
2. discipline-first hardening;
3. DomainSpec template extension;
4. formula validator;
5. standards crosswalk only.

## Risks

- Duplicating OpenAPI, AsyncAPI, CloudEvents, or vendor guidance.
- Mutating DomainSpec vocabulary without definitions-governance.
- Treating runtime evidence as canonical spec truth.
- Creating an arcana package when a discipline plus templates would do.
