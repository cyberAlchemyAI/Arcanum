# Playbook: Reuse The Whisper-Core Pattern For Your Own Idea

Use this playbook when you have a broad idea and want to explore it before turning it into implementation work.

## 1. Name The Idea

Write the richest version first:

```text
I want to build a tool/workflow/guide that helps <audience> do <outcome>.
It matters because <promise>.
It should not <risk>.
MVP proof would be <evidence>.
The ambitious version could become <future>.
```

## 2. Extract The Three Cores

| Core | Fill This In |
| --- | --- |
| `idea_resonance` | What should this make the user feel, trust, notice, or believe is possible? |
| `idea_relevance` | Who is it for, what context does it enter, and what objections must be respected? |
| `idea_trajectory` | What movement does the user make from first contact to proof of value? |

## 3. Generate Candidate Routes

Create at least three routes:

- a balanced route,
- a utility-first route,
- a conceptually ambitious route.

Score each one across resonance, relevance, and trajectory. Preserve rejected candidates and why they were rejected.

## 4. Add Hard Gates

Hard gates are not preferences. They are checks that prevent a candidate from winning even if it is attractive.

Examples:

- accessibility gate,
- citation integrity gate,
- audience legibility gate,
- privacy gate,
- scope boundary gate,
- runtime feasibility gate,
- evidence safety gate.

## 5. Decompose The Selected Candidate Into Parts

For each part, define:

- responsibility,
- dependencies,
- inputs,
- must-do rules,
- must-not-do rules,
- validation checks,
- mini-tournament triggers if the part is delegated, revised, or fails validation.

## 6. Create One Task-Session Unit

A task-session unit should be small enough to finish with evidence.

Use this shape:

```text
[$task-session] Execute <work-pack path> --swu <SWU-ID>
```

The SWU should have:

- source anchors,
- write scope,
- done criteria,
- validation commands,
- acceptance evidence,
- follow-up residue.

## 7. Preserve Residue

Residue is not failure. It is the next loop.

Record:

- unresolved decisions,
- blocked references,
- rejected candidates,
- next transport pressure,
- validation gaps,
- user review needs,
- future fixture ideas.

## Reusable Prompt

```text
[$refine] I want to explore this idea using the Whisper-core pattern.

Idea:
<describe the broad idea>

Please extract idea_resonance, idea_relevance, and idea_trajectory.
Then compare candidate routes, add hard gates, choose a non-dominated route, decompose it into parts, and produce the next task-session-ready SWU.
```
