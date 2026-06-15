# TASK-CLP-003: Build And Validate Tooling

Goal: generate and validate `index.json` plus `.craft/projections/*.csv`.

Acceptance:

- `craft-index build` creates deterministic outputs.
- `craft-index validate` detects stale source hashes.
- Unsupported row families are flagged, not silently skipped.
