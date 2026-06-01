# Invoke Refresh Report: x-ray YAML Visual Library

## Summary

- Mode: refresh
- Spell: invoke
- Phase status: pass
- Mutation mode: proposal-only
- Evidence date: 2026-05-29
- Target workflow root: `arcana/x-ray`
- Refresh scope: correct the visual-library plan so structured YAML files become the canonical component and pattern source before schema work.

## Source Signals

```yaml
- id: signal-xray-yaml-library-correction
  source_path: current session user feedback
  signal_type: artifact_drift
  target_artifacts:
    - arcana/x-ray/library/components.md
    - arcana/x-ray/library/patterns.md
    - arcana/x-ray/library/user-shapes-template.md
    - arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md
  claim: "The visual component and pattern library should use YAML as the canonical data shape, with Markdown retained as human-readable reference."
  evidence: "The next schema work needs stable machine-readable component and pattern entries; Markdown-only docs are useful but awkward as the source for validation and renderer consumption."
  confidence: high
  mutation_safety: safe
```

## Target Artifact Inventory

- `arcana/x-ray/library/README.md`
- `arcana/x-ray/library/components.md`
- `arcana/x-ray/library/patterns.md`
- `arcana/x-ray/library/user-shapes-template.md`
- `arcana/x-ray/SKILL.md`
- `arcana/x-ray/README.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md`
- `arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/task-session/TASK-XRAY-VIS-005-RESULT.md`

## Delta Summary

| Delta | Status | Summary |
| --- | --- | --- |
| artifact_drift | proposed | Current docs say "documentation-first" and include component/pattern records in Markdown, but schema-readiness now needs YAML as the canonical library data. |
| route_changed | proposed | Insert `SWU-XRAY-VIS-005B` before `SWU-XRAY-VIS-006A`. |
| status_changed | proposed | Keep `SWU-XRAY-VIS-006A` pending until YAML canonicalization is complete. |

## Proposed Changes

1. Add `TASK-XRAY-VIS-005B` / `SWU-XRAY-VIS-005B` to the visual revision work-pack.
2. Add the x-ray visual library constitution and task-specific constitution pack:
   - `arcana/x-ray/development/XRAY-VISUAL-LIBRARY-CONSTITUTION.md`
   - `arcana/x-ray/development/constitution-pack.md`
3. Add canonical YAML files:
   - `arcana/x-ray/library/components.yml`
   - `arcana/x-ray/library/patterns.yml`
   - `arcana/x-ray/library/user-shapes-template.yml`
4. Update the Markdown files to become human-readable guides that point to the YAML source of truth.
5. Update `arcana/x-ray/SKILL.md` and `arcana/x-ray/README.md` to state that reusable library entries are YAML-backed.
6. Update `SWU-XRAY-VIS-006A` so the lane-model schema remains next after YAML canonicalization, and `SWU-XRAY-VIS-006B` can later validate component/pattern YAML.

## Skipped Changes

- No target artifact mutation was applied because refresh mode is proposal-only by default.
- No JSON Schema was drafted in this refresh. Schema work remains a Task Session follow-up.
- No renderer or adapter implementation was added.

## Validation

Review checks performed:

```bash
sed -n '1,260p' spells/invoke/refresh.md
sed -n '1,280p' arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md
find arcana/x-ray/library -maxdepth 1 -type f -print
```

Refresh output checks to run:

```bash
python3 -m json.tool arcana/x-ray/development/invoke-runs/20260529T135625Z-yaml-library-refresh/refresh-report.json >/dev/null
test -f arcana/x-ray/development/invoke-runs/20260529T135625Z-yaml-library-refresh/REFRESH-PATCH-PROPOSAL.md
```

## Decisions

- Treat YAML as the canonical library data shape.
- Keep Markdown as reference prose and examples.
- Treat the YAML authority rule as constitution-governed, not just a task preference.
- Insert a correction SWU before schema work instead of folding this into schema implementation.

## Unresolved Gaps

- Target artifact gap: YAML files do not exist yet.
- Target artifact gap: work-pack currently routes directly to `SWU-XRAY-VIS-006A`.
- Invoke gap: none.

## Next Route

`task-session to arcana/x-ray/development/invoke-runs/20260529T112301Z-visual-layered-xray/WORK-PACK.md --swu SWU-XRAY-VIS-005B`
