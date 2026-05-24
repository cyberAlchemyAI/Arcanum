# Skill-Aware Observation Interrogation

## Scope

Review the current skill-aware observability update after adding:

- `DERIVE-INVOCATION-TELEMETRY-DESIGN.md`,
- `CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md`,
- `SKILL-AWARE-OBSERVATION-LAYERING.md`,
- `SKILL-AWARE-OBSERVATION-WORK-PACK.md`.

The review asks whether the architecture needs more artifacts before implementation.

## Verdict

Status: flag.

The design is coherent enough to implement the L0-L3 closeout path. It does not need a new broad architecture artifact. It did need the existing architecture overview refreshed so it does not keep describing Move 1 as only envelope open/close.

Continuation feedback should remain a deferred layer, not part of the first implementation window.

## Findings

### INT-OBS-001: Architecture Overview Lagged The New Dual-Loop Model

Severity: medium.

Evidence:

- The development design and work-pack describe derivation and continuation feedback.
- `ARCHITECTURE-OVERVIEW.md` still centered the old "Observed Invocation Envelope Pipeline" and recommended Move 1 as preserving the same Stop-hook closeout path.

Risk:

Implementation could skip `derive-invocation-telemetry.sh` or treat delayed feedback as out of scope because the top-level architecture did not name those responsibilities.

Resolution:

Patch the architecture overview to name the **Observed Run Feedback Cycle**, add derivation before append, and add continuation feedback as a linked delayed-feedback ledger.

### INT-OBS-002: Do Not Create A Second Architecture Family Yet

Severity: low.

Evidence:

- The development pack already has one architecture overview, one design, one derivation design, one continuation design, one layering artifact, and one work-pack.
- The missing piece was synchronization, not absence of another artifact type.

Risk:

Adding another broad architecture document would duplicate authority and create drift.

Resolution:

Keep one architecture overview and one development pack. Add focused review artifacts only when they record validation findings or decisions.

### INT-OBS-003: Continuation Feedback Needs Implementation Gates Before Necronomicon Integration

Severity: medium.

Evidence:

- The user-identified signal appears after the skill run, often in the next one or two prompts.
- Necronomicon owns active interaction and durable gap memory, but full integration is larger than the closeout derivation change.

Risk:

Tackling Necronomicon first would expand scope before the feedback event shape is proven.

Resolution:

Implement active-run context and `signals/continuation-feedback.jsonl` first. Mirror to Necronomicon only after feedback events are useful and stable.

## Artifact Decision

No new broad design or architecture artifact is required now.

Keep these as the authoritative set:

- `ARCHITECTURE-OVERVIEW.md`: top-level architecture and moves.
- `SKILL-AWARE-OBSERVATION-DESIGN.md`: detailed bridge design.
- `DERIVE-INVOCATION-TELEMETRY-DESIGN.md`: closeout extraction boundary.
- `CONTINUATION-FEEDBACK-ATTRIBUTION-DESIGN.md`: delayed feedback boundary.
- `SKILL-AWARE-OBSERVATION-LAYERING.md`: layer sequencing.
- `SKILL-AWARE-OBSERVATION-WORK-PACK.md`: execution plan.
- This file: interrogation validation record.

## Implementation Gate

Proceed with L0-L3 only:

1. Explicit skill detection.
2. Derive invocation telemetry.
3. Observer preservation of enriched fields.
4. Route regression fixtures.
5. Documentation sync.

Defer L4 continuation feedback until L0-L3 pass validation.

## Remaining Question

One decision can wait until L4:

Should continuation feedback events stay permanently in a sibling ledger, or should `observe-invocation.sh` evolve into a generic event append authority with typed event schemas?

Recommended default: sibling ledger for the pilot.

## Structured Interview Result

- Target scope: skill-aware observability development pack.
- Mode: validation review.
- Questions asked: 0.
- Decisions recorded: 2.
- Artifacts updated: `ARCHITECTURE-OVERVIEW.md`; this review artifact.
- Remaining ambiguities: long-term feedback ledger unification.
- Verdict: flag.
- Next step: implement L0-L3 through `task-session`.
