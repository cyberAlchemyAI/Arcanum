# Stage 03: Promotion Gap Ledger

Status: pass-with-flags
Owner: `interrogation`
Mode: refine-review

## Open Gaps

| ID | Gap | Severity | Owner | Repair Route |
| --- | --- | --- | --- | --- |
| G-RLP-PROMO-001 | `Reading Learning Package` is not listed in `arcanum/registry/SPELLS.md`. | blocker for discoverable promotion | `spellcraft` | Add a registry row after confirmation. |
| G-RLP-PROMO-002 | Bootstrap install for `--spells reading-learning-package` has not been captured as a promotion receipt. | blocker for runtime-surface promotion | `spellcraft` / `bootstrap_arcanum.sh` | Validate against a temporary target before syncing mirrors. |
| G-RLP-PROMO-003 | Generated runtime mirrors are not synchronized as part of this promotion. | blocker for generated-surface claim | `bootstrap_arcanum.sh` | Sync only the standard profiles proven by temporary-target validation. |
| G-RLP-PROMO-004 | Final promotion receipt does not yet exist. | blocker for release audit | `spellcraft` | Add a promotion receipt under `development/` after validation. |
| G-RLP-PROMO-005 | Submodule-first commit and parent gitlink publication have not run. | blocker for published promotion | `domainspec-core` | Commit/push `arcanum`, run `make bump-check`, then commit/push parent. |
| G-RLP-PROMO-006 | Optional aliases are undecided. | non-blocking | maintainer | Default to no aliases unless a maintainer selects one. |
| G-RLP-PROMO-007 | Deterministic PDF renderer is not integrated. | non-blocking | `task-session` | Defer; HTML fallback behavior is validated. |

## Verdict

Promotion is ready to execute after confirmation. The open blockers are concrete
release steps, not design unknowns.

