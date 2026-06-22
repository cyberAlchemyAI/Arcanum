# g2 — Spivak lane: maximal principled reuse of the subagents-strategy machinery in `/refine`

**Lens:** FORMAL / integration. Treat `/refine` as a *consumer* of the dispatch
algebra, not a parallel orchestrator. Each subagents-strategy mechanism is a
morphism that already exists; refine should compose them, not re-invent them.

**Problem (lane-independent):** `/refine` runs a single deterministic track —
the canonical ten stages, each one owner, each one critic — so the *design* it
elaborates is never confronted by a structurally opposed design. Its critique
stages (Interrogation, Distill repair) attack *the artifact's quality*, never
*the artifact's framing*. That is the anchoring failure TWO-LANE-DISCIPLINE.md
names: "shipping the first framing because nobody was assigned to disagree with
it" (`TWO-LANE-DISCIPLINE.md`, Lane A rationale). Refine's own
`anti-patterns` warns against freeform prose replacing stages, but says nothing
about framing monoculture (`arcanum/arcana/refine/SKILL.md` §anti-patterns).

The subagents-strategy stack is exactly the missing apparatus: it manufactures
*structurally opposed* agents and proves the opposition before a human commits.
Below, each mechanism is mapped onto one refine stage or overlay.

## The mapping (mechanism → refine stage/overlay)

| subagents-strategy mechanism | refine stage / overlay it owns | how |
|---|---|---|
| `dispatch_type: research` | **Stage 4, Research Decision** (`bounded-research` / `research-if-gap-appears`) | Refine already has a research decision; today it is unregistered. Make `bounded-research` and any `if-gap` trigger emit a real `research` dispatch with a `working_folder` (research requires one — `register-dispatch` top-level table, `working_folder`). This is a pure widening: the stage's "named external-context gap" (`SKILL.md` §research-policy) becomes the dispatch `goal`. |
| `dispatch_type: review` | **Stages 3, 7, 10** (Interrogation `refine-review` / `refine-design-review` / `refine-final`) | Each interrogation is a single-agent critique today. Re-cast as a `review` dispatch — inline by default, so no `working_folder` cost (`register-dispatch`, `working_folder` "Optional for `review`"). Review judgment (attack lenses, severity taxonomy) is owned by the review type skill; refine stops defining critique form and routes to it. |
| `dispatch_type: experiment` | **`toy_game_for_low_cost_falsification` overlay** (already in `SKILL.md` §technique-overlay-policy) | The overlay says a selected abstraction may need "a controlled failure test before planning." That is precisely an `experiment` dispatch: a criterion frozen *before* the probe, verdict SURVIVED/FALSIFIED/INVALID (`domainspec-subagents-strategy` routing table; criterion is a `working_folder` artifact, never a column). The overlay fires between Distill (5) and Invoke Design (6). |
| **anti-bias vector composition** | **the seed/dispatch-design step** (process steps 4–5) where the *second lane* is authored | This is the load-bearing reuse. To break single-track, refine must spawn an n≥2 **subject group** whose two agents hold *opposed framings* of the same underlying problem. Anti-bias composition is the design rule for that opposition: micro-vectors "structurally opposed … not merely non-overlapping" (`anti-bias-vector-composition/SKILL.md`, principle). Map the canonical axes onto framing: Lane Z = advocate angle, Lane A = alternative-framing angle, tensioned on the **methodology** or **source-corpus** axis (closed vocabulary, same skill §four-canonical-axes). The `anti_bias` axis names *why the two refinements cannot collapse into one*. |
| **check-tension gate (Tests 1–4)** | **a new gate inside the strategy-preview/permission step** (process steps 7–8) | Refine already pauses for a human "Run Strategy Proposal" confirm. Insert the check-tension gate *before* that human confirm, exactly where the router places it ("between Propose and Confirm" — `check-tension/SKILL.md` §when-it-runs). The two independent agents verify the two refinement lanes are genuinely tensioned (Test 2 clone / Test 4 evidence) so the human never confirms a fake-opposition pair. This is the formal guarantee that the two-lane discipline is *real*, not decorative — directly answering TWO-LANE-DISCIPLINE.md's "honest only if it ran the idea into at least one real counterexample." Gate agents are infrastructure: no ledger row, not self-gated (`check-tension` §infrastructure). |
| **register-dispatch ledger (two appends, `exit_reason` vocab)** | **fused with the run-manifest contract** (`RUN-MANIFEST.md` / `evidence-index.json`) | Refine's manifest is a private evidence folder; the dispatch ledger is the repo-wide append-only record. Make every refine-spawned dispatch (research, the review interrogations, the experiment overlay, the two-lane subject group) emit its **dispatch row at spawn** and **close row at termination** (`register-dispatch` §two-appends, P3 append-only). Refine's per-stage `pass\|flag\|block` verdicts map onto the close-row `exit_reason` closed vocabulary `resolved \| loop_ceiling_reached \| dissent_irreconcilable \| user_abort \| error`. Crucially: a two-lane synthesis that cannot adjudicate closes `dissent_irreconcilable`, not `pass` — refine gains a *first-class vocabulary for honest non-convergence* it currently lacks. `max_loops`/`loop_cap`/`layers` (three dials, three scopes) replace refine's ad-hoc preset budget knobs. |
| **robot_talks** | **the Final Interrogation → synthesis seam** (stage 10) and the two-lane join | P7: `robot_talks: true` → the group *synthesizes* rather than concats; a downstream synthesizer "MUST receive each agent's initial AND final positions" (`domainspec-subagents-strategy` P14). Refine's final synthesis is the natural adjudicator of the two lanes — bind the two-lane subject group `robot_talks: true` so the lanes discuss and the synthesis sees collapse vs. genuine-convergence. This *is* TWO-LANE-DISCIPLINE.md's "synthesis (adjudication)" step, with its bridge-decision verdicts (`borrow-carefully \| analogy-only \| block \| promotion-candidate \| future-work`) recorded as the refine `RESULT.md` per-claim verdicts. |

## What refine becomes

A first-class dispatch consumer: the canonical ten stages stay, but stages 3/4/7/10
and the toy-game overlay each *route to a LIVE dispatch_type* instead of running
private single-agent prose. The single track splits into a tensioned n≥2 subject
group (anti-bias composition designs it, check-tension proves it, the human
confirms it once), and every spawned dispatch lands two rows in the shared ledger
with honest `exit_reason`s. `final_approver: parent` stays the one human gate
refine already has (P12 / `SKILL.md` §strategy-preview-and-permission).

## Boundary the maximal version must respect

The two-lane group is a **subject group** (`investigate`/`evaluate`), so anti-bias
applies; the synthesis writer and any auditor are single-owner and are *not*
gate-checked (`anti-bias-vector-composition` §where-it-applies). Refine must not
register its check-tension agents (infrastructure, no row). And refine stays
non-executing: bridge decisions are local, promotion needs a separate
`task-session` (TWO-LANE-DISCIPLINE.md §synthesis) — consistent with refine's
existing "Task Session … out of the loop except as optional next-route"
(`SKILL.md` §quality-bar).
