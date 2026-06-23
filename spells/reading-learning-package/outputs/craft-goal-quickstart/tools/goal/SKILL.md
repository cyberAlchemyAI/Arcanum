---
name: goal
description: "`goal` drives a Craft-backed work graph through an autonomous, fail-closed control loop. It reads the current frontier, classifies each node by risk, routes work to the owning capability, gates closure with audit evidence, stages ledger deltas, and promotes only behind an explicit approval token."
surface_kind: generated-native-runtime-package
runtime: codex
canonical_source: spells/goal/README.md
alias_of: null
generated_by: tools/bootstrap_arcanum.sh --profile
mutation_policy: regenerate-from-canonical-source
---

# Goal

- Status: registered reusable spell
- Canonical id: `goal`
- Aliases: `autonomous-dag-goal-loop`, `dag-goal-loop`
- Lifecycle owner: `spellcraft`

## Purpose

`goal` drives a Craft-backed work graph through an autonomous, fail-closed
control loop. It reads the current frontier, classifies each node by risk,
routes work to the owning capability, gates closure with audit evidence, stages
ledger deltas, and promotes only behind an explicit approval token.

The spell is a router. It does not claim ownership of delegated sigil behavior,
does not execute protected work directly, and does not mutate the source ledger
without an approved staged proposal.

## Trigger Conditions

| Trigger | Route |
| --- | --- |
| A Craft scope has open next moves, gaps, blockers, or not-started SWUs and the user asks Codex to continue toward a goal. | Read the frontier, classify risk, route eligible nodes, and stage deltas. |
| A work node requires source mutation, shell/network/CI, publication, commit/push, or ledger promotion. | Stop before mutation and request an explicit approval path. |
| The frontier appears complete and gap discovery is enabled. | Run a bounded gap-discovery round and queue proposed next slices, not active ledger changes. |
| A staged batch is ready to apply. | Stop with a framed batch summary and wait for an approval token. |

## Required Capabilities

| Capability | Required For | Boundary |
| --- | --- | --- |
| `arcana/craft` | Read frontier state, validate ledger state, and apply approved ledger batches. | The spell may stage proposals; active ledger mutation remains approval-gated. |
| `formulae/dispatch-spec` | Validate per-node owner, technique, and receipt routes. | The spell assembles routes but does not redefine dispatch techniques. |
| `spells/observed-invocation-loop` | Wrap delegated node execution in an observation envelope. | Execution receipts remain separate from reusable spell validation evidence. |
| `arcana/decision-gate` | Record durable approval or blocker decisions. | Human approval remains explicit and reviewable. |
| `arcana/task-session` | Execute one bounded node or SWU with done criteria and validation. | Task Session owns bounded execution evidence for the selected node. |
| `formulae/observability-setup` and `arcana/signal-observer` | Emit spell-level telemetry and post-run signals. | Observability is evidence, not promotion by itself. |

## Optional Capabilities

| Capability | Use When | Boundary |
| --- | --- | --- |
| `arcana/robot-talks` | An approved medium-or-higher-risk audit lane needs adversarial review. | Not spawned automatically; requires route authorization and receipts. |
| `arcana/refine` | A named gap needs repair or rescoping before execution. | Used for the named gap only. |
| `arcana/distill` | A broad or tangled node needs reduction to a smallest coherent slice. | Produces residue or slice guidance, not direct ledger mutation. |
| `experiment-harness` | The spell is being validated for reusable promotion. | Promotion evidence is separate from task-session runtime evidence. |

## Prerequisites

- A Craft ledger or equivalent scope state is available.
- The user has named a goal or selected a Craft context.
- The runtime can distinguish read-only analysis from mutation, publication, and
  promotion operations.
- A public `decision-profile.schema` exists in this spell package.
- Any filled decision profile is supplied by the consuming repository at runtime
  and is not part of this public spell package.

## Shared State

| State | Owner | Updated By | Consumed By |
| --- | --- | --- | --- |
| Craft ledger | `arcana/craft` | Approved craft operations | Frontier reader, staging review, promotion gate |
| Frontier snapshot | `goal` | Read-frontier phase | Risk classifier and owner selector |
| Dispatch route | `formulae/dispatch-spec` | Owner and technique selection | Dispatch phase and receipt join |
| Staged deltas | `goal` proposal state, applied by `arcana/craft` after approval | Stage-delta phase | Batch approval and promotion |
| Approval record | `arcana/decision-gate` | Approval gate | Promotion phase and audit trail |
| Runtime receipts | Delegated owner capability | Dispatched node execution | Audit gate and close decision |
| Spell telemetry | Observability capabilities | Each round and final report | Reflection, validation, and later promotion review |

## Decision Profile

`goal` accepts an optional decision profile that parameterizes risk thresholds,
approval defaults, slice sizing, owner boundaries, gap-filling style, technique
preferences, and anti-pattern stops. The public package ships only
`decision-profile.schema` and neutral defaults. A filled profile is private
runtime data owned by the consuming repository.

If no filled profile is supplied, the spell uses the neutral defaults from the
schema and remains fail-closed: unknown risk, unknown authority, or unclear write
permission stops before mutation.

## Execution Phases

| Phase | Entry Criteria | Exit Criteria | Failure Behavior |
| --- | --- | --- | --- |
| Goal bind | Goal intent and Craft scope are present. | Scope, source ledger, and validation surface are identified. | Stop if scope or source authority is ambiguous. |
| Read frontier | Scope is bound. | Open next moves, blockers, gaps, and candidate SWUs are listed. | Stop if frontier cannot be read safely. |
| Classify risk | Frontier nodes are available. | Every node has a risk tier; unknown resolves to protected. | Stop on protected or unknown work that lacks approval. |
| Select owner and technique | A node is eligible for routing. | Dispatch route names owner, technique, inputs, expected receipt, and gate. | Stop if route validation fails. |
| Dispatch and receipt join | Route passes. | Delegated owner returns a terminal receipt or a recorded block. | Stop if a delegated lane remains open or unjoined. |
| Audit gate | Receipt exists. | Completion evidence is accepted, flagged, or vetoed. | Stop on audit veto or missing done evidence. |
| Stage delta | Audit accepts progress. | Proposed ledger delta and framed diff are staged. | Stop if staging would mutate active ledger rows directly. |
| Batch approval | One or more staged deltas exist. | Approval token and durable decision record exist, or residue is recorded. | Stop until approval exists; reject or defer on denial. |
| Promote | Approval exists. | Batch applies through Craft validation and records the result. | Block on validation failure; never silently partially apply. |
| Gap discovery | Frontier is empty and module is enabled. | New gaps are deduped into a next-slice proposal queue or no new work is found. | Stop at round budget or duplicate loop. |

## Control Spine

1. Read the Craft frontier.
2. Classify each node by risk with an allowlist and default-deny fallback.
3. Select owner and technique through a Dispatch Spec route.
4. Dispatch the node through the owner and collect an AFK-safe receipt.
5. Run audit and review gates before accepting progress.
6. Stage the ledger delta as a proposal, never as a direct active-row mutation.
7. Promote only after an explicit approval token and durable decision record.

Cross-cutting guards run each round: stop/escalation, budget and proportionality,
decision-profile policy, source-authority reconcile, and subagent closeout.

## Modules

### Gap Discovery

Runs only after the active frontier is empty and the caller opts in. It mines
recorded residue and evidence for untracked work, dedupes by `(kind, target)`,
terminates after a configured dry round count, and queues proposals for a later
slice. It does not reopen the active frontier by itself.

### Proportionality Guard

Tracks turn, token, spawn, and no-progress budgets. When an audit passes without
changing the verdict, the spell records a down-route opportunity and selects a
cheaper technique on the next comparable node. The guard stops before exceeding
the budget ceiling.

### Read-Only Boundary

Delegated owners receive read-only Craft context unless an approval path grants a
staged proposal lane. Any direct ledger write attempt becomes a proposed delta or
a block.

## Handoff Artifacts

| Artifact | Producer | Consumer | Purpose |
| --- | --- | --- | --- |
| Frontier snapshot | `goal` read-frontier phase | Risk classifier and selector | Freezes the candidate node set for one round. |
| Dispatch route | `goal` plus `formulae/dispatch-spec` | Delegated owner and audit gate | Names owner, technique, inputs, receipt expectations, and fallback. |
| Execution receipt | Delegated owner capability | Audit gate and Task Session review | Proves terminal closeout or records residue. |
| Staged delta | `goal` stage-delta phase | Batch approval | Holds proposed ledger changes before active mutation. |
| Framed batch diff | `goal` batch approval phase | Decision Gate and user approval | Shows exactly what would be promoted. |
| Decision record | `arcana/decision-gate` | Promotion phase and audit trail | Durable approval or rejection evidence. |
| Spell telemetry signal | Observability capabilities | Spellcraft, reflection, and Experiment Harness | Records runtime behavior without implying promotion. |

## Gates

| Gate | Required Evidence | Result |
| --- | --- | --- |
| Source authority | Craft ledger or selected context is identified. | pass/block |
| Risk classification | Every routed node has a tier; unknown becomes protected. | pass/block |
| Route validation | Dispatch Spec route names owner, technique, receipt, gate, and fallback. | pass/block |
| Read-only boundary | Delegated owner cannot mutate active ledger rows directly. | pass/block |
| Receipt closeout | Every dispatched lane is terminal: closed, blocked with residue, timed out with reroute, or handed off. | pass/block |
| Audit veto | Review evidence is present and veto overrides apparent success. | pass/flag/block |
| Stage review | Proposed delta has a framed diff and no active-ledger direct write. | pass/block |
| Approval token | Batch has an explicit approval and durable decision record before apply. | pass/block |
| Budget ceiling | Round, spawn, and no-progress budgets remain under ceiling. | pass/stop |
| Promotion readiness | Experiment Harness evidence proves reusable behavior before draft promotion. | pass/block |

## Failure Policy

- Stop when risk is protected, unknown, or outside the allowlist.
- Stop when a blocking decision, approval token, or human gate is missing.
- Stop when audit vetoes progress or a delegated lane lacks terminal closeout.
- Stop before direct ledger mutation, publication, commit, push, PR creation, or
  parent gitlink movement unless that exact operation is approved.
- Stop when a filled decision profile would need to be copied into public
  artifacts.
- Block promotion until Experiment Harness proves the reusable spine.

Each stop reports `stop_reason`, `escalation_context`, staged-delta state,
evidence used, and the next route.

## Local Customization

- Library spell root: `arcanum/spells/goal/`.
- This `README.md` is the source contract for the reusable spell.
- Generated native runtime surfaces, including any `SKILL.md`, are produced by
  the runtime installer and are not hand-authored here.
- Public profile shape: `decision-profile.schema`.
- Public artifact schemas: `schemas/*.schema.json`.
- Filled decision profiles remain private consuming-repository runtime data.

## Observability

When repository observability is installed, emit one spell-level signal per
round and one final signal per goal.

| Signal Field | Meaning |
| --- | --- |
| `spell` | Always `goal`. |
| `goal_context_id` | Bound Craft context or selected goal handle. |
| `round_index` | Control-loop round number. |
| `frontier_size` | Frontier count at round start. |
| `nodes_classified` | Counts by risk tier. |
| `nodes_dispatched` | Count of delegated nodes. |
| `audit_verdicts` | Counts of pass, flag, block, and veto. |
| `downroutes` | Count and reason for cheaper-technique routing. |
| `staged_deltas` | Proposed deltas created this round. |
| `batch_promotions` | Applied, rejected, and held batches. |
| `stop_reason` | Stop enum or `none`. |
| `budget_spent` | Turns, spawns, tokens, and configured ceiling. |
| `gap_discovery` | Rounds run and new proposals. |
| `decision_profile_ref` | Public-safe profile reference or `neutral-default`. |
| `subagent_closeout` | Spawned, joined, closed, blocked, timed out, handed off, and open counts. |

## Output Contract

```markdown
## Goal Loop Result

- Spell: goal
- Goal: <intent>
- Result: PASS | STOP | BLOCK | FLAG
- Rounds: <count>
- Decision profile: <ref | neutral-default>
- Frontier: <start size -> end size>
- Risk tiers seen: T0:<n> T1:<n> T2:<n> T3:<n>
- Dispatched: <count>
- Audit: pass <n> | flag <n> | block <n> | veto <n>
- Down-routes: <count and reasons>
- Staged deltas: <count>
- Promoted batches: applied <n> | rejected <n> | held <n>
- Stop reason: t3-node | open-decision | budget-ceiling | audit-veto | batch-ready | source-authority | none
- Budget: turns <n> / spawns <n> / tokens <n> (ceiling <value>)
- Gap discovery: rounds <n> | new proposals <n>
- Subagent closeout: spawned <n> | joined <n> | closed <n> | blocked <n> | timed out <n> | handed off <n> | open <n>
- Telemetry: recorded | skipped
- Extra sources: <none or list with named gap>
- Next route: continue | operator-approval | decision-gate | task-session | experiment-harness | none
```

## Validation Examples

| Example | Expected Result |
| --- | --- |
| Read-only authoring node with clear owner and validation. | Route through owner, audit, and stage a proposed delta. |
| Unknown shell or network action. | Stop as protected risk. |
| Delegated owner attempts direct ledger mutation. | Block direct write and convert to staged proposal or residue. |
| Batch ready without approval token. | Stop with framed diff and approval request. |
| Frontier empty with gap discovery disabled. | Return PASS or STOP with no new proposals. |
| Promotion requested without Experiment Harness evidence. | Block promotion. |

## Registry Readiness

Registry status: registered. Spellcraft review and Experiment Harness evidence
prove that the fail-closed spine cannot be bypassed, gap discovery terminates,
and approvals emit durable decision records. Generated runtime surfaces remain
installer-owned and consuming-repository-local.
