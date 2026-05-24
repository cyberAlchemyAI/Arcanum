---
title: CyberAlchemy Ontology Lifecycle Architecture
status: candidate-design
task: CAOL-006
route: invoke-design
createdAt: 2026-05-23
updatedAt: 2026-05-24
refinementCycle: design draft -> interrogation -> Distill repair -> final architecture/lifecycle pass
---

# Ontology Architecture

## Status

This is a candidate architecture package for CyberAlchemy's ontology-governed agentic development lifecycle.

It does not mutate or promote canonical CyberAlchemy ontology, Arcanum runtime, Necronomicon, skill, sigil, or spell files. It is a design artifact for review and for CAOL-007 interrogation.

## Source Contracts

| Source | Design Use |
| --- | --- |
| [CONTEXT-HANDOFF.md](CONTEXT-HANDOFF.md) | Local source baseline, obligations, contradictions, and selected repo evidence. |
| [DEFINITIONS-GLOSSARY.md](DEFINITIONS-GLOSSARY.md) | Candidate vocabulary and confidence/status distinctions. |
| [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md) | CAOL-003 flags to repair: false branch authority, signal-as-truth risk, promotion-gate field gaps, axiom/constitution semantics. |
| [external-research-appendix.md](external-research-appendix.md) | External vocabulary/design pressure for provenance, catalog metadata, KG change objects, telemetry semantics, memory tiering, software ontology layering. |
| [CONCEPT-TOURNAMENT.md](CONCEPT-TOURNAMENT.md) | CAOL-005 selected model: `PromotionRecord` as smallest coherent recomposable unit. |
| [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md) | Companion lifecycle design. |

## Design Thesis

CyberAlchemy should treat agentic development as a governed knowledge-change loop, not as a memory dump and not as direct telemetry promotion.

The selected design center is:

```text
ReviewableSignal / InventoryEvidence / LifecycleEvidenceEnvelope / UserDecision / SourceSelector
  -> PromotionRecord
  -> Candidate / Premise / PromotedEntry / Policy / Constitution / Axiom / Contradiction / Retirement
```

`PromotionRecord` is the governing boundary object. It carries provenance, evidence, confidence, authority, branch placement, review owner, contradiction path, and route impact across all ontology branches.

## Six Design Views

### 1. Context View

The architecture sits between source evidence and canonical ontology/runtime authority.

| Layer | Role | Authority Boundary |
| --- | --- | --- |
| Raw source and runtime material | Source docs, run logs, telemetry envelopes, user decisions, DomainSpec/AEO route results. | Not ontology authority. |
| Evidence substrate | Inventory evidence, source selectors, reviewable signals, lifecycle evidence envelopes. | Reusable support or contradiction, not promoted meaning. |
| Governance object | PromotionRecord. | Candidate governance object; can decide state only within this package until accepted. |
| Ontology branches | Business, System, Bridge, and candidate Operational extension. | Stable branches are Business/System/Bridge; Operational remains candidate. |
| Operational use | Agent routing, context retrieval, capability lessons, maintenance proposals. | Allowed only after promotion state, use scope, and bridge validation are explicit. |

### 2. High-Level Structure View

```text
Source / Run / Decision Inputs
  -> adapters
  -> PromotionRecord
  -> branch-targeted ontology state
  -> bridge validation
  -> operational use
  -> observability feedback
  -> new PromotionRecord or contradiction
```

Stable branch baseline:

- Business Ontology: domain intent, actors, policies, value, business rules, premises, business-facing invariants.
- System Ontology: implementation facts, services, APIs, data flows, tests, infrastructure, runtime surfaces.
- Bridge Ontology: traceability, drift, evidence links, validation relationships across business/system/operation.

Candidate extension:

- Operational Ontology: agent routes, capability behavior, workflow lessons, context solution cards, route policies, observed execution patterns. It is not a permanent fourth branch until user or ontology-harness review accepts that branch shape.

### 3. Low-Level Component View

| Component | Kind | Required Fields / Responsibilities | Source Basis |
| --- | --- | --- | --- |
| `SourceSelector` | adapter input | path, anchor/line, summary, claim supported or challenged. | Context Builder and Source Map evidence. |
| `InventoryEvidence` | adapter input | source id, tags, selector, summary, contradiction notes, catalog metadata, expiry. | Inventory plus DCAT influence. |
| `ReviewableSignal` | adapter input | envelope/artifact reference, timestamp, route/capability identity, observed outcome, expected outcome, terminal/validation state, dedupe/recurrence/severity, owner route, review status. | Arcanum observability, Signal Observer, OIL, AEO observability, OpenTelemetry influence. |
| `LifecycleEvidenceEnvelope` | adapter input | DomainSpec intent, route, stage, terminal outcome, evidence envelope, telemetry pair, drift/convergence context, validation proof. | DomainSpec/AEO sources and SEON influence. |
| `UserDecision` | adapter input | decision text, owner, scope, rationale, rejected alternatives, review date. | Decision Gate and structured interview patterns. |
| `PromotionRecord` | governing object | id, claim, sourceInputs, provenance, branchTarget, status, evidenceConfidence, commitmentConfidence, reviewOwner, gateResult, useScope, contradictionPath, rollbackOrRetirement, routeImpact. | CAOL-005, PROV-O, KGCL, local authority ladder. |
| `OntologyEntry` | output | concept/premise/policy/constitution/axiom/etc., evidence, confidence, branch, edges, maintenance path. | CyberAlchemy ontology entry model and Ontology Vault. |
| `BridgeValidation` | output/gate | alignment proof from intent to system/operation with evidence and contradiction path. | Ontology Harness and Bridge Ontology sources. |

### 4. Workflow Process View

```text
discovery
  -> inventory/catalog evidence
  -> adapter-normalized input
  -> PromotionRecord draft
  -> premise/evidence/confidence review
  -> promotion outcome
  -> bridge validation
  -> operational use
  -> observability feedback
  -> new PromotionRecord, contradiction, retirement, or maintenance route
```

### 5. Decision Flow View

| Decision | Question | Default | Escalate When |
| --- | --- | --- | --- |
| Branch target | Which branch owns the claim? | Business/System/Bridge stable branch; Operational only as candidate extension. | Claim affects route policy, agent behavior, or cross-branch governance. |
| Evidence confidence | Is the claim well supported? | Assess independently from commitment. | Evidence is weak, contradictory, generated, stale, or source-indirect. |
| Commitment confidence | Should agents rely on this now? | Low until use scope, owner, and rollback are explicit. | Claim affects behavior, policy, privacy, architecture, capability contracts, or canonical ontology. |
| Signal semantics | Is this signal only reviewable, or promoted evidence? | Reviewable only. | Someone wants it to govern behavior without promotion review. |
| Axiom promotion | Is the claim invariant-bearing and dependency-bearing? | No. | It constrains downstream governance or must remain true for the model to work. |
| Constitution promotion | Does this govern form/model/structure/transformation/invariant preservation? | Policy unless it preserves those structures. | It changes artifact shape, model rules, allowed transformations, or review gates. |

### 6. Dependency Interface View

| External System / Concept | Interface Into CAOL | CAOL Output |
| --- | --- | --- |
| Arcanum observability / OIL / signal-observer | ReviewableSignal adapter. | Signal evidence inside PromotionRecord. |
| Inventory / context-builder | InventoryEvidence and SourceSelector adapters. | Candidate entry and source map references. |
| Ontology Vault / ontology-harness | Promotion and bridge validation gates. | Branch-aware ontology candidate or promoted record proposal. |
| Necronomicon / invoke / task-session | Runtime route and artifact provenance. | Operational candidate, policy candidate, or maintenance route. |
| Skills / sigils / spells | Capability contract adapter. | Capability, policy, constitution, or route-impact candidate. |
| DomainSpec / AEO | LifecycleEvidenceEnvelope adapter. | Bridge validation and software lifecycle ontology candidate. |
| User review / decision-gate | UserDecision adapter. | Approved, deferred, rejected, or blocker PromotionRecord state. |

## Ontology Branches

| Branch | Authority Status | Owns | Does Not Own | CAOL-006 Rule |
| --- | --- | --- | --- | --- |
| Business Ontology | stable local model | Domain intent, actors, policies, value, business rules, premises, business-facing invariants. | Code structure, transient execution details, raw telemetry. | Business-facing claims require business evidence or user decision before promotion. |
| System Ontology | stable local model | Codebase facts, services, APIs, data flows, tests, infrastructure, runtime behavior, execution surfaces. | Business policy justification. | System claims require source, test, runtime, or implementation evidence. |
| Bridge Ontology | stable local model | Traceability, drift, residue, evidence links, validation relationships between business, system, and operation. | Source truth of either side. | Bridge claims require at least two-sided evidence or explicit contradiction. |
| Operational Ontology | candidate extension | Agent routes, capability behavior, workflow lessons, context solution cards, route policies, observed execution patterns. | Raw memory, raw logs, unreviewed telemetry, canonical capability mutation. | Must be labeled candidate until accepted; operational claims route through PromotionRecord. |

## Node Types

| Type | Branches | Meaning | Authority Notes |
| --- | --- | --- | --- |
| `Concept` | all | Named semantic object with scope and definition. | Must cite source/evidence when used beyond draft. |
| `SourceSelector` | bridge | Source path/anchor used as evidence. | Evidence pointer only. |
| `InventoryEvidence` | bridge | Cataloged reusable evidence with summary, tags, selectors, metadata, and contradictions. | Not governed meaning by itself. |
| `ReviewableSignal` | bridge, system, candidate operational | Structured observation from a run, route, telemetry envelope, test, outcome, or reflection. | Verifies provenance/envelope/route shape only, not truth. |
| `LifecycleEvidenceEnvelope` | bridge, system, candidate operational | DomainSpec/AEO route-stage-outcome evidence bundle. | Input to PromotionRecord and bridge validation. |
| `PromotionRecord` | bridge, candidate operational | Governed knowledge-change proposal or decision. | Required boundary object for promotion, contradiction, retirement, and route-impact changes. |
| `OntologyCandidate` | all | Thick draft meaning object with branch, scope, evidence, confidence, edges, and maintenance path. | Can guide only if candidate status is visible. |
| `Premise` | business, bridge, candidate operational | Falsifiable working bet with explicit uncertainty. | Must retain falsification criteria. |
| `Policy` | business, candidate operational | Scoped decision rule with owner and applicability. | Does not become constitution unless it preserves model/form/invariant governance. |
| `Constitution` | business, system, candidate operational | Enforceable governance for artifact form, model structure, allowed transformations, review gates, and process rules that preserve those invariants. | Requires decision gate, owner, rollback, and affected artifact scope. |
| `Axiom` | business, bridge, candidate operational | Behavior invariant or load-bearing principle that downstream governance depends on. | Requires invariant-bearing test, dependency review, strong evidence, and explicit commitment. |
| `Capability` | system, candidate operational | Skill, sigil, spell, agent, command, runtime adapter, or orchestrated route. | Capability changes remain owned by their lifecycle; ontology proposes, it does not mutate. |
| `ContextSolution` | candidate operational | Reusable task-shaped retrieval pattern with evidence, confidence, gaps, and expiry. | Must expire or be revalidated. |
| `DriftFinding` | bridge | Mismatch between intended meaning and system/operational behavior. | Can trigger PromotionRecord or contradiction. |

## Edge Types

| Edge | From -> To | Meaning | Gate |
| --- | --- | --- | --- |
| `traced_to` | any claim -> SourceSelector/InventoryEvidence | Claim cites source evidence. | Source relevance and selector validity. |
| `generated_by` | PromotionRecord -> provenance activity/agent | Claim or evidence came from a named activity/agent. | Provenance present. |
| `feeds_record` | ReviewableSignal/LifecycleEvidenceEnvelope/UserDecision -> PromotionRecord | Input contributes to a governance decision. | Input normalized by adapter. |
| `targets_branch` | PromotionRecord -> branch | Record proposes branch placement. | Branch authority check. |
| `promotes_to` | PromotionRecord -> outcome node | Record changes status. | Review owner and confidence gates. |
| `validated_by` | PromotionRecord/Entry -> BridgeValidation | Claim is supported by bridge proof. | Traceability evidence. |
| `challenged_by` | Entry -> DriftFinding/contradiction record | Evidence creates uncertainty or contradiction. | Contradiction path. |
| `governs` | Axiom/Constitution/Policy -> downstream object | Governance constrains behavior, structure, or decisions. | Decision gate and rollback path. |
| `realized_by` | Business/Operational concept -> System concept | Intent is implemented or executed. | Bridge validation. |
| `routes_to` | PromotionRecord -> lifecycle owner | Work belongs to ontology-vault, ontology-harness, task-session, invoke, sigil-development, etc. | Owner is explicit. |
| `expires_when` | candidate/context solution -> condition | Validity ends when evidence becomes stale or scope changes. | Expiry/review rule. |

## Authority Levels

| Level | Name | Can Guide Agents? | PromotionRecord Role | Required Evidence |
| --- | --- | --- | --- | --- |
| L0 | Raw observation | No | None; may be adapted later. | Run, note, log, memory, source mention. |
| L1 | Cataloged evidence | Only as cited support. | Input to PromotionRecord. | Source selector, inventory metadata, summary, contradiction notes. |
| L2 | Reviewable signal / lifecycle envelope | Only as review input. | Input to PromotionRecord. | Provenance, route/stage/outcome, validation or terminal state, dedupe/severity. |
| L3 | Ontology candidate | Yes, with visible candidate status. | Created or updated by PromotionRecord. | Claim, scope, branch, evidence, confidence split, owner. |
| L4 | Reviewed premise | Yes, within falsifiable scope. | PromotionRecord records premise review. | Falsification criteria, contradiction path, owner. |
| L5 | Promoted entry / policy | Yes, within use scope. | PromotionRecord records decision and use scope. | Confidence review, approval, rollback/retirement path. |
| L6 | Constitution | Yes, as structure/model/form governance. | PromotionRecord records governance decision. | Affected artifacts, allowed transformations, review gates, rollback. |
| L7 | Axiom | Yes, as invariant-bearing governance. | PromotionRecord records explicit commitment. | Strong evidence, dependency review, contradiction review, explicit commitment. |

## Confidence Model

Every PromotionRecord and non-raw ontology candidate must carry:

| Field | Meaning | Failure Mode If Missing |
| --- | --- | --- |
| `evidenceConfidence` | How strongly the selected evidence supports or challenges the claim. | Weak evidence can be mistaken for knowledge. |
| `commitmentConfidence` | How strongly CyberAlchemy should rely on the claim now. | High-risk claims can silently govern behavior. |

Confidence is not a single score. Evidence can be strong while commitment remains low because the claim is outside scope, too risky, or not yet reviewed. Commitment can never outrun evidence without explicit risk acceptance and review-owner signoff.

## Evidence Rules

1. Raw memory, telemetry, and source digests are not ontology authority.
2. Evidence must be source-linked, reviewable, and scoped.
3. Evidence can support, challenge, narrow, or retire a claim.
4. Observability signals become evidence only after adapter normalization and review route assignment.
5. DomainSpec/AEO outputs become evidence through LifecycleEvidenceEnvelope, not by direct ontology mutation.
6. User decisions are evidence only with owner, scope, rationale, and rejected alternatives.
7. External research can supply vocabulary and design pressure but does not override local repo evidence.

## PromotionRecord Schema

| Field | Required? | Description |
| --- | --- | --- |
| `id` | yes | Stable reference for the knowledge-change proposal or decision. |
| `claim` | yes | Statement being proposed, promoted, contradicted, retired, or deferred. |
| `claimType` | yes | concept, premise, policy, constitution, axiom, capability, context-solution, drift, contradiction, retirement. |
| `sourceInputs` | yes | SourceSelector, InventoryEvidence, ReviewableSignal, LifecycleEvidenceEnvelope, or UserDecision references. |
| `provenance` | yes | Activity/agent/entity-style record of how claim and evidence were produced. |
| `branchTarget` | yes | Business, System, Bridge, or candidate Operational extension. |
| `status` | yes | draft, candidate, premise, reviewed, promoted, policy, constitution, axiom, contradicted, retired, rejected, deferred. |
| `evidenceConfidence` | yes | Evidence support level plus rationale. |
| `commitmentConfidence` | yes | Reliance level plus rationale. |
| `reviewOwner` | yes | Human or lifecycle owner needed for the gate. |
| `gateResult` | yes | pass, flag, block, defer, reject, promote, contradict, retire. |
| `useScope` | yes for promoted use | Where agents may rely on the result. |
| `contradictionPath` | yes | How later evidence challenges, reopens, or invalidates the record. |
| `rollbackOrRetirement` | yes for promoted use | How to undo, supersede, or retire the effect. |
| `routeImpact` | conditional | Affected skill, sigil, spell, task-session, invoke flow, AEO route, DomainSpec lifecycle, or context-builder retrieval. |
| `bridgeValidation` | conditional | Required before operational use or cross-branch authority. |
| `expiresWhen` | conditional | Expiry condition for context solutions, operational lessons, and version-sensitive evidence. |

### PromotionRecord Boundary

CAOL-007 repair: PromotionRecord is not a general container for all ontology data. It is only the governed change record for one claim or decision.

It may contain:

- one primary claim;
- pointers to source inputs;
- provenance for how the claim/evidence was produced;
- confidence and commitment decisions;
- branch target and outcome state;
- gate owner and route impact;
- contradiction, rollback, retirement, and expiry paths.

It must not contain:

- full source excerpts;
- raw telemetry payloads;
- complete ontology entry bodies when a pointer is enough;
- implementation plans;
- canonical runtime mutation instructions;
- unrelated claims bundled for convenience.

If a claim needs independent evidence, owner, confidence, or rollback, it needs its own PromotionRecord linked by `related_record`, not an overloaded record.

## Adapter Design

| Adapter | Input | Output | Must Preserve | Must Not Do |
| --- | --- | --- | --- | --- |
| Source-to-inventory adapter | Source files, docs, source digests. | InventoryEvidence / SourceSelector. | Path, selector, summary, contradiction notes, metadata. | Promote meaning. |
| Signal-to-record adapter | OIL envelopes, signal-observer outputs, telemetry, validation outcomes. | ReviewableSignal, then PromotionRecord draft. | Provenance, route identity, observed/expected outcome, terminal state, dedupe/severity, owner route. | Claim signal truth. |
| Lifecycle-envelope adapter | DomainSpec/AEO route, stage, evidence, telemetry, terminal outcomes. | LifecycleEvidenceEnvelope, then PromotionRecord draft. | Intent, route, stage, terminal outcome, evidence envelope, drift/convergence context. | Collapse implementation outcome into business truth. |
| Capability-contract adapter | Skills, sigils, spells, invoke/task-session routes. | Capability, policy, constitution, or route-impact PromotionRecord. | Capability owner, lifecycle boundary, install/runtime status, observability support. | Mutate capability files without lifecycle authority. |
| Decision adapter | User decisions, decision-gate outputs, structured interviews. | UserDecision and PromotionRecord decision. | Owner, scope, rationale, rejected alternatives, expiry/review date. | Hide unresolved ambiguity. |

## Review Owner Matrix

CAOL-007 repair: owner routing must be explicit enough to prevent vague gates.

| PromotionRecord Claim Type | Default Review Owner | Escalate To | Required Before Use |
| --- | --- | --- | --- |
| Business concept / premise | business ontology reviewer or user domain owner | decision-gate when policy/invariant impact exists | source evidence, scope, falsification path. |
| System concept / implementation fact | system ontology reviewer or repository maintainer | technical owner when architecture/runtime behavior changes | source/test/runtime evidence and affected system scope. |
| Bridge validation / drift finding | bridge ontology reviewer | ontology-harness when cross-branch alignment is claimed | two-sided evidence and contradiction path. |
| Operational lesson / route policy | operational lifecycle reviewer | sigil-development, spellcraft, invoke, task-session, or observability owner when route behavior changes | ReviewableSignal or run evidence, recurrence/severity, route impact, rollback. |
| Capability contract | owning skill/sigil/spell lifecycle | capability maintainer or user approval for behavior change | owner, installed/runtime surface, validation evidence, rollback. |
| Constitution | governance owner for affected artifact/model | decision-gate before structural governance | affected scope, allowed transformations, preserved invariant/gate, rollback. |
| Axiom | ontology governance owner plus user review | decision-gate before commitment | invariant/dependency proof, strong evidence, contradiction review, explicit commitment. |

No PromotionRecord can reach promoted, policy, constitution, or axiom state with `reviewOwner = unknown`.

## Axiom And Constitution Semantics

| Concept | CAOL-006 Working Definition | Promotion Test | Not This |
| --- | --- | --- | --- |
| Axiom | Behavior invariant or load-bearing principle that downstream governance depends on. | PromotionRecord proves invariant-bearing, dependency-bearing, strongly evidenced, contradiction-reviewed, and explicitly committed. | A useful rule of thumb or observed pattern. |
| Constitution | Enforceable governance for form, model structure, allowed transformations, review gates, and process rules that preserve those invariants. | PromotionRecord proves affected artifact/model scope, governed transformations, owner, rollback, and relation to axioms/gates. | Ordinary workflow preference or local style choice. |
| Policy | Scoped decision rule with owner and applicability. | PromotionRecord proves use scope and owner. | Structural governance unless it preserves model/form/invariant behavior. |
| Premise | Falsifiable working bet. | PromotionRecord records uncertainty, falsification path, evidence, and owner. | A promoted fact or axiom. |

## Observability-Backed Validation

Observability contributes reviewable evidence through ReviewableSignal. It does not prove ontology truth by itself.

A ReviewableSignal is valid only when it has:

- envelope or artifact reference;
- timestamp;
- route/capability identity;
- observed outcome;
- expected outcome or governing intent;
- terminal status or validation state;
- failure/success mode;
- dedupe, recurrence, or severity assessment;
- owner route;
- confidence impact;
- review status;
- candidate PromotionRecord target.

ReviewableSignal can:

- create a PromotionRecord draft;
- support or challenge an existing PromotionRecord;
- trigger drift finding or maintenance route;
- contribute to bridge validation.

ReviewableSignal cannot:

- directly create promoted knowledge;
- mutate skill/sigil/spell/runtime files;
- bypass evidence confidence or commitment confidence;
- become "truth" without review.

## Use Cases

### 1. Any Repository Using Arcanum

Flow:

```text
task-session/invoke/sigil run
  -> observability envelope
  -> ReviewableSignal
  -> PromotionRecord draft
  -> candidate operational lesson or route policy
  -> bridge validation / lifecycle owner review
  -> scoped operational use
```

Expected output: operational knowledge candidates such as "this route needs stricter context-builder handoff" or "this sigil repeatedly emits incomplete telemetry." They remain candidates until PromotionRecord gates pass.

### 2. Software Development Agent Lifecycle

Flow:

```text
DomainSpec intent
  -> AEO route/stage execution
  -> LifecycleEvidenceEnvelope
  -> PromotionRecord
  -> System/Bridge/Operational candidate
  -> bridge validation
  -> promoted guidance or contradiction
```

Expected output: traceable lifecycle knowledge such as route reliability, evidence-envelope completeness, drift findings, or validation obligations.

### 3. Business Software Knowledge Discovery

Flow:

```text
business docs/interviews
  -> InventoryEvidence / SourceSelector
  -> PromotionRecord
  -> Business Ontology candidate or premise
  -> System realization mapping
  -> Bridge validation
  -> policy, constitution, axiom, or scoped promoted entry
```

Expected output: business terms, premises, policies, and invariants that are visibly grounded in evidence and separate from implementation claims.

## Interrogation Pass

### Findings

1. Operational Ontology false authority risk remains if displayed as peer branch without status.
   - Repair: every branch table labels Operational Ontology as candidate extension.

2. PromotionRecord could become a vague "everything object."
   - Repair: define adapter inputs, required fields, authority role, and outputs; defer full implementation schema to later accepted work.

3. ReviewableSignal could still overclaim if "validated" language leaks in.
   - Repair: use `ReviewableSignal`; define verification as provenance/envelope/route validity only.

4. Axiom and constitution could collapse.
   - Repair: axiom uses invariant-bearing/dependency-bearing test; constitution uses form/model/structure/transformation/invariant preservation test.

5. Operational use could bypass bridge validation.
   - Repair: authority levels and lifecycle require bridge validation before operational use.

## Concept-Layer Repair

Smallest repaired layer:

```text
adapter input -> PromotionRecord -> lifecycle outcome
```

This prevents three common failures:

- signals becoming truth;
- operational branch becoming canonical by implication;
- promotion becoming an invisible state flip.

## CAOL-007 Compact Repair Addendum

Second interrogation found no blocker contradiction, but it flagged four conceptual issues and repaired them in place:

| Flag | Repair |
| --- | --- |
| PromotionRecord overbreadth | Added PromotionRecord Boundary: one primary claim per record, pointer-based inputs, no raw telemetry/source dumps, no bundled unrelated claims. |
| Weak owner/gate specificity | Added Review Owner Matrix with default owners, escalation paths, and required evidence before use. |
| Bridge-validation ambiguity | Companion lifecycle now defines bridge validation outcomes: aligned, partial, drift, insufficient, contradicted. |
| Signal threshold ambiguity | Companion lifecycle now defines recurrence/severity thresholds and states that thresholds affect evidence confidence, not commitment confidence. |

Re-interrogation verdict: `pass-with-explicit-review-items`. False authority, signal truth claims, and confidence collapse are absent in the repaired sections. Remaining review items are schema normalization and final owner assignments, both routed to CAOL-008 planning or later user decision.

## Design Decisions

| Decision | Result | Rationale |
| --- | --- | --- |
| Core unit | PromotionRecord | Smallest cross-lane unit with governance closure. |
| Branch shape | Business/System/Bridge stable; Operational candidate extension. | Avoid false authority while preserving operational modeling. |
| Signal term | ReviewableSignal | Avoids truth-like "VerifiedSignal" language. |
| Axiom test | Invariant-bearing plus dependency-bearing. | Reconciles user hypothesis with source-backed load-bearing principle model. |
| Constitution test | Form/model/structure/transformation/invariant preservation. | Keeps process rules constitutional only when they preserve governed structure. |
| Operational use | Behind promotion state, use scope, and bridge validation. | Prevents raw observations from governing agents. |

## Risks And Gaps

| Risk / Gap | Severity | Route |
| --- | --- | --- |
| PromotionRecord schema may need normalization before implementation. | medium | CAOL-007/008 |
| Operational Ontology branch status still needs user or ontology-harness acceptance. | medium | CAOL-007 or later decision-gate |
| Review owner matrix is not final. | medium | CAOL-007/008 |
| Signal recurrence/severity thresholds are not final. | medium | CAOL-007/008 |
| No canonical ontology mutation has happened. | intentional | Later user-approved route only. |

## CAOL-006 Gate

| Gate | Result | Evidence |
| --- | --- | --- |
| Branches included | pass | Business, System, Bridge, candidate Operational extension. |
| Nodes included | pass | Node table includes source, evidence, signal, lifecycle envelope, PromotionRecord, candidates, premises, policies, constitutions, axioms, capabilities, context solutions, drift findings. |
| Edges included | pass | Edge table includes trace, provenance, feed, target, promote, validate, challenge, govern, realize, route, expire. |
| Authority included | pass | Authority levels L0-L7 and branch status. |
| Confidence included | pass | Evidence confidence and commitment confidence required and distinct. |
| Promotion states included | pass | PromotionRecord status and output states listed. |
| Evidence rules included | pass | Evidence rules and adapter boundaries included. |
| Adapters included | pass | Five adapters with inputs, outputs, preserved fields, and forbidden behavior. |
| Lifecycle included | pass | Workflow process view and companion lifecycle file. |
| Use cases included | pass | Arcanum repo, software development lifecycle, business software discovery. |
| Stop condition avoided | pass | No canonical ontology/runtime mutation required. |

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: CAOL architecture package
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md), [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md)
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: package-local architecture bundle driven by CAOL-005 tournament
- Implementation layering: gap recorded for CAOL-008
- Work-pack: n/a
- Decisions: PromotionRecord-centered architecture; ReviewableSignal; candidate Operational Ontology extension; invariant-bearing axiom test; structure-preserving constitution test
- Unresolved gaps: review owner matrix, recurrence/severity thresholds, canonical acceptance path
- Next route: CAOL-007 interrogation plus compact repair

## Observability Closeout

- `OBSERVATION`: CAOL-006 converted define/research/tournament evidence into a PromotionRecord-centered architecture design.
- `LEDGER`: Updated [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md), [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md), [TASKS.md](TASKS.md), and [index.json](index.json).
- `REFLECTION_TRIGGER`: no immediate workflow-reflect trigger; CAOL-007 should interrogate the design.
- `RECOMMENDATION`: proceed to CAOL-007 to test false authority, vague gates, signal truth claims, and confidence collapse.
- `DEDUPE_KEY`: `caol-006-invoke-design-2026-05-24`
