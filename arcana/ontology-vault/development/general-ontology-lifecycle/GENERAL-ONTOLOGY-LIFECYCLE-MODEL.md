# General Ontology Lifecycle Model

Status: exploratory, non-canonical
Date: 2026-05-27
Source: generalized from `development/cyberalchemy-ontology-lifecycle/`

## Purpose

Define the general, reusable ontology-governance model extracted from the CyberAlchemy Ontology Lifecycle package.

This model belongs in Ontology Vault development because it describes how evidence, signals, decisions, candidates, confidence, bridge validation, and promotion should be governed across systems. It does not carry DomainSpec/AEO-specific lifecycle mechanics.

## Core Model

```text
SourceSelector / InventoryEvidence / ReviewableSignal / LifecycleEvidenceEnvelope / UserDecision
  -> PromotionRecord
  -> Candidate / Premise / Reviewed / PromotedEntry / Policy / Constitution / Axiom / Contradiction / Retirement
```

## Layer Responsibilities

| Layer | General responsibility | Boundary |
| --- | --- | --- |
| SourceSelector | Points to source evidence with enough selector detail to inspect it. | Not ontology meaning by itself. |
| InventoryEvidence | Reusable source-backed evidence prepared for retrieval. | Inventory remains non-authority. |
| ReviewableSignal | Structured observation from execution, telemetry, validation, or reflection. | Review input only; never truth by itself. |
| LifecycleEvidenceEnvelope | Evidence envelope from a lifecycle system. | General concept only; DomainSpec/AEO-specific fields belong elsewhere. |
| UserDecision | Scoped human or governance decision. | Requires owner, scope, rationale, and rejected alternatives. |
| PromotionRecord | Bounded governance/change record for one claim or decision. | Does not replace ontology entries and does not contain raw dumps. |
| Ontology outcome | Candidate, premise, promoted entry, policy, constitution, axiom, contradiction, or retirement. | Promotion depends on evidence, commitment, owner, scope, bridge, and contradiction path. |

## PromotionRecord Boundary

A PromotionRecord may contain:

- one primary claim,
- source and evidence pointers,
- provenance,
- branch target,
- status,
- evidence confidence,
- commitment confidence,
- review owner,
- gate result,
- use scope,
- contradiction path,
- rollback or retirement path,
- route impact,
- bridge validation when needed.

A PromotionRecord must not contain:

- unrelated bundled claims,
- full source excerpts,
- raw telemetry payloads,
- full ontology entry bodies when a pointer is enough,
- implementation plans,
- canonical mutation instructions.

## Branch-Aware Mapping

| Concept | Candidate branch mapping |
| --- | --- |
| Meaning claim | `meaning`, with possible local alias such as `business`, `domain`, `intent`, or `proposition`. |
| System artifact or mechanism | `system`. |
| Situated use, route lesson, context solution, self-application | `operational`, with explicit operating context. |
| PromotionRecord, evidence relation, drift, validation, contradiction | usually `bridge` or companion governance record. |

## Lifecycle States

| State | Meaning | Can guide work? |
| --- | --- | --- |
| `raw` | Unreviewed observation, memory, run, source mention, or telemetry. | no |
| `catalogedEvidence` | Source or inventory evidence with selector and summary. | only as cited support |
| `reviewableSignal` | Structured observation with provenance and route/outcome fields. | only as review input |
| `promotionRecordDraft` | Proposed governed change record. | no, except for review |
| `candidate` | Draft ontology object with visible candidate status. | yes, with caveat and scope |
| `premise` | Falsifiable working bet. | yes, with uncertainty visible |
| `reviewed` | Evidence checked but not necessarily promoted. | yes, within review scope |
| `promoted` | Accepted for scoped reliance. | yes |
| `policy` | Scoped decision rule. | yes, within applicability |
| `constitution` | Enforceable governance for form, model, structure, transformation, or gates. | yes, when accepted |
| `axiom` | Load-bearing principle or invariant-bearing claim. | yes, when accepted |
| `contradicted` | Challenged by evidence. | no, except as warning/repair input |
| `retired` | No longer active. | no |
| `rejected` | Unsupported or out of scope. | no |
| `deferred` | Evidence, owner, or scope missing. | no |

## Confidence Rules

Every candidate, PromotionRecord, and promoted entry should separate:

| Field | Question |
| --- | --- |
| Evidence confidence | How strongly does the selected evidence support or challenge the claim? |
| Commitment confidence | How strongly should the system rely on this claim now? |
| Bridge alignment confidence | How well does the relation across branches hold? |
| Scope confidence | How clearly is the claim bounded? |

Rules:

- Recurrence and severity can raise evidence confidence.
- Commitment confidence requires owner, use scope, rollback/retirement, and contradiction path.
- Low evidence plus high commitment is a risk state, not promotion.
- High evidence plus low commitment can remain reviewed or candidate.

## Bridge Validation Outcomes

| Outcome | Meaning |
| --- | --- |
| `aligned` | Evidence supports the relation across branches. |
| `partial` | Evidence supports a narrower claim or smaller scope. |
| `drift` | Observed behavior diverges from expected meaning, system contract, or operational behavior. |
| `insufficient` | Evidence does not yet prove alignment. |
| `contradicted` | Evidence actively challenges the claim. |

Bridge validation is required when a promoted claim asserts alignment between meaning, system realization, and operational use.

## Operational Use Rules

Operational use is allowed only when:

1. candidate or promoted status is visible,
2. use scope is explicit,
3. evidence confidence and commitment confidence are present,
4. bridge validation is complete where cross-branch alignment matters,
5. rollback, retirement, or contradiction path is known.

Operational use cannot:

- mutate canonical runtime or ontology files by itself,
- treat observability as truth,
- hide candidate status,
- skip owner review for behavior-changing guidance.

## Review Owner Rules

General owner classes:

| Claim type | Default owner class |
| --- | --- |
| Meaning concept or premise | meaning ontology reviewer or domain owner |
| System concept or implementation fact | system ontology reviewer or repository maintainer |
| Bridge validation or drift | bridge ontology reviewer |
| Operational lesson or route policy | operational lifecycle reviewer |
| Capability contract | owning skill, sigil, spell, or route lifecycle |
| Constitution | governance owner for affected artifact or model |
| Axiom | ontology governance owner plus user or decision-gate review |

No record should reach promoted, policy, constitution, or axiom state with unknown owner.

## Candidate Role Semantics

These semantics are useful but not canonical:

```text
axiom = behavior invariant or load-bearing principle that downstream governance depends on
constitution = enforceable form/model/structure/transformation/gate governance that preserves invariants
policy = scoped decision rule with owner and applicability
premise = falsifiable working bet
```

Route canonical definition changes through Definitions Governance or decision gate.

## Validation Fixture Shape

A minimal review-only fixture should prove:

- one primary claim,
- candidate status visible,
- source inputs are pointers,
- evidence confidence separate,
- commitment confidence separate,
- review owner present,
- bridge outcome present,
- signal truth guard explicit,
- operational use gated,
- no canonical mutation.

## Deferred Particulars

These are intentionally not copied into the general model:

- DomainSpec route/stage execution semantics,
- AEO telemetry envelope implementation details,
- DomainSpec-specific constitution and authority map,
- CyberAlchemy package-specific scenario names,
- native `/goal` prompts,
- article/presentation prose.
