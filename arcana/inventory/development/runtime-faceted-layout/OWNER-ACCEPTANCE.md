---
module: inventory-runtime-faceted-layout
owner: sigil-development
status: accepted
decision: supersede-current-selection
updatedAt: 2026-07-24
---

# Sigil Development Owner Acceptance

## Decision

Accept the generic runtime/faceted-layout lane as Inventory's current
implementation selection and select `SWU-IFR-001`.

`SWU-INT-001` is superseded only as the current selection. Its
interface/link/index lane remains preserved, unimplemented, and resumable
through a later explicit Sigil Development decision.

## Evidence

- The incoming Define, Design, Plan, Dispatch Spec, and Distill artifacts
  passed their authoring gates.
- The first runtime unit writes only three new public files under
  `schemas/`, `lib/`, and `test/`.
- The first runtime unit does not overlap `SWU-INT-001`, mutate consumer
  Inventory state, or require generated-runtime synchronization.
- The existing interface work pack dates from June 2026 and remains
  unexecuted; preserving it as the selected lane would leave the accepted
  runtime plan unable to start.

## Accepted Source Placement

Canonical implementation:

```text
arcana/inventory/
  schemas/
  lib/
  bin/
  test/
  scripts/
  runtime-manifest.json
```

Canonical lifecycle package:

```text
arcana/inventory/development/runtime-faceted-layout/
```

Generated runtime scope, admitted only by `SWU-IFR-006`:

```text
bin/
lib/
schemas/
scripts/validate-index-json.sh
scripts/validate_projection_conformance.py
runtime-manifest.json
```

Consumer-owned state is never a generated managed target:

```text
entries/
queries/
raw/
receipts/
index.json
index.md
schema.md
tags.md
log.md
```

## Admission

- Work-pack gate: pass.
- Task Session route: `SWU-IFR-001`.
- Mutation before Task Session admission: forbidden.
- Promotion readiness: not claimed.
- Commit, push, publication, and release: not authorized.
