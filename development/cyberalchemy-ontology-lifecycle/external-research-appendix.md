---
title: CyberAlchemy Ontology Lifecycle External Research Appendix
status: complete
task: CAOL-004
route: bounded-research
createdAt: 2026-05-23
updatedAt: 2026-05-24
sourceLimit: 8
refinementCycle: search/source table -> fit/misfit interrogation -> influence synthesis -> final bounded appendix
---

# External Research Appendix

## Status

CAOL-004 bounded online research is complete.

Scope: ontology engineering, provenance, knowledge graph governance, agent observability, agent memory, and software lifecycle ontologies.

Boundaries honored:

- Maximum sources: 8.
- Search depth: bounded to source discovery plus direct source inspection.
- Local evidence remains governing evidence for CyberAlchemy.
- External research is used only for vocabulary, analogy, design pressure, or rejected alternatives.

## Source Table

| Source | Type | Relevance | Extracted Idea | Fit For CyberAlchemy | Misfit / Risk | Influence |
| --- | --- | --- | --- | --- | --- | --- |
| [Ontology Development 101: A Guide to Creating Your First Ontology](https://www.gm.th-koeln.de/~hk/lehre/ki/literatur/ontology-tutorial-noy-mcguinness.pdf) | Ontology engineering guide / methodology | Gives CAOL a disciplined ontology-development frame. | Ontology design is iterative; there is no single correct model; scope and intended use decide modeling choices; evaluation happens through use and expert review. | Strong fit for the task-split CAOL flow: definitions are candidates, CAOL-003 flags alternatives, CAOL-005/006 choose the smallest useful model. | It is introductory and not governance-heavy; it should not decide CyberAlchemy authority levels. | `vocabulary` and `analogy`; reinforces iterative candidate modeling. |
| [PROV-O: The PROV Ontology](https://www.w3.org/TR/prov-o/) | W3C Recommendation / provenance ontology | Directly informs evidence envelopes, source attribution, and run provenance. | Provenance can be represented through entities, activities, agents, usage, generation, derivation, attribution, association, and delegation. | Excellent fit for adapters from observability/run artifacts into reviewable evidence. | PROV models provenance, not truth, confidence, promotion, or governance commitment by itself. | `evidence`; CAOL should align Promotion Record fields with entity/activity/agent/provenance-chain vocabulary. |
| [Data Catalog Vocabulary (DCAT) Version 3](https://www.w3.org/TR/vocab-dcat-3/) | W3C Recommendation / catalog and metadata vocabulary | Gives vocabulary for inventory/catalog records, versioning, policies, checksums, datasets, services, and provenance links. | Cataloged resources need metadata, identifiers, distributions, services, versioning, policy, quality/conformance, and provenance. | Good fit for inventory and ontology vault metadata; useful for distinguishing evidence cataloging from ontology promotion. | DCAT is data-catalog focused, so CyberAlchemy should not inherit dataset-centric assumptions for agent runs or skills. | `vocabulary`; supports inventory metadata and version/policy fields. |
| [A Change Language for Ontologies and Knowledge Graphs](https://arxiv.org/abs/2409.13906) | Research paper / KG and ontology change governance | Addresses how ontology/KG changes are requested, represented, reviewed, and applied. | KGCL treats ontology/KG evolution as explicit change objects, including human-readable change requests and applied changes. | Strong fit for Promotion Record and candidate-to-promoted transitions; supports treating agent suggestions as change proposals, not direct mutations. | It focuses on graph edit operations, not agentic lifecycle or confidence split. | `evidence` and `analogy`; CAOL should model promotions as reviewable change records. |
| [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/) | Official observability documentation | Gives stable language for structured telemetry across traces, metrics, logs, profiles, and resources. | Semantic conventions standardize common names for operations and data so telemetry is comparable across systems. | Strong fit for verified/reviewable signal criteria: route identity, trace/span/event names, attributes, resource metadata. | Telemetry conventions do not validate semantic meaning or ontology truth. | `vocabulary`; supports renaming "verified signal" to "reviewable signal" or scoping verification to transport/provenance. |
| [AgentOps Introduction](https://docs.agentops.ai/v2/introduction) | Official agent observability docs / mature OSS-adjacent platform | Provides current agent-specific observability patterns. | Agent execution can be captured as sessions, traces, LLM calls, tool calls, action events, errors, timings, SDK/framework metadata, and dashboard drilldowns. | Fits Operational Ontology as run/session/route evidence and supports the need for adapters from agent traces into ontology candidates. | Product docs can bias toward convenience and dashboards; they do not define governance or promotion truth. | `analogy`; sharpens agent observability fields without overriding Arcanum observability. |
| [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) | Research paper / agent memory architecture | Gives current agent memory vocabulary for context windows, memory tiers, reflection, and long-term interaction. | Agent memory benefits from explicit memory tiers and control flow; memory enables long-running agents to remember, reflect, and evolve. | Fits CyberAlchemy's separation between raw memory, retrieved context, inventory evidence, and ontology promotion. | MemGPT optimizes memory operation, not evidence governance; memory must not become ontology authority directly. | `analogy`; reinforces memory as operational substrate, not promoted knowledge. |
| [SEON - Software Evolution ONtologies](https://se-on.org/) | Software engineering ontology network / OWL ontology set | Directly addresses software lifecycle ontology needs. | Software evolution can be modeled through layered ontologies for stakeholders, activities, artifacts, version control, issues, code, history, and maintenance. | Strong fit for DomainSpec/software lifecycle lane: separates general concepts, domain-spanning concepts, and domain-specific software artifacts. | SEON is software-evolution oriented, not business-intent or agentic-governance oriented; CAOL should borrow layering, not the full ontology. | `analogy` and `vocabulary`; supports layered system/operational ontology modeling. |

## Fit / Misfit Interrogation

### What Repeats Across Sources

1. Provenance must identify **what changed or was produced**, **which activity produced it**, and **which agent or system bears responsibility**.
2. Metadata and cataloging make material findable and reusable, but they do not promote it into authority.
3. Ontologies and knowledge graphs change over time; serious systems represent changes as explicit requests, patches, diffs, or versioned records.
4. Observability gains value from stable event/span/log/resource conventions, but telemetry is still evidence input, not semantic truth.
5. Agent memory systems emphasize retrieval, tiering, reflection, and long-horizon context; this supports operational usefulness but not direct promotion.
6. Software lifecycle ontologies work best when layered: general concepts, domain-spanning concepts, and domain-specific artifacts.

### What Does Not Fit CyberAlchemy Directly

1. PROV-O and DCAT do not encode CyberAlchemy's evidence confidence vs commitment confidence distinction.
2. OpenTelemetry and AgentOps do not define ontology promotion, contradiction review, or lifecycle owner gates.
3. MemGPT-style memory systems can encourage persistent recall, but CyberAlchemy needs memory to remain below inventory and ontology authority.
4. SEON is valuable for software artifact modeling, but it does not include business ontology, bridge validation, or agentic governance as first-class concerns.
5. KGCL makes ontology change explicit, but CAOL still needs its own authority ladder and promotion states.

## Influence Synthesis

The external sources do not overturn the local CyberAlchemy/Arcanum model. They sharpen four design choices for CAOL-005 and CAOL-006:

1. **Promotion Record should become the governing change object.**
   KGCL and PROV-O both support making ontology changes explicit, attributable, reviewable, and replayable. CAOL should treat promotion as a governed change record, not a passive state flip.

2. **Verified Signal should be renamed or tightly scoped.**
   OpenTelemetry and AgentOps support structured telemetry, but neither makes telemetry semantically true. CAOL should use `reviewableSignal` or define `verifiedSignal` as verified provenance/envelope/route integrity only.

3. **Inventory should borrow catalog metadata, not catalog authority.**
   DCAT strengthens the distinction between findable/reusable evidence and promoted ontology knowledge. Inventory entries can have identifiers, status, versioning, provenance, checksums, policy, and quality metadata while remaining unpromoted.

4. **Operational Ontology should stay candidate until the branch model is selected.**
   SEON supports layered software lifecycle modeling, and MemGPT supports memory/operation modeling, but neither proves Operational Ontology should be a permanent peer branch. This remains a CAOL-005 tournament decision.

## Concept Fit Check

| Distill Layer | External Impact | CAOL Action |
| --- | --- | --- |
| Ontology structure | Sources support iterative/layered ontology design, not a single mandatory branch shape. | Keep Operational Ontology candidate; compare fourth-branch vs cross-branch extension in CAOL-005. |
| Promotion gates | KGCL and PROV-O support explicit change/provenance records. | Make Promotion Record the adapter output for candidate, promotion, contradiction, and retirement. |
| Signal semantics | OpenTelemetry and AgentOps support structured telemetry, not truth. | Rename or constrain Verified Signal; require review before promotion. |
| Inventory/evidence | DCAT and FAIR-adjacent vocabulary support metadata, identifiers, policies, versioning, and provenance. | Treat inventory as cataloged evidence substrate. |
| Agent memory | MemGPT supports tiered long-term memory and reflection. | Keep memory as operational substrate below inventory/ontology authority. |
| Software lifecycle | SEON supports layered software artifact and evolution ontologies. | Use SEON as analogy for System/Operational branch layering. |

## Changes To Final Model

| Source | Changed The Model? | Change |
| --- | --- | --- |
| Ontology Development 101 | Yes, mildly | Reinforces that CAOL can keep competing axiom/constitution models until task use selects one. |
| PROV-O | Yes | Promotion Record should include provenance roles equivalent to entity, activity, agent, derivation/attribution/association. |
| DCAT 3 | Yes, mildly | Inventory evidence should include catalog-style metadata such as identifier, status, version, policy, provenance, and quality/conformance hints. |
| KGCL | Yes | Promotion should be modeled as reviewable change request / accepted change / rejected change, not only as state. |
| OpenTelemetry | Yes, mildly | Signal verification should mean standardized telemetry shape and attributes, not semantic truth. |
| AgentOps | No structural change | Confirms current agent observability fields: sessions, traces, tool calls, LLM calls, errors, timings. |
| MemGPT | No structural change | Confirms memory tiering and reflection, while preserving local rule that memory is not authority. |
| SEON | Yes, mildly | Supports layered software lifecycle ontology design for CAOL-005/006. |

## CAOL-004 Gate

| Gate | Result | Evidence |
| --- | --- | --- |
| Max 8 sources | pass | Exactly 8 sources listed. |
| Source type present | pass | Every row includes Type. |
| Relevance present | pass | Every row includes Relevance. |
| Extracted idea present | pass | Every row includes Extracted Idea. |
| Fit/misfit present | pass | Every row includes Fit and Misfit/Risk. |
| Influence present | pass | Every row includes Influence and synthesis records whether it changed the model. |
| Stop rule honored | pass | Search stopped when sources repeated provenance, cataloging, change governance, telemetry, and layered ontology patterns. No source required immediate user-review blocker. |

## Next Route

Proceed to CAOL-005 distill tournament. Feed these external pressures into the four lanes:

- Ontology model lane: compare permanent fourth Operational Ontology vs candidate operational extension.
- Promotion lifecycle lane: make Promotion Record the explicit change object.
- Observability/signal lane: constrain or rename Verified Signal.
- DomainSpec/software lifecycle lane: use layered software lifecycle ontology as analogy, not authority.
