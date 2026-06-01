# Arcanum Sigil: constitution governance

<!-- arcanum:capability-id constitution-governance -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command constitution-governance -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-constitution-governance-<UTC timestamp>`.
- `capability.id`: `constitution-governance`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.

## Objective

Run the installed Arcanum sigil `constitution-governance` using the canonical local files:

- `arcana/constitution-governance/README.md`
- `arcana/constitution-governance/SKILL.md`
- `arcana/constitution-governance/templates/`

## Process

1. Read the local README and SKILL as the execution contract.
2. Resolve the requested mode: `create`, `add-rule`, `select`, `compose`, `validate`, `split`, or `promote`.
3. Execute only this sigil unless the contract explicitly delegates or the user asks to route elsewhere.
4. Preserve constitution scope, selectors, composition rules, validator impact, conflicts, decision gates, and next route.
5. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on modular constitution governance.
- Do not silently mutate validators without a constitution rule and validation adapter mapping.
- Do not treat Context Builder selection as constitution composition.
- Do not load every constitution when a selected composition pack is sufficient.
- Do not treat generated observer telemetry as a substitute for the primary result.
