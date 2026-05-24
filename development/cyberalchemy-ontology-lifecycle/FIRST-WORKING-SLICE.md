---
title: CyberAlchemy Ontology Lifecycle First Working Slice
status: plan-ready
task: CAOL-008
route: implementation-layering-l0
createdAt: 2026-05-24
---

# First Working Slice

## Purpose

Prove the candidate ontology lifecycle with the smallest useful review-only artifact: one PromotionRecord fixture that turns one operational observation into one governed candidate decision without mutating canonical ontology or runtime files.

This slice is planning/execution handoff only. It does not create canonical ontology entries.

## Layer

Layer: L0 POC.

Decision question:

```text
After this layer, we know whether a PromotionRecord can represent one observed operational lesson with evidence, confidence, owner, bridge status, and route impact without false authority.
```

## Write Scope

Allowed:

```text
development/cyberalchemy-ontology-lifecycle/first-slice/
```

Recommended files:

```text
development/cyberalchemy-ontology-lifecycle/first-slice/promotion-record-fixture.md
development/cyberalchemy-ontology-lifecycle/first-slice/validation-result.md
```

Forbidden:

```text
../cyberAlchemy/ontology/
arcana/
spells/
framework/
runtime or observability ledgers
```

## Fixture Scenario

Use this scenario unless later evidence suggests a better one:

```text
An Arcanum invoke/task-session style run produces enough reviewed evidence to propose an operational lesson: future ontology lifecycle runs should require a context-builder handoff before synthesis.
```

This is intentionally modest: it exercises source/inventory evidence, ReviewableSignal-style operational evidence, branch targeting, confidence split, review owner, bridge validation, and route impact.

## PromotionRecord Fixture Requirements

The fixture must include:

| Field | Required Content |
| --- | --- |
| `id` | Stable fixture id, e.g. `CAOL-L0-PR-001`. |
| `claim` | One primary claim only. |
| `claimType` | `operational-lesson` or `policy-candidate`. |
| `sourceInputs` | At least two package-local source references, preferably `CONTEXT-HANDOFF.md`, `INTERROGATION-VERDICT.md`, `ONTOLOGY-ARCHITECTURE.md`, or `PROMOTION-LIFECYCLE.md`. |
| `provenance` | How the fixture was produced and which artifacts informed it. |
| `branchTarget` | `candidate Operational Ontology extension` or Bridge if the claim is about traceability. |
| `status` | `candidate`, `premise`, `defer`, or `reviewed`; not `promoted`. |
| `evidenceConfidence` | Separate rationale. |
| `commitmentConfidence` | Separate rationale. |
| `reviewOwner` | Owner class from Review Owner Matrix. |
| `gateResult` | `pass`, `flag`, `defer`, or `block` with rationale. |
| `useScope` | Narrow scope, such as future CAOL planning runs. |
| `contradictionPath` | How later evidence would challenge it. |
| `rollbackOrRetirement` | How to retire or narrow the lesson. |
| `routeImpact` | Affected Arcanum route(s), e.g. context-builder, invoke, task-session. |
| `bridgeValidation` | One of `aligned`, `partial`, `drift`, `insufficient`, `contradicted`. |
| `expiresWhen` | Condition that makes the record stale. |

## Validation Checklist

| Check | Pass Condition |
| --- | --- |
| One primary claim | Fixture does not bundle unrelated claims. |
| Candidate status visible | Fixture does not pretend to be canonical or promoted. |
| Source inputs are pointers | No raw source dumps or raw telemetry payloads. |
| Evidence confidence separate | Evidence rationale is distinct from commitment rationale. |
| Commitment confidence separate | Commitment is scoped and does not follow signal recurrence automatically. |
| Review owner present | Owner class is not `unknown`. |
| Bridge outcome present | Fixture uses one defined bridge-validation outcome. |
| Signal truth guard | Any signal input is reviewable evidence only. |
| Operational use gated | Use scope is narrow and bridge/status gated. |
| Canonical mutation absent | Only files under `first-slice/` are created or changed. |

## Execution Steps

1. Read [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md#promotionrecord-schema), [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md#transition-table), and [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md#caol-007-architecture-and-lifecycle-interrogation).
2. Create `first-slice/promotion-record-fixture.md`.
3. Fill every required field in the fixture table.
4. Create `first-slice/validation-result.md`.
5. Evaluate the fixture against the validation checklist.
6. Return `pass`, `flag`, or `block`.

## Exit Evidence

L0 passes only when:

- fixture exists;
- validation result exists;
- every required field is present or explicitly marked not applicable with rationale;
- no canonical ontology/runtime files were touched;
- validation result states whether the model is ready for L1 repeatability.

## Promotion Decision

Continue to L1 when:

- one fixture validates cleanly;
- PromotionRecord boundary feels sufficient;
- no missing required field blocks review.

Pivot when:

- fixture needs fields not covered by CAOL-006/007;
- owner/gate mapping is too vague for review.

Stop when:

- a useful fixture cannot be represented without mutating canonical ontology/runtime files;
- evidence confidence and commitment confidence cannot be kept separate.

## Handoff Prompt

```text
/goal Execute the CAOL-008 L0 first working slice.

Read development/cyberalchemy-ontology-lifecycle/FIRST-WORKING-SLICE.md first. Create only review-only artifacts under development/cyberalchemy-ontology-lifecycle/first-slice/. Produce one PromotionRecord fixture and validation result. Do not mutate canonical ontology, runtime, skill, sigil, spell, or observability files. Mark pass, flag, or block against the checklist.
```
