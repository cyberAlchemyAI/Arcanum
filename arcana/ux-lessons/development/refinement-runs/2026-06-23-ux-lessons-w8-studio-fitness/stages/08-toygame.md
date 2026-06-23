# Stage 8 evidence — toy_game: project `detail-beside-the-subject` → FitnessVector

**Falsification question:** does the s6 projection turn the real `detail-beside-the-subject` ux-pattern (example 02) into a valid studio fitness intent using ONLY existing `FitnessVector` fields, with the honesty rule intact?

## Input (the pattern's validator claim map)
- `hard_gate`: "detail panel in-viewport & adjacent to the inspected element" (geometric, objective)
- `soft_flag`: "detail updates within one interaction"
- `human_study`: "co-visibility reduces perceived effort"
- `screenshot_review`: "looks balanced beside a wide stack"
- pattern `status: seed`, `signal_strength: anecdote`

## Projected `studio_fitness_intent` (output body)
```yaml
pattern_id: detail-beside-the-subject
hard_gate_refs: []        # NONE — the co-visibility claim is checkable, BUT signal_strength=anecdote (<repeated) ⇒ NOT promoted to a hard gate (honesty rule)
soft_signals:
  - dimension: cognitive/attention   # "divided attention"
    preference: 1
    severity: low
    confidence: 0.3                   # anecdote
    source: governance                # fallback; `pattern` pending studio enum decision (DR-1)
  - dimension: laws-of-ux:proximity
    preference: 1
    severity: low
    confidence: 0.3
    source: governance
human_objective_residue:
  - "co-visibility reduces perceived effort (human_study — surfaced to the human objective, not machine-scored)"
parked_until: ["studio axe/layout evaluator in cycle", "OQ-5 soft-score weights"]
```

## Verdict: SURVIVED
- Uses only existing `FitnessVector` fields (preference/severity/confidence/dimension) — **no invented fields**.
- **Honesty rule held (DR-2 example):** the co-visibility claim *is* objectively checkable, yet because `signal_strength=anecdote` it is **NOT** emitted as a hard gate — it lands as a low-confidence soft signal. A future `repeated`/`cross_session` capture of the same pattern *would* qualify the hard-gate ref. This is exactly the qualified-promotion rule working.
- `source: pattern` correctly fell back to `governance` (DR-1) rather than inventing an enum value.
- Confirms producer boundary: the intent is a *candidate*; studio still owns whether/how it weights it (OQ-5) and never discards on it.
