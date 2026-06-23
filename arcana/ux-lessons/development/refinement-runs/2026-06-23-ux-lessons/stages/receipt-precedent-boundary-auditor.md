# Receipt — precedent_boundary_auditor

- **role_id:** precedent_boundary_auditor
- **bias (declared, intentional):** minimize new surface area / force build-from-owned. I am the skeptic that ux-lessons does NOT need to be a net-new sigil.

## findings

### 1. Which existing capabilities already own each piece of `session → lesson → ux-pattern → consumer`?

The pipeline is NOT greenfield. Each stage has an in-repo owner; the gap is a thin UX-specific framing, not a new engine.

- **session-signal substrate** — fully owned. `signal-observer` (arcanum/arcana/signal-observer/SKILL.md) derives behavior-level signals from an invocation envelope and appends telemetry; the top-level `observed-invocation-loop` skill guarantees the post-run handoff. ux-lessons must NOT re-derive signals; it consumes the envelope/ledger these already produce.
- **session → improvement unit** — owned by `workflow-reflect` (arcanum/arcana/workflow-reflect/SKILL.md). It is the closest cousin: it groups accumulated signals, separates threshold-backed findings from weak signals, and emits evidence-backed *proposals*. CAVEAT: it has zero "lesson" or "pattern-library" vocabulary (grep confirmed empty) and its authority-rule forbids mutating downstream artifacts — its output is a *proposal*, not a *reusable pattern*. So it owns the analysis shape but NOT a reuse store.
- **reduce to coherent unit (lesson → pattern distillation)** — owned by `distill` (arcanum/arcana/distill/SKILL.md): smallest coherent unit + proof of recompose into the larger system. The "lesson → ux-pattern" compression step is a distill call, not new logic.
- **reusable pattern store** — owned by `architecture-pattern-inventory` (arcanum/arcana/architecture-pattern-inventory/SKILL.md): concept cards, dependency rules, selectively loadable, "observed vs recommended" separation, refresh-trigger. The "save & reuse ux-pattern" half mirrors this store shape directly.
- **residue / learning ledger** — owned by `residuality-spec` (Step 3 "Decide Residue", arcanum/arcana/residuality-spec/SKILL.md) and whisper residue. Don't invent a residue ledger format.
- **consumer #1 intake** — `ux-evidence-validator` already defines the intake contract: "Evidence cards and claim map", `source-card set`, "Load or create evidence cards before creating rule candidates" (SKILL.md L29/L65/L73). A ux-pattern must land as a source-card/evidence-card, NOT a new validator input type.
- **consumer #2 intake** — `projects/ui-prototyping-studio/` (confirmed present) owns its explore/annotate/mutate loop. ux-lessons emits variant/annotation *intents*; it does not generate variants.

### 2. Owner BOUNDARY for ux-lessons

- **Must NOT duplicate:** signal derivation (signal-observer/observed-invocation-loop own it); accumulated-signal grouping & proposal logic (workflow-reflect); the reduction engine (distill); the reusable-pattern store mechanics — cards, dependency rules, refresh-trigger (architecture-pattern-inventory); residue-ledger format (residuality-spec); validator rule authoring & fixtures (ux-evidence-validator); variant generation (ui-prototyping-studio).
- **Must compose/borrow:** signal-observer ledger as input substrate; workflow-reflect's group→threshold→evidence shape for the `session → lesson` step; distill for `lesson → ux-pattern`; architecture-pattern-inventory's card/store schema for the ux-pattern store; residuality-spec residue shape; ux-evidence-validator's evidence-card/claim-map as the consumer #1 output contract.
- **The only genuinely new thing** ux-lessons owns: the *UX-domain framing* of the lesson and ux-pattern artifacts (the page-iteration vocabulary — revert-3D, offset cascade, nested overlay, right-rail inspector, guided tour) and the two-direction consumer adapter (pattern → validator-card / pattern → studio-intent). That is a binding/translation surface, not an engine.

### 3. Capability-shape verdict (from minimize-surface bias)

**SPELL** (composition), not a net-new sigil. Justification: 5 of 6 pipeline stages already have sigil owners; a sigil would re-implement signal-grouping (workflow-reflect), reduction (distill), and pattern-store (architecture-pattern-inventory) under a UX label. A spell (spellcraft owner) wires signal-observer → workflow-reflect-shaped analysis → distill → architecture-pattern-inventory store → two consumer adapters, and contributes ONLY the UX framing + adapter contracts. This is the cheapest shape that still delivers the artifact.
- Honest counter-argument for sigil: a spell only composes *existing* sigils; the `lesson` and `ux-pattern` *artifact schemas* and the bidirectional consumer adapters have no current owner, and spells own no schema. If the new schema + adapter surface is substantial enough to need its own quality-bar/anti-patterns/output-contract, a thin sigil (or a discipline carded under discipline-governance) is defensible. I rate the schema surface as moderate, not large — so spell-first, with a sigil only if spellcraft surfaces an un-ownable schema. **Discipline** is the fallback if "turn a session into a saved lesson" turns out to be a recurring cross-capability *practice* rather than an executable pipeline.

### 4. Single biggest duplication risk if it becomes a net-new sigil

A **second reusable-pattern store** parallel to `architecture-pattern-inventory` — a "ux-pattern-library" that re-invents concept cards, dependency rules, observed-vs-recommended separation, and refresh-triggers under a UX name. This forks the repo's pattern-store mechanics, splits the "where do reusable patterns live" answer, and creates drift between two card formats that both consumers and future agents must learn. Second-order risk: re-deriving session signals instead of consuming the signal-observer envelope, duplicating the observability substrate.

## precedent_owners

| Pipeline stage | Existing owner | What it owns | ux-lessons relation |
| --- | --- | --- | --- |
| session signal substrate | signal-observer + observed-invocation-loop | envelope→telemetry, post-run handoff | consume, never re-derive |
| session → improvement unit | workflow-reflect | group→threshold→evidence proposals (no "lesson"/store vocab) | borrow analysis shape; do NOT borrow proposal-only authority |
| lesson → ux-pattern | distill | smallest coherent unit + recompose proof | call as the compression step |
| reusable pattern store | architecture-pattern-inventory | concept cards, dependency rules, refresh-trigger, observed-vs-recommended | mirror store schema; do NOT fork it |
| learning residue ledger | residuality-spec / whisper residue | residue decision shape | reuse format |
| consumer #1 | ux-evidence-validator | evidence-card / claim-map / source-card intake | emit pattern as evidence-card, not new input type |
| consumer #2 | projects/ui-prototyping-studio | explore/annotate/mutate loop | emit variant/annotation intents only |

## shape_verdict

**SPELL** (spellcraft-owned composition). New surface limited to: (a) `lesson` + `ux-pattern` UX-domain artifact schemas, (b) two consumer adapter contracts. Escalate to thin sigil only if those schemas prove un-ownable by a spell; escalate to discipline if it is a practice not a pipeline. Net-new full sigil REJECTED under build-from-owned.

## confidence

**med** — high on the precedent ownership map (file-cited); medium on spell-vs-thin-sigil, because spells own no schema and the lesson/ux-pattern schemas have no current owner — that single fact is the legitimate pull toward a sigil and should be resolved at the spellcraft/sigil-development boundary in Design.

## anti_bias_note

My minimize-surface bias is intentional and could be wrong in one specific place: it discounts that **a spell owns no artifact schema**, while `lesson` and `ux-pattern` are genuinely new typed artifacts with their own quality-bar/anti-patterns needs. If the reuse-architect (Role B) shows the schema + bidirectional adapter is rich enough to need its own contract and lifecycle, "thin sigil composing the owners" beats "schema-less spell" — and my reflex to call it a spell would be under-building. The tension to resolve: spell (cheap, no schema home) vs thin sigil (owns schema, slight duplication risk). I am biased toward the former; weight Role B's schema-richness evidence against me.

## blocked_reason

none. All seven precedent owners read or grep-confirmed; ux-lessons dir contains only this run's scaffolding (REFINE-SEED-PROPOSAL.md, REFINE-DISPATCH.json) — no prior ux-lessons design to conflict with. observed-invocation-loop is a top-level skill, not under arcana/ (noted; does not change the verdict).
