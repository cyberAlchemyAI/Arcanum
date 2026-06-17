"""Small reference implementation for the fixed-mask Top2 router objective.

This module intentionally uses only the Python standard library so it can run in
the research tree before PyTorch/Triton dependencies are available. It is not a
performance implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import acos, cos, exp, sqrt
from typing import Dict, List, Sequence, Tuple


Matrix = List[List[float]]
Tensor3 = List[List[List[float]]]


@dataclass(frozen=True)
class RouterContract:
    sigma: str = "softmax"
    reconstruction_weight: str = "lambda_rec"
    ffn_scope: str = "precomputed_h"
    combine: str = "masked_probability"
    capacity_mode: str = "check_only"
    mask_source: str = "saved_forward_mask"
    f_gradient: str = "fixed_no_gradient"
    relaxation: str = "fixed_mask_baseline"

    def validate(self) -> None:
        expected = {
            "sigma": "softmax",
            "reconstruction_weight": "lambda_rec",
            "ffn_scope": "precomputed_h",
            "combine": "masked_probability",
            "capacity_mode": "check_only",
            "mask_source": "saved_forward_mask",
            "f_gradient": "fixed_no_gradient",
            "relaxation": "fixed_mask_baseline",
        }
        actual = {
            "sigma": self.sigma,
            "reconstruction_weight": self.reconstruction_weight,
            "ffn_scope": self.ffn_scope,
            "combine": self.combine,
            "capacity_mode": self.capacity_mode,
            "mask_source": self.mask_source,
            "f_gradient": self.f_gradient,
            "relaxation": self.relaxation,
        }
        mismatches = [
            f"{key}={actual[key]!r} expected {value!r}"
            for key, value in expected.items()
            if actual[key] != value
        ]
        if mismatches:
            raise ValueError("Unsupported or unresolved router contract: " + "; ".join(mismatches))


def assert_shapes(x: Matrix, w: Matrix, h: Tensor3, m: Matrix, f: Sequence[float]) -> None:
    t = len(x)
    if t == 0:
        raise ValueError("X must contain at least one token")
    d = len(x[0])
    e = len(w)
    if e == 0:
        raise ValueError("W must contain at least one expert")
    if any(len(row) != d for row in x):
        raise ValueError("X rows must have consistent feature dimension")
    if any(len(row) != d for row in w):
        raise ValueError("W rows must match X feature dimension")
    if len(h) != t or any(len(h_t) != e for h_t in h):
        raise ValueError("H must have shape [T][E][D]")
    if any(len(h_tj) != d for h_t in h for h_tj in h_t):
        raise ValueError("H expert outputs must match X feature dimension")
    if len(m) != t or any(len(row) != e for row in m):
        raise ValueError("M must have shape [T][E]")
    if len(f) != e:
        raise ValueError("f must have length E")


def matmul_router_logits(x: Matrix, w: Matrix) -> Matrix:
    return [[sum(x_td * w_jd for x_td, w_jd in zip(x_t, w_j)) for w_j in w] for x_t in x]


def softmax_rows(z: Matrix) -> Matrix:
    rows: Matrix = []
    for row in z:
        max_z = max(row)
        exps = [exp(v - max_z) for v in row]
        denom = sum(exps)
        rows.append([v / denom for v in exps])
    return rows


def sigmoid(value: float) -> float:
    if value >= 0.0:
        z = exp(-value)
        return 1.0 / (1.0 + z)
    z = exp(value)
    return z / (1.0 + z)


def sparsemax_rows(z: Matrix) -> Matrix:
    rows: Matrix = []
    for row in z:
        sorted_row = sorted(row, reverse=True)
        cumsum = 0.0
        support_size = 0
        support_sum = 0.0
        for idx, value in enumerate(sorted_row, start=1):
            cumsum += value
            if 1.0 + idx * value > cumsum:
                support_size = idx
                support_sum = cumsum
        if support_size == 0:
            raise ValueError("sparsemax support must be non-empty")
        tau = (support_sum - 1.0) / support_size
        rows.append([max(value - tau, 0.0) for value in row])
    return rows


def cap2_adjusted_logits_rows(
    z: Matrix,
    load: Sequence[float],
    *,
    tau_cap: float = 0.25,
    mu: float = 1.0,
) -> Tuple[Matrix, List[float], float]:
    if tau_cap <= 0.0:
        raise ValueError("tau_cap must be positive")
    if mu < 0.0:
        raise ValueError("mu must be non-negative")
    if not z:
        raise ValueError("z must contain at least one row")
    e = len(z[0])
    if len(load) != e:
        raise ValueError("load must have length E")
    capacity = 2.1 / e
    overload = [sigmoid((load_j - capacity) / tau_cap) for load_j in load]
    adjusted = [[value - mu * overload[j] for j, value in enumerate(row)] for row in z]
    return adjusted, overload, capacity


def cap2_pairwise_soft_rank_rows(
    z_adjusted: Matrix,
    *,
    tau_rank: float = 0.5,
) -> Matrix:
    if tau_rank <= 0.0:
        raise ValueError("tau_rank must be positive")
    ranks: Matrix = []
    for row in z_adjusted:
        rank_row = []
        for j, value_j in enumerate(row):
            rank_row.append(sum(sigmoid((value_j - value_k) / tau_rank) for k, value_k in enumerate(row) if k != j))
        ranks.append(rank_row)
    return ranks


def cap2_membership_rows(
    soft_rank: Matrix,
    *,
    tau_gate: float = 0.5,
) -> Matrix:
    if tau_gate <= 0.0:
        raise ValueError("tau_gate must be positive")
    if not soft_rank:
        raise ValueError("soft_rank must contain at least one row")
    e = len(soft_rank[0])
    threshold = e - 2 - 0.5
    return [[sigmoid((rank_value - threshold) / tau_gate) for rank_value in row] for row in soft_rank]


def cap2_routing_weights_rows(
    z: Matrix,
    load: Sequence[float],
    *,
    tau_rank: float = 0.5,
    tau_gate: float = 0.5,
    tau_cap: float = 0.25,
    mu: float = 1.0,
    epsilon: float = 1e-12,
) -> Dict[str, object]:
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    z_adjusted, overload, capacity = cap2_adjusted_logits_rows(z, load, tau_cap=tau_cap, mu=mu)
    p = softmax_rows(z_adjusted)
    soft_rank = cap2_pairwise_soft_rank_rows(z_adjusted, tau_rank=tau_rank)
    membership = cap2_membership_rows(soft_rank, tau_gate=tau_gate)
    gated = [[g_tj * p_tj for g_tj, p_tj in zip(g_row, p_row)] for g_row, p_row in zip(membership, p)]
    a: Matrix = []
    for row in gated:
        denom = epsilon + sum(row)
        a.append([value / denom for value in row])
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


def convex_sparse_topk_mask_rows(
    z: Matrix,
    *,
    k: int = 2,
    lambda_smooth: float = 1e-2,
) -> Matrix:
    """Sparse soft top-k mask via the PAV p=4/3 path from Sander et al.

    This is a small standard-library extraction of the official
    ``sparse_soft_topk_mask_pav`` contract for p=4/3. It returns a sparse relaxed
    top-k mask, not a router combine rule.
    """

    if k <= 0:
        raise ValueError("k must be positive")
    if lambda_smooth <= 0.0:
        raise ValueError("lambda_smooth must be positive")

    masks: Matrix = []
    for row in z:
        n = len(row)
        if k > n:
            raise ValueError("k must be no larger than the row length")
        order = sorted(range(n), key=lambda idx: row[idx], reverse=True)
        sorted_scores = [row[idx] for idx in order]
        weights = [1.0 if idx < k else 0.0 for idx in range(n)]
        isotonic = _isotonic_l4_mask_pav_1d(sorted_scores, weights, lambda_smooth)
        sorted_mask = [((score - value) / lambda_smooth) ** 3 for score, value in zip(sorted_scores, isotonic)]
        mask = [0.0 for _ in row]
        for sorted_idx, original_idx in enumerate(order):
            mask[original_idx] = max(sorted_mask[sorted_idx], 0.0)
        masks.append(mask)
    return masks


def _isotonic_l4_mask_pav_1d(scores: Sequence[float], weights: Sequence[float], lmbda: float) -> List[float]:
    n = len(scores)
    target = list(range(n))
    solution = [scores[i] - lmbda * _signed_power(weights[i], 1.0 / 3.0) for i in range(n)]
    sums_a3 = [1.0 for _ in range(n)]
    sums_a2 = [-3.0 * value for value in scores]
    sums_a1 = [3.0 * value * value for value in scores]
    sums_a0 = [-(value**3) + (lmbda**3) * weight for value, weight in zip(scores, weights)]

    i = 0
    while i < n:
        next_block = target[i] + 1
        if next_block == n:
            break
        if solution[i] > solution[next_block]:
            i = next_block
            continue

        sum_a3 = sums_a3[i]
        sum_a2 = sums_a2[i]
        sum_a1 = sums_a1[i]
        sum_a0 = sums_a0[i]
        while True:
            previous_solution = solution[next_block]
            sum_a3 += sums_a3[next_block]
            sum_a2 += sums_a2[next_block]
            sum_a1 += sums_a1[next_block]
            sum_a0 += sums_a0[next_block]
            next_block = target[next_block] + 1
            if next_block == n or previous_solution > solution[next_block]:
                solution[i] = _solve_real_cubic_root(sum_a3, sum_a2, sum_a1, sum_a0)
                sums_a3[i] = sum_a3
                sums_a2[i] = sum_a2
                sums_a1[i] = sum_a1
                sums_a0[i] = sum_a0
                target[i] = next_block - 1
                target[next_block - 1] = i
                if i > 0:
                    i = target[i - 1]
                break

    i = 0
    while i < n:
        next_block = target[i] + 1
        for j in range(i + 1, next_block):
            solution[j] = solution[i]
        i = next_block
    return solution


def _solve_real_cubic_root(a: float, b: float, c: float, d: float) -> float:
    f_value = ((3.0 * c / a) - (b / a) ** 2) / 3.0
    g_value = (2.0 * (b / a) ** 3 - (9.0 * b * c) / (a * a) + 27.0 * d / a) / 27.0
    h_value = g_value * g_value / 4.0 + f_value**3 / 27.0
    if h_value < 0.0:
        i_value = sqrt((g_value * g_value / 4.0) - h_value)
        j_value = _signed_power(i_value, 1.0 / 3.0)
        k_value = acos(-g_value / (2.0 * i_value))
        return 2.0 * j_value * cos(k_value / 3.0) - (b / (3.0 * a))
    if h_value > 0.0:
        r_value = -(g_value / 2.0) + sqrt(h_value)
        s_value = _signed_power(r_value, 1.0 / 3.0)
        t_value = -(g_value / 2.0) - sqrt(h_value)
        u_value = _signed_power(t_value, 1.0 / 3.0)
        return s_value + u_value - (b / (3.0 * a))
    return -_signed_power(d / a, 1.0 / 3.0)


def _signed_power(value: float, power: float) -> float:
    if value == 0.0:
        return 0.0
    return (1.0 if value > 0.0 else -1.0) * (abs(value) ** power)


def normalized_relu_rows(z: Matrix) -> Matrix:
    rows: Matrix = []
    for row in z:
        positive = [max(value, 0.0) for value in row]
        denom = sum(positive)
        if denom <= 0.0:
            raise ValueError("ReLU routing row must have at least one positive logit")
        rows.append([value / denom for value in positive])
    return rows


def apply_mask(p: Matrix, m: Matrix) -> Matrix:
    return [[p_tj * m_tj for p_tj, m_tj in zip(p_t, m_t)] for p_t, m_t in zip(p, m)]


def normalize_masked_probabilities(a: Matrix) -> Matrix:
    normalized: Matrix = []
    for row in a:
        denom = sum(row)
        if denom <= 0.0:
            raise ValueError("masked probabilities must have positive row sum")
        normalized.append([value / denom for value in row])
    return normalized


def combine_outputs(a: Matrix, h: Tensor3) -> Matrix:
    y: Matrix = []
    for a_t, h_t in zip(a, h):
        d = len(h_t[0])
        y_t = [0.0 for _ in range(d)]
        for a_tj, h_tj in zip(a_t, h_t):
            for idx in range(d):
                y_t[idx] += a_tj * h_tj[idx]
        y.append(y_t)
    return y


def squared_residual_loss(y: Matrix, x: Matrix, lambda_rec: float) -> Tuple[float, Matrix]:
    residual = [[y_td - x_td for y_td, x_td in zip(y_t, x_t)] for y_t, x_t in zip(y, x)]
    loss = lambda_rec * sum(v * v for row in residual for v in row)
    return loss, residual


def mean_expert_probabilities(p: Matrix) -> List[float]:
    t = len(p)
    e = len(p[0])
    return [sum(p_t[j] for p_t in p) / t for j in range(e)]


def fixed_mask_top2_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    m: Matrix,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    contract: RouterContract | None = None,
) -> Dict[str, object]:
    contract = contract or RouterContract()
    contract.validate()
    assert_shapes(x, w, h, m, f)
    z = matmul_router_logits(x, w)
    p = softmax_rows(z)
    a = apply_mask(p, m)
    y = combine_outputs(a, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def soft_routing_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
) -> Dict[str, object]:
    assert_shapes(x, w, h, [[1.0 for _ in w] for _ in x], f)
    z = matmul_router_logits(x, w)
    p = softmax_rows(z)
    y = combine_outputs(p, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def sparsemax_routing_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
) -> Dict[str, object]:
    assert_shapes(x, w, h, [[1.0 for _ in w] for _ in x], f)
    z = matmul_router_logits(x, w)
    p = sparsemax_rows(z)
    y = combine_outputs(p, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def relu_routing_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
) -> Dict[str, object]:
    assert_shapes(x, w, h, [[1.0 for _ in w] for _ in x], f)
    z = matmul_router_logits(x, w)
    p = normalized_relu_rows(z)
    y = combine_outputs(p, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def cap2_routing_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    load: Sequence[float],
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    tau_rank: float = 0.5,
    tau_gate: float = 0.5,
    tau_cap: float = 0.25,
    mu: float = 1.0,
    epsilon: float = 1e-12,
) -> Dict[str, object]:
    """Run the CAP2-v0 capacity-aware pairwise relaxation."""

    assert_shapes(x, w, h, [[1.0 for _ in w] for _ in x], f)
    if len(load) != len(w):
        raise ValueError("load must have length E")
    z = matmul_router_logits(x, w)
    cap2 = cap2_routing_weights_rows(
        z,
        load,
        tau_rank=tau_rank,
        tau_gate=tau_gate,
        tau_cap=tau_cap,
        mu=mu,
        epsilon=epsilon,
    )
    a = cap2["a"]  # type: ignore[assignment]
    p = cap2["p"]  # type: ignore[assignment]
    y = combine_outputs(a, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def convex_topk_mask_direct_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    k: int = 2,
    lambda_smooth: float = 1e-2,
) -> Dict[str, object]:
    """Use the relaxed sparse top-k mask directly as router weights."""

    assert_shapes(x, w, h, [[1.0 for _ in w] for _ in x], f)
    z = matmul_router_logits(x, w)
    mask = convex_sparse_topk_mask_rows(z, k=k, lambda_smooth=lambda_smooth)
    y = combine_outputs(mask, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(mask)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def convex_topk_normalized_masked_softmax_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    k: int = 2,
    lambda_smooth: float = 1e-2,
) -> Dict[str, object]:
    """Normalize softmax probabilities after relaxed sparse top-k masking."""

    assert_shapes(x, w, h, [[1.0 for _ in w] for _ in x], f)
    z = matmul_router_logits(x, w)
    p = softmax_rows(z)
    mask = convex_sparse_topk_mask_rows(z, k=k, lambda_smooth=lambda_smooth)
    masked = apply_mask(p, mask)
    a = normalize_masked_probabilities(masked)
    y = combine_outputs(a, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
    return {
        "loss": l_rec + l_aux,
        "l_rec": l_rec,
        "l_aux": l_aux,
        "z": z,
        "p": p,
        "relaxed_mask": mask,
        "masked": masked,
        "a": a,
        "y": y,
        "residual": residual,
        "pbar": pbar,
    }


def normalized_pair_weight_reference(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    m: Matrix,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    contract: RouterContract | None = None,
) -> Dict[str, object]:
    contract = contract or RouterContract()
    contract.validate()
    assert_shapes(x, w, h, m, f)
    z = matmul_router_logits(x, w)
    p = softmax_rows(z)
    masked = apply_mask(p, m)
    a = normalize_masked_probabilities(masked)
    y = combine_outputs(a, h)
    l_rec, residual = squared_residual_loss(y, x, lambda_rec)
    pbar = mean_expert_probabilities(p)
    e = len(w)
    l_aux = gamma * e * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))
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


def fixed_mask_manual_backward(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    m: Matrix,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
) -> Dict[str, object]:
    forward = fixed_mask_top2_reference(
        x,
        w,
        h,
        m,
        f,
        lambda_rec=lambda_rec,
        gamma=gamma,
    )
    p = forward["p"]  # type: ignore[assignment]
    a = forward["a"]  # type: ignore[assignment]
    residual = forward["residual"]  # type: ignore[assignment]
    t = len(x)
    e = len(w)
    d = len(x[0])

    d_y = [[2.0 * lambda_rec * residual[t_i][d_i] for d_i in range(d)] for t_i in range(t)]
    d_a = []
    d_h: Tensor3 = []
    for t_i in range(t):
        d_a_t = []
        d_h_t = []
        for j in range(e):
            d_a_t.append(sum(d_y[t_i][d_i] * h[t_i][j][d_i] for d_i in range(d)))
            d_h_t.append([a[t_i][j] * d_y[t_i][d_i] for d_i in range(d)])
        d_a.append(d_a_t)
        d_h.append(d_h_t)

    d_p = []
    for t_i in range(t):
        d_p_t = []
        for j in range(e):
            d_from_rec = m[t_i][j] * d_a[t_i][j]
            d_from_aux = gamma * e * f[j] / t
            d_p_t.append(d_from_rec + d_from_aux)
        d_p.append(d_p_t)

    d_z = []
    for t_i in range(t):
        row_dot = sum(d_p[t_i][j] * p[t_i][j] for j in range(e))
        d_z.append([p[t_i][j] * (d_p[t_i][j] - row_dot) for j in range(e)])

    d_w = [[0.0 for _ in range(d)] for _ in range(e)]
    for j in range(e):
        for d_i in range(d):
            d_w[j][d_i] = sum(d_z[t_i][j] * x[t_i][d_i] for t_i in range(t))

    d_x_router = [[0.0 for _ in range(d)] for _ in range(t)]
    for t_i in range(t):
        for d_i in range(d):
            d_x_router[t_i][d_i] = sum(d_z[t_i][j] * w[j][d_i] for j in range(e))

    return {
        "d_y": d_y,
        "d_a": d_a,
        "d_p": d_p,
        "d_z": d_z,
        "d_w": d_w,
        "d_x_router": d_x_router,
        "d_h": d_h,
        "forward": forward,
    }


def finite_difference_d_w(
    x: Matrix,
    w: Matrix,
    h: Tensor3,
    m: Matrix,
    f: Sequence[float],
    *,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    eps: float = 1e-6,
) -> Matrix:
    e = len(w)
    d = len(w[0])
    grad = [[0.0 for _ in range(d)] for _ in range(e)]
    for j in range(e):
        for d_i in range(d):
            w_plus = [row[:] for row in w]
            w_minus = [row[:] for row in w]
            w_plus[j][d_i] += eps
            w_minus[j][d_i] -= eps
            loss_plus = fixed_mask_top2_reference(
                x, w_plus, h, m, f, lambda_rec=lambda_rec, gamma=gamma
            )["loss"]
            loss_minus = fixed_mask_top2_reference(
                x, w_minus, h, m, f, lambda_rec=lambda_rec, gamma=gamma
            )["loss"]
            grad[j][d_i] = (float(loss_plus) - float(loss_minus)) / (2.0 * eps)
    return grad


def max_abs_diff(a: Matrix, b: Matrix) -> float:
    return max(abs(a_ij - b_ij) for row_a, row_b in zip(a, b) for a_ij, b_ij in zip(row_a, row_b))


def fixture() -> Tuple[Matrix, Matrix, Tensor3, Matrix, List[float]]:
    x = [[0.2, -0.4], [0.7, 0.1], [-0.3, 0.5]]
    w = [[0.6, -0.2], [-0.1, 0.4], [0.3, 0.8]]
    h = [
        [[0.1, 0.2], [0.5, -0.1], [-0.2, 0.3]],
        [[0.4, 0.0], [-0.3, 0.6], [0.2, -0.2]],
        [[-0.1, 0.7], [0.3, 0.2], [0.5, -0.4]],
    ]
    # Saved forward top-2 mask. This harness does not differentiate through it.
    m = [[1.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 1.0]]
    f = [2.0 / 3.0, 2.0 / 3.0, 2.0 / 3.0]
    return x, w, h, m, f


if __name__ == "__main__":
    x, w, h, m, f = fixture()
    result = fixed_mask_top2_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
    backward = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
    fd = finite_difference_d_w(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
    diff = max_abs_diff(backward["d_w"], fd)  # type: ignore[arg-type]
    print(f"loss={result['loss']:.12f}")
    print(f"max_abs_diff_manual_vs_fd_dW={diff:.12e}")
