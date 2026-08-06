# Task Session reflection: Work Pack fast-entry runner bridge

## Trigger

Severe gap. A real `SWU-APE-ONT-001` run reached `TASK_READY` through the
Work Pack execution binding, but the governance runner still required one
legacy prose `selected` row. The new bounded execution feature therefore
stopped before its first intended implementation mutation.

## Signals

- The fast guard read the declared four logical inputs and returned a
  zero-mutation `TASK_READY` receipt.
- The outer loop selected one bounded Task Session route with zero additional
  authorization prompts.
- Plan selection, material package, mutation admission, and target baselines
  were current.
- The governance runner ignored that evidence and reparsed Work Pack prose.

## Targeted update

- Add a `work-pack-fast-entry` governance request profile.
- Require exact references to both the fast-entry request and receipt.
- Revalidate the receipt against the request, not by receipt shape alone.
- Bind selected SWU, Work Pack path, Task Session route, write scope, expected
  terminal receipt, plan selection, and single-use mutation admission.
- Preserve the legacy prose-selected-row behavior when the new profile is not
  selected.
- Exercise canonical and generated-package runtime layouts.

## Rejected changes

- Do not add a duplicate `selected` row to the APE Work Pack.
- Do not treat a digest-correct receipt as proof of legitimate derivation when
  the original guard request is absent.
- Do not weaken live baseline, validation, admission consumption, or closeout
  checks.
- Do not make Work Pack fast entry the universal default.

## Validation expectation

Positive fast-entry execution and legacy selection must both pass. Stale
request, stale receipt, selected-unit mismatch, expanded write scope, and
single-use replay must block before prohibited writes. Generated Codex and
Claude packages must resolve the sibling Implementation Readiness contracts
and run the same guard/runner tests.

## Next trigger

Reflect again after five real Work-Pack-bound Task Session executions or any
new failure that bypasses a declared owner, scope, baseline, or admission gate.
