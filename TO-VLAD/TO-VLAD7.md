---
to: Vlad
from: Victor (x-ray composition analysis, synthesized)
re: "Arcanum/x-ray — how it composes with the discovery pipeline (discovery agent, two-view system/engineer, the research skill), and the two borrows that get x-ray past its own promotion gate"
date: 2026-06-10
audit-against: "Arcanum/arcana/x-ray @ HEAD (seed, v0.2.0-seed); domainspec two-view-discovery + domainspec-discovery-writer; research skill in Arcanum (research-tower/evidence-harness/publication-pipeline) and in domainspec-theorem (explorer/skeptic/writer/auditor)"
status: draft for discussion — implementation handoff
---

# To Vlad — where x-ray sits in the discovery pipeline, and what it should borrow

Seventh pass. This one is not an audit of an Arcanum object against a gap; it is a
**placement argument**. I was asked how `x-ray` would help — or be helped by — four
neighbours that all live in the same neighbourhood: the **discovery agent**
(`domainspec-discovery-writer`), the **two-view discovery** (system-view +
engineer-view), and the **research skill** (Arcanum's three-skill tower/harness/pipeline
*and* domainspec-theorem's explorer/skeptic/writer/auditor dispatch). The short answer is
that x-ray composes *downstream* of all of them, and the highest-value move is not wiring
x-ray into everything — it is pulling two disciplines *into* x-ray. That borrow is what
clears x-ray's own promotion gate.

## 1. The one observation that organizes everything

x-ray, the two-view discovery, the discovery agent, and the research skill are the **same
move along four different axes**: *split an opaque target into typed perspectives, hold an
evidence/inference boundary, then compose.* They differ only in what they split by.

| Subsystem | Splits by | Boundary it enforces |
| --- | --- | --- |
| research (theorem) | epistemic **role** — explorer / skeptic / writer / auditor | reference status `verified / em-leitura / nao-lido / refuta` + dissent |
| research (Arcanum) | **register** — source-reader / glossary / distill | source-claim vs. Arcanum-reading + residue ledger |
| two-view discovery | **altitude** — system-view (why) / engineer-view (contract) | decision state `Settled / Recommended / Open / Deferred` |
| x-ray | visual **lane** — surface / components / flow / deps / risk… | source-evidence vs. inference, rendered as toggleable layers |

x-ray is the only one whose output axis is **visual rendering**. That is why it does not
compete with the other three — it composes after them. The natural pipeline:

```text
research  →  discovery agent  →  two-view split  →  x-ray
(epistemic   (writes the         (altitude          (visual decomposition
 evidence)    discovery node)     decomposition)      + layered HTML render)
```

Each stage hands a more-structured artifact to the next; x-ray is the terminal renderer
that makes the accumulated structure inspectable. Read that way, x-ray is not a peer of
the discovery machinery — it is its display surface.

## 2. x-ray ↔ two-view discovery — the strongest fit, and it runs both ways

The mapping is almost exact. x-ray's two interaction primitives — **layer isolate** and
**layer compare** — are precisely what a two-view discovery needs: toggle the "why" layer
(system-view) against the "contract" layer (engineer-view), with the `refines` /
`refined-by` edge rendered as x-ray's **trace** interaction.

- **system-view** ≈ x-ray `{surface, properties, risk_questions}` at C4-L1 / explanation altitude.
- **engineer-view** ≈ x-ray `{components, internal_dependencies, external_dependencies, flow, lifecycle}` at C4-L2/3 / reference altitude.

So **x-ray is a renderer for the two-view pair** (`mode: artifact`, target = the
`system-view.md` + `engineer-view.md` pair). The engineer-view's terminal **Decision
inventory** (Settled/Recommended/Open/Deferred) and **What-we-don't-know** table map onto
x-ray's `risk_questions` lane plus the evidence/inference boundary. And x-ray's hard rule —
*every visual element maps back to source evidence or an explicit inference* — is the same
discipline as the two-view's traceability axiom.

**Reverse direction — the two-view fixes a real hole in x-ray.** x-ray's nine lanes are
flat: no concept of altitude, no decision-state. The two-view contributes exactly what
x-ray lacks: (a) **altitude separation** as a first-class structuring principle, and (b)
the **decision-completeness graduation gate** ("zero *critical* Open/Deferred rows
licenses the next artifact"). x-ray's `risk_questions` lane is a blunter version of the
engineer-view's typed Decision inventory; it should adopt that typing.

## 3. x-ray ↔ the discovery agent (and a duplication flag)

`domainspec-discovery-writer` emits a `node_type: discovery` with a fixed shape:
decisions, alternatives table, open questions, **connections table** (graph edges). Every
one of those maps to an x-ray lane — `risk_questions ← open questions`, `flow`/`components
← connections`, `properties ← decision content`. So x-ray is a clean downstream renderer
of a discovery node, for a reviewer who needs to judge conceptual shape without reading
prose.

**Flag worth raising on the domainspec side:** there is an in-flight
`knowledge-graph-visualization` feature. x-ray is, definitionally, a "turn graph structure
into layered HTML/SVG" engine with a YAML visual library. Either x-ray *is* a candidate
rendering engine for that feature, or a boundary needs to be drawn deliberately — left
alone they will drift into duplicated capability.

**Candor:** the discovery agent is deterministic and schema-precise (it is even forbidden
from writing `veracidade`/`convicção`). x-ray *adds inference*. Run over a discovery node,
x-ray must operate in high-fidelity mode and mark essentially nothing as inference — the
structure is already precise; inventing more corrupts a governance artifact.

## 4. x-ray ↔ the research skill — the borrow that matters most

This is where the load-bearing recommendation lives, and it goes **both ways**.

**Research → x-ray (the important direction).** x-ray's single biggest weakness — the one
gating its own promotion — is that its evidence/inference boundary is **binary**. The
research subsystems are masters of exactly this distinction:

- theorem's `references_consulted.status` = `verified / em-leitura / nao-lido / refuta`;
- Arcanum's tower: source-claim vs. related-source vs. local-inference vs. analogy vs.
  open-residue, plus the **residue ledger** and typed **closure marks**.

x-ray should **adopt the research reference-status vocabulary as its evidence-marker
palette** instead of a binary split. That is a direct, shippable upgrade, and it is
*your own* vocabulary — no new coinage. The residue ledger / closure marks
(`open → closed-borrowing / closed-contribution / …`) map onto x-ray's `lifecycle` lane.

**x-ray → research.** A research dispatch *produces a graph with provenance baked in* —
Layer-1 per-agent records, Layer-2 LEDGER, Layer-3 discovery, references-with-status,
dissent records, closure marks. That is x-ray's home turf:

- `components` ← the agent roster (explorer/skeptic/writer/auditor);
- `flow` ← the dispatch composition (triangulation / nested-waves / zig-zag);
- `external_dependencies` + evidence markers ← references with their status;
- `risk_questions` ← surviving dissent + open residue;
- `lifecycle` ← closure marks.

Highest-value piece: x-ray could **make the false-consensus check visible** — render
whether the declared anti-bias tension was actually *exercised* (where each skeptic's
attack vector landed, which pairs disagreed). Today that lives in an auditor's text
record; x-ray turns it into a layer you can see.

**The pipeline insight.** When x-ray faces a target it cannot honestly understand from
surface inspection — a Lean proof in `domainspec-theorem`, a category-theory bridge like
the `CRAFT-FORMAL-FOUNDATIONS.md` we committed two days ago — it should **dispatch a
research run first** to build the source-backed claim ledger, then render that ledger.
Research is the *understand* phase; x-ray is the *show* phase. For formal content the
renderer ladder finally earns its keep: Mermaid for proof DAGs, inline SVG for commutative
diagrams.

## 5. Caveats said plainly, not papered over

- **Generated-artifact drift.** x-ray output is *derived* HTML. For governance artifacts
  (discovery nodes, two-view pairs, research Layer-3) the source of truth must stay the
  markdown. x-ray output is a disposable, regenerable view — never committed as canonical,
  or you have minted a second source of truth.
- **Seed status is load-bearing here.** x-ray is unpromoted with no live evidence. You
  cannot make a *spec-licensing* artifact (the two-view's whole purpose) depend on an
  unproven renderer. x-ray is an optional visualization adapter, not part of the
  governance chain — yet.
- **Do not let x-ray re-decompose.** research and the two-view already carry a native
  split (by role, by altitude). x-ray must *respect* that split — render system-view as
  one layer-set, engineer-view as another — not impose its own nine lanes on top and
  create a third, conflicting structure.

## 6. The recommendation, in one line

The genuinely load-bearing move is **not** "wire x-ray into everything." It is the **two
borrows that flow into x-ray**: pull the research skill's typed reference-status +
residue/closure vocabulary into x-ray's evidence boundary, and pull the two-view's
altitude + decision-state typing into x-ray's lane model. Those two borrows are what would
actually carry x-ray *past its own promotion gate*. The rendering direction (x-ray over
discoveries / research dispatches / two-view pairs) is real and nice-to-have, but it is
downstream polish — and it should wait until x-ray clears seed status, so we are not
rendering governance artifacts through an unproven engine.

---

## Three sharpest questions, in order

1. **Does x-ray's binary evidence/inference marker become the research four-value status
   (`verified | em-leitura | nao-lido | refuta`), or a superset that also carries
   `analogy` and `open-residue`?** This decides the evidence-boundary vocabulary x-ray
   promotes on.
2. **x-ray vs. `knowledge-graph-visualization`: one engine or two?** If one, which owns
   the YAML visual library; if two, where is the boundary drawn so they do not duplicate.
3. **Does the research → x-ray pipeline ("understand then show") become a named spell, or
   stay an ad-hoc invocation?** A spell forces the evidence ledger to exist before any
   pixel is drawn — which is the whole point.

— V.
