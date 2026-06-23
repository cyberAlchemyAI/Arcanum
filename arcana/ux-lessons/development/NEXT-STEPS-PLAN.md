# ux-lessons — Next-Steps Plan (invoke plan)

- **Observed capability:** invoke · **Mode:** plan · **Target artifact:** `ux-lessons` (arcana sigil, seed) · **Owner cycle:** sigil-development
- **Authored:** 2026-06-23 · **Complexity:** medium · **Work-pack:** single-file (below)
- **Source evidence:** the 2026-06-23 refine run (`refinement-runs/2026-06-23-ux-lessons/RESULT.md`), the seed package (`../SKILL.md`), and the experiment harness (`experiment-harness/VALIDATION-REPORT.md`).

---

## 1. Refine-necessity evaluation (the explicit ask)

**Verdict: a second `/refine` run is NOT necessary for any ready or closeout step.** The capability is already designed and falsification-tested; the remaining work is execution, evidence completion, and governance — none of it is a vague target needing discovery/critique/design. Refine is warranted for **exactly one deferred item**, and only when it is prioritized.

| # | Workstream | Already designed? | Refine needed? | Why / Route |
| - | ---------- | ----------------- | -------------- | ----------- |
| W1 | Register the refine dispatch (2 subagents) | yes (mechanical) | **no** | `register-dispatch` appends rows; no design choice. |
| W2 | Submodule-first commit of ux-lessons + run | yes (governed) | **no** | `SUBMODULE-DISCIPLINE.md` dictates the steps. |
| W3 | Evidence durability (copy `.xray-iter` shots into pkg) | yes | **no** | File move; trivial. |
| W4 | Capture a 2nd real iteration session | n/a — it IS the sigil running | **no** | Use `ux-lessons --mode capture` when a real session happens. |
| W5 | Live validator ingestion (fixture-plan→calibrate) | yes (claim map→`spec` exists) | **no** | Execution via `ux-evidence-validator`; design already in example 02. |
| W6 | Live studio annotation apply | yes (CommentEvent→MutationTask shape) | **no** | Execution via `ui-prototyping-studio`. |
| W7 | Promote ux-lessons (seed→calibrated) | n/a — gated on evidence | **no** | `sigil-development --reflect` after W4+W5+W6 evidence. |
| W8 | **Studio variant/fitness intake** | **NO — genuinely undesigned** | **YES (conditional)** | Real design gap (what fitness evaluator? how does variant intake map?), blocked on studio **OQ-5**. Refine it *when prioritized*, then sigil-development. |

**Bottom line:** route everything through plan → task-session now; reserve `/refine` solely for W8 if/when it is taken off the deferred shelf.

---

## 2. Implementation layering (value/cost boundaries)

| Layer | Slice | Promotion evidence to advance |
| ----- | ----- | ----------------------------- |
| **L0 — Durability & governance floor** | W1 register-dispatch · W3 evidence durability · W2 submodule-first commit | dispatch rows present; screenshots in-package; `make bump-check` clean; arcanum pushed before parent gitlink bump |
| **L1 — Evidence completion** | W4 second session capture · W5 validator fixtures · W6 studio apply | ≥2 sessions captured; validator calibrated on good/bad/false-positive fixtures; studio annotation applied on a real session |
| **L2 — Promotion** | W7 reflect + promote ux-lessons | promotion-gate criteria in `../SKILL.md` met; harness re-run pass; cross-session promotion demonstrated |
| **L3 — Deferred design** | W8 studio variant/fitness intake | studio OQ-5 resolved + fitness evaluator exists → **refine W8** → sigil-development |

Layer rule: **L1 may not start W7 until L0 is durable** (don't promote uncommitted work); **L2 requires L1 evidence, not preference**; **L3 stays parked** behind named external unblocks.

---

## 3. Work-pack (single-file; SWUs)

| Task | Layer | SWU | Write scope | Acceptance evidence | Verify | Owner route |
| ---- | ----- | --- | ----------- | ------------------- | ------ | ----------- |
| T1 register dispatch | L0 | append dispatch + close rows for the 2 subagents | `telemetry/agents/subagents-dispatch.yaml` | 2 rows with angle + anti_bias axis | file diff shows valid rows | `register-dispatch` |
| T2 evidence durability | L0 | copy cited screenshots into pkg; repoint refs | `arcana/ux-lessons/examples/`, `.../experiment-harness/` (+ an `assets/`) | no example cites untracked `.xray-iter/` | grep finds no `.xray-iter` refs | task-session |
| T3 submodule commit | L0 | commit+push arcanum; bump parent gitlink | `arcanum/**`, parent gitlink | arcanum pushed; `make bump-check` clean | `make doctor` + `make bump-check` | task-session |
| T4 capture 2nd session | L1 | run `capture` on a real future session | `arcana/ux-lessons/examples/` | a 2nd `lesson` set, honest signal | schema conformance | `ux-lessons --mode capture` |
| T5 validator fixtures | L1 | author good/bad/false-positive fixtures for `detail-beside-the-subject` | `ux-evidence-validator` fixtures dir | fixture set + calibrate report | `ux-evidence-validator --mode fixture-plan`→`calibrate` | `ux-evidence-validator` |
| T6 studio apply | L1 | apply the annotation intent on a studio session | studio session data (isolated) | applied MutationTask + manifest entry | `studio` CLI run | `ui-prototyping-studio` |
| T7 reflect + promote | L2 | re-run harness; advance status | `arcana/ux-lessons/**` | harness pass; gate met | harness VALIDATION-REPORT pass | `sigil-development --reflect` |
| T8 (deferred) variant intake | L3 | refine then design | new run folder | — | — | `refine` → `sigil-development` |

**Ready now:** T1, T2, T3 (L0). **T4–T6** need a real second session / live consumer runs. **T7** gated on L1. **T8** parked.

---

## 4. Validation strategy per slice
- L0: `make doctor`, `make bump-check`, grep for dangling evidence refs, telemetry-row schema check.
- L1: schema conformance (capture), validator calibrate report (good/bad/false-positive separation), studio append-only manifest entry.
- L2: experiment-harness re-run must move from `flag`→`pass`; promotion-gate checklist in SKILL.md fully checked.
- L3: n/a until unblocked.

## 5. Distill validation
- **Verdict: pass.** Smallest coherent unit = the L0 closeout trio (T1–T3), independently executable and recomposing into the lifecycle. Large enough to preserve meaning (durable, governed, registered); small enough to execute now. No hidden gaps: L1/L2 dependencies are explicit; L3 is honestly parked with named external unblocks. No overbuilt task labels (each task has write scope + verify).

## 6. Dispatch technique trace
- `sequence` → ordered layers L0→L3 (activation: multi-step plan; affects work-pack ordering).
- `owner_boundary_check` → each task names its owner capability (validator/studio/sigil-development/refine), preventing ux-lessons from absorbing consumer execution (gate: §3 owner-route column).
- `authority_split_gate` → L2 promotion owned by sigil-development, not this plan (evidence expectation: harness pass).
- `residue_ledger` → W8 + live-ingestion parked with named unblocks (gap route: §1 + L3).
- `concrete_path_evidence` → every task has write scope + verify command.
- **Skipped:** `scu_swu_reduction` heavy decomposition — rejected; tasks already SWU-sized. Full dispatch JSON — not needed; no new cross-capability route artifact beyond the existing validated REFINE-DISPATCH.
- No unused citations.

## 7. Next route
**task-session** for the ready L0 slice (T1–T3). L1 (T4–T6) when a real second session and live consumer runs are available. L2 via **sigil-development --reflect**. L3 (**refine** then sigil-development) only when studio OQ-5 + a fitness evaluator unblock it.
