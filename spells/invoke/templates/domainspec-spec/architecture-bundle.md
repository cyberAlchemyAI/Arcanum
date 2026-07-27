---
module: {module-name}
version: current
status: draft
updatedAt: {date}
docType: architecture-bundle
---

# Architecture Bundle: {Module Name}

Translate an approved DomainSpec `SPEC.md` into structural and process design views. This is the design-stage companion to the DomainSpec template family.

## Design Intent
Summarize architecture goals and constraints in two to three sentences.

## Inputs
- [SPEC.md](SPEC.md) — capabilities + Concept Registry (typed against DS-D1)
- aspect docs: [operations.md](operations.md), [queries.md](queries.md), [interfaces.md](interfaces.md), [states.md](states.md), [events.md](events.md), [mappings.md](mappings.md)
- canonical vocabulary: `arcanum/definitions/DEFINITIONS.md` (DS-D1 meta-types, DS-D2 edges)
- system of interest: `{target_id}`
- closed Design scope: `{DesignScopeManifest path and input_digest}`
- Design selection: `{DesignSelectionResult path and result_digest}`

## Required View Set

### 1. Context View
```mermaid
graph TD
    Actor --> Module[{Module}]
    Module --> External[External Dependency]
```

### 2. Capability View
One node per SPEC capability; edges are DS-D2 relationship verbs between the Concept Registry entries they touch.

### 3. Concept/Type View
The Concept Registry as a typed graph: nodes carry their DS-D1 meta-type; edges carry DS-D2 verbs and must satisfy the DS-D8 edge signature.

### 4. Operation/Flow View
For each Operation (from `operations.md`): inputs → rules → calculations → state transition → postconditions → events. Maps the write-side flow.

### 5. State View
The State Machine(s) from `states.md`: states + transition table; one transition row = one behavioral obligation downstream (test-derivation / obs-derivation).

### 6. Dependency/Interface View
Interfaces (`interfaces.md`) and mappings (`mappings.md`): exposure boundaries, contracts, and cross-shape transformations.

## Significant Behavior Scenario

Choose the smallest scenario that can falsify the selected architecture:

- use a runtime scenario when external effects, durable state, operational
  claims, or human recovery are present;
- otherwise use a deterministic artifact/evidence scenario.

Record stimulus, preconditions, ordered response, failure/recovery behavior,
observable evidence, and acceptance owner.

## Concern-to-view trace

| Concern ID | Primary class | Source signal IDs | Disposition | Accountable owner | Contributing owners | Artifact owner | Validator owner | View or extension | Evidence selectors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `{concern_id}` | `{class}` | `{signal_ids}` | required, recommended, not-applicable-with-rationale, or block | `{owner}` | `{owners}` | `{owner}` | `invoke-design-selection-validator` | `{view/extension}` | `{selectors}` |

Only `required` rows select an extension. Recommended and N/A rows remain
visible with rationale and revisit conditions; blocked rows prevent normal Plan
handoff.

## Planned Witness Contracts

### Fixture spec

| Fixture ID | Claim ID | Polarity | Target | Input or violation | Expected result | Execution owner | Execution phase |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `{fixture_id}` | `{claim_id}` | positive or negative | `{target}` | `{input}` | `{result}` | `{owner}` | plan, implementation, or validation |

### Validator contract

| Contract ID | Claim ID | Target contract | Accepted digest/binding | Verdicts | Stale rule | Self-issue rule | Validator owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `{validator_contract_id}` | `{claim_id}` | `{contract}` | `{digest or rule}` | pass and fail | reject | reject | `{owner}` |

These rows are planned contracts, not executed Plan evidence.

## Triggered architecture extensions

Author only extensions selected as `required` by the Design selection receipt.

| Output ID | Trigger boundary | Required depth |
| --- | --- | --- |
| `architecture:authority-trust` | admission, privileged effect, or trust boundary | authority decisions, enforcement placement, bypass/forgery controls |
| `architecture:state-event` | legal state/event lifecycle | transitions, forbidden edges, replay, terminality, supersession |
| `architecture:persistence-concurrency` | store, queue, or writer signal | write authority, ordering, idempotency, concurrency |
| `architecture:failure-compensation` | external/irreversible effect or recovery obligation | timeout, retry, partial effect, compensation, rollback |
| `architecture:integration-versioning` | independently evolving interface or protocol | compatibility rules, negotiation, recovery |
| `architecture:migration-rollout` | persisted representation or deployment transition | old/new conversion, staging, rollback |
| `architecture:data-lifecycle` | data/log sink | purpose, access, retention, disclosure, deletion |
| `architecture:security-abuse` | adversarial trust/resource boundary | abuse cases, controls, residual risk owner |
| `architecture:quality` | measurable reliability/performance claim | quality scenario, threshold, measurement owner |

## Design Rules
- Every view references Concept Registry IDs; do not introduce concepts absent from `SPEC.md`.
- Forbidden edges are those whose endpoint meta-types violate the DS-D8 signature — flag, do not draw.
- Keep the aspect-doc contract (M2-CONTRACT) stable; design adds views, it does not redefine the spec interface.
- Preserve all six baseline views even when no triggered extension is selected.
- Do not describe planned fixtures or validator contracts as executed evidence.

## Output
A six-view design that downstream `plan` (execution-pack) and the M2 derivation capabilities can consume without reopening discovery.
