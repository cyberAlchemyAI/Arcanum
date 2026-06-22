---
module: definitions-governance-definition-voices-audit
version: current
status: active
updatedAt: 2026-06-19
docType: work-pack
---

# WORK-PACK: Definitions Governance Definition Voices Audit

## Purpose

Canonical executable plan for auditing and migrating
`definitions/DEFINITIONS.md` to the three-voice definition contract.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | Single ready SWU has source anchors, write scope, done criteria, and validation surface. |
| complexity | low | One canonical source and one lookup index; no cross-repository mutation. |
| outputMode | single-file | Split task files are unnecessary for one SWU. |
| executionPackRef | n/a | Low-complexity local execution. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | L0 selected. |
| activeLayerWindow | L0 | Voice completeness migration. |
| lastUpdatedAt | 2026-06-19 | Task Session completed `SWU-DVA-001`. |
| readinessProfile | pilot | First real migration of the new definition voice model. |

## Objective Summary

- Objective: Make every current canonical definition in
  `definitions/DEFINITIONS.md` visibly carry scientific/formal, plain-language,
  and domain-context voices.
- Primary inputs: `definitions-governance` SKILL contract, canonical definitions
  source, lookup index, existing drift audit, DomainSpec explanatory layers, and
  Arcanum user-guide context.
- Success condition: all indexed definition IDs have all three voices, stable
  IDs and anchors are preserved, index notes are synchronized, and validation
  checks pass.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| Three-voice sigil contract | SWU done criteria | Every definition must expose scientific/formal, plain-language, and domain-context voices. |
| Canonical source and index | Write scope and validation | Preserve IDs and anchors; update only governance notes if needed. |
| Existing explanatory layers | Domain context anchors | Use as local context, not normative replacement. |
| Existing drift audit | Deferred scope | Do not remediate downstream consumers in this SWU. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-DVA-001 | Canonical definitions file has complete three-voice sections for every indexed definition. | L0 | W0 | none | voice-completeness check, markdown link check, diff check |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-DVA-001 | Audit and migrate `definitions/DEFINITIONS.md` for three-voice completeness. | L0 | low | W0 | [definitions/DEFINITIONS.md](../../../../definitions/DEFINITIONS.md), [definitions-governance SKILL](../../SKILL.md) | pass | completed |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-DVA-001 | TASK-DVA-001 | `definitions/DEFINITIONS.md` headings `DEF-ARC-*`, `DS-D*`, `DS-P*`; `definitions/DEFINITIONS-INDEX.md` terms table; `arcana/definitions-governance/SKILL.md` definition-voice-model | `definitions/TAXONOMY.md`, `definitions/RELATIONSHIPS.md`, `development/user-guide/README.md`, existing `DEFINITION-DRIFT-AUDIT.md` | none | `definitions/DEFINITIONS.md`, `definitions/DEFINITIONS-INDEX.md`, `definitions/DEFINITION-DRIFT-AUDIT.md`, this development run folder | Each indexed definition has scientific/formal, plain-language, and domain-context voices; plain/domain voices are non-normative; IDs and anchors remain stable. | [AUDIT-REPORT.md](AUDIT-REPORT.md) and [task-session report](task-session-20260619T170113Z/TASK-SESSION-REPORT.md). | Perl voice-completeness check, markdown link checks, `git diff --check`. | local-fallback | completed |

## Completion Evidence

| Evidence | Result |
| --- | --- |
| [AUDIT-REPORT.md](AUDIT-REPORT.md) | 11 indexed definitions complete with 3 voices. |
| [task-session-20260619T170113Z/TASK-SESSION-REPORT.md](task-session-20260619T170113Z/TASK-SESSION-REPORT.md) | Task Session PASS. |
| Voice-completeness check | `PASS definitions=11 voices=3`. |
| Markdown link checks | pass for `DEFINITIONS.md` and `DEFINITIONS-INDEX.md`. |
| `git -C arcanum diff --check` | pass. |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| none | n/a | No blocker-level decisions identified. | n/a | n/a | n/a |

## Gate Checks

1. `workPackGateStatus` must be pass before mutation-capable execution.
2. The task must not rewrite definition IDs or heading anchors.
3. The task must not promote local glossary terms.
4. The task must not mutate generated runtime skill packages.
5. Downstream consumer remediation remains deferred unless validation shows an immediate broken link.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-19 | Initial work-pack created by Invoke plan. | Codex |
| 2026-06-19 | Completed `SWU-DVA-001` through Task Session. | Codex |
