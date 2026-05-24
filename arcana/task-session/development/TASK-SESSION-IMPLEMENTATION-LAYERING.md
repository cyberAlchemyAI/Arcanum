# Task Session Implementation Layering

## Invocation

- Spell: `invoke`
- Mode: `plan`
- Target artifact: `task-session`
- Companion work-pack: `CONTEXT-PACK-GOAL-HANDOFF-WORK-PACK.md`

## Layer Strategy

This plan uses the context-pack handoff as the implementation axis. The work crosses Task Session, Context Builder, Codex Goal Profile, the Codex Goal adapter, and Invoke templates, so changes should progress from schema to producer to consumers.

## L0 - Handoff Schema Proof

**Question:** Can the task-scoped handoff pack be specified clearly enough that every downstream consumer knows what to expect?

**Work:**

- SWU-CTX-GOAL-001

**Boundary:**

- Define schema and quality gates.
- Do not implement runtime behavior yet.

**Promotion Evidence:**

- Required sections, provenance, authority precedence, strict coverage, Markdown plus JSON/index outputs, session-evidence persistence, fallback search rule, and blocker handling are documented.

## L1 - Context Builder Producer

**Question:** Can Context Builder emit the handoff pack without taking over Task Session or runtime responsibilities?

**Work:**

- SWU-CTX-GOAL-002

**Boundary:**

- Add handoff output and session-evidence persistence.
- Preserve evidence/inference separation and selector-level excerpts.

**Promotion Evidence:**

- A task/SWU can produce Markdown plus JSON/index handoff output with strict coverage and gaps.

## L2 - Pack-First Runtime Consumption

**Question:** Can Task Session and Codex Goal consume the handoff pack safely before mutation or runtime delegation?

**Work:**

- SWU-CTX-GOAL-003
- SWU-CTX-GOAL-004
- SWU-CTX-GOAL-005

**Boundary:**

- Task Session gates pack quality before delegation.
- Codex Goal Profile receives pack-first instructions.
- Codex Goal adapter blocks unsafe handoffs and records pack evidence.

**Promotion Evidence:**

- Dry-run task session confirms context pack is produced before goal creation.
- Goal profile includes fallback exploration only for named gaps.
- Adapter preserves pack reference in completion evidence.
- Missing strict coverage blocks goal handoff.

## L3 - Invoke Readiness And Reuse

**Question:** Can future invoke-generated work-packs be context-builder-ready without pre-generating stale context packs?

**Work:**

- SWU-CTX-GOAL-006

**Boundary:**

- Add planning guidance and template fields for source anchors, validation surfaces, write scope, and handoff notes.
- Do not require invoke plan to generate context packs.

**Promotion Evidence:**

- Future work-pack tasks/SWUs expose enough structure for Context Builder to select task context at execution time.

## Layer Dependencies

```text
L0 schema
  -> L1 Context Builder producer
  -> L2 Task Session / Codex Goal consumers
  -> L3 Invoke readiness guidance
```

`SWU-CTX-GOAL-006` may start after L0 because it only needs the schema concept, but it should be reviewed again after L2 to keep template guidance aligned with runtime behavior.
