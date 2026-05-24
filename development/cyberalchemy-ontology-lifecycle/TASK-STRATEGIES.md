---
title: CyberAlchemy Ontology Lifecycle Task Strategies
status: draft
createdAt: 2026-05-23
---

# Task Strategies

This file carries the Arcanum lifecycle strategy and budget envelope for every CAOL task. Short `/goal` prompts should point to [TASKS.md](TASKS.md), but each task must execute through the matching strategy here.

## Shared Lifecycle Contract

The full 11-step refinement workflow is the workstream spine across CAOL-001 through CAOL-010. It must not be rerun in full inside every task.

Each individual task still needs more than one pass. Every task follows a bounded Arcanum-shaped refinement loop:

```text
orient
  -> consume context
  -> invoke/produce draft artifact
  -> interrogate or gate-check the draft
  -> optimize/repair the smallest failing concept layer
  -> update artifact
  -> final task-local gate/check
  -> update package state
  -> hand off next route
```

Minimum rule:

- No task should stop after its first synthesis pass unless it is blocked before synthesis.
- Every task must include at least one critique/gate pass after the first output.
- Tasks with conceptual synthesis must include a Distill check or an explicit explanation of why the optimizer is not applicable.
- If the same disagreement appears twice without new evidence, stop and record it as an open decision instead of looping.

Required inputs for every task:

- [README.md](README.md)
- [EXECUTION-STRATEGY.md](EXECUTION-STRATEGY.md)
- [TASKS.md](TASKS.md)
- [TASK-STRATEGIES.md](TASK-STRATEGIES.md)
- [index.json](index.json)
- [CONTEXT-HANDOFF.md](CONTEXT-HANDOFF.md)
- [context-pack.json](context-pack.json), after CAOL-001

Required closeout for every task:

- update [TASKS.md](TASKS.md) status;
- update [index.json](index.json) task and obligation status;
- record blockers or decision questions in [INTERROGATION-VERDICT.md](INTERROGATION-VERDICT.md) when relevant;
- do not mutate canonical ontology, skill, sigil, spell, or runtime files;
- keep writes inside `development/cyberalchemy-ontology-lifecycle/`.

## Budget Model

Budgets are governance envelopes, not exact token meters. If a task approaches its budget before satisfying its acceptance criteria, stop with a checkpoint rather than forcing completion.

| Size | Expected Work | Minimum Refinement | Stop Rule |
| --- | --- | --- |
| S | focused critique or one small artifact update | draft/check -> repair/confirm | stop if more than one new evidence expansion is needed |
| M | one synthesis pass plus one validation/repair cycle | define/draft -> interrogate -> compact repair -> confirm | stop after repair if major unresolved gaps remain |
| L | multi-source synthesis, research, or tournament | context/define -> interrogate -> optimize -> repair -> confirm | stop after checkpoint if the model changes materially |
| XL | cross-artifact synthesis and final verification | audit -> interrogate -> repair -> final audit | stop rather than compressing unresolved decisions into a false pass |

## Task-Local Refinement Patterns

Use the smallest pattern that satisfies the task:

| Pattern | Used When | Passes |
| --- | --- | --- |
| `define-check-repair` | definitions, glossary, roadmap, article sections | define/draft -> interrogation -> compact repair -> closeout |
| `research-sift-apply` | external research | search -> source table -> fit/misfit interrogation -> influence update |
| `tournament-recompose` | conceptual model convergence | lane drafts -> lane interrogation -> optimizer selection -> recomposition check |
| `design-validate-repair` | architecture and lifecycle design | design draft -> interrogation -> concept repair -> final design update |
| `audit-repair-verdict` | final verification | audit -> interrogation -> repair if allowed -> pass/flag/block |

## CAOL-001: Context Pack

| Field | Value |
| --- | --- |
| Status | done |
| Arcanum route | `context-builder --handoff codex-goal` style pass |
| Budget | L |
| Budget rationale | Broad local evidence across Arcanum, CyberAlchemy, DomainSpec, and AEO. |
| Inputs | scaffold files, source map targets, local source evidence |
| Outputs | `CONTEXT-HANDOFF.md`, `SOURCE-MAP.md`, `context-pack.json`, `index.json` |
| Gate | strict coverage pass or explicit deferral per obligation |
| Stop condition | block if local evidence cannot cover CAOL-002 through CAOL-010 handoff needs |
| Refinement cycle | initial evidence selection -> coverage interrogation -> source-map repair -> JSON/index verification |

## CAOL-002: Definitions

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `invoke define` with glossary and definition governance |
| Budget | M |
| Budget rationale | One definition synthesis pass from the context pack; no architecture expansion yet. |
| Inputs | `CONTEXT-HANDOFF.md`, `context-pack.json`, existing `ONTOLOGY-ARCHITECTURE.md`, source selectors for O1/O2/O8 |
| Outputs | `DEFINITIONS-GLOSSARY.md`, definition updates or notes in `ONTOLOGY-ARCHITECTURE.md`, open questions in `INTERROGATION-VERDICT.md` |
| Gate | every required term has definition, evidence source, status, confidence posture, and unresolved questions |
| Stop condition | stop if axiom/constitution semantics cannot be represented without user decision |
| Refinement cycle | define draft -> interrogation of definitions -> Distill compact repair -> final glossary pass |

Strategy:

1. Extract definitions only from selected local sources.
2. Produce a first glossary draft with evidence selectors and status labels.
3. Interrogate the draft for false authority, missing distinctions, and confidence collapse.
4. Run a compact Distill repair on the smallest failing distinction, especially axiom/constitution/premise/signal.
5. Produce a final task-local glossary pass that later architecture can cite directly.

## CAOL-003: Interrogate Definitions

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `interrogation` pass over define output |
| Budget | S |
| Budget rationale | Focused critique of CAOL-002, not new research. |
| Inputs | `DEFINITIONS-GLOSSARY.md`, `CONTEXT-HANDOFF.md`, `context-pack.json` |
| Outputs | updated `INTERROGATION-VERDICT.md`, decision questions, repaired task statuses |
| Gate | definitions pass, flag, or block with exact reasons |
| Stop condition | stop if a blocker decision is needed on axiom/constitution semantics |
| Refinement cycle | critique -> decision-question reduction -> compact repair recommendation -> final verdict |

Strategy:

1. Check false authority.
2. Check candidate/promoted separation.
3. Check signal/evidence/truth separation.
4. Check confidence split.
5. Reduce findings to the smallest set of repairable issues.
6. Run a compact repair recommendation pass for non-blocking issues.
7. Return the fewest high-leverage decisions needed.

## CAOL-004: Bounded Online Research

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | bounded research companion to `invoke design` |
| Budget | L |
| Budget rationale | External research can expand quickly; cap at 8 sources and depth 2. |
| Inputs | `external-research-appendix.md`, context pack gaps, CAOL-002/003 questions |
| Outputs | completed `external-research-appendix.md`, influence notes in `index.json` |
| Gate | each source has type, relevance, extracted idea, fit/misfit, influence |
| Stop condition | stop when sources repeat patterns or a source materially changes the model and needs user review |
| Refinement cycle | search/source table -> fit/misfit interrogation -> influence synthesis -> final bounded appendix |

Strategy:

1. Search only for missing vocabulary and design pressure.
2. Build the source table before synthesis.
3. Interrogate each candidate source for fit, misfit, and risk of overriding local evidence.
4. Run a lightweight concept fit check: does the source change ontology structure, promotion gates, signal semantics, or only vocabulary?
5. Mark influence as `evidence`, `analogy`, `vocabulary`, or `rejected`.

## CAOL-005: Concept Tournament

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `distill` Tournament mode, role-simulated if subagents are unavailable |
| Budget | L |
| Budget rationale | Four lanes plus recomposition; bounded to one tournament and one selection. |
| Inputs | context pack, CAOL-002 definitions, CAOL-003 interrogation, CAOL-004 research |
| Outputs | `CONCEPT-TOURNAMENT.md`, selected model notes for architecture/lifecycle |
| Gate | smallest coherent model selected and recomposition proof stated |
| Stop condition | stop if lanes disagree twice without new evidence |
| Refinement cycle | lane draft -> lane interrogation -> tournament selection -> recomposition repair -> final model note |

Lanes:

1. Ontology model lane.
2. Promotion lifecycle lane.
3. Observability/signal lane.
4. DomainSpec/software lifecycle lane.

Strategy:

1. Keep each lane independent at first.
2. Draft each lane's smallest coherent unit, invariant, gate, and risk.
3. Interrogate each lane for missing distinctions and overreach.
4. Run tournament selection across the repaired lanes.
5. Recompose only after each lane names its invariants, gates, and risks.
6. Validate that the selected model can drive CAOL-006 without reopening source discovery.

## CAOL-006: Architecture And Lifecycle

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `invoke design` |
| Budget | L |
| Budget rationale | Main architecture synthesis from already prepared evidence and tournament output. |
| Inputs | context pack, definitions, research appendix, concept tournament |
| Outputs | updated `ONTOLOGY-ARCHITECTURE.md`, updated `PROMOTION-LIFECYCLE.md` |
| Gate | architecture includes branches, nodes, edges, authority, confidence, promotion states, evidence rules, adapters, use cases |
| Stop condition | stop if architecture requires canonical ontology mutation before user acceptance |
| Refinement cycle | design draft -> interrogation -> Distill repair -> final architecture/lifecycle pass |

Strategy:

1. Design from the selected model, not from fresh broad research.
2. Produce a first architecture/lifecycle draft.
3. Interrogate the draft for false authority, vague gates, missing evidence types, lifecycle gaps, and unclear axiom/constitution semantics.
4. Run a Distill repair only on flagged layers.
5. Tie every major architecture claim to source selectors or research influence.
6. Keep operational use behind bridge validation and promotion gates.

## CAOL-007: Repair

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `interrogation` plus `distill` Validate/Compact repair |
| Budget | M |
| Budget rationale | One critique pass and one repair pass. |
| Inputs | CAOL-006 architecture/lifecycle, prior interrogation findings |
| Outputs | repaired architecture/lifecycle sections, updated `INTERROGATION-VERDICT.md` |
| Gate | false authority, vague gates, signal truth claims, and confidence collapse are absent or explicitly flagged |
| Stop condition | stop if a blocker contradiction remains after one repair pass |
| Refinement cycle | interrogation -> compact repair -> re-interrogation -> final flag/pass/block |

Strategy:

1. Do not reopen the whole model.
2. Interrogate only the CAOL-006 outputs and prior findings.
3. Repair only flagged conceptual issues.
4. Re-interrogate the repaired sections once.
5. Preserve unresolved decisions as explicit review items.

## CAOL-008: Roadmap And First Slice

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `invoke plan` plus `implementation-layering` |
| Budget | M |
| Budget rationale | Plan synthesis, not implementation. |
| Inputs | accepted candidate architecture, lifecycle model, repair verdict |
| Outputs | updated `ROADMAP.md`, optional `FIRST-WORKING-SLICE.md` |
| Gate | roadmap has phases, next work, validation strategy, and no canonical mutation without acceptance |
| Stop condition | stop if first slice cannot be bounded without changing canonical ontology/runtime files |
| Refinement cycle | plan draft -> implementation-layer interrogation -> layer repair -> final roadmap/slice pass |

Strategy:

1. Draft roadmap and first slice from accepted candidate architecture.
2. Interrogate the plan for premature implementation, missing validation, and canonical mutation risk.
3. Run implementation-layering repair from proof-first slice to hardening.
4. Name exact next artifacts and validation checks.
5. Keep implementation tasks separate from architecture acceptance.

## CAOL-009: Article

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | `invoke design` article synthesis / publication pass |
| Budget | M |
| Budget rationale | One public-facing synthesis from validated internal model. |
| Inputs | final candidate architecture, lifecycle, roadmap, source map, research appendix |
| Outputs | updated `SUBSTACK-ARTICLE.md`, updated package README summary |
| Gate | article is accessible, accurate, and preserves candidate/promoted caveats |
| Stop condition | stop if article would need to hide unresolved model decisions |
| Refinement cycle | article draft -> accuracy/interrogation pass -> conceptual clarity repair -> final article pass |

Strategy:

1. Draft from the validated internal model.
2. Interrogate for unsupported claims, missing caveats, and inaccessible jargon.
3. Repair conceptual clarity without weakening evidence boundaries.
4. Explain deeply but accessibly.
5. Preserve epistemic humility: signals are not truth; candidates are not promoted knowledge.

## CAOL-010: Final Verification

| Field | Value |
| --- | --- |
| Status | pending |
| Arcanum route | final `interrogation` plus completion audit |
| Budget | M |
| Budget rationale | Requirement-by-requirement verification across package artifacts. |
| Inputs | every package artifact |
| Outputs | final `INTERROGATION-VERDICT.md`, updated `index.json`, closeout summary |
| Gate | pass, flag, or block against [EXECUTION-STRATEGY.md](EXECUTION-STRATEGY.md) completion criteria |
| Stop condition | block if any required artifact is missing, weakly evidenced, or falsely promoted |
| Refinement cycle | completion audit -> final interrogation -> allowed repair/checkpoint -> final verdict |

Strategy:

1. Derive requirements from the original goal and package strategy.
2. Verify each requirement against current files.
3. Interrogate the verification for weak evidence, missing artifacts, and false pass risk.
4. Repair only package metadata or verdict wording if the artifacts are already sufficient.
5. Mark `pass` only when every required output is present and source-grounded.
6. Otherwise mark `flag` or `block` with exact remaining work.
