# Invoke Handoff Mode

## Identity

- Spell: `invoke`
- Mode: `handoff`
- Status: implemented (L2 companion contract, validation examples pending)

## Purpose

Handoff mode creates a reviewable artifact for opening a new session or thread from an existing session.

It combines:

- the user's new prompt,
- a source session reference,
- the intended handoff type,
- a Context Builder selection from the whole referenced session,
- a clear next route for the new thread.

Handoff mode is for continuity without carrying the entire prior conversation forward. It selects only the context that will help the next session begin well, records what was excluded, and preserves the user's reason for splitting the work.

## Activation Gate

Normal handoff mode requires:

- a prompt for the new session,
- a source session reference, thread reference, run reference, or session evidence path,
- a requested or inferred handoff type,
- permission to use Context Builder over the referenced session evidence,
- an output path or accepted default under session evidence,
- enough source session material to select useful context.

Handoff mode blocks when the prompt or session reference is missing, when the referenced session cannot be inspected, or when Context Builder cannot cover the obligations needed by the target handoff type.

## Handoff Types

| Type | Use When | Recommended Next Route |
| --- | --- | --- |
| `workflow-reflection` | The user feels a gap, friction, repeated failure, or improvement opportunity in a sigil or spell they are using. | `workflow-reflect`, then `sigil-development` or `spellcraft` if changes are needed. |
| `new-lifecycle-thread` | A related idea emerged from the current session but needs its own define/design/plan lifecycle. | `invoke define`, `invoke design`, or `invoke full` depending on maturity. |
| `research-direction` | The session surfaced a research question, external project angle, or cross-project investigation. | `research` template, external project route, or deferred research thread. |
| `execution-continuation` | A bounded SWU, task-session, or implementation follow-up should continue elsewhere. | `task-session` or runtime-goal handoff after Context Builder strict coverage. |
| `generic-continuation` | The split is useful but does not match a specialized type yet. | `invoke define` or deferred follow-up. |

If multiple types are plausible, handoff mode asks for user choice unless one type is explicitly named by the user.

## Required Sigils

| Sigil | Role In Mode | Required Mode |
| --- | --- | --- |
| `context-builder` | Select obligation-linked context from the referenced session and reject merely interesting history. | standard; strict coverage for execution continuations |
| `structured-interview-kits` | Ask one focused question when handoff type, prompt, or target route is ambiguous. | gap-check |
| `inventory` | Resolve local session evidence, related artifacts, and handoff template paths. | lookup |

## Optional Sigils

| Sigil | Use When | Notes |
| --- | --- | --- |
| `workflow-reflect` | The handoff type is `workflow-reflection`. | Handoff mode prepares the reflection packet; Workflow Reflect owns analysis. |
| `decision-gate` | The handoff cannot safely choose among multiple lifecycle routes. | Route only consequential blocker choices. |
| `task-session` | The handoff targets one execution SWU or bounded work task. | Context Builder strict coverage is required before execution handoff. |
| `spellcraft` | The reflected or continued work targets a spell lifecycle. | Invoke emits handoff context only. |
| `sigil-development` | The reflected or continued work targets a sigil lifecycle. | Invoke emits handoff context only. |

## Inputs

- source session reference,
- new session prompt,
- handoff type or selection rationale,
- user-stated gap, idea, question, or continuation need,
- target project or lifecycle owner when known,
- source session evidence paths,
- existing artifacts mentioned by the session,
- constraints, non-goals, and desired output depth,
- optional destination thread/session label.

## Context Builder Policy

Context Builder must select from the whole referenced session, but the output must stay bounded.

The selection rules are:

- derive obligations from the new prompt and handoff type,
- scan the source session for decisions, artifacts, gaps, constraints, terms, routes, and unresolved questions relevant to those obligations,
- include selected excerpts or summaries only when they map to an obligation,
- exclude conversational history that is not needed for the new thread,
- record excluded candidates when they look tempting but are not obligation-relevant,
- block execution-continuation handoffs unless every obligation is covered or explicitly resolved,
- allow non-execution handoffs to pass with named gaps when the new thread can resolve them safely.

## Output Contract

Handoff mode emits a session/thread artifact using the `session-handoff` template family.

Required sections:

- identity and source session reference,
- new session prompt,
- handoff type and route rationale,
- Context Builder selection summary,
- obligation coverage matrix,
- selected session context,
- excluded context,
- target lifecycle or project boundary,
- gaps and blockers,
- next-session start prompt,
- next route,
- provenance and output paths.

## Mode Gates

- Prompt and source session reference are mandatory.
- Handoff type must be explicit or selected with rationale.
- Context Builder must run before the final handoff artifact is considered pass-ready.
- Selected context must map to obligations derived from the new prompt and handoff type.
- Handoff mode must not summarize the whole session as a transcript substitute.
- Handoff mode must not mutate the target sigil, spell, project, or work-pack.
- Workflow-reflection handoffs must preserve the user's felt gap as first-class evidence instead of converting it into a generic improvement request.
- New-lifecycle-thread handoffs must name whether the next lifecycle should start at define, design, plan, or full.
- Research-direction handoffs must distinguish known session evidence from questions to investigate elsewhere.
- Execution-continuation handoffs must require strict Context Builder coverage and route to `task-session` or runtime-goal handoff.

## Handoff Artifacts

- session handoff artifact path,
- optional Context Builder Markdown handoff pack path,
- optional Context Builder JSON/index path,
- target thread/session label,
- selected source session references,
- next-session start prompt,
- recommended next route.

## Observability

When `.arcanum/observability/` exists, record:

- spell name and mode,
- source session reference,
- handoff type,
- target route,
- Context Builder coverage status,
- selected context count,
- excluded context count,
- gaps and blockers,
- target lifecycle owner,
- whether the handoff opens a new lifecycle, reflection, research, or execution continuation.

## Output Shape

Return:

```markdown
## Invoke Validation Fixture Result

- Mode: handoff
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass | flag | block
- Mode contract: arcanum/spells/invoke/handoff.md
- Outputs: <session handoff path>, <context-builder pack path or n/a>
- Handoff type: <workflow-reflection | new-lifecycle-thread | research-direction | execution-continuation | generic-continuation>
- Source session: <reference>
- Context Builder coverage: pass | flag | block
- Next-session prompt: <prompt summary or path>
- Decisions: <route decisions>
- Unresolved gaps: <gaps or none>
- Next route: <workflow-reflect | invoke define | invoke design | invoke full | research | task-session | spellcraft | sigil-development | deferred>
```
