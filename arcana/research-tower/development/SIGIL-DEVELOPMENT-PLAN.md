# Research Tower Sigil Development Plan

Status: draft candidate

Origin: extracted from the AutoBayes research tower closure.

## Goal

Make the AutoBayes-style research workflow reproducible for future papers and
research corpora while preserving source boundaries, notation literacy, local
definitions, distilled operator knowledge, subagent closeout, and promotion
guardrails.

## Current Candidate

The first draft contains:

- `README.md` for human-facing orientation;
- `SKILL.md` for the sigil contract;
- templates for claim ledgers, notation bridges, glossary entries, definition
  cards, related-framework crosswalks, subagent closeout, tower readmes, and
  final learning packs.

## Validation Regimes

1. AutoBayes replay:
   - Input: `research/autobayes/`;
   - Expected: the sigil recognizes the existing tower and reports closure
     instead of duplicating artifacts;
   - Required proof: source record, notation bridge, glossary, definitions,
     distilled knowledge, bridge decisions, final pack, and residue all found.
2. Small-paper smoke:
   - Input: one short paper or source note;
   - Expected: compact mode emits claim ledger, glossary, distill, residue, and
     final pack without overbuilding related-work artifacts.
3. Notation-heavy paper:
   - Input: a source with formal notation;
   - Expected: notation bridge appears before definitions and final pack.
   - Current evidence: `research/monoidal-categories-multicategories/`
     and `development/test-run-monoidal-categories-multicategories.md`
     passed a standard notation-heavy run.
4. Subagent hardening:
   - Input: full/deep mode with delegated lanes;
   - Expected: every lane has a closeout ledger row before closure.

## Work Units

### RT-001 Scaffold Candidate

Create the draft sigil package and templates.

Completion evidence:

- `arcana/research-tower/README.md`;
- `arcana/research-tower/SKILL.md`;
- `arcana/research-tower/templates/*`;
- structure validation passes.

### RT-002 AutoBayes Replay Report

Run the candidate against `research/autobayes/` as a recognition/replay test.

Completion evidence:

- report under `arcana/research-tower/development/replay-autobayes.md`;
- no duplicated AutoBayes artifacts;
- missing-contract gaps identified.

### RT-003 Experiment Harness

Initialize an experiment harness with low, medium, and complex prompts.

Completion evidence:

- local experiment prompts;
- validation report;
- blocked state if model-backed execution cannot run.

### RT-004 Observability Hook

Define usage telemetry for meaningful executions.

Completion evidence:

- telemetry schema or sigil-local hook reference;
- reflection threshold;
- gap categories.

### RT-005 Promotion Decision

Decide whether this moves from draft candidate to registered reusable sigil.

Completion evidence:

- experiment evidence reviewed;
- registry update only if approved;
- promotion risks and non-goals documented.

## Hardening Checks

- Existing artifacts are detected before creation.
- Source claims use source-kind labels.
- Notation bridge is required when symbols carry reasoning load.
- Local glossary and governed definitions do not become canonical by accident.
- Subagents cannot remain open at closure.
- Related work is bounded by named residue.
- Final pack includes borrow, analogy-only, and block sections.
- Open residue has owners or next routes.
