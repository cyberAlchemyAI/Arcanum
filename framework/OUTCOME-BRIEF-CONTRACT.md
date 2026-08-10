# Outcome Brief Contract

The Outcome Brief Contract makes a capability result understandable before it
makes the result auditable. It is a human-facing projection of the same evidence
used by the technical result and machine receipts; it is not a replacement for
those receipts and grants no authority.

## Problem It Solves

Arcanum capabilities can return precise paths, statuses, validators, digests,
and receipts while still leaving the operator to reconstruct what happened and
why it matters. That is strong audit evidence but weak communication.

Every significant user-facing result should therefore lead with meaning, state
its boundary and next decision, and only then show the technical details.

## Required Order

Use these layers in this order:

```markdown
## Outcome Brief

<Two to five plain-language sentences that explain the objective, result, and
why the result matters.>

- Objective: <what the capability was trying to accomplish>
- Result: <what is now known, available, completed, flagged, or blocked>
- Why it matters: <the practical consequence for the operator or next owner>

## Boundary and Next Decision

- Changed: <what changed in artifacts, evidence, or state>
- Unchanged: <what explicitly did not change, including authority boundaries>
- Open questions: <remaining uncertainty or none>
- User decision: <the exact decision needed or none>
- Next action: <the next bounded action and owner>

## Technical Details

<The capability's existing detailed result, receipt references, paths, hashes,
validation results, statuses, and follow-up fields.>
```

The first paragraph is the primary explanation. The labeled fields make that
explanation easy to scan and harder to omit.

## Plain-Language Rules

- Start with the practical outcome, not the command, workflow, artifact list,
  receipt, hash, or internal identifier.
- Avoid undefined acronyms, internal status names, and paths in the opening
  paragraph. Translate them when they are necessary.
- Say `blocked`, `incomplete`, or `not run` plainly when that is the result.
- Explain why the result matters without claiming evidence that the technical
  result does not contain.
- Keep the brief short. Technical nuance belongs in the final layer.

## Evidence And Authority Boundary

- Derive every brief statement from the same run evidence as the technical
  result. Do not invent an interpretation that the receipt cannot support.
- A brief does not turn a proposal into a decision, a plan into implementation,
  validation into promotion, or a receipt into authority.
- Preserve machine-readable receipt schemas and digest identities. The Outcome
  Brief is a sibling human projection unless an owning schema explicitly adds a
  compatible field.
- When evidence conflicts, describe the conflict under `Open questions` and
  keep the stricter technical verdict. The machine receipt and lifecycle-owner
  evidence control when the human projection conflicts with them.
- Do not turn a missing-evidence or unavailable-tool blocker into a user
  approval question. Ask for a decision only when a real operator choice can
  change the route.
- When no user decision is required, write `none`; do not manufacture a gate.

## Pre-Execution Results

Strategies, previews, and proposals also use the first two layers. Their third
layer is still named `Technical Details`, because a proposal is not an execution
receipt. The boundary must say that no execution or mutation has occurred and
name the exact confirmation, if any, needed to proceed.

## Pilot Bindings

The first pilot covers:

| Capability | Canonical contract | Required user-facing results |
| --- | --- | --- |
| `invoke` | `spells/invoke/README.md` | every root mode result |
| `refine` | `arcana/refine/SKILL.md` | strategy proposal and final result |
| `task-session` | `arcana/task-session/SKILL.md` | terminal result, including blocked results |

Each pilot contract repeats the required fields so generated skill packages are
self-contained even when this framework document is not installed beside them.

## Conformance

A pilot capability conforms when:

- `Outcome Brief` appears before `Boundary and Next Decision`;
- both appear before the existing detailed result;
- objective, result, significance, changed, unchanged, uncertainty, user
  decision, and next action are explicit;
- blocked and pre-execution results preserve their real status;
- existing machine receipts and authority semantics remain unchanged; and
- generated Codex and Claude skill projections preserve the same ordering.
