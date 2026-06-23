# Stage 8 evidence — toy_game falsification on the x-ray session

- **Technique:** toy_game + assessment_failure_reference · **Fixture:** the live x-ray iteration session (`refine-skill-xray.html`)
- **Falsification question:** Does the s6 design actually turn THIS session's moves into a `ux-pattern` that BOTH consumers can ingest? If any step needs invention not in the schema, the design is falsified.

## Step 1 — capture lessons from the real session
Three real iteration moves became `lesson` records:

| lesson_id | trigger / failure_mode | change | signal_strength |
| --------- | ---------------------- | ------ | --------------- |
| L-xray-01 | 3D isometric tilt made text illegible & overflowed (screenshots 01,03) | reverted 3D → offset cascade; depth via overlap+shadow, text level | repeated (recurred when 3D re-added then reverted again) |
| L-xray-02 | drill panel below stack split attention from the layers | moved detail into a sticky **right-rail beside the stack** | anecdote (one session) |
| L-xray-03 | layers received all-at-once; depth not understood | optional **guided tour** that constructs the stack one layer at a time | anecdote |

## Step 2 — distill to a ux-pattern (fill schema B)
**Pattern `detail-beside-the-subject`** (from L-xray-02):
- intent: keep explanatory detail co-visible with the thing it explains.
- problem: a separate/below detail panel forces eye travel → divided attention.
- solution: sticky inspector rail adjacent to the inspected structure; updates on hover.
- when_to_use: layered/structured artifact a user reads while needing per-item detail.
- anti_pattern: modal/below panel for per-item detail during active reading.
- evidence_link: screenshots 19-21 (right-rail updates on layer + nested-overlay hover).
- status: **seed** (anecdote signal — cannot promote to a validator hard_gate per honesty rule).

## Step 3 — emit to BOTH consumers (the actual falsification)
- **validator intake:** claim "detail panel is co-visible with the inspected element (no scroll/modal to read it)" → class **hard_gate proxy** via `mode=spec`→`fixture-plan` with good/bad/false-positive fixtures (panel in-viewport beside target vs below-fold vs visually-adjacent-but-occluded). ✅ maps with no invention.
- **studio intake:** `CommentEvent{ target:{odId:"inspector", elementLabel:"detail panel"}, severity:"major", intent:"reposition", note:"make detail co-visible with the subject (sticky rail), not below" }` → `MutationTask{ odId:"inspector", changeType:"layout-reposition" }`. ✅ maps with no invention.

## Verdict: SURVIVED (design not falsified)
Both consumer intakes filled from the schema with **zero invented fields**. One honest limit confirmed: anecdote-signal patterns stop at `seed`/`soft_flag` — they cannot drive a hard gate until cross-session signal accrues. This is the schema working as intended, not a failure.
