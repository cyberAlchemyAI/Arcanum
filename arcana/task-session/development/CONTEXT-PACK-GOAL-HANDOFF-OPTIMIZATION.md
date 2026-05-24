# Context Pack Goal Handoff Optimization

## Invocation

- Skills: `distill`, then `invoke`
- Target: Task Session, Context Builder, Codex Goal handoff
- Question: Should Task Session delegate context selection before Codex Goal execution, and should Context Builder persist a reusable task context pack?

## Optimized Concept Unit

The smallest coherent unit is not "Task Session uses Context Builder" by itself. That is already the direction of the current contract.

The optimized unit is:

> A task-scoped context handoff pack, produced before runtime delegation, that Codex Goal treats as its selected source context.

This unit keeps responsibility boundaries clean:

- Task Session owns orchestration, gates, delegation, and final evidence sync.
- Context Builder owns source selection, obligation coverage, provenance, and compact excerpts.
- Codex Goal owns implementation inside the prepared context, using broad exploration only for named gaps.

## Proposed Shape

Task Session should invoke Context Builder before any `--via goal` delegation. When a subagent runtime is available, Context Builder can run as a subagent or delegated worker. When no subagent runtime is available, Task Session should run Context Builder inline/local and still produce the same handoff artifact.

Context Builder should emit a persistent, task-scoped pack for later consultation. The pack should be generated at execution time, stored as session evidence, and not treated as canonical planning truth. Its job is to preserve the evidence and excerpts used for a specific task session.

Codex Goal should receive either:

- a path to the persisted Markdown handoff pack, and
- a path to the JSON/index handoff pack.

The goal prompt should instruct the runtime to use the pack first, and to broaden repository exploration only for uncovered obligations or explicitly named context gaps. Strict coverage is required before handoff: every parsed obligation must be covered or explicitly resolved.

## Pack Contents

A task-ready handoff pack should include:

- Task/SWU identity and source work-pack reference.
- Selected file paths, selector ranges, and short excerpts.
- Architecture guidelines relevant to the task.
- Related feature or neighboring implementation context.
- Hard constraints and non-goals.
- Allowed write scope and files that should not be touched.
- Validation surface and expected evidence.
- Open blockers, contradictions, and unresolved obligations.
- Authority precedence between task contract, work-pack, architecture, code, and inferred notes.
- Fallback exploration rule for Codex Goal.
- Provenance metadata: timestamp, source refs, git SHA or content hashes when available.
- Markdown output path and JSON/index output path.
- Strict coverage status.
- Secret/noise exclusions and max excerpt rules.

## What This Fixes

This addresses the problem seen in the previous task session: the implementation goal had to rediscover architecture expectations during execution. The better contract is to select those expectations before the goal starts, so the goal can spend its budget on implementation and verification instead of broad discovery.

## What Could Be Missing

The main missing pieces are contract quality controls:

- **Coverage threshold:** block goal delegation unless every obligation is covered by selected evidence or explicitly resolved by the context pack.
- **Staleness policy:** mark or reject packs when source files changed after pack generation.
- **Authority order:** define which source wins when architecture, task, and code disagree.
- **Fallback audit:** if Codex Goal uses broad exploration, it must report which gap forced it and which new sources it used.
- **Persistence boundary:** saved packs are session evidence, not canonical project docs.
- **Privacy/noise boundary:** context packs should exclude secrets, generated dependency blobs, logs, and oversized excerpts.
- **Feedback loop:** if a goal finds missing context, Task Session should record the gap so the next pack improves.

## Concept-Layer Decision

Adopt the context handoff pack as the shared concept between Task Session, Context Builder, and Codex Goal.

Avoid making "subagent" the concept boundary. Subagent execution is an implementation strategy. The durable concept is the pack contract and its authority over goal execution.
