# Experiment Bundle Contract

Purpose: define the mandatory directory contract for experiment-scoped artifacts.

Scope: all new and modified experiments in this project.

## Contract Rules

| Rule ID | Rule | Enforcement |
|---|---|---|
| BC1 | Every experiment uses its own bundle directory under `experiments/<experiment-key>/`. | Protocol review blocks when bundle directory is missing. |
| BC2 | Methodology profile file must be `experiments/<experiment-key>/methodology.md`. | G1 cannot pass without canonical methodology path. |
| BC3 | Protocol file must be `experiments/<experiment-key>/protocol.md`. | G1 cannot pass without canonical protocol path. |
| BC4 | Source selection file must be `experiments/<experiment-key>/sources.md`. | G2 cannot pass without canonical source-selection path. |
| BC5 | Context bundle file must be `experiments/<experiment-key>/context.md`. | Execution readiness is incomplete without context synthesis artifact. |
| BC6 | Raw run data must be append-only JSONL under `experiments/<experiment-key>/data/*.jsonl`. | G4 blocks when data is outside bundle or not JSONL. |
| BC7 | Analysis outputs must be stored under `experiments/<experiment-key>/results/*.md`. | S8-S10 outputs are incomplete without results artifacts. |
| BC8 | Legacy flat artifacts are migration-only and must not receive new writes. | Pull request review blocks new edits to legacy flat paths unless migration-only. |

## Canonical Bundle Layout

```
experiments/
  <experiment-key>/
    methodology.md
    protocol.md
    sources.md
    context.md
    data/
      run-YYYY-MM-DD[-suffix].jsonl
    results/
      <run-id>-results.md
```

Notes:
- `<experiment-key>` should include stable ID plus slug (example: `E9-cross-feature-composition`).
- Additional experiment-local files are allowed when they preserve traceability (for example `notes.md`, `charts/`).

## No Compatibility Aliases

This contract does not define compatibility aliases.

- New and updated experiments must use bundle paths directly.
- Legacy flat files may remain only until migrated.

## Migration Reference

Current migration plan:

- `runbooks/EXPERIMENT-BUNDLE-MIGRATION-PLAN.md`
