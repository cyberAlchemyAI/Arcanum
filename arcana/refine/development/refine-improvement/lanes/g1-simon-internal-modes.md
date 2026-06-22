# g1-simon — Do problem-classes need different /refine MODES?

Lane question: derive any /refine *modes* bottom-up from refine's own canonical
ten-stage loop and observed internal evidence. Admit a mode only when a real,
observed failure or usage gap earns it. Prefer parameterizing the single loop.

## Method (read-only)

I read the contract surface (`SKILL.md`, `REFINEMENT-LOOP.md`), the existing
parameterization (presets + overlays), and the internal development evidence
(`WORK-PACK.md`, `VALIDATION.md`, `SELF-REFINEMENT-2026-05-24.md`,
`TASK-MATRIX.md`, `LIVE-EXAMPLE-SEEDS.md`, the `development/runs/` harness records).
A "mode" here means a *named variant that changes which stages run or the loop's
control flow* — distinct from a preset (budget tuning) or an overlay (per-stage
config). Below, each candidate mode is admitted only on cited observed evidence.

## What the system already parameterizes (so a mode would have to beat this)

The single loop is fixed at ten stages and is *not* allowed to drop stages:
"Presets tune budget, depth, and configuration; they do not remove stages"
(`SKILL.md` line 39; `REFINEMENT-LOOP.md` line 57). Variation is already carried
by two orthogonal axes:

- **Presets** `compact|standard|full|deep` tune budget only
  (`SKILL.md` lines 278-287; `REFINEMENT-LOOP.md` lines 117-124).
- **Technique overlays** (`route_menu_for_ambiguity`, `dialectic_for_tension`,
  `tournament_for_alternatives`, `xray_for_hidden_structure`,
  `toy_game_for_low_cost_falsification`, `memory_residue_for_context_recovery`,
  `protected_context_for_external_or_sensitive_evidence`) change stage config,
  gates, and validation expectations but "do not remove required stages"
  (`SKILL.md` lines 101-126; `REFINEMENT-LOOP.md` lines 85-114).

This is the key bottom-up finding: the loop authors *already chose* to map
problem-class variation onto overlays, not modes. Any proposed mode must show an
observed failure that overlay-or-preset parameterization cannot reach.

## Problem-classes actually observed, and where they land

The internal evidence names exactly these distinct problem-classes — and each one
is already handled by a *trigger into the single loop*, not a mode:

| Observed problem-class (evidence) | Already handled by |
| --- | --- |
| New-sigil-seed from a vague idea (`TASK-MATRIX.md` refine-xray-new; `LIVE-EXAMPLE-SEEDS.md` Example 1) | compact/standard preset + baseline sequence |
| Existing work-pack / SWU as source, skip seed creation (`TASK-MATRIX.md` refine-existing-target-medium; `SELF-REFINEMENT-2026-05-24.md` "Seed needed: no" branch, lines 44-48) | seed-needed decision (process step 1, `SKILL.md` line 290), not a mode |
| Blocked: missing dispatch/handoff/receipt (`TASK-MATRIX.md` refine-blocked-medium; `VALIDATION.md` line 19 "Status: block" as valid evidence) | block path is intrinsic to every stage, not a mode |
| Broad architecture/package refinement (`TASK-MATRIX.md` refine-observability-complex; `LIVE-EXAMPLE-SEEDS.md` Example 2) | full/deep preset + `xray_for_hidden_structure` overlay |
| Next-route recommendation after synthesis (`TASK-MATRIX.md` refine-next-route-complex) | post-synthesis step (process step 16), not a mode |

Every observed class is reachable by (preset × overlay × seed-needed decision).
No observed class required a control-flow variant that the existing axes cannot
express. This is direct evidence *against* mode proliferation.

## Candidate modes, judged on earned-or-not

1. **"discovery vs design vs plan" output modes** — REJECT as proliferation.
   The ten-stage loop already *contains* Define, Design, and Plan as ordered
   stages (`SKILL.md` lines 44-51). The user's desired output (seed / design /
   non-executed plan) is named in the description line 3 and selected by the seed
   proposal's "done criteria" field (process step 3, `SKILL.md` line 292), not by
   forking the loop. Splitting these into modes would re-introduce the exact
   drift the design rejected in `SELF-REFINEMENT-2026-05-24.md` (Distill rejected
   "Add a new refinement engine ... Duplicates REFINEMENT-LOOP.md and increases
   drift risk", lines 83). No observed failure earns it.

2. **"existing-work-pack preflight" mode** — REJECT; it is a *decision*, not a mode.
   The self-refinement run found a real gap (SELF-REFINE-001, medium: examples
   only covered seed + blocked, not the existing-work-pack branch,
   `SELF-REFINEMENT-2026-05-24.md` lines 56-57). But the fix it chose was an
   *example + the "Seed needed: no" branch* inside the same loop (lines 44-48,
   90-100), explicitly keeping the "seed/preflight controller" as the single
   selected unit (Distill, lines 76-85). The gap was a documentation gap, not a
   missing mode.

3. **"blocked / preflight-only" mode** — REJECT; block is a universal verdict.
   Observed `Status: block` runs (`VALIDATION.md` line 19) are explicitly "valid
   blocked evidence, not promotion evidence" produced by the *same* loop hitting
   a missing-field gate. The harness already distinguishes a proposal from
   manifest-backed loop evidence (`VALIDATION.md` line 15) without a separate
   mode. Making block a mode would let a run *choose* to stop early — the opposite
   of the contract's intent.

4. **"broad architecture / repository-area" mode** — REJECT; covered by preset+overlay.
   The one complex live target (observability package, `LIVE-EXAMPLE-SEEDS.md`
   Example 2) expects "full architecture/design refinement seed" reachable by
   `full`/`deep` preset plus the hidden-structure overlay. No stage needed to be
   added or removed.

5. **A genuine *interaction* mode: proposal-only vs run-through.** — EARNED, but it
   already exists as the permission gate, not a new mode. The single most
   load-bearing observed failure is `REFINE_LIVE_VALIDATION=flag`: "sigil-new-low
   output does not prove the refinement loop ... executed through required stage
   evidence" — the run "can only produce a proposal"
   (`development/runs/20260524T225248Z.md`; `LIVE-EXAMPLE-SEEDS.md` Example 1
   "flag or block the run if it can only produce a proposal"). This is a real,
   recurring gap (proposal produced, loop not executed). But the contract already
   has the two states as a *gate*: the `Refine Run Strategy Proposal` then a
   human permission gate before runtime-backed stages (`SKILL.md` lines 77-99,
   222-251). The fix is hardening that gate's *completion accounting*
   (flag/block when only a proposal exists), not adding a mode. Parameterize, do
   not proliferate.

## Verdict

**No new MODE is earned.** Every observed problem-class and every observed
failure is reachable through the existing three parameterization axes — presets
(budget), technique overlays (per-stage config/gates), and the seed-needed +
permission decisions inside the single canonical loop. The internal evidence
actively argues against modes: the only design alternative that *was* a mode-like
fork ("Add a new refinement engine") was explicitly rejected for drift risk
(`SELF-REFINEMENT-2026-05-24.md` line 83), and the self-refinement gaps were
closed with examples and a decision branch, not a fork.

The one real, recurring failure (proposal emitted but loop not executed) is a
**gate-accounting bug in the single loop**, not a missing mode. Recommended
improvement, framed as parameterization not modes:

- Harden the proposal→run completion gate: a materialized run that stops at the
  proposal must record `flag`/`block` with the missing stage evidence (already
  the harness's intent, `runs/20260524T225248Z.md`), so "proposal-only" can never
  silently pass as a completed refinement.

Modes considered and rejected as proliferation: output-mode (discovery/design/
plan), existing-work-pack mode, blocked/preflight-only mode, broad-architecture
mode. Each collapses into a preset, overlay, or decision the loop already owns.
