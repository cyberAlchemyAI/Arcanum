---
title: CyberAlchemy Ontology Lifecycle Execution Strategy
status: draft
createdAt: 2026-05-23
---

# Execution Strategy

## Purpose

This file holds the full strategy that does not fit inside the native Codex `/goal` character limit.

Use short `/goal` prompts from [GOALS.md](GOALS.md). Each prompt tells Codex to read this strategy, execute one bounded task from [TASKS.md](TASKS.md), and update package files.

Per-task Arcanum route, budget, gates, and stop conditions live in [TASK-STRATEGIES.md](TASK-STRATEGIES.md). That file is authoritative for executing each CAOL task.

Important: each CAOL task is a slice of the full refinement workflow, but it must still run more than one task-local pass. Do not stop at the first synthesis. Each task should produce a draft, interrogate or gate-check it, repair/optimize the smallest failing layer, then close with a task-local verification.

## Execution Rule

Every task must:

- consume [README.md](README.md), [index.json](index.json), and [CONTEXT-HANDOFF.md](CONTEXT-HANDOFF.md) first;
- consume the matching section in [TASK-STRATEGIES.md](TASK-STRATEGIES.md) before doing task work;
- write only inside `development/cyberalchemy-ontology-lifecycle/`;
- use direct file references;
- keep candidate knowledge separate from promoted knowledge;
- keep evidence confidence separate from commitment confidence;
- treat observability signals as inputs to review gates, not truth;
- update [index.json](index.json) and [TASKS.md](TASKS.md) status when done;
- stop with a checkpoint if evidence is insufficient or a decision requires user review.

Every task must record or reflect its local refinement cycle in the output artifact, task notes, or `INTERROGATION-VERDICT.md` when relevant.

## Budget Governance

Each task has a size budget in [TASK-STRATEGIES.md](TASK-STRATEGIES.md):

- `S`: focused critique or one artifact update.
- `M`: one synthesis pass plus one validation pass.
- `L`: multi-source synthesis or bounded research.
- `XL`: final cross-artifact synthesis or audit.

Budgets are stop/governance envelopes. If a task approaches its budget without satisfying its gate, produce a checkpoint instead of compressing unresolved work into a false pass.

Task-local loop guard:

- Run at least two passes per task after context consumption: draft plus critique/repair.
- Use at most the refinement cycle declared for the task in [TASK-STRATEGIES.md](TASK-STRATEGIES.md).
- If the same disagreement appears twice without new evidence, record it as an open decision.
- Do not spend a task's whole budget trying to force a clean pass; preserve the partial artifact and checkpoint.

## Full Workflow

1. Context Builder Pass
   - Convert [CONTEXT-HANDOFF.md](CONTEXT-HANDOFF.md) into a strict local evidence pack.
   - Produce selector-level excerpts, obligation coverage, gaps, contradictions, excluded candidates, fallback exploration rule, Markdown handoff, and JSON/index output.
   - Expand local search only for obligations marked partial, uncovered, candidate, draft, or initial-only.

2. Define Pass
   - Produce definitions, glossary, lifecycle boundaries, ontology branches, promotion concepts, and confidence distinctions.
   - Mark unresolved concepts as questions, not assumptions.

3. Interrogation Pass 1
   - Critique define output.
   - Find missing distinctions, contradictions, promotion gaps, lifecycle gate ambiguity, and false authority.

4. Bounded Online Research Pass
   - Fill [external-research-appendix.md](external-research-appendix.md) with up to 8 external sources.
   - Prefer standards, research papers, official docs, mature OSS architecture docs, and well-cited essays.
   - Record source type, relevance, extracted idea, fit/misfit for CyberAlchemy, and whether it changed the model.
   - Use external research as vocabulary and design pressure, not authority over local repo evidence.

5. Distill Tournament
   - Run or simulate four lanes:
     1. Ontology model lane: business, system, bridge, operational ontology.
     2. Promotion lifecycle lane: premise, knowledge, axiom, constitution, confidence, evidence, commitment.
     3. Observability and signal lane: runs, telemetry, skill use, route outcomes, reflection, verified knowledge.
     4. DomainSpec/software lifecycle lane: agentic software development flows and ontology updates.
   - Select the smallest coherent model that recomposes into the full CyberAlchemy lifecycle.

6. Design Pass
   - Update [ONTOLOGY-ARCHITECTURE.md](ONTOLOGY-ARCHITECTURE.md) and [PROMOTION-LIFECYCLE.md](PROMOTION-LIFECYCLE.md).
   - Include node types, edge types, authority levels, promotion states, confidence fields, evidence requirements, adapters, lifecycle transitions, and first use cases.

7. Interrogation Pass 2 And Repair
   - Validate the architecture.
   - Repair only flagged conceptual layer issues.
   - Do not reopen the whole model unless a blocker contradiction remains.

8. Plan Pass
   - Update [ROADMAP.md](ROADMAP.md) with phases, implementation plan, first working slice, validation strategy, and next concrete work.

9. Final Synthesis
   - Update [SUBSTACK-ARTICLE.md](SUBSTACK-ARTICLE.md).
   - Update [SOURCE-MAP.md](SOURCE-MAP.md).
   - Update [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md) with pass, flag, or block.
   - Update [index.json](index.json) obligation statuses.

## Completion Criteria

The package is complete only when it contains:

- strict context handoff summary and JSON/index;
- updated source map;
- external research appendix;
- coherent ontology architecture;
- lifecycle/promotion model;
- adapter/interface discussion;
- first use cases;
- roadmap and implementation plan;
- Substack-ready article;
- final interrogation verdict.

## Stop Conditions

Stop and report a checkpoint if:

- context coverage cannot support the model;
- axiom, constitution, premise, confidence, and signal semantics remain contradictory;
- external research changes the model materially and needs user review;
- canonical artifact mutation would be required;
- the task becomes too large for one run.
