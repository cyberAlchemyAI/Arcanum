# Invoke Handoff: Refine Aggregate Receipt Model

## Identity

| Field | Value |
| --- | --- |
| spell | `invoke` |
| mode | `handoff` |
| handoff_type | `new-lifecycle-thread` |
| source_session_reference | current Craft/Refine aggregate receipt session, ending 2026-06-07 |
| target_lifecycle_owner | `arcana/refine` |
| target_development_pack | `arcana/refine/development/` |
| target_thread_label | Refine aggregate receipt model hardening |
| phase_status | pass |

## New Session Prompt

Continue Refine development inside `arcana/refine/development/`.

The current Craft run exposed a contract problem: Refine was drifting into one
receipt per internal stage (`Context Builder`, `Invoke Define`, `Interrogation`,
`Distill`, etc.). The operator decided that Refine should be treated as one
receipt-bearing capability. Internal Refine stages should remain internal
evidence, not standalone receipt gates.

Create the Refine-owned development plan/work-pack for this aggregate receipt
model, then route execution through `task-session`.

## Handoff Type And Route Rationale

This is a `new-lifecycle-thread` handoff, not direct execution.

Reason:

- The Craft session already proved the immediate artifact shape by creating an
  aggregate Refine receipt for one live run.
- The reusable Refine contract, templates, validator expectations, generator,
  examples, and development validation need a Refine-owned plan before mutation.
- Existing `WORK-PACK-DISPATCH-STABILITY.md` is completed and does not own this
  new aggregate receipt model change.

Recommended next route:

```text
invoke plan arcana/refine aggregate receipt model hardening
```

Then:

```text
task-session to arcana/refine/development/<new aggregate receipt work-pack> --task <first ready task>
```

## Context Builder Selection Summary

Selected context is obligation-linked to the next Refine development thread:

| Obligation | Coverage | Selected Evidence |
| --- | --- | --- |
| Preserve the user's route decision. | pass | `docs/decisions/craft-distill-receipt-route.md` selects `Option D: Single Refine Receipt`. |
| Preserve live proof from Craft. | pass | `development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-RECEIPT.md` and `receipts/refine-run.json`. |
| Preserve task-session outcome. | pass | `development/craft/task-sessions/20260607T175719Z-CRAFT-REFINE-SINGLE-RECEIPT-001-RESULT.md`. |
| Identify current Refine contract conflict. | pass | `arcana/refine/SKILL.md` still describes native runtime stage receipts and stage evidence as the execution model. |
| Locate active Refine development pack. | pass | `arcana/refine/development/WORK-PACK-DISPATCH-STABILITY.md` is completed and can be used as precedent, not as the active owner for this new change. |
| Preserve boundaries. | pass | Craft promotion remains deferred; command-surface evidence is historical; canonical registry/runtime mutation needs explicit approval. |

Context Builder coverage status: `pass`.

## Selected Session Context

### User Decision

```text
i think we should continue this, but treat refine as just 1 receipt
```

### Decision Record

`docs/decisions/craft-distill-receipt-route.md` now records:

- result: `PASS`
- selected option: `Option D: Single Refine Receipt`
- rationale: Refine should be the receipt-bearing unit; internal stages become
  evidence inside one aggregate Refine receipt.

### Live Craft Evidence

The Craft run now contains:

```text
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-RECEIPT.md
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json
```

The aggregate receipt status is `block`, because internal Refine work remains
incomplete. That is an honest result, not a failure of the handoff.

Important current route:

```text
continue the current Refine run under the aggregate receipt model;
Distill is internal evidence, not a standalone receipt gate
```

### Refine Development Context

Current Refine surfaces still contain stage-receipt language:

- `arcana/refine/SKILL.md` objective says Refine should run or hand off
  validated route through native runtime stage receipts.
- required capabilities require each stage capability to provide its own
  evidence.
- run-manifest contract requires stage artifacts and an evidence index.
- templates and examples expect per-stage evidence.

Existing dispatch stability work is completed:

```text
arcana/refine/development/WORK-PACK-DISPATCH-STABILITY.md
```

Use it as precedent for planning style, SWU shape, and validation strategy, but
do not reopen it as if this aggregate receipt model were already covered.

## Excluded Context

| Excluded Context | Reason |
| --- | --- |
| Full Craft architecture history. | Not needed for the Refine receipt model correction. |
| Old Codex Goal wording in historical Refine artifacts. | Already marked historical by dispatch-stability work; not the current blocker. |
| Unrelated inventory or dispatch-spec local dirty files. | Outside this handoff boundary. |
| Craft promotion readiness details beyond deferral. | Promotion remains deferred and should not be mutated in this thread. |

## Target Lifecycle Boundary

The next thread is Refine development work, not Craft promotion and not runtime
adapter implementation.

Allowed target scope for the next plan:

- `arcana/refine/SKILL.md`
- `arcana/refine/README.md`
- `arcana/refine/REFINEMENT-LOOP.md`
- `arcana/refine/templates/`
- `arcana/refine/scripts/generate-refine-dispatch.py`
- `arcana/refine/development/`
- focused dispatch-spec fixture or validator updates only if the aggregate
  receipt model requires schema/validation support.

Out of scope unless separately approved:

- canonical registry promotion,
- runtime adapter mutation,
- command-surface resurrection as execution authority,
- Craft promotion,
- broad rewrite of unrelated historical Refine development artifacts.

## Gaps And Blockers

| ID | Gap Or Blocker | Status | Next Action |
| --- | --- | --- | --- |
| REFINE-AGG-001 | Refine contract still describes active stage-receipt execution. | open | Plan how to represent a single aggregate Refine receipt while retaining internal stage evidence. |
| REFINE-AGG-002 | Templates do not yet include an aggregate receipt artifact. | open | Add or revise templates after plan approval. |
| REFINE-AGG-003 | Dispatch generator/validator expectations may still assume stage receipt requirements. | open | Audit generator output and dispatch-spec validation before mutation. |
| REFINE-AGG-004 | Existing live examples expect per-stage evidence. | open | Add fixture coverage for aggregate receipt behavior. |
| REFINE-AGG-005 | Craft proof is one live case only. | non-blocking | Use as seed evidence, not as promotion proof. |

No blocker prevents starting the Refine development lifecycle.

## Next-Session Start Prompt

```text
We are continuing Refine development inside /home/vrondelli/projects/domainspec-core/arcanum/arcana/refine/development.

Use the handoff at arcana/refine/development/REFINE-AGGREGATE-RECEIPT-HANDOFF.md.

Goal: turn the aggregate Refine receipt decision into a governed Refine-owned plan/work-pack. The user decided that Refine should be treated as one receipt-bearing capability. Internal stages such as Distill, Invoke Design, Design Review, Distill Repair, Invoke Plan, and Final Synthesis should be internal Refine evidence, not standalone receipt gates.

Start by using invoke plan or equivalent governed planning to create a new Refine development work-pack for the aggregate receipt model. Do not mutate Refine SKILL/templates/scripts until that plan names the write scope, validation surface, and task order.
```

## Provenance And Output Paths

Handoff artifact:

```text
arcana/refine/development/REFINE-AGGREGATE-RECEIPT-HANDOFF.md
```

Primary source artifacts:

```text
docs/decisions/craft-distill-receipt-route.md
development/craft/CRAFT-REFINE-SINGLE-RECEIPT-WORK-PACK.md
development/craft/task-sessions/20260607T175719Z-CRAFT-REFINE-SINGLE-RECEIPT-001-RESULT.md
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/REFINE-RECEIPT.md
development/craft/development/refinement-runs/20260601T080122Z-context-builder-receipt-proof/receipts/refine-run.json
arcana/refine/SKILL.md
arcana/refine/development/WORK-PACK-DISPATCH-STABILITY.md
```

## Invoke Result

- Mode: `handoff`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: library
- Phase status: `pass`
- Mode contract: `spells/invoke/handoff.md`
- Outputs: `arcana/refine/development/REFINE-AGGREGATE-RECEIPT-HANDOFF.md`
- Handoff type: `new-lifecycle-thread`
- Source session: current Craft aggregate receipt session
- Context Builder coverage: `pass`
- Next-session prompt: included above
- Decisions: single Refine receipt model already selected
- Unresolved gaps: aggregate receipt model plan and implementation gaps listed above
- Next route: `invoke plan`, then `task-session`
