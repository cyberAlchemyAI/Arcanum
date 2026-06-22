# Work-Pack — refine-improvement fixes

> `invoke plan` output (single-file, medium complexity). Companions:
> `IMPLEMENTATION-PLAN.md`, `IMPLEMENTATION-LAYERING.md`. Every task maps to a layer and an
> owner. Tags: `[obs]` observability/harness · `[refine]` refine sigil · `[dec]` recorded
> decision. Execution route: `task-session` per parent task (refine boundaries preserved).

## SWU manifest (shared)

| SWU id | Layer | Owner | Title | Parent task |
|---|---|---|---|---|
| SWU-RFX-C6 | L0 | [obs] harness | Validation requires a completed run | T1 |
| SWU-RFX-P1 | L1 | [obs] observer | Repoint observer to native surface | T2 |
| SWU-RFX-P2 | L1 | [obs] observer | Substantive reflection (no boilerplate) | T3 |
| SWU-RFX-C3 | L2 | [refine] | Hire-ability route predicate at handoff | T4 |
| SWU-RFX-P3 | L2 | [refine] | Missing-target prompt | T5 |
| SWU-RFX-C2 | L3 | [refine] | Lean cold-target path-to-first-value | T6 |
| SWU-RFX-C7 | L3 | [refine] | check-tension discipline at spawn gate | T7 |
| DEC-RFX-C4 | — | [dec] | Record "no new mode earned" | T8 |

One parent task per SWU. Each task below states write scope, acceptance evidence, and a
verification command/reviewable check.

---

## T1 — [obs] SWU-RFX-C6 · Validation requires a completed run  (L0, first)
- **Write scope:** the refine validation harness that emits `REFINE_LIVE_VALIDATION`
  (`development/run-validation-fixtures.sh` + the rule it applies); note the rule in
  `VALIDATION.md`. Do NOT touch `SKILL.md` contract semantics beyond referencing the rule.
- **Change:** `pass` iff `terminal_artifact_exists(preset) AND no_blocked_required_stage`;
  proposal-only stop → `flag` + missing-stage list; blocked required stage → `block`.
- **Acceptance evidence:** an all-blocked fixture run scores `flag`/`block`; a completed
  fixture run scores `pass`. The 05-24 all-blocked artifact no longer scores `pass`.
- **Verify:** run `development/run-validation-fixtures.sh` against both fixtures; assert the
  two scores differ as above.
- **Next route:** task-session (harness owner). Shares the "completed run" definition with T6.

## T2 — [obs] SWU-RFX-P1 · Repoint observer to native surface  (L1)
- **Write scope:** signal-observer emission config / `observed-invocation-loop` wiring under
  `.arcanum/observability/`. Not the refine sigil.
- **Change:** `target_artifact = arcana/refine/SKILL.md`; emit a signal on native
  skill/subagent refine invocation (not only the Codex command surface).
- **Acceptance evidence:** a native refine run appends a ledger line with `mode != command`
  and `target_artifact = arcana/refine/SKILL.md`.
- **Verify:** `grep` the newest refine line in
  `.arcanum/observability/signals/sigil-invocations.jsonl`; assert the two fields.
- **Depends on:** T1. **Next route:** task-session (observability owner).

## T3 — [obs] SWU-RFX-P2 · Substantive reflection (no boilerplate)  (L1)
- **Write scope:** the reflection emitter (signal-observer 0.1.0 reflection step).
- **Change:** at threshold, carry `workflow_gaps[].detail` into the report OR defer to a
  `workflow-reflect` pass; stop emitting the fixed two-line text.
- **Acceptance evidence:** a `reflect-now` report names a concrete target section instead of
  the boilerplate seen in the 11 prior refine reports.
- **Verify:** trigger one reflection; assert the report body contains a gap/target reference.
- **Depends on:** T1. **Next route:** task-session (observability owner).

## T4 — [refine] SWU-RFX-C3 · Hire-ability route predicate at handoff  (L2)
- **Write scope:** `RESULT.md` template + the final-synthesis stage spec in `SKILL.md`
  output-contract. Flag the ownership-boundary question (vs dispatch-spec input contract)
  before promotion.
- **Change:** a `RESULT.md` is hire-able iff `## Recommended Next Route` lists ≥1 owner unit
  (SWU/task id) with precondition/ordering + done-criterion + no unresolved blocker; gate it.
- **Acceptance evidence:** predicate passes `arcana/x-ray/.../20260529T124546Z-schema-readiness/RESULT.md`
  and fails the all-blocked `20260524T225844Z-sigil-new-low` run.
- **Verify:** apply the predicate to both `RESULT.md`s; assert pass vs fail.
- **Depends on:** T1, T2. **Residue:** ownership-boundary review (findings §5).
- **Next route:** task-session after ownership-boundary review.

## T5 — [refine] SWU-RFX-P3 · Missing-target prompt  (L2)
- **Write scope:** refine target-resolution / process step 1 + `simple-operator-sentence-policy`.
- **Change:** if target missing AND interactive → one-question prompt for the target; else keep
  the current `missing-refine-target` block.
- **Acceptance evidence:** an empty-intent interactive invocation asks for a target rather than
  returning a hard block.
- **Verify:** dry invoke with empty target; assert a clarifying question is emitted.
- **Next route:** task-session (refine maintainer).

## T6 — [refine] SWU-RFX-C2 · Lean cold-target path-to-first-value  (L3)
- **Write scope:** dispatch-spec gating reference in `SKILL.md` (`compact` preset cold path);
  preserve the full route-validation gate for richer presets.
- **Change:** under `compact`, a refined *seed* is reachable without a fully validated
  `REFINE-DISPATCH.json`; record the relaxation and where full validation re-enters.
- **Acceptance evidence:** a cold target yields a seed artifact even when dispatch validation
  would otherwise block (the 05-24 brittleness residue).
- **Verify:** run a cold-target `compact` refine fixture; assert a seed artifact exists.
- **Depends on:** T1 (shared "completed run" definition). **Next route:** task-session.

## T7 — [refine] SWU-RFX-C7 · check-tension discipline at spawn gate  (L3)
- **Write scope:** refine process step 11 (subagent spawn) + strategy-preview-and-permission.
- **Change:** before operator confirm of a sibling spawn, run the four-test tension check
  (axis / clone / spread / evidence) as *behavior* (not the ledger/dispatch_type form); return
  untensioned sibling sets to the strategist. Single-agent helper (P11) is exempt.
- **Acceptance evidence:** an untensioned sibling set is returned pre-confirm; a tensioned one
  passes to the human gate.
- **Verify:** feed a clone-pair sibling set; assert rejection before confirm.
- **Depends on:** finished-loop behavior (L0–L2). **Next route:** task-session.

## T8 — [dec] DEC-RFX-C4 · Record "no new mode earned"  (recorded decision)
- **Write scope:** a decision note in `SKILL.md` non-applicability / a dev DECISIONS note.
- **Change:** record that variation stays carried by preset × overlay × seed-needed decision;
  do not add `/refine` modes until a problem-class the existing axes cannot express is witnessed.
- **Acceptance evidence:** the decision is written with its cite (`SELF-REFINEMENT-2026-05-24.md:83`).
- **Verify:** reviewable check — the note exists and cites the evidence.
- **Next route:** none (decision recorded).

---

## Deferred backlog (future-work — NOT scheduled)
- **C8** maximal dispatch-algebra integration — owner: dispatch-spec. Referents empty today.
- **C9** early Distill anti-anchor gate — controls timing, not adversariality.
- **C10 / `reframe`** — Distill emits a solution-independent problem statement; late governed
  Design fork. Leading anchoring candidate; promote when a problem-class the existing axes
  cannot express is witnessed.

## Validation summary (every delivery slice has a check)
T1 fixture pair · T2 ledger-line assert · T3 reflection target-section assert · T4 predicate
discrimination · T5 prompt test · T6 cold-seed reachability · T7 untensioned-sibling rejection
· T8 reviewable note check.
