# Implementation Layering: Craft Index Improvements

## Target And Scope

- Target: `arcana/craft`
- Scope: Craft schema, docs, public fixtures, deterministic projection tooling,
  generated runtime refresh gates.
- Current state: planned from two executed refine packets.

## Layer Decision Table

| Layer | Decision Question | Minimum Working Unit | Included Scope | Deferred Scope | Exit Evidence | Promotion Decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | After this layer, we know whether readiness and projection contracts can coexist without breaking Craft authority. | `SWU-CII-001` | Schema/docs/SKILL contract wording. | Fixtures, scripts, generated mirrors. | YAML parse, grep checks, dispatch/work-pack refs. | Continue only if contract is additive. |
| L1 | After this layer, we know whether a public-safe fixture can prove row-family coverage. | `SWU-CII-002` | Synthetic fixture and expected outputs. | Import writeback, mirror refresh. | YAML/JSON/CSV fixture checks and public-boundary scan. | Continue only if fixture is clean. |
| L2 | After this layer, we know whether deterministic build/validate tooling makes reads faster and safer. | `SWU-CII-003`, `SWU-CII-004` | `craft-index build`, `validate`, status/export integration. | CSV writeback mutation. | Tool output checks and stale detection. | Continue only if generator is deterministic. |
| L3 | After this layer, we know whether CSV dry-run import and runtime mirrors are safe to prepare. | `SWU-CII-005`, `SWU-CII-006`, `SWU-CII-007` | Import dry-run, generated mirror refresh, publication-prep checks. | Commit/push/parent gitlink unless explicitly requested. | Dry-run patch plan, generated mirror grep, `make bump-check`. | Defer publication until submodule-first approval. |

## Recommended Next Layer

- Next layer: L0
- Key decision unlocked: whether combined readiness/projection contract can be
  added additively to Craft.
- Major deferred scope: import writeback, generated mirror refresh, and
  publication.
