---
title: CyberAlchemy Ontology Lifecycle Definitions And Glossary
status: candidate-definition-baseline
task: CAOL-002
route: invoke-define
createdAt: 2026-05-23
refinementCycle: define -> interrogate -> compact repair -> final glossary
---

# Definitions And Glossary

## Purpose

This file is the CAOL-002 definition baseline for the CyberAlchemy ontology lifecycle package.

It defines the ontology branches, lifecycle terms, promotion terms, confidence model, signal model, and candidate/promoted knowledge distinctions needed before design and planning continue.

Status rule: these definitions are task-local candidate definitions. They may guide CAOL-003 through CAOL-006, but they do not promote canonical ontology knowledge.

## Source Basis

| Source | Used For |
| --- | --- |
| `BUSINESS-ONTOLOGY.md#L3-L35` | Business/system/bridge ontology, axioms, constitutions, premises, confidence split. |
| `arcana/ontology-vault/README.md#L33-L57` | Ontology roles, branch-aware authority, bridge evidence. |
| `spells/ontology-harness/README.md#L10-L18`, `#L66-L81` | Inventory/ontology/context-builder composition and bridge validation. |
| `../cyberAlchemy/agentic-system-glossary.md#L18-L55` | Agentic-system candidate vocabulary. |
| `../cyberAlchemy/agentic-system-ontology-entry-model.md#L57-L70` | Required ontology entry shape and confidence/promotion fields. |
| `../cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md#L82-L131` | Knowledge authority ladder and required checks. |
| `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L9-L43`, `#L151-L177` | Operational authority ladder, axiom/constitution promotion, confidence model. |
| `framework/observability/ARCHITECTURE-OVERVIEW.md#L9-L34`, `#L257-L270` | Observability as evidence and reflection route, not mutation authority. |
| `spells/observed-invocation-loop/README.md#L61-L81` | Invocation envelope, telemetry append, reflection route gates. |
| `arcana/signal-observer/README.md#L29-L47` | Behavior-level signal derivation from envelopes. |
| `arcana/workflow-reflect/README.md#L29-L37` | Cross-run evidence-backed reflection. |
| `../implementation/domainspec/DRIFT-CONVERGENCE.md#L16-L55` | Drift, convergence, Saturn control loop. |
| `../implementation/domainspec/CONSTITUTION.md#L8-L37` | Constitution as enforceable governance mapped to axioms and gates. |
| `../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md#L31-L35`, `#L79-L86` | Agent execution route lifecycle and telemetry envelope evidence. |

## Status And Confidence Legend

| Field | Meaning |
| --- | --- |
| `source-backed` | Existing local evidence already defines the term strongly enough for CAOL use. |
| `candidate` | Current package can use the term, but it is not canonical ontology authority. |
| `decision-tension` | Existing evidence supports the term, but the definition needs user or later interrogation decision before promotion. |
| `derived` | Synthesized from multiple source-backed terms for this package. |
| `evidenceConfidence` | How strongly the selected evidence supports the definition. |
| `commitmentConfidence` | How strongly CAOL should rely on the definition now. |

## Lifecycle Spine

```text
discovery
  -> inventory evidence
  -> ontology candidate
  -> premise review
  -> confidence review
  -> promoted entry / policy / constitution / axiom
  -> bridge validation
  -> operational use
  -> observability feedback
  -> new candidate, contradiction, retirement, or maintenance route
```

## Core Distinctions

### Candidate Knowledge vs Promoted Knowledge

Candidate knowledge is useful, source-linked knowledge that may guide work only while its candidate status, evidence, confidence, scope, and open questions remain visible.

Promoted knowledge is accepted for a defined scope after the appropriate review gates. Promotion requires evidence review, confidence review, owner route, contradiction path, and often decision-gate approval.

### Evidence Confidence vs Commitment Confidence

Evidence confidence asks whether the claim is well supported.

Commitment confidence asks whether the system should rely on the claim now.

The two fields must remain separate. A high-evidence fact may be low-commitment if it is not important enough to govern behavior. A low-evidence claim with high commitment is a dangerous bet and must remain gated.

### Signal vs Evidence vs Truth

A raw signal says something happened.

Evidence is a curated, source-linked support item that can be inspected.

Truth or authority is never produced by a signal alone. Signals can feed inventory entries, evidence records, reflection, and ontology candidates, but promotion requires review gates.

## Glossary

| Term | Definition | Status | Confidence Posture | Evidence | Open Questions |
| --- | --- | --- | --- | --- | --- |
| Agentic System | A coordinated stack of agents, capabilities, memory, ontology, telemetry, and governance loops that performs repository work while preserving traceable evidence. | candidate | evidence: medium; commitment: medium | `../cyberAlchemy/agentic-system-glossary.md#L34-L36` | Should this become a CyberAlchemy ontology root concept or remain package-local? |
| Ontology | Governed knowledge with roles, edges, confidence, evidence, promotion rules, and maintenance paths. | source-backed | evidence: high; commitment: high for CAOL | `arcana/ontology-vault/README.md#L5-L13`, `../cyberAlchemy/agentic-system-glossary.md#L25-L27` | None for CAOL. |
| Ontology Branch | A scoped ontology partition with its own knowledge role and authority boundary. | derived | evidence: high; commitment: high for CAOL | `BUSINESS-ONTOLOGY.md#L5-L11`, `arcana/ontology-vault/README.md#L43-L57` | Whether Operational Ontology is promoted as fourth top-level branch remains open. |
| Business Ontology | The domain intent branch: language, actors, value, rules, policies, outcomes, premises, and business-facing invariants, separated from implementation details. | source-backed | evidence: high; commitment: high | `BUSINESS-ONTOLOGY.md#L5-L11`, `arcana/ontology-vault/README.md#L43-L45` | None for CAOL. |
| System Ontology | The realization branch: codebase facts, runtime evidence, infrastructure, APIs, data flows, tests, and technical architecture. | source-backed | evidence: high; commitment: high | `BUSINESS-ONTOLOGY.md#L9-L11`, `arcana/ontology-vault/README.md#L51-L53` | None for CAOL. |
| Bridge Ontology | The traceability branch connecting business intent to system realization through evidence, tests, constraints, observations, drift, and validation links. | source-backed | evidence: high; commitment: high | `BUSINESS-ONTOLOGY.md#L10-L11`, `arcana/ontology-vault/README.md#L55-L57` | None for CAOL. |
| Operational Ontology | Candidate branch for governed knowledge about agent operation: routes, capabilities, workflow lessons, failures, maintenance proposals, context solutions, and observed execution patterns. | candidate | evidence: medium-high; commitment: medium | `../cyberAlchemy/agentic-system-architecture.md#L302-L315`, `../cyberAlchemy/agentic-system-glossary.md#L41-L41` | Should it become top-level, or remain a specialized bridge/system sub-branch until validated? |
| Discovery | The activity of finding source evidence, unknowns, vocabulary, contradictions, and possible claims before durable knowledge is created. | derived | evidence: medium; commitment: medium | `framework/CYBERALCHEMY-METHOD.md#L45-L96`, `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L34-L36` | None for CAOL. |
| Inventory | Reusable source-backed evidence storage that makes source summaries, tags, selectors, and contradictions retrievable before ontology promotion. | source-backed | evidence: high; commitment: high | `arcana/inventory/README.md#L7-L17`, `#L64-L77` | What exact inventory entry schema should represent authority ladders remains later work. |
| Ontology Candidate | A thick draft meaning object with definition, scope, evidence, edges, confidence, promotion state, and maintenance path. It may guide work only while its candidate status is visible. | source-backed | evidence: high; commitment: high for CAOL | `../cyberAlchemy/agentic-system-ontology-entry-model.md#L57-L70`, `../cyberAlchemy/ontology/README.md#L45-L51` | None for CAOL. |
| Premise | A falsifiable working bet or unverified domain/operational assumption under review. It can guide work only within explicit uncertainty, evidence, and scope. | source-backed | evidence: high; commitment: high | `BUSINESS-ONTOLOGY.md#L27-L28`, `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L38-L40` | None for CAOL. |
| Reviewed Premise | A premise that has passed premise review but remains falsifiable and scoped. | derived | evidence: medium-high; commitment: medium | `../cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md#L94-L111` | Exact state naming can be refined in CAOL-005/006. |
| Confidence Decision | A review result that separately evaluates evidence confidence and commitment confidence before stronger reliance or promotion. | source-backed | evidence: high; commitment: high | `../cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md#L112-L125`, `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L163-L177` | None for CAOL. |
| Evidence Confidence | How well a claim is supported by sources, observed reality, tests, telemetry, or reviewable artifacts. | source-backed | evidence: high; commitment: high | `BUSINESS-ONTOLOGY.md#L30-L35`, `arcana/ontology-vault/README.md#L33-L40` | None. |
| Commitment Confidence | How strongly the project/system should rely on a claim now, regardless of whether evidence is strong or weak. | source-backed | evidence: high; commitment: high | `BUSINESS-ONTOLOGY.md#L30-L35`, `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L163-L177` | None. |
| Axiom | Candidate CAOL definition: a load-bearing behavior invariant or principle that downstream governance depends on, promotable only through strong evidence, contradiction review, and explicit commitment. | decision-tension | evidence: high for load-bearing principle; commitment: medium for behavior-invariant wording | `BUSINESS-ONTOLOGY.md#L21-L22`, `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L151-L161` | Should "behavior invariant" be the primary definition, or a subtype of load-bearing principle? |
| Constitution | Candidate CAOL definition: enforceable governance for artifact form, model structure, conventions, allowed transformations, and review gates; process rules belong here only when they preserve those structures or invariants. | decision-tension | evidence: high for governance-rule role; commitment: medium for narrowed structure-governance wording | `BUSINESS-ONTOLOGY.md#L24-L25`, `../implementation/domainspec/CONSTITUTION.md#L8-L37` | Should constitutions govern process conventions broadly, or only structure/form/model/invariant preservation? |
| Policy | A scoped decision rule with owner, applicability context, and review path. | derived | evidence: medium; commitment: medium | `BUSINESS-ONTOLOGY.md#L37-L47`, `../cyberAlchemy/agentic-system-deep-dive.md#L492-L503` | Exact policy node type belongs to CAOL-006. |
| Promotion Gate | A governance decision point that determines whether a candidate becomes a premise, reviewed entry, promoted entry, policy, constitution, axiom, contradiction, or retirement. | source-backed | evidence: high; commitment: high | `../cyberAlchemy/agentic-system-glossary.md#L51-L51`, `../cyberAlchemy/agentic-system-deep-dive.md#L450-L467` | None for CAOL. |
| Decision Gate | A gate for consequential promotions or changes affecting behavior, policy, privacy, architecture, capability contracts, or commitment. | source-backed | evidence: medium-high; commitment: high | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L145-L147`, `../cyberAlchemy/agentic-system-deep-dive.md#L461-L462` | Which owner handles route-policy promotion remains open. |
| Evidence | A reviewable source, selector, artifact, test, telemetry reference, decision record, or validation report that supports or challenges a claim. | derived | evidence: high; commitment: high | `../cyberAlchemy/agentic-system-ontology-entry-model.md#L136-L146`, AEO evidence envelope sources | None. |
| Raw Observation | An unreviewed event, note, memory, run, log, or telemetry item. It is not authority. | derived | evidence: high; commitment: high | `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L29-L43`, `framework/observability/ARCHITECTURE-OVERVIEW.md#L117-L121` | None. |
| Signal | A structured observation derived from execution, telemetry, route outcome, validation state, or reflection. It can feed evidence and candidates but is not truth by itself. | source-backed | evidence: high; commitment: high | `arcana/signal-observer/README.md#L29-L47`, `spells/observed-invocation-loop/README.md#L61-L81` | None. |
| Verified Signal | Candidate CAOL definition: a signal with provenance, route/capability identity, required envelope fields, validation/terminal status, dedupe or recurrence assessment, and a review route. | candidate | evidence: medium-high; commitment: medium | `spells/observed-invocation-loop/README.md#L72-L81`, `../implementation/domainspec/docs/features/agent-execution-orchestrator/observability.md#L127-L138` | Exact recurrence/severity threshold belongs to CAOL-006/007. |
| Drift | Measurable divergence from intended behavior, semantics, contracts, runtime expectations, governance fidelity, or coordination closure. | source-backed | evidence: high; commitment: high | `../implementation/domainspec/DRIFT-CONVERGENCE.md#L16-L30` | None. |
| Convergence | Evidence-backed reduction of critical drift over time. | source-backed | evidence: high; commitment: high | `../implementation/domainspec/DRIFT-CONVERGENCE.md#L32-L41` | None. |
| Bridge Validation | The act of proving that claims about alignment between intent and implementation are supported by traceable evidence across business/system branches. | source-backed | evidence: high; commitment: high | `spells/ontology-harness/README.md#L73-L81`, `arcana/ontology-vault/README.md#L55-L57` | None. |
| Capability | A skill, sigil, spell, agent, command, adapter, route, or orchestrated lifecycle unit that performs reusable work. | derived | evidence: medium-high; commitment: medium | `framework/CYBERALCHEMY-METHOD.md#L125-L141`, `spells/invoke/README.md#L31-L47` | Exact node fields belong to CAOL-006. |
| Adapter | A transformation boundary that converts non-ontology-shaped material, such as envelopes, runtime results, DomainSpec artifacts, or user decisions, into candidate evidence or ontology candidate form. | candidate | evidence: medium-high; commitment: medium | `spells/invoke/README.md#L123-L138`, `arcana/task-session/README.md#L78-L97`, AEO interfaces | Adapter schema belongs to CAOL-006. |
| Context Solution | A task-shaped retrieval object that packages prior operational knowledge with evidence, confidence, gaps, and expiry for future agent use. | candidate | evidence: medium; commitment: medium | `../cyberAlchemy/agentic-system-architecture.md#L375-L407` | Needs validation in CAOL-005/006. |
| Promotion Record | A decision artifact recording claim, scope, evidence, confidence, gate results, decision, maintenance, and contradiction path. | candidate | evidence: medium-high; commitment: medium | `../cyberAlchemy/agentic-system-deep-dive.md#L520-L589` | Exact required schema belongs to CAOL-006. |
| Operational Use | Use of promoted or visible candidate knowledge to guide future agent routing, context selection, capability behavior, or maintenance proposals. | derived | evidence: medium; commitment: medium | `../cyberAlchemy/agentic-system-architecture.md#L165-L206`, `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md#L228-L237` | Must remain gated by status and confidence. |

## Interrogation Pass

### Findings

1. The draft could falsely promote Operational Ontology by defining it too cleanly.
   - Repair: mark Operational Ontology as `candidate` and keep top-level branch status open.

2. Axiom and constitution language could collapse into a single "important rule" bucket.
   - Repair: define axiom as invariant/principle and constitution as governance/form/model/rule structure that preserves invariants.

3. Signal and evidence could collapse if "verified signal" is overclaimed.
   - Repair: define verified signal as candidate CAOL vocabulary with provenance and review route, not as truth.

4. Evidence confidence and commitment confidence are source-backed and must be required fields for promoted/candidate ontology entries.
   - Repair: make both fields part of the status/confidence legend and glossary.

5. Adapter is needed but not yet schema-level authority.
   - Repair: mark Adapter as candidate and defer schema to CAOL-006.

## Compact Concept-Layer Repair

Smallest failing layer: authority-bearing terms around `axiom`, `constitution`, `premise`, and `signal`.

Repair model:

```text
signal: what happened, after structured observation
evidence: reviewable support or contradiction
premise: what may be true and remains falsifiable
axiom: what must stay invariant if promoted
constitution: what form/model/rules preserve invariants
policy: what scoped decision rule applies
promoted knowledge: what passed gates and may govern within scope
```

This repair preserves the user's hypothesis without pretending it is canonical:

- "Axiom as behavior invariant" is now the CAOL candidate definition.
- Existing "axiom as load-bearing principle" remains source-backed evidence.
- The unresolved question is whether behavior invariant is the primary definition or a subtype.
- "Constitution as form/model/structure governance" is now the CAOL candidate definition.
- Existing "constitution as enforceable governance/process rule" remains source-backed evidence.
- The unresolved question is whether process convention remains inside constitution when it preserves model structure.

## Final CAOL-002 Definition Gate

| Gate | Result | Notes |
| --- | --- | --- |
| Required ontology branches defined | pass | Business, System, Bridge source-backed; Operational candidate. |
| Required lifecycle terms defined | pass | Lifecycle spine, inventory, candidate, premise, confidence, promotion, bridge validation, operational use. |
| Axiom/constitution/premise distinctions visible | pass-with-decision-tension | Usable for CAOL; not promoted. |
| Evidence/commitment confidence split preserved | pass | Both defined and required. |
| Signal/evidence/truth separation preserved | pass | Verified signal remains candidate and gated. |
| Candidate/promoted knowledge separation preserved | pass | Core distinction defined. |
| Source selectors present | pass | Every term has evidence. |

## Next Route

CAOL-003 should interrogate this definition baseline before CAOL-004/005 use it for research and concept tournament work.

