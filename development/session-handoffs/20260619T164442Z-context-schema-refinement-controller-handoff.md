# Session Handoff: Context-Schema Refinement Controller

## Identity

- Source session reference: current Claude Code thread (ZefraHub), user request at `2026-06-19T16:44:42Z`
- Destination label: `context-schema-refinement-controller`
- Handoff type: `new-lifecycle-thread`
- Target project or lifecycle: `arcanum` — new method/capability lifecycle (sigil candidate, owner decided at define)
- Created for: open a governed `invoke define` lifecycle for a method that, at a given moment in an agentic task, selects the next-best information chunk to inject into the agent's context window and decides how far to refine the task's schema — driven by task entropy reduction and the marginal utility of further schema definition.

## New Session Prompt

```text
Continue from arcanum/development/session-handoffs/20260619T164442Z-context-schema-refinement-controller-handoff.md.

Goal: define an Arcanum method that decides (a) the best chunk of information to add to an
agent's context window at a given moment, and (b) how far to refine that task's schema — as a
function of task uncertainty (entropy) and the marginal utility of revealing more schema.

Start from the conceptual model in this handoff (typed residue, schema/instance, reflection
tower, governance-attenuation ceiling, orthogonal veracidade × convicção). Do not implement;
run `invoke define` first and decide the owner type (sigil vs spell vs transmutation) at the
define gate.
```

## Route Rationale

- Recommended next route: `invoke define`
- Rationale: the idea is conceptually rich but the artifact type, the measurable signals, and the stop-rule are not yet pinned. A define-stage spec + glossary must fix the method's inputs/outputs, the context-level taxonomy, the entropy/utility signals, and the owner type before any design or implementation.
- Lifecycle owner: `invoke` for the next authoring step; likely downstream owner is `sigil-development` (if the method is an atomic reusable sigil that spells like `context-builder`, `distill`, `decision-gate` call) or `spellcraft` (if it composes several sigils into a controller loop).

## The Method in One Statement

> At any moment in a task, inject the information chunk that maximizes expected reduction of the
> task's entropy per unit of context cost, and keep refining the task's schema only while the
> marginal utility of further schema definition exceeds its marginal cost.

This is a **Value-of-Information controller for schema discovery**: context injection and schema refinement are not "load everything" — they are an economic decision bounded below by uncertainty and above by saturation.

## Conceptual Model (carried from the source session)

This method is the operational head of a chain developed across the source session, grounded in the sibling `domainspec` project:

1. **Typed residue.** Every task is a rich reality translated into a lean description; what fails to cross is the *residue*. The task's *schema* is the latent structure (invariants, contracts, edge cases) the description is trying to capture. (`domainspec` `ResidueStructure`.)
2. **Schema vs instance.** Schema = the abstract task structure (L1); instance = the concrete artifact/diff the agent produces. The agent's residual error splits into η^sch (schema-leakage: right realization, wrong contract — invisible to green tests) and η^ins (instance-failure: right contract, broken realization).
3. **Reduce entropy → reveal schema.** Injecting the *right* context chunk lowers the task's uncertainty, which makes the optimal schema legible. The method's objective function is entropy reduction, not coverage.
4. **Refinement is inverse to uncertainty.** The less uncertainty remains, the more of the optimal schema becomes visible, so the deeper you can responsibly refine. You cannot refine past what the evidence reveals.
5. **Marginal-utility stop rule (the real inflection point).** Refine until the marginal utility of revealing more schema drops below its marginal cost. The "ponto de inflexão" is NOT where uncertainty crosses investment — it is where `MU(more schema) = MC(defining + governing it)`.
6. **Governance-attenuation ceiling.** From `domainspec/GOVERNANCE-ATTENUATION.md`: governance/instruction fidelity decays as layers accumulate (Shannon `C = B·log₂(1+S/N)`; observer-executor conflation; instruction dilution). Over-refining past the saturation point *reduces* fidelity. This is the hard upper brake on refinement depth.
7. **Orthogonality correction (from `domainspec/vault/ontology-conventions.md`).** "How much to refine" is governed by TWO orthogonal axes, not one curve: `veracidade` (evidence ≈ 1 − uncertainty) and `convicção` (commitment/investment). They have zero mutual information by design. The interesting cell is `veracidade:low + convicção:high` — the **Strategic Bet**: refine the schema *early*, before evidence, when marginal utility is high. The `status` lifecycle (draft → exploratory → active → consolidated → evergreen) is the staged refinement ladder. A naive "invest more as you know more" curve collapses these two axes and must be rejected.

## Context Levels — Open Taxonomy Question

The user proposed market / business / technical and asked whether there are more. Provisional answer: **yes**. A task's context is multi-level; the method should choose the chunk from the level where current uncertainty is concentrated. Candidate taxonomy to ratify at define (mapped partly onto `domainspec` `layer` values: ontology, architecture, market, domain, application):

| Level | What it carries | Source-of-truth analog |
| --- | --- | --- |
| Market | external/regulatory/competitive reality | `domainspec` `layer: market` |
| Business | goals, value, priorities, ROI of the task | premise/convicção |
| Domain | specific business rules (e.g. FIDC, CCB, liquidação) | `domainspec` `layer: domain` |
| Technical | architecture, code, infra, types | `domainspec` `layer: architecture/application` |
| Regulatory / Compliance | hard external constraints that bound the schema | (candidate — split from Market) |
| Data / Evidence | available data, its shape and reliability | veracidade |
| Organizational / Process | team conventions, ownership, workflow | (candidate) |
| Ontological / Vocabulary | the definitions the task's terms commit to | `domainspec` `layer: ontology` |
| Temporal / Provenance | why prior decisions were made (history) | sessions / provenance edges |

Define must decide which of these are first-class levels vs collapsible, and whether "context level" is the right partition at all (open question O-CTX below).

## Context Builder Selection

| Obligation | Coverage | Selected Source | Why It Matters |
| --- | --- | --- | --- |
| O-001 Preserve the user's split reason. | covered | User prompt: "passar isso para o arcanum, como podemos criar um método disso." | Keep this as a lifecycle split toward a new method definition, not immediate implementation. |
| O-002 Carry the user's refined hypothesis verbatim. | covered | User hypothesis on best-chunk / entropy / schema / refinement inverse to uncertainty / marginal utility. | It is the seed spec; the define stage must preserve and operationalize it, not paraphrase it away. |
| O-003 Ground the typed-residue / schema model. | covered | `domainspec-lean-formalization` `ResidueStructure`, reflection tower, η^sch vs η^ins. | The method's "schema" and "residue" must mean what `domainspec` formalizes, not loose metaphor. |
| O-004 Ground the refinement ceiling. | covered | `domainspec/GOVERNANCE-ATTENUATION.md` (Shannon capacity, layer-fidelity decay). | Without it, the method would recommend unbounded refinement; attenuation is the upper brake. |
| O-005 Ground the orthogonality correction. | covered | `domainspec/vault/ontology-conventions.md` §6 veracidade × convicção 2×2 + `status` lifecycle. | Fixes the false single-curve model and supplies the Strategic-Bet cell that justifies early refinement. |
| O-006 Keep implementation deferred. | covered | `spells/invoke/handoff.md` (handoff prepares context, does not mutate downstream lifecycle). | Define/design must precede any controller implementation. |
| O-007 Resolve the context-level taxonomy. | partial | Provisional taxonomy above; `domainspec` `layer` values. | Define must ratify or restructure the levels; flagged as open. |

Strict coverage: `flag` (O-007 partial — non-blocker for a new-lifecycle-thread handoff).

## Selected Session Context

- User refined hypothesis (verbatim seed)
  - Obligation refs: O-001, O-002
  - Context summary: choose the best chunk to add to the agent's window at a moment; depends on task context (market/business/technical + more); objective is to reduce task entropy; that reveals the task's schema; refine the schema up to a point; refinement level is inverse to uncertainty; the stop-point depends on the marginal utility of defining more of the schema.
- Typed-residue chain (this session's prior turns)
  - Obligation refs: O-003
  - Context summary: task = rich→lean translation; residue is what fails to cross; schema/instance split; η^sch (schema-leakage, test-invisible) vs η^ins (instance-failure); reflection tower names the residual to produce the next refinement level.
- Governance-attenuation finding
  - Obligation refs: O-004
  - Context summary: governance/instruction fidelity decays as layers accumulate (only ~30–40% of expected signals emitted in domainspec's own runs); Shannon channel-capacity framing; over-refinement saturates the LLM's instruction bandwidth.
- ontology-conventions finding
  - Obligation refs: O-005
  - Context summary: "how much to refine" answered by orthogonal veracidade (evidence) × convicção (commitment); 2×2 archetypes (Strategic Bet / Ignored Fact / Consolidated Law / Loose Thread); `status` lifecycle as staged refinement ladder; the single inverse curve is explicitly refuted (zero mutual information by design).

## Excluded Context

| Candidate | Reason Excluded |
| --- | --- |
| Full domainspec Lean file inventory (291 files) | The method needs the concepts (residue, tower, attenuation), not the proof artifacts. |
| ZefraHub matching-test rule files (cluster_*.json) | A strong empirical testbed for a later validation stage, but not needed to define the method. Note it for design/validation. |
| Prior CV / unrelated dispatch ledger rows | Not relevant to the method's concept. |
| Full chat transcript | Obligation-relevant excerpts above suffice; carrying the transcript defeats the handoff. |

## Target Boundary

- In scope for the new thread:
  - Define the method's inputs (task, current context window, candidate chunks, context levels) and outputs (next-best chunk + refinement stop decision).
  - Operationalize the signals: a usable proxy for task entropy / uncertainty, expected entropy-reduction-per-token (information gain density), and marginal utility vs marginal cost of schema definition.
  - Ratify the context-level taxonomy (or replace it).
  - Encode the two brakes: lower (uncertainty/veracidade — don't refine past evidence) and upper (governance-attenuation — don't refine past saturation).
  - Encode the Strategic-Bet exception (refine early when MU is high despite low veracidade).
  - Decide the owner type at the define gate: sigil (atomic, called by `context-builder`/`distill`/`decision-gate`), spell (composed controller loop), or transmutation (cross-cutting).
- Out of scope for the new thread:
  - Implementing the controller or wiring it into any spell before define/design approval.
  - Mutating `context-builder`, `distill`, `refine`, or `decision-gate` sigils.
  - Treating "context level = market/business/technical" as final before O-CTX is resolved.
- Prior decisions to preserve:
  - Reject the single inverse-curve model; refinement is governed by two orthogonal axes.
  - The inflection point is the marginal-utility crossing, not the uncertainty/investment crossing.
  - Governance-attenuation is a hard ceiling on refinement depth.

## Gaps And Blockers

| Gap | Owner | Status | Next Action |
| --- | --- | --- | --- |
| O-CTX: Is "context level" the right partition, and what is the canonical level set? | `invoke define` | open | Ratify/replace the provisional 9-level taxonomy; decide first-class vs collapsible levels. |
| O-ENT: What is a computable proxy for "task entropy" the controller can actually evaluate? | `invoke define` then `invoke design` | open | Choose a measurable signal (e.g. spread of candidate schemas, agent self-reported uncertainty, disagreement across probes) — avoid an immeasurable abstraction. |
| O-UTIL: How is marginal utility of schema definition estimated at runtime? | `invoke define` | open | Define a VoI estimate (expected error reduced × value-at-stake) and its marginal-cost counterpart. |
| O-OWN: Sigil vs spell vs transmutation. | `invoke define` gate | open | Decide owner type from the input/output and reuse surface. |
| O-VAL: What proves the method works? | `invoke design` | deferred | Candidate testbed: ZefraHub matching-test rule synthesis (cluster_*.json) — does the controller pick chunks that reveal the cluster's rule schema in fewer steps? |

## Next-Session Start Prompt

```text
Read arcanum/development/session-handoffs/20260619T164442Z-context-schema-refinement-controller-handoff.md.

Task: run `invoke define` for the Context-Schema Refinement Controller method.

Preserve the user's seed hypothesis verbatim and the three groundings (typed residue,
governance-attenuation ceiling, veracidade × convicção orthogonality). Produce:
1. a define spec: inputs, outputs, the entropy objective, the marginal-utility stop rule,
   the two brakes, and the Strategic-Bet exception;
2. a glossary (task entropy, schema, residue, refinement level, marginal utility, context level,
   information gain density, governance-attenuation ceiling, veracidade, convicção);
3. a resolved or explicitly-deferred decision on O-CTX (context-level taxonomy) and O-OWN (owner type).

Do not implement. Stop at the define gate and recommend design vs sigil-development vs spellcraft.
```

## Provenance

- Source refs:
  - current Claude Code (ZefraHub) user prompt at `2026-06-19T16:44:42Z`
  - `c:\Users\victo\domainspec-lean-formalization` — `ResidueStructure`, reflection tower
  - `c:\Users\victo\domainspec\GOVERNANCE-ATTENUATION.md`
  - `c:\Users\victo\domainspec\vault\ontology-conventions.md` (§6, Appendix B)
  - `c:\Users\victo\ZefraHub\internal_tools\ccb-registration-demo\matching-test\rules\` (candidate validation testbed)
  - `spells/invoke/handoff.md`
- Context Builder mode: `standard`
- Evidence date: `2026-06-19`
- Output path: `development/session-handoffs/20260619T164442Z-context-schema-refinement-controller-handoff.md`
- Context index: `development/session-handoffs/20260619T164442Z-context-schema-refinement-controller-context-index.json`

## Gate Result

- Status: `pass`
- Reason: the handoff carries the user's seed hypothesis verbatim, grounds it in the three domainspec sources, names the correct next route (`invoke define`), preserves the marginal-utility-inflection and orthogonality decisions, and records the open taxonomy/owner/signal gaps for the new lifecycle to resolve.
