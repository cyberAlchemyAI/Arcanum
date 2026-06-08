# MOGT Canonical Definitions

Purpose: authoritative source of project definitions for research on multi-objective game theory in agentic conversation decisions.

This document is the normative definition contract for the project. The paper is a condensed synthesis artifact, not the definition authority.

## Authority and Precedence

1. `definitions/DEFINITIONS.md` is the canonical definition source.
2. `definitions/DEFINITIONS-INDEX.md` is the lookup and traceability layer.
3. `papers/mogt-agentic-conversation-paper.md` is a narrative synthesis of definitions plus empirical evidence.

## Definition Families

- `MOGT-D*`: core domain and formal constructs
- `MOGT-M*`: measurement and research-execution definitions

Interpretation rule: each definition may include a short `Intuition` note as non-normative guidance.

## Core Definitions

### MOGT-D1: Agentic Conversation Decision Process

An agentic conversation decision process is a bounded sequence of conversational turns in which an orchestrator or participating agents choose the next action under explicit objectives, constraints, and escalation rules.

Intuition: this project studies the decision policy inside the conversation loop, not the entire product or organization around it.

### MOGT-D2: Decision State

At turn $t$, the decision state is:

$$
s_t = (c_t, A_t, O_t, K_t)
$$

where:

- $c_t$ is the conversation context available at turn $t$
- $A_t$ is the candidate action set
- $O_t$ is the active objective set
- $K_t$ is the active constraint set

Intuition: every decision episode can be described by what is known, what can be done, what matters, and what is forbidden.

### MOGT-D3: Objective Vector

For candidate action $a \in A_t$, the objective vector is:

$$
v(a, s_t) = (q(a), -cost(a), -latency(a), -risk(a), -esc(a))
$$

where higher values are preferred and omitted dimensions are permitted when a protocol scopes a smaller set.

Intuition: decisions are judged against multiple objectives simultaneously, not compressed into one scalar by default.

### MOGT-D4: Candidate Action Set

The candidate action set $A_t$ is the finite set of actions available at decision state $s_t$, such as answer, defer, ask clarifying question, escalate, invoke specialist, or stop.

Intuition: game-theoretic reasoning applies only to actions that are actually available at the decision point.

### MOGT-D5: Pareto Frontier

Given objective vectors for all actions in $A_t$, the Pareto frontier is:

$$
P_t = \{a \in A_t \mid \nexists b \in A_t: v(b, s_t) \succ v(a, s_t)\}
$$

where $\succ$ denotes strict dominance across all active objectives.

Intuition: frontier membership means an action is not obviously worse than another available action on every objective.

### MOGT-D6: Conversation Game

A conversation game is the structured interaction among conversational roles where each role exposes preferences, proposes actions, or contests proposals under shared or partially conflicting objectives.

Intuition: disagreement between agents can be treated as strategic interaction rather than pure noise.

### MOGT-D7: Negotiation Stability

A decision episode is negotiation-stable when it reaches an accepted action within a bounded number of turns and without repeating a conflict cycle above a defined threshold.

Intuition: the point is not perfect consensus, but bounded convergence without churn.

### MOGT-D8: Overhead Envelope

The overhead envelope is the admissible bound on token cost, latency, and review burden imposed by a decision policy:

$$
H = (tokens, latency, review\_burden)
$$

Intuition: an elegant policy is not useful if it is too expensive or too slow to run.

### MOGT-D9: Policy Regime

A policy regime is the operational decision rule used in a trial, such as heuristic arbitration, weighted-sum scoring, Pareto-guided filtering, or bargaining-guided negotiation.

Intuition: experiments compare regimes, not isolated prompts.

## Measurement Definitions

### MOGT-M1: Decision Quality Score

Decision quality score is the protocol-defined evaluation of how well the selected action satisfies the active objective set under blinded review or benchmark scoring.

Intuition: this is the primary outcome measure for whether a policy helps.

### MOGT-M2: Traceability Coverage

Traceability coverage is the fraction of decision episodes where reviewers can recover the active objectives, principal tradeoff, and reason for final action selection from the recorded trace.

Intuition: a better policy should make decisions easier to inspect, not just easier to make.

### MOGT-M3: Conflict Resolution Convergence Rate

Conflict resolution convergence rate is the proportion of contested decision episodes that converge within the protocol's bounded-turn threshold.

Intuition: this measures whether disagreement handling actually resolves decisions.

### MOGT-M4: Overhead Acceptability Ratio

Overhead acceptability ratio is the fraction of runs where the observed overhead envelope remains within the protocol's allowed threshold while maintaining minimum decision quality.

Intuition: operational feasibility must be measured jointly with outcome quality.
