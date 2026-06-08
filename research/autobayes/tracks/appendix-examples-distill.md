# Appendix Examples Distill

## Lane Receipt

- Lane: `appendix-examples-distiller`
- Result: `PASS`
- Scope: AutoBayes Appendix A and Appendix B.
- Primary source: [AutoBayes: A Compositional Framework for Generalized Variational Inference](https://arxiv.org/pdf/2503.18608), Appendix A and Appendix B.
- Rendered source used for line-checking: [ar5iv AutoBayes v2](https://ar5iv.labs.arxiv.org/html/2503.18608v2), especially Appendix A Examples and Appendix B On dependently typed models.
- Local context: `research/autobayes/tracks/open-model-definition-card.md`, `research/autobayes/sessions/full-mode-source-receipts.md`, `research/autobayes/levels/L0-corpus.md`.
- Promotion guardrail: this is a local research distill. It does not promote AutoBayes terms into canonical Arcanum vocabulary.

## One-Sentence Distill

Appendix A and B show that AutoBayes is not only a categorical restatement of Bayes; it is a way to re-express familiar learning cases as compositions of open models, lenses, local energy/entropy terms, parameter exposure, and optimization semantics.

## Example A.1 - Gaussian Mixture Model / Maximum Likelihood Estimation

### What It Demonstrates

The Gaussian mixture example demonstrates the simplest useful optimization story: compose a prior over mixture components with a conditional Gaussian observation model, expose the mixture probabilities as parameters, and recover maximum likelihood by descending the gradient of the resulting loss.

Source basis: Appendix A.1 says the setup has an unobserved finite set, a Gaussian distribution over observations conditional on that finite set, and a prior over mixture components whose probabilities are parameterized. The goal is to optimize those probabilities to maximize marginal likelihood on observed data.

### Minimal Paper Mechanics

- There is a finite latent selector for mixture component.
- There is an observation model conditioned on that selector.
- The marginal over observations is a mixture of Gaussians.
- The conditional Gaussian component is equipped with exact inversion.
- Energy is negative log-likelihood.
- Entropy is included where the inversion is nontrivial.
- The prior side has trivial inversion/entropy.
- The exposed parameter is not on the conditional Gaussian component; it is on the prior mixing probabilities.

### Arcanum Mental Model

This is parameter exposure discipline in miniature.

The component that produces the observation does not automatically own the optimizer knobs. The optimizer is allowed to act on the mixture probabilities because the prior component exposes them. In Arcanum terms: the route can have multiple local pieces, but only the declared handle is legitimate for mutation.

```text
local model piece + local loss + exposed parameter
  -> optimizer knows exactly which knob it may touch
```

### Misuse Warning

Do not read this as "AutoBayes is just mixture-model MLE." The example is deliberately simple. Its point is to show how a classic MLE case fits the statistical-game machinery, not to introduce a new GMM algorithm.

## Example A.2 - Expectation-Maximization

### What It Demonstrates

The EM example demonstrates how the E-step and M-step can be viewed inside the same compositional loss setup. The expectation step computes the relevant expected joint-density quantity under the current inversion/posterior structure; the maximization step optimizes the parameterized composite model.

Source basis: Appendix A.2 describes EM as maximum likelihood estimation for a model with an unobserved component. The paper equips a lens and a prior lens with negative log-likelihood energies and entropy terms, then says computing the composite expression constitutes the expectation step, while maximizing with respect to the parameter corresponds to the maximization step.

### Minimal Paper Mechanics

- Start with a model involving an unobserved component.
- Use a lens for the model and a prior lens with trivial inversion.
- Equip both with negative log-likelihood energies.
- Include entropy terms.
- Compose the games.
- The expected joint-density calculation is the E-step.
- Parameter optimization of the composite model is the M-step.

### Arcanum Mental Model

EM is a two-phase route where one phase derives the current hidden-state receipt and the other phase updates the exposed parameter.

```text
E-step = compute current reverse/evidence receipt
M-step = mutate only the parameter handle authorized by the game
```

The Arcanum analogy is a task session that separates "build the evidence frame" from "perform the permitted mutation." The evidence phase and mutation phase are coupled, but they are not the same authority.

### Misuse Warning

Do not collapse EM into "alternate between guessing and tuning." The paper's useful claim is structural: expected loss and parameter update live inside a compositional statistical-game account.

## Example A.3 - Variational Bayesian Expectation-Maximization

### What It Demonstrates

VBEM extends the EM story by making the parameter itself part of the model and adding a prior over that parameter. The result is not just optimizing a point estimate; it is optimizing a composed loss involving a parameterized prior/posterior structure.

Source basis: Appendix A.3 says VBEM extends the preceding EM example so the parameter forms part of the model, adds a prior on the parameter, composes the games, and performs gradient descent on the resulting composite loss.

### Minimal Paper Mechanics

- Start from the EM composition.
- Treat the parameter as part of the model rather than only an external knob.
- Add a prior over the parameter.
- Parameterize that prior/posterior side.
- Compose the resulting parameterized game with the earlier game.
- Optimize the composite loss with respect to the relevant parameter.

### Arcanum Mental Model

VBEM is the moment where the "knob" becomes a modeled object.

For Arcanum: sometimes an execution parameter is just an operator choice; sometimes it deserves its own evidence model, prior assumptions, and update discipline. VBEM is a caution that exposed handles can themselves have structure.

```text
parameter as knob
  -> EM-like

parameter as modeled uncertain object with prior
  -> VBEM-like
```

### Misuse Warning

Do not treat "parameter" as a generic mutable field. In VBEM, the parameter enters the probabilistic composition and is constrained by a prior. That is much stricter than an arbitrary runtime setting.

## Example A.4 - Supervised Learning

### What It Demonstrates

The supervised-learning example shows how AutoBayes uses cups to represent known labels as observed, even when those labels would otherwise occupy an unobserved position in the model. This lets paired input/label data become the observed training surface.

Source basis: Appendix A.4 says cups incorporate supervised learning: one typically knows labels corresponding to observed data, composes a tensor after the cup, and obtains a model in which both labels and data are observed. The inversion usually trivializes because the prior is a deterministic sample, though the regularizer may remain.

### Minimal Paper Mechanics

- There is a parameterized model to train.
- Labels that would be "unobserved" in the model are known in the supervised dataset.
- A cup turns that known unobserved label surface into an observed surface.
- Both data and labels become observed.
- The inversion often trivializes because the prior is deterministic data.
- The resulting loss depends on parameters and paired data.
- The regularizer may still matter.

### Arcanum Mental Model

The cup is a boundary-shift operator.

It says: this thing would normally be hidden or inferred, but in this training situation it is supplied as evidence. In Arcanum terms, that is like turning a normally internal state into an explicit receipt because the operator has ground-truth data for it.

```text
normally hidden label
  + supervised dataset
  -> observed training receipt
```

### Misuse Warning

Do not translate "cup" as just "attach labels." The paper's point is formal: cups and caps bend unobserved and observed spaces in the open-model calculus. The supervised-learning example is one application of that boundary move.

## Example A.5 - Bayesian Deep Learning

### What It Demonstrates

The Bayesian deep-learning example combines supervised-learning structure with a prior over neural-network weights. It shows that both the prediction model and the weight prior can be complex compositional models, while optimization may target posterior parameters over the weights.

Source basis: Appendix A.5 extends supervised learning and VBEM: a model has a neural-network-like forward component with weights and stochastic predictions, the energy may be a complex machine-learning loss, there is a prior over weights, and a mean-field factorization can leave a posterior over weights to optimize.

### Minimal Paper Mechanics

- Begin with a supervised-learning-shaped model.
- Include weights in the model.
- The forward component can be a neural network.
- Predictions are stochastic.
- The energy can be a complex ML loss.
- Add a prior over the weights.
- If the inversion factorizes mean-field over labels/data and weights, the label/data factor can be trivialized by the cup.
- The remaining posterior over weights is optimized.
- Both the forward model and the prior can themselves be compositionally constructed.

### Arcanum Mental Model

This is the "local structure does not disappear just because the component is large" example.

A neural network can sit inside AutoBayes as a forward component, but the framework still asks: where is the prior, where is the inversion, where is the local energy, where is the regularizer, and what parameter/posterior handle is exposed?

For Arcanum: even a powerful runtime component should not erase boundary discipline.

```text
large learned component
  still needs declared prior / evidence / inversion / parameter boundary
```

### Misuse Warning

Do not read AutoBayes as replacing deep-learning training loops with a fully specified implementation. The paper explicitly leaves implementation for future work. This example identifies how Bayesian deep-learning objects fit the framework, not a ready optimizer.

## Appendix B - Dependently Typed Model Example

### What It Demonstrates

Appendix B demonstrates that AutoBayes can model cases where the output space depends on the input value. The example is a weather-report model: a report for a sea location may need tide and wind fields that are irrelevant or undefined on land.

Source basis: Appendix B contrasts ordinary joint distributions over product spaces with dependently typed models over dependent sums. It says dependent types can enforce structural differences in the output type, saving the model from learning those differences from data.

### Minimal Paper Mechanics

- A simply typed joint distribution ranges over a product space.
- A dependently typed model lets the output space vary with the input.
- Instead of one fixed product space, the joint distribution ranges over a dependent sum.
- The weather-report example has location as input and report type as output family.
- Sea locations and land locations can have different valid report fields.
- The type structure carries domain knowledge before learning.

### Arcanum Mental Model

This is the strongest appendix warning against "one schema fits all."

In Arcanum terms, a handoff schema may need to depend on the target region of the problem. If the branch is "sea," the valid fields differ from "land." The point is not optional metadata; the type itself changes with the input.

```text
input value chooses the valid output shape
```

This rhymes with Arcanum's boundary/evidence contracts: the legal receipt shape can depend on the declared state namespace or route branch.

### Misuse Warning

Do not treat dependent typing as ordinary conditional validation bolted on afterward. The paper's claim is stronger: the output space is input-indexed, so invalid fields are excluded structurally rather than learned or checked late.

## Cross-Example Synthesis

Across the appendix examples, AutoBayes is showing one repeated pattern:

```text
familiar learning case
  -> identify open-model structure
  -> attach inversion/lens where needed
  -> split energy from entropy/regularizer
  -> expose only the legitimate parameter handle
  -> choose optimization semantics after syntax is declared
```

For Arcanum, the safest translation is:

```text
Do not let a familiar workflow become a monolith.
Break it into declaration, reverse/evidence behavior, local objective pressure,
authorized knobs, and runtime semantics.
```

## Borrow / Block / Analogy-Only Notes

| Candidate | Status | Reason |
| --- | --- | --- |
| Parameter exposure as authorized optimization handle | `borrow-candidate` | Strong fit with Arcanum authority boundaries, but needs local vocabulary decision. |
| Cup as boundary-shift analogy | `analogy-only` | Useful for supervised learning and observed/unobserved flips, but mathematically specific. |
| Dependent output shape | `borrow-candidate` | Useful for evidence schemas that depend on route branch or state namespace. |
| EM as task-session analogy | `analogy-only` | Helpful for separating evidence frame from mutation, but not the same formal object. |
| Bayesian deep-learning example as implementation recipe | `block` | The paper is framework-level and leaves implementation for future work. |

## Open Residue

- Work one example in notation from open model to lens to statistical game to exposed parameter.
- Add a diagram card for cups/caps/reveal/copier using the supervised-learning example as anchor.
- Create a parameter-exposure card that distinguishes mixture weights, EM parameters, VBEM priors, and posterior parameters over neural weights.
- Decide whether dependent receipt shapes belong in Arcanum as a glossary term, a validator pattern, or only a research analogy.

