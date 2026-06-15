# Glossary Consistency: Craft Feature Readiness Indexes

## Status

- Phase status: `pass`
- Candidate glossary promotion: none
- Canonical definition mutation: none

## Terms

| Term | Local Meaning | Consistency Notes |
| --- | --- | --- |
| execution-readiness index | Optional Craft ledger index family that points to executable artifacts, ready SWUs, approvals, execution modes, worktrees, and blocked scopes. | Consistent with Craft's existing index model because it is derived lookup data, not source authority. |
| current execution target | The artifact or SWU that a future executor should select first. | Must point to an artifact ID, path, or SWU ID; must not imply execution happened. |
| work-pack gate status | A compact pass/flag/block status copied or linked from the work-pack readiness gate. | Mirrors Invoke output; Craft should not recompute it. |
| ready SWU IDs | SWUs that are currently selectable for bounded execution. | Comes from Invoke plan or work-pack; Craft records references only. |
| approval record | Decision or artifact that authorizes a specific execution scope. | Fits existing `decision_type: approval` and artifact link patterns. |
| execution mode | The allowed mode for the current target, such as documentation-only, local-static, fixture-only, runtime-mutation, publication, or CI-promotion. | Local enum should remain open string initially to avoid overfitting examples. |
| product worktree | The repository or nested worktree where mutation would happen. | Optional; needed when Craft coordination scope differs from product git status scope. |
| blocked mutation scope | Mutation classes not allowed under the current approval. | Must remain explicit so local/static work is not confused with app/runtime mutation. |
| blocked publication scope | Publication actions not allowed under the current approval, such as commit, push, PR, release, or CI promotion. | Optional companion to blocked mutation scope. |

## Conflicts

No term conflict requires canonical glossary mutation. The update should keep all terms local to Craft until there is broader cross-sigil evidence for promotion.
