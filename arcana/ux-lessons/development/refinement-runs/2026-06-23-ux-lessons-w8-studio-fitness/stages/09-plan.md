# Stage 9 — Invoke Plan (parked) · pass

**This is a parked plan. The build is blocked; nothing here executes until the named unblocks land.**

## When unblocked
Trigger to un-park: BOTH (a) studio per-candidate evaluator exists (axe/layout runner + ux-evidence-validator wired into the cycle), AND (b) studio OQ-5 resolved (soft-score weights + L4/laws-of-ux scoring functions).

## Build steps (parked)
1. Add `emit-studio-fitness` mode to ux-lessons SKILL.md (output = `studio_fitness_intent` schema from stage 06). Producer-side only — buildable even before the studio side, but pointless to ship until consumed.
2. Open a studio decision request: add `pattern` to `FitnessSignalSource`, or confirm `governance` fallback.
3. When studio evaluator + OQ-5 exist: wire `studio_fitness_intent.soft_signals` into the explore/exploit cycle as candidate `FitnessVector`s; map `hard_gate_refs` (signal≥repeated) onto L1/L2 acceptance.
4. Calibrate confidence→weight against the UX-EVIDENCE-REPORT fixtures (studio-owned, OQ-5).

## Validation surface (when run)
Projection uses only existing FitnessVector fields; honesty rule (anecdote⇏hard_gate) enforced; never gates disposal; producer boundary preserved.

## Out of scope
The studio evaluator, the weights (OQ-5), and any disposal-gating. All studio-owned.
