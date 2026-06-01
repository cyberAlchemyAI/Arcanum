# Distill Result

## Observer Envelope

- `run_id`: arcanum-distill-20260525T-adapter-pattern-review
- `capability.id`: distill
- `capability.kind`: sigil
- `capability.tier`: arcana
- `capability.mode`: command
- `target_artifact`: `RUNTIME-ADAPTER-PATTERN.md`, `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- Request summary: distill what may be missing from the runtime adapter design and identify the smallest coherent repair before implementation.
- Expected outputs: distilled concept unit, role trace, technique trace, verdict, and next route.

## Intent And Budget

- Design intent: make runtime adapters explicit enough that new runtimes can be added without changing refine or task-session.
- Target context: implementation handoff for durable Arcanum runtime.
- Expected output artifact: repair-focused review artifact.
- Optimization goal: prevent adapter ambiguity before `codex-exec` implementation.
- Selected budget: Standard, inferred from the user's `/distill` request and the package maturity.
- Role execution path: labeled Proposer and Balancer passes in one agent.

## Discovery Baseline

Reviewed artifacts:

- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `RUNTIME-SCHEMAS.md`
- `WORK-PACK.md`

Current strength:

- The architecture separates orchestrator, durable runner, translator/executor, and adapter.
- Codex is correctly treated as `codex-exec`, not as the runtime model.
- Per-run Codex state isolation is explicit and well-motivated.
- The work-pack has a sensible L0 to L3 ordering.

Current tension:

- The adapter pattern is clear as design prose but not yet complete as an implementation contract.
- The first real adapter, `codex-exec`, needs exact classification rules and validation grades because blocked backend execution can still be a valid safety proof.

## Broadest Concept Layer

Layer: runtime extensibility architecture.

This layer includes all future runtimes, refine/task-session reuse, command compatibility, and adapter validation.

## Smallest Coherent Unit

The smallest coherent repair unit is:

```text
Adapter Contract Repair
```

This unit should define:

- where adapter profiles live,
- how the runner references the selected profile,
- who owns event writes,
- how adapter terminal status is classified,
- how validation distinguishes contract proof, safety proof, and execution proof.

It is smaller than implementing `codex-exec`, but large enough to prevent the first real runtime adapter from encoding accidental policy.

## Proposer Pass

Claim:

The package should add a small adapter contract decision artifact before implementation.

Evidence or assumption:

- `RUNTIME-ADAPTER-PATTERN.md` defines profile fields but does not put the selected profile into `RUN.json`.
- `CODEX-RUNTIME-ADAPTER-DESIGN.md` gives a nuanced status table, but the pseudocode collapses nonzero execution into `failed`.
- `RUNTIME-SCHEMAS.md` defines adapter result `events`, while runner core owns `events.jsonl`.
- `WORK-PACK.md` validates `codex-exec` but does not separate blocked safety validation from actual model execution validation.

Candidate unit:

`ADAPTER-CONTRACT-DECISIONS.md` plus small updates to `WORK-PACK.md` and possibly `RUNTIME-SCHEMAS.md`.

## Balancer Pass

Objection category: scope control.

- Objection: adding another artifact could delay implementation.
- Reconciliation: accept the concern, but keep the repair artifact small and decision-only. Do not redesign the runtime.

Objection category: duplicate contract.

- Objection: adapter profile details already exist in `RUNTIME-ADAPTER-PATTERN.md`.
- Reconciliation: revise. The repair should not restate the whole pattern; it should lock implementation decisions that remain ambiguous across existing artifacts.

Objection category: validation granularity.

- Objection: too many validation grades may overcomplicate L1.
- Reconciliation: accept a minimal three-grade model:
  - contract validation,
  - adapter safety validation,
  - execution validation.

Objection category: premature generality.

- Objection: future adapter rules may be overbuilt before a second real adapter exists.
- Reconciliation: reject broad plugin-loading design for now; keep static dispatch and require only profile metadata plus classification rules.

## Technique Trace

| Technique | Activation Reason | Decision | Readiness Effect |
| --- | --- | --- | --- |
| abstraction-level guard | Adapter pattern spans both design and implementation. | Keep repair at contract boundary, not runtime redesign. | improves readiness |
| recomposition proof | Need to prove small repair recomposes into L0/L1. | Adapter Contract Repair feeds `SWU-RUNTIME-003` and future adapters. | improves readiness |
| evolution profile | More runtimes are explicitly expected. | Add profile and validation semantics without dynamic loading. | improves readiness |
| frame-expiry note | Current frame is pre-implementation. | Revisit after dry-run and first `codex-exec` fixture. | contains drift |
| navigable result check | User needs actionable next route. | Route to adapter contract repair before implementation. | improves handoff |

## Closure Test

| Closure Property | Result |
| --- | --- |
| Responsibility | Defines adapter implementation contract decisions. |
| Inputs | Existing adapter pattern, Codex design, runtime schemas, work-pack. |
| Outputs | Repair decisions and implementation guidance. |
| Abstraction level | Between architecture design and first adapter implementation. |
| Recomposition | Feeds `SWU-RUNTIME-003` without changing refine/task-session. |
| Hidden glue | Event/status/profile ownership becomes explicit. |
| Future scale | Supports more adapters without dynamic plugin loading. |
| Meaning if split further | Splitting further would scatter classification, profiles, and validation. |

## Distilled Repair

Add an adapter contract repair before implementing `codex-exec`:

1. Add a selected adapter profile reference to runtime evidence.
   - Either add `adapter_profile_path` to `RUN.json`, or require `artifacts/adapter-profile.json`.
   - Keep adapter-specific details out of top-level runtime fields unless generic.

2. Define status classification as adapter-owned, runner-applied.
   - Adapter classifies raw runtime outcome into `passed`, `flagged`, `blocked`, or `failed`.
   - Runner validates the status is allowed, writes `STATUS.json`, and records events.

3. Define event ownership.
   - Runner owns `events.jsonl`.
   - Adapter may return event contributions.
   - Runner appends normalized adapter events and rejects malformed ones.

4. Define validation grades.
   - Contract validation: files and schemas exist.
   - Adapter safety validation: isolation and blocked reporting behave correctly.
   - Execution validation: runtime actually completes requested work.

5. Tighten Codex state safety validation.
   - Check for any `.sqlite`, `.sqlite-wal`, and `.sqlite-shm` files in run-local Codex home.
   - Do not only check `state_5.sqlite` and `goals_1.sqlite`.

## Recomposition Proof

The repair recomposes like this:

```text
RUNTIME-ADAPTER-PATTERN.md
  -> ADAPTER-CONTRACT-DECISIONS.md
    -> SWU-RUNTIME-003 codex-exec implementation
      -> SWU-RUNTIME-004 tools/arcanum --exec compatibility
        -> SWU-RUNTIME-005 refine runtime migration
        -> SWU-RUNTIME-006 task-session runtime adapter
```

It does not change the core architecture. It makes the first real adapter deterministic enough to implement.

## Verdict

`flag`

The design is conceptually ready, but implementation should not start at `codex-exec` until the adapter contract repair is captured.

## Next Route

Invoke refresh or design repair:

```text
Create ADAPTER-CONTRACT-DECISIONS.md and update the work-pack so SWU-RUNTIME-003 depends on that repair.
```

## Observability Closeout

OBSERVATION:

- Local command resolution confirmed `/distill` resolves to `.codex/commands/distill.md`.
- This was executed as a local skill-contract pass because the current durable runtime runner does not exist yet.

LEDGER:

- Inputs: runtime adapter pattern, Codex adapter design, runtime schemas, work-pack.
- Output: `RUNTIME-ADAPTER-DISTILL-REVIEW.md`.
- Verdict: `flag`.

REFLECTION_TRIGGER:

- Trigger when `codex-exec` implementation begins or if `SWU-RUNTIME-003` is promoted without adapter contract repair.

RECOMMENDATION:

- Repair adapter contract decisions before writing the Codex adapter.

DEDUPE_KEY:

- `distill:durable-runtime:adapter-contract-review:20260525`
