# Passing Example: SWU To Native Codex Goal

## Input SWU

| Field | Value |
| --- | --- |
| Work-pack | `spells/example/development/WORK-PACK.md` |
| Parent task | `TASK-DOCS-003` |
| SWU | `SWU-DOCS-003-001` |
| Source | `README.md`, `docs/feature-notes.md` |
| Dependencies | `TASK-DOCS-001`, `TASK-DOCS-002` complete |
| Write scope | `docs/feature.md`, `README.md` |
| Done criteria | Feature docs explain lifecycle, commands, and examples. |
| Validation | `npm run docs:check` |
| Blockers | none |

## Output Profile

```text
/goal Complete SWU-DOCS-003-001 by producing feature docs that explain the lifecycle, commands, and examples, verified by `npm run docs:check`, while preserving the current public command names and README navigation. Use only `README.md`, `docs/feature-notes.md`, `docs/feature.md`, and related documentation context. Between iterations, record what changed, run or explain the docs check, and choose the smallest next documentation fix. If dependencies are contradicted, docs validation cannot run, or the command behavior is unclear, stop with the attempted changes, evidence gathered, blocker, and next input needed.
```

## Verdict

Pass. The profile names outcome, verification, constraints, boundaries, iteration policy, and blocked stop condition.
