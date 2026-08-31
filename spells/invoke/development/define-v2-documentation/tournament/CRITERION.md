<!-- Generated from CRITERION.json by render_criterion.py. Do not edit this view directly. -->

# Pre-Registered Criterion: Define v2 Documentation Order

## State

- Status: `proposed`
- Freeze owner: human confirmation gate
- Run status: `not_started`
- Criterion version: `3`

This criterion must be confirmed and frozen before any trial result exists.

Editing the hypothesis, cases, guide-to-candidate map, scorer, outcome rule, or trial brief after freeze creates a new criterion.

A freeze record must bind these inputs by SHA-256 and byte size:

- CRITERION.json
- criterion.schema.json
- render_criterion.py
- CRITERION.md
- TOURNAMENT-SPEC.md
- GUIDE-MANIFEST.json
- oracle/blind-map.json
- every rendered guide
- every case and trial brief
- oracle/cases.json
- score_tournament.py and its runtime
- compiler executable and schema bytes
- root scorer identity and scoring command

## One Falsifiable Hypothesis

The ownership-first progressive guide produces more correct first-attempt invoke.define-source.v2 documents than both the schema-order guide and the tutorial-first guide when otherwise identical agents solve the same three real authoring cases.

## Fixed Candidates

The three candidate structures are:

1. ownership-first progressive
2. schema-order
3. tutorial-first

There are exactly 3 cases, 2 trials per candidate, and 3 source records per trial. This yields 6 total trials, 18 source records, and 3 candidate aggregates.

The sealed map binds alpha, beta, and gamma to the three structures before any run, remains hidden from trial agents, and is revealed only to the root scorer after all six terminal joins.

## Observable

Each candidate aggregate is an ordered four-metric tuple:

1. number of sources that compile atomically (more)
2. number of compiled sources whose intended semantic projection matches the case oracle (more)
3. number of category errors detected in authored source bytes (fewer)
4. total deterministic score (more)

The parent compiles each first-returned source exactly once. Semantic projection is evaluated only for atomically compiled sources; a non-compiling source contributes zero semantic passes.

The freeze-bound scorer alone computes category errors and total score and must retain per-source contributions from which every aggregate can be re-summed.

## Mechanical Outcome Rule

Apply invalidation before ranking. Otherwise compare the three candidate aggregate tuples lexicographically across the four stated metrics in this order:

1. atomic_compile_passes
2. semantic_projection_passes
3. category_errors
4. deterministic_score

- `SURVIVED`: Render SURVIVED only when ownership-first is the sole lexicographic maximum.
- `FALSIFIED`: Render FALSIFIED when another candidate is the sole maximum or two or more candidates share the maximum tuple.
- `INVALID`: Render only INVALID when any invalidation condition holds; do not also report SURVIVED or FALSIFIED.

Render `INVALID` if any of the following holds:

1. Other than exactly six preassigned trials reach terminal completion, or a trial lacks its one assigned opaque guide, three required first-returned sources, and structured receipt.
2. Trials are replaced, reassigned, merged, or allowed to share an agent, source directory, conversational context, or another trial's artifacts.
3. A trial agent reads a forbidden scope, learns the opaque-label mapping, views another guide or trial, invokes the compiler or scorer, or receives materially different instructions beyond its assigned opaque guide.
4. Rendered candidates differ in section inventory or section bytes rather than section order, as checked against the freeze-bound manifest and independent guide-equivalence receipt.
5. Any first-returned source byte is repaired, regenerated, normalized, or otherwise changed before scoring.
6. Any freeze-bound input, runtime, compiler, schema, oracle, scorer, command, or identity is missing or differs at scoring or re-adjudication.
7. The scorer does not emit all 18 per-source records and three candidate aggregates, cannot re-sum those aggregates from the per-source records, or a clean re-run over the same freeze-bound bytes changes the scorecard payload outside explicitly excluded run metadata.
8. Any required receipt reports a policy breach or leaves a required isolation, source-identity, or read-scope assertion unknown.

## Discrimination Check

- `SURVIVED`: Supports using ownership-first ordering for the first public Invoke Define v2 authoring guide under this model and case set.
- `FALSIFIED`: Shows the editorial preference did not produce a uniquely better first-attempt result and should not be promoted as a tested behavioral advantage.
- `INVALID`: Says nothing about documentation quality; redesign or repeat under a newly frozen criterion.

## Non-Goals

- This tournament does not test every model, repository, definition domain, or future schema revision.
- It does not prove the candidate Whisper transport.
- It does not establish that generated definitions are true, accepted, active, or promoted.
- With two trials per candidate, any result is directional evidence rather than a universal performance claim.
