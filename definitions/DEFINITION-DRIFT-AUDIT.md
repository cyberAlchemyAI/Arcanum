# Definition Drift Audit

Date: 2026-06-08
Scope: initial Arcanum-wide governance source for `contract` and `schema`

## Result

| Check | Result | Notes |
| --- | --- | --- |
| Canonical source exists | pass | `definitions/DEFINITIONS.md` is the project-level source. |
| Index exists | pass | `definitions/DEFINITIONS-INDEX.md` links terms and aliases. |
| Undefined critical terms | resolved | `contract` and `schema` were previously used across the project without a project-level authority source. |
| Conflicting consumers | none blocking | Existing usage is broadly compatible with the new definitions. |
| Soft drift | present | Several downstream artifacts define or explain these terms locally and should reference the canonical IDs when next edited. |

## Remediation Targets

| Target | Drift type | Recommended action |
| --- | --- | --- |
| `development/craft/contract-language/README.md` | Local definitions for contract and schema. | Keep local framing, but reference `DEF-ARC-CONTRACT` and `DEF-ARC-SCHEMA` as upstream authority. |
| `development/craft/contract-language/CONTRACT-LANGUAGE-HANDOFF.md` | Local language design repeats contract/schema distinction. | Link the two canonical IDs before expanding the contract language. |
| `development/craft/CRAFT-INITIAL-DEFINITION.md` | Craft-specific schema definition is broader and method-oriented. | Mark the Craft wording as method-local and link `DEF-ARC-SCHEMA` for Arcanum-wide meaning. |
| `formulae/dispatch-spec/README.md` | Dispatch spec describes deterministic contract and schema roles. | Reference `DEF-ARC-CONTRACT` for route obligations and `DEF-ARC-SCHEMA` for `dispatch.schema.yml`. |
| `framework/SCHEMA-CONSTITUTION.md` | Defines governance for schema artifacts. | Add a reference to `DEF-ARC-SCHEMA` during the next constitution refresh. |
| `spells/README.md` | Mentions spell and mode contracts. | Reference `DEF-ARC-CONTRACT` when spell contract language is next revised. |
| `transmutations/context-builder/SKILL.md` | Uses output and handoff contract language. | Reference `DEF-ARC-CONTRACT` when skill output contract language is next revised. |

## Boundary

This audit creates the project-level authority source and records drift targets.
It does not mutate downstream capability contracts, schemas, glossaries,
registries, or generated runtime surfaces.

## 2026-06-19 Three-Voice Completeness Audit

Scope: `definitions/DEFINITIONS.md` and `definitions/DEFINITIONS-INDEX.md`.

| Check | Result | Notes |
| --- | --- | --- |
| Definition voices complete | pass | All indexed definitions now include scientific/formal, plain-language, and domain-context voices. |
| Stable IDs and anchors | pass | Existing definition IDs and heading anchors were preserved. |
| Index synced | pass | Governance notes now mention the three-voice requirement; term rows did not require anchor changes. |
| Downstream drift | deferred | Existing downstream drift targets remain outside this L0 migration. |

### Follow-Up

- L1 should review downstream explanatory and consumer artifacts for references
  to the canonical definitions, starting from the remediation targets above.

## 2026-06-20 Goal Spell Spec And Definitions Addendum

Scope: `spells/goal/` define-stage spec and definitions baseline.

| Check | Result | Notes |
| --- | --- | --- |
| Canonical terms promoted | pass | Added `DEF-ARC-GOAL-SPELL`, `DEF-ARC-STAGED-DELTA`, and `DEF-ARC-APPROVAL-TOKEN`. |
| Definition voices complete | pass | Each promoted term includes scientific/formal, operational, plain-language, domain-context, boundary, consumers, and related definitions. |
| Index synced | pass | `DEFINITIONS-INDEX.md` includes term rows and alias mappings for the promoted terms. |
| Local glossary boundary | pass | Goal-specific terms remain in `spells/goal/development/invoke-runs/20260620T202601Z-goal-spec-definitions/DEFINITIONS.md`. |
| Downstream drift | non-blocking | `spells/goal/README.md` and the new spec already use the promoted terms compatibly; future spellcraft validation should add direct definition-ID references if needed. |

### Follow-Up

- Spellcraft should validate the goal spell contract, spec, and definitions as
  one package before runtime SWU execution.
- Experiment Harness should produce reusable behavior evidence before any
  registry promotion beyond draft.
