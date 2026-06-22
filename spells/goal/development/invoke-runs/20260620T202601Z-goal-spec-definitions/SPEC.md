---
artifact_id: GOAL-SPEC-001
artifact_type: invoke-define-spec
target: arcanum/spells/goal
invoke_mode: define
status: draft
owner: spellcraft
source_contract: ../../README.md
local_definitions: DEFINITIONS.md
canonical_definition_updates:
  - DEF-ARC-GOAL-SPELL
  - DEF-ARC-STAGED-DELTA
  - DEF-ARC-APPROVAL-TOKEN
discovery_waiver_reason: The goal spell already has a source contract, Craft ledger, and Codex Goal handoff pack; this run creates the spec and definitions baseline from that bounded evidence instead of running broader discovery.
created_at: 2026-06-20
---

# Goal Spell Spec

## Intent

Define the public specification baseline for the `goal` spell. The spell drives
a Craft-backed work graph through a fail-closed control loop: read frontier,
classify risk, select owner and technique, dispatch, audit, stage deltas, and
promote only after explicit approval.

This spec is descriptive and contract-aligned. It does not implement runtime
logic, promote the spell, generate `SKILL.md`, publish, commit, push, or move
the parent gitlink.

## Source Evidence

| Source | Role |
| --- | --- |
| `arcanum/spells/goal/README.md` | Public source contract for the draft spell. |
| `arcanum/spells/goal/decision-profile.schema` | Public decision-profile shape and neutral defaults. |
| `arcanum/spells/goal/.craft/ledger.yml` | Craft source of truth for the goal spell build state. |
| `arcanum/spells/goal/CRAFT.md` | Human-readable Craft view of build state. |

Bounded execution evidence was used to author the first source contract, but it
is intentionally not a public spell dependency and is not referenced by path
here.

## Scope

In scope:

- Public specification for `arcanum/spells/goal`.
- Local definitions for goal-spell vocabulary.
- Canonical promotion of reusable Arcanum-wide terms.
- Validation expectations for source contract, schema, no-leak boundary, and
  future reusable-behavior proof.

Out of scope:

- Runtime implementation of all `SWU-GOAL-*` work.
- Generated native runtime packages.
- Filled private decision profiles.
- Direct Craft ledger mutation or promotion.
- Experiment Harness promotion evidence.
- Publication, commit, push, PR, or parent gitlink movement.

## Concept Registry

| Concept | ID | Type | Authority |
| --- | --- | --- | --- |
| Goal spell | `DEF-ARC-GOAL-SPELL` | Workflow | Canonical Arcanum definition. |
| Craft frontier | `GOAL-CPT-FRONTIER` | StateMachine | Local spell concept. |
| Risk tier | `GOAL-CPT-RISK-TIER` | Enum | Local spell concept. |
| Dispatch route | `GOAL-CPT-DISPATCH-ROUTE` | Workflow | Local use of `formulae/dispatch-spec`. |
| Execution receipt | `GOAL-CPT-EXECUTION-RECEIPT` | Event | Local spell concept. |
| Staged delta | `DEF-ARC-STAGED-DELTA` | Event | Canonical Arcanum definition. |
| Approval token | `DEF-ARC-APPROVAL-TOKEN` | Event | Canonical Arcanum definition. |
| Decision profile | `GOAL-CPT-DECISION-PROFILE` | Policy | Local spell concept with public schema. |
| Gap discovery | `GOAL-CPT-GAP-DISCOVERY` | Workflow | Local spell module. |
| Proportionality guard | `GOAL-CPT-PROPORTIONALITY-GUARD` | Guard | Local spell module. |

## Required Behavior

### R1 - Bind Goal Scope

The spell must bind a user goal to a Craft scope or equivalent state source
before reading work. Ambiguous scope blocks before dispatch.

Evidence:

- Source authority gate in `README.md`.
- Bound context recorded in the output contract.

### R2 - Read Frontier

The spell must read open next moves, blockers, gaps, and candidate SWUs without
mutating the source ledger.

Evidence:

- `frontier_size` observability field.
- Frontier snapshot handoff artifact.

### R3 - Classify Risk

Every candidate node must receive a risk tier before routing. Unknown or
protected work defaults to a stop condition.

Evidence:

- `nodes_classified` observability field.
- Risk classification gate.

### R4 - Select Owner And Technique

Each routable node must name an owner capability, technique, input set,
expected receipt, and fallback route through a Dispatch Spec-compatible route.

Evidence:

- Dispatch route handoff artifact.
- Route validation gate.

### R5 - Dispatch With Terminal Receipt

Delegated work must return a terminal receipt before audit: closed, blocked with
residue, timed out with reroute, or handed off with reroute.

Evidence:

- Execution receipt handoff artifact.
- Receipt closeout gate.

### R6 - Audit Before Close

The spell must run review/audit before accepting progress. Audit veto overrides
apparent success.

Evidence:

- Audit gate result.
- `audit_verdicts` observability field.

### R7 - Stage Before Promote

Progress that changes the Craft source of truth must first become a staged
delta with a framed diff. Direct active-ledger mutation is not allowed.

Evidence:

- Staged delta artifact.
- Stage review gate.

### R8 - Approve Before Apply

Applying staged deltas requires an explicit approval token and durable decision
record. Without approval, the batch is held, rejected, or deferred.

Evidence:

- Approval token gate.
- Decision record artifact.

### R9 - Keep Public/Private Boundary

Public spell files may ship `decision-profile.schema` and neutral defaults only.
Filled decision profiles are consuming-repository runtime data and must not be
copied into `arcanum`.

Evidence:

- Public-boundary validation scan.
- Decision profile section in `README.md`.

### R10 - Keep Promotion Gated

The spell remains draft until Experiment Harness evidence proves reusable
behavior: fail-closed boundary, gap-discovery termination, and durable approval
records.

Evidence:

- Promotion readiness gate.
- Registry readiness section in `README.md`.

## State Model

| State | Description | Exit |
| --- | --- | --- |
| `unbound` | Goal intent exists but source authority is not selected. | Bind scope or block. |
| `frontier-read` | Candidate work is known for one round. | Classify risk. |
| `routable` | Node has acceptable risk and owner route. | Dispatch. |
| `protected-stop` | Node is protected, unknown, or requires approval. | Decision Gate or explicit approval path. |
| `receipt-ready` | Delegated work has terminal receipt. | Audit. |
| `delta-staged` | Proposed source change is staged with framed diff. | Batch approval. |
| `batch-ready` | Staged deltas are grouped for review. | Approval token or deferral. |
| `promoted` | Approved batch applied through Craft validation. | Continue or finish. |
| `blocked` | A hard gate failed. | Report blocker and next input. |

## Interfaces

| Interface | Producer | Consumer | Required Shape |
| --- | --- | --- | --- |
| Frontier snapshot | `goal` | Risk classifier | Context id, source ref, nodes, blockers, gaps, timestamp. |
| Dispatch route | `goal` + `dispatch-spec` | Delegated owner | Owner, technique, inputs, receipt fields, fallback. |
| Execution receipt | Delegated owner | Audit gate | Status, evidence, files touched, validation, residue. |
| Staged delta | `goal` | Batch approval | Target, proposed change, framed diff, validation expectation. |
| Approval token | Human or decision gate | Promotion phase | Batch id, decision record ref, approval state. |
| Decision profile | Consuming repo runtime | Risk and selector policy | Must validate against `decision-profile.schema` if supplied. |

## Events

| Event | Emitted When |
| --- | --- |
| `goal_bound` | Scope authority is selected. |
| `frontier_read` | Candidate work is listed. |
| `risk_classified` | All candidates have tiers. |
| `node_dispatched` | A route is sent to an owner. |
| `receipt_joined` | A terminal receipt returns. |
| `audit_vetoed` | Review blocks progress. |
| `delta_staged` | A proposed delta is staged. |
| `batch_ready` | Staged deltas await approval. |
| `batch_promoted` | Approved batch applies through Craft. |
| `goal_stopped` | A stop condition is reached. |

## Validation Matrix

| Check | Command Or Evidence | Expected Result |
| --- | --- | --- |
| Source contract exists | `test -f arcanum/spells/goal/README.md` | pass |
| Public schema parses | `python3 -m json.tool arcanum/spells/goal/decision-profile.schema` | pass |
| Spec exists | `test -f arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/SPEC.md` | pass |
| Definitions exist | `test -f arcanum/spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md` | pass |
| Canonical definitions synced | Definition IDs present in `arcanum/definitions/DEFINITIONS.md` and `DEFINITIONS-INDEX.md` | pass |
| Public boundary | Scan public goal and definition files for private paths, filled profile identifiers, and private corpus references | no hits |
| Diff hygiene | `git -C arcanum diff --check -- spells/goal definitions` | pass |

## Gaps And Follow-Up

| Gap | Owner | Route |
| --- | --- | --- |
| Runtime implementation SWUs remain incomplete. | `task-session` | Execute selected `SWU-GOAL-*` units after this spec baseline is accepted. |
| Reusable behavior proof is absent. | `experiment-harness` | Create low/medium/high validation scenarios before promotion. |
| Generated runtime package is absent. | runtime installer | Generate only after source contract validation. |
| ADO design artifact move remains deferred. | operator approval | Move only scrubbed public-safe design notes when explicitly approved. |

## Next Route

`spellcraft validate` should review the source contract, this spec, local
definitions, and canonical definition updates. Runtime implementation remains a
later Task Session route.
