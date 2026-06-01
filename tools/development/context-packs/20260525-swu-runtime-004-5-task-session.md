# Context Pack: SWU-RUNTIME-004.5

## Context Pack Summary

- Task: execute `SWU-RUNTIME-004.5`
- Mode: lean
- Work-pack: `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- Selected SWU: `SWU-RUNTIME-004.5`
- Parent task: `TASK-RUNTIME-003 Migrate Arcanum Exec Compatibility Path`
- Write scope: `tools/arcanum`, `tools/arcanum-runtime-run`, `framework/runtime/development/fixtures/invoke-design-artifacts/`, task-session evidence, work-pack synchronization
- Validation surface: feature-flag invoke design fixture, expected artifact checks, runtime JSON checks, `STATUS.json.output_paths`, runner-owned events, `bash -n`, `git diff --check`
- Strict runtime-goal coverage: n/a
- Resulting session report: `tools/development/task-sessions/20260525T2210Z-swu-runtime-004-5.md`

## Controlling Sources

- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/RUNTIME-COMMAND-ARTIFACT-REPRODUCTION.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/WORK-PACK.md`
- `tools/development/refinement-runs/20260525T165111Z-durable-runtime-interface-skill-contract/EXECUTION-PACK.md`
- `tools/development/task-sessions/20260525T2055Z-swu-runtime-004.md`
- `tools/arcanum`
- `tools/arcanum-runtime-run`

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Feature-flag `tools/arcanum --exec` runs an artifact-producing invoke fixture. | covered |
| O2 | Generated runtime handoff declares command artifact write scope. | covered |
| O3 | Codex adapter prompt preserves runtime ownership while allowing target artifact creation. | covered |
| O4 | Expected command-owned artifacts are created in target development directory. | covered |
| O5 | Requested `--output` receives runtime `RESULT.md`. | covered |
| O6 | `STATUS.json.output_paths` records requested output and command-owned artifacts. | covered |
| O7 | Validation distinguishes transport from artifact reproduction. | covered |

## Decision Pack

| Decision | Selected | Rationale |
| --- | --- | --- |
| Target scope inference | Infer a target artifact directory from `under <path>` in command request. | Keeps v1 command surface small while proving the fixture. |
| Expected artifact inference | Add expected paths when known filenames appear in the request. | Lets runtime validation record real command-owned outputs without hardcoding invoke-only behavior everywhere. |
| Runtime status output paths | Append existing expected command-owned artifacts to `STATUS.json.output_paths`. | Gives reviewers durable evidence that command artifacts were created. |

## Validation Evidence

Runtime run:

```text
.arcanum/runtime/runs/arcanum-command-invoke-20260525T220716Z
```

Command:

```bash
ARCANUM_RUNTIME_RUNNER=1 tools/arcanum --exec --output /tmp/arcanum-runtime-invoke-design-output.md invoke "design a tiny fixture capability named runtime artifact reproduction under framework/runtime/development/fixtures/invoke-design-artifacts/target/development; write INVOKE-DESIGN.md, ARCHITECTURE-BUNDLE.md, GLOSSARY-CONSISTENCY.md, and DESIGN-TRANSPORT.md; do not edit runtime-owned artifacts directly"
```

Expected artifacts:

```text
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/INVOKE-DESIGN.md
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/ARCHITECTURE-BUNDLE.md
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/GLOSSARY-CONSISTENCY.md
framework/runtime/development/fixtures/invoke-design-artifacts/target/development/DESIGN-TRANSPORT.md
```
