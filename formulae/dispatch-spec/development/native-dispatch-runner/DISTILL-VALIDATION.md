# Distill Validation

Verdict: pass

Execution path: local labeled Proposer/Balancer simulation. No subagents were dispatched for this validation because this Invoke authoring run did not have a separate multi-agent execution authorization. This is a design challenge record, not runtime integration evidence.

## Frame

- Larger target: a trustworthy native executor for capability-bound dispatches.
- Smallest coherent unit: compile one valid dispatch into its exact first eligible action set.
- Recomposition target: failure-first and success native canaries entered only through `orchestrate execute`.
- Stopping rule: stop design expansion when every contract requirement maps to an independently acceptable SWU and a concrete final proof.

## Challenge Round 1 — Architecture Scope

- Proposer: implement a complete autonomous executor across all host runtimes.
- Balancer challenge: overbuild and false portability. Host-native subagent calls are not a portable shell API, and host parity has no current proof.
- Reconciliation: split a deterministic portable coordinator from one host-native Orchestrate driver; defer other hosts until the first causal canary passes.

## Challenge Round 2 — Atomicity

- Proposer: implement coordinator, driver, gates, generation, and canaries as one runner task.
- Balancer challenge: the task could pass only as a bundle and conceal whether dispatch compilation, receipt reduction, native spawning, or evidence integrity failed.
- Reconciliation: divide the work into 13 single-behavior SWUs, with a closure-only verification exemption. `SWU-NDR-001` is side-effect-free and independently passable.

## Challenge Round 3 — Proof Integrity

- Proposer: retain the existing native-host canary as integration proof because its receipts and validators pass.
- Balancer challenge: the parent manually spawned agents before finalizing dispatch-shaped evidence; that proves host tools, not dispatch-to-spawn causality.
- Reconciliation: require a single entry point, live ordered action events, host identifiers, failure withholding before success, and a separate historical adjudication rather than evidence rewriting.

## Premortem

Most likely false success: an implementer manually spawns agents, then writes a passing event stream and result. The plan prevents this by requiring:

- only `orchestrate execute <dispatch.json>` as canary entry;
- an action-attempt event before or with every host call;
- a deterministic event-order validator;
- exact host agent identifiers bound to action receipts;
- zero dependent spawns in the failure scenario.

## Acceptance-Critical Gap Check

| Question | Result |
| --- | --- |
| Is the runtime owner explicit? | yes — Orchestrate |
| Is Dispatch Spec still validation-only? | yes |
| Can the first unit pass without host side effects? | yes |
| Can each SWU be accepted independently? | yes |
| Are failure and success causally testable? | yes |
| Is historical overclaim correction planned without rewriting evidence? | yes |
| Are cross-host parity and legacy migration separated? | yes |
| Does the execution dispatch validate? | yes — no blocks or flags |

## Frame Expiry

Revisit the coordinator/native-driver boundary if the host exposes a stable programmatic native-agent API usable by deterministic runtime code. Until then, collapsing the layers would reintroduce hidden host dependence.

No acceptance-critical design or planning gap remains. Implementation risk remains and is intentionally owned by the Task Session SWUs.
