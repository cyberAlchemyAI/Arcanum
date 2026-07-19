# Task Session Lifecycle Receipt: SWU-DEE-012

## Identity

- Lifecycle owner: `task-session`
- Spell: `invoke`
- Canonical ID: `invoke`
- Source SWU: `SWU-DEE-012`
- Decision: **accept read-only replay validation of the current Workbench package**
- Lifecycle status: resolved

## Accepted Responsibility

`SWU-DEE-012` replays the current `projects/ide-extension` manual-session-bridge plan as an
evidence package. It recomputes the eleven-SWU manifest, resolves every task-session result,
parses checked-in runtime artifacts, verifies approval -> claim -> execution -> result identity,
and byte-preserves the historical execution evidence.

The replay result is evidence-only. It does not rewrite Workbench files, synchronize Craft status,
or authorize the next Task Session route; those belong to DEE-013.

## Binding

Execution owner: Task Session, one SWU only.

Current Workbench package:

- `projects/ide-extension/development/manual-session-bridge-plan/WORK-PACK.md`
- `projects/ide-extension/development/manual-session-bridge-plan/DISTILL-VALIDATION.md`
- `projects/ide-extension/development/manual-session-bridge-plan/IMPLEMENTATION-LAYERING.md`
- `projects/ide-extension/development/manual-session-bridge-plan/EXECUTION-PACK.md`
- `projects/ide-extension/development/manual-session-bridge-plan/INVOKE-RESULT.md`
- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/tasks/`
- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/`

Exact implementation and evidence scope:

- `arcanum/spells/invoke/development/run-distill-workbench-replay-fixture.sh`
- `arcanum/spells/invoke/development/distill-execution-evidence/work-pack/results/SWU-DEE-012-RESULT.md`

Historical predecessor checked by the runner:

- `projects/ide-extension/development/manual-session-bridge-plan/work-pack/evidence/SWU-MSB-011-assets/runtime-artifacts/artifact-run-61e2f724-fd9a-49a9-ad70-3c0a00fbe947-receipt-816aacd8-4619-472c-b963-bf9920dbe1ed-execution-receipt.json`
- its matching `...-result.json` and `...-receipt-...-after.json` artifacts

## Acceptance Conditions

- exactly eleven unique `SWU-MSB-*` rows resolve from the current Workbench manifest;
- every referenced task-session result exists;
- plan, layering, execution-pack, Distill, transport, and dispatch artifacts exist;
- checked-in JSON evidence parses and approval/claim/result identities agree;
- historical predecessor bytes and digest are recorded without mutation;
- the replay emits `pass` or an owned `flag` with `mutation_handoff_allowed=false`;
- the focused Workbench replay Node test passes;
- no Workbench or Craft artifact is rewritten.

## Next Route

`task-session` must bind `SWU-DEE-013` append-only status and route derivation. It remains blocked
and unselected until this replay result is recorded.
