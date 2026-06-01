# Goal Handoff: Boundary Evidence Schema Refinement

Status: prepared
Target: `formulae/dispatch-spec/`

## Objective

Refine a corrected Arcanum-native boundary/evidence schema for
`dispatch-spec`, then produce a new architecture and non-executed plan.

## Stage Dispatch Contract

Every command-backed stage should be resolved with:

```bash
tools/arcanum --resolve <command>
```

Every available command-backed stage should be dispatched with:

```bash
tools/arcanum --exec --output <stage-output> <command> <stage-request>
```

If runtime dispatch fails, record the blocker exactly and continue with
Refine-owned synthesis only where evidence is sufficient.

## Blocked Fields

- Missing command resolution blocks the corresponding stage.
- Missing model-backed runtime execution blocks semantic stage output unless a
  dry-run artifact is explicitly labelled as command-surface evidence only.
- Any plan that makes Tandem or any external runtime the owner is invalid for
  this run.

## Goal Status

Native Codex Goal was not started. This handoff is a refinement evidence
artifact, not an active goal.
