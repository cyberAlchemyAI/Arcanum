# Interrogation: Refine Definition

## Scope

Critique the `refine` definition before design and planning.

## Verdict

Status: pass with guardrails.

The proposed sigil is useful if it remains a seed/preflight controller. It becomes harmful if it copies Task Session's execution gates or duplicates the Refine Loop phase choreography outside the loop contract.

## Findings

### INT-REFINE-001: Risk Of Duplicating Task Session

Severity: high.

Risk: `refine` could start building context packs, gates, and runtime handoff logic itself.

Resolution: `refine` may summarize handoff readiness, but Task Session remains the authority for context pack generation, gate checks, execution, validation, evidence review, and synchronization.

### INT-REFINE-002: Risk Of Duplicating Refine Loop

Severity: high.

Risk: `refine` could copy the phase list and drift from the profile.

Resolution: `refine` references `REFINEMENT-LOOP.md` for the one-loop unit, presets, research bounds, mutation guard, and output requirements. If the loop changes, update the loop contract, not scattered `refine` prose.

### INT-REFINE-003: Research Must Be Offered But Not Smuggled In

Severity: medium.

Risk: external research can change budget, privacy posture, or evidence authority.

Resolution: `refine` always offers research choices and records the selected research mode. Local repository evidence remains authoritative.

### INT-REFINE-004: Codex Goal Default Needs A Blocked Path

Severity: medium.

Risk: "default to Codex Goal" could become unsafe if handoff artifacts or strict coverage are missing.

Resolution: default to Codex Goal as the intended runtime, but block rather than silently fall back when strict handoff coverage is missing.

### INT-REFINE-005: Confirmation Gate Is Non-Negotiable

Severity: medium.

Risk: a seed controller could create artifacts or delegate execution before the user accepts the budget and scope.

Resolution: `refine` proposes first. It only writes seed artifacts or delegates after explicit confirmation.

## Required Repairs

- Make research offer part of the preflight output contract.
- Make Codex Goal default but strict-coverage gated.
- Make local execution an explicit override, not fallback.
- Make Sigil Development the lifecycle handoff owner.

## Proceed Decision

Proceed to Distill with candidate shapes:

- seed/preflight controller,
- Task Session fallback mode,
- Invoke wrapper,
- new refinement engine.
