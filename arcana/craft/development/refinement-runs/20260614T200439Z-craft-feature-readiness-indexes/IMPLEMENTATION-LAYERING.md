# Implementation Layering: Craft Feature Readiness Indexes

## Status

- Complexity: `medium`
- Output mode: `split`
- Layer coverage: L0-L3
- Execution status: non-executed plan

## Layer Decisions

| Layer | Question | Scope | Promotion Evidence |
| --- | --- | --- | --- |
| L0 Schema Contract | Can Craft represent execution readiness additively without invalidating existing ledgers? | `templates/ledger.schema.yml`, index contract, validation notes. | YAML parses, example ledgers still parse, readiness fields are optional. |
| L1 Skill And View Contract | Can agents and humans see readiness without treating Craft as an executor? | `SKILL.md`, `README.md`, all-status/export wording. | Grep confirms readiness fields in contract; wording preserves interaction boundary. |
| L2 Examples And Fixture Coverage | Can public-safe examples demonstrate ready and blocked scopes? | Examples or fixture snippets under `arcana/craft/examples/`. | YAML parse plus review that no private workspace evidence leaked. |
| L3 Runtime Surface Sync | Can generated runtime packages and publication checks align with canonical source? | Regenerated skill surfaces, parent/submodule validation. | Generated copies match canonical source; `git diff --check`; `make bump-check` before parent publication. |

## Deferrals

- Direct Invoke readiness block changes are deferred to the Invoke lifecycle.
- Refine non-executable marker changes are deferred to the Refine lifecycle.
- Automated renderer/indexer implementation remains deferred unless a separate Craft renderer task is approved.

## Promotion Rule

Layer promotion requires evidence from the previous layer. Do not regenerate runtime surfaces until canonical schema and skill text pass local validation.
