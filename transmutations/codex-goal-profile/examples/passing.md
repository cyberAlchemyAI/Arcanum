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
| Goal budget | 4000 characters, pass |
| Decision profile | none |
| One-shot mode | no |
| Sidecar profile | none |

## Output Profile

```text
/goal Complete SWU-DOCS-003-001 by producing feature docs, verified by `npm run docs:check`. Use `.arcanum/runs/run-123/context-pack.md` and `.arcanum/runs/run-123/context-pack.json` as the execution frame. Write only `docs/feature.md` and `README.md`. Broaden only for named gaps: none. Iterate by running or explaining the docs check after each change. Stop if dependencies, validation, or command behavior contradict the pack, reporting attempted changes, evidence, blocker, and next input.
```

## Verdict

Pass. The profile names outcome, verification, constraints, boundaries, handoff pack, strict coverage, goal budget, fallback limits, extra-source reporting, iteration policy, and blocked stop condition.
