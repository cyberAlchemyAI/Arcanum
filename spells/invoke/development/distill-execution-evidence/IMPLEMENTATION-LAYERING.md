# Implementation Layering: Distill Execution Evidence

## Target And Scope

- Target: Invoke/Distill execution-evidence enforcement
- Scope: public Arcanum spell/sigil contracts, deterministic validation, generated mirrors,
  and one Workbench replay
- Current state: brownfield contracts with an accepted review and no accepted enforcement
  architecture

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether the lifecycle accepts a non-gameable evidence architecture and whether one valid and one fabricated case discriminate. | accepted architecture plus receipt/event schemas, validator kernel, one positive and one fabricated negative | DEC-DEE-001, schemas, runtime event resolution, semantic kernel, two fixtures | all Invoke modes, generated mirrors, Workbench replay | Spellcraft receipt; positive pass; fabricated block | continue, narrow, or stop |
| L1 | After this layer, we know whether active Invoke modes and deferred-mode fail-close behavior compose with the validator. | mode capability table plus active-mode evidence projections and complete fixture set | define/design/plan/handoff/refresh projections; full/validate unsupported; missing-evidence fixture | mirror packaging and Workbench replay | mode fixtures and canonical contract validation | harden or remediate |
| L2 | After this layer, we know whether generated surfaces preserve the canonical contract and the real Workbench package can be replayed without rewriting history. | generated parity plus Workbench replay and superseding record | mirror regeneration, replay, append-only observability, handoff recalculation | wider migration of historical Invoke runs | parity checks; replay receipt; history-preservation check | accept handoff result or remediate |
| L3 | After this layer, we know whether the evidence path is ready for reusable packaging beyond the first replay. | multi-run operational evidence and release decision | documentation, migration policy, release/rollout evidence | scale and external runtime adapters | repeated run corpus and lifecycle audit | package, pilot, or defer |

## Non-Regression Guardrails

- Existing Distill role policy remains intact.
- Historical observability is append-only.
- No `pass` or `flag` unlocks mutation without a validator-owned result.
- Deferred modes remain unsupported until separately implemented.
- Public Arcanum receives no private authority prose.
- Anti-bias remains bounded to qualifying governed subject groups.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether the proposed enforcement architecture becomes an accepted
  Invoke lifecycle contract
- First unit: `SWU-DEE-001`
- Major deferred scope: canonical mutation, runtime implementation, mirrors, and Workbench
  replay
