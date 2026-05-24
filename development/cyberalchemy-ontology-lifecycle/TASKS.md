---
title: CyberAlchemy Ontology Lifecycle Tasks
status: draft
createdAt: 2026-05-23
---

# Tasks

## Status Legend

- `pending`: not started.
- `active`: current task.
- `done`: complete and reflected in package files.
- `blocked`: cannot proceed without user decision or missing evidence.

## Task List

| ID | Status | Route | Budget | Refinement Cycle | Task | Outputs |
| --- | --- | --- | --- | --- | --- | --- |
| CAOL-001 | done | context-builder handoff | L | evidence -> coverage interrogation -> repair -> verify | Build strict context handoff pack from current scaffold and local evidence. | `CONTEXT-HANDOFF.md`, `SOURCE-MAP.md`, `context-pack.json`, `index.json` |
| CAOL-002 | done | invoke define | M | define -> interrogate -> compact repair -> final glossary | Define glossary, ontology branches, lifecycle terms, axiom/constitution/premise/confidence distinctions. | `DEFINITIONS-GLOSSARY.md`, updates to `ONTOLOGY-ARCHITECTURE.md`, `INTERROGATION-VERDICT.md` |
| CAOL-003 | done | interrogation | S | critique -> reduce -> repair recommendation -> verdict | Run first interrogation over definitions and lifecycle assumptions. | `INTERROGATION-VERDICT.md`, flagged questions, updated `index.json` |
| CAOL-004 | done | bounded research | L | search -> interrogate fit/misfit -> influence synthesis -> appendix | Run bounded online research pass with up to 8 sources. | `external-research-appendix.md`, source influence notes |
| CAOL-005 | done | distill tournament | L | lane draft -> lane interrogation -> tournament -> recomposition check | Run or simulate four-lane concept tournament and select smallest coherent model. | `CONCEPT-TOURNAMENT.md`, updates to architecture files |
| CAOL-006 | done | invoke design | L | design -> interrogate -> concept repair -> final architecture | Produce refined ontology architecture and promotion lifecycle. | `ONTOLOGY-ARCHITECTURE.md`, `PROMOTION-LIFECYCLE.md` |
| CAOL-007 | done | interrogation + compact repair | M | interrogate -> repair -> re-interrogate -> verdict | Run second interrogation and repair flagged conceptual issues. | `INTERROGATION-VERDICT.md`, repaired architecture/lifecycle sections |
| CAOL-008 | done | invoke plan + implementation-layering | M | plan -> interrogate -> layer repair -> final slice | Produce roadmap, implementation plan, and first working slice. | `ROADMAP.md`, `FIRST-WORKING-SLICE.md` |
| CAOL-009 | done | article synthesis | M | draft -> accuracy interrogation -> clarity repair -> final article | Produce final Substack-ready article and final synthesis. | `SUBSTACK-ARTICLE.md`, `README.md`, `index.json` |
| CAOL-010 | done | final interrogation + audit | M | audit -> interrogate -> allowed repair/checkpoint -> verdict | Final verification pass and closeout verdict. | `INTERROGATION-VERDICT.md`, `README.md`, `SOURCE-MAP.md`, `TASKS.md`, `index.json` |

Per-task lifecycle, budget, gates, and strategy live in [TASK-STRATEGIES.md](TASK-STRATEGIES.md). A task is not runnable unless the matching strategy section is read first.

## Task Boundaries

### CAOL-001

Goal: make the evidence baseline runnable.

Must inspect:

- current package files;
- CyberAlchemy ontology pack and source ledger;
- Arcanum ontology-vault, inventory, observability, invoke, task-session, Necronomicon, signal-observer, workflow-reflect, observed-invocation-loop;
- DomainSpec observability, tuning, drift/convergence, governance, Agent Execution Orchestrator evidence.

Do not synthesize final architecture yet.

### CAOL-002

Goal: define the language.

Must separate:

- business ontology;
- system ontology;
- bridge ontology;
- operational ontology;
- premise;
- axiom;
- constitution;
- evidence confidence;
- commitment confidence;
- signal;
- verified signal;
- candidate knowledge;
- promoted knowledge.

### CAOL-004

Goal: add outside perspective without letting it govern the model.

Max 8 external sources. Record fit, misfit, and influence.

### CAOL-005

Goal: converge the concept model.

Use four lanes:

- ontology model;
- promotion lifecycle;
- observability/signal;
- DomainSpec/software lifecycle.

If subagents are unavailable, simulate lanes explicitly.

### CAOL-010

Goal: decide pass, flag, or block.

Pass only if every completion criterion in [EXECUTION-STRATEGY.md](EXECUTION-STRATEGY.md) is satisfied.
