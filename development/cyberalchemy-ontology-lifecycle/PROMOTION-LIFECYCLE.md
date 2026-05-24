---
title: CyberAlchemy Ontology Promotion Lifecycle
status: candidate-design
task: CAOL-006
route: invoke-design
createdAt: 2026-05-23
updatedAt: 2026-05-24
---

# Promotion Lifecycle

## Status

This lifecycle is a candidate design companion to [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md). It uses [CONCEPT-TOURNAMENT.md](CONCEPT-TOURNAMENT.md)'s selected model: `PromotionRecord` as the governing change object.

Promotion is not a passive state flip. Promotion is a reviewable, attributable, confidence-bearing decision recorded in a PromotionRecord.

## Lifecycle Diagram

```text
[Discovery]
     |
     v
[InventoryEvidence / SourceSelector]
     |
     +--> [ReviewableSignal]
     |
     +--> [LifecycleEvidenceEnvelope]
     |
     +--> [UserDecision]
     |
     v
[PromotionRecord Draft]
     |
     v
[Evidence + Confidence Review]
     |
     +--> [Reject]
     +--> [Defer]
     +--> [OntologyCandidate]
     +--> [Premise]
     +--> [PromotedEntry]
     +--> [Policy]
     +--> [Constitution]
     +--> [Axiom]
     +--> [Contradiction]
     +--> [Retirement]
     |
     v
[Bridge Validation]
     |
     v
[Operational Use]
     |
     v
[Observability Feedback]
     |
     +--> [New PromotionRecord]
     +--> [Maintenance Route]
     +--> [Contradiction Review]
```

## Lifecycle States

| State | Meaning | Can Guide Agents? | Required Gate |
| --- | --- | --- | --- |
| `raw` | Unreviewed source, run, note, memory, telemetry, or user comment. | No. | None. |
| `catalogedEvidence` | Source/inventory evidence with selectors, metadata, and contradiction notes. | Only as cited support. | Source relevance and catalog quality. |
| `reviewableSignal` | Structured observation with provenance/envelope/route validity. | Only as review input. | Signal validity check. |
| `lifecycleEvidenceEnvelope` | DomainSpec/AEO lifecycle evidence preserving intent, route, stage, outcome, and telemetry. | Only as review input. | Lifecycle envelope check. |
| `promotionRecordDraft` | Proposed governed knowledge-change record. | No, except for review. | Required fields present. |
| `candidate` | Draft ontology meaning object with visible candidate status. | Yes, with visible candidate status and limited scope. | Candidate gate. |
| `premise` | Falsifiable working bet. | Yes, within explicit uncertainty. | Premise gate. |
| `reviewed` | Claim has passed review but is not hardened further. | Yes, within review scope. | Evidence/confidence gate. |
| `promoted` | Claim can guide agents within defined use scope. | Yes. | Promotion gate and bridge validation where needed. |
| `policy` | Scoped decision rule. | Yes, as scoped rule. | Owner and applicability gate. |
| `constitution` | Enforceable form/model/structure/transformation/invariant governance. | Yes, as governance. | Constitution gate. |
| `axiom` | Behavior invariant or load-bearing principle. | Yes, as invariant-bearing governance. | Axiom gate. |
| `contradicted` | Later evidence challenges the claim. | No, except as warning/repair input. | Contradiction gate. |
| `retired` | Claim no longer applies. | No. | Retirement gate. |
| `rejected` | Evidence does not support the claim or it is out of scope. | No. | Rejection reason. |
| `deferred` | Claim may matter but evidence, owner, or scope is missing. | No, except as backlog. | Deferral reason. |

## Transition Table

| From | To | Gate | Required Evidence / Fields | Forbidden Shortcut |
| --- | --- | --- | --- | --- |
| Discovery | InventoryEvidence / SourceSelector | Source relevance gate | source path, selector, summary, tags, contradiction notes. | Treating source mention as ontology entry. |
| Runtime / telemetry | ReviewableSignal | Signal validity gate | envelope/artifact reference, route identity, observed/expected outcome, terminal/validation state, dedupe/severity, owner route. | Treating telemetry as truth. |
| DomainSpec/AEO run | LifecycleEvidenceEnvelope | Lifecycle envelope gate | intent, route, stage, terminal outcome, telemetry pair, evidence envelope, drift/convergence context. | Collapsing execution result into business authority. |
| User review | UserDecision | Decision evidence gate | owner, scope, rationale, rejected alternatives, review/expiry date. | Treating unscoped preference as policy. |
| Any adapter input | PromotionRecord Draft | Record completeness gate | id, claim, claimType, sourceInputs, provenance, branchTarget, status, confidence fields, reviewOwner, contradictionPath. | Invisible state change. |
| PromotionRecord Draft | Candidate | Candidate gate | branch, scope, evidence, confidence split, owner, candidate visibility. | Candidate used as promoted knowledge. |
| Candidate | Premise | Premise gate | falsifiable claim, uncertainty, contradiction path, owner. | Premise treated as fact. |
| Candidate/Premise | Reviewed | Evidence/confidence gate | evidenceConfidence, commitmentConfidence, support/challenge summary, review owner. | Collapsing evidence and commitment confidence. |
| Reviewed | PromotedEntry | Promotion gate | owner approval, useScope, bridge validation if cross-branch, rollback/retirement path. | Promotion without use scope. |
| Reviewed | Policy | Policy gate | scoped rule, applicability, owner, route impact. | Treating policy as constitution. |
| Reviewed | Constitution | Constitution gate | governed artifact/form/model/structure/transformation, preserved invariant/gate, owner, rollback. | Constitution for ordinary process preference. |
| Reviewed | Axiom | Axiom gate | invariant-bearing test, dependency review, strong evidence, contradiction review, explicit commitment. | Axiom from repeated observation alone. |
| Any active state | Contradicted | Contradiction gate | challenge evidence, affected claims, severity, owner route. | Silent overwrite. |
| Any active state | Retired | Retirement gate | expiry/invalidating condition, replacement or rollback, owner. | Deleting history. |

## PromotionRecord Lifecycle

```text
draft
  -> candidate-record
  -> reviewed-record
  -> decisioned-record
  -> applied-as-scope-limited-guidance
  -> monitored
  -> reaffirmed / contradicted / retired
```

PromotionRecord outcomes:

| Outcome | Meaning | Next Route |
| --- | --- | --- |
| `reject` | Claim unsupported or out of scope. | Archive with reason. |
| `defer` | Evidence, owner, or scope missing. | Research, context-builder, or user decision. |
| `candidate` | Worth drafting as ontology but unpromoted. | CAOL design or ontology-vault candidate route. |
| `premise` | Falsifiable working bet. | Premise review and observation. |
| `reviewed` | Evidence checked, not hardened. | Promotion or monitoring decision. |
| `promoted` | Can guide agents in defined use scope. | Bridge validation and retrieval proof. |
| `policy` | Scoped decision rule. | Policy owner / route impact review. |
| `constitution` | Form/model/structure/transformation/invariant governance. | Governance owner and rollback path. |
| `axiom` | Behavior invariant / load-bearing principle. | Strong contradiction monitoring. |
| `contradicted` | Later evidence challenges claim. | Repair, retire, or reopen. |
| `retired` | No longer applies. | Preserve history; remove from active use. |

## Confidence And Commitment Gates

| Gate | Evidence Confidence Question | Commitment Confidence Question |
| --- | --- | --- |
| Candidate gate | Is there enough evidence to draft the claim? | Can it guide work only as candidate? |
| Premise gate | Is the claim plausible and falsifiable? | Can work proceed while uncertainty is explicit? |
| Promotion gate | Is the claim supported across required sources or review? | Should agents rely on it now, in this scope? |
| Policy gate | Does evidence justify the rule? | Should this rule govern behavior or routing? |
| Constitution gate | Does evidence justify structural governance? | Should this constrain artifact shape, model rules, transformations, or gates? |
| Axiom gate | Is the claim strongly evidenced and invariant-bearing? | Should downstream governance depend on it? |
| Contradiction gate | Does new evidence challenge the claim? | Should reliance stop, narrow, or continue with warning? |

Rules:

- Evidence confidence and commitment confidence are separate fields.
- Low evidence plus high commitment is a risk state, not a promotion.
- High evidence plus low commitment can remain cataloged, reviewed, or candidate.
- Commitment must name use scope, owner, rollback/retirement path, and contradiction path.

## Evidence Requirements

| Evidence Type | Can Start Record? | Can Promote Alone? | Notes |
| --- | --- | --- | --- |
| SourceSelector | yes | no | Anchors a claim to a source. |
| InventoryEvidence | yes | no | Catalog evidence; not governed meaning. |
| ReviewableSignal | yes | no | Review input only; not truth. |
| LifecycleEvidenceEnvelope | yes | no | Strong software lifecycle evidence, still requires review. |
| UserDecision | yes | sometimes | Can decide scope/commitment, but should cite rationale and affected model. |
| BridgeValidation | no | required for operational use | Proves alignment across branches. |
| ExternalResearchInfluence | yes, as design pressure | no | Vocabulary/analogy/evidence pressure only. |

## Signal Recurrence And Severity

CAOL-007 repair: a ReviewableSignal can start a PromotionRecord only when recurrence or severity justifies review.

| Signal Pattern | Minimum Threshold | Allowed Outcome |
| --- | --- | --- |
| Single successful run | Provenance/envelope valid and tied to an existing claim. | Evidence support only; no promotion by itself. |
| Repeated success | Same route/capability succeeds in at least two comparable runs, or one run plus independent validation evidence. | Candidate or reviewed support if scope remains narrow. |
| Repeated failure | Same failure mode appears in at least two comparable runs, or one severe failure has clear route impact. | DriftFinding, contradiction, or maintenance PromotionRecord. |
| Severe one-off failure | Safety, data loss, policy violation, canonical mutation risk, privacy risk, or blocked lifecycle closeout. | Immediate flag/block PromotionRecord and owner escalation. |
| Cross-repository pattern | Same signal pattern appears across more than one repository or context. | Stronger operational candidate, still requiring owner review. |
| Ambiguous signal | Missing provenance, route identity, expected outcome, terminal state, or dedupe. | Defer; cannot promote or contradict. |

A signal's recurrence/severity changes evidence confidence only. Commitment confidence still requires review owner, use scope, rollback/retirement path, and contradiction path.

## Adapter Outputs

| Adapter | Produces | PromotionRecord Claim Examples |
| --- | --- | --- |
| Source-to-inventory | InventoryEvidence, SourceSelector | "This source defines Business Ontology as intent branch." |
| Signal-to-record | ReviewableSignal, PromotionRecord draft | "Observed invoke runs repeatedly lack complete handoff evidence." |
| Lifecycle-envelope | LifecycleEvidenceEnvelope, PromotionRecord draft | "AEO terminal outcomes should feed bridge validation." |
| Capability-contract | PromotionRecord draft with routeImpact | "This sigil should require context-builder before execution." |
| Decision adapter | UserDecision, PromotionRecord decision | "Operational Ontology remains candidate until ontology-harness review." |

## Bridge Validation

Bridge validation is required before promoted knowledge guides operational use when the claim crosses intent, implementation, and runtime behavior.

Minimum bridge proof:

- business or operational intent;
- system realization or runtime evidence;
- evidence links on both sides;
- contradiction path;
- confidence split;
- retrieval proof for future agents when operational use is expected.

Bridge validation outcomes:

| Outcome | Meaning | Operational Effect |
| --- | --- | --- |
| `aligned` | Intent and system/operational evidence support the same claim. | May proceed to scoped operational use if PromotionRecord status permits. |
| `partial` | Evidence supports a narrower claim or smaller scope. | Narrow useScope or keep candidate/premise status. |
| `drift` | System/operational behavior diverges from intent. | Create or update DriftFinding and contradiction path. |
| `insufficient` | Evidence does not yet prove alignment. | Defer promotion or require more evidence. |
| `contradicted` | Evidence actively challenges the claim. | Block promotion and route to contradiction review. |

## Operational Use

Operational use is allowed only when:

1. PromotionRecord status permits use.
2. Candidate/promoted status is visible to the agent.
3. Use scope is explicit.
4. Evidence confidence and commitment confidence are present.
5. Bridge validation is complete when cross-branch alignment is required.
6. Rollback, retirement, or contradiction path is known.

Operational use can guide:

- context-builder retrieval;
- task-session handoff checks;
- invoke define/design/plan routing;
- skill/sigil/spell maintenance proposals;
- DomainSpec/AEO route tuning;
- ontology-vault candidate creation.

Operational use cannot:

- mutate canonical runtime or ontology files without lifecycle authority;
- treat observability as truth;
- hide candidate status;
- skip owner review for behavior-changing guidance.

## Use Case Flows

### Arcanum Repository Agentic Operation

```text
invoke/task-session/sigil run
  -> OIL envelope
  -> ReviewableSignal
  -> PromotionRecord draft
  -> operational candidate or route policy
  -> review owner
  -> bridge validation
  -> scoped future guidance
```

### Software Development Agent Lifecycle

```text
DomainSpec intent
  -> AEO route/stage execution
  -> LifecycleEvidenceEnvelope
  -> PromotionRecord
  -> System/Bridge candidate
  -> promoted validation obligation or drift finding
  -> route tuning / ontology candidate / contradiction
```

### Business Software Knowledge Discovery

```text
business evidence
  -> InventoryEvidence / SourceSelector
  -> PromotionRecord
  -> Business candidate or premise
  -> system realization mapping
  -> bridge validation
  -> policy / constitution / axiom / promoted entry
```

## Lifecycle Interrogation And Repair

Findings:

1. Old lifecycle implied `inventory -> ontology candidate` directly.
   - Repair: insert adapter-normalized inputs and PromotionRecord draft.

2. Old lifecycle used `Verified Signal`.
   - Repair: use `ReviewableSignal`; verification means provenance/envelope validity only.

3. Promotion states were listed but not governed by a change object.
   - Repair: every transition to candidate, premise, promoted, policy, constitution, axiom, contradiction, or retirement is a PromotionRecord outcome.

4. Operational use could happen too early.
   - Repair: require status, use scope, confidence split, bridge validation where needed, and rollback/contradiction path.

## CAOL-007 Compact Repair Addendum

Second interrogation repair:

| Flag | Repair |
| --- | --- |
| PromotionRecord could absorb too much | PromotionRecord Boundary added to architecture; lifecycle keeps record outcomes and evidence inputs separate. |
| Owner gates too vague | Review Owner Matrix added to architecture; lifecycle still requires owner on PromotionRecord and transition gates. |
| Signal recurrence/severity underspecified | Signal Recurrence And Severity table added above. |
| Bridge validation too binary | Bridge validation outcomes added: aligned, partial, drift, insufficient, contradicted. |
| Commitment confidence could follow signal strength accidentally | Signal threshold section states recurrence/severity affects evidence confidence only; commitment still requires owner, scope, rollback, and contradiction path. |

Re-interrogation verdict: `pass-with-explicit-review-items`. The repaired lifecycle blocks direct signal-to-truth promotion and keeps operational use behind status, use scope, confidence split, bridge validation, and contradiction/retirement paths.

## CAOL-006 Lifecycle Gate

| Gate | Result | Evidence |
| --- | --- | --- |
| Lifecycle flow included | pass | Diagram and transition table. |
| Promotion mechanisms included | pass | PromotionRecord lifecycle, outcomes, transition gates. |
| Confidence included | pass | Confidence and commitment gates. |
| Evidence requirements included | pass | Evidence requirements table and bridge validation. |
| Adapter/interface discussion included | pass | Adapter outputs table. |
| Observability-backed validation included | pass | ReviewableSignal and operational use constraints. |
| Use cases included | pass | Arcanum, software lifecycle, business knowledge discovery. |
| Stop condition avoided | pass | No canonical mutation required. |

## Next Route

CAOL-008 should plan implementation around:

- PromotionRecord schema normalization;
- review-owner assignments;
- signal threshold defaults;
- bridge-validation evidence templates;
- user decision path for Operational Ontology acceptance.
