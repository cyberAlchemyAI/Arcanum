---
module: whisper-readability-dynamics
version: current
status: draft
updatedAt: 2026-06-23
docType: implementation-layering
---

# Implementation Layering: Whisper Readability Dynamics

## Purpose

Define the layer sequence for adding paragraph-density and readability
governance to Whisper without overloading the first execution step or silently
mutating the reusable spell contract.

## Source Contract

- Invoke plan contract: `.agents/skills/invoke/plan.md`
- Prior refinement: `arcanum/spells/whisper/development/refinement-runs/20260531T164421Z-readability-dynamics/`
- Target lifecycle owner: `spellcraft` for Whisper spell revision acceptance.

## Target And Scope

- Target: `whisper`
- Scope: reusable library spell readability layer
- Current state: brownfield, partially designed, not implemented in canonical spell contract

## Layer Boundary Rule

Each layer answers:

```text
After this layer, we know whether <decision unlocked>.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether readability density can be governed non-breakingly by substrate and validator. | `SWU-WHISPER-READABILITY-001` | Optional `readability_dynamics` schema in one test substrate plus validator-only checks. | Renderer beats, browser review validation, canonical spell README mutation. | YAML parse, existing validator checks still pass, readability flags appear for known dense drafts. | Continue to Spellcraft validation, then L1 renderer if evidence is useful. |
| L1 | After this layer, we know whether rhythm units can improve review HTML while preserving anchors. | `SWU-WHISPER-READABILITY-002` | Beat/rhythm rendering, child anchors, review payload extension. | Cross-transport tuning and publication promotion. | Review HTML renders old and beat-enabled drafts with stable payloads. | Harden renderer or roll back to validator-only. |
| L2 | After this layer, we know whether browser review and revision loops can consume beat-level evidence. | `SWU-WHISPER-READABILITY-003` and `004` | Localhost browser checks, Playwright payload extraction, targeted revision from comments. | Reusable fixture suite and canonical promotion. | Desktop/mobile checks plus extracted payload used in a revision plan. | Promote to reusable validation examples or revise thresholds. |
| L3 | After this layer, we know whether the layer is portable across Whisper transports. | Experiment harness suite | Multiple transport fixtures, docs, promotion report. | Advanced academic metrics. | Experiment report across Substack, presentation, and site/page copy examples. | Promote contract update or keep as optional profile. |

## Non Regression Guardrails

- Existing substrates without `readability_dynamics` must validate as before.
- Existing review payload fields remain stable.
- Paragraph density cannot become word-count-only policing.
- Spellcraft must accept lifecycle changes before canonical Whisper contract
  mutation.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether validator-only readability governance is useful
  and non-breaking.
- Major deferred scope: renderer, browser validation, and canonical contract
  promotion.

