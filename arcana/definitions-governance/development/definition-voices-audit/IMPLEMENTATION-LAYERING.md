---
module: definitions-governance-definition-voices-audit
version: current
status: active
updatedAt: 2026-06-19
docType: implementation-layering
---

# Implementation Layering: Definitions Governance Definition Voices Audit

## Purpose

Define the smallest evidence-backed route for migrating
`definitions/DEFINITIONS.md` to the three-voice definition contract introduced
by `definitions-governance`.

## Source Contract

- Sigil contract: [../../SKILL.md](../../SKILL.md)
- Canonical definitions source: [../../../../definitions/DEFINITIONS.md](../../../../definitions/DEFINITIONS.md)
- Lookup index: [../../../../definitions/DEFINITIONS-INDEX.md](../../../../definitions/DEFINITIONS-INDEX.md)
- Existing drift audit: [../../../../definitions/DEFINITION-DRIFT-AUDIT.md](../../../../definitions/DEFINITION-DRIFT-AUDIT.md)
- DomainSpec explanatory layers:
  [../../../../definitions/TAXONOMY.md](../../../../definitions/TAXONOMY.md),
  [../../../../definitions/RELATIONSHIPS.md](../../../../definitions/RELATIONSHIPS.md)
- Arcanum reader context: [../../../../development/user-guide/README.md](../../../../development/user-guide/README.md)

## Target And Scope

- Target: `definitions/DEFINITIONS.md`
- Scope: semantic-governance migration
- Current state: brownfield canonical definitions source with partial plain-language intuition and missing explicit domain-context voices.

## Layer Boundary Rule

Use this sentence for every layer boundary:

```text
After this layer, we know whether {decision unlocked}.
```

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 (POC) | After this layer, we know whether every current canonical definition can carry scientific/formal, plain-language, and Arcanum domain-context voices without changing its authority. | Audit all current definition IDs and add missing voice sections in place. | `definitions/DEFINITIONS.md`, index governance notes, audit report. | Downstream drift remediation in consumer artifacts. | Voice-completeness check, markdown link check, diff review. | Continue if every indexed definition has all three voices. |
| L1 | After this layer, we know whether downstream explanatory layers still point at the canonical source without redefining it. | Review `TAXONOMY.md`, `RELATIONSHIPS.md`, and existing drift targets. | Consumer drift report updates only. | Broad downstream edits. | Drift report with exact targets. | Harden or defer by drift severity. |
| L2 | After this layer, we know whether definition voice completeness can be validated repeatably. | Add or adapt a lightweight structure check. | Optional validation script or documented command. | Full schema for all definition files. | Repeatable command output. | Add validator when repeated audits justify it. |
| L3 | After this layer, we know whether the pattern should be packaged for other repositories. | Create migration guidance or template. | Documentation/template only. | Automated migration. | Reusable migration notes. | Package only after at least one more real migration. |

## Non Regression Guardrails

- The scientific/formal voice must preserve existing normative semantics.
- Plain-language and domain-context voices are non-normative aids.
- Domain context may cite Arcanum `development/user-guide/` only for this repository.
- Existing definition IDs and index anchors must remain stable.
- DomainSpec `TAXONOMY.md` and `RELATIONSHIPS.md` remain explanatory layers, not authority.

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: every current canonical definition can satisfy the new three-voice contract without semantic promotion or downstream mutation.
- Major deferred scope: downstream drift remediation and reusable validator packaging.
