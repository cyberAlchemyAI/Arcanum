---
stage: Research decision
owner: refine
status: pass
research_mode: research-if-gap-appears
---

# Research Decision

## Decision

Use local evidence for this refine execution. Do not run external web research
inside this stage.

## Reason

The user asked for next-step refinement after local harness completion. Local
artifacts are sufficient to distinguish current state, desired state, and the
immediate next governed route.

## Deferred External Research Trigger

Bounded web research should be requested before publication framing if the next
route attempts to declare novelty, update related work, or submit the paper.

Named gap:

- current prior-art freshness and novelty position may be stale relative to
  2026 literature.

## Confirmation Needed Later

Ask before external prior-art refresh unless the user explicitly selects
bounded research for the next run.
