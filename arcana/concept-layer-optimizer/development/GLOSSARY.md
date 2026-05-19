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
| Proposal track | One candidate solution path with its own proposer and balancer passes. | no-match | Required for tournament mode. |
| Recursive round | One pass of splitting, testing, balancing, and reconciling concept units. | no-match | Must be finite and budgeted. |
| Composition model | The explanation of how smaller units add or combine back into an upper concept layer. | no-match | Guards against reduction that cannot rebuild the original design. |
| Tension ledger | The record of objections, contradictions, unresolved decisions, and premature-complexity risks. | partial | Similar to decision-gate and robot-talks tension records. |
| Premature complexity | Complexity introduced before the current context has a named tension that requires it. | partial | Aligns with implementation-layering's progressive hardening principle. |
| Evolution profile | A short statement of how the system, solution, or plan is expected to change, such as variants, integrations, actors, policy rules, volume, migration, or governance. | no-match | Used to distinguish natural extensibility needs from speculative future scale. |
| Open-endedness | A design property where the current unit remains simple but can accept likely future evolution without being rewritten immediately. | no-match | Must be balanced against premature complexity. |
| Cycle guard | A rule that stops infinite reduction, repeated renaming, or unresolved role argument loops. | no-match | Required runtime safety rule. |
| Pitch-off | Comparison stage where multiple proposal tracks are evaluated against the same target context. | no-match | Only applies when multiple tracks are enabled. |
| Robot-Talks handoff | Optional route when tensions span layers and require independent investigation. | linked | Existing sigil: arcana/robot-talks/. |
| Decision-Gate handoff | Optional route when a blocker choice prevents selecting an optimization point. | linked | Existing sigil: arcana/decision-gate/. |

## Glossary Gate

- Candidate glossary promotion: not requested.
- Global definition changes: none.
- Unresolved terms: none blocking.
- Linking status: partial, because most core terms are new candidate-local concepts for this sigil.
