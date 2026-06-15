# TASK-CLP-004: CSV Import Dry Run

Goal: produce a patch plan from edited CSV projections without mutating YAML.

Acceptance:

- Dry run blocks stale projections.
- Dry run blocks ID churn and unresolved references.
- Dry run reports read-only nested fields instead of flattening them unsafely.
