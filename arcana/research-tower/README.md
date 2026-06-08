# Research Tower

Research Tower is a draft Arcana sigil for turning a paper, source corpus, or
research question into a reproducible local learning tower. It generalizes the
AutoBayes research run into a standard contract: source-first claims, notation
translation, local glossary, governed definitions, distilled knowledge,
related-work crosswalks, bridge decisions, residue, validation, and final
operator-facing learning packs.

Status: draft candidate, not promoted.

## Problem Solved

One strong research run can be hard to repeat. The Research Tower sigil makes
the research method reusable by requiring every learning artifact to carry:

- source evidence or an explicit inference label;
- local-vs-canonical promotion status;
- notation explanations when symbols matter;
- reusable definitions and glossary entries;
- distilled operator knowledge;
- unresolved residue and follow-up routes;
- validation evidence that the tower can be trusted by a later agent.

## When To Use

Use this sigil when the target is more than a quick summary:

- a paper needs to become durable Arcanum-facing understanding;
- related papers must be mapped without losing source boundaries;
- notation, definitions, and examples must become teachable;
- a future sigil, spell, runtime, or ontology decision needs a research basis;
- subagents are useful, but their outputs must be closed and reconciled.

## When Not To Use

Do not use this sigil for:

- a one-paragraph paper summary;
- canonical term promotion without a separate governance decision;
- implementation work that already has an approved task-session route;
- unbounded literature review with no artifact contract;
- replacing the source paper with an Arcanum analogy.

## Standard Artifact Set

A standard research tower should produce or update:

- `README.md` - local orientation and artifact index;
- `TOWER.md` - layer model, gates, and closure state;
- `levels/L0-corpus.md` - source inventory and evidence boundary;
- `levels/L1-residue-map.md` - open questions and research lanes;
- `levels/L2-closure-plan.md` - closure tasks and validation route;
- `NOTATION.md` - local notation bridge to shared notation terms;
- `GLOSSARY.md` - local glossary with promotion status;
- `DEFINITIONS.md` - governed definitions with intuition and misuse warnings;
- `DISTILLED-KNOWLEDGE.md` - compact operator knowledge;
- `tracks/paper-claim-ledger.md` - claim/source/inference ledger;
- `tracks/related-framework-crosswalk.md` - related paper/framework map;
- `tracks/*-definition-card.md` - reusable cards for important concepts;
- `tracks/*-worked-example.md` - symbolic or concrete examples when needed;
- `tracks/*-bridge-decision.md` - borrow/block/analogy-only/promotion decision;
- `residue/open-residue.md` - remaining questions and future tasks;
- `FINAL-LEARNING-PACK.md` - final source-backed operator pack;
- `work-pack/*-RESULT.md` - execution evidence when routed by task-session.

## Extraction Source

This candidate was extracted from the AutoBayes research tower. The AutoBayes
run proved the useful artifact spine: claim ledger, notation bridge, glossary,
definitions, related-framework crosswalk, definition cards, worked example,
implementation residue note, bridge decision, final learning pack, and explicit
local-only promotion boundary.

## Lifecycle

Research Tower is an Arcana candidate because it governs a multi-artifact,
multi-source learning workflow and coordinates other capabilities. It should
compose with:

- `refine` for shaping the research question and candidate route;
- `dispatch-spec` for route and subagent strategy design;
- `context-builder` for compact source/evidence packs;
- `feature-glossary` for local glossary extraction;
- `definitions-governance` for definition authority and drift checks;
- `distill` for compact concept units and operator knowledge;
- `task-session` for bounded execution;
- `codex-goal-profile` for long-running native Codex research goals;
- `experiment-harness` for replay validation before promotion.

## Evidence Execution Handoff

Research Tower should hand off instead of expanding when the next blocker is
empirical evidence production rather than durable source understanding.

Route to `research-evidence-harness` when the tower or target project needs:

- append-only run schemas;
- JSONL fixture validation;
- objective-vector or metric calculators;
- reviewer-rubric ingestion;
- result summaries;
- claim-adjudication readiness from measured runs.

This preserves the tower's local-learning authority while letting a dedicated
evidence harness own data mechanics and publication-safe evidence boundaries.

## Promotion Rule

This sigil may create local research knowledge. It may recommend promotion
candidates, but it must not promote source terms into Inventory, Ontology,
canonical glossary, sigils, spells, or runtime contracts without a later
governed decision.
