---
tags: [craft, ledger-integrity, evidence-governance]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-25T11:42:36-03:00
updated_at: 2026-08-25T11:42:36-03:00
expires: 2026-10-24
decisions_made: true
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session separated two load-bearing Craft problems and established a bounded starting point for investigating ledger integrity."
---

# Craft: semantic evolution and ledger integrity

## Summary

The session examined the existing Craft claim-evidence-strengthening material to determine what it contained and whether it framed the work that Craft actually needs. It established that the material was an initial informational definition rather than completed research. Two distinct Craft problems were separated: evolving Craft with new concepts and ensuring that its authoritative ledger, derived views, and capability handoffs remain current and mutually consistent. They should not be collapsed because the first asks what semantics Craft should gain, while the second asks which existing state transitions can drift and what integrity properties they require. The ledger-integrity question has a concrete local witness in a Craft ledger whose blocker index and lifecycle values diverge from canonical contracts, but that witness does not establish the cause or repository-wide prevalence. A dedicated initial-definitions artifact was created for ledger integrity while keeping methods, agents, source plans, and proposed solutions outside the baseline. The baseline preserves Craft's current authority boundary: the ledger remains authoritative, derived views remain non-authoritative, and called capabilities retain ownership of their native artifacts and verdicts. Further investigation should keep internal repository evidence distinct from external precedent and treat semantic evolution as a separate Craft research scope.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Craft capability](../arcana/craft/SKILL.md) | `is-part-of` | This session frames two unresolved questions about the Craft capability's semantics and ledger guarantees. |
| [Craft ledger-integrity initial definitions](../research/craft-ledger-integrity/research-initial-definitions.md) | `contextualizes` | This session records the decisions and evidence boundary that produced the ledger-integrity baseline. |
| [Goal Craft ledger](../spells/goal/.craft/ledger.yml) | `contradicts` | The observed closed blocker remaining in the active-blocker index and noncanonical lifecycle state conflict with the current Craft contract. |

## Open questions

- Which Craft state transitions can cause authoritative rows, derived indexes, human views, and native capability results to diverge, and which divergences are Craft's responsibility?
- Which new claim-evidence concepts, if any, should enter Craft through the separate semantic-evolution line of research?

## Next steps

1. Run the Craft ledger-integrity investigation from its validated baseline, keeping internal evidence and external precedent distinct.
2. Open a separate Craft research scope for semantic evolution before proposing new claim-evidence concepts.

## Recommendation

Prioritize ledger integrity first because a concrete repository inconsistency already witnesses the problem, while keeping semantic evolution as the separate second research line identified above.

## Files touched

- `research/craft-ledger-integrity/research-initial-definitions.md`
