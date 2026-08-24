---
id: inventory-recall-context
type: spell
status: candidate
version: 0.1.0-candidate
aliases: []
authority_effect: none
---

# Inventory Recall Context

`inventory-recall-context` is a candidate read-only spell for one explicit,
task-local recall turn. It composes Inventory discovery with Context Builder
packaging, verifies every selected source against current repository evidence,
and denies context injection unless every required gate passes.

The spell is accepted for candidate development only. It is not registered,
installed, generated, promoted, runtime-proven, or available as automatic or
durable agent memory.

## Purpose

Convert one bounded `RecallRequest` into either:

- a strict lean `RecallContextPack` that may enter the current task context; or
- a fail-closed `RecallReceipt` that explains why no pack may be injected.

Inventory remains a non-authority discovery/read-model owner. Current
owner-controlled source bytes remain authoritative for the claims they carry.

## Trigger

Use this spell only when an agent or operator explicitly asks for repository
context relevant to one current task and the required evidence is expected to
exist in an Inventory index.

Do not trigger it automatically on prompts, sessions, repository changes, or
post-run attachment events.

## Required sigils

- `inventory`
  - operation: `lookup`
  - obligation: validate the current machine index and return selector-level
    matches with source bindings
- `context-builder`
  - operation: `lean --strict --emit both --handoff runtime`
  - obligation: compile current selected evidence into Markdown plus a machine
    index with complete obligation coverage and a bounded context budget

## Optional sigils

- `signal-observer`: derive non-authority behavior signals after a completed
  recall turn.
- `decision-gate`: route a contradiction or ownership decision that current
  source verification cannot settle.

Experiment Harness is a lifecycle prerequisite for this reusable candidate;
it is not a runtime child invocation.

## Prerequisites

- an explicit task-local request ID and objective;
- a resolvable Inventory target with a current validator receipt;
- an allowlisted repository root and bounded source scope;
- explicit obligations and a positive lean context budget;
- a writable run-local evidence location for the receipt only;
- no requested writeback, automatic hook, cache, or durable model-memory side
  effect.

Missing prerequisites produce a denied receipt. They never cause the spell to
broaden scope or reuse older prose.

## Shared state

| Record | Required meaning |
| --- | --- |
| `RecallRequest` | request ID, task objective, lookup terms, obligations, source scope, and budget |
| `InventoryLookupPacket` | validated index binding, lookup readiness, selected matches, source refs, and diagnostics |
| `VerifiedSourceRef[]` | current path/selector/digest observations and one classified source state per selected ref |
| `RecallContextPack` | strict lean Markdown and JSON/index outputs with obligation coverage, source bindings, and measured budget |
| `RecallReceipt` | request binding, stage outcomes, final decision, reason codes, digests, warnings, and optional pack locator |

`injectionAllowed` is derived. Callers cannot set or override it.

## Phases

### 1. Request intake

Validate the request identity, task objective, lookup terms, obligations,
allowlisted source scope, and budget. On invalid or unbounded input, emit a
denied receipt and stop.

### 2. Index-bound lookup

Invoke Inventory `lookup`. Require a validator result bound to the current
`index.json` bytes. A blocked or stale index denies injection before source
selection.

### 3. Current-source verification

Resolve every selected path and selector within the allowed repository root.
Bind observed bytes to SHA-256 evidence and classify each required ref as one
of `current`, `stale`, `missing`, `contradictory`, or `unsafe`.

Ranking cannot resolve contradictory current authority claims. Contradiction
must deny injection and may be handed to `decision-gate`.

### 4. Strict lean context pack

Only current and safe refs may be handed to Context Builder. Require strict
obligation coverage, Markdown plus JSON/index output, retained source handles,
and measured budget compliance.

### 5. Derived injection gate

Allow injection only when all of these predicates are true:

```text
lookup_ready
and all_required_sources_current
and no_contradiction
and source_scope_safe
and obligations_complete
and pack_within_budget
```

Any false or unknown predicate denies injection. A result label cannot override
the predicates.

### 6. Receipt and optional observation

Emit a `RecallReceipt` for both allowed and denied outcomes. The receipt binds
the request, current inputs, stage results, source evidence, output locators,
and final decision. Optional observation may derive signals from the completed
receipt but cannot change it.

## Handoffs

- Inventory returns an `InventoryLookupPacket`; it does not authorize source
  use or context injection.
- The source verifier returns `VerifiedSourceRef[]`; it does not choose source
  authority when claims conflict.
- Context Builder returns a strict pack; it does not decide whether the host
  injects the pack.
- The spell returns a `RecallReceipt` and, only on pass, a
  `RecallContextPack` handle to the parent-native host.
- The host may place the passing pack into the current task context only. It
  must not persist it as durable memory through this spell.

## Gates

| Gate | Pass condition | Failure result |
| --- | --- | --- |
| request | bounded, typed, explicit request | deny, `invalid-request` |
| index | current Inventory validation and lookup-ready packet | deny, `blocked-index` |
| source | every required path/selector resolves to current safe bytes | deny with `stale`, `missing`, or `unsafe` reason |
| contradiction | no incompatible current claims for one obligation | deny, `contradictory` |
| pack | strict obligation coverage and retained source refs | deny, `incomplete-pack` |
| budget | measured pack is within the declared positive limit | deny, `over-budget` |
| injection | every preceding predicate is true | allow exactly one task-local pack |

## Failure semantics

- Fail closed on invalid, missing, stale, contradictory, unsafe, incomplete,
  over-budget, or unverifiable evidence.
- Never fall back to cached summaries, broaden source scope, silently drop a
  required obligation, or retry through a write operation.
- Emit a receipt even when no pack artifact exists.
- Observer or telemetry failure is recorded as residue and cannot elevate the
  recall decision.
- Dependency or contract mismatch blocks the turn; it does not redefine the
  child capability.

## Customization policy

Allowed candidate-local customization:

- smaller positive budget values;
- repository-specific allowlisted roots and Inventory target selection;
- additional denial reason detail that does not weaken a gate;
- additional fixtures and observations.

Forbidden without a new lifecycle decision:

- automatic invocation, background daemon, cache, embeddings, vector store,
  ranking that resolves authority, Inventory/source writeback, durable memory,
  network transport, credential access, public exposure, or promotion claims;
- weakening strict coverage, current-source verification, or fail-closed
  injection rules.

## Observability

Record, at minimum:

- spell ID/version and request ID;
- Inventory target and index digest;
- child invocation statuses;
- source-state counts and exact evidence handles;
- obligation coverage and measured budget;
- final reason code and `injectionAllowed`;
- pack and receipt digests when present;
- lifecycle/harness version and validation residue.

Observability is non-authority execution evidence. It does not prove promotion,
installation, release, deployment, or semantic correctness beyond the captured
run.

## Output contract

On pass, return:

1. one `RecallReceipt` with `injectionAllowed: true`; and
2. one source-bound `RecallContextPack` locator and digest for the current task.

On any other outcome, return:

1. one `RecallReceipt` with `injectionAllowed: false`;
2. one or more stable reason codes; and
3. no injectable pack handle.

## Lifecycle state

The candidate lifecycle and L0 preparation artifacts are under
`development/`. The release registry and generated host mirrors remain
untouched until live native execution, required negative controls, reusable
Experiment Harness evidence, and a separate promotion decision all pass.
