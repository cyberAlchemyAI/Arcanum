---
name: refine
description: Use when the user asks to run or test Arcanum refine, create a refinement seed, refine a vague target through the canonical discovery/design loop, or inspect the refine lifecycle using native skill execution and dispatch-spec validation.
metadata:
  short-description: Run Arcanum refine
---

# Refine

Refine is the Arcanum sigil for designing an initial seed, validating a dispatch-spec route for the canonical discovery/design refinement loop, indexing stage evidence, and returning a final refined synthesis.

Use this skill when the user asks for `refine`, `/refine`, a refine seed, a refinement run, or a test of the refine workflow.

## Local Source

In the `domainspec-core` checkout, the canonical refine contract lives at:

```text
arcanum/arcana/refine/SKILL.md
```

Read that file first. It is the source of truth for presets, research policy, dispatch route validation, native stage execution, run-manifest contract, evidence-index requirements, runtime handoff, and quality bar.

Also read only the supporting file needed for the request:

- `arcanum/arcana/refine/REFINEMENT-LOOP.md` for loop phases, budgets, stage configuration, repair rules, and research bounds.
- `arcanum/arcana/refine/templates/` when materializing a refinement run folder.
- `arcanum/arcana/refine/examples/` when the user wants an example or comparison.
- `arcanum/arcana/refine/development/run-validation-fixtures.sh` when validating fixture-level behavior.

## Execution Surface

Prefer the installed native skill package and the canonical source contract:

- active package: `refine`
- canonical source: `arcanum/arcana/refine/SKILL.md`
- deterministic resolver, when present: `arcanum/tools/arcanum --resolve refine`

If deterministic resolution is unavailable, follow `arcanum/arcana/refine/SKILL.md` directly and record the missing resolver as a runtime-surface gap. Do not require `.codex/commands/` for normal Refine execution.

## Stage Dispatch

Refine should first write `REFINE-DISPATCH.json` and validate it through `formulae/dispatch-spec/dispatch.schema.yml`. Native runtime-backed stages run only after the route shape, technique references, gates, handoffs, and observability grouping are valid.

Refine then uses the parent native skill/subagent surface for stage work. When a durable adapter handoff is useful, the deterministic tool surface can prepare a receipt contract:

```bash
arcanum/tools/arcanum --exec --adapter native-skill --output <stage-output> <capability-id> <stage-request>
```

Record each owning capability, resolved capability handle, requested mode/config, artifact path, observer status, verdict, and blocked reason in the manifest/index.

## Runtime Boundary

The durable Arcanum runtime remains the execution target. When dispatch validation, capability resolution, or runtime execution cannot run, Refine records `BLOCK` with exact missing fields rather than silently switching to Task Session, Sigil Development, or local fallback.

## Output

Report:

- target,
- preset and research mode,
- whether native skill or deterministic capability resolution worked,
- dispatch route validation status,
- runtime handoff status,
- run manifest path when created,
- evidence index path when created,
- dispatch route path when created,
- runtime handoff path when created,
- validation command and result when run,
- final synthesis or remaining blocker.
