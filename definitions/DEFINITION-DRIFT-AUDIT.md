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
