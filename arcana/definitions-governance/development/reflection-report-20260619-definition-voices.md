# Sigil Reflection Report

## Reflection Context

- Sigil: definitions-governance
- Tier: arcana
- Reflection trigger: manual
- Signals reviewed: 4 sources; user request, canonical SKILL, canonical README, registry/tier docs
- Period or usage window: 2026-06-19 targeted maintenance turn
- Observer pass: local fallback

## Signal Summary

| Signal Type | Count | Notes |
| ----------- | ----- | ----- |
| Meaningful executions | 1 | User requested a sigil-development improvement to definitions-governance. |
| Generated outputs | 0 | No prior output body was provided for this reflection. |
| Quality Bar failures | 1 | Existing Quality Bar required colocated plain-language intuition but not a domain-context voice for every definition. |
| Anti-Pattern hits | 0 | No observed misuse in a produced artifact. |
| Workflow gaps | 1 | The process covered formal constructs but did not require a complete three-voice definition package for all canonical definitions. |
| Output-contract drift | 1 | The summary contract did not report whether definition voices were complete or which domain context surface was used. |
| User corrections | 1 | User clarified that every definition needs at least scientific/formal, plain-language, and domain-context language. |

## Patterns Found

- The existing sigil already separated normative definitions from explanatory intuition, so the core authority contract was sound.
- The interpretation package was too narrow because it primarily named formal or mathematical constructs.
- Domain context needed a consuming-workspace boundary so Arcanum's `development/user-guide/` can help Arcanum readers without becoming a universal example authority.

## Gap Analysis

| Gap | Severity | Evidence | Affected Contract Area | Recommended Response |
| --- | -------- | -------- | ---------------------- | -------------------- |
| Missing required domain-context voice | medium | User request plus current SKILL process and Quality Bar | process / quality-bar / anti-pattern | Add an explicit three-voice definition model and audit checks. |
| Output did not report voice completeness | medium | Current output contract omitted voice and context-surface status | output-contract | Add `Definition voices complete` and `Domain context surface` fields. |

## Proposed Iterations

- Add a `definition-voice-model` section naming scientific/formal, plain-language, and domain-context voices.
- Update process, authority rule, Quality Bar, and Anti-Patterns so all definitions carry the three voices.
- Update README with human-facing explanation of the voice model and the Arcanum user-guide tie-in.

## Rejected Changes

- Updating `definitions/DEFINITIONS.md`: rejected because the request targets the sigil contract, not a definition migration.
- Treating Arcanum `development/user-guide/` as universal context: rejected because consuming repositories must resolve their own workspace context.
- Renaming the concept to literal natural languages: rejected because the user examples describe explanatory voices rather than translation locales.

## Contract Preservation

- Core contract preserved: yes
- If no, justification: n/a
- Compatibility impact: minor; future runs must audit one extra completeness dimension.

## Updated Reflection Policy

- Next manual review condition: user asks to inspect actual canonical definitions for three-voice completeness.
- Usage threshold: 5
- Output threshold: 10
- Gap threshold: 3
- Severe gap rule: 1 severe authority-boundary or hidden-redefinition gap triggers reflection.

## Decision

- Outcome: targeted update
- Owner or reviewer: sigil-development
- Next lifecycle step: audit `definitions/DEFINITIONS.md` for three-voice completeness when requested.
