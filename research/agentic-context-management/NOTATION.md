# Notation Bridge

Target: `arXiv:2607.21503v1`

The paper is light on formalism, but two equations carry much of its economic
and information argument. Reusable notation conventions remain in the
[shared research notation glossary](../shared-notation-glossary.md); the symbols
below are source-specific.

## Cost Model

| Symbol | Source meaning | Plain-language reading | Used in |
| --- | --- | --- | --- |
| `n` or `N` | Number of conversation turns | How long the conversation runs | Paper §3.1, §5, Appendix A |
| `k` | Current turn index | One position in the conversation | Paper §3.1 |
| `t` | Approximate new tokens added per turn | Average turn growth | Paper §3.1, Appendix A |
| `W` | Fixed context budget per turn | Maximum bounded working context | Paper §3.1, Appendix A |
| `p` | Turns between compactions | Compaction cadence | Paper §5 |
| `c` | Validation/compaction cost as a multiple of bounded context | Extra periodic checking cost | Paper §5 |
| `C_append` | Cumulative input tokens under full append | Total tokens paid when all history is resent | Paper §3.1 |
| `C_bounded` | Cumulative input tokens under fixed budget | Total tokens paid with bounded context | Paper §3.1 |

The source's core derivation is:

```text
C_append = sum(k * t, k=1..n)
         = t * n(n+1) / 2
         = O(n^2)

C_bounded = n * W = O(n)

C_append / C_bounded = t(n+1) / (2W)
```

The repeated validated-compaction envelope is:

```text
C_managed(N) = N * W * (1 + c/p)
```

These are conditional accounting models. They do not include prompt caching,
variable turn sizes, output-token billing, retrieval overhead, or quality loss.

## Sufficiency Bottleneck

The paper writes:

```text
answer quality <= min(extraction quality,
                      retrieval quality,
                      reasoning sufficiency)
```

Read this as a bottleneck model: the weakest stage caps the answer. It is not a
calibrated metric, statistical estimator, or proved inequality over specified
random variables.

## Lifecycle Product Shape

The paper's `primitives x scopes` phrase means that every primitive must be
considered at every allowed context scope. It is a design matrix, not numeric
multiplication.

## Reading Order

1. Cost symbols and assumptions
2. Sufficiency bottleneck
3. Five primitives in [DEFINITIONS.md](DEFINITIONS.md)
4. Worked [cost envelope](worked-examples/cost-envelope.md)
5. Worked [retrieval-sufficiency counterexample](worked-examples/retrieval-sufficiency.md)

## Notation Residue

None for reading the paper. Empirical values for fidelity, latency, and
context-rot resistance remain evidence residue rather than notation residue.
