# Implementation Readiness

## Identity

- Canonical ID: `implementation-readiness`
- Aliases: none
- Scope: library

Implementation Readiness composes planning, decision, routing, and unit execution so a rough implementation goal becomes staged, decided, and—when a Work Pack declares an execution policy—runs through one bounded outer loop.

## Trigger Conditions

- The user has a feature, workflow, infrastructure change, or improvement idea.
- The work needs staged implementation before execution.
- Blocker decisions should be resolved before mutation.
- A direct request names one exact Work Pack and an execution mode: `one-unit`, `finite-frontier`, or `until-real-blocker`.

## Required Sigils

| Sigil | Role In Spell | Required Mode |
| ----- | ------------- | ------------- |
| `implementation-layering` | Create staged implementation layers. | standard |
| `decision-gate` | Resolve blocker-level decisions revealed by the layers. | generic |
| `continuation-router` | Admit and join one declared internal owner route from the current Work-Pack binding. | work-pack-bound |
| `task-session` | Prepare or execute one selected task. | dry-run or execute |

## Shared State

| State | Owner | Updated By | Consumed By |
| ----- | ----- | ---------- | ----------- |
| layer plan | spell | `implementation-layering` | `decision-gate`, `task-session` |
| decision record | spell | `decision-gate` | `task-session` |
| execution policy and entry | Work Pack / Plan | Invoke and readiness owners | outer-loop reducer |
| execution intent binding | outer loop | `implementation-readiness` | `continuation-router` |
| owner receipt chain | outer loop | selected capability through Router | outer-loop reducer |
| task run report | spell | `task-session` | user, observability |

## Execution Phases

| Phase | Sigil | Input | Output | Gate | Failure Policy |
| ----- | ----- | ----- | ------ | ---- | -------------- |
| 1 | `implementation-layering` | implementation goal | layer plan | minimum useful proof identified | block if scope is unclear |
| 2 | `decision-gate` | layer plan | decision record | blocker decisions resolved | block on unresolved blockers |
| 3 | `task-session` | selected layer or task | task report | done criteria and validation path known | flag if execution should wait |
| 4 | optional `inventory` | layer plan and decisions | inventory entries | inventory exists | skip if no inventory package |

## Work-Pack Execution Outer Loop

`scripts/execution_loop.py` is the deterministic reducer and
`scripts/run_execution_loop.py` is its JSON command surface. The controller:

1. freezes one Work Pack ID, semantic digest, allowed-routes digest, ordered frontier, direct invocation ID, execution mode, and finite step budget;
2. creates a stable loop ID plus a route-specific `ExecutionIntentBinding`;
3. classifies one execution-entry projection;
4. selects expected future material locally when the entry is `selection-ready`;
5. submits exactly one `owner-prerequisite` or `task-ready` route to Continuation Router;
6. records `authorization_source=work-pack-binding` and never asks for another route authorization;
7. waits for the exact action-correlated owner or fresh Task Session receipt;
8. advances only inside the captured frontier and stops on completion, budget, replay, failed join, or a declared stop decision.

`scripts/readiness_execution.py` is the producer/consumer boundary. It compiles
the exact Work Pack Readiness config and report into the policy and entry used
to initialize the loop. For plan-once execution, `selection-ready` can become
`task-ready` only when the current execution binding produced the selection
intent and both the selected-unit receipt and the single-use mutation-admission
receipt match the plan epoch and unit contract. A separate confirmation cannot
substitute for the direct Work Pack execution intent.

For a guarding Task Session prerequisite, the same boundary calls the
`task-session-until-blocker` fresh-session owner only after the exact task route
is admitted. It binds the resume request to the live outer-loop projection,
the exact latest joined owner receipt, reclassified binding, captured
fresh-session budget, and existing Task Session receipt history. It persists
one exclusive admission and replaces the candidate task action's synthetic
identifier with the admitted fresh session identifier. A missing, stale,
mismatched, or replayed admission blocks instead of falling back to recursive
or untracked Task Session entry.

The reducer states are `ready`, `awaiting-selection`, `awaiting-owner`,
`awaiting-task-session`, `complete`, and `blocked`. Only one action may be
outstanding. Every join event must match its action ID, route fingerprint, and,
for Task Session, its fresh session ID.

Owner receipts and Task Session receipts are separate arrays. An owner receipt
may reclassify the entry but cannot complete a unit. Only a passing fresh Task
Session receipt adds a unit to the ordered completion frontier.

Historical completion is a third, immutable input. The readiness producer
validates an ordered `completion_continuity.completed_prefix` and binds it into
the execution policy, intent binding, loop ID, state, and fresh-resume digest.
The active loop keeps newly completed units in `visited_units`; it never copies
historical units there. The current cursor is therefore the historical prefix
length plus the active-loop visited length. A selected unit before that cursor,
a gap or replay in the prefix, or a policy/state continuity mismatch blocks
before selection or dispatch.

Execution-policy schema `1.1.0`, execution-intent-binding schema `1.1.0`, and
outer-loop-state schema `1.2.0` carry this continuity contract. A legacy `1.0.0`
policy is accepted only for a single-unit compatibility path; it may classify
or bind an already explicit entry, but it cannot initialize this
selection-capable outer loop. After a semantic repair, the repaired readiness
report must initialize a new loop. A pre-repair intent cannot be rebound to the
repaired report, and a historically advanced semantic-drift report must be
freshly audited rather than synthesized as all-pending.

When the digest-bound execution policy declares `declared-retry`, an owner may
return exactly `REPAIRABLE_OWNER_CONDITION` for the same selected unit, entry,
binding, and route. The controller records the causal owner receipt, preserves
the consumed route fingerprint as immutable replay history, and gives only the
next Router admission a derived one-shot view of that same route. The retry uses
the ordinary step budget and requires no authorization prompt. A changed route,
entry, unit, receipt correlation, or blocker code fails closed; a second retry
ends with `DECLARED_RETRY_EXHAUSTED` before a third owner dispatch.

### Pre-execution prerequisite return boundary

The generic outer-loop `owner-prerequisite` transition above occurs before a
Task Session exists, so a successful owner join may reclassify the entry to
`task-ready` and start one fresh Task Session. It is not the return path for an
owner hop requested by an already-running Task Session.

When `source_phase=pre-execution-prerequisite`, Implementation Readiness may
normalize authorization evidence only from the current direct user request or
an exact durable approval that binds the declared route, task, SWU, attempt,
target inventory, validation contracts, and allowed effect. It must preserve
the Router's bound control handle, return it to the same Task Session attempt,
and resume exactly once at `task-session:context-build`. It must not enqueue a
fresh Task Session, reinterpret the owner receipt as unit completion, or treat
the Work-Pack declaration, execution-entry projection, or retrieved context as
ambient apply authority.

The eight stop classes are product or semantic choice, scope expansion,
destructive or irreversible effect, credentials or secrets, external message
or network effect, cost or risk acceptance, authority/promotion/publication/
deployment, and failed acceptance-critical validation. They stop before the
next dispatch; they are not converted into authorization prompts.

### Machine contracts

- `schemas/execution-policy.schema.json` — frozen automatic and stop policy.
- `schemas/execution-entry-projection.schema.json` — one truthful current entry state.
- `schemas/execution-intent-binding.schema.json` — one current route binding derived from direct intent.
- `schemas/outer-loop-state.schema.json` — stable run, frontier, budget, histories, and pending correlation.
- `schemas/outer-loop-action.schema.json` — the one next controller action.
- `schemas/outer-loop-event.schema.json` — the exact selection, owner, or Task Session join event.

The controller does not perform owner mutation, weaken Task Session admission,
absorb a new frontier unit, recursively resume a Task Session, promote evidence,
publish, deploy, or contact external systems.

## Observability

Record layer count, decision count, blockers, selected task, validation readiness, automatic/stop decision counts, route admissions, owner joins, fresh Task Session IDs, authorization prompt count, budget, completion frontier, and stop reason when `.arcanum/observability/` exists.

## Output Contract

Return a readiness report with the layer plan, resolved decisions, Work Pack/loop identity, captured frontier and mode, automatic decisions, distinct owner and Task Session receipts, authorization prompt count, completed units, stop reason, and recommended next action.
