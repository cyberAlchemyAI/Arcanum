# Structured Interview Result

## Observer Envelope

- `run_id`: arcanum-interrogation-20260525T-adapter-pattern-review
- `capability.id`: structured-interview-kits
- `capability.kind`: sigil
- `capability.tier`: arcana
- `capability.mode`: command
- `target_artifact`: `RUNTIME-ADAPTER-PATTERN.md`, `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- Request summary: review the runtime adapter pattern and Codex adapter design after the invoke design pass.
- Expected outputs: review verdict, risk list, repair targets, and next action.

## Selected Mode

- Mode: `refine-design-review`
- Review stance: artifact readiness critique before implementation.
- Cadence note: this execution is a local skill-contract review, not an interactive interview, because the user requested interrogation plus distill over the current artifacts.

## Questions Asked

None. The available artifacts are sufficient for a first-pass review.

## Answers Recorded

None.

## Artifacts Reviewed

- `RUNTIME-ADAPTER-PATTERN.md`
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`
- `RUNTIME-SCHEMAS.md`
- `WORK-PACK.md`

## Verdict

`flag`

The adapter model is implementation-worthy, but it needs one contract repair before `SWU-RUNTIME-003` starts. The main issue is not the architecture direction; it is that the status, profile, event, and validation boundaries are still split across documents in a way an implementer could interpret inconsistently.

## Findings

### 1. Codex blocked-vs-failed mapping is underspecified in the runner pseudocode

- Severity: high
- Evidence: `CODEX-RUNTIME-ADAPTER-DESIGN.md` says backend/network unavailable before sampling maps to `blocked`, while the shell sketch maps any nonzero `codex exec` result to `failed`.
- Risk: a backend/auth/preflight outage could be recorded as execution failure, which weakens the durable runtime model and hides whether work actually began.
- Repair target: define a `classify_codex_exit` or equivalent adapter classification step before writing terminal status.

Required decision:

```text
Raw Codex outcome -> adapter classifier -> adapter_status -> runner terminal status
```

### 2. Adapter profile fields are not yet part of durable runtime evidence

- Severity: medium
- Evidence: `RUNTIME-ADAPTER-PATTERN.md` defines required runtime adapter profile fields, while `RUNTIME-SCHEMAS.md` records only `adapter_id`.
- Risk: later review can prove which adapter was selected, but not which adapter properties and limitations were in force for that run.
- Repair target: add `adapter_profile_path` to `RUN.json`, or require `artifacts/adapter-profile.json` in every runtime run.

Required decision:

```text
Runtime evidence must include the selected adapter profile snapshot or path.
```

### 3. Event ownership is split between runner and adapter

- Severity: medium
- Evidence: `RUNTIME-ADAPTER-PATTERN.md` lets adapters return `events`, while `RUNTIME-SCHEMAS.md` says the runner owns `events.jsonl`.
- Risk: implementations may double-write, skip adapter events, or let malformed adapter events pollute runtime evidence.
- Repair target: runner owns the event log; adapters return event contributions; runner validates and appends them.

Required decision:

```text
Adapters do not write events.jsonl directly in v1.
```

### 4. Validation currently mixes safety proof with execution proof

- Severity: high
- Evidence: `CODEX-RUNTIME-ADAPTER-DESIGN.md` allows backend/network blocked execution to count as adapter-safety validation when isolation and blocked closeout are correct.
- Risk: `SWU-RUNTIME-003` could be promoted as a working execution adapter when it only proved safe blocked behavior.
- Repair target: define validation grades and require the work-pack to name which grade each check proves.

Required decision:

```text
Contract validation != adapter safety validation != execution validation.
```

### 5. Codex state validation is too narrow

- Severity: medium
- Evidence: `CODEX-RUNTIME-ADAPTER-DESIGN.md` validation checks specific files like `state_5.sqlite` and `goals_1.sqlite`; `RUNTIME-SCHEMAS.md` forbids any `.sqlite`, `.sqlite-wal`, or `.sqlite-shm` files.
- Risk: another Codex database filename could leak into the per-run home while validation still passes.
- Repair target: validate no SQLite-like files exist anywhere under the run-local Codex home.

Required decision:

```text
Use pattern-based SQLite exclusion checks, not filename-only checks.
```

### 6. Auth/config unavailable status is ambiguous

- Severity: medium
- Evidence: the Codex status table says source auth/config unavailable maps to `blocked` or `flagged`.
- Risk: an implementer may continue into a runtime call when the selected adapter cannot safely authenticate.
- Repair target: make the rule deterministic.

Recommended rule:

```text
For selected adapter `codex-exec`, missing required auth/config is blocked.
For dry-run or validation-only mode, missing auth/config may be flagged.
```

## Decision Record

- Keep Codex as an adapter, not the runtime model.
- Keep static adapter dispatch for v1.
- Keep `dry-run` as the L0 proof adapter.
- Add an adapter contract repair before implementing `codex-exec`.
- Do not move refine/task-session integration forward until command compatibility proves runtime evidence.

## Remaining Ambiguities

- Whether adapter profiles should live as `framework/runtime/adapters/<adapter-id>.md`, `framework/runtime/adapters/<adapter-id>/RUNTIME-PROFILE.md`, or generated JSON snapshots under each run.
- Whether `codex-exec` should run a cheap preflight before invoking `codex exec`, or classify stderr/exit results after a failed invocation.
- Whether `tools/arcanum-runtime-run` should expose an explicit `--validation-grade` flag or only record grades in fixtures and status metadata.

## Readiness Verdict

`flag`

The design can continue, but the next refresh should produce an adapter contract decision artifact before implementation begins.

## Supersession Note

This review originally recommended validating that no SQLite-like files exist anywhere under the run-local Codex home. A later task-session run proved Codex creates SQLite files during normal startup.

The active contract supersedes that recommendation:

- allow contained run-local Codex SQLite,
- forbid shared, copied, or symlinked source Codex SQLite,
- block only when watched SQLite files are symlinks or resolve outside the runtime run folder.

## Recommended Patch Targets

- `ADAPTER-CONTRACT-DECISIONS.md`: new repair artifact.
- `RUNTIME-SCHEMAS.md`: selected adapter profile evidence and event ownership wording.
- `WORK-PACK.md`: make `SWU-RUNTIME-003` depend on adapter contract repair and distinguish validation grades.
- `CODEX-RUNTIME-ADAPTER-DESIGN.md`: replace the simple nonzero-to-failed pseudocode with explicit classification.

## Observability Closeout

OBSERVATION:

- Local command resolution confirmed `/interrogation` resolves to `.codex/commands/interrogation.md`.
- This was executed as a local skill-contract pass because the durable runtime runner is the thing being designed and cannot yet host this review.

LEDGER:

- Inputs: runtime adapter pattern, Codex adapter design, runtime schemas, work-pack.
- Output: `RUNTIME-ADAPTER-INTERROGATION-REVIEW.md`.
- Verdict: `flag`.

REFLECTION_TRIGGER:

- Trigger when `SWU-RUNTIME-003` starts without adapter contract repair.

RECOMMENDATION:

- Run invoke refresh to add `ADAPTER-CONTRACT-DECISIONS.md` and update implementation layering/work-pack references.

DEDUPE_KEY:

- `interrogation:durable-runtime:adapter-pattern-review:20260525`
