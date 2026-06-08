# MOGT Methodology And Theory Baseline

Purpose: define the project-level methodology and theory baseline that must guide claim framing, protocol design, source normalization, and inventory extraction before experiment execution.

This artifact is the research-side counterpart to `foundations/DOMAIN-CONTEXT.md`. The domain-context artifact explains what setting MOGT is studying. This artifact explains how MOGT should study it and which theories justify the design choices.

## Why This Artifact Exists

MOGT needs more than a list of citations. It needs a stable explanation of:

- why the research uses paired comparative experiments instead of ad hoc prompting
- why multi-objective reasoning is modeled through explicit objective vectors and frontier logic
- why value-tradeoff structuring belongs upstream of policy comparison
- why traceability, dialogue evaluation, system overhead, and reviewer burden must all be measured explicitly
- how source catalog, reference ledger, and inventory library work together as a reusable research baseline

Without this artifact, protocols can cite the right papers while still drifting methodologically.

## Methodological Stance

### Comparative, Not Anecdotal

MOGT should prefer controlled or paired comparisons over one-off demonstrations.

The default pattern for E1 through E4 is:

1. hold the scenario family fixed
2. compare at least one baseline regime and one intervention regime
3. capture the same metadata envelope for every run
4. evaluate both the final outcome and the trace that produced it

This stance is grounded primarily in `PAPER-WOHLIN-2012` and secondarily in `PAPER-LIU-2024-AGENTBENCH` for agent-evaluation framing.

### Explicit Measurement Before Strong Claims

MOGT should not upgrade claims from design plausibility alone.

Protocols must define measurable outcomes for:

- decision quality
- traceability and explanation recovery
- convergence under disagreement
- token, latency, and reviewer burden overhead

This follows the measurement discipline from `PAPER-WOHLIN-2012`, the evaluation framing from `REPORT-DOSHI-VELEZ-KIM-2017` and `PAPER-WALKER-1997`, and the overhead measurement discipline from `BOOK-JAIN-1991` and `PAPER-HART-STAVELAND-1988`.

### Foundation Tier First

MOGT is still in a greenfield evidence state, so the first research wave should stay at foundation tier unless a protocol is explicitly publication-critical.

That means the default evidence bar is directional validity with hard gates, not maximal sophistication. The goal of the first wave is to learn whether the research direction survives contact with structured measurement.

## Methodology Authority Map

| Source                        | Core contribution to MOGT                                                     | Direct use                                                          |
| ----------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `PAPER-WOHLIN-2012`           | comparative experimental design, validity threats, reproducibility discipline | baseline methodology for E1-E4                                      |
| `REPORT-DOSHI-VELEZ-KIM-2017` | rigorous evaluation of explanation and interpretability                       | E1 traceability and rubric design                                   |
| `PAPER-WALKER-1997`           | quality-plus-cost evaluation framing for dialogue episodes                    | E1 acceptance scoring and E4 quality-versus-overhead interpretation |
| `BOOK-JAIN-1991`              | measurement discipline for latency, throughput, and breakpoint analysis       | E4 overhead instrumentation and threshold reasoning                 |
| `PAPER-HART-STAVELAND-1988`   | reviewer workload measurement through NASA-TLX                                | E4 human-burden accounting                                          |

## Theory Baseline

### Multi-Objective Decision Theory

`PAPER-DEB-2001` is the main authority for objective-vector reasoning, dominance, and frontier logic.

The operational implication for MOGT is that a policy regime should not be called "multi-objective" merely because it mentions several desiderata in prose. It should expose or preserve a structured view of multiple objectives during decision selection.

### Value-Tradeoff Structuring

`BOOK-KEENEY-RAIFFA-1976` is the main authority for explicit objective articulation and value-tradeoff framing.

Its role in MOGT is upstream of algorithm choice. It helps define:

- which objectives belong in the active set
- how objectives are named and bounded
- how reviewer rubrics should distinguish objective satisfaction from explanation quality

### Weighted-Sum Versus Broader Method-Family Framing

MOGT currently keeps `PAPER-MARLER-2010` as the weighted-sum-specific authority because E2 and E4 need a realistic scalarization baseline.

Decision rule:

- keep the 2010 weighted-sum paper when a protocol compares directly against a weighted-sum baseline or discusses weighted-sum failure modes
- add the broader survey as a separate source when the protocol needs field-level framing beyond weighted-sum itself

This avoids forcing one reference to serve two different authority roles.

### Traceability And Explainability Evaluation

`REPORT-DOSHI-VELEZ-KIM-2017` and `PAPER-WALKER-1997` together justify why MOGT treats explanation recovery and quality evaluation as explicit measurement problems instead of informal reviewer impressions.

That means E1 should reward recoverable tradeoff reasoning, not verbosity alone, and E4 should interpret operational cost together with retained decision quality.

### Overhead And Workload Theory

`BOOK-JAIN-1991` and `PAPER-HART-STAVELAND-1988` jointly ground the overhead envelope.

MOGT should keep two overhead families separate:

- system overhead: tokens, latency, and turn count
- human overhead: reviewer burden and interpretive workload

This separation matters because a policy can be cheap for the model while still being expensive for human review.

## Design Implications For E1 Through E4

| Experiment | Baseline implication                                                                                | Main authorities                                                                                             |
| ---------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| E1         | use paired scenarios, blinded review, explicit objective framing, and traceability-specific scoring | `PAPER-WOHLIN-2012`, `BOOK-KEENEY-RAIFFA-1976`, `REPORT-DOSHI-VELEZ-KIM-2017`, `PAPER-WALKER-1997`           |
| E2         | expose candidate actions and objective vectors so dominance and regret are measurable               | `PAPER-WOHLIN-2012`, `PAPER-DEB-2001`, `BOOK-KEENEY-RAIFFA-1976`, `PAPER-MARLER-2010`                        |
| E3         | treat negotiation as bounded structured interaction with explicit convergence and cycling metrics   | `PAPER-WOHLIN-2012`, agentic-conversation prior-art sources, and later negotiation-specific theory           |
| E4         | measure quality, latency, token cost, turn count, and reviewer burden together on matched scenarios | `PAPER-WOHLIN-2012`, `PAPER-WALKER-1997`, `BOOK-JAIN-1991`, `PAPER-HART-STAVELAND-1988`, `PAPER-MARLER-2010` |

## Reference Library Obligations

The MOGT source baseline is not complete when citations are merely listed. It is complete only when the following layers are all present and usable:

1. `sources/SOURCE-CATALOG.md` identifies and pins relevant authorities.
2. `sources/REFERENCE-LEDGER.md` records how each authority is allowed to influence protocol or analysis decisions.
3. `inventory/*.md` acts as a reusable library, not a snippet cache. Each inventory artifact should preserve enough content that later protocol work does not need to re-discover the same source.
4. this artifact and `foundations/DOMAIN-CONTEXT.md` translate the library into project-level guidance.

For MOGT, a library-grade inventory entry should retain:

- canonical citation and pin
- the operational constructs MOGT actually reuses
- where the source is relevant and where it is not
- which experiments it should influence
- what cautions or adaptation rules apply

## Pre-Protocol Checklist

Do not harden or approve a protocol until these conditions are true:

1. `foundations/DOMAIN-CONTEXT.md` explains the decision setting and prior-art context for the target experiment.
2. this artifact explains the methodology and theory baseline the protocol relies on.
3. every primary authority for the protocol is source-cataloged, reference-ledgered, and inventoried.
4. any unresolved authority ambiguity, such as the Marler split, is called out explicitly instead of being hidden in shorthand citations.
5. the protocol can explain why each metric and threshold exists in terms of these foundations rather than prompt intuition.
