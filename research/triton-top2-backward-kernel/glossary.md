# Glossary

This glossary is written for two jobs:

1. explain the challenge without pretending the math is already solved;
2. make prior-art and novelty conversations safer.

**Router logits** - The matrix `Z = X W^T`; each token/input row receives one score per expert.

**Router probabilities** - `P = softmax(Z)` over experts for each token.

**Softmax** - A function that turns raw scores into positive weights that add
up to 1. In this challenge, each row of `Z = X W^T` becomes a probability-like
row `P`. Plainly: softmax says "which routes look strongest, and by how much?"

**Logits** - Raw scores before softmax. Logits are not probabilities yet; they
can be negative, positive, large, or small. Here the logits are `Z`.

**Backward pass** - The training step that moves from the loss back through the
computation graph to compute gradients. If the forward pass asks "what output do
we get?", the backward pass asks "which inputs/weights caused this error, and in
which direction should they change?"

**Gradient** - A slope or sensitivity. A gradient tells us how much a small
change in one value changes the loss. Training uses gradients to update weights.

**Softmax backward** - The derivative rule for sending gradients through
softmax. For one row, if `P = softmax(Z)`, the usual vector-Jacobian product is
`dZ_j = P_j * (dP_j - sum_k P_k * dP_k)`. This is one of the clean math
identities we can test in PyTorch and prove over real numbers in Lean.

**Router** - The part of a model that decides which expert, latent space, or route should process an input.

**Expert** - One candidate computation path. In MoE systems, experts are often feed-forward networks. In a more general latent-space reading, an expert can be one representational route.

**FFN** - Feed-forward network. In this tower, `FFN(X)` is usually treated as
precomputed expert output `H`, so the router backward problem can focus on
`W`, `X`, logits, probabilities, and route weights.

**Latent space** - A hidden representation space where the model organizes information. In this challenge, "routing between latent spaces" means deciding which hidden computational route should influence the output.

**Mixture** - A weighted combination of multiple expert outputs. A soft mixture uses many experts; a sparse mixture uses only a few.

**Mixture weights** - The numbers used to combine route/expert outputs. In the
plain bridge, the flow is `request/input -> route scores -> mixture weights ->
combined output`.

**Combined output** - The result after weighted expert outputs are added
together. In notation, this is often `Y_t = sum_j A_tj H_tj`.

**Top-2 routing** - A sparse routing rule that keeps only the two selected experts per token. It is efficient, but the selection itself is a hard/discrete operation.

**Top2 / Top-2** - The operation "keep the best two." If applied to router
probabilities, it selects the two highest-scoring experts for each token. The
selection is useful for sparse computation, but the identity of "the best two"
can change suddenly when scores are close.

**Hard selection** - A discrete choice such as `argmax`, `top2`, sorting, or
thresholding. Hard selections are usually where gradients become unsafe or
undefined.

**Soft routing** - Routing that keeps continuous weights instead of a hard
choice. Full softmax routing can be differentiable, but it may route through all
experts instead of only two.

**Sparse routing** - Routing that uses only a small number of experts for each
token. Hard Top2 is sparse. Some continuous relaxations try to be sparse or
sparse-ish while remaining trainable.

**Top-2 mask** - A binary indicator saying which two experts were selected. If
`M_tj = 1`, expert `j` is selected for token `t`; if `M_tj = 0`, it is not.

**Combine weights (`A`)** - The route weights after applying the Top2 decision
or relaxation. In the current V0 baseline, `A = M * P`, meaning selected
softmax probabilities are kept and unselected probabilities become zero.

**Nondifferentiable** - A function is nondifferentiable at a point when it has no well-defined local slope/gradient there. Hard choices such as `top2`, `argmax`, thresholding, and sorting can jump when two scores swap order, so standard backpropagation cannot pass an exact gradient through the choice itself.

**Differentiable** - Smooth enough for gradients to tell the model how a small input change affects the output. Differentiability is what lets backpropagation train a component directly.

**Continuous relaxation** - A smooth or gradient-friendly replacement for a hard choice. Instead of "pick exactly these two experts," a relaxation gives soft/sparse weights that can change gradually.

**Surrogate** - A substitute objective or operation used because the original operation is hard to optimize. A surrogate can be useful even when it is not identical to the original.

**Straight-through estimator** - A trick where the forward pass uses a hard choice, but the backward pass pretends a smoother operation was used. Useful in practice, but not an exact mathematical gradient of the hard choice.

**Fixed-mask backward** - A compromise where the forward pass chooses top-2 experts, saves the mask, and the backward pass treats that mask as constant. This gives exact gradients after the choice, but not through the choice.

**Exact backward** - Exact gradients for the chosen differentiable computation graph. It cannot mean exact gradients through hard top-2 indices at discontinuities unless a subgradient or surrogate is explicitly defined.

**Exact for the surrogate** - The safe reading of "exact backward" in this
challenge. Once we choose fixed-mask Top2, relaxed Top2, or another named
bridge, the backward pass can be exact for that chosen graph. It is not exact
for an unspecified hard Top2 choice.

**Zero-allocation kernel** - A kernel path whose hot operation does not allocate intermediate device tensors for logits, softmax probabilities, masks, or partial gradient buffers; it writes only caller-provided outputs/scratch if scratch is explicitly part of the contract.

**Triton** - A Python-based language and compiler for writing custom GPU
kernels. Here it is the tool for fusing router backward math so we avoid
materializing large intermediate tensors.

**Kernel** - A small program executed many times in parallel on a GPU. A Triton
kernel is the GPU-side implementation of a chunk of the computation.

**CUDA** - NVIDIA's GPU programming platform/runtime. Triton compiles down to
GPU code that runs through the CUDA stack on NVIDIA GPUs.

**FP16** - 16-bit floating point. It uses less memory and can be faster on GPUs,
but it has less precision and smaller safe numeric range than FP32. FP16 makes
overflow, underflow, rounding error, and tolerance choices important.

**FP32 accumulation** - A common mixed-precision tactic: store inputs/outputs in
FP16, but do reductions and sensitive sums in FP32. This is important for
softmax rows, dot products, and gradient reductions.

**Mixed precision** - Using more than one numeric precision in the same
computation, such as FP16 inputs with FP32 accumulators.

**Numerical tolerance** - The acceptable error margin when comparing FP16/Triton
results against a reference. FP16 will not match ideal real-number math exactly,
so tests need explicit tolerances.

**Overflow** - When a number is too large for the format and becomes infinity or
an invalid value. Stable softmax usually subtracts the row maximum before
calling `exp` to reduce overflow risk.

**Underflow** - When a number is too small for the format and rounds to zero.
This can erase tiny probabilities or gradients in FP16.

**Load-balancing loss** - Auxiliary MoE router loss encouraging experts to receive balanced traffic.

**Load fraction (`f_j`)** - The fraction of tokens assigned to expert `j`.
If this is a hard count from Top2 selections, it is not differentiable unless we
replace it with a relaxed load.

**Mean router probability (`P_j`)** - The average softmax probability assigned
to expert `j` across tokens. In the auxiliary loss, it is paired with `f_j`.

**Capacity constraint** - A maximum allowed fraction of tokens per expert; here `2.1 / E`.

**Capacity overflow** - A case where some expert receives more traffic than the
allowed cap. A backward kernel can detect or penalize this only if the contract
says how capacity is represented.

**Prior art** - Existing published or known solutions that already attack a similar problem. Prior art is not "the answer we must copy"; it is the map of what has already been tried, so we can avoid claiming novelty where the literature already exists.

**Novelty** - The part of a solution that is meaningfully new relative to prior art. For this challenge, novelty is unlikely to be "a differentiable top-k exists." Prior art already covers that. A more plausible novelty target is a specific relaxation/backward/kernel combination that is simpler, more testable, more capacity-aware, or better suited to zero-allocation FP16 Triton.

**Contribution** - The claim we would make if we invented something. Good contribution statements are narrow: "we propose X under assumptions Y, and it improves Z compared with baselines A/B/C."

**Baseline** - A known reference solution used for comparison. Here likely baselines include fixed-mask top-2, soft routing, sparsemax/entmax, SOFT top-k, convex sparse top-k, and ReLU routing.

**Oracle** - A trusted reference implementation used for testing. A PyTorch reference can act as an oracle for a Triton kernel.

**Relaxation candidate** - One possible way to make hard `Top2` trainable. Candidates include soft routing, sparsemax/entmax, SOFT top-k, convex sparse top-k, Gumbel top-k, and ReLU MoE routing.

**Capacity-aware routing** - Routing that accounts for expert load limits. It can be a hard gate, an assignment rule, a penalty, a barrier, or a differentiable load-balancing term.

**Proof target** - A precise theorem we want a formal system such as Lean to validate. Example: the softmax backward identity or `dW = dZ^T X`.

**Lean** - A theorem prover. In this project, Lean can validate ideal
real-number math identities, such as softmax derivative formulas. Lean does not
by itself validate FP16 behavior, Triton compilation, GPU memory allocation, or
performance.

**Gradcheck** - A test that compares analytic gradients against numerical
finite-difference estimates. It is useful for smooth reference graphs and helps
catch backward-pass mistakes before writing a GPU kernel.

**Finite differences** - A numerical way to estimate a derivative by slightly
perturbing an input and measuring how the output changes.

**PyTorch reference / oracle** - A clear, executable implementation used as the
truth source for tests. The Triton kernel should match this reference within
declared tolerances.

**Kernel-friendly** - Suitable for efficient GPU implementation. A kernel-friendly relaxation uses row-local math, simple reductions, limited branching, stable FP16 behavior, and no large temporary tensors.

## Pending Glossary / Contract Terms

These terms are known sources of confusion and should stay visible until the
math contract fully settles:

**Top-2 combine semantics** - Whether `A` means `M * P` or normalized selected
probabilities `M * P / sum(M * P)`. These have different backward equations.

**Continuous relaxation identity** - The exact smooth substitute for hard Top2.
Candidates include fixed-mask Top2, soft routing, sparsemax/entmax-like routing,
convex sparse top-k, SOFT top-k, Gumbel top-k, and straight-through variants.

**Exact 2-sparsity** - Whether the training-time relaxation must always keep
exactly two active experts, or whether "sparse-ish" differentiable routing is
acceptable.

**Saved mask/gates** - Whether the backward pass receives the forward-selected
top-2 indices and gates, or recomputes them. Saved values are safer because ties
and near-ties can make recomputation disagree with forward.

**Dynamic load gradient** - Whether gradients should flow through `f_j`.
For V0, `f_j` is fixed/hard and not differentiated. A later relaxed-load design
would need its own definition and proof/test target.

**Capacity behavior** - Whether capacity is only checked, enforced by routing,
penalized, or relaxed through a differentiable barrier. Each choice changes what
the kernel is responsible for.

**Target GPU/Triton version** - The hardware and software environment used for
performance and FP16 claims. These details affect atomics, block sizes,
available dtypes, and expected tolerance.

**Full FFN backward scope** - Whether the challenge asks only for router
gradients (`dW`, router-side `dX`) with `H = FFN(X)` precomputed, or also for
gradients through expert FFN parameters.

**Zero allocation boundary** - Whether "zero allocation" applies only inside
the hot Triton kernel, to the Python wrapper too, or to the entire training
step. The current tower treats the hot backward path as the core boundary.

**FP16 behavior proof boundary** - Real-number proofs and FP16 GPU behavior are
different validation layers. Lean can help with ideal formulas; FP16 behavior
needs reference parity, tolerance tests, and hardware runs.
