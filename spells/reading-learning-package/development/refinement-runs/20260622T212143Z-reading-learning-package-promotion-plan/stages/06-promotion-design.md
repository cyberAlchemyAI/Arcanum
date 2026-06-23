# Stage 06: Promotion Design

Status: pass
Owner: `invoke`
Mode: design

## Patch Set Design

| Patch Area | Files | Notes |
| --- | --- | --- |
| Registry | `arcanum/registry/SPELLS.md` | Add `Reading Learning Package` row. |
| Spell evidence | `arcanum/spells/reading-learning-package/development/` | Add final promotion receipt after validation. |
| Generated surfaces | parent `.agents/skills/`, `.claude/skills/`, `.github/skills/` or target-local mirrors selected by bootstrap profiles | Sync only after temporary-target validation proves expected files. |
| Publication | `arcanum` submodule, then parent gitlink | Commit/push public submodule first, then parent after `make bump-check`. |

## Runtime Surface Strategy

1. Run bootstrap into a temporary target with:

   ```bash
   bash arcanum/tools/bootstrap_arcanum.sh \
     --target <tmp> \
     --sigils none \
     --spells reading-learning-package \
     --profile repo-codex,claude \
     --force
   ```

2. Verify generated spell package metadata:
   - `name: reading-learning-package`;
   - `canonical_source: spells/reading-learning-package/README.md`;
   - runtime/profile metadata matches the selected surface.

3. Use the temporary target result to decide the exact mirror paths to sync.

## Authority Design

- `spellcraft` owns promotion readiness.
- `experiment-harness` owns reusable fixture mechanics.
- `task-session` owns optional renderer integration.
- `domainspec-core` owns parent gitlink publication.

## Design Boundary

The promotion patch must not modify `research-tower`, `whisper`, unrelated
spells, or generated learning outputs except for validation timestamp refreshes
caused by rerunning fixtures.

