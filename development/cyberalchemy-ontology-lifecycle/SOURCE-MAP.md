---
title: CyberAlchemy Ontology Lifecycle Source Map
status: final-source-map
task: CAOL-010
createdAt: 2026-05-23
updatedAt: 2026-05-24
---

# Source Map

## Authority Precedence

1. Canonical local source files in Arcanum, CyberAlchemy, and DomainSpec.
2. Existing CyberAlchemy ontology source digests and entries, treated as candidate evidence.
3. Curated development/provenance plans.
4. Runtime signal docs and feature packs.
5. External research, only in CAOL-004 and only as vocabulary/design pressure.
6. Raw memory or telemetry, never authority by itself.

## Inspected Source Set

| Path | Source Area | Relevance | Extracted Idea | Fit / Misfit |
| --- | --- | --- | --- | --- |
| `BUSINESS-ONTOLOGY.md` | Arcanum | Branch-aware ontology and knowledge substrate. | Business/system/bridge split; axioms, constitutions, premises, confidence split. | Strong fit; axiom/constitution semantics need correction review. |
| `arcana/ontology-vault/README.md` | Arcanum | Ontology governance owner. | Knowledge roles, maturity states, confidence, branch mapping, premise review, promotion/demotion. | Strong fit. |
| `spells/ontology-harness/README.md` | Arcanum | Composition route for inventory + ontology-vault + context-builder. | Branch-aware path maps business/system and validates bridge; blocks false alignment. | Strong fit. |
| `arcana/inventory/README.md` | Arcanum | Evidence substrate before ontology. | Inventory stores reusable source-backed knowledge and feeds context-builder. | Strong fit; inventory is not ontology authority. |
| `framework/CYBERALCHEMY-METHOD.md` | Arcanum | Governing method. | Agent work becomes governed artifacts through discovery, tension, traceability, routing, and reflection. | Strong fit. |
| `spells/necronomicon/development/KNOWLEDGE-SUBSTRATE-FLOW.md` | Arcanum | Operational knowledge ladder. | Raw interaction moves through session evidence, inventory, ontology candidate, premise/confidence review, constitution/axiom, bridge evidence. | Strong fit. |
| `spells/necronomicon/development/OBSERVABILITY-PROVENANCE-PLAN.md` | Arcanum | Observability ownership and adapter boundary. | Observed capability and target artifact ownership must be separated; high-risk commands need subject metadata. | Strong fit. |
| `spells/invoke/README.md` | Arcanum | Define/design/plan authoring route. | Invoke authors handoff artifacts but does not own target lifecycle completion. | Strong fit for lifecycle boundaries. |
| `arcana/task-session/README.md` | Arcanum | Bounded execution and context handoff. | Runtime-goal handoff needs strict Markdown plus JSON/index context pack. | Strong fit for CAOL execution mechanics. |
| `framework/observability/ARCHITECTURE-OVERVIEW.md` | Arcanum | Repository-local telemetry/reflection architecture. | Run evidence becomes envelopes, ledger rows, indexes, counters, and reflection routes; observer records evidence, not meaning. | Strong fit. |
| `spells/observed-invocation-loop/README.md` | Arcanum | Managed invocation observation. | OIL appends exactly one telemetry signal and routes to reflection when thresholds/gates require. | Strong fit. |
| `arcana/signal-observer/README.md` | Arcanum | Signal derivation route. | Converts invocation envelopes into behavior-level signals and reflection recommendations. | Strong fit; not promotion authority. |
| `arcana/workflow-reflect/README.md` | Arcanum | Cross-run reflection. | Accumulated telemetry becomes evidence-backed improvement proposals. | Strong fit. |
| `../cyberAlchemy/ontology/README.md` | CyberAlchemy | Candidate ontology pack. | Entries must name evidence, confidence, promotion state, next gate, and contradiction path. | Strong fit. |
| `../cyberAlchemy/ontology/source-ledger.md` | CyberAlchemy | Source digest ledger. | Source files become digests, then ontology evidence, then context-builder retrieval. | Strong fit. |
| `../cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md` | CyberAlchemy | Existing candidate authority ladder. | Controls progression from raw evidence into promoted ontology and downstream updates. | Strong fit; still candidate. |
| `../cyberAlchemy/agentic-system-glossary.md` | CyberAlchemy | Candidate vocabulary. | Defines operational ontology, promotion gate, schema/evidence layers, feedback loop. | Strong fit; terms remain candidate. |
| `../cyberAlchemy/agentic-system-ontology-entry-model.md` | CyberAlchemy | Ontology entry shape. | Thick entries require content, context, agent payload, edges, evidence, confidence, promotion, maintenance. | Strong fit. |
| `../cyberAlchemy/agentic-system-architecture.md` | CyberAlchemy | Candidate architecture. | Operational Ontology as fourth branch, memory separation, route ledger, context cards, signal bridge. | Strong fit; candidate-only. |
| `../cyberAlchemy/agentic-system-deep-dive.md` | CyberAlchemy | Deep architecture/promotion rationale. | Ontology Promotion System, gates, confidence matrix, non-promotion rules, observability/reflection. | Strong fit. |
| `../implementation/domainspec/README.md` | DomainSpec | Structured intent overview. | Spec-first chain of custody from business intent to observability and verification. | Strong fit. |
| `../implementation/domainspec/AUTHORITY-MAP.md` | DomainSpec | Canonical source routing. | Defines where DomainSpec concepts, governance, drift, observability, and feature truth live. | Strong fit. |
| `../implementation/domainspec/CONSTITUTION.md` | DomainSpec | Governance rule model. | Constitution binds rules to axioms and gates; rules are pruned by evidence. | Strong fit for constitution semantics tension. |
| `../implementation/domainspec/OBSERVABILITY.md` | DomainSpec | Doc-to-metric derivation. | Outer loop validates production behavior, metrics cite documentation source, drift triggers correction. | Strong fit. |
| `../implementation/domainspec/TUNING-LOOP.md` | DomainSpec | Async signal learning. | Fast append-only observation plus async threshold analysis and evidence-backed proposals. | Strong fit. |
| `../implementation/domainspec/DRIFT-CONVERGENCE.md` | DomainSpec | Drift/convergence semantics. | Drift is measurable divergence; convergence is evidence-backed reduction; Saturn acts on drift. | Strong fit. |
| `../implementation/domainspec/docs/features/agent-execution-orchestrator/SPEC.md` | DomainSpec AEO | Agent execution lifecycle. | AEO owns deterministic route composition, run semantics, telemetry envelopes, and governance signal emission. | Strong fit. |
| `../implementation/domainspec/docs/features/agent-execution-orchestrator/interfaces.md` | DomainSpec AEO | Adapter/interface contracts. | Route artifact, sandbox, telemetry ledger, terminal guard, and signal observer interfaces. | Strong fit. |
| `../implementation/domainspec/docs/features/agent-execution-orchestrator/rules.md` | DomainSpec AEO | Run/evidence invariants. | Terminal outcomes, telemetry pair requirement, artifact evidence minimum. | Strong fit. |
| `../implementation/domainspec/docs/features/agent-execution-orchestrator/observability.md` | DomainSpec AEO | AEO observability mapping. | Delegation ledger, terminal guard, signal observer, standard evidence envelope checklist. | Strong fit. |

## Coverage By Obligation

| Obligation | Evidence Coverage |
| --- | --- |
| O1 Definitions/glossary | Business Ontology, Ontology Vault, CyberAlchemy glossary, ontology entry model. |
| O2 Architecture branches | Business Ontology, Ontology Vault, Ontology Harness, CyberAlchemy architecture/deep dive. |
| O3 Promotion mechanisms | Knowledge ladder, Necronomicon substrate, Ontology Harness, Ontology Vault, source ledger. |
| O4 Observability validation | Observability overview, OIL, Signal Observer, Workflow Reflect, DomainSpec observability/tuning, AEO observability. |
| O5 DomainSpec execution | DomainSpec README, Authority Map, Constitution, Drift/Convergence, AEO SPEC/interfaces/rules/observability. |
| O6 Source map | This file. |
| O7 External research | Covered by [external-research-appendix.md](external-research-appendix.md), with 8 bounded sources and influence synthesis. |
| O8 Axiom/constitution | Business Ontology, Necronomicon substrate, DomainSpec Constitution, Authority Map. |
| O9 Adapters/interfaces | Invoke provenance, Task Session adapters, Observability Provenance, AEO interfaces/rules. |
| O10 First use cases | CyberAlchemy architecture/deep dive and DomainSpec/AEO execution evidence. |
| O11 Roadmap/plan | Covered by [ROADMAP.md](ROADMAP.md) and [FIRST-WORKING-SLICE.md](FIRST-WORKING-SLICE.md). |
| O12 Article | Covered by [SUBSTACK-ARTICLE.md](SUBSTACK-ARTICLE.md), with candidate/promoted and signal-not-truth caveats preserved. |
| O13 Final verdict | Covered by [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md) CAOL-010 final verification. |

## Current Evidence Verdict

`pass`

The local evidence and package artifacts are sufficient to mark the CyberAlchemy ontology lifecycle architecture package complete as a reviewed candidate package. This is not canonical ontology promotion; unresolved acceptance decisions remain in [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md).
