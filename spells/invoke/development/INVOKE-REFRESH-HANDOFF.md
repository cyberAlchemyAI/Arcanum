# Session Handoff: Invoke Refresh Mode

## Identity

- Source session reference: current benchmark workflow session, especially the post-task-session refresh need around benchmark artifacts and blockers.
- Destination label: `invoke-refresh-mode`
- Handoff type: `new-lifecycle-thread`
- Target project or lifecycle: `invoke` spell development cycle
- Created for: designing and planning a new `invoke refresh` command/mode.

## New Session Prompt

```text
Use invoke development artifacts to design and implement a new `invoke refresh` mode.

The mode should inspect the latest session outputs and decide whether they compose valid refresh input for the current workflow's invoke-authored artifacts. It should detect new information, new data, new evidence, new blockers, resolved blockers, changed next routes, and artifact drift. It should then produce a reviewable refresh plan or patch proposal for the affected artifacts without silently mutating unrelated lifecycle outputs.

Preserve invoke's authority boundary: `invoke refresh` owns artifact refresh synthesis and routing, not task execution, benchmark scoring, or target lifecycle completion.
```

## Route Rationale

- Recommended next route: `invoke design`, then `invoke plan`, then `spellcraft` or `task-session` for implementation.
- Rationale: `refresh` is a new invoke mode. It needs a mode contract, design boundaries, fixtures, and an implementation work-pack before runtime mutation.
- Lifecycle owner: `invoke` for design/plan; `spellcraft` for spell lifecycle implementation/promotion if canonical files are changed.

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| Preserve user's requested behavior | covered | current session request | The requested command must identify whether last outputs provide valid refresh inputs for current workflow artifacts. |
| Avoid demo-only refresh | covered | benchmark probe lessons | The session repeatedly distinguished setup proof from real score evidence; refresh must update blockers without promoting false completion. |
| Preserve invoke authority boundary | covered | `spells/invoke/README.md` | Invoke authors lifecycle artifacts and handoffs; it must not execute target work or silently mutate upstream owners. |
| Fit existing mode architecture | covered | `spells/invoke/handoff.md`, `design.md`, `plan.md` | `refresh` should be a mode contract like `handoff`, with gates and output artifacts. |
| Testability | covered | invoke validation fixture pattern | The mode needs pass/block/flag fixtures to prove it detects new data, no-op state, and unsafe ambiguity. |

Strict coverage: `pass`

## Selected Session Context

- User need:
  - Last session outputs may contain new evidence, new data, or a new blocker.
  - The command should decide if that evidence composes a valid refresh input for the active workflow invoke artifacts.
  - It should refresh artifacts such as work-packs, plans, implementation layering, handoffs, and blockers.
- Benchmark lesson:
  - SWE-bench and SmellBench required score artifacts derived from official/upstream outputs, not local inference.
  - PerfCodeBench materialization produced setup proof, not a score, and the work-pack had to be refreshed to keep the next blocker honest.
- Workflow lesson:
  - A useful refresh is not "rewrite everything"; it is a typed delta: evidence added, blocker opened/resolved, status changed, route changed, or artifact drift detected.

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Full benchmark implementation details | Too broad; only the refresh-pattern lesson is needed. |
| Raw external benchmark docs | Not needed for invoke mode design. |
| Unrelated dirty worktree state | Not obligation-relevant. |

## Target Boundary

- In scope:
  - New `refresh` mode contract.
  - Refresh input model.
  - Artifact inventory and delta classification.
  - Patch proposal or approved mutation flow.
  - Fixtures for pass, flag, block, and no-op refresh.
  - Observability fields for refresh decisions.
- Out of scope:
  - Executing benchmark tasks.
  - Inferring scores from setup proof.
  - Auto-promoting blockers or artifacts without evidence.
  - Replacing `task-session`, `workflow-reflect`, or `spellcraft`.
- Prior decisions to preserve:
  - Invoke remains the authoring front door.
  - Target lifecycle ownership must be explicit.
  - New modes need validation fixtures before maturity claims.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| No `refresh` mode contract exists | invoke | open | Add `spells/invoke/refresh.md`. |
| No refresh template exists | invoke | open | Add `templates/refresh/refresh.md` or a standalone template. |
| No fixtures prove refresh behavior | invoke | open | Add pass/block/flag/no-op fixtures. |
| Command adapter does not route `/invoke refresh` | invoke runtime/spellcraft | open | Update command router after contract approval. |

## Next-Session Start Prompt

```text
Open `arcanum/spells/invoke/development/INVOKE-REFRESH-HANDOFF.md`, `INVOKE-REFRESH-DESIGN.md`, and `INVOKE-REFRESH-PLAN.md`.

Implement the planned `invoke refresh` mode as an invoke spell lifecycle change. Start with the mode contract and fixtures. Do not update canonical command routing until pass/block/flag/no-op fixture coverage exists. Preserve the rule that refresh may propose artifact updates from new evidence, but it must not execute target work or silently promote unsupported completion.
```

## Provenance

- Source refs:
  - `spells/invoke/README.md`
  - `spells/invoke/handoff.md`
  - `spells/invoke/plan.md`
  - current benchmark task-session closeout around `SWU-HARNESS-008A.1`
- Context Builder mode: standard manual selection
- Evidence date: 2026-05-25
- Output path: `spells/invoke/development/INVOKE-REFRESH-HANDOFF.md`

## Gate Result

- Status: `pass`
- Reason: the mode idea is bounded, source-backed, and belongs to invoke development, but implementation remains future work.
