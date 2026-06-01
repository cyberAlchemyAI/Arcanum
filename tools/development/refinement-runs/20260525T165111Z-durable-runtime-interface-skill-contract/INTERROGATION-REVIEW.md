## Structured Interview Result

- Target scope: Durable Arcanum Runtime Interface development package
- Mode: package-readiness-review
- Questions asked: 0
- Decisions recorded: 4
- Artifacts updated: `INTERROGATION-REVIEW.md`
- Remaining ambiguities: execution-pack requirement and exact runtime schema details need repair before implementation handoff is fully task-session-ready.
- Verdict: flag
- Next step: repair `WORK-PACK.md`, `IMPLEMENTATION-LAYERING.md`, and runtime schema examples before starting `SWU-RUNTIME-001`.

## Findings

### 1. Medium-complexity invoke plan is missing an execution-pack decision

Severity: high

Evidence:

- `WORK-PACK.md` marks the package as multi-layer medium-complexity work with L0-L3 slices and six SWUs.
- `INVOKE-PLAN.md` declares `Complexity: medium` and `Per-layer planning: L0, L1, L2, L3`.
- `spells/invoke/plan.md` requires medium/high plans to include execution-pack handoff or a recorded blocker.
- No `EXECUTION-PACK.md` exists, and no explicit execution-pack blocker/deferral is recorded in `WORK-PACK.md`, `INVOKE-PLAN.md`, or `PLAN-TRANSPORT.md`.

Risk:

The package may look task-session-ready but fail invoke plan governance because medium-complexity choreography is not represented.

Repair:

Add either:

- `EXECUTION-PACK.md` with wave ordering and parallelization boundaries, or
- an explicit `Execution-Pack Deferral` section naming why `WORK-PACK.md` is sufficient for this package and what validation accepts instead.

Recommended default:

Add a compact `EXECUTION-PACK.md` because the package already has L0-L3 layer slices and blocked downstream dependencies.

### 2. Runtime schemas are conceptual, not exact enough for SWU-RUNTIME-001 execution

Severity: high

Evidence:

- `ARCHITECTURE-BUNDLE.md` lists `RUN.json` and `STATUS.json` fields as concepts.
- `IMPLEMENTATION-LAYERING.md` requires templates for `RUN.json` and `STATUS.json`.
- `WORK-PACK.md` asks `SWU-RUNTIME-001` to create runtime docs/templates, but does not define exact required JSON shapes, enum values, or fixture values.

Risk:

The first implementer must invent schema details during execution. That violates the purpose of Invoke Plan for medium-complexity work and can create drift between docs, fixture validation, and runner implementation.

Repair:

Add exact minimal schemas or template examples before executing `SWU-RUNTIME-001`:

- `RUN.json` field names, required/optional status, and sample values.
- `STATUS.json` allowed status enum and adapter status fields.
- `events.jsonl` minimum event fields.
- `RUNTIME-HANDOFF.md` required sections.

Recommended default:

Put field-level templates in `ARCHITECTURE-BUNDLE.md` and mirror them in `WORK-PACK.md` task details.

### 3. SWU verification commands are not concrete enough for task-session handoff

Severity: medium

Evidence:

- `SWU-RUNTIME-001` verification is `test -f framework/runtime/README.md and template file checks`.
- `SWU-RUNTIME-002` verification uses `tools/arcanum-runtime-run --adapter dry-run ...` but does not name the fixture path or expected output paths.
- `SWU-RUNTIME-003` allows `codex-exec fixture or blocked adapter status evidence` without defining the fixture or blocked evidence shape.

Risk:

Task Session can select an SWU but still needs to invent the exact validation commands and acceptance evidence.

Repair:

Make each SWU verification command literal, even if paths are fixture placeholders created in L0:

```bash
test -f framework/runtime/README.md
test -f framework/runtime/templates/RUNTIME-HANDOFF.md
test -f framework/runtime/templates/RUN.json
test -f framework/runtime/templates/STATUS.json
tools/arcanum-runtime-run --adapter dry-run --handoff framework/runtime/development/fixtures/dry-run/RUNTIME-HANDOFF.md --run-dir /tmp/arcanum-runtime-dry-run
jq empty /tmp/arcanum-runtime-dry-run/RUN.json
jq empty /tmp/arcanum-runtime-dry-run/STATUS.json
```

### 4. `tools/arcanum --exec` migration needs an output compatibility contract

Severity: medium

Evidence:

- `WORK-PACK.md` says feature-flag `--exec` should delegate to runtime runner and preserve output path.
- `ARCHITECTURE-BUNDLE.md` says runtime runner writes `RESULT.md`.
- The package does not define whether `--output` receives a copy, symlink, or direct adapter output.

Risk:

Existing callers and refine validation may disagree about where the final artifact lives. This is especially risky because prior refine work already found output-last-message/artifact overwrite problems.

Repair:

Define exact compatibility behavior:

- runtime runner always writes canonical runtime `RESULT.md`,
- `tools/arcanum --exec --output <path>` copies runtime `RESULT.md` to `<path>` after adapter completion,
- if adapter fails before result, `<path>` receives a blocked summary instead of being absent,
- manifest records both runtime result and requested output path.

### 5. Stale-language cleanup scope is still under-specified

Severity: low

Evidence:

- `WORK-PACK.md` says historical `/goal` references should not break active validation.
- `INVOKE-DEFINE.md` and `GLOSSARY-CONSISTENCY.md` defer historical cleanup.
- The package does not define the exact active-path stale-language allowlist.

Risk:

Implementation may either over-clean historical evidence or leave active runtime surfaces stale.

Repair:

Add a validation section with active paths and allowed historical exceptions.

Recommended active-path check:

```bash
rg -n "GOAL-HANDOFF|Codex Goal|codex-goal|/goal" arcana/refine .codex/commands/refine.md ~/.codex/skills/refine/SKILL.md
```

Allowed exceptions should be explicit migration notes only.

## Decisions Recorded

| Decision | Value | Rationale |
| --- | --- | --- |
| Package verdict | flag | The architecture is coherent, but the work-pack needs repair before mutation-capable execution. |
| Blocker status | non-blocking for design, blocking for task-session execution | The gaps affect execution readiness, not conceptual validity. |
| Next repair owner | invoke plan refresh | The gaps are in plan/work-pack detail, not define/design intent. |
| First SWU after repair | SWU-RUNTIME-001 | L0 remains the right first slice once schema and validation are concrete. |

## Readiness Verdict

The development package is conceptually sound and internally aligned around the generic runtime model, but it is not yet fully execution-ready.

Status: `flag`

Required before implementation:

1. Add execution-pack handoff or explicit deferral.
2. Add exact runtime schema/template examples.
3. Make SWU validation commands literal.
4. Define `tools/arcanum --exec --output` compatibility behavior.

## Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: none
- RECOMMENDATION: repair-plan-before-task-session
- DEDUPE_KEY: interrogation-runtime-package-review-20260525T165111Z
