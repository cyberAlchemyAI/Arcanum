# Implementation Plan — refine-improvement fixes

> `invoke plan` output. Complexity: **medium** (multi-owner, 7 build tasks + 1 recorded
> decision, contained blast radius). Per-layer slices L0–L3 below. Companion:
> `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`.

## Objective

Fix the accept-tier issues surfaced by the refine-improvement research dispatch and the
`/refine` workflow-reflect, in trust+dependency order: honest measurement → observe the
native surface → handoff fitness → cold-path + spawn-gate hardening. Defer all anchoring /
dispatch-algebra work to future-work.

## Native capability handles & receipts (no command-surface gating)

This plan names **native** execution surfaces only (per the refine stage-receipt-contract:
deprecated Codex command files are not success gates):
- C6/P1/P2 receipts: the validation harness output (`REFINE_LIVE_VALIDATION`) and a fresh
  native signal line in `.arcanum/observability/signals/sigil-invocations.jsonl`.
- C3/P3/C2/C7 receipts: refine `SKILL.md` contract text + a fixture refine run's `RESULT.md`
  / seed artifact + the spawn-gate tension check transcript.

## Per-layer planning slices

### L0 slice — C6 measurement gate
- Inputs: current validator emitting `REFINE_LIVE_VALIDATION`; the "completed run" definition
  (terminal artifact for the preset + no blocked required stage).
- Rules/pseudocode: `pass` iff `terminal_artifact_exists(preset) AND no_blocked_required_stage`;
  else `flag` (proposal-only / non-blocking gaps) or `block` (blocked required stage), and
  attach the missing-stage evidence.
- Edge cases: proposal-only stop (no run) → `flag` with missing-stage list; `flag=1` non-blocking
  (e.g. schema-readiness) still `pass` if no *blocked* required stage.
- Failure modes: definition drift between C6 (gate) and C1 (path-fix) — shared definition,
  single owner section (residue, findings §5).
- Validation: two fixtures (all-blocked, completed) produce `block`/`pass` respectively.

### L1 slice — P1 repoint + P2 substantive reflection
- Inputs: signal-observer emission config; reflection emitter.
- Rules: set `target_artifact = arcana/refine/SKILL.md`; emit on native skill/subagent runs;
  reflection at threshold carries `workflow_gaps[].detail` or defers to `workflow-reflect`.
- Edge cases: legacy `mode: command` signals still allowed but tagged legacy-surface.
- Validation: native refine run → ledger line `mode != command`, `target_artifact` native;
  a `reflect-now` produces a report naming a target section.

### L2 slice — C3 predicate + P3 missing-target
- Inputs: `RESULT.md` template + final-synthesis stage; seed-needed decision branch.
- Rules (C3): a `RESULT.md` is hire-able iff `## Recommended Next Route` lists ≥1 owner unit
  (SWU/task id) with precondition/ordering + done-criterion + no unresolved blocker.
- Rules (P3): if target missing AND interactive → one-question prompt for target; else `block`
  with the existing `missing-refine-target` gap.
- Edge cases: route names a *proposable* (not-yet-existing) unit → allowed if it carries the
  three fields. Non-interactive missing target → keep current block.
- Failure modes: C3 may overlap dispatch-spec input-contract ownership → ownership-boundary
  review before promotion (residue, findings §5).
- Validation: predicate passes `schema-readiness/RESULT.md`, fails the all-blocked 05-24 run.

### L3 slice — C2/C1 lean cold path + C7 spawn-gate tension
- Inputs: dispatch-spec validation gate; the subagent spawn point (process step 11).
- Rules (C2/C1): under `compact`, a refined *seed* is reachable without a fully validated
  `REFINE-DISPATCH.json` (defer full route validation to later stages); record the relaxation.
- Rules (C7): before operator confirm of a sibling spawn, run the four-test tension check
  (axis / clone / spread / evidence) as *behavior*; return untensioned sets to the strategist.
- Edge cases: single-agent helper (P11) is not a dispatch → no tension gate.
- Validation: cold target yields a seed despite a would-block dispatch; untensioned siblings
  are rejected pre-confirm.

## Validation strategy (per delivery slice)
- L0: fixture pair (all-blocked / completed) → `block` / `pass`.
- L1: native-run ledger line assertion + reflection-report target-section assertion.
- L2: predicate discrimination test (passing vs blocked `RESULT.md`); missing-target prompt test.
- L3: cold-target seed-reachability test; untensioned-sibling rejection test.

## Sequencing & gates
L0 → L1 → L2 → L3, each promoted only on its layer's evidence (see layering). C4 recorded at
L0 time. Deferred items (C8/C9/C10) are NOT scheduled here.

## Ownership boundary (preserved)
- Harness owner: C6, and (jointly with refine maintainer) the shared "completed run" definition.
- Observability/signal-observer: P1, P2.
- Refine-sigil maintainer: C3 (pending ownership-boundary review vs dispatch-spec), P3, C2/C1, C7.
- Invoke authored these artifacts; it does NOT own the refine/observer lifecycles. Next route
  per task below.
