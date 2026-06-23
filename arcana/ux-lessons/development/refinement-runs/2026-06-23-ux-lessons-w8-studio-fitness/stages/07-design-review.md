# Stage 7 — Interrogation design-review · flag (2 non-blocking)

- ✅ Reuses the validator claim map (no duplicate analysis); honesty rule transferred via `confidence = f(signal_strength)`; producer boundary held; build-blocked named.
- ⚠ **DR-1:** the `FitnessSignalSource` value `pattern` is **not** in the studio enum (`human|test|risk|telemetry|governance`). The design correctly does not assume it. → Repair: name a fallback (`governance`) and flag a studio decision; do not invent an enum value unilaterally.
- ⚠ **DR-2:** the `hard_gate` projection rule (checkable AND `signal ≥ repeated`) needs an explicit example to be unambiguous. → Repair: the toy_game must show one claim that qualifies and one that does not.

No contested ownership and no scored alternatives remained → `dialectic`/`tournament` not triggered (recorded).
