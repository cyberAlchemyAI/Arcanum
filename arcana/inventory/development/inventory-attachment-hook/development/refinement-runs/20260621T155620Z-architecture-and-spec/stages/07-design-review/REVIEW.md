---
module: inventory-attachment-hook
runId: 20260621T155620Z-architecture-and-spec
stage: s7-design-review
status: flag-repaired
updatedAt: 2026-06-21
docType: interrogation-design-review
---

# Design Review: Architecture And Spec

## Mode

`refine-design-review`

## Subagent Lifecycle

| Role | Agent | Spawn | Join | Close | Verdict |
| --- | --- | --- | --- | --- | --- |
| inventory-contract-architect | `019eeaed-ae2b-7f01-8521-c9a314259e88` | spawned | completed | closed | flag |
| runtime-handoff-skeptic | `019eeaed-aed4-70f0-83e5-ac8c31231622` | spawned | completed | closed | flag |
| promotion-boundary-reviewer | `019eeaed-b092-71f0-9990-93cc1d474c37` | spawned | completed | closed | flag |

## Review Findings

| Finding | Source Role | Repair |
| --- | --- | --- |
| Per-output idempotency was inconsistent with the envelope example. | runtime-handoff-skeptic | Moved idempotency keys into `selected_outputs[]` and documented partial dedupe. |
| Disabled/absent policy was mixed with invalid attempted handoff. | runtime-handoff-skeptic | Added Attachment Attempt Decision: absent/disabled skips before envelope validation. |
| Observed Invocation Loop insertion point was not explicit enough. | runtime-handoff-skeptic | Added OIL insertion sequence after envelope/primary telemetry and before closeout. |
| Attachment operations could recursively attach themselves. | runtime-handoff-skeptic | Added recursion guard for attachment operations, Inventory writes, hook rows, failures, and dedupe rows. |
| Observed Invocation generated mirror scope was optional. | runtime-handoff-skeptic | Made observed-invocation mirror deterministic when OIL docs change. |
| `publicBoundary: inherit` needed resolution rules. | promotion-boundary-reviewer | Added resolution order and block rule for unresolved public writes. |
| Draft docs needed explicit non-authority status. | promotion-boundary-reviewer | Added non-authoritative-until-canonical-source note to architecture and spec. |
| `promotionOwner` did not match Inventory vocabulary. | inventory-contract-architect | Normalized to `promotion_owner`. |
| Weak source refs needed confidence/residue behavior. | inventory-contract-architect | Added `source_ref_strength`, confidence/residue routing, and material-claim rules. |
| Inventory mapping did not define evidence-card/EvidenceSet population. | inventory-contract-architect | Added evidence-card and EvidenceSet mapping table. |
| Validation needed schema/fixture checks beyond grep. | inventory-contract-architect | Added validation requirements for vocab, source refs, non-authority text, per-output dedupe, public boundary, and EvidenceSet refs. |

## Remaining Residue

| Residue | Owner | Route |
| --- | --- | --- |
| Canonical `inventoryAttachment` anchors do not yet exist in `inventory/SKILL.md`. | Inventory | `SWU-IAH-001` |
| OIL canonical docs do not yet include the Inventory attachment phase. | Observed Invocation Loop | `SWU-IAH-004` |
| Templates and fixtures do not yet exist. | Inventory | `SWU-IAH-005` |
| Generated mirrors still need regeneration after canonical edits. | bootstrap/runtime generation | `SWU-IAH-006` |

## Verdict

Initial role verdicts were `flag`. After repair, the architecture/spec packet is
safe to use as pre-implementation guidance. It is not a live canonical contract
until the canonical sources are patched and generated mirrors are refreshed.
