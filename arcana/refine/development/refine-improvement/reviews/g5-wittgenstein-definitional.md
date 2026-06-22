# G5 Skeptic Review — Definitional Soundness

Reviewer: SKEPTIC (attack-vector = DEFINITIONAL-SOUNDNESS)
Zig-zag partner: synthesizer (findings.md)
Target: `arcanum/arcana/refine/development/refine-improvement/findings.md` against `arcanum/arcana/refine/SKILL.md`

Test applied to every proposed mode/mechanism: does it COLLAPSE into an existing preset (`compact/standard/full/deep`) or overlay (`route_menu_for_ambiguity`, `dialectic_for_tension`, `tournament_for_alternatives`, `xray_for_hidden_structure`, `toy_game_for_low_cost_falsification`, `memory_residue_for_context_recovery`, `protected_context_for_external_or_sensitive_evidence`)? Kill re-skins; survivors must carry a distinguishing definition. Wittgenstein-bias guard active: a genuinely new mode is NOT killed merely because it resembles an overlay name.

## A. Proposed modes/mechanisms — collapse test

### C5 — five external modes (diverge / reframe / strengthen / evaluate / converge)

Collapse verdict, mode-by-mode:

- **converge** = COLLAPSE. This is the entire canonical loop's terminal motion (Distill → Plan → synthesis). No distinguishing function over `standard`. Pure re-skin.
- **diverge** = COLLAPSE into `tournament_for_alternatives` + `route_menu_for_ambiguity`. "Generate multiple candidates" is exactly `tournament` (several plausible designs compared via `pareto_gate`) and `one_or_more_option_set`. No residual.
- **strengthen** = COLLAPSE into `toy_game_for_low_cost_falsification` (controlled failure test that hardens a unit) plus the existing Distill Repair stage (stage 8). "Make the surviving unit more robust" is already an owned stage, not a mode.
- **evaluate** = COLLAPSE into the two Interrogation stages (3/7/10) and `tournament`'s `pareto_gate`. Refine already grades units; "evaluate" names that, adds nothing.
- **reframe** = SURVIVES the collapse test, narrowly. None of the existing overlays *change the problem statement*. `dialectic_for_tension` argues competing principles within a fixed frame; `route_menu` chooses among routes for a fixed target; `tournament` compares solutions to a fixed problem. Re-stating the problem-unit itself (G3-Hewitt's "Distill emits a solution-independent problem statement") is not expressed by any current overlay. **This is the one non-vacuous mechanism in C5.**

findings.md already classifies C5 as `analogy-only`/defer, which is the correct disposition. **CHANGE-ASK 1:** the synthesis lumps all five as "unwitnessed five-mode taxonomy." That under-credits `reframe` and over-credits the other four. Split C5: kill converge/diverge/strengthen/evaluate explicitly as re-skins of {loop, tournament, toy_game, interrogation}; carry forward ONLY `reframe`, and merge it into C10 (it is literally G3-Hewitt's mechanism) rather than leaving it floating in C5. A five-name taxonomy where four names are existing machinery is a definitional liability, not merely "unwitnessed."

### "Add a refinement engine" (rejected fork, `SELF-REFINEMENT-2026-05-24.md:83`)

COLLAPSE / already-killed. Correctly cited as rejected-for-drift. No action; it is a non-proposal.

### C8 — maximal dispatch-algebra integration (route stages to LIVE dispatch_types, register, robot_talks)

Not a refine *mode* — it is an external-machinery import. Collapse test n/a in the preset/overlay sense, BUT a definitional problem exists: routing stages 3/4/7/10 to `dispatch_type` is only meaningful if those stages already produce tensioned sibling agents. They do not (G2-Goldratt). So C8's terms are well-defined but their *referents are empty* under current behavior. `future-work` is the right verdict. No change-ask beyond noting referent-emptiness.

### C7 — borrow check-tension discipline at spawn gate

Definitionally clean. "Borrow behavior not form" is sharp: it names the verification predicate (siblings genuinely tensioned before synthesis) without importing the ledger/dispatch_type vocabulary. Survives. No re-skin: refine has NO existing anti-bias gate at its spawn point. Keep as `borrow-carefully`.

## B. Winning recommendations — undefined-notion smuggling check

### C1 — "fix delivery so runs finish" / "reach value"

**CHANGE-ASK 2: "value" is undefined and load-bearing.** C1 is the #1 recommendation and rests on the phrase "runs block before reaching value" (findings.md:104, 117). "Value" is never defined. Two incompatible readings are both live in the text: (a) value = a materialized non-blocked `RESULT.md` (the C6 measurement reading); (b) value = a *useful refined seed/plan a human would act on* (the C3 hire-ability reading). These are not the same: a run can finish with a non-blocked RESULT.md that is useless. If "value" silently slides between (a) and (b), C1 and C3 stop being distinct recommendations and the ordering in §4 becomes incoherent. **Demand:** define "reach value" operationally as "the loop produces the preset's declared terminal artifact (seed | design | non-executed plan) with no blocked required stage" — i.e. the *completion* reading (a) — and explicitly hand the *usefulness* reading (b) to C3. This keeps C1=completion, C3=fitness as separable.

### C3 — "hire-ability gate" / "would the next owner accept this?"

**CHANGE-ASK 3: "hire-ability" is the single most under-defined term and it is a promotion-candidate (buildable NOW).** A gate cannot be built against an undefined predicate. findings.md:165-166 even flags this as residue ("Is hire-ability measurable *inside* refine or only downstream when Task Session accepts/rejects?") — but then still lists C3 as a promotion-candidate to build first-wave. That is the contradiction: you cannot promote a gate whose acceptance criterion is admittedly unknown. Either C3 is future-work (resolve the residue first) OR C3 must ship with a *concrete, refine-internal, non-circular* acceptance predicate. "Would Task Session accept this?" is circular/downstream — it defines the gate by the very owner the gate is supposed to pre-clear. **Demand:** C3 must name a self-contained decidability predicate refine can evaluate without invoking the downstream owner. Candidate (the synthesizer should accept or counter): the plan passes iff each step has (i) a named owner capability, (ii) a stated done-criterion, (iii) a validation surface, and (iv) no unresolved blocker — i.e. reuse the `dispatch-spec`/`task-session` *input contract* as the fitness predicate. If no such internal predicate can be written, C3 drops to future-work and the residue owner is correct that only downstream accept/reject is real.

### C6 — "gate-accounting" / "health on empty runs"

Definitionally the soundest of the three. "Gate-accounting bug" is well-anchored: `REFINE_LIVE_VALIDATION=pass` co-existing with zero end-to-end refinements (findings.md:24) is a concrete, witnessed mismeasurement. The fix-predicate ("`REFINE_LIVE_VALIDATION` requires a non-blocked `RESULT.md`") is operational and checkable. Survives clean.

**CHANGE-ASK 4: ordering coherence between C6 and C1.** §4 puts C6 first ("cheapest") then C1. But C6 as defined ("require a non-blocked RESULT.md") presupposes the C1 completion-notion of "non-blocked / value." So C6 cannot be specified before C1's "reach value" is defined (CHANGE-ASK 2). The dependency is definitional, not just sequencing: C6 *is* the measurement instrument for C1's completion predicate. Recommend stating that C6 and C1 share one definition of "completed run," authored once, with C6 = the gate that enforces it and C1 = the path change that makes it satisfiable. As written they read as two independent items resting on the same undefined "value."

## C. Summary of change-asks

1. Split C5: kill converge/diverge/strengthen/evaluate as re-skins of {canonical loop, tournament, toy_game, interrogation}; carry only `reframe` and fold it into C10 (it is G3-Hewitt's mechanism).
2. Define "reach value" (C1) operationally as completion of the preset's terminal artifact with no blocked required stage; hand usefulness to C3.
3. Give C3 a concrete refine-internal acceptance predicate (non-circular, not "Task Session would accept") or demote it to future-work; reuse the dispatch-spec/task-session input contract as the candidate predicate.
4. State the C6/C1 shared definition of "completed run" explicitly; C6 enforces it, C1 makes it satisfiable — they are not independent.

Wittgenstein-bias check passed: I did NOT kill `reframe` despite its surface resemblance to dialectic/route_menu, because it operates on the problem-unit (not principles within a frame, not routes to a fixed target). C7 also survived as a genuinely-new gate. Everything killed (converge/diverge/strengthen/evaluate/refinement-engine) has a named existing owner that performs the identical function.
