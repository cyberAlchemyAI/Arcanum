# Arcanum Formulae: dispatch-spec

<!-- arcanum:capability-id dispatch-spec -->
<!-- arcanum:capability-kind formulae -->
<!-- arcanum:capability-tier formulae -->
<!-- arcanum:command dispatch-spec -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-dispatch-spec-<UTC timestamp>`.
- `capability.id`: `dispatch-spec`
- `capability.kind`: `formulae`
- `capability.tier`: `formulae`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the dispatch route or validation target before execution.
- expected outputs: list intended validation/design artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.

## Objective

Run the repository-local Formulae package `dispatch-spec`.

## Canonical Sources

- README: `formulae/dispatch-spec/README.md`
- SKILL: `formulae/dispatch-spec/SKILL.md`
- Schema: `formulae/dispatch-spec/dispatch.schema.yml`
- Validator: `formulae/dispatch-spec/scripts/validate-dispatch.py`
- Fixtures: `formulae/dispatch-spec/development/run-validation-fixtures.sh`

## Process

1. Read `formulae/dispatch-spec/SKILL.md` before executing.
2. Treat the user request as either:
   - a dispatch JSON path to validate, or
   - route intent to design into a dispatch document.
3. For an existing dispatch JSON file, run:

   ```bash
   python3 formulae/dispatch-spec/scripts/validate-dispatch.py <dispatch.json>
   ```

4. For package fixture validation, run:

   ```bash
   formulae/dispatch-spec/development/run-validation-fixtures.sh
   ```

5. Return the Dispatch Spec Result from the canonical skill.

## Guardrails

- `dispatch-spec` validates route shape; it does not execute owner capabilities.
- Do not promote inventory, ontology, glossary, sigil, spell, or Craft artifacts from dispatch evidence alone.
- Do not duplicate or mutate the Formulae source package from this command route.
- If a route claims execution, promotion, or lifecycle authority that belongs to another capability, return `block` or `flag` according to the canonical skill.
