# Concept Layer Optimizer Glossary

## Feature Language

| Term | Meaning | Status | Notes |
| --- | --- | --- | --- |
| Seed point | The initial idea, model, architecture, design, plan, or problem the user wants to optimize. | no-match | Candidate local term for this sigil. |
| Target context | The working size and purpose of the problem space the optimized concept must serve. | partial | Related to bounded context and implementation-layering scope, but narrower here. |
| Concept layer | A level of abstraction where concepts make sense together and can be decomposed into smaller cooperating concepts. | no-match | Candidate local term. |
| Concept unit | A candidate smaller concept produced during recursive reduction. | no-match | Candidate local term. |
| Smallest coherent unit | The smallest concept that remains meaningful, testable, and recomposable inside the target context. | partial | Related to Smallest Working Unit, but conceptual rather than execution-task oriented. |
| Closed system | A concept unit with clear responsibility, inputs, outputs, and recomposition boundaries for the current context. | no-match | Local closure rule, not a global ontology claim. |
| Optimization point | The selected balance between smaller working units and enough context to keep the design coherent. | no-match | Core decision produced by the sigil. |
| Proposer | The role conversation that builds a candidate decomposition or design. | partial | Role is compatible with robot-talks investigators, but this sigil uses it for proposal construction. |
| Balancer | The role conversation that challenges proposal scope, premature complexity, lost context, and false reductions. | partial | Related to critique/counterbalance behavior in robot-talks and interrogation workflows. |
| Role conversation trace | The record of Proposer claims, Balancer objections, reconciliation decisions, and stable disagreements. | no-match | Used to make multi-role reasoning auditable. |
| Stable disagreement | A repeated tension that does not change after another round of Proposer and Balancer exchange. | no-match | Routes to decision-gate or robot-talks when it blocks optimization-point selection. |
| Proposal track | One candidate solution path with its own proposer and balancer passes. | no-match | Required for tournament mode. |
| Recursive round | One pass of splitting, testing, balancing, and reconciling concept units. | no-match | Must be finite and budgeted. |
| Composition model | The explanation of how smaller units add or combine back into an upper concept layer. | no-match | Guards against reduction that cannot rebuild the original design. |
| Tension ledger | The record of objections, contradictions, unresolved decisions, and premature-complexity risks. | partial | Similar to decision-gate and robot-talks tension records. |
| Premature complexity | Complexity introduced before the current context has a named tension that requires it. | partial | Aligns with implementation-layering's progressive hardening principle. |
| Evolution profile | A short statement of how the system, solution, or plan is expected to change, such as variants, integrations, actors, policy rules, volume, migration, or governance. | no-match | Used to distinguish natural extensibility needs from speculative future scale. |
| Open-endedness | A design property where the current unit remains simple but can accept likely future evolution without being rewritten immediately. | no-match | Must be balanced against premature complexity. |
| Technique pack | The set of gates, lenses, checks, classifiers, closeouts, and mode mechanics used during a run. | no-match | Internal instrument set, not a separate mode. |
| Invocation surface | The user-facing setup layer that captures intent, asks the budget question, and normalizes overrides. | no-match | Does not own decomposition or verdicts. |
| Mode surface | The layer that converts a budget choice into a finite run profile. | no-match | Owns orchestration shape, not technique semantics. |
| Technique surface | The layer that selects and runs techniques through explicit phase hooks. | no-match | Owns technique activation, not core verdicts. |
| Core sigil engine | The layer that owns run state, concept layers, candidate units, closure, recomposition, tensions, and readiness verdicts. | no-match | Runtime-neutral conceptual owner. |
| Trace surface | The layer that preserves role trace, technique trace, reduction trace, tension ledger, and result envelope. | no-match | Makes reasoning auditable. |
| Handoff surface | The layer that routes pass, flag, or block outcomes to the next lifecycle action. | no-match | Routes but does not reinterpret verdicts. |
| RunFrame | Structured state for a run: seed point, target context, optimization goal, constraints, evidence boundary, selected mode, and active techniques. | no-match | Owned by the core sigil engine. |
| ModeProfile | Structured mode configuration with tracks, rounds, role model, technique policy, pitch-off policy, human gates, and closeout policy. | no-match | Produced by the mode surface. |
| TechniqueSpec | Structured technique contract with id, type, phase, trigger, inputs, outputs, failure behavior, and trace fields. | no-match | Produced by the technique surface. |
| PhaseHook | A named phase boundary where techniques may inspect allowed state and emit trace output. | no-match | Prevents technique phase leakage and hidden mutation. |
| ResultEnvelope | Final structured output containing mode, budget, tracks, verdict, selected unit, traces, proofs, deferred complexity, and route. | no-match | Returned through the trace surface. |
| Abstraction-level guard | A classifier that labels each layer or unit by purpose, value, capability, function, workflow, policy, interface, artifact, or operation. | no-match | Prevents reducing one level as if it were another. |
| Recomposition proof | Evidence that smaller concept units can combine back into the upper concept layer without hidden glue. | no-match | Required for accepted splits. |
| Frame-expiry note | A closeout statement naming what context change would invalidate the chosen optimization point. | no-match | Prevents false finality. |
| Cognitive load check | A Balancer check asking whether a split reduced or increased what the user must hold in mind. | no-match | Helps avoid tiny fragments that create more coordination work. |
| Requisite variety check | A Balancer check comparing external variation the unit must handle against internal mechanisms available to handle it. | partial | Derived from cybernetics; used locally as a proportion check. |
| Boundary-object check | A conditional technique for multi-actor contexts that separates stable shared meaning from local variation. | partial | Related to boundary-object literature; no global definition promotion requested. |
| Concept-vs-knowledge status | A label distinguishing a speculative concept claim from a knowledge-backed unit. | no-match | Prevents uncertain ideas from being treated as settled design facts. |
| Premortem pass | A closeout technique that imagines why the selected optimization point failed and adds a guardrail or downgraded readiness. | no-match | Required outside Compact unless explicitly skipped by risk profile. |
| Set-based tournament | A tournament mode mechanic that keeps multiple proposal tracks open until evidence justifies convergence. | no-match | Proposal tracks need assumptions, option value, and elimination conditions. |
| Hidden glue | Unnamed coordination, adapter work, policy, or interpretation required for decomposed units to recombine. | no-match | A sign that a split is not closed. |
| Brittle minimalism | A unit made so small that it cannot absorb known natural evolution pressure. | no-match | Counterbalance to premature complexity. |
| Cycle guard | A rule that stops infinite reduction, repeated renaming, or unresolved role argument loops. | no-match | Required runtime safety rule. |
| Pitch-off | Comparison stage where multiple proposal tracks are evaluated against the same target context. | no-match | Only applies when multiple tracks are enabled. |
| Robot-Talks handoff | Optional route when tensions span layers and require independent investigation. | linked | Existing sigil: arcana/robot-talks/. |
| Decision-Gate handoff | Optional route when a blocker choice prevents selecting an optimization point. | linked | Existing sigil: arcana/decision-gate/. |

## Glossary Gate

- Candidate glossary promotion: not requested.
- Global definition changes: none.
- Unresolved terms: none blocking.
- Linking status: partial, because most core terms are new candidate-local concepts for this sigil.
