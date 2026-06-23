# Stage 3 — Interrogation refine-review · pass (parent-only, no subagents)

**Critique of the Define:**
- **R1 (duplication risk):** a separate fitness projection would duplicate the validator claim map. → Resolution: reuse it. The validator claim_class already encodes hard vs soft; the projection is a re-tag, not a new analysis.
- **R2 (honesty risk):** an anecdote-signal pattern must not become a studio *hard gate* any more than a validator hard gate. → The honesty rule transfers: `signal_strength` maps to `FitnessVector.confidence`; anecdote ⇒ low confidence ⇒ soft term only.
- **R3 (boundary risk):** ux-lessons could drift into owning weights/evaluator. → Keep the producer/consumer line: ux-lessons emits a `FitnessSignal` *candidate*; studio owns the cycle, the weights (OQ-5), and the per-candidate evaluator.
- **R4 (scope):** build is blocked; what ships? → Only the projection *design* + a parked adapter spec. Nothing enters studio until the evaluator + OQ-5 exist.

Carried to Design: reuse validator map (R1), confidence-from-signal honesty (R2), strict producer boundary (R3), design-only scope (R4).
