---
name: MOGT Next Publishable State Refine Seed
run_id: 20260608T052100Z-next-publishable-state
target: research/mogt-agentic-conversation
preset: standard
research_mode: research-if-gap-appears
status: strategy-proposal
---

# Refine Seed Proposal

## Operator Intent

Refine the next steps after completing the MOGT harness fixture-validation
chain. Show the current state, the desired publishable-paper state, and the
governed route from here to there.

## Current State

The project is fixture-validation-ready, not publication-ready.

Confirmed local evidence:

- `development/WORK-PACK.md` marks `SWU-MOGT-HARNESS-001` through `005` complete.
- `development/fixture-validation-report.md` reports PASS for fixture-only S4
  dry-run readiness.
- `development/fixtures/mogt-runtime-decision-receipts.jsonl` validates with
  four synthetic rows covering heuristic, weighted-sum, Pareto-guided, and
  bargaining-guided regimes.
- `tools/calculate-pareto-frontier.py` computes frontier/dominance metrics over
  an E2-like fixture.
- `tools/generate-result-summary.py` produces fixture-only summaries for E1,
  E2, and E4.
- `module-formulae/formal-runtime-definition.md` and
  `module-formulae/runtime-decision-receipt.md` define the formal/runtime MOGT
  decision surface.

Current hard boundary:

- No live experiments have been run.
- Synthetic fixtures cannot update `results/MOGT-EVIDENCE-STATUS.md`.
- Paper result sections and publication claims remain unsupported by live or
  claim-bearing evidence.

## Desired State

The desired state is a paper-ready MOGT research package:

- prior-art and novelty ledger is current enough for submission framing;
- live or approved claim-bearing experiment protocol has run;
- E1, E2, E3, and E4 have result summaries with evidence status decisions;
- reviewer/rubric scoring is calibrated and recorded;
- `results/MOGT-EVIDENCE-STATUS.md` reflects only supported evidence;
- paper claims, method, limitations, and result sections match the evidence;
- reusable tool lessons are separated into development handoffs for Whisper,
  Dispatch Spec, and Research Evidence Harness without mutating canonical
  contracts prematurely.

## Gap

The next gap is not schema or fixture readiness. The next gap is claim-bearing
research execution and paper synthesis.

The project needs a governed route that decides whether to:

1. run S4 as a dry-run-only rehearsal first;
2. calibrate reviewer rubrics and live protocol gates;
3. request approval for live experiments;
4. update evidence status and paper sections only after approved evidence exists.

## Write Scope For This Refine Run

- `research/mogt-agentic-conversation/development/refinement-runs/20260608T052100Z-next-publishable-state/`

This refinement proposal must not mutate experiment results, paper claims,
canonical Arcanum capability contracts, or MOGT evidence status.

## Done Criteria

- Current state and desired state are explicit.
- Next-route options are compared.
- Dispatch route validates.
- Subagent strategy is previewed before any delegated work.
- Runtime-backed stages remain unexecuted until operator confirmation.

## Research Decision

Research mode: `research-if-gap-appears`.

Local evidence is sufficient for this strategy proposal. External research may
be needed later for novelty/current-prior-art refresh, but it should be
requested explicitly before that lane runs.
