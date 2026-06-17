"""PyTorch reference for the fixed-mask Top2 router objective.

This module mirrors ``router_reference.py`` while leaving the saved Top2 mask as
fixed input data. Autograd is used only for the continuous path through
softmax/logits, masked probabilities, expert outputs, and the auxiliary term.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

import torch

from reference.router_reference import (
    Matrix,
    RouterContract,
    Tensor3,
    _isotonic_l4_mask_pav_1d,
    fixture,
)


TensorTuple = Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]


def tensors_from_fixture(
    *,
    dtype: torch.dtype = torch.float64,
    device: torch.device | str = "cpu",
    requires_grad_w: bool = False,
    requires_grad_h: bool = False,
) -> TensorTuple:
    """Return the standard fixture as tensors for PyTorch parity tests."""

    x, w, h, m, f = fixture()
    return tensors_from_values(
        x,
        w,
        h,
        m,
        f,
        dtype=dtype,
        device=device,
        requires_grad_w=requires_grad_w,
        requires_grad_h=requires_grad_h,
    )


def tensors_from_values(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    m: Matrix,
    f: Sequence[float],
    *,
    dtype: torch.dtype = torch.float64,
    device: torch.device | str = "cpu",
    requires_grad_w: bool = False,
    requires_grad_h: bool = False,
) -> TensorTuple:
    x_t = torch.tensor(x, dtype=dtype, device=device)
    w_t = torch.tensor(w, dtype=dtype, device=device, requires_grad=requires_grad_w)
    h_t = torch.tensor(h, dtype=dtype, device=device, requires_grad=requires_grad_h)
    m_t = torch.tensor(m, dtype=dtype, device=device)
    f_t = torch.tensor(f, dtype=dtype, device=device)
    return x_t, w_t, h_t, m_t, f_t


def fixed_mask_top2_torch(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    m: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    contract: RouterContract | None = None,
) -> Dict[str, torch.Tensor]:
    """Run the V0 fixed-mask objective with differentiable PyTorch ops."""

    contract = contract or RouterContract()
    contract.validate()
    _assert_tensor_shapes(x, w, h, m, f)

    z = x @ w.transpose(0, 1)
    p = torch.softmax(z, dim=-1)
    a = p * m
    y = torch.einsum("te,ted->td", a, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = p.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)

    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "p": p,
        "a": a,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


def sparsemax_torch(z: torch.Tensor, *, dim: int = -1) -> torch.Tensor:
    """Sparsemax projection over one tensor dimension."""

    z_sorted, _ = torch.sort(z, descending=True, dim=dim)
    z_cumsum = torch.cumsum(z_sorted, dim=dim)
    rhos = torch.arange(1, z.shape[dim] + 1, dtype=z.dtype, device=z.device)
    view_shape = [1 for _ in z.shape]
    view_shape[dim] = z.shape[dim]
    rhos = rhos.view(view_shape)
    support = 1 + rhos * z_sorted > z_cumsum
    support_size = support.sum(dim=dim, keepdim=True).to(dtype=z.dtype)
    support_sum = (z_sorted * support.to(dtype=z.dtype)).sum(dim=dim, keepdim=True)
    tau = (support_sum - 1) / support_size
    return torch.clamp(z - tau, min=0)


def sparsemax_routing_torch(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
) -> Dict[str, torch.Tensor]:
    """Run a sparsemax routing baseline without a Top2 mask."""

    m = torch.ones((x.shape[0], w.shape[0]), dtype=x.dtype, device=x.device)
    _assert_tensor_shapes(x, w, h, m, f)

    z = x @ w.transpose(0, 1)
    p = sparsemax_torch(z, dim=-1)
    y = torch.einsum("te,ted->td", p, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = p.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)

    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "p": p,
        "a": p,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


def cap2_routing_weights_torch(
    z: torch.Tensor,
    load: torch.Tensor,
    *,
    tau_rank: float = 0.5,
    tau_gate: float = 0.5,
    tau_cap: float = 0.25,
    mu: float = 1.0,
    epsilon: float = 1e-12,
) -> Dict[str, torch.Tensor]:
    """CAP2-v0 routing weights from capacity-adjusted pairwise soft rank."""

    if z.ndim != 2:
        raise ValueError("z must have shape [T, E]")
    if load.ndim != 1 or load.shape[0] != z.shape[1]:
        raise ValueError("load must have shape [E]")
    if tau_rank <= 0.0:
        raise ValueError("tau_rank must be positive")
    if tau_gate <= 0.0:
        raise ValueError("tau_gate must be positive")
    if tau_cap <= 0.0:
        raise ValueError("tau_cap must be positive")
    if mu < 0.0:
        raise ValueError("mu must be non-negative")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")

    capacity = z.new_tensor(2.1 / z.shape[1])
    overload = torch.sigmoid((load - capacity) / tau_cap)
    z_adjusted = z - z.new_tensor(mu) * overload
    p = torch.softmax(z_adjusted, dim=-1)
    pairwise = torch.sigmoid((z_adjusted.unsqueeze(-1) - z_adjusted.unsqueeze(-2)) / tau_rank)
    eye = torch.eye(z.shape[1], dtype=torch.bool, device=z.device)
    soft_rank = pairwise.masked_fill(eye.unsqueeze(0), 0.0).sum(dim=-1)
    threshold = z.new_tensor(z.shape[1] - 2 - 0.5)
    membership = torch.sigmoid((soft_rank - threshold) / tau_gate)
    gated = membership * p
    a = gated / (z.new_tensor(epsilon) + gated.sum(dim=-1, keepdim=True))
    return {
        "z_adjusted": z_adjusted,
        "overload": overload,
        "capacity": capacity,
        "p": p,
        "soft_rank": soft_rank,
        "membership": membership,
        "gated": gated,
        "a": a,
    }


def cap2_routing_torch(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    load: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    tau_rank: float = 0.5,
    tau_gate: float = 0.5,
    tau_cap: float = 0.25,
    mu: float = 1.0,
    epsilon: float = 1e-12,
) -> Dict[str, torch.Tensor]:
    """Run CAP2-v0 with fixed load and differentiable router logits."""

    m = torch.ones((x.shape[0], w.shape[0]), dtype=x.dtype, device=x.device)
    _assert_tensor_shapes(x, w, h, m, f)
    if load.ndim != 1 or load.shape[0] != w.shape[0]:
        raise ValueError("load must have shape [E]")

    z = x @ w.transpose(0, 1)
    cap2 = cap2_routing_weights_torch(
        z,
        load,
        tau_rank=tau_rank,
        tau_gate=tau_gate,
        tau_cap=tau_cap,
        mu=mu,
        epsilon=epsilon,
    )
    a = cap2["a"]
    p = cap2["p"]
    y = torch.einsum("te,ted->td", a, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = p.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)
    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "z_adjusted": cap2["z_adjusted"],
        "overload": cap2["overload"],
        "capacity": cap2["capacity"],
        "p": p,
        "soft_rank": cap2["soft_rank"],
        "membership": cap2["membership"],
        "gated": cap2["gated"],
        "a": a,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


def cap2_manual_backward(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    load: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    tau_rank: float = 0.5,
    tau_gate: float = 0.5,
    tau_cap: float = 0.25,
    mu: float = 1.0,
    epsilon: float = 1e-12,
) -> Dict[str, torch.Tensor]:
    """Manual VJP for the smooth CAP2-v0 graph with fixed load."""

    m = torch.ones((x.shape[0], w.shape[0]), dtype=x.dtype, device=x.device)
    _assert_tensor_shapes(x, w, h, m, f)
    if w.shape[0] < 2:
        raise ValueError("CAP2 requires at least two experts")
    if load.ndim != 1 or load.shape[0] != w.shape[0]:
        raise ValueError("load must have shape [E]")
    if tau_rank <= 0.0:
        raise ValueError("tau_rank must be positive")
    if tau_gate <= 0.0:
        raise ValueError("tau_gate must be positive")
    if tau_cap <= 0.0:
        raise ValueError("tau_cap must be positive")
    if mu < 0.0:
        raise ValueError("mu must be non-negative")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")

    z = x @ w.transpose(0, 1)
    capacity = z.new_tensor(2.1 / w.shape[0])
    overload = torch.sigmoid((load - capacity) / tau_cap)
    z_adjusted = z - z.new_tensor(mu) * overload
    p = torch.softmax(z_adjusted, dim=-1)
    pairwise = torch.sigmoid((z_adjusted.unsqueeze(-1) - z_adjusted.unsqueeze(-2)) / tau_rank)
    eye = torch.eye(w.shape[0], dtype=torch.bool, device=z.device)
    pairwise_offdiag = pairwise.masked_fill(eye.unsqueeze(0), 0.0)
    soft_rank = pairwise_offdiag.sum(dim=-1)
    threshold = z.new_tensor(w.shape[0] - 2 - 0.5)
    membership = torch.sigmoid((soft_rank - threshold) / tau_gate)
    gated = membership * p
    normalizer = z.new_tensor(epsilon) + gated.sum(dim=-1, keepdim=True)
    a = gated / normalizer
    y = torch.einsum("te,ted->td", a, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = p.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)

    d_y = x.new_tensor(2.0 * lambda_rec) * residual
    d_a = torch.einsum("td,ted->te", d_y, h)
    d_h = a.unsqueeze(-1) * d_y.unsqueeze(1)

    contraction = torch.sum(d_a * gated, dim=-1, keepdim=True)
    d_gated = (d_a * normalizer - contraction) / (normalizer * normalizer)
    d_membership = d_gated * p
    d_p = d_gated * membership
    d_p = d_p + x.new_tensor(gamma) * x.new_tensor(w.shape[0] / x.shape[0]) * f.unsqueeze(0)

    softmax_dot = torch.sum(d_p * p, dim=-1, keepdim=True)
    d_u_softmax = p * (d_p - softmax_dot)

    d_soft_rank = d_membership * membership * (1.0 - membership) / tau_gate
    rank_factor = pairwise * (1.0 - pairwise) / tau_rank
    rank_factor = rank_factor.masked_fill(eye.unsqueeze(0), 0.0)
    rank_messages = d_soft_rank.unsqueeze(-1) * rank_factor
    d_u_rank = rank_messages.sum(dim=-1) - rank_messages.sum(dim=-2)

    d_z = d_u_softmax + d_u_rank
    d_w = d_z.transpose(0, 1) @ x
    d_x_router = d_z @ w

    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "z_adjusted": z_adjusted,
        "overload": overload,
        "capacity": capacity,
        "p": p,
        "pairwise": pairwise,
        "soft_rank": soft_rank,
        "membership": membership,
        "gated": gated,
        "normalizer": normalizer,
        "a": a,
        "y": y,
        "residual": residual,
        "pbar": pbar,
        "d_y": d_y,
        "d_a": d_a,
        "d_h": d_h,
        "d_gated": d_gated,
        "d_membership": d_membership,
        "d_p": d_p,
        "d_u_softmax": d_u_softmax,
        "d_soft_rank": d_soft_rank,
        "d_u_rank": d_u_rank,
        "d_z": d_z,
        "d_w": d_w,
        "d_x_router": d_x_router,
    }


def convex_sparse_topk_mask_torch(
    z: torch.Tensor,
    *,
    k: int = 2,
    lambda_smooth: float = 1e-2,
) -> torch.Tensor:
    """Source-backed PyTorch custom-autograd oracle for PAV p=4/3 masks.

    This is a CPU/reference parity operator. It follows the official
    sparse-soft-top-k PAV mask composition with stopped-gradient sorting and a
    custom backward for the isotonic PAV subproblem.
    """

    if z.ndim != 2:
        raise ValueError("z must have shape [T, E]")
    return _ConvexSparseTopKMaskPAV.apply(z, k, float(lambda_smooth))


def convex_topk_mask_direct_torch(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    k: int = 2,
    lambda_smooth: float = 1e-2,
) -> Dict[str, torch.Tensor]:
    """Use the relaxed sparse top-k mask directly as router weights."""

    m = torch.ones((x.shape[0], w.shape[0]), dtype=x.dtype, device=x.device)
    _assert_tensor_shapes(x, w, h, m, f)

    z = x @ w.transpose(0, 1)
    mask = convex_sparse_topk_mask_torch(z, k=k, lambda_smooth=lambda_smooth)
    y = torch.einsum("te,ted->td", mask, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = mask.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)

    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "relaxed_mask": mask,
        "p": mask,
        "a": mask,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


class _ConvexSparseTopKMaskPAV(torch.autograd.Function):
    @staticmethod
    def forward(ctx, z: torch.Tensor, k: int, lambda_smooth: float) -> torch.Tensor:  # type: ignore[override]
        if not z.is_floating_point():
            raise ValueError("z must be floating point")
        if z.device.type != "cpu":
            raise ValueError("convex sparse top-k PAV oracle is CPU-only")
        if k <= 0:
            raise ValueError("k must be positive")
        if lambda_smooth <= 0.0:
            raise ValueError("lambda_smooth must be positive")
        if k > z.shape[-1]:
            raise ValueError("k must be no larger than the row length")

        masks: List[torch.Tensor] = []
        sorted_scores: List[torch.Tensor] = []
        isotonic_solutions: List[torch.Tensor] = []
        orders: List[torch.Tensor] = []
        weights = [1.0 if idx < k else 0.0 for idx in range(z.shape[-1])]

        for row in z.detach():
            order = torch.argsort(row, descending=True)
            sorted_row = row[order].contiguous()
            isotonic = _isotonic_l4_mask_pav_1d(sorted_row.tolist(), weights, lambda_smooth)
            isotonic_t = torch.tensor(isotonic, dtype=z.dtype, device=z.device)
            sorted_mask = ((sorted_row - isotonic_t) / lambda_smooth) ** 3
            mask = torch.zeros_like(row)
            mask.scatter_(0, order, torch.clamp(sorted_mask, min=0.0))
            masks.append(mask)
            sorted_scores.append(sorted_row)
            isotonic_solutions.append(isotonic_t)
            orders.append(order)

        ctx.lambda_smooth = lambda_smooth
        ctx.save_for_backward(
            torch.stack(sorted_scores),
            torch.stack(isotonic_solutions),
            torch.stack(orders),
        )
        return torch.stack(masks)

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None, None]:  # type: ignore[override]
        sorted_scores, isotonic_solutions, orders = ctx.saved_tensors
        lambda_smooth = ctx.lambda_smooth
        grad_z = torch.zeros_like(grad_output)

        for row_idx in range(grad_output.shape[0]):
            order = orders[row_idx]
            upstream_sorted = grad_output[row_idx][order]
            s = sorted_scores[row_idx]
            v = isotonic_solutions[row_idx]
            alpha = 3.0 * (s - v) ** 2 / (lambda_smooth**3)
            vector = alpha * upstream_sorted
            sorted_grad = vector - _isotonic_pav_vjp_p43(s, v, vector)
            grad_z[row_idx].scatter_(0, order, sorted_grad)

        return grad_z, None, None


def _isotonic_pav_vjp_p43(
    sorted_scores: torch.Tensor,
    isotonic_solution: torch.Tensor,
    vector: torch.Tensor,
) -> torch.Tensor:
    """Official PAV VJP specialization for p=4/3, q=4."""

    diff = torch.abs(isotonic_solution - sorted_scores) ** 2
    out = torch.zeros_like(vector)
    start = 0
    n = vector.numel()
    while start < n:
        end = start + 1
        while end < n and bool(torch.abs(isotonic_solution[end] - isotonic_solution[end - 1]) <= 1e-9):
            end += 1
        denom = diff[start:end].sum() + sorted_scores.new_tensor(1e-15)
        out[start:end] = diff[start:end] * vector[start:end].sum() / denom
        start = end
    return out


def normalized_relu_torch(z: torch.Tensor, *, dim: int = -1) -> torch.Tensor:
    positive = torch.relu(z)
    denom = positive.sum(dim=dim, keepdim=True)
    if bool(torch.any(denom <= 0)):
        raise ValueError("ReLU routing row must have at least one positive logit")
    return positive / denom


def relu_routing_torch(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
) -> Dict[str, torch.Tensor]:
    """Run a normalized ReLU routing baseline."""

    m = torch.ones((x.shape[0], w.shape[0]), dtype=x.dtype, device=x.device)
    _assert_tensor_shapes(x, w, h, m, f)

    z = x @ w.transpose(0, 1)
    p = normalized_relu_torch(z, dim=-1)
    y = torch.einsum("te,ted->td", p, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = p.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)

    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "p": p,
        "a": p,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


def normalized_pair_weight_torch(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    m: torch.Tensor,
    f: torch.Tensor,
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    contract: RouterContract | None = None,
) -> Dict[str, torch.Tensor]:
    """Run the selected-pair renormalized comparison objective."""

    contract = contract or RouterContract()
    contract.validate()
    _assert_tensor_shapes(x, w, h, m, f)

    z = x @ w.transpose(0, 1)
    p = torch.softmax(z, dim=-1)
    masked = p * m
    denom = masked.sum(dim=-1, keepdim=True)
    if bool(torch.any(denom <= 0)):
        raise ValueError("masked probabilities must have positive row sum")
    a = masked / denom
    y = torch.einsum("te,ted->td", a, h)
    residual = y - x
    l_rec = x.new_tensor(lambda_rec) * torch.sum(residual * residual)
    pbar = p.mean(dim=0)
    l_aux = x.new_tensor(gamma) * x.new_tensor(w.shape[0]) * torch.sum(f * pbar)

    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "p": p,
        "masked": masked,
        "a": a,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


def _assert_tensor_shapes(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    m: torch.Tensor,
    f: torch.Tensor,
) -> None:
    if x.ndim != 2:
        raise ValueError("X must have shape [T, D]")
    if w.ndim != 2:
        raise ValueError("W must have shape [E, D]")
    if h.ndim != 3:
        raise ValueError("H must have shape [T, E, D]")
    if m.ndim != 2:
        raise ValueError("M must have shape [T, E]")
    if f.ndim != 1:
        raise ValueError("f must have shape [E]")

    t, d = x.shape
    e = w.shape[0]
    if t == 0:
        raise ValueError("X must contain at least one token")
    if e == 0:
        raise ValueError("W must contain at least one expert")
    if w.shape[1] != d:
        raise ValueError("W rows must match X feature dimension")
    if h.shape != (t, e, d):
        raise ValueError("H must have shape [T, E, D]")
    if m.shape != (t, e):
        raise ValueError("M must have shape [T, E]")
    if f.shape[0] != e:
        raise ValueError("f must have length E")
