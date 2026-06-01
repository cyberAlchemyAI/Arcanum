# Context Pack: Invoke Refresh

## Context Pack Summary

- Task: create and refresh `invoke refresh` development artifacts
- Mode: standard
- Files selected: 12
- Snippets selected: 18
- Obligation coverage: 100%
- Noise ratio: low
- Output markdown: `spells/invoke/development/INVOKE-REFRESH-CONTEXT-PACK.md`
- Output index: none
- Handoff pack: none
- Session evidence path: `spells/invoke/development/`
- Strict coverage: pass
- Blockers: 0

## Obligations

| Obligation | Required Evidence | Coverage |
| --- | --- | --- |
| O1: Keep this session invoke-only. | Durable session boundary. | covered |
| O2: Define what `invoke refresh` is allowed to do. | Existing refresh handoff/design/plan. | covered |
| O3: Preserve invoke authority boundaries. | Root invoke contract. | covered |
| O4: Fit mode architecture. | Mode table, shared state, output contract, validation runner. | covered |
| O5: Use Context Builder for evidence selection. | `context-builder` skill and handoff mode policy. | covered |
| O6: Use Distill to reduce the refresh scope. | `distill` skill and refresh design tension. | covered |
| O7: Add validation before maturity claims. | Fixture runner, validation report, template matrix. | covered |
| O8: Refresh artifacts with interrogation and distill outcomes. | New interrogation and distill artifacts plus design/plan updates. | covered |

## Included Context

- [DURABLE-SESSION-CONTEXT.md](DURABLE-SESSION-CONTEXT.md)
  - Selectors: `## Scope Boundary`, `## Operating Rules`
  - Obligations: O1, O8
  - Why included: establishes that the thread must stay inside invoke development.

- [INVOKE-REFRESH-HANDOFF.md](INVOKE-REFRESH-HANDOFF.md)
  - Selectors: `## New Session Prompt`, `## Context Builder Selection`, `## Target Boundary`
  - Obligations: O2, O5
  - Why included: captures the initial refresh intent and source-backed handoff boundary.

- [INVOKE-REFRESH-DESIGN.md](INVOKE-REFRESH-DESIGN.md)
  - Selectors: `## Purpose`, `## Refresh Input Model`, `## Delta Classes`, `## Gates`
  - Obligations: O2, O3, O6
  - Why included: defines the core refresh model that should be promoted into a mode contract.

- [INVOKE-REFRESH-PLAN.md](INVOKE-REFRESH-PLAN.md)
  - Selectors: `## SWUs`, `## Acceptance Criteria`, `## Recommended Next Route`
  - Obligations: O7, O8
  - Why included: names the implementation sequence and fixture expectations.

- [../README.md](../README.md)
  - Selectors: `## Mode Contracts`, `## Shared State`, `## Global Gates`, `## Root Output Contract`
  - Obligations: O3, O4
  - Why included: refresh must integrate as a normal invoke mode without breaking global behavior.

- [../handoff.md](../handoff.md)
  - Selectors: `## Context Builder Policy`, `## Mode Gates`
  - Obligations: O5
  - Why included: handoff mode already established the session-context selection rule that refresh should reuse for source session outputs.

- [../templates/README.md](../templates/README.md)
  - Selectors: `## Ownership Model`, `## Family Scaffold Contract`, `## Promotion Gate`
  - Obligations: O4, O7
  - Why included: refresh needs a template family with the same scaffold shape.

- [TEMPLATE-VALIDATION-TASKS.md](TEMPLATE-VALIDATION-TASKS.md)
  - Selectors: `## Template Task Matrix`, `## Fixture Requirements`
  - Obligations: O7
  - Why included: refresh template coverage needs low, medium, and complex prompt tasks.

- [run-validation-fixtures.sh](run-validation-fixtures.sh)
  - Selectors: contract variables, contract checks, fixture registration block
  - Obligations: O4, O7
  - Why included: deterministic validation must know about `refresh`.

- [VALIDATION.md](VALIDATION.md)
  - Selectors: `## Checks Performed`, `## Fixture Status`, `## Runner Output`
  - Obligations: O7, O8
  - Why included: durable validation record must include refresh coverage.

- [../../arcana/distill/SKILL.md](../../arcana/distill/SKILL.md)
  - Selectors: `objective`, `process`, `output-contract`
  - Obligations: O6
  - Why included: refresh needs a smallest coherent unit before implementation.

- [../../transmutations/context-builder/SKILL.md](../../transmutations/context-builder/SKILL.md)
  - Selectors: `process`, `quality-bar`, `output-contract`
  - Obligations: O5
  - Why included: this pack follows the Context Builder evidence selection contract.

## Excluded Candidates

- Full benchmark task-session implementation files: excluded because only the refresh-pattern lesson is needed.
- Raw observability hook state: excluded because refresh-specific telemetry can be described without importing unrelated hook churn.
- Broad Arcanum runtime design: excluded because refresh is an invoke authoring mode, not a runtime execution feature.

## Next Actions

1. Add `spells/invoke/refresh.md`.
2. Add `spells/invoke/templates/refresh/`.
3. Add pass, flag, block, and no-op fixtures.
4. Wire refresh into invoke root docs and deterministic validation.
5. Run `./spells/invoke/development/run-validation-fixtures.sh`.
