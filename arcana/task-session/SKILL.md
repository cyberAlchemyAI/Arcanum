---
name: task-session
description: "Use when: executing or resuming one nearest evidence-backed bounded work-pack task or SWU end to end, or routing explicit until-blocker series intent to its owning spell."
argument-hint: "[<task-reference|to <target>>] [--task <TASK-ID>] [--swu <SWU-ID>] [--until-blocker] [--list-nearest] [--from <path>] [--session <id>] [--runtime <id>] [--via runtime] [--follow-next-route] [--authorize-route <capability>:<mode>[:<mutation-mode>]] [--auto] [--dry-run] [--output <path>]"
tier: arcana
domain: guided-execution
version: 0.8.0
origin: generalized from recurring single-task execution governance practice
allowed-tools: Read, Write, Glob, Grep, AskQuestions, Task, Bash
---

# Sigil: Task Session

<objective>
Execute one bounded task end to end while making trade-offs explicit, enforcing blockers, validating completion, and closing only after required task evidence and declared projections are synchronized through their owner.
</objective>

<logic-type>
Arcana: guided execution loop with human decision points, hard gates, and completion evidence.
</logic-type>

<required-sigils>

| Sigil | Role In Task Session | Required Mode |
| --- | --- | --- |
| `context-builder` | Build a bounded context pack from the selected task/SWU, source links, constraints, related architecture/spec artifacts, write scope, and validation surface before decisions, gates, or runtime handoff. For `--via runtime`, produce a strict Markdown plus JSON/index handoff pack stored as session evidence. | lean or standard |
| `decision-gate` | Convert unresolved blocker-level choices into user-ready option cards with context, trade-offs, recommendation, and a durable decision record before returning `BLOCK`. | blocker-only |
| `continuation-router` | Normalize a terminal Task Session receipt, prevent unchanged re-entry, dispatch and join the required bounded closeout-sync owner hop when eligible, and expose an optional non-closeout owner route without absorbing either owner's work. | one-hop |

</required-sigils>

<flags>
- `--until-blocker`: declare series intent. Task Session must route the request
  to the installed `task-session-until-blocker` spell with the exact work-pack,
  stop condition, runtime, and caller scope. It must not execute multiple SWUs
  inside one Task Session receipt.
- With no positional target or selector, resolve the nearest evidence-backed
  work pack or returned Task Session SWU, revalidate it live, and execute at
  most one SWU.
- `--list-nearest`: rank and report eligible continuity candidates without
  executing or mutating.
- `--from <path>`: override automatic discovery with one explicit
  `WORK-PACK.md` or Task Session continuity cursor.
- `--session <id>`: select the exact repository-local continuity cursor for a
  native runtime session when visible conversational context is unavailable;
  normally Task Session uses the current runtime session id without requiring
  this flag.
- `--auto`: auto-select only an option explicitly classified both nonconsequential and reversible; otherwise return `BLOCK` for the unresolved choice and record why it was not auto-selected.
- `--dry-run`: return the execution path, decision pack, and gate checks without mutating files.
- `--output <path>`: write the session report to a specific path.
- `to <target>`: resolve a work-pack target by explicit path or current context.
- `--task <TASK-ID>`: select one task from a work-pack.
- `--swu <SWU-ID>`: select one Smallest Working Unit from a work-pack.
- `--runtime <id>`: choose the execution runtime adapter, such as `codex`.
- `--via runtime`: delegate through the selected runtime adapter when available.
- `--follow-next-route`: after required closeout synchronization, run one optional non-closeout Continuation Router hop and return the selected owner's receipt and next route. Never recursively resume Task Session.
- `--authorize-route <capability>:<mode>[:<mutation-mode>]`: authorize only an optional non-closeout continuation tuple for the declared target and write scope. It does not bypass the selected owner's gates. Required closeout synchronization derives its own narrower authorization from the task contract and terminal receipt.
</flags>

<applicability>
Use this sigil when:

- there is one explicit task to execute,
- a no-argument invocation should resume one uniquely nearest, evidence-backed
  SWU from current-session or repository-local continuity evidence,
- the task has dependencies, deliverables, or done criteria,
- implementation choices need visible trade-offs,
- gate failures must stop mutation,
- the task record should be synchronized with evidence after completion.
</applicability>

<inputs>
Expected inputs, if available:

- explicit task reference or task file,
- task objective,
- dependency list,
- implementation checklist,
- deliverables,
- done criteria,
- done-criterion and validation-obligation criticality when already classified; unclassified obligations fail closed as acceptance-critical,
- relevant constraints,
- validation commands or accepted substitutes,
- optional `WORK-PACK.md` with task board, SWU manifest, waves, and task contracts,
- optional runtime adapter selection from the installed repository command context.
- optional lifecycle owner and experiment harness path when executing spell or sigil development work.
- optional previous terminal receipt and continuation receipt for repeated-block and cycle detection.
- optional exact continuation authorization evidence from the current user request or a durable approval artifact.
- closeout synchronization target inventory, baseline identities or digests, and validation commands when the task or work-pack already declares them.
- closeout source-receipt contract and expected owner-receipt contract when
  execution will require evidence, status, route, work-pack, checklist,
  Dispatch, registry, or declared Craft projection synchronization.
- optional explicit series intent such as `--until-blocker`, `all until
  blocker`, `all SWUs`, `one go`, or an equivalent request to traverse one
  ordered work-pack stream.
- optional native runtime session id, visible-session selector, or
  repository-local Task Session continuity cursor.
</inputs>

<process>
## Step 0 - Route Multi-Session Intent

0a. Before selecting one task/SWU, detect explicit series intent from the
`--until-blocker` flag or equivalent current user wording.
0b. Resolve the exact work-pack scope and route it to the installed
`task-session-until-blocker` spell. Pass the stop condition, captured
work-pack identity, runtime selector, and current approval boundary.
0c. Stop direct Task Session execution after the handoff. If the spell is
missing or the work-pack scope is ambiguous, return `BLOCK` with that exact
gap. Never silently narrow series intent to one SWU and never place several
SWUs in one Task Session receipt.

## Step 1 - Resolve Task Scope

1. Resolve exactly one target task. Explicit user selectors, `--from`, `to
   <target>`, `--task`, and `--swu` always outrank automatic discovery.
2. With no positional target or selector, enter `resume-nearest` mode and cap
   execution at one task or SWU.
3. In `resume-nearest` mode, rank selectors lexicographically in this order:
   visible current-session context, the exact current native-session continuity
   cursor (or `--session` override), the nearest ancestor `WORK-PACK.md` from
   the current working directory, then uniquely scope-matched repository-local
   Task Session continuity.
4. Visible current-session context means the active prompt/session evidence
   supplied by the runtime. When older conversational content is not available
   because of compaction, use the durable cursor; never claim access to lost
   tokens or crawl unscoped user transcripts.
5. Resolve durable cursors from
   `.arcanum/task-session/continuity/<session-or-scope-id>.json` using
   `continuity.schema.json`. A cursor is selector evidence, not task-readiness
   authority.
6. Use `scripts/resolve-nearest-swu.py` when deterministic filesystem
   resolution is available. `--list-nearest` returns its ranked candidates and
   stops before context building or mutation.
7. Reject stale or scope-escaping cursors, non-Task-Session next routes,
   global-latest telemetry, fuzzy relevance, and cross-project inference. If
   the highest-priority tier contains multiple candidates, return `BLOCK` with
   the ranked candidates and the smallest disambiguation.
8. Re-read the selected live work pack and prove that the candidate exists, is
   not complete, is selected or the unique next-ready unit, has satisfied
   dependencies and blockers, and declares write scope, done criteria, and a
   validation surface. If any check fails, return `BLOCK`; never fall through
   to a lower-priority candidate silently.
9. Parse the task objective, dependencies, deliverables, write scope, done
   criteria, validation surface, and related artifacts that may need
   synchronization after completion.

## Step 2 - Build Context Pack

10. Run `context-builder` in lean or standard mode for the selected task/SWU.
11. Include the task contract, source links, architecture/spec references, work-pack row, dependency rows, blocker rows, write scope, done criteria, validation surface, and known repository conventions.
12. When `--via runtime` is set, request a runtime handoff pack from Context Builder, emitted as Markdown plus JSON/index and persisted under session/run evidence.
13. Extract hard constraints and cross-artifact obligations from the context pack before selecting an implementation path.
14. If linked context is missing, contradictory, stale, unsafe, too weak, missing write scope, missing validation, or lacks strict coverage for a runtime handoff, return `BLOCK` with the missing context or contradiction and stop before mutation.
15. Record the context pack summary, handoff artifact paths, strict coverage status, and the source artifacts that controlled execution.

## Step 3 - Build Decision Pack

16. Enumerate unresolved task decisions with more than one viable option.
17. For each decision, build option cards with:
   - what the option entails,
   - short-term consequence,
   - long-term consequence,
   - speed impact,
   - complexity impact,
   - risk impact,
   - maintenance impact,
   - recommended option with rationale.
18. Classify each decision as blocker, deferrable, or assumption. Independently
    classify the proposed choice as consequential or nonconsequential and as
    reversible or irreversible.
19. Ask the user to choose each blocker decision when the blocker is discovered before mutation.
20. If `--auto` is provided, auto-select only an option explicitly classified
    both nonconsequential and reversible. Otherwise ask when interactive or
    return `BLOCK` in unattended auto mode, and record the missing or
    disqualifying classification.
21. If a blocker-level decision remains unresolved and consequential work cannot proceed, invoke `decision-gate` before returning `BLOCK`; include the exact context, option cards, recommendation, and decision artifact path in the task-session report.

## Step 4 - Evaluate Gates

22. Check task dependencies, stated constraints, required approvals, source links, context-pack obligations, strict handoff coverage when applicable, write scope, and available validation paths.
23. If a blocker exists because a human approval, policy choice, destructive cleanup, irreversible mutation, cost/risk acceptance, or rollout option is unresolved, run `decision-gate` for that blocker before continuing to Step 4A or returning `BLOCK`.
24. If a blocker exists for missing evidence, missing files, unavailable tools, or contradictory context with no meaningful user option, preserve `BLOCK`, record exact unblock actions, and continue only to Step 4A when a terminal owner handoff can be formed. Stop mutation inside the selected task, then continue to Step 8 for required closeout synchronization.
25. If the task can proceed with assumptions, record those assumptions before mutation.
25a. When a passing terminal receipt would require closeout synchronization,
run the closeout prerequisite preflight before mutation admission. Require the
declared target inventory, live baseline identities or exact digests,
source-receipt contract, owner validation commands, expected owner-receipt
contract, admitted delta classes, and unique-successor policy.
25b. Persist the preflight result with the controlling work-pack identity and
current target baselines. Missing, ambiguous, stale, expanded, or forbidden
closeout inputs return `BLOCK` before implementation writes and before owner
dispatch.
25c. This preflight proves only that a later terminal result can be synchronized
within declared bounds. The actual typed deltas, source receipt, owner
dispatch, joined receipt, and cursor remain Step 8 obligations.

## Step 4A - Resolve One Terminal Continuation

26. When the gate is terminal, emit a normalized continuation handoff containing the source result, receipt path, target scope, blocker class, controlling evidence identities or digests, blocker fingerprint, explicit next-route advice, and unblock actions.
27. Preserve this handoff for Step 8 closeout synchronization. Do not return before the closeout-sync decision is complete.
28. For continuation beyond synchronization, invoke `continuation-router` to expose one to three probable routes. Do not re-enter Task Session when the same blocker fingerprint and source evidence are unchanged.
29. Without `--follow-next-route`, do not dispatch the optional non-closeout route. This does not disable required Step 8 closeout synchronization.
30. With `--follow-next-route`, pass the exact `--authorize-route` tuple and current approval evidence to Continuation Router only after closeout synchronization. It may dispatch at most one non-closeout owner route and must run that owner's own gates.
31. Preserve the Task Session source result even when either owner route succeeds. Every owner returns a separate receipt and next route; Task Session must not recursively execute it.
32. Treat an ambiguous optional route, missing optional-route authorization, cycle, owner validation failure, or unjoined helper as `BLOCK` and report the exact missing condition.

## Step 5 - Select Runtime

33. Resolve the current repository runtime from the installed command context or `--runtime`.
34. If `--via runtime` is set, load the matching runtime adapter from `arcana/task-session/runtime-adapters/`.
35. For durable Arcanum runtime runs, use the `runtime-handoff` adapter and selected executor adapter such as `native-skill`, `codex-skill`, `claude-skill`, `copilot-instructions`, `dry-run`, or explicit legacy `codex-exec`.
36. If `--via runtime` is set and the session lacks a complete session-evidence handoff pack with Markdown plus JSON/index and strict coverage, return `BLOCK`.
37. If the adapter cannot safely produce a runtime command, return `BLOCK` with the exact missing field or setup action.

## Step 5A - Verify Routed Mutation Admission

37a. When the selected path claims routed or reusable mutation readiness,
assemble a mutation-admission request that binds the live task/SWU, exact
controlling artifact references, dependency frontier, material writes,
validation-owned execution outputs, their complete allowed-write union,
validation commands, lifecycle owner, authority class, and publication class.
Standalone non-mutating execution does not require this request.
37b. Include the material package and its producer receipt plus an exact
artifact reference to the producer-owned receipt schema. Run
`scripts/verify-mutation-readiness.py`; never copy or reimplement the Invoke
material-package validator inside Task Session.
37c. Run the consumer after scope, context, gates, and runtime resolution and
immediately before the first local write or mutating runtime handoff. It must
re-read every exact controlling artifact and dependency, bind the material
package to the producer receipt digest, and compare declared targets,
validation, ownership, authority, and publication against the live request.
Normalize and validate all three write lists, require material writes and
execution outputs to be disjoint, require their union to equal allowed writes,
and require package changes, target inventory, and producer validated paths to
equal only the material-write set.
37d. An absent, schema-invalid, stale, mismatched, expanded, or unclassified
input returns `BLOCK` before mutation. Rebuild the bounded context/material
handoff only through its owner; approval does not repair a failed binding.
37e. Persist the schema-valid mutation-admission receipt. Only
`admissionVerdict=admit` and `mutationReady=true` may cross this gate.
`not-applicable` is valid only for `standalone-nonmutating`.
37f. The admission receipt is execution evidence, not mutation, lifecycle,
promotion, or publication authority. Live done-criterion and post-mutation
validation in Step 7 remain mandatory.
37g. Mutation admission authorizes the ordered lifecycle only: apply admitted
material writes, run the declared validation that may create only predeclared
execution outputs, verify every declared output, then persist the terminal Task
Session receipt as the final write. Execution outputs are not required to exist
at admission time and may not expand the admitted union.

## Step 6 - Execute Task

38. Convert selected options, context-pack obligations, and checklist items into an ordered execution path.
39. If a runtime adapter is used, pass the handoff pack Markdown path and JSON/index path to the runtime handoff and preserve the Task Session synchronization obligations.
40. If running locally, make only the changes required for the task scope.
41. Avoid unrelated refactors or opportunistic cleanup unless they are necessary for completion.

## Step 7 - Validate Completion

42. Classify every done criterion and validation obligation as
    acceptance-critical or noncritical before evaluating completion.
    Unclassified done criteria and validation obligations are
    acceptance-critical.
43. Validate against every done criterion and context-pack obligation.
44. Run relevant checks based on touched assets.
45. If a runtime adapter performed execution, review the runtime result against the original work-pack contract, context pack, handoff pack/index, and any reported fallback exploration.
46. If Task Session or Continuation Router spawned, inherited, or requested subagents, verify the subagent lifecycle ledger before reporting success: every agent must be joined, closed, blocked with residue, timed out with residue and reroute, or handed off with reroute.
47. Treat hidden open agents, pending joins, pending closes, and unreported thread-cap failures as `BLOCK`, not as successful fallback exploration.
48. If acceptance-critical validation fails or cannot be run, attempt bounded
    recovery or a named accepted equivalent. Until the original validation or
    accepted equivalent passes, return `BLOCK`; recording a substitute does not
    itself satisfy the obligation.
48a. For routed or reusable mutation, reconcile paths created or modified by
     validation against `executionOutputs`. Block on an undeclared output, a
     missing declared output, or any write outside `allowedWrites`. Write the
     terminal Task Session receipt only after this reconciliation passes.
49. Return `FLAG` only for named noncritical residue that cannot falsify any
    done criterion. Unnamed residue or residue that can falsify a done criterion
    returns `BLOCK`.

## Step 8 - Synchronize Evidence

50. Assemble a `CloseoutSync` record from the terminal Task Session receipt:
    source result and receipt, declared target inventory, baseline identities or
    digests, typed deltas, validation commands, expected owner receipt, and the
    mechanically determined next route when one exists.
    Revalidate the Step 4 closeout preflight against the live targets; target
    drift invalidates the preflight and returns `BLOCK`.
51. Treat synchronization as required when the terminal receipt changes
    evidence, blocker, status, route, work-pack, checklist, traceability,
    Dispatch, registry, or declared Craft projection state. Treat it as
    `no-op` only when current artifacts already represent the terminal receipt.
52. Admit automatic closeout synchronization only when:
    - the route is exactly `invoke:refresh:apply-approved`;
    - every target is in the declared closeout inventory;
    - every delta is one of `evidence_added`, `blocker_opened`,
      `blocker_resolved`, `status_changed`, or `route_changed`;
    - source receipt, target baselines, validation commands, and expected owner
      receipt are present;
    - any successor selection is the one unique, already declared,
      dependency-ready successor; and
    - the delta does not execute implementation or another task, change
      authority, promote, publish, deploy, perform destructive cleanup, accept
      policy/cost/risk, or touch unrelated targets.
53. When Step 52 passes, derive an exact closeout authorization bound to the
    route tuple, source receipt, target inventory, baseline identities or
    digests, delta classes, and validation surface. This is the current Task
    Session's authorization for closeout bookkeeping only; do not ask for a
    second user approval.
54. Dispatch the closeout authorization through `continuation-router`.
    Continuation Router must run the Invoke Refresh owner's strict
    `apply-approved` gates, dispatch exactly one owner hop, and join a separate
    validated owner receipt. Task Session never edits the owner's targets
    directly.
55. Update the task result with separate execution and closeout outcomes.
    Preserve the execution result even if synchronization blocks. A required
    closeout with missing inputs, target drift, ambiguous successor, owner
    validation failure, cycle, or unjoined owner receipt makes the Task Session
    result `BLOCK`.
56. If the task belongs to a spell or sigil lifecycle, preserve experiment harness status and report whether reusable-behavior validation is updated, pending, blocked, or not applicable.
57. Return the synchronized next route but never execute the next task/SWU as
    part of closeout.
58. After a joined closeout owner receipt or receipt-backed no-op, emit or
    update one repository-local Task Session continuity cursor. Prefer the
    native runtime session id; when unavailable, use a stable scope-derived id
    so repeated calls in the same work-pack scope update one cursor. The
    cursor records the scope root, work pack, source SWU/result/receipt,
    closeout owner receipt, returned next route/SWU, and blocker fingerprint.
    It must conform to `continuity.schema.json` and must never rewrite work-pack
    authority.
59. If no synchronization is needed, report the receipt-backed no-op reason.

## Step 9 - Report

60. Return a compact task-session report with resolution mode/source,
    candidates considered, session recovery status, context pack, handoff pack
    artifact, strict coverage, fallback-search status, decisions and their
    classifications, runtime adapter, gate verdict, execution result,
    closeout-sync status and authorization, closeout owner receipt, continuity
    cursor, continuation handoff, probable non-closeout routes, optional
    continuation status, optional owner receipt, returned next route, subagent
    closeout, files updated, validation criticality and outcomes, experiment
    harness status, and remaining follow-up.
61. Report subagent closeout as `n/a`, `pass`, `flag`, or `block`; when it is not `n/a`, include counts for spawned, joined, closed, blocked, timed-out, handed-off, open, plus residue and reroute paths.
62. When the result is `BLOCK` because a decision is required, append a `Decision Gate Result` section that names the target scope, lists the blocker question, presents 2-4 concrete options with trade-offs, records the recommended option if one exists, and points to the decision artifact path.
</process>

<authority-rule>
No consequential mutation proceeds inside the selected task when its gate status is `BLOCK`. Required closeout synchronization is not ambient mutation authority: it is one exact, receipt-bound `invoke:refresh:apply-approved` owner hop over the declared synchronization inventory and allowed delta classes. A separate optional owner route may run only through Continuation Router with explicit authorization and the owner's own gates. Every mutation and receipt remain attributed to its owner. Completion state may only be updated when supporting evidence exists.
</authority-rule>

<observability>
For reusable use, emit a post-run invocation signal using the repository-local observability package when available.

Recommended signals:

- task reference,
- resolution mode and source,
- session recovery status,
- continuity cursor path,
- candidate count, ambiguity count, stale exclusions, and cross-scope rejects,
- context pack status and source count,
- handoff pack markdown and JSON/index paths when runtime delegation is used,
- strict coverage status,
- fallback exploration/search status,
- decision count,
- gate result,
- subagent closeout result and unresolved agent count when delegated execution is present,
- files changed count,
- validation commands,
- validation result,
- completion status,
- follow-up count,
- dry-run or auto mode usage.
- selected runtime and adapter when used,
- runtime handoff command shape or blocked fallback.
- experiment harness status when the task belongs to spell or sigil lifecycle work.
- continuation handoff path, blocker fingerprint, candidate count, probable route tuples, selection and authorization status,
- continuation dispatch status, owner receipt, returned next route, and repeated-route or cycle detection.
- mutation-admission mode, verdict, receipt path, request/package/producer
  schema digests, bound task/SWU, controlling paths, dependency IDs, allowed
  writes, validation commands, boundary classes, live-validation requirement,
  and block reasons.
- closeout-sync required/no-op status, source receipt, target count, baseline
  status, delta classes, derived authorization identity, owner dispatch and
  receipt, validation result, and synchronized next route.
</observability>

<quality-bar>
A successful execution of this sigil must:

- route explicit series intent to `task-session-until-blocker` without
  executing more than one SWU inside Task Session,
- resolve exactly one task scope,
- make a no-argument invocation resume at most one uniquely nearest,
  evidence-backed SWU,
- recover from missing conversational context only through runtime-supplied
  current-session evidence or repository-local continuity,
- revalidate every cursor-selected candidate against the live work pack,
- resolve exactly one work-pack task or SWU when the input is a work-pack,
- build a bounded context pack before decisions, gates, runtime selection, or mutation,
- require strict handoff-pack coverage before `--via runtime` delegation,
- block when required source context is missing, contradictory, or too weak to check constraints,
- expose meaningful implementation trade-offs,
- auto-select only choices explicitly classified both nonconsequential and reversible,
- stop before mutation when blockers remain,
- emit an actionable machine-readable continuation handoff for a terminal result when owner routing evidence exists,
- expose one to three probable routes before any continuation dispatch,
- dispatch at most one exactly authorized continuation route and preserve the selected owner's gates,
- prevent unchanged blocked Task Session re-entry and recursive continuation,
- run `decision-gate` before reporting blocker-level human approval, destructive cleanup, rollout, or policy choices,
- keep runtime delegation behind an explicit adapter boundary,
- require a current producer-schema-validated, digest-bound mutation-admission
  receipt immediately before routed or reusable mutation,
- bind admission to the live task/SWU, controlling artifacts, dependency
  frontier, allowed writes, validation surface, and authority/publication
  class,
- leave standalone non-mutating execution outside the receipt requirement,
- retain live post-mutation validation after admission,
- block success when delegated subagents remain open, pending, hidden, or only implicitly abandoned,
- keep edits within the declared task scope,
- validate all available done criteria,
- classify validation obligations and block unmet acceptance-critical validation unless a named accepted equivalent passes,
- reserve `FLAG` for named noncritical residue that cannot falsify a done criterion,
- distinguish task/SWU execution evidence from reusable-behavior experiment evidence,
- synchronize required completion and blocker evidence before returning,
- fail before implementation mutation when required closeout inputs are absent,
  ambiguous, stale, expanded, or forbidden,
- derive closeout authorization only for the exact receipt-bound target
  inventory, admitted delta classes, and validation surface,
- join a validated owner receipt for required closeout synchronization,
- block closeout when synchronization inputs, baselines, owner validation, or
  lifecycle joins are incomplete,
- return but never execute the next task/SWU selected by closeout,
- emit a schema-valid continuity cursor after joined closeout or a
  receipt-backed no-op,
- return a report that a reviewer can audit without reconstructing the full session.
</quality-bar>

<anti-patterns>
Avoid:

- using the sigil for many unrelated tasks at once,
- silently narrowing explicit `all`, `one go`, or `until blocker` series intent
  to one SWU instead of routing to the outer-loop owner,
- emitting one Task Session receipt that claims execution of several SWUs,
- choosing the globally latest work pack, telemetry row, or cursor,
- treating fuzzy relevance or cross-project recency as “nearest,”
- assuming compacted conversational tokens remain readable,
- treating a continuity cursor as readiness or completion authority,
- treating an Invoke material receipt alone as Task Session admission without
  binding it to the live task/SWU and strict execution controls,
- copying Invoke material-package validity logic into Task Session,
- reusing a mutation-admission receipt after any controlling artifact,
  dependency, write scope, validation command, owner, authority, or publication
  binding changes,
- treating mutation admission as a substitute for live validation or as
  lifecycle authority,
- falling through to a lower-priority candidate when the selected evidence is
  stale or contradictory,
- executing from the task file alone when source links, architecture, or work-pack context can change the correct implementation choice,
- delegating through `--via runtime` without a complete session-evidence handoff pack and JSON/index,
- treating `--auto` as permission to guess consequential user choices,
- treating a recommendation, confidence judgment, or “clearly safe” label as an automatic-choice classification,
- changing files outside the task scope without recording why,
- marking completion without evidence,
- discovering a predictable missing closeout inventory, baseline, validation,
  or expected owner receipt only after implementation writes,
- skipping validation because the edit looks small,
- hiding failed checks inside a success report,
- returning `FLAG` for failed or unavailable acceptance-critical validation,
- returning `FLAG` for unnamed residue or residue that can falsify a done criterion,
- letting synchronization updates rewrite unrelated planning or status history.
- ending a terminal task with a separate proposal-only Refresh or apply-approval
  request when the required closeout delta is deterministic and satisfies the
  bounded closeout-sync policy.
- ending with a vague approval request when a blocker-level decision could be presented as concrete options with context.
- hardcoding Codex as the only possible runtime,
- treating a generated runtime handoff as completed work before evidence returns.
- reporting AFK research as successful while subagent joins, closes, residues, or reroutes are unproven.
- treating free-text `next_route` as mutation approval.
- re-entering Task Session with the same blocker fingerprint and unchanged controlling evidence.
- performing Invoke Refresh, Decision Gate, Goal, or another owner's mutation directly inside Task Session instead of dispatching and joining the owner.
- deriving closeout authorization for implementation, another task, authority,
  promotion, publication, deployment, destructive cleanup, policy/cost/risk
  acceptance, an ambiguous successor, or an undeclared target.
- recursively executing the next route returned by a continuation owner.
</anti-patterns>

<output-contract>
Return:

```markdown
## Task Session Result

- Task: <task-reference>
- Series intent: none | routed to task-session-until-blocker | blocked, <handoff path or reason>
- Resolution mode: explicit | resume-nearest | list-nearest
- Resolution source: explicit-source | visible-session-context | exact-session-cursor | cwd-ancestor-work-pack | scope-matched-continuity
- Session recovery: visible | durable-cursor | cwd-work-pack | scoped-continuity | unavailable
- Resolution candidates: <ranked count, rejected stale/cross-scope count, ambiguity | none>
- Result: PASS | BLOCK | FLAG
- Execution result: PASS | BLOCK | FLAG
- Decisions: <resolved count and summary>
- Decision classifications: <consequence and reversibility per automatic choice | none>
- Context pack: <source count and controlling constraints | blocked reason>
- Handoff pack: <markdown path and JSON/index path | none | blocked reason>
- Strict coverage: pass | block | n/a
- Fallback search: none | named gaps only | blocked
- Runtime: <runtime id or local>
- Adapter: <adapter id or none>
- Gate verdict: <summary>
- Closeout sync: pass | no-op | block
- Closeout authorization: derived | not-needed | not-derivable, <exact bound tuple and scope identity | reason>
- Closeout owner receipt: <path | none>
- Closeout validation: <owner checks and join result | none>
- Continuity cursor: <path | none | blocked reason>
- Continuation handoff: <path or inline id | none>
- Blocker fingerprint: <stable identifier | none>
- Probable routes: <ranked 1-3 capability/mode tuples | none>
- Optional continuation: not-requested | not-authorized | ambiguous | blocked | completed | flagged
- Continuation owner receipt: <path | none>
- Returned next route: <capability>:<mode> <target | none>
- Subagent closeout: n/a | pass | flag | block, <spawned/joined/closed/blocked/timed_out/handed_off/open counts, residue, reroute>
- Files updated: <paths or none>
- Validation: <commands and results>
- Validation criticality: <acceptance-critical/noncritical classification, accepted equivalents, and residue>
- Experiment harness: pass | flag | block | not_run | not_applicable
- Synchronized records: <paths or none>
- Follow-up: <items or none>

## Decision Gate Result

- Target scope: <scope | n/a>
- Result: PASS | BLOCK | n/a
- Decisions resolved: <count>
- Blockers remaining: <count>
- Decision artifact: <path | none>
- Options: <numbered option cards with benefit, cost/risk, when to choose, downstream impact | none>
- Recommendation: <recommended option and rationale | none>
- Next step: <proceed | ask remaining decision | stop>
```
</output-contract>
