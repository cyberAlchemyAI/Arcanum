# Stage 6 — Invoke Design · pass

## Route-menu decisions (resolved)
| Decision | Options | Resolved | Why |
| -------- | ------- | -------- | --- |
| capability_shape | new mode / extend `emit-studio` | **new mode `emit-studio-fitness`** | distinct output (FitnessSignal candidate vs CommentEvent); keeps the annotation path clean |
| scope | design+parked / build now | **design + parked adapter spec** | build is blocked; ship nothing into studio yet |
| mapping ownership | ux-lessons / studio | **ux-lessons owns the projection; studio owns cycle + weights (OQ-5) + evaluator** | preserves producer/consumer boundary |

## X-ray structure map (the mapping)

```
ux-pattern.consumer_intake.validator[ claim_class ]      ──►  studio fitness role        ──►  FitnessVector
─────────────────────────────────────────────────────         ───────────────────────         ─────────────────────────────
hard_gate        (objective, geometric/a11y/layout)     ──►   HARD GATE (fail ⇒ discard)  ──►  (not a vector; a gate ref:
                                                                = existing L1/L2 acceptance       feeds the candidate evaluator)
soft_flag        (heuristic/latency)                     ──►   SOFT gradient               ──►  { dimension, preference:±1,
screenshot_review(subjective-but-reviewable)             ──►   SOFT gradient (lower weight)      severity, confidence }
human_study      (perceived/felt)                        ──►   HUMAN OBJECTIVE only        ──►  (no machine term; residue)
not_automatable  (—)                                     ──►   dropped                     ──►  (—)
```

**Confidence rule (honesty transfer):** `FitnessVector.confidence = f(signal_strength)` → `anecdote≈0.3`, `repeated≈0.6`, `cross_session≈0.9`. A `hard_gate` mapping is emitted **only** when the underlying claim is objectively checkable AND `signal_strength ≥ repeated`; anecdote patterns emit soft terms only. (This is the `<honesty rule>` from SKILL.md, re-expressed in studio terms.)

**FitnessSignalSource:** ux-lessons emits with a new conceptual source `pattern` (or, if studio won't add an enum value, reuse `governance`) — flagged for studio to confirm; ux-lessons does not assume the enum.

## `emit-studio-fitness` adapter (design)
Input: a `ux-pattern` (status ≥ seed). Output: a `studio_fitness_intent` =
```yaml
pattern_id:
hard_gate_refs: []          # claims that should be wired as hard gates (only if checkable + signal>=repeated)
soft_signals:               # one FitnessVector candidate per soft claim
  - dimension:              # e.g. cognitive/attention, laws-of-ux:<law>
    preference:             # -1 | 0 | 1
    severity:
    confidence:             # from signal_strength
    source: pattern         # pending studio enum confirmation
human_objective_residue: [] # human_study claims, surfaced not scored
parked_until: ["studio axe/layout evaluator in cycle", "OQ-5 soft-score weights"]
```

## Buildable-now vs blocked
- **Buildable now (producer side):** the `emit-studio-fitness` projection design + a parked adapter spec in ux-lessons. Pure data transform; no studio dependency to *produce* the intent.
- **Blocked (consumer side):** studio *using* the intent — needs the per-candidate evaluator (axe/layout + ux-evidence-validator in the cycle) AND OQ-5 (weights/scoring). Until both exist, the intent is authored-and-parked, never wired.

## Boundary preserved
ux-lessons emits a candidate signal; studio owns selection pressure, weights, evaluator, and disposal policy (which never discards on this signal anyway).
