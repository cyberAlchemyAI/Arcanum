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
| Handoff pack | `.arcanum/runs/run-123/context-pack.md` |
| Handoff index | `.arcanum/runs/run-123/context-pack.json` |
| Strict coverage | pass |
| Fallback exploration | none |
| Blockers | none |

## Output Profile

```text
/goal Complete SWU-DOCS-003-001 by producing feature docs that explain the lifecycle, commands, and examples, verified by `npm run docs:check`, while preserving the current public command names and README navigation. Use the handoff pack at `.arcanum/runs/run-123/context-pack.md` and structured index at `.arcanum/runs/run-123/context-pack.json` as selected source context, plus only `docs/feature.md` and `README.md` write scope. Broaden repository exploration only for named gaps from the pack: none. If you use extra sources, report the named gap, source path, and whether it changed the result. Between iterations, record what changed, run or explain the docs check, and choose the smallest next documentation fix. If dependencies are contradicted, docs validation cannot run, the handoff pack is contradicted, or the command behavior is unclear, stop with the attempted changes, evidence gathered, blocker, and next input needed.
```

## Verdict

Pass. The profile names outcome, verification, constraints, boundaries, handoff pack, strict coverage, fallback limits, extra-source reporting, iteration policy, and blocked stop condition.
