# Invoke Transport

## Authored target

- Artifact: Work-Pack Execution Grant
- Type: cross-capability extension of the existing
  `implementation-readiness` spell
- Lifecycle owner: Spellcraft
- Supporting lifecycle owners: Sigil Development for Continuation Router and
  Task Session; Task Session for one selected SWU

## Handoff frame

- Work Pack: `WORK-PACK.md`
- Dispatch: `work-pack-execution-grant.dispatch.json`
- First candidate: `SWU-WPEG-001`
- Selected SWU: none
- Write scopes: task-local paths only
- Current dirty-worktree rule: inventory exact overlapping targets and preserve
  existing changes before every implementation SWU

## Route

```text
Invoke authored package
  -> Spellcraft admits/updates implementation-readiness composition
  -> lifecycle-owned sigil updates
  -> one bounded Task Session per selected SWU
  -> owner closeout and fresh successor selection
```

Once the Work Pack execution begins, these internal owner/tool hops are
automatic under the plan's execution policy. Stop only on the explicit stop
classes in `SPEC.md`.

## Claim boundary

This transport is not implementation, selection, promotion, publication,
release, deployment, or production proof.

