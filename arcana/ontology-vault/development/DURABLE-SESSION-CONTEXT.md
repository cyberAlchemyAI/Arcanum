# Ontology Vault Development Durable Session Context

## Purpose

This session is dedicated to developing the `ontology-vault` sigil, with the current focus on a general branch-aware ontology model.

Use this file as the durable session baseline for future work in this thread or for new handoff threads that continue ontology development. The session should stay scoped to ontology branch models, ontology role governance, confidence and promotion rules, bridge rules, branch-aware validation, and ontology handoff boundaries.

## Scope Boundary

In scope:

- `arcana/ontology-vault/README.md`
- `arcana/ontology-vault/SKILL.md`
- `arcana/ontology-vault/templates/`
- `arcana/ontology-vault/development/`
- source handoffs that explicitly target ontology development
- Inventory artifacts only as source evidence or handoff inputs
- CyberAlchemy, DomainSpec, or future-system sources only as examples and pressure tests for the general model

Out of scope unless explicitly routed back through a separate handoff:

- Inventory implementation, indexes, selectors, or evidence-card design
- structured-action-schema mutation
- runtime command implementation
- unrelated sigil or spell development
- CyberAlchemy-specific ontology promotion
- DomainSpec-specific ontology promotion
- observability hook churn not directly relevant to ontology governance

## Current Session Decision

This chat should contain only ontology development work.

If a related but separate idea appears, create a new handoff artifact instead of expanding this session. The handoff should include:

- the user's new-session prompt,
- the source session reference,
- the target lifecycle owner,
- selected source context,
- excluded context,
- target boundary,
- next route.

## Active Development Focus

Current focus:

- draft an exploratory, non-canonical general branch-aware ontology model,
- preserve the branch-context discriminator from the Inventory handoff,
- support systems such as Arcanum, CyberAlchemy, DomainSpec, and future systems,
- define candidate branch semantics without promoting them to governed ontology truth,
- clarify role-catalog governance, context rules, self-application handling, bridge rules, confidence boundaries, Inventory handoff boundaries, and unresolved decisions.

## Relevant Context Pack

Primary source handoff:

- [../../inventory/development/ONTOLOGY-BRANCH-MODEL-HANDOFF.md](../../inventory/development/ONTOLOGY-BRANCH-MODEL-HANDOFF.md)

Primary local ontology contracts:

- [../README.md](../README.md)
- [../SKILL.md](../SKILL.md)

Supporting source context:

- [../../inventory/development/BRANCH-ROLE-EXPANSION-DISTILL.md](../../inventory/development/BRANCH-ROLE-EXPANSION-DISTILL.md)
- [../../inventory/development/BRANCH-ROLE-EXPANSION-NOTE.md](../../inventory/development/BRANCH-ROLE-EXPANSION-NOTE.md)
- [../../../../cyberAlchemy/agentic-system-architecture.md](../../../../cyberAlchemy/agentic-system-architecture.md)
- [../../../../cyberAlchemy/agentic-system-ontology-entry-model.md](../../../../cyberAlchemy/agentic-system-ontology-entry-model.md)

Current output:

- [BRANCH-AWARE-ONTOLOGY-CANDIDATE.md](BRANCH-AWARE-ONTOLOGY-CANDIDATE.md)
- [BRANCH-NAMING-DISTILL.md](BRANCH-NAMING-DISTILL.md)
- [BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md](BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md)
- [cyberalchemy-ontology-lifecycle/](cyberalchemy-ontology-lifecycle/)
- [general-ontology-lifecycle/](general-ontology-lifecycle/)
- [handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md](handoffs/DOMAIN-SPEC-ONTOLOGY-LIFECYCLE-HANDOFF.md)

## Operating Rules

1. Treat this branch-aware ontology work as exploratory until explicitly promoted.
2. Do not mutate Inventory or structured-action-schema from this session.
3. Use Inventory only as evidence capture and handoff source, not ontology authority.
4. Preserve local truth: each system may have its own branch role catalogs and context overlays.
5. Keep global ontology language small enough for cross-system comparison.
6. Distinguish evidence confidence, commitment confidence, and bridge alignment confidence.
7. Represent self-application as an operational context over a system, not as circular authority.
8. When a decision would govern future ontology behavior, route it through a decision gate or explicit ontology convention update.

## Latest Verification

Review performed:

- read the handoff and source distillation files,
- read the Ontology Vault contracts,
- read CyberAlchemy's candidate architecture and ontology entry model,
- confirmed the output is under `arcana/ontology-vault/development/`,
- avoided changes to Inventory and structured-action-schema.

## Durable Handoff Note

When resuming this session, start from this file, then inspect the current git diff for ontology-vault-scoped files only.

Suggested resume prompt:

```text
Continue the durable ontology-vault development session. Use arcana/ontology-vault/development/DURABLE-SESSION-CONTEXT.md as the scope boundary. Focus only on ontology development unless a separate idea is explicitly routed through a handoff.
```
