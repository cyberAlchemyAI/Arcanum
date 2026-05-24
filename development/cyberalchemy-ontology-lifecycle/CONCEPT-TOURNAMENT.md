---
title: CyberAlchemy Ontology Lifecycle Concept Tournament
status: complete
task: CAOL-005
route: distill-tournament
createdAt: 2026-05-24
mode: tournament
roleExecution: role-simulated
refinementCycle: lane draft -> lane interrogation -> tournament selection -> recomposition repair -> final model note
---

# Concept Tournament

## Intent And Budget

Design intent: converge the CyberAlchemy ontology lifecycle model into the smallest coherent concept layer that can drive CAOL-006 architecture work.

Target context: a planning architecture package, not canonical ontology mutation.

Expected output artifact: a tournament result with four independent lanes, Proposer/Balancer trace, selected model, recomposition proof, and next-route guidance.

Optimization goal: select the smallest model that preserves ontology branches, promotion lifecycle, signal governance, DomainSpec/software lifecycle evidence, and the axiom/constitution distinction.

Budget: Tournament mode, four lanes, one draft/interrogation/repair cycle, one selection.

Subagent note: the runtime exposes subagent tooling, but the active objective allowed "run or simulate" and did not explicitly request delegation. This execution uses the distill role-simulated path and preserves the same Proposer/Balancer trace.

## Discovery Baseline

| Input | Role In Tournament |
| --- | --- |
| [CONTEXT-HANDOFF.md](CONTEXT-HANDOFF.md) | Local evidence baseline and contradiction ledger. |
| [DEFINITIONS-GLOSSARY.md](DEFINITIONS-GLOSSARY.md) | Candidate vocabulary, lifecycle spine, confidence split, axiom/constitution definitions. |
| [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md) | CAOL-003 flags: Operational Ontology authority, Verified Signal wording, promotion-gate fields, axiom/constitution semantics. |
| [external-research-appendix.md](external-research-appendix.md) | External pressure: provenance, catalog metadata, explicit change records, telemetry semantics, memory tiering, software ontology layering. |
| [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md) | Current candidate branch/node/edge model. |
| [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md) | Current candidate lifecycle and promotion outcomes. |

## Broad concept layer

Broad layer: CyberAlchemy agentic development ontology.

Abstraction level: governance architecture. It sits above raw telemetry, memory, inventory, and implementation details, and below canonical ontology promotion.

Candidate smallest coherent unit selected for testing:

```text
Promotion Record
```

Why this is the right candidate unit: every lane needs a common object that can carry claim, evidence, provenance, confidence, branch placement, promotion state, review owner, contradiction path, and route impact. Smaller units such as `Signal`, `Premise`, or `Evidence` lose governance closure. Larger units such as `Operational Ontology` or `Full Lifecycle` reopen unresolved branch-shape disputes.

## Tournament Lanes

### Lane 1: Ontology Model

Proposer claim: Use Business/System/Bridge as stable branches and treat Operational Ontology as a candidate extension until accepted.

Smallest coherent unit: `PromotionRecord` as a branch-neutral governed change object.

Invariant: branch authority must remain visible; candidate branch material cannot look canonical by layout.

Gate: every ontology candidate must name branch, scope, evidence, confidence, owner, and promotion state.

Risk: presenting Operational Ontology beside stable branches makes it look promoted.

Balancer objection:

| Category | Objection | Reconciliation |
| --- | --- | --- |
| False authority | Operational Ontology has useful evidence but not enough authority to be permanent peer branch. | Accept. CAOL-006 should model it as `candidate fourth branch` or `operational extension across System/Bridge` until user/ontology-harness acceptance. |
| Boundary object | A branch alone does not solve promotion or signal flow. | Accept. PromotionRecord becomes the cross-branch object rather than making Operational Ontology the center. |

Lane result: `pass-with-flag`. Use branch labels, but do not select branch shape yet.

### Lane 2: Promotion Lifecycle

Proposer claim: The promotion lifecycle should be driven by explicit Promotion Records, not informal state changes.

Smallest coherent unit: `PromotionRecord`.

Invariant: candidate knowledge and promoted knowledge must remain separate.

Gate: promotion requires evidence confidence, commitment confidence, provenance, decision owner, use scope, contradiction path, and rollback/retirement path.

Risk: lifecycle diagrams can imply automatic promotion from evidence or signal.

Balancer objection:

| Category | Objection | Reconciliation |
| --- | --- | --- |
| Hidden glue | A PromotionRecord must transform source evidence, observability, inventory, and DomainSpec output into the same review surface. | Revise. CAOL-006 should define PromotionRecord as adapter output for candidate, promotion, contradiction, and retirement. |
| Overfit | KGCL/PROV-O should not replace CyberAlchemy authority rules. | Accept. Use external sources for provenance/change vocabulary, not authority semantics. |

Lane result: `pass`. PromotionRecord is the strongest candidate for the tournament winner.

### Lane 3: Observability And Signal

Proposer claim: Observability should feed ontology through reviewable signals, not truth claims.

Smallest coherent unit: `ReviewableSignal` feeding `PromotionRecord`.

Invariant: telemetry can verify envelope/provenance/route integrity, not semantic truth.

Gate: signal must have provenance, route/capability identity, observed/expected outcome, terminal status or validation state, dedupe/recurrence/severity assessment, owner route, and review status.

Risk: `Verified Signal` sounds like verified truth.

Balancer objection:

| Category | Objection | Reconciliation |
| --- | --- | --- |
| Naming risk | The word "verified" can overclaim authority. | Accept. CAOL-006 should prefer `ReviewableSignal`; if `VerifiedSignal` remains, it must mean verified transport/provenance only. |
| Meaning loss | Signal alone cannot hold evidence confidence, commitment confidence, or promotion outcome. | Accept. Signals feed PromotionRecords; they are not the selected tournament unit. |

Lane result: `pass-with-repair`. Rename or constrain signal semantics.

### Lane 4: DomainSpec / Software Lifecycle

Proposer claim: DomainSpec/AEO evidence should become operational ontology candidates through route/evidence envelopes and bridge validation.

Smallest coherent unit: `LifecycleEvidenceEnvelope` feeding `PromotionRecord`.

Invariant: software lifecycle evidence must preserve intent, route, stage, terminal outcome, telemetry, validation evidence, and drift/convergence context.

Gate: DomainSpec-derived candidates require traceability from business intent through system realization and bridge validation.

Risk: software lifecycle ontology can pull CAOL toward implementation detail and away from governance.

Balancer objection:

| Category | Objection | Reconciliation |
| --- | --- | --- |
| Abstraction drift | AEO route/stage details are too low-level to become the core ontology unit. | Accept. Treat AEO outputs as evidence envelopes feeding PromotionRecord. |
| Requisite variety | DomainSpec needs enough fields to preserve lifecycle context. | Revise. PromotionRecord must include route/stage/outcome/evidence pointers when sourced from DomainSpec/AEO. |

Lane result: `pass`. DomainSpec evidence recomposes through PromotionRecord, not as a separate governing model.

## Pitch-Off

| Candidate Unit | Fit | Option Value | Risk | Cost | Decision |
| --- | --- | --- | --- | --- | --- |
| Operational Ontology branch | High domain usefulness | High if accepted later | False authority; branch-shape unresolved | Medium | Reject as tournament winner; keep candidate branch/extension choice for CAOL-006. |
| PromotionRecord | Highest cross-lane closure | High; supports all lanes and later schema work | Could become too large if it absorbs all lifecycle concepts | Medium | Select. Smallest coherent recomposable unit. |
| ReviewableSignal | Strong observability clarity | Medium; fixes signal truth risk | Too small; cannot carry promotion authority | Low | Keep as input object to PromotionRecord. |
| LifecycleEvidenceEnvelope | Strong DomainSpec fit | Medium; preserves route and stage evidence | Too source-specific for global model | Medium | Keep as adapter input to PromotionRecord. |

Selected model:

```text
ReviewableSignal / InventoryEvidence / LifecycleEvidenceEnvelope / UserDecision
  -> PromotionRecord
  -> Candidate, Premise, PromotedEntry, Policy, Constitution, Axiom, Contradiction, Retirement
```

## Current Smallest Coherent Unit

Name: `PromotionRecord`

Responsibility: represent one governed knowledge-change proposal or decision across the ontology lifecycle.

Minimum fields for CAOL-006:

| Field | Purpose |
| --- | --- |
| `id` | Stable reference for the proposed or accepted knowledge change. |
| `claim` | What is being proposed, promoted, contradicted, retired, or deferred. |
| `sourceInputs` | Source selectors, inventory entries, reviewable signals, lifecycle envelopes, or user decisions. |
| `provenance` | Entity/activity/agent-style record of what produced the claim and evidence. |
| `branchTarget` | Business, System, Bridge, or candidate Operational branch/extension. |
| `status` | Draft, candidate, premise, reviewed, promoted, policy, constitution, axiom, contradicted, retired, rejected, or deferred. |
| `evidenceConfidence` | Strength of evidence supporting or challenging the claim. |
| `commitmentConfidence` | Degree to which CyberAlchemy should rely on the claim now. |
| `reviewOwner` | Human, lifecycle, or governance owner needed for the gate. |
| `gateResult` | Pass, flag, block, defer, reject, or promote. |
| `useScope` | Where agents may rely on the result. |
| `contradictionPath` | How later evidence challenges or reopens it. |
| `rollbackOrRetirement` | How to undo, retire, or supersede the promoted effect. |
| `routeImpact` | Any affected skill, sigil, spell, task-session, invoke flow, AEO route, or DomainSpec lifecycle path. |

## Axiom / Constitution Selection

The tournament does not fully promote either definition, but it selects the smaller working model for CAOL-006:

```text
axiom = behavior invariant or load-bearing principle that must remain true for downstream governance
constitution = enforceable form/model/structure/process governance that preserves axioms, allowed transformations, and review gates
```

Decision: keep `behavior invariant` as the primary operational test for axiomhood, while allowing "load-bearing principle" as the broader evidence-backed wording. A candidate only becomes an axiom when the PromotionRecord proves it is invariant-bearing, dependency-bearing, and explicitly committed.

Decision: include process conventions in constitutions only when they preserve artifact form, model structure, allowed transformation, or invariant governance. Ordinary process preference remains policy, not constitution.

## Technique Trace

| Technique | Activation Reason | Inspected State | Decision | Readiness Effect |
| --- | --- | --- | --- | --- |
| Abstraction-level guard | Branch, lifecycle, signal, and DomainSpec models were competing at different levels. | CAOL-003 flags and CAOL-004 influence synthesis. | Select governance object level, not branch or telemetry level. | Prevents Operational Ontology or Signal from becoming overlarge authority objects. |
| Recomposition proof | Tournament must prove the selected unit recomposes into full architecture. | Four lane outputs. | PromotionRecord recomposes all lanes. | Gate satisfied. |
| Evolution profile | Future CAOL tasks will add schema and implementation plan. | CAOL-006 through CAOL-010 task queue. | Preserve schema extension boundary, defer canonical mutation. | Supports next route without overbuilding now. |
| Frame-expiry note | Current result is a planning architecture, not canonical ontology. | Package status and constraints. | Expires when CAOL-006 design or user decision changes branch shape. | Prevents false promotion. |
| Concept-vs-knowledge status | Some selected terms sound authoritative. | Operational Ontology, Verified Signal, Axiom, Constitution. | Mark output as candidate design selection. | Keeps promoted/candidate split. |
| Set-based tournament | Four lanes had competing smallest units. | Pitch-off table. | Select PromotionRecord and retain other units as inputs or branch choices. | Produces navigable result. |

## Closure Test

| Closure Question | Result |
| --- | --- |
| Responsibility named? | Yes: represent one governed knowledge-change proposal or decision. |
| Inputs named? | Yes: reviewable signals, lifecycle envelopes, inventory evidence, source selectors, user decisions. |
| Outputs named? | Yes: candidate, premise, promoted entry, policy, constitution, axiom, contradiction, retirement, rejection, deferral. |
| Abstraction level explicit? | Yes: governance object above evidence and below canonical mutation. |
| Recomposition possible without hidden glue? | Yes: adapters feed PromotionRecord; PromotionRecord routes to lifecycle outcomes. |
| Smuggled future scale avoided? | Mostly. Schema details are deferred to CAOL-006. |
| Meaning preserved if split further? | No. Splitting into signal/evidence/premise loses promotion authority and confidence coupling. |

## Recomposition Proof

```text
discovery
  -> inventory evidence
  -> reviewable signal / lifecycle evidence envelope / user decision / source selector
  -> PromotionRecord
       - claim
       - provenance
       - branch target
       - evidence confidence
       - commitment confidence
       - gate owner
       - contradiction path
       - route impact
  -> ontology candidate / premise / promoted entry / policy / constitution / axiom
  -> bridge validation
  -> operational use
  -> observability feedback
  -> new PromotionRecord, contradiction, retirement, or maintenance route
```

How the lanes recompose:

- Ontology model lane: PromotionRecord carries branch target and prevents Operational Ontology from becoming silently canonical.
- Promotion lifecycle lane: PromotionRecord is the explicit change object for promotion, rejection, contradiction, and retirement.
- Observability/signal lane: reviewable signals feed PromotionRecord but never become truth alone.
- DomainSpec/software lifecycle lane: route/stage/outcome/evidence envelopes feed PromotionRecord and later bridge validation.

## Selected Model For CAOL-006

CAOL-006 should design the architecture around this smallest coherent model:

1. Stable branch baseline: Business, System, Bridge.
2. Candidate branch extension: Operational Ontology, explicitly labeled until accepted.
3. Adapter inputs: InventoryEvidence, ReviewableSignal, LifecycleEvidenceEnvelope, UserDecision, SourceSelector.
4. Governing object: PromotionRecord.
5. Promotion outputs: Candidate, Premise, PromotedEntry, Policy, Constitution, Axiom, Contradiction, Retirement.
6. Authority rule: evidence confidence and commitment confidence are required and separate.
7. Signal rule: signals verify provenance/envelope/route shape only; meaning requires review.
8. Axiom rule: behavior-invariant test is primary for promotion; load-bearing principle is accepted as broader wording.
9. Constitution rule: process conventions are constitutional only when they preserve model/form/structure/transformation/invariant governance.

## Deferred Complexity

- Full PromotionRecord schema: defer to CAOL-006.
- Operational Ontology final branch status: defer to CAOL-006 design and later user/ontology-harness review.
- Exact review-owner matrix: defer to CAOL-006/007.
- Recurrence/severity thresholds for reviewable signals: defer to CAOL-006/007.
- Canonical ontology mutation: defer until package acceptance.

## Tension Ledger

| Tension | Tournament Decision | Route |
| --- | --- | --- |
| Operational Ontology peer branch vs candidate extension | Keep candidate; do not promote by layout. | CAOL-006 |
| Verified Signal wording | Prefer `ReviewableSignal`; if retained, verification means provenance/envelope validity only. | CAOL-006 |
| Axiom as behavior invariant vs load-bearing principle | Use behavior-invariant test for promotion; keep broader wording as evidence-compatible. | CAOL-006/007 |
| Constitution as structure governance vs process governance | Include process only when preserving form/model/structure/transformation/invariant governance. | CAOL-006/007 |
| Promotion state vs change object | Use PromotionRecord as the governing change object. | CAOL-006 |

## Verdict

`pass`

The four-lane tournament selected the smallest coherent recomposable unit: `PromotionRecord`.

No blocker disagreement repeated twice. All stable disagreements have next routes and do not block CAOL-006.

## Next Route

Proceed to CAOL-006 architecture and lifecycle design. Start with `PromotionRecord` as the governing object and repair the architecture/lifecycle files around the selected model.
