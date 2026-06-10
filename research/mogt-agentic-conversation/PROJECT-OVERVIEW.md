# Multi-Objective Game Theory for Agentic Conversation Decisions

> Scoping + status artifact. Plain language first, then the formal scope tables.
> Every status claim points to its source file. ⚠️ marks things that are
> **designed but not yet tested**. New to the project? Read [README.md](README.md)
> first — it explains MOGT from scratch with a worked example.

## Summary

**In one sentence:** MOGT is a *decision layer* you put right before an agent picks its
next conversation move — it scores each available action (answer, clarify, escalate,
defer, …) across quality, cost, latency, safety, and escalation risk, then selects one
using a named *policy regime* and records why. Source:
[module-formulae/formal-runtime-definition.md](module-formulae/formal-runtime-definition.md).

**The question:** can making those objectives explicit — instead of relying on an implicit
"answer if you can, escalate if risky" heuristic — produce decisions that are more
traceable, higher quality under competing goals, and calmer under disagreement, *without*
unacceptable overhead? The project exists to decide whether an explicit
multi-objective / game-theoretic decision layer is worth adding to an agent orchestrator.

⚠️ **Reality check, up front:** this is at the **design + dry-run** stage. The model and a
synthetic-fixture test harness exist, but **no live experiment has run** — all four claims
are rated *insufficient evidence* and all four experiments are *not started*. Nothing about
MOGT is proven yet. Source: [results/MOGT-EVIDENCE-STATUS.md](results/MOGT-EVIDENCE-STATUS.md),
[experiments/EXPERIMENTS.md](experiments/EXPERIMENTS.md). See §"Designed vs proven" below.

## Discovery Mode

- Mode: greenfield
- Research state: scoped
- Interview date: 2026-04-27
- Sponsor / decision owner: research operator

## Research Problem

- Core question: Can multi-objective game theory improve traceability, decision quality, disagreement handling, and operational feasibility in agentic conversation decision processes?
- Decision pressure: whether to invest in a game-theoretic decision layer for orchestrated agent conversations
- Unit of analysis: conversation decision episode
- Why this matters now: agentic systems increasingly balance quality, speed, cost, and safety under multi-role coordination, but most orchestration policies still rely on ad hoc heuristics
- Non-goals: proving optimality for all multi-agent systems, designing a production market mechanism, or replacing human governance entirely

## Current Evidence Baseline

| Area              | State   | Evidence Type | Notes                                                                                                     |
| ----------------- | ------- | ------------- | --------------------------------------------------------------------------------------------------------- |
| Prior claims      | draft   | observed      | Claims are seeded in this project but not yet empirically tested.                                         |
| Prior protocols   | draft   | observed      | Four experiment bundles are defined at draft level.                                                       |
| Prior data        | none    | observed      | No run data exists yet.                                                                                   |
| Decision criteria | partial | stated        | The user request defines the high-level goal, but the target deployment envelope still needs calibration. |

Evidence type:

- `observed` = seen in repository or artifacts
- `stated` = given by operator
- `hypothesized` = inferred but not yet validated

## Designed vs Proven (completeness snapshot, 2026-06-10)

The project enforces one boundary: synthetic fixtures prove the *machinery runs*, never
that *MOGT works*. Source:
[module-formulae/flows-policies.md](module-formulae/flows-policies.md) (EvidenceStatusBoundaryPolicy).

### Weighted completeness

- Structural completeness (40% weight): ~100% — required contract and governance artifacts present.
- Empirical completeness (40% weight): **0%** — no sources-to-results evidence chain has run.
- Publication completeness (20% weight): ~10% — paper stub + pilot contracts only.
- Overall weighted: ~42%.

### Artifact lane status

| Lane | Expected outcome | Current state | Status |
|---|---|---|---|
| Project contract | PROJECT, claims, dependencies, registry, telemetry schema | Present | complete |
| Governance definitions | canonical definitions, hypotheses, protocol checklist, experiment index, draft bundles | Present but greenfield and unvalidated | in progress |
| Execution evidence | experiment specs, data files, analysis outputs | Draft bundles + synthetic-fixture harness exist; ⚠️ no live data or results | missing |
| Foundations, source, inventory | foundations baseline, source selection, library + raw provenance | foundations present; some authorities still await raw input | in progress |
| Claim adjudication | claim-level evidence status updates | Scaffold exists; ⚠️ all four claims insufficient | in progress |
| Publication | paper updates and retrospective outputs | Paper stub + pilot contracts; no empirical synthesis | in progress |
| Exports | reusable published artifacts for dependents | Scaffold only; no published outputs | missing |

### What is missing right now

1. Build the first benchmark conversation corpus and decision-review rubric for E1 and E2.
2. Run a gate walkthrough and the first dry execution for the highest-priority experiments.
3. Produce the first append-only JSONL run files and integrity reports under the bundles.
4. Upgrade or reject the claims based on measured results rather than design-time reasoning.

## Stakeholders

| Stakeholder             | Decision                                                                                    | Risk If Wrong                                                            | Evidence Type |
| ----------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------- |
| research operator       | whether to fund deeper protocol design and live experiments                                 | wasted research effort or premature abandonment of a viable intervention | stated        |
| orchestration architect | whether to add explicit objective and negotiation layers to conversation routing            | higher complexity without measurable gains                               | hypothesized  |
| evaluation owner        | whether benchmark conversations need multi-objective scoring instead of single-score review | evaluation blind spots hide real tradeoffs                               | hypothesized  |

## Scope Boundaries

| Boundary        | In Scope                                                                            | Out Of Scope                                                | Status |
| --------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------ |
| decision layer  | turn selection, escalation, arbitration, and negotiation within agent conversations | full autonomous product strategy or organization design     | draft  |
| objective model | quality, latency, cost, safety, escalation risk, and explanation quality            | arbitrary financial utility functions for unrelated domains | draft  |
| evidence mode   | replay, simulation, benchmark scenarios, and structured reviewer adjudication       | production rollout claims without controlled evidence       | draft  |

## Variables And Confounders

| Type                 | Item                        | Why It Matters                                                                     | Status    |
| -------------------- | --------------------------- | ---------------------------------------------------------------------------------- | --------- |
| independent variable | decision policy regime      | the central intervention is the policy used to arbitrate between candidate actions | candidate |
| independent variable | number of active objectives | higher-dimensional objective sets may change both performance and overhead         | candidate |
| dependent variable   | decision quality            | determines whether the policy actually improves outcomes                           | candidate |
| dependent variable   | convergence rate            | shows whether conversations settle decisions faster or more reliably               | candidate |
| confounder           | model capability            | stronger models may outperform weaker ones regardless of policy design             | candidate |
| confounder           | scenario difficulty         | harder decisions may inflate disagreement and regret independent of policy choice  | candidate |

## Success Criteria For Scoping

| Criterion                       | Why It Matters                                               | Current State |
| ------------------------------- | ------------------------------------------------------------ | ------------- |
| clear decision owner            | experiments should change a real architecture decision       | partial       |
| falsifiable claim set           | prevents research from collapsing into generic brainstorming | complete      |
| runnable first-wave experiments | allows transition from scope to protocol design              | complete      |
| source normalization plan       | required for G2 source governance                            | partial       |

## Open Questions

1. Which objective set should be treated as the default baseline for early experiments: quality, cost, latency, and safety, or a narrower subset?
2. Should the first evaluation wave use simulated agent role conflicts only, or also human-reviewed historical conversations?

## Recommended Next Artifacts

1. `definitions/INITIAL-DEFINITIONS.md`
2. `claims/HYPOTHESES.md`
3. `experiments/EXPERIMENT-CANDIDATES.md`
