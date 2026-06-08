# Multi-Objective Game Theory for Agentic Conversation Decisions

## Status

Partial synthesis draft. `PSEC-01` through `PSEC-03` are now drafted from project foundations and canonical definitions; result-facing sections remain evidence-gated. This file is a narrative synthesis artifact and is not the normative definition source.

## Provisional Abstract

This paper studies whether explicit multi-objective and game-theoretic decision policies can improve agentic conversation decisions when systems must trade off quality, cost, latency, risk, and escalation pressure. The current draft establishes the problem setting, the canonical decision model, and the planned experimental methodology, while leaving result-facing claims evidence-gated until live runs are completed. The research program compares heuristic, weighted-sum, Pareto-guided, and negotiation-enabled regimes across traceability, arbitration quality, negotiation stability, and operational feasibility. The intended contribution is not a claim that game-theoretic reasoning is universally beneficial, but a traceable evaluation framework for deciding when these policy regimes produce inspectable and operationally acceptable gains.

## Paper Design Pilot Artifacts

- `papers/PAPER-SPEC.md` - section registry and design contract
- `papers/PAPER-STORIES.md` - section-scoped writing stories
- `papers/PAPER-TEST-SPEC.md` - evidence and structure checks
- `papers/PAPER-REVIEW.md` - current readiness verdict

These artifacts are a pilot application of a contract-first design workflow to the MARS paper lifecycle. They are intentionally lightweight and should be revised after MOGT completes live evidence work.

## Paper Section Nodes

1. `PSEC-01` Motivation and problem framing - drafted
2. `PSEC-02` Canonical definitions and decision model - drafted
3. `PSEC-03` Experimental methodology - drafted
4. `PSEC-04` Traceability and arbitration results - evidence-gated
5. `PSEC-05` Negotiation stability results - evidence-gated
6. `PSEC-06` Overhead envelope and adoption guidance - evidence-gated
7. `PSEC-07` Threats to validity and future work - partially draftable, to be refreshed after live runs

These section node IDs are referenced by `registry/RESEARCH-GRAPH.md` so the narrative paper plan can be traced explicitly to claims, experiments, and authority sources before empirical results exist.

## PSEC-01 Motivation And Problem Framing

Agentic systems increasingly make decisions through conversation rather than through a single monolithic scoring function or a fixed pipeline. In these settings, the decision problem is not merely to generate a plausible next response. It is to select an action under competing pressures such as output quality, runtime cost, latency, safety risk, and the need to escalate or defer when confidence is insufficient. The core premise of this project is that these competing pressures should be treated as an explicit decision surface instead of being left inside prompt heuristics or hidden reviewer intuition.

The motivation for MOGT comes from a mismatch between how conversational agent systems are often evaluated and how they are actually used. Real decision episodes are bounded, role-sensitive, and operationally constrained. An orchestrator may prefer fast progress, a specialist agent may prefer deeper reasoning, a governance voice may prefer caution, and a reviewer may prefer decision traces that are easy to reconstruct. When these tensions are collapsed into an opaque final choice, it becomes difficult to tell whether a system is genuinely making better decisions or merely producing answers that look fluent after the fact.

This motivates four linked research claims. First, MOGT asks whether explicit objective vectors improve traceability and reviewability relative to implicit heuristics (`MOGT-C1`). Second, it asks whether Pareto-aware or dominance-aware selection improves multi-objective decision quality over heuristic arbitration (`MOGT-C2`). Third, it asks whether negotiation-oriented interaction can reduce oscillation, deadlock, and unresolved disagreement in multi-agent conversational settings (`MOGT-C3`). Fourth, it asks whether any such gains survive operational constraints on cost, latency, and review burden (`MOGT-C4`). These claims are deliberately connected: a regime that improves quality while destroying inspectability or feasibility would not satisfy the intended contribution of this work.

The project does not treat all conversational systems as interchangeable. Its unit of analysis is the bounded conversational decision episode: a finite sequence of turns ending in an action choice, an escalation, or a stop condition. Within that episode, the relevant question is whether explicit multi-objective and game-theoretic policy regimes produce more legible and better controlled decisions than the kinds of loosely structured heuristics that are common in current agentic orchestration. This framing keeps the research grounded in operational decision episodes rather than in unrestricted open-ended chat.

The paper therefore positions MOGT as a research program about decision policy quality inside agentic conversations, not as a blanket claim that game theory should be added everywhere. The first contribution is conceptual and methodological: make the tradeoff structure visible. The second contribution, which remains evidence-gated until the experiment wave completes, is empirical: determine where explicit multi-objective or negotiation-enabled regimes provide measurable benefits and where they merely add overhead.

## PSEC-02 Canonical Definitions And Decision Model

The canonical semantics for this project live in `definitions/DEFINITIONS.md`; this section is a condensed synthesis of those terms rather than a replacement for them. MOGT defines an agentic conversation decision process as a bounded sequence of conversational turns in which agents or an orchestrator choose the next action under explicit objectives, constraints, and escalation rules. The important implication is that the research target is the decision policy operating inside the loop, not the entire software system around it.

At each turn $t$, the decision state is described as:

$$
s_t = (c_t, A_t, O_t, K_t)
$$

where $c_t$ is the available conversation context, $A_t$ is the candidate action set, $O_t$ is the active objective set, and $K_t$ is the active constraint set. This framing matters because it prevents the project from slipping into vague discussion of “better decisions” without saying what information was available, which actions were actually possible, what objectives were active, and what constraints were binding.

MOGT treats decision quality as a genuinely multi-objective problem. For any candidate action $a$, the project models an objective vector rather than assuming that all value can be compressed immediately into a single scalar. In the canonical formulation, the vector tracks dimensions such as quality, cost, latency, risk, and escalation pressure. This leads directly to the distinction between scalarized baselines and frontier-aware reasoning. A weighted-sum regime turns several objectives into one score for comparison. A Pareto-guided regime preserves the fact that an action can be strong on one dimension without being dominated on all others. This difference is not cosmetic; it is central to the claim that explicit multi-objective structure may produce more faithful decision selection than heuristic or prematurely scalarized policies.

The project also defines a conversation game, where conversational roles expose preferences, propose actions, or contest proposals under shared or partially conflicting objectives. This is the conceptual bridge from pure multi-objective choice to game-theoretic interaction. Under this view, disagreement between roles is not only noise to be suppressed. It can be treated as structured interaction that reveals whether a proposed action is robust under competing pressures. Negotiation stability then becomes a measurable property of the episode: can the system reach an accepted action within bounded turns without entering repetitive conflict cycles?

These definitions support four measurement constructs used throughout the planned experiments. Decision quality score (`MOGT-M1`) measures how well the chosen action satisfies the active objective set under benchmark or blinded review. Traceability coverage (`MOGT-M2`) measures whether reviewers can reconstruct active objectives, the main tradeoff, and the final selection rationale from the recorded trace. Conflict resolution convergence rate (`MOGT-M3`) measures whether contested episodes actually resolve within bounded turns. Overhead acceptability ratio (`MOGT-M4`) measures whether the policy remains within an acceptable envelope for tokens, latency, and review burden while preserving minimum quality.

Taken together, the decision model implies that MOGT is comparing policy regimes rather than prompts. The relevant alternatives are heuristic arbitration, weighted-sum scalarization, Pareto-guided filtering, and bargaining-guided negotiation. Each regime makes a different commitment about how objectives are represented, how conflicts are handled, and what information remains visible for later inspection. The paper’s empirical sections will eventually evaluate those commitments; the present design-time draft establishes the conceptual model they are meant to test.

## PSEC-03 Experimental Methodology

The MOGT methodology is intentionally comparative rather than anecdotal. The project does not treat a single impressive transcript as sufficient evidence for a claim about decision policy. Instead, the planned design holds scenario families fixed, compares baseline and intervention regimes on the same decision problems, records a stable metadata envelope for each run, and evaluates both final outcomes and the traces that produced them. This stance follows the project’s methodology baseline, which prioritizes paired comparative experiments, explicit measurement, and reproducible execution before any strong claim upgrades.

The first research wave is organized at foundation tier rather than publication-maximal rigor. That is a deliberate choice. MOGT is still in a greenfield evidence state, so the immediate objective is directional validity under strong gates rather than premature overfitting to sophisticated analysis. The methodology therefore emphasizes measurable criteria, controlled comparisons, source-governed evaluation, and clean handoff into later evidence adjudication. The paper can describe this methodology now, but it cannot yet report empirical findings because no live run data has been produced.

The experiment program is divided into four linked bundles. E1 focuses on tradeoff traceability and asks whether explicit objective articulation improves reviewability relative to heuristic baselines. E2 focuses on Pareto-aware arbitration quality and asks whether dominance-aware selection improves decision quality over heuristic or weighted-sum selection. E3 focuses on negotiation stability under conflict and asks whether bounded negotiation structures reduce unresolved disagreement and cycling. E4 focuses on the overhead feasibility envelope and asks whether any observed benefits remain acceptable once latency, token cost, turn count, and reviewer burden are measured together. The recommended first-wave order is E1, E2, E4, then E3 so that the baseline policy comparison is stabilized before deeper disagreement handling is evaluated.

Methodologically, the project treats measurement as part of the design, not as an afterthought. Decision quality, traceability recovery, convergence, and overhead must all be operationalized explicitly in protocols rather than inferred from narrative impressions. This is especially important because the policy regimes under comparison create different kinds of trace. A regime that appears strong on final choice quality but produces opaque or reviewer-expensive traces cannot automatically be treated as an improvement. For that reason, the MOGT methodology keeps system overhead and human review burden separate and evaluates them alongside quality rather than below it.

The paper’s methodology section also has to make clear what the current draft does not yet contain. It does not report completed runs, effect sizes, or adjudicated claim outcomes. It describes the planned evidence path: controlled comparison of policy regimes, protocol-defined measurement, append-only JSONL run capture, and later claim updates through the evidence-status layer. This is important for scope discipline. The present document can responsibly explain why the methodology is designed the way it is and what each experiment is intended to establish, while reserving empirical support statements for the sections that will be completed only after live execution.
