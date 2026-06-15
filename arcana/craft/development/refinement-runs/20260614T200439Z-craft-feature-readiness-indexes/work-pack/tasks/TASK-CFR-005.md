# TASK-CFR-005: Regenerate Surfaces And Prepare Publication Gates

## Goal

After canonical Craft source edits pass, regenerate generated runtime surfaces and prepare submodule-safe publication checks.

## Layer

L3 Runtime Surface Sync

## Source Contracts

- [../../IMPLEMENTATION-LAYERING.md](../../IMPLEMENTATION-LAYERING.md)
- [../../../../../SKILL.md](../../../../../SKILL.md)
- Repository `AGENTS.md` submodule discipline.

## Inputs

- Completed canonical Craft source edits.
- Validation evidence from `TASK-CFR-004`.
- Current bootstrap/generation scripts.

## Implementation Detail

1. Generate runtime surfaces from canonical `arcana/craft` sources, using the repository's current bootstrap path.
2. Copy generated `craft` packages only into the appropriate generated surfaces.
3. Do not hand-edit generated copies.
4. Grep generated copies for readiness contract terms.
5. Run `git diff --check`.
6. If publishing is requested, commit and push inside `arcanum` first.
7. Run parent `make bump-check` before committing or pushing the parent gitlink.

## Edge Cases

- If the generator path changes, record the exact command used in the result artifact.
- If generated surfaces include stale text, fix canonical source or generator inputs, not generated copies.
- Parent publication must not reference an unpushed submodule commit.

## Smallest Working Units

| SWU | Work | Acceptance |
| --- | --- | --- |
| `SWU-CFR-007` | Regenerate runtime surfaces. | Generated Craft copies include readiness contract terms. |
| `SWU-CFR-008` | Run submodule-safe publication checks. | `git diff --check` passes; `make bump-check` passes before parent publication. |

## Verification

```bash
rg -n "execution_readiness|approval_record|blocked_mutation_scope" .agents/skills/craft .claude/skills/craft
git diff --check
make bump-check
```

## Done When

- Generated surfaces match canonical source.
- Publication gates are ready, or exact blockers are recorded.
