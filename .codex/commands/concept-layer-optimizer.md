# Arcanum Sigil: concept-layer-optimizer

<!-- arcanum:capability-id concept-layer-optimizer -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command concept-layer-optimizer -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-concept-layer-optimizer-<UTC timestamp>`.
- `capability.id`: `concept-layer-optimizer`
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

Run the installed Arcanum sigil `concept-layer-optimizer` using the canonical package definition.

## Canonical Sources

- README: `arcana/concept-layer-optimizer/README.md`
- SKILL: `arcana/concept-layer-optimizer/SKILL.md`
- Technique specs: `arcana/concept-layer-optimizer/development/techniques/README.md`
- Usage telemetry: `arcana/concept-layer-optimizer/templates/usage-telemetry.md`

## Process

1. Read the canonical README and SKILL before executing.
2. Follow the SKILL process exactly; do not duplicate or rewrite the canonical contract inside this adapter.
3. Treat the user request as the seed point and any provided mode, target context, output artifact, constraints, or artifacts as input evidence.
4. Use true subagents for Proposer and Balancer roles when the active runtime supports them.
5. If the runtime does not support subagents, run labeled Proposer and Balancer passes in one agent with the same role trace contract.
6. Preserve finite recursive rounds, technique trace, complexity balance, output contract, and navigable result closeout.
7. Return the Concept Layer Optimizer Result plus observability closeout status.

## Guardrails

- Keep this command focused on `concept-layer-optimizer`.
- Do not execute downstream implementation work directly.
- Do not silently promote the sigil to registry status.
- Do not treat generated observer telemetry as a substitute for the primary result.
