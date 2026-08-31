# Codex Goal Handoff Pack

## Identity

- Task/SWU: `<task-or-swu-id>`
- Source task/work-pack: `<path-or-reference>`
- Session/run id: `<id-or-none>`
- Session evidence path: `<path>`
- Runtime handoff: `codex-goal`
- Repository revision: `<git-sha-or-unknown>`
- Evidence date: `<yyyy-mm-dd>`

## Obligation Coverage

| Obligation | Status | Selected Evidence | Resolution |
| --- | --- | --- | --- |
| `<obligation-id>` | `covered | resolved | block` | `<path#selector>` | `<required when resolved or block>` |

Strict coverage: `<pass | block>`

## Selected Sources

- `<path>`
  - Selectors: `<heading/symbol/range>`
  - Obligations: `<ids>`
  - Evidence excerpt: `<short selector-level excerpt or summary>`

## Architecture Guidance

`<architecture constraints or none>`

## Related Feature Context

`<related behavior, prior feature, or none>`

## Constraints And Non-Goals

- `<constraint>`

## Write Scope

- `<allowed path or module>`

## Validation Surface

- `<command, review, or accepted substitute>`

## Gaps And Blockers

- `<gap with owner/status, or none>`

## Authority Precedence

1. `<highest authority>`
2. `<next authority>`

## Fallback Exploration Rule

Broad repository exploration is allowed only for obligations listed in `Gaps And Blockers` or for a gap explicitly named before exploring. Extra sources must be reported in the runtime result.

## Provenance

- Source refs: `<paths/selectors>`
- Content hashes or git SHA: `<hashes-or-sha>`
- Builder mode: `<lean | standard | deep>`

## Output Paths

- Markdown: `<path>`
- JSON/index: `<path>`
