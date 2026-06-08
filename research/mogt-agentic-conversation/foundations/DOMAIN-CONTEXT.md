# MOGT Domain Context

Purpose: establish the project-level problem setting and agentic-conversation prior-art context before protocol design, execution, or claim updates.

This artifact is not an experiment protocol. It is the baseline explanation of the decision setting MOGT is studying, the kinds of conversational policies that are in scope, and the prior-art assumptions that should shape later experiments.

## Why This Artifact Exists

MOGT is not testing abstract multi-objective optimization in isolation.

It is testing whether multi-objective and game-theoretic ideas improve how agentic systems make decisions through conversation. That means protocol design has to start from a stable understanding of:

- what counts as a conversational decision episode
- which conversational policy regimes are being compared
- which prior-art papers define the relevant orchestration, debate, negotiation, and evaluation context
- which failure modes matter operationally in multi-agent or role-based conversational settings

Without this baseline, experiments drift into generic optimization or generic LLM-agent evaluation without staying anchored to the actual research question.

## Research Setting

- Primary question: can explicit multi-objective and game-theoretic decision policies outperform implicit heuristic arbitration inside agentic conversations?
- Unit of analysis: bounded conversational decision episodes rather than full end-to-end products or organizations.
- Decision surface: per-turn action choice under competing objectives such as quality, cost, latency, risk, and escalation pressure.
- Canonical definitions: `MOGT-D1` through `MOGT-D9` and `MOGT-M1` through `MOGT-M4` in `definitions/DEFINITIONS.md`.

## What Counts As An Agentic Conversation Decision

| Element              | MOGT interpretation                                                                   | Why it matters                                                        |
| -------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| Decision episode     | a bounded sequence of turns ending in an action choice, escalation, or stop condition | keeps experiments focused on comparable decision units                |
| Conversational role  | a participant with a recognizable objective pressure or decision responsibility       | allows contested preferences and explicit disagreement handling       |
| Candidate action set | the finite menu of actions available at a decision point                              | prevents policy evaluation from drifting into unconstrained prompting |
| Policy regime        | the explicit rule used to choose, filter, or negotiate among actions                  | makes experiments compare regimes rather than prompts                 |
| Outcome              | both the final action and the trace of how it was selected                            | supports quality, traceability, and overhead evaluation together      |

## Role And Conflict Structure

MOGT assumes that conversational decision quality emerges from role interaction, not just from a single scalar score.

| Role archetype           | Typical pressure                              | Common conflict                                         |
| ------------------------ | --------------------------------------------- | ------------------------------------------------------- |
| Orchestrator             | forward progress and bounded cost             | may over-prioritize speed over quality                  |
| Specialist agent         | local excellence on a subproblem              | may prefer deeper analysis and more turns               |
| Risk or governance voice | constraint preservation and escalation safety | may block actions that optimize short-term utility      |
| Reviewer or evaluator    | inspectability and acceptability              | may disagree with a policy that is efficient but opaque |

These role tensions are important because MOGT is not merely testing whether one action scores better on paper. It is testing whether a policy remains legible, negotiable, and operational when multiple conversational perspectives interact.

## Policy Regimes In Scope

| Regime                     | Description                                                                    | Why it is in scope                                            | Main experiments |
| -------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------- | ---------------- |
| Heuristic baseline         | implicit or loosely structured arbitration using operator or prompt heuristics | realistic current baseline for many agent systems             | E1, E2, E4       |
| Weighted-sum baseline      | explicit scalarization of multiple objectives into one score                   | practical comparison arm for multi-objective reasoning        | E2, E4           |
| Pareto-guided regime       | filters or prioritizes non-dominated actions before final selection            | direct test of multi-objective advantage beyond scalarization | E2, E4           |
| Negotiation-enabled regime | uses bounded dialogue, concession, or bargaining structure among roles         | direct test of disagreement handling and convergence          | E3, E4           |

## Prior-Art Synthesis

### Orchestration And Conversational Coordination

| Source                                  | What it contributes                                                          | How MOGT should use it                                                            | Caution                                                                  |
| --------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `PAPER-WU-2024-AUTOGEN`                 | role-based multi-agent conversation and explicit handoff patterns            | define how role interaction and intermediate traces can be modeled in experiments | framework and demo authority, not a threshold-setting methodology source |
| `PAPER-GUO-2024-LLM-MULTIAGENTS-SURVEY` | landscape of communication, coordination, failure modes, and open challenges | define the broader design space and external-validity boundaries for MOGT         | survey framing should not substitute for direct empirical authority      |

### Agent Evaluation And Benchmark Framing

| Source                      | What it contributes                                          | How MOGT should use it                                                        | Caution                                                                            |
| --------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `PAPER-LIU-2024-AGENTBENCH` | benchmark-oriented evaluation discipline for agentic systems | guide how MOGT frames evaluation tasks, comparisons, and controlled baselines | stronger on evaluation discipline than on conversational multi-agent policy itself |
| `PAPER-WALKER-1997`         | task-quality plus cost interpretation in dialogue evaluation | support acceptance-style scoring and quality-versus-overhead interpretation   | spoken-dialogue setting must be adapted carefully to LLM-agent conversations       |

### Debate, Negotiation, And Conflict Handling

| Source                             | What it contributes                                                | How MOGT should use it                                                     | Caution                                                                                      |
| ---------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `PAPER-DU-2023-MULTIAGENT-DEBATE`  | critique and revision loops through structured dialogue            | inspire bounded debate mechanisms and disagreement-surfacing telemetry     | debate is not the same as full negotiation                                                   |
| `PAPER-LEWIS-2017-DEAL-OR-NO-DEAL` | negotiation dialogue, agreement structure, and convergence metrics | guide E3 conflict-resolution framing and bounded-turn convergence measures | pre-LLM setting; use for task structure and metrics rather than modern orchestration details |

## Failure Modes MOGT Must Address

1. Decision opacity: agents choose actions but reviewers cannot reconstruct the active objectives or tradeoffs.
2. Scalarization blindness: a weighted-sum policy hides dominated alternatives behind a single score.
3. Conversational churn: disagreement creates cycling, redundant debate, or late escalation instead of resolution.
4. Evaluation drift: agentic-conversation tasks are judged with generic LLM criteria rather than task-specific decision quality and traceability criteria.
5. Operational overreach: more reasoning steps or more agents produce theoretical gains that do not survive cost, latency, or reviewer-burden constraints.

## Consequences For MOGT Experiment Design

| Experiment | Domain-context implication                                                                                                        |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| E1         | compare not just final choices but the inspectability of decision traces under realistic conversational roles                     |
| E2         | include explicit candidate action sets and objective annotations so Pareto versus weighted-sum differences are visible            |
| E3         | define contested scenarios with role-specific utility asymmetries instead of generic disagreement prompts                         |
| E4         | measure operational feasibility on the same family of conversational tasks used in E1-E3 so overhead results remain interpretable |

## Non-Goals

- proving that every multi-agent conversational framework benefits from game theory
- evaluating unrestricted open-ended chat performance
- replacing empirical protocol design with framework demos or survey claims
- treating debate, orchestration, and negotiation as interchangeable mechanisms

## Consultation Rule

Before any experiment protocol is hardened, check this artifact for:

1. the exact conversational setting being studied
2. the policy regimes that are in or out of scope
3. the prior-art papers that define orchestration, evaluation, debate, and negotiation assumptions
4. the failure modes the experiment is supposed to observe or mitigate
