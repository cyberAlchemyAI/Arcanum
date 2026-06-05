# Arcanum Sigil: refine

<!-- arcanum:capability-id refine -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command refine -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-refine-<UTC timestamp>`.
- `capability.id`: `refine`
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

Run the installed Arcanum sigil `refine` using the canonical package definition.

## Canonical Sources

- README: `arcana/refine/README.md`
- SKILL: `arcana/refine/SKILL.md`
- Refinement loop: `arcana/refine/REFINEMENT-LOOP.md`
- Templates: `arcana/refine/templates/`

## Process

1. Read the canonical SKILL and Refinement Loop before executing.
2. Follow the SKILL process exactly.
3. Treat the user request as the target, preset, research mode, desired outcome, and optional output-location input. A simple sentence such as `refine everything until we have an MVP-ready plan` is valid input and should infer the current repository/scope plus an MVP-ready non-executed plan outcome.
4. Materialize and validate `REFINE-DISPATCH.json` before command-backed stages. The route must name applicable dispatch-spec technique overlays, subagent strategy, gates, handoffs, and observability grouping.
5. Show `Refine Run Strategy Proposal` with inferred target/outcome, selected overlays, why they apply, subagent roles, join policy, receipt requirements, authorization state, what will run next, and what remains deferred.
6. Stop after the strategy proposal and ask for confirmation. Do not spawn subagents, execute stages, or run the canonical loop before confirmation.
7. After confirmation, spawn approved subagents when the strategy recommends or requires them, then use `tools/arcanum --resolve` and `tools/arcanum --exec` for approved command-backed stages according to the Stage Dispatch Contract. When this command is invoked through `tools/arcanum --exec refine`, native root orchestration in `tools/arcanum` owns child stage dispatch to avoid Codex-inside-Codex recursion.
8. Preserve the run manifest, evidence index, dispatch route, runtime handoff, subagent receipts, stage outputs, final synthesis, and recommended next routes.
9. Return the Refine Result plus observability closeout status after the confirmed run.

## Guardrails

- Keep this command focused on `refine`.
- Do not execute Task Session or Sigil Development as part of the refine loop.
- Do not skip dispatch-spec validation or treat technique overlays as decorative labels.
- Do not run command-backed stages or subagents before showing the Dispatch Spec strategy and receiving permission.
- Do not treat a simple "refine everything" request as permission to run before the user confirms the proposed strategy.
- Do not silently fall back from failed runtime handoff or failed command dispatch.
- Do not treat generated observer telemetry as a substitute for the primary result.
