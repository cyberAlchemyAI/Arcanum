# Native Dispatch Runner Glossary

| Term | Meaning in this package | Not the same as |
| --- | --- | --- |
| Dispatch | A structured route document naming steps, dependencies, boundaries, and evidence. | A running process. |
| Dispatch Spec | The capability that validates dispatch structure and route rules. | The executor. |
| Native Dispatch Runner | Orchestrate's execution mode for a valid capability-bound dispatch. | Dispatch Spec itself. |
| Coordinator | Deterministic code that compiles permitted actions and reduces receipts. | A model-backed agent. |
| Native host driver | Skill logic that calls the current host's native subagent operations. | A portable shell command. |
| Action | A coordinator-emitted instruction such as `spawn`, `wait`, `join`, `block`, or `complete`. | Evidence that the action happened. |
| Event | Append-only evidence recorded when an action is attempted or resolved. | A synthesized narrative. |
| Receipt | Structured result bound to a dispatch, run, wave, step, role, capability, and agent. | A test expectation. |
| Gate | Deterministic decision that permits or withholds dependent actions. | Human lifecycle approval. |
| Wave | A set of roles eligible to execute under the same dependency boundary. | Arbitrary concurrency. |
| Failure withholding | The rule that non-pass or missing required evidence prevents dependent spawns. | Merely marking the final result failed. |
| Integration canary | A small causal run starting at the public execution entry point and ending in native host evidence. | A manually assembled receipt fixture. |
| Closeout | Final validation of the completed dispatch state and result evidence. | Promotion. |
| Installed surface | A generated host-specific skill package derived from canonical source. | Canonical authority. |
