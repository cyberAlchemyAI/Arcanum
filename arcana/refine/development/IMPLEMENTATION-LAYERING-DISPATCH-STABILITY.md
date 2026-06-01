---
module: refine-dispatch-stability
version: current
status: draft
updatedAt: 2026-05-29
docType: implementation-layering
---

# Implementation Layering: Refine Dispatch Stability

## Purpose

Plan the selected Refine hardening improvements:

1. Sync installed skill / command surface.
2. Refresh stale development docs.
4. Add overlay-specific validator fixtures.
5. Add a dispatch generator.

This is an Invoke `plan` artifact. It does not execute source mutation.

## Source Contract

- Invoke plan contract: [../../../spells/invoke/plan.md](../../../spells/invoke/plan.md)
- Refine contract: [../SKILL.md](../SKILL.md)
- Refine loop: [../REFINEMENT-LOOP.md](../REFINEMENT-LOOP.md)
- Dispatch Spec contract: [../../../formulae/dispatch-spec/SKILL.md](../../../formulae/dispatch-spec/SKILL.md)
- Dispatch validator: [../../../formulae/dispatch-spec/scripts/validate-dispatch.py](../../../formulae/dispatch-spec/scripts/validate-dispatch.py)

## Target And Scope

- Target: `arcana/refine`
- Scope: sigil hardening and validation support
- Current state: pilot, architecturally coherent, still flagged by stale live output and stale development surfaces

## Layer Boundary Rule

```text
After this layer, we know whether the dispatch-route Refine contract is consistently represented, validated, and executable by the next owner.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether installed/runtime-facing Refine surfaces match the repo-local dispatch contract. | Sync skill and command docs to `REFINE-DISPATCH.json` / `RUNTIME-HANDOFF.md` vocabulary. | `.codex/commands/refine.md`, `.codex/commands/arcanum-sigil-refine.md`, `arcana/refine/development/codex-skill-install/SKILL.md`, installed skill handoff note. | Live rerun. | No stale `GOAL-HANDOFF` / Codex Goal wording in active surfaces. | Continue to doc refresh if sync passes. |
| L1 | After this layer, we know whether historical development docs no longer read as current guidance. | Refresh current-facing docs and mark historical Codex Goal material explicitly as superseded or historical. | `arcana/refine/development/*.md`, examples/regimes/fixtures that influence validation. | Deep rewrite of old session archaeology. | Targeted grep shows stale wording only in archived/historical contexts. | Continue to validator fixture hardening. |
| L2 | After this layer, we know whether every dispatch technique overlay has executable validation coverage. | Add one pass/block/flag fixture family for overlay behavior. | Dispatch-spec fixtures for route menu, dialectic, tournament, x-ray, toy-game, memory, protected-context. | Full semantic Refine execution. | `formulae/dispatch-spec/development/run-validation-fixtures.sh` passes and proves overlay-specific failures. | Continue to generator only if fixture matrix catches intended errors. |
| L3 | After this layer, we know whether Refine can materialize a dispatch route from seed + selected overlays without hand editing JSON. | Add deterministic generator and fixture smoke. | Script, generator fixtures, docs, Refine validation wrapper integration. | Model-backed nested runtime execution and fresh live example rerun. | Generator output validates with `validate-dispatch.py`; Refine fixture wrapper consumes generated route. | Ready for Task Session execution of fresh live example. |

## Non Regression Guardrails

- Do not remove the canonical ten-stage Refine loop.
- Do not reintroduce `GOAL-HANDOFF.md` as the current required artifact.
- Do not treat dispatch validation as proof that semantic stage execution completed.
- Do not let technique overlays become decorative labels; each overlay needs a validation consequence.
- Do not mutate registry or lifecycle promotion state in this plan.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether every active user-facing Refine surface points to the dispatch-route contract.
- Major deferred scope: rerunning the stale live example after the plan is implemented.
