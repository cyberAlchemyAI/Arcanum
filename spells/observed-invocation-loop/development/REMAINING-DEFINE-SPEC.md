# Invoke Define Spec: Observed Invocation Loop Remaining Items

## Intent Record

- User goal: harden Observed Invocation Loop from a strong pilot into runtime baseline readiness.
- Selected artifact type: follow-up invoke pack.
- Existing baseline: the original OIL define, design, implementation plan, and work-pack remain historical evidence and are not rewritten.
- Target capability: `observed-invocation-loop`.

## Problem

The current OIL implementation proves generic telemetry append, hook-backed envelopes, adapter markers, and reflection report generation. Review found the remaining maturity gaps are not about the first append path; they are about loop closure and reliability semantics:

1. Managed closeout paths print reflection recommendations but do not route reflection.
2. Threshold counters can stay hot after a reflection report.
3. Dedupe is committed before telemetry append and index updates are complete.
4. Codex Stop closeout can mark partial or failed work as completed/pass.
5. Legacy ledger rows can appear as anonymous capability groups in summaries.

## Capability Definition

This follow-up pack makes OIL runtime-baseline-ready by adding:

- managed reflection execution policy through `OBSERVED_REFLECT=off|auto|always`,
- threshold scoping since the last reflection while preserving immediate severe-gap triggers,
- post-success dedupe commit semantics,
- evidence-derived hook closeout status,
- deterministic migration checks for legacy telemetry rows.

## Boundary

Included:

- `observe-invocation.sh`,
- `reflect-invocation-signals.sh`,
- `tools/arcanum`,
- Codex Stop hook scripts,
- observability migration check script,
- follow-up invoke pack artifacts.

Excluded:

- mutating capability contracts from reflection reports,
- rewriting the completed original OIL work-pack,
- changing external repository runtimes outside this workspace,
- forcing strict telemetry by default.

## Decisions

| Decision | Result | Rationale |
| --- | --- | --- |
| Artifact strategy | New follow-up pack | Preserves completed original evidence. |
| Reflection owner | Managed wrapper or hook | `observe-invocation.sh` remains append/recommend only. |
| Reflection default | `auto` | Threshold-backed recommendations route without making every run noisy. |
| Threshold reset | Since `last_reflection_at` | Prevents permanent hot thresholds after report write. |
| Dedupe timing | Commit after successful append path | Avoids suppressing retry after partial failure. |
| Legacy rows | Compatibility fallback | Existing `sigil` rows remain valid while summaries use generic capability shape. |

## Unresolved Gaps

| Gap | Severity | Route |
| --- | --- | --- |
| External runtime rollout is not verified here. | non-blocker | future adapter rollout pack |
| Stop hook status is inferred from available hook evidence, not full model-native run semantics. | accepted limitation | improve if richer hook payload becomes available |

## Invoke Result

- Mode: define
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: spells/invoke/define.md
- Outputs: spells/observed-invocation-loop/development/REMAINING-DEFINE-SPEC.md
- Template selection: invoke.spell follow-up hardening pack
- Decisions: new remaining-items pack, hook/wrapper reflection routing, scoped thresholds, post-success dedupe
- Unresolved gaps: external runtime rollout
- Next route: design
