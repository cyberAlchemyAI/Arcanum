---
name: refine
description: Use when the user asks to run or test Arcanum refine, create a refinement seed, refine a vague target through the canonical discovery/design loop, or inspect the refine lifecycle using deterministic Arcanum command dispatch.
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

Read that file first. It is the source of truth for presets, research policy, dispatch route validation, stage dispatch, run-manifest contract, evidence-index requirements, runtime handoff, and quality bar.

Also read only the supporting file needed for the request:

- `arcanum/arcana/refine/REFINEMENT-LOOP.md` for loop phases, budgets, stage configuration, repair rules, and research bounds.
- `arcanum/arcana/refine/templates/` when materializing a refinement run folder.
- `arcanum/arcana/refine/examples/` when the user wants an example or comparison.
- `arcanum/arcana/refine/development/run-validation-fixtures.sh` when validating fixture-level behavior.

## Command Surface

Prefer the repository-local command surface:

```bash
arcanum/tools/arcanum --resolve /refine
arcanum/tools/arcanum --exec refine <target>
```

If `/refine` does not resolve, report that the command bridge is missing and follow `arcanum/arcana/refine/SKILL.md` directly only as a read-only diagnostic fallback.

## Stage Dispatch

Refine should first write `REFINE-DISPATCH.json` and validate it through `formulae/dispatch-spec/dispatch.schema.yml`. Command-backed stages run only after the route shape, technique references, gates, handoffs, and observability grouping are valid.

Refine then uses deterministic Arcanum dispatch for command-backed stages:

```bash
arcanum/tools/arcanum --exec --output <stage-output> <command> <stage-request>
```

Record each command, resolved command file, requested mode/config, artifact path, observer status, verdict, and blocked reason in the manifest/index.

## Runtime Boundary

The durable Arcanum runtime remains the execution target. When dispatch validation, command resolution, or runtime execution cannot run, Refine records `BLOCK` with exact missing fields rather than silently switching to Task Session, Sigil Development, or local fallback.

## Output

Report:

- target,
- preset and research mode,
- whether `/refine` command resolution worked,
- dispatch route validation status,
- runtime handoff status,
- run manifest path when created,
- evidence index path when created,
- dispatch route path when created,
- runtime handoff path when created,
- validation command and result when run,
- final synthesis or remaining blocker.
