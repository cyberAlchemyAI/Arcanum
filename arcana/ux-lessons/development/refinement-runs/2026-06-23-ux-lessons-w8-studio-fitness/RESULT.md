# Refine Result — W8: ux-pattern → studio fitness mapping

- **Target:** the producer-side `ux-pattern → studio FitnessSignal` mapping (W8)
- **Status:** flag (design complete; 2 design-review flags repaired; build remains blocked by design)
- **Preset:** compact · **Research:** no-research
- **Run manifest:** `RUN-MANIFEST.md` · **Evidence index:** `evidence-index.json` · **Seed:** `REFINE-SEED-PROPOSAL.md`
- **Dispatch route:** `REFINE-DISPATCH.json` (dispatch-spec `VALIDATION=pass`)
- **Dispatch strategy:** overlays baseline_sequence + xray + route_menu + toy_game; subagent strategy `none` (authorization not_needed); dialectic/tournament not triggered.
- **Runtime handoff:** `RUNTIME-HANDOFF.md`
- **Stage evidence:** Context pass · Define pass · review pass · Research pass · Distill pass · Design pass · design-review flag(2 repaired) · Distill-Repair pass(toy_game survived) · Plan pass(parked) · Final pass

## Final synthesis

W8 is **smaller than it looked**. The studio already designed its exploit/explore fitness (SPEC.md §3): UX-constraint layers as the signal, a hard-gate/soft-gradient split, `FitnessSignal`/`FitnessVector` types. The only undesigned piece was the **producer-side projection** — and that turns out to **reuse the ux-pattern's existing validator claim map**:

- `hard_gate` claims → studio **hard gates** (only if objectively checkable AND `signal_strength ≥ repeated`),
- `soft_flag` / `screenshot_review` → studio **soft-gradient** `FitnessVector`s, with `confidence = f(signal_strength)`,
- `human_study` → **human objective** residue (not machine-scored),
- `not_automatable` → dropped.

So W8 is a new `emit-studio-fitness` mode that **re-tags** what ux-lessons already produces — *not* a new fitness engine. The honesty rule transfers cleanly: an anecdote pattern emits only low-confidence soft signals and **cannot** become a hard gate, even when the claim is geometrically checkable (proven in the toy_game on `detail-beside-the-subject`, which survived with zero invented `FitnessVector` fields).

**Buildable-now vs blocked:** the projection (producer side) is buildable and falsification-tested; **shipping it into studio is blocked** by design on (a) the studio per-candidate evaluator (axe/layout + ux-evidence-validator in the cycle) and (b) OQ-5 (soft-score weights). The adapter is **authored-and-parked**.

**Refine-necessity, in hindsight:** warranted but light — the value delivered was the *structure map* (claim_class → hard/soft → FitnessVector) and the *toy_game* confirming the honesty rule survives the projection. A full/standard preset would have wastefully re-derived the studio fitness mechanism.

## Recommended next routes (not executed)
1. **Parked** — un-park only when studio evaluator + OQ-5 land (see `stages/09-plan.md`). Until then, do nothing.
2. **sigil-development (minor)** — optionally add the `emit-studio-fitness` *mode stub* to ux-lessons SKILL.md marked `parked`, so the design is discoverable. Low value until consumed; operator's call.
3. **studio decision request** — add a `pattern` value to `FitnessSignalSource`, or confirm the `governance` fallback.

## Boundary / discipline
All artifacts under `arcanum/` (public), uncommitted. Parent dispatch: `2026-06-23-ux-lessons`. claim ≤ proof: this is a parked design, nothing built.
