## Distill Result

- Target context: Durable Arcanum Runtime Interface development package after interrogation review.
- Objective and output artifact: Find anything missed by review and identify the smallest coherent repair unit before implementation.
- Mode and budget: validate
- Proposal tracks: 1 Balancer-led validation track with Proposer repair notes.
- Recursive rounds: 2 / 2
- Verdict: flag
- Role conversation trace: Proposer claimed the package can start with `SWU-RUNTIME-001`; Balancer found missing lock/resume semantics, output compatibility details, and an execution-pack gap; reconciliation selects a plan-repair unit before implementation.
- Current smallest coherent unit: `PLAN-REPAIR-001`, a pre-implementation package repair that adds exact runtime schemas, execution-pack choreography, lock/resume policy, and literal SWU validation.
- Optimization point: Repair the package once before implementing runtime code; smaller than rewriting the architecture, larger than patching only `WORK-PACK.md`.
- Concept layer map: Durable runtime architecture -> execution-ready package -> plan repair unit -> first implementation SWU.
- Technique pack trace: abstraction-level guard passed; recomposition proof passed; evolution profile triggered; boundary-object check triggered; premortem triggered; navigable result check flagged until repair is applied.
- Closure and recomposition proof: The repair unit closes around the missing execution contract details and recomposes into `SWU-RUNTIME-001` through concrete templates, validation commands, and runner lifecycle rules.
- Evolution profile: The runtime will likely evolve toward retry/resume, child runs, multiple adapters, and async scheduling; v1 needs explicit lock/resume semantics even if scheduling is deferred.
- Deferred complexity: background scheduler, remote queue, UI, automatic adapter discovery, and full historical `/goal` cleanup remain deferred.
- Tension ledger: resolved that architecture is coherent; unresolved execution readiness until package repair; unresolved whether `EXECUTION-PACK.md` is added or explicitly deferred.
- Premortem: The most likely failure is implementing the runner from conceptual docs and discovering inconsistent schema, output, lock, or existing-run behavior during validation.
- Frame-expiry note: This distillation expires once `EXECUTION-PACK.md`, exact schemas, lock/resume policy, and literal SWU validation are added.
- Navigation guide: Do not start `SWU-RUNTIME-001` yet. First run an Invoke Plan repair over `WORK-PACK.md`, `IMPLEMENTATION-LAYERING.md`, `ARCHITECTURE-BUNDLE.md`, and `INTERROGATION-REVIEW.md`.
- Next route: invoke plan

## Additional Misses Found

### 1. Runtime lock and existing-run behavior is missing

Severity: high

Why Distill caught it:

The package says runtime runs are durable and async-ish, but it does not define what happens when a run directory already exists or two executions target the same run.

Evidence:

- `ARCHITECTURE-BUNDLE.md` says the runner creates `.arcanum/runtime/runs/<runtime-run-id>/`.
- `WORK-PACK.md` lists `existing run dir` as an edge case but does not define behavior.
- `STATUS.json` includes `queued`, `running`, `passed`, `flagged`, `blocked`, and `failed`, but no transition policy.

Risk:

The first runner implementation may overwrite an existing run, treat a partial run as fresh, or fail inconsistently. That directly undermines the durable runtime premise.

Required repair:

Add a v1 lock/resume policy:

- create a run-local lock file before adapter execution,
- if lock exists and status is `running`, return `blocked` with `blocked_reason: run-already-active`,
- if status is terminal, default to no overwrite unless `--force` or a new run id is supplied,
- if status is `failed` or `blocked`, a future retry must create a continuation child run rather than mutate the original run,
- record lock acquisition and release in `events.jsonl`.

### 2. Status transition semantics are not defined

Severity: high

Why Distill caught it:

The package names statuses, but the smallest coherent runtime unit needs transition rules to avoid becoming a loose file dump.

Required repair:

Define v1 transitions:

```text
queued -> running -> passed
queued -> running -> flagged
queued -> running -> blocked
queued -> running -> failed
```

Rules:

- `blocked` means execution did not safely begin or a required adapter/input was unavailable.
- `failed` means execution began and the adapter/process failed unexpectedly.
- `flagged` means output exists but warnings/gaps remain.
- terminal statuses are `passed`, `flagged`, `blocked`, `failed`.

### 3. Event schema is missing

Severity: medium

Why Distill caught it:

`events.jsonl` is repeatedly listed as required, but no minimum event shape exists.

Required repair:

Define the minimum event object:

```json
{
  "timestamp": "2026-05-25T00:00:00Z",
  "run_id": "runtime-run-id",
  "event": "created|locked|status-changed|adapter-started|adapter-finished|result-written|blocked|failed",
  "status": "queued|running|passed|flagged|blocked|failed",
  "message": "human readable summary",
  "data": {}
}
```

### 4. Adapter result contract is underspecified

Severity: medium

Why Distill caught it:

The architecture says adapters return status and outputs, but the runner needs a stable adapter result shape to handle `dry-run` and `codex-exec` uniformly.

Required repair:

Define adapter result fields:

- `adapter_id`
- `adapter_status`
- `exit_code`
- `output_paths`
- `result_path`
- `blocked_reason`
- `error_summary`
- `state_path`
- `events`

### 5. Source Codex home handling needs a safety boundary

Severity: medium

Why Distill caught it:

The package says to symlink stable auth/config from source Codex home, but does not define what counts as stable or what must never be shared.

Required repair:

Specify:

- allowed symlinks: `auth.json`, `config.toml`, `installation_id`, `models_cache.json` when present,
- disallowed sharing: SQLite state/log/goal databases, per-run logs, transient sockets, runtime state directories,
- per-run Codex home path: `<runtime-run-dir>/adapter-state/codex-home`.

### 6. First implementation unit is close, but not yet closed

Severity: medium

Why Distill caught it:

`SWU-RUNTIME-001` only covers docs/templates; `SWU-RUNTIME-002` covers the runner/dry-run. The package recommends starting at `SWU-RUNTIME-001`, but the real smallest coherent proof is the pair `SWU-RUNTIME-001 + SWU-RUNTIME-002`.

Repair options:

- Keep two SWUs, but mark L0 promotion blocked until both complete.
- Or merge them into one larger `SWU-RUNTIME-L0-001` if the team wants one proof slice.

Recommended default:

Keep them split, but update `PLAN-TRANSPORT.md` and `WORK-PACK.md` to say the first **execution target** is `SWU-RUNTIME-001`, while the first **proof of runtime viability** requires both `SWU-RUNTIME-001` and `SWU-RUNTIME-002`.

## Proposer/Balancer Trace

| Role | Claim or Objection | Category | Reconciliation |
| --- | --- | --- | --- |
| Proposer | The package can proceed from SWU-RUNTIME-001. | implementation path | revise: SWU-RUNTIME-001 can start only after plan repair; L0 proof needs SWU-RUNTIME-001 and SWU-RUNTIME-002. |
| Balancer | Existing run behavior is missing. | lifecycle/state | accept: add lock/resume and terminal-state policy. |
| Balancer | Status names lack transition rules. | state machine | accept: add v1 transition table. |
| Balancer | `events.jsonl` has no event schema. | evidence contract | accept: add event object schema. |
| Balancer | Codex home isolation is underspecified. | adapter safety | accept: define allowed symlinks and forbidden shared state. |

## Required Repair Checklist

Before implementation:

1. Add `EXECUTION-PACK.md` or explicit execution-pack deferral.
2. Add exact `RUN.json`, `STATUS.json`, `events.jsonl`, and adapter result schemas.
3. Add lock/existing-run/resume semantics.
4. Add `codex-exec` source-home sharing boundary.
5. Make SWU validation commands literal.
6. Clarify that L0 proof requires both `SWU-RUNTIME-001` and `SWU-RUNTIME-002`.

## Readiness

The package remains conceptually good, but Distill agrees with Interrogation that it is not execution-ready yet.

Status: `flag`

Best next action: run `invoke plan` repair on the package using `INTERROGATION-REVIEW.md` and this `DISTILL-REVIEW.md` as required inputs.

## Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: invoke-plan-repair-before-task-session
- DEDUPE_KEY: distill-runtime-package-review-20260525T165111Z
