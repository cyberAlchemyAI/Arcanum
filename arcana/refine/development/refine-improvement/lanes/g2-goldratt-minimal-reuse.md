# Lane G2 — Goldratt minimal-reuse: what /refine should *borrow*, not *import*

**Lens:** Theory-of-Constraints / adversarial-cost. Every mechanism imported from the
subagents-strategy machinery is judged by one test: does relieving refine's binding
constraint pay for the coupling and maintenance it adds — or does it just add another
unused technique name to the route?

That failure mode is already named by refine itself: a successful run must
"select technique overlays based on target evidence rather than **decorating the route
with unused technique names**" (`refine/SKILL.md` quality-bar, line 314; restated at
line 322: "cite dispatch techniques only when they are expressed by steps, gates,
handoffs, or validation notes"). So refine has *already declared* that importing
vocabulary it does not exercise is a defect. The adversarial-cost lens just extends that
rule from techniques to whole mechanisms.

## The bottleneck constraint

Refine is not throughput-bound (its ten stages are fixed and cheap to schedule) and not
quality-bound at the artifact level (each stage capability owns its own validation). Its
binding constraint sits at **one point**: the moment refine decides to *spawn
role-bound sibling subagents* and present that decision to the operator.

That is the only place where refine's output can be *systematically wrong rather than
merely thin*. Everywhere else a weak stage produces a weak-but-honest artifact. But when
`subagent_strategy.status` is `recommended`/`required` (`refine/SKILL.md`
strategy-preview, lines 88–97; process step 11, line 300), refine spawns n≥2 agents
whose returns it then synthesizes — and if those agents share a hidden bias, refine
synthesizes a **confidently false** seed/design/plan and hands it forward as the run
deliverable. A correlated-bias sibling set is the one input that defeats refine's own
downstream interrogation, because the critique stage inherits the same blind spot.

**The constraint to relieve: refine's multi-agent stages can emit a confident synthesis
over agents that were never verified to be genuinely tensioned.** Refine already requires
operator *permission* to spawn (lines 93–97), but permission is a willingness gate, not a
bias gate — the operator confirms *that* subagents run, not *that they disagree by
design*. Relieving this constraint improves refine more than any other change because it
is the only defect that is silent.

## Mechanism-by-mechanism: borrow as discipline vs import as dependency

| Mechanism | Subagents-strategy role | Pays for itself in refine? | Verdict |
|---|---|---|---|
| **check-tension** | Two independent agents run validator Tests 1–4 before the human confirm; only "both PASS" advances (`check-tension/SKILL.md` lines 6–58) | **Yes — directly relieves the bottleneck.** Refine's only systematically-wrong output comes from untensioned siblings; this is the exact gate. | **BORROW as discipline** |
| **anti-bias vectors** | Design principle behind P5 pairwise tension (router line 29) | Yes, but only as the *content* of the discipline above — refine needs the four-test rubric, not a second skill dependency. | **BORROW (subsumed by check-tension)** |
| **dispatch_types** | Router routes by `research \| review \| experiment` (LIVE) to type skills (router lines 43–50) | **No.** Refine's stages are already typed by capability (`invoke`, `interrogation`, `distill`); a second type taxonomy adds a parallel routing surface with no new decision. | **IMPORT-only-if-already-spawning** |
| **ledger / register-dispatch** | Append-only telemetry, two rows per dispatch (`register-dispatch/SKILL.md` lines 8–13) | **Partly.** Refine already materializes its own run manifest + evidence-index (`refine/SKILL.md` lines 169–191). A second append-only ledger duplicates that bookkeeping. | **IMPORT only when refine actually fans out** |
| **robot_talks** | Group synthesizes vs concats; P7/P14 binding (router lines 30, 37) | **No.** Refine owns its *own* final synthesis stage (`refine-final`, line 50; ownership-boundary line 255). Importing robot_talks would put a second synthesis owner inside a loop that already has one. | **DO NOT IMPORT** |

## Why most of it is discipline, not dependency

The adversarial cost of *importing* (taking a dependency) is threefold: (1) refine must
track the imported skill's version and re-validate when it changes; (2) refine's route
gains fields/enums it may not exercise — the exact "decoration" its own quality-bar
forbids; (3) two owners now touch the same concern (e.g. synthesis: refine-final *and*
robot_talks), violating the single-owner boundary refine already maintains
(ownership-boundary, lines 253–264).

The adversarial cost of *borrowing as discipline* is near-zero: refine adopts the
**behavior** (verify tension before synthesizing over siblings) without inheriting the
**form** (a registered dispatch row, a dispatch_type, a robot_talks flag). The
subagents-strategy machinery is, on this lens, a *worked example of how to do
multi-agent work safely* — and refine should copy the lesson, not link the library.

Concretely:

- **The one import that pays:** a check-tension-shaped gate, but **scoped to refine's
  own spawn point** (process step 11). Refine already stops for operator permission
  there; add a tension check *before* that stop, so the operator only ever confirms a
  sibling set that an independent double-check found genuinely tensioned — mirroring the
  router's "the human Confirm only ever sees a sheet that passed an independent
  double-check" (`check-tension/SKILL.md` line 58). This is one gate at one place, not a
  new dependency graph.

- **Everything else stays discipline.** Refine cites anti-bias *reasoning* in its seed
  proposal's subagent section; it does **not** grow a `dispatch_type`, a second ledger,
  or a `robot_talks` field. If a refine run ever genuinely fans out beyond its own loop
  (the helper-vs-dispatch boundary, router P11, line 14 — itself "provisional"), *that*
  is the trigger to register in the real ledger — not refine's default path.

## Bottom line

Refine has exactly one silent-failure constraint: synthesizing over un-verified-tensioned
siblings. Relieve it by **borrowing check-tension's discipline at refine's existing spawn
gate** — the four-test verification of pairwise tension before the operator confirm.
Borrow anti-bias as the rubric content of that gate. **Import** the ledger and
dispatch_type only on the rare path where refine truly fans out beyond its own loop.
**Do not import** robot_talks at all — refine already owns its synthesis. The rest of the
machinery is a lesson to copy, not a library to link; importing it would be precisely the
"unused technique name" decoration refine's own quality-bar already prohibits.
