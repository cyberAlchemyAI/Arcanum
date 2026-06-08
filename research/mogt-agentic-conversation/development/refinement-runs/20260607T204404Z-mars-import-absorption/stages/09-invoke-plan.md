---
stage: 09-invoke-plan
status: pass
---

# Invoke Plan: MARS Import and Arcanum Absorption

## Phase 1: MOGT-Local Import

Write scope:

- `research/mogt-agentic-conversation/experiments/schema/`
- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/development/WORK-PACK.md`

Actions:

1. Create `experiments/schema/mogt-run.schema.json` using MARS schema conventions but MOGT-specific fields.
2. Create a validator for append-only JSONL rows.
3. Add one passing and one failing synthetic fixture under `development/fixtures/`.
4. Record validation commands and outputs.

## Phase 2: MOGT Runner Pack

Write scope:

- `research/mogt-agentic-conversation/tools/`
- `research/mogt-agentic-conversation/development/fixtures/`
- `research/mogt-agentic-conversation/experiments/*/results/`

Actions:

1. Define policy-regime/scenario fixture shape for heuristic, weighted-sum, Pareto-guided, and bargaining-guided regimes.
2. Implement objective-vector validation and Pareto/frontier metrics.
3. Add reviewer-rubric ingestion.
4. Generate dry-run result summaries without upgrading evidence status.

## Phase 3: Arcanum Absorption Proposal

Write scope:

- proposal/handoff only until separately approved

Candidates:

1. Research experiment bundle contract for `experiment-harness` or a new research-harness sigil.
2. Methodology profile governance as a reusable transmutation.
3. Research graph and paper derivation as paper-design support.
4. Telemetry signal schema as observability extension.
5. Multi-source context pattern as context-builder extension.

## Stop Conditions

- BLOCK if MOGT schema cannot be derived without changing live experiment protocols.
- BLOCK if copied MARS assets would introduce MARS-specific project evidence into MOGT.
- BLOCK if Arcanum absorption requires canonical mutation before MOGT-local proof exists.
