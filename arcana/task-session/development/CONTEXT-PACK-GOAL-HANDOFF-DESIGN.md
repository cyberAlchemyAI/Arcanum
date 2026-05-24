# Context Pack Goal Handoff Design

## Purpose

Make Task Session delegation to Codex Goal context-first instead of exploration-first.

The intended behavior is:

1. Task Session identifies the task or SWU.
2. Context Builder selects the relevant context and emits a task-ready handoff pack.
3. Task Session gates the pack for strict coverage, contradiction, and staleness.
4. Codex Goal executes from the pack, broadening exploration only for named gaps.
5. Task Session synchronizes evidence, validation, and any context gaps discovered during the goal.

## Six-View Design

### User Workflow View

The user can run:

```text
/task-session to benchmark/WORK-PACK.md --swu SWU-HARNESS-003 --runtime codex --via goal
```

Task Session prepares the goal by first building context. The user does not need to manually say "run context-builder first" for every task session.

### Runtime View

Context Builder should run as delegated work when the environment supports it:

- preferred: subagent or worker delegated by Task Session,
- fallback: inline/local Context Builder execution with identical output contract.

This avoids coupling the feature to a specific multi-agent implementation.

### Artifact View

Context Builder emits a handoff pack as session evidence, such as:

```text
.arcanum/runs/<session-id>/context-pack.md
.arcanum/runs/<session-id>/context-pack.json
```

The exact path is runtime-specific, but the artifact should be task-scoped, durable for consultation, and safe to reference in reports.

Suggested sections:

- Identity
- Obligations
- Selected Sources
- Architecture Guidance
- Related Feature Context
- Constraints And Non-Goals
- Write Scope
- Validation Surface
- Gaps And Blockers
- Authority Precedence
- Fallback Exploration Rule
- Provenance
- Strict Coverage Status

### Goal Handoff View

Codex Goal receives a prompt fragment like:

```text
Use the context pack at <path> as the selected source context for this goal.
Use the structured index at <path> for adapter-readable selectors and obligations.
Broaden repository exploration only for obligations listed as uncovered or for gaps you explicitly name before exploring.
If you use additional sources, report the gap and the source in the final result.
```

The goal profile should include:

- handoff pack Markdown path,
- handoff pack JSON/index path,
- strict coverage status,
- required obligations,
- fallback exploration rule,
- allowed write scope,
- validation surface,
- blocked stop condition.

### Gate View

Task Session should block or ask for decision when:

- no handoff pack Markdown and JSON/index can be produced,
- any obligation is neither covered nor explicitly resolved,
- the pack contains contradictions without an authority decision,
- source refs are stale,
- write scope is too broad or missing,
- the pack contains unsafe or irrelevant material.

### Feedback View

If Codex Goal discovers missing context, Task Session should append that gap to session evidence. Context Builder can use those recorded gaps to improve future selection.

This creates a learning loop without making generated packs canonical project truth.

## Contract Changes

### Task Session

- Add a "Build Context Pack Handoff" phase before decision gates and runtime delegation.
- For `--via goal`, require a session-evidence handoff pack with Markdown plus JSON/index and strict coverage.
- Include context artifact paths, strict coverage, gaps, and fallback search status in the task-session report.

### Context Builder

- Add a task-ready handoff output mode.
- Persist the context pack under session/run evidence when requested.
- Include provenance, authority precedence, and validation surface.
- Distinguish selected evidence from inferred notes.

### Codex Goal Profile

- Accept handoff pack Markdown path and JSON/index path as first-class input.
- Emit a goal prompt that enforces pack-first execution.
- Include context gaps and extra sources used in final reporting.

### Codex Goal Adapter

- Reject goal delegation when required pack quality gates fail.
- Pass pack Markdown path and JSON/index into the native goal.
- Preserve pack reference in final task-session evidence.

### Invoke Plan

Invoke-generated work packs should be context-builder-ready, not pre-packed.

That means SWUs should have clear task identity, source anchors, acceptance evidence, validation surfaces, and implementation boundaries. Context packs should be generated at execution time to avoid drift.
