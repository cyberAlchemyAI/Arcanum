# Open Model Definition Card

## Lane Receipt

- Lane: `open-model-definition-card`
- Result: `PASS`
- Scope: AutoBayes section 2, plus existing local AutoBayes research artifacts.
- Primary source: [AutoBayes: A Compositional Framework for Generalized Variational Inference](https://arxiv.org/pdf/2503.18608), section 2.
- Local context: `research/autobayes/GLOSSARY.md`, `research/autobayes/DEFINITIONS.md`, `research/autobayes/DISTILLED-KNOWLEDGE.md`, `research/autobayes/sessions/full-mode-source-receipts.md`.
- Promotion guardrail: this is a local research definition card. It does not promote AutoBayes vocabulary into canonical Arcanum terms.

## Source Definition

AutoBayes defines an open model as a composable probabilistic model between two measurable spaces. For measurable spaces `X` and `Y`, an open model

```text
p : X -> Y
```

consists of:

- a latent space, written in the paper as the denotation/carrier of `p`;
- a measure kernel:

```text
p : X -> latent(p) x Y
```

The paper names:

- `X` as the unobserved space;
- `Y` as the observed space;
- `latent(p)` as the latent space.

The word "open" is not a metaphor for flexibility. It means the model is not complete by itself: it is composition-ready and behaves like a conditional probabilistic component. Models with domain `1` are non-conditional distributions; a model `1 -> 1` is closed.

## Notation Translation

The paper uses a specialized arrow for open models and a bracket-like notation for the latent carrier. For this card, the ASCII form is:

```text
p : X -> Y
latent(p) = hidden carrier of p
kernel(p) : X -> latent(p) x Y
```

This is not just an ordinary stochastic map `X -> Y`. The observable output `Y` is only one part of the kernel output. The model also carries an internal latent component that may become hidden when composition closes over intermediate values.

## Worked Composition Example

Take two open models:

```text
p : X -> Y
q : Y -> Z
```

with kernels:

```text
p : X -> latent(p) x Y
q : Y -> latent(q) x Z
```

Their sequential composite is:

```text
q after p : X -> Z
```

But the composite latent space is not merely:

```text
latent(p) x latent(q)
```

AutoBayes defines it as:

```text
latent(q after p) = latent(p) x Y x latent(q)
```

The intermediate observed value `Y` becomes hidden inside the composite. This is the core reason the open-model definition matters.

In kernel form, the composite samples:

```text
s, y from p given x
t, z from q given y
```

and stores the hidden carrier as:

```text
(s, y, t)
```

while exposing only:

```text
z
```

So composition changes what counts as latent. A value can be observed at one local boundary and latent at the composite boundary.

## Minimal Toy Reading

Suppose:

```text
p : patient-condition -> symptom
q : symptom -> diagnosis-report
```

Locally, `symptom` is the observed output of `p` and the input of `q`.

After composing:

```text
q after p : patient-condition -> diagnosis-report
```

the symptom is no longer exposed by the composite model. It is carried in the composite latent space:

```text
latent(p) x symptom x latent(q)
```

This is why the intermediate output must not disappear from the formal account. It is hidden from the outside, but still structurally present.

## Arcanum Reading

For Arcanum, the safest translation is:

```text
An open model is a route-capable probabilistic component whose boundary records
both visible outputs and the hidden carrier that composition must preserve.
```

The useful analogy is not "Bayesian model equals sigil." The better analogy is:

```text
composition is only trustworthy when every step declares what enters,
what exits, and what hidden state becomes carried after composition.
```

This maps cleanly to Arcanum instincts:

- `X`: upstream condition or unobserved input surface;
- `Y`: local observed output or handoff boundary;
- `latent(p)`: state namespace carried by this component;
- `latent(p) x Y x latent(q)`: composite state that keeps the intermediate handoff accountable after it is no longer visible.

This is close to why Arcanum separates source context, handoff handles, receipts, state namespaces, and promotion boundaries. Composition should not erase the intermediate thing that made the next step legal.

## Misuse Warnings

- Do not read "open" as vague extensibility. In AutoBayes, open means open to composition.
- Do not collapse latent space into generic Arcanum context. Latent space is a typed carrier in a probabilistic model.
- Do not equate latent space with Arcanum residue. Residue is an analogy at best; it is not the paper's term.
- Do not treat `p : X -> Y` as an ordinary function arrow. The open model includes a kernel into `latent(p) x Y`.
- Do not forget that composition changes the latent carrier. The intermediate `Y` becomes latent in `q after p`.
- Do not canonize this into Arcanum vocabulary yet. Use it as a research analogy until crosswalk and residue passes decide what should be borrowed, blocked, or kept analogy-only.

## Why This Card Matters

Open model is the first load-bearing object in AutoBayes. Later concepts depend on it:

- Bayesian lenses add local inversion to open models.
- Statistical games add local energy and entropy to Bayesian lenses.
- Parameterized statistical games expose optimization handles after the model/lens/loss structure exists.
- Optimization semantics are layered on top, not mixed into the open-model definition.

If "open model" drifts, every later Arcanum reading drifts with it.

## Open Residue

- Closed follow-up: [cups-caps-boundary-shift-card.md](cups-caps-boundary-shift-card.md) covers `reveal`, `copier`, `cup`, `cap`, and boundary-shift reading at operator level.
- Closed follow-up: [bayesian-lens-definition-card.md](bayesian-lens-definition-card.md) follows one open model into a Bayesian lens and reverse-state discipline.
- Closed follow-up: [two-step-symbolic-loss-calculation.md](two-step-symbolic-loss-calculation.md) shows how the open-model carrier affects local free-energy composition.
- Closed follow-up: [arcanum-bridge-decision.md](arcanum-bridge-decision.md) and [implementation-residue-note.md](implementation-residue-note.md) record borrow/block/analogy-only decisions before any Arcanum governance import.
