---
module: skill-surface-dispatch-canonicalization
version: current
status: blocked-pending-user-decision
updatedAt: 2026-06-05
docType: decision-gate
blocker: B-DISP-SURF-001
---

# Decision Gate: Live Codex Skill Refresh

## Decision Needed

`SWU-DISP-SURF-005` would mutate the machine-global Codex skill discovery surface under `/mnt/c/Users/vlad_/.codex/skills`. Source contracts and staged installs now pass, but live refresh still requires explicit approval.

## Options

| Option | Decision | Trade-Off |
| --- | --- | --- |
| A | Approve backed-up live refresh | Fixes the installed-version error now; requires a timestamped backup and preservation of non-Arcanum and unknown packages. |
| B | Approve dry-run backup manifest only | Shows exactly what would change before mutation; leaves the installed-version error in place until the next approval. |
| C | Defer live refresh | Avoids global mutation; leaves stale live aliases and the missing dispatch-spec dependency failure unresolved. |

## Recommendation

Choose Option A if the goal is to fix the installed version now. The staged evidence is complete enough to proceed safely with backup-first live refresh:

- generated `dispatch-spec` packages include `dispatch.schema.yml`, `TECHNIQUE-CATALOG.md`, and `scripts/validate-dispatch.py`;
- staged personal and repo validators pass against `pass-refine-dispatch.json`;
- active skill contracts no longer require command-surface invocation for stage execution;
- unknown packages remain explicitly preserved by policy.

## Stop Condition

Do not run `SWU-DISP-SURF-005` until the user explicitly approves Option A or Option B.
