## Invoke Result

- Mode: plan
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/plan.md`
- Outputs: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/stages/09-invoke-plan.md`, refreshed by `INVOKE-PLAN.md`
- Design views: n/a
- Glossary consistency: pass
- Implementation layering: artifact seed included
- Work-pack: single-file plan below
- Complexity: medium
- Per-layer planning: compact
- Implementation detail: inline task specs complete
- Smallest working units: complete
- Target artifact: Durable Arcanum Runtime Interface, implementation plan, owner `framework/runtime`
- Template or recipe selection: compact implementation-layered plan.
- Decisions: dry-run first, adapter contract repair before `codex-exec`, allow contained run-local Codex SQLite while forbidding shared/symlinked source SQLite, feature-flag command migration, add `SWU-RUNTIME-004.5` for artifact-producing command reproduction, active-path refine migration after artifact reproduction, schema-discipline rules for runtime artifacts.
- Unresolved gaps: none blocking.
- Next route: task-session

### Implementation Plan

#### L0: Runtime Contract And Dry-Run

- Create `framework/runtime/README.md`.
- Create `framework/runtime/templates/RUNTIME-HANDOFF.md`.
- Create `framework/runtime/templates/RUN.json`.
- Create `framework/runtime/templates/STATUS.json`.
- Create `tools/arcanum-runtime-run`.
- Implement `--adapter dry-run`.
- Validate handoff exists, create run folder, write `RUN.json`, `STATUS.json`, `RESULT.md`, `events.jsonl`.
- Preserve lightweight schema discipline: `schema_version`, inline enums, stable ids/paths, adapter profile provenance, and validation grades.

#### L1: Codex Adapter

- Implement `--adapter codex-exec`.
- Create isolated per-run `CODEX_HOME`.
- Symlink stable auth/config from source Codex home.
- Allow Codex-created SQLite only when contained inside run-local adapter state.
- Block shared, symlinked, or copied SQLite from source Codex home.
- Record adapter profile evidence, classified status, and validation grade.
- Run `codex exec`.
- Capture result and failures in runtime artifacts.

#### L2: Command Surface Migration

- Add `ARCANUM_RUNTIME_RUNNER=1` route to `tools/arcanum --exec`.
- Generate runtime handoff from resolved command and request.
- Copy or link runtime `RESULT.md` to `--output`.
- Preserve existing command summary output.
- Prove artifact-producing invoke commands create expected target development artifacts, not only runtime `RESULT.md`.

#### L3: Refine And Task-Session Migration

- Update refine active docs/templates/fixtures from `GOAL-HANDOFF.md` to `RUNTIME-HANDOFF.md`.
- Require runtime run evidence in refine manifest/index for non-blocked command-backed stages.
- Add `arcana/task-session/runtime-adapters/runtime-handoff.md`.
- Deprecate `codex-goal.md` as legacy/historical.

### Work-Pack

| SWU | Layer | Write Scope | Acceptance Evidence |
| --- | --- | --- | --- |
| SWU-RUNTIME-001 | L0 | `framework/runtime/` | runtime docs/templates preserve schema discipline |
| SWU-RUNTIME-002 | L0 | `tools/arcanum-runtime-run`, fixtures | dry-run fixture creates valid run folder |
| SWU-RUNTIME-003 | L1 | `tools/arcanum-runtime-run`, codex fixture | codex-exec uses isolated runtime home and records classified evidence |
| SWU-RUNTIME-004 | L2 | `tools/arcanum` | feature-flag exec route delegates to runtime runner |
| SWU-RUNTIME-004.5 | L2 | `tools/arcanum`, `tools/arcanum-runtime-run`, invoke design fixture | artifact-producing invoke design creates target development files |
| SWU-RUNTIME-005 | L3 | `arcana/refine/`, `.codex/commands/refine.md` | refine validation expects `RUNTIME-HANDOFF.md` |
| SWU-RUNTIME-006 | L3 | `arcana/task-session/runtime-adapters/` | task-session has generic runtime handoff adapter |

### Validation Commands

```bash
tools/arcanum-runtime-run --adapter dry-run --handoff <fixture>/RUNTIME-HANDOFF.md --run-dir <tmp-run>
jq empty <tmp-run>/RUN.json
jq empty <tmp-run>/STATUS.json
jq -e '.schema_version == "arcanum.runtime.run.v1"' <tmp-run>/RUN.json
jq -e '.schema_version == "arcanum.runtime.status.v1"' <tmp-run>/STATUS.json
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output <tmp-output> invoke "define runtime smoke"
arcana/refine/development/run-validation-fixtures.sh
```

### Observability Closeout

- OBSERVATION: skipped
- LEDGER: n/a
- REFLECTION_TRIGGER: trigger if implementation accepts undocumented runtime enum values or treats adapter-safety as execution proof.
- RECOMMENDATION: continue at `SWU-RUNTIME-004.5`; run schema-discipline handoff separately before broadening governance.
- DEDUPE_KEY: local-skill-contract-invoke-plan-20260525T165111Z
