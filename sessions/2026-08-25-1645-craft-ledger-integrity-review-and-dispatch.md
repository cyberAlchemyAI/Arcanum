---
tags: [craft, ledger-integrity, research-governance]
artifact_kind: session
layer: capability
version: 0.1.0
created_at: 2026-08-25T16:45:17-03:00
updated_at: 2026-08-25T16:45:17-03:00
expires: 2026-10-24
decisions_made: true
contradictions_found: true
specs_updated:
  - research/craft-ledger-integrity/research-initial-definitions.md
  - research/craft-ledger-integrity/craft-ledger-integrity-research.dispatch.json
promoted_candidates: []
expected_importance: 8
importance_rationale: "The session made the Craft ledger-integrity scope reproducible, independently reviewable, and ready for a governed internal/external research dispatch without overstating route preparation as research evidence."
---

# Craft ledger integrity: reviewed baseline and deferred research dispatch

## Summary

The session resumed the bounded Craft ledger-integrity scope and confirmed that the earlier work had framed research rather than conducted it. An adversarial review found three major problems in the initial baseline: ambiguity between embedded and generated indexes, a mutable witness without a reproducible snapshot, and an unbounded proposal corpus. All three changes were applied to `research-initial-definitions.md`, whose structure and evidence snapshot were then validated. A governed seven-lane research dispatch was prepared to inspect repository evidence and external precedent, with local runtime, material-strategy, and composite-readiness checks passing. Two independent tension checks also passed the route and material strategy. No research agents were launched, no dispatch event was registered, and no `research.md` or `findings.md` was produced. The unexecuted investigation therefore remains an explicit open Craft point rather than a completed finding or an authorization to change canonical Craft surfaces.

## Connections

| Document | Type | Description |
|----------|------|-------------|
| [Earlier ledger-integrity scope](2026-08-25-1142-craft-ledger-integrity-scope.md) | `refines` | This session reviews, corrects, and operationalizes the research scope established in the earlier session. |
| [Research initial definitions](../research/craft-ledger-integrity/research-initial-definitions.md) | `validates` | The session records the adversarial review, applied corrections, and successful structural validation of the baseline. |
| [Review report](../research/craft-ledger-integrity/review.md) | `derives-from` | The three baseline corrections and the resulting readiness judgment derive from this severity-ranked review. |
| [Prepared research dispatch](../research/craft-ledger-integrity/craft-ledger-integrity-research.dispatch.json) | `contextualizes` | The dispatch encodes the prepared internal/external research route, but it has not been executed. |
| [Craft capability](../arcana/craft/SKILL.md) | `is-part-of` | The unresolved investigation concerns the integrity guarantees and responsibility boundary of the Craft capability. |

## Decisions

- Treat embedded `.craft/ledger.yml#indexes`, generated `.craft/index.json`, and `CRAFT.md` as distinct integrity surfaces throughout the research.
- Anchor mutable repository witnesses to a dated commit, stable selectors, authority status, dirty-state note, and content hashes.
- Keep the initial proposal corpus finite and authority-labelled rather than treating development material as canonical behavior.
- Leave the research dispatch unexecuted and visible as open work; route validation and tension checks establish readiness only.

## Contradictions and resolution

- The initial baseline blurred embedded and generated index obligations; the revised baseline now names each surface and preserves the current contractual ambiguity around embedded active-blocker filtering.
- The `spells/goal` ledger witness still contains a noncanonical typed-item lifecycle value and stale embedded active-blocker membership. This was recorded as evidence, not repaired, because the research scope is diagnostic and did not authorize mutation of that ledger.

## Open questions

- Which current Craft mutation entry points and state transitions can produce divergence, and how prevalent are the observed inconsistencies?
- Which integrity properties belong to schema validation, runtime behavior, generated surfaces, or operator discipline?
- Where is the exact boundary between applying a called capability's result and preserving that result as externally owned evidence?

## Next steps

1. Obtain explicit operator confirmation to launch the prepared internal/external research dispatch.
2. Execute the governed research and produce `research.md` and `findings.md`, including skeptic and citation checks required by the research protocol.
3. Use the reviewed findings to decide whether any Craft contract, validator, runtime, migration, or operator-discipline change is warranted.

## Recommendation

Keep the point open until the governed research is executed and reviewed. Do not treat the prepared dispatch as execution evidence, and do not repair the witness or change canonical Craft surfaces before the investigation establishes cause, prevalence, responsibility, and minimum integrity properties.

## Files touched

- `research/craft-ledger-integrity/research-initial-definitions.md`
- `research/craft-ledger-integrity/review.md`
- `research/craft-ledger-integrity/runtime-profile.json`
- `research/craft-ledger-integrity/dispatch-runtime.py`
- `research/craft-ledger-integrity/material-strategy.json`
- `research/craft-ledger-integrity/craft-ledger-integrity-research.dispatch.json`
- `sessions/2026-08-25-1645-craft-ledger-integrity-review-and-dispatch.md`
- `.craft/ledger.yml`
- `CRAFT.md`
