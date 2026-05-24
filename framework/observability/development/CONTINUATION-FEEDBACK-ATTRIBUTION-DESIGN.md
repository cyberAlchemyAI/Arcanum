# Continuation Feedback Attribution Design

## Purpose

Continuation feedback attribution captures the user's next-turn corrections, clarifications, and friction signals and links them back to the capability run that likely caused them.

This solves a gap that post-run telemetry cannot solve alone:

```text
skill runs
  -> final answer seems acceptable
  -> user asks a correction two turns later
  -> original run should receive a feedback signal
```

The system needs both:

- `derive-invocation-telemetry`: extracts evidence available at run close.
- continuation feedback attribution: detects later user feedback and attaches it to the prior run or active interaction.

## Why Necronomicon Matters

Necronomicon already owns the durable repository harness concepts needed here:

- active interaction state,
- route history,
- gap ledger,
- checkpoint memory,
- maintenance recommendations,
- distinction between fresh request and continuation.

But the next implementation should **not** be "rewrite Necronomicon." The smallest useful unit is an interface between observability and Necronomicon:

```text
observability writes recent run metadata
Necronomicon/session layer reads next user turn
feedback attribution links the turn to a prior run when appropriate
observer records a follow-up telemetry event
```

## Current Gap

Current observability can record:

- what happened during a run,
- what the Stop hook saw at closeout,
- what the observer derived from available evidence.

It cannot reliably know:

- the user needed another explanation,
- the output created confusion,
- the route was wrong but only became obvious after the next prompt,
- the user corrected an omitted requirement,
- the user switched to a better capability because the prior capability underfit.

Those are continuation signals.

## Component Boundary

### Owns

- detecting follow-up user turns that reference the previous capability result,
- classifying the follow-up as correction, clarification, continuation, route miss, dissatisfaction, or unrelated fresh work,
- linking feedback to a previous `run_id`,
- emitting a compact feedback event to observability,
- optionally adding a Necronomicon gap-ledger entry or active-interaction note.

### Does Not Own

- re-running the original skill,
- editing the original skill,
- deciding ontology or inventory promotion,
- replacing Necronomicon's full session model,
- storing raw chat transcripts.

## Data Model

### Recent Run Pointer

After each observed capability run, keep a small pointer that later prompts can use:

```json
{
  "version": "0.1.0",
  "last_run": {
    "run_id": "arcanum-hook-abc123",
    "capability": {
      "id": "distill",
      "kind": "sigil",
      "tier": "arcana",
      "mode": "skill"
    },
    "target_artifact": ".agents/skills/distill/SKILL.md",
    "ended_at": "2026-05-23T00:00:00Z",
    "summary": "Reviewed skill-aware observation work-pack."
  },
  "recent_runs": [
    {
      "run_id": "arcanum-hook-abc123",
      "capability_id": "distill",
      "ended_at": "2026-05-23T00:00:00Z",
      "summary": "Reviewed skill-aware observation work-pack."
    }
  ]
}
```

Possible path:

```text
.arcanum/observability/active-run-context.json
```

If Necronomicon is active, it may mirror this into:

```text
.arcanum/necronomicon/sessions/<session-id>/active-interaction.json
```

### Feedback Event

When a later user turn is attributed to a prior run, append a separate event:

```json
{
  "timestamp": "2026-05-23T00:02:00Z",
  "event_type": "continuation-feedback",
  "linked_run_id": "arcanum-hook-abc123",
  "capability": {
    "id": "distill",
    "kind": "sigil",
    "tier": "arcana",
    "mode": "skill"
  },
  "feedback": {
    "kind": "correction",
    "confidence": "high",
    "summary": "User says the plan missed delayed feedback from later prompts.",
    "evidence": "User: 'the problem is not when its still running... answers ... in the next two prompts'"
  },
  "observer": {
    "quality_bar_status": "partial",
    "workflow_gaps": [
      {
        "category": "process",
        "severity": "medium",
        "summary": "Original architecture optimized post-run extraction but missed delayed user feedback attribution.",
        "evidence": "Continuation prompt identified missing next-turn correction loop."
      }
    ],
    "reflection_trigger": "none",
    "recommendation": "targeted-update"
  }
}
```

The event can be stored in the same central ledger if `observe-invocation.sh` accepts `event_type`, or in a sibling feedback ledger:

```text
.arcanum/observability/signals/continuation-feedback.jsonl
```

Recommended first implementation: sibling feedback ledger. It avoids overloading the invocation schema before the model is proven.

## Classification Rules

Classify the next user turn against recent runs before routing fresh.

| Signal | Feedback Kind | Attribution |
| --- | --- | --- |
| "that missed...", "you forgot...", "not enough", "why didn't..." | correction | high if prior run is within 1-2 turns |
| "what do you mean by..." | clarification | high if about prior answer terms |
| "so should we..." | continuation | medium/high if it continues prior design route |
| "this route is wrong" | route-miss | high |
| "actually use X instead" | route-switch | medium/high |
| unrelated new task | fresh | no attribution |

Default attribution window:

- previous 2 user turns,
- previous 1 observed run,
- or active Necronomicon interaction if present.

## Runtime Flow

```text
Observed run closes
  -> write active-run-context.json

Next UserPromptSubmit
  -> if explicit command/skill, route normally
  -> otherwise compare prompt to active-run-context
  -> if continuation feedback, write feedback candidate

Stop or Necronomicon checkpoint
  -> append feedback event
  -> update gap ledger / active interaction when Necronomicon is present
```

## Relationship To Derive Invocation Telemetry

`derive-invocation-telemetry` handles evidence available at closeout:

- final message,
- tool events,
- skill profile,
- run status.

Continuation feedback attribution handles evidence available after closeout:

- user correction,
- user confusion,
- route dissatisfaction,
- continuation pressure.

They are complementary. Neither replaces the other.

## Relationship To Necronomicon

Necronomicon should own durable conversation memory and route history. Observability should own telemetry event shape and append mechanics.

Boundary:

| Concern | Owner |
| --- | --- |
| recent run pointer | observability |
| active interaction | Necronomicon |
| feedback event schema | observability |
| route/gap ledger | Necronomicon |
| maintenance proposal from repeated feedback | workflow-reflect or Necronomicon maintain |

## Minimal Implementation Plan

L0:

- write `.arcanum/observability/active-run-context.json` after observed runs,
- detect obvious next-turn corrections in UserPromptSubmit,
- write `.arcanum/observability/runs/arcanum-feedback/<id>/feedback-candidate.json`.

L1:

- append feedback events to `signals/continuation-feedback.jsonl`,
- include linked `run_id`, capability id, feedback kind, confidence, summary, and workflow gap.

L2:

- when `.arcanum/necronomicon/` exists, mirror feedback to Necronomicon's session gap ledger or active interaction.

L3:

- use accumulated feedback events in `workflow-reflect` and Necronomicon maintain mode.

## Open Design Decisions

| Decision | Recommendation |
| --- | --- |
| Same ledger or separate ledger? | Start with separate `continuation-feedback.jsonl`; later decide whether to merge event types. |
| How many turns to attribute? | Start with two user turns or one active interaction. |
| Should feedback block current routing? | No. It should annotate and continue unless user explicitly asks to revise. |
| Does Necronomicon need to be required? | No. Observability can record feedback alone; Necronomicon enriches it when installed. |

## Next Route

- Update the skill-aware observation work-pack with a deferred-but-designed continuation feedback slice.
- Do not implement full Necronomicon now.
- Implement derive telemetry first, then add continuation feedback attribution as the next coherent layer.

