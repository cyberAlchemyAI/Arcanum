# Stage 1 — Context baseline (lean) · pass

**Studio fitness model (SPEC.md:169-200, already designed):**
- `GenerationMode{explore, exploit}` driven by the studio's UX-constraint layers as the fitness signal.
- **Hard gates** (binary, fail ⇒ discard in both modes): L1 a11y (axe), L2 layout integrity, deterministic L3.
- **Soft gradient** (scored, never discards): L4 cognitive/attention, `laws-of-ux`, subjective L3. Human objective weights soft terms.
- Signal **informs selection only — never gates disposal** (DEC-REVERSIBILITY-NOT-GATING-026).
- Types: `FitnessSignal`, `FitnessVector(preference -1|0|1 / severity / confidence 0..1 / dimension)`, `FitnessSignalSource(human|test|risk|telemetry|governance)`.

**Blockers (carried):** per-candidate constraint evaluator (axe/layout runner + ux-evidence-validator in the cycle) does not exist in code; **OQ-5** (soft-score weights + L4/laws-of-ux scoring functions; calibrate against UX-EVIDENCE-REPORT fixtures).

**Key insight (controls the design):** the ux-lessons `ux-pattern.consumer_intake.validator` already pre-sorts claims into 5 authority classes — which map *directly* onto the studio's hard-gate/soft-gradient split. So the producer-side mapping is largely a **re-projection of the already-designed validator claim map**, not a new mechanism.
