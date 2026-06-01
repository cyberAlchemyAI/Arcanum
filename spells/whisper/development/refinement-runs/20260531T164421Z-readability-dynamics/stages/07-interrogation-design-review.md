# Stage 07: Interrogation Design Review

Status: `pass`

## Review Findings

The design is directionally correct, with three required repairs.

## Repair 1: Do Not Make Beat IDs Authoritative Without Source Mapping

`beat_id` must be derived from source blocks or declared in the schema. It cannot become an untraceable visual-only unit.

Decision: `beat_id` is a child anchor under `block_id`.

## Repair 2: Keep Visual Treatment Transport-Specific

A Substack post may benefit from short paragraphs, micro-heads, pull quotes, and question lines. Fundraising copy will need proof blocks, trust markers, objection handling, and ask mechanics. Slides will need slide beats.

Decision: `visual_treatments` should live inside `transport_schema` or be referenced from it.

## Repair 3: Avoid Pseudo-Scientific Readability Scores

The first validator should not pretend to measure all comprehension. It should enforce simple, inspectable checks that help operators and agents identify block walls.

Decision: start with deterministic thresholds and explicit flags. Add computational cohesion metrics only after the schema and renderer are stable.

## Verdict

The design passes if implemented as a lightweight layer with source-stable anchors, transport-specific visual treatments, and validator flags rather than opaque quality scores.

