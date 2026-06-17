"""Triton kernels for the fixed-mask Top2 router baseline.

The W5 baseline keeps the Triton surface deliberately narrow: compute
``dW = dZ^T @ X`` after the fixed-mask reference graph has produced ``dZ``.
This proves the first CUDA/Triton parity slice without claiming a fused or
zero-allocation backward pass.
"""

from __future__ import annotations

from typing import Any

import torch

try:  # pragma: no cover - availability is environment-dependent.
    import triton
    import triton.language as tl
except ModuleNotFoundError:  # pragma: no cover - exercised on CPU-only hosts.
    triton = None  # type: ignore[assignment]
    tl = None  # type: ignore[assignment]


def triton_available() -> bool:
    return triton is not None and tl is not None


if triton_available():

    @triton.jit
    def _fixed_mask_dw_kernel(
        d_z_ptr,
        x_ptr,
        d_w_ptr,
        t_size: tl.constexpr,
        e_size: tl.constexpr,
        d_size: tl.constexpr,
        stride_dz_t: tl.constexpr,
        stride_dz_e: tl.constexpr,
        stride_x_t: tl.constexpr,
        stride_x_d: tl.constexpr,
        stride_dw_e: tl.constexpr,
        stride_dw_d: tl.constexpr,
        block_e: tl.constexpr,
        block_d: tl.constexpr,
        block_t: tl.constexpr,
    ) -> None:
        e_offsets = tl.program_id(0) * block_e + tl.arange(0, block_e)
        d_offsets = tl.program_id(1) * block_d + tl.arange(0, block_d)
        t_offsets = tl.arange(0, block_t)

        acc = tl.zeros((block_e, block_d), dtype=tl.float32)
        for t_start in range(0, t_size, block_t):
            t_idx = t_start + t_offsets
            dz = tl.load(
                d_z_ptr + t_idx[:, None] * stride_dz_t + e_offsets[None, :] * stride_dz_e,
                mask=(t_idx[:, None] < t_size) & (e_offsets[None, :] < e_size),
                other=0.0,
            )
            x = tl.load(
                x_ptr + t_idx[:, None] * stride_x_t + d_offsets[None, :] * stride_x_d,
                mask=(t_idx[:, None] < t_size) & (d_offsets[None, :] < d_size),
                other=0.0,
            )
            acc += tl.dot(tl.trans(dz), x, input_precision="ieee")

        tl.store(
            d_w_ptr + e_offsets[:, None] * stride_dw_e + d_offsets[None, :] * stride_dw_d,
            acc,
            mask=(e_offsets[:, None] < e_size) & (d_offsets[None, :] < d_size),
        )

    @triton.jit
    def _fixed_mask_dx_router_kernel(
        d_z_ptr,
        w_ptr,
        d_x_ptr,
        t_size: tl.constexpr,
        e_size: tl.constexpr,
        d_size: tl.constexpr,
        stride_dz_t: tl.constexpr,
        stride_dz_e: tl.constexpr,
        stride_w_e: tl.constexpr,
        stride_w_d: tl.constexpr,
        stride_dx_t: tl.constexpr,
        stride_dx_d: tl.constexpr,
        block_t: tl.constexpr,
        block_d: tl.constexpr,
        block_e: tl.constexpr,
    ) -> None:
        t_offsets = tl.program_id(0) * block_t + tl.arange(0, block_t)
        d_offsets = tl.program_id(1) * block_d + tl.arange(0, block_d)
        e_offsets = tl.arange(0, block_e)

        acc = tl.zeros((block_t, block_d), dtype=tl.float32)
        for e_start in range(0, e_size, block_e):
            e_idx = e_start + e_offsets
            dz = tl.load(
                d_z_ptr + t_offsets[:, None] * stride_dz_t + e_idx[None, :] * stride_dz_e,
                mask=(t_offsets[:, None] < t_size) & (e_idx[None, :] < e_size),
                other=0.0,
            )
            w = tl.load(
                w_ptr + e_idx[:, None] * stride_w_e + d_offsets[None, :] * stride_w_d,
                mask=(e_idx[:, None] < e_size) & (d_offsets[None, :] < d_size),
                other=0.0,
            )
            acc += tl.dot(dz, w, input_precision="ieee")

        tl.store(
            d_x_ptr + t_offsets[:, None] * stride_dx_t + d_offsets[None, :] * stride_dx_d,
            acc,
            mask=(t_offsets[:, None] < t_size) & (d_offsets[None, :] < d_size),
        )

    @triton.jit
    def _fixed_mask_dh_kernel(
        a_ptr,
        d_y_ptr,
        d_h_ptr,
        t_size: tl.constexpr,
        e_size: tl.constexpr,
        d_size: tl.constexpr,
        stride_a_t: tl.constexpr,
        stride_a_e: tl.constexpr,
        stride_dy_t: tl.constexpr,
        stride_dy_d: tl.constexpr,
        stride_dh_t: tl.constexpr,
        stride_dh_e: tl.constexpr,
        stride_dh_d: tl.constexpr,
        block_e: tl.constexpr,
        block_d: tl.constexpr,
    ) -> None:
        t_idx = tl.program_id(0)
        e_offsets = tl.program_id(1) * block_e + tl.arange(0, block_e)
        d_offsets = tl.program_id(2) * block_d + tl.arange(0, block_d)

        a = tl.load(
            a_ptr + t_idx * stride_a_t + e_offsets * stride_a_e,
            mask=(t_idx < t_size) & (e_offsets < e_size),
            other=0.0,
        )
        d_y = tl.load(
            d_y_ptr + t_idx * stride_dy_t + d_offsets * stride_dy_d,
            mask=(t_idx < t_size) & (d_offsets < d_size),
            other=0.0,
        )
        d_h = a[:, None].to(tl.float32) * d_y[None, :].to(tl.float32)
        tl.store(
            d_h_ptr
            + t_idx * stride_dh_t
            + e_offsets[:, None] * stride_dh_e
            + d_offsets[None, :] * stride_dh_d,
            d_h,
            mask=(t_idx < t_size) & (e_offsets[:, None] < e_size) & (d_offsets[None, :] < d_size),
        )

    @triton.jit
    def _cap2_row_backward_kernel(
        x_ptr,
        w_ptr,
        h_ptr,
        load_ptr,
        f_ptr,
        d_z_ptr,
        d_h_ptr,
        t_size: tl.constexpr,
        e_size: tl.constexpr,
        d_size: tl.constexpr,
        stride_x_t: tl.constexpr,
        stride_x_d: tl.constexpr,
        stride_w_e: tl.constexpr,
        stride_w_d: tl.constexpr,
        stride_h_t: tl.constexpr,
        stride_h_e: tl.constexpr,
        stride_h_d: tl.constexpr,
        stride_dz_t: tl.constexpr,
        stride_dz_e: tl.constexpr,
        stride_dh_t: tl.constexpr,
        stride_dh_e: tl.constexpr,
        stride_dh_d: tl.constexpr,
        lambda_rec: tl.constexpr,
        gamma: tl.constexpr,
        tau_rank: tl.constexpr,
        tau_gate: tl.constexpr,
        tau_cap: tl.constexpr,
        mu: tl.constexpr,
        epsilon: tl.constexpr,
        block_e: tl.constexpr,
        block_d: tl.constexpr,
    ) -> None:
        t_idx = tl.program_id(0)
        e_offsets = tl.arange(0, block_e)
        d_offsets = tl.arange(0, block_d)
        e_mask = e_offsets < e_size

        z = tl.zeros((block_e,), dtype=tl.float32)
        for d_start in range(0, d_size, block_d):
            d_idx = d_start + d_offsets
            d_mask = d_idx < d_size
            x = tl.load(
                x_ptr + t_idx * stride_x_t + d_idx * stride_x_d,
                mask=(t_idx < t_size) & d_mask,
                other=0.0,
            ).to(tl.float32)
            w = tl.load(
                w_ptr + e_offsets[:, None] * stride_w_e + d_idx[None, :] * stride_w_d,
                mask=e_mask[:, None] & d_mask[None, :],
                other=0.0,
            ).to(tl.float32)
            z += tl.sum(w * x[None, :], axis=1)

        capacity = 2.1 / e_size
        load = tl.load(load_ptr + e_offsets, mask=e_mask, other=0.0).to(tl.float32)
        overload = tl.sigmoid((load - capacity) / tau_cap)
        u = z - mu * overload
        u = tl.where(e_mask, u, -float("inf"))

        p_num = tl.exp(u - tl.max(u, axis=0))
        p = p_num / tl.sum(p_num, axis=0)
        p = tl.where(e_mask, p, 0.0)

        row_offsets = e_offsets[:, None]
        col_offsets = e_offsets[None, :]
        pair_mask = (row_offsets < e_size) & (col_offsets < e_size) & (row_offsets != col_offsets)
        pairwise = tl.sigmoid((u[:, None] - u[None, :]) / tau_rank)
        pairwise = tl.where(pair_mask, pairwise, 0.0)
        soft_rank = tl.sum(pairwise, axis=1)
        threshold = e_size - 2.5
        membership = tl.sigmoid((soft_rank - threshold) / tau_gate)
        membership = tl.where(e_mask, membership, 0.0)
        gated = membership * p
        normalizer = epsilon + tl.sum(gated, axis=0)
        a = gated / normalizer

        d_a = tl.zeros((block_e,), dtype=tl.float32)
        for d_start in range(0, d_size, block_d):
            d_idx = d_start + d_offsets
            d_mask = d_idx < d_size
            x = tl.load(
                x_ptr + t_idx * stride_x_t + d_idx * stride_x_d,
                mask=(t_idx < t_size) & d_mask,
                other=0.0,
            ).to(tl.float32)
            h = tl.load(
                h_ptr
                + t_idx * stride_h_t
                + e_offsets[:, None] * stride_h_e
                + d_idx[None, :] * stride_h_d,
                mask=(t_idx < t_size) & e_mask[:, None] & d_mask[None, :],
                other=0.0,
            ).to(tl.float32)
            y = tl.sum(a[:, None] * h, axis=0)
            d_y = 2.0 * lambda_rec * (y - x)
            d_h = a[:, None] * d_y[None, :]
            tl.store(
                d_h_ptr
                + t_idx * stride_dh_t
                + e_offsets[:, None] * stride_dh_e
                + d_idx[None, :] * stride_dh_d,
                d_h,
                mask=(t_idx < t_size) & e_mask[:, None] & d_mask[None, :],
            )
            d_a += tl.sum(h * d_y[None, :], axis=1)

        contraction = tl.sum(d_a * gated, axis=0)
        d_gated = (d_a * normalizer - contraction) / (normalizer * normalizer)
        d_membership = d_gated * p
        f = tl.load(f_ptr + e_offsets, mask=e_mask, other=0.0).to(tl.float32)
        d_p = d_gated * membership + gamma * (e_size / t_size) * f
        softmax_dot = tl.sum(d_p * p, axis=0)
        d_u_softmax = p * (d_p - softmax_dot)
        d_soft_rank = d_membership * membership * (1.0 - membership) / tau_gate

        rank_factor = pairwise * (1.0 - pairwise) / tau_rank
        rank_messages = d_soft_rank[:, None] * rank_factor
        d_u_rank = tl.sum(rank_messages, axis=1) - tl.sum(rank_messages, axis=0)
        d_z = d_u_softmax + d_u_rank
        tl.store(
            d_z_ptr + t_idx * stride_dz_t + e_offsets * stride_dz_e,
            d_z,
            mask=(t_idx < t_size) & e_mask,
        )


def fixed_mask_dw_triton(
    d_z: torch.Tensor,
    x: torch.Tensor,
    *,
    out: torch.Tensor | None = None,
    block_e: int = 16,
    block_d: int = 16,
    block_t: int = 32,
) -> torch.Tensor:
    """Return ``dW = dZ^T @ X`` using a Triton CUDA kernel.

    Args:
        d_z: Router-logit gradient with shape ``[T, E]``.
        x: Input activations with shape ``[T, D]``.

    Passing ``out`` lets callers use a preallocated output buffer for the
    zero-allocation hot path measured in W7.
    """

    _validate_kernel_inputs(d_z, x)
    if not triton_available():
        raise RuntimeError("Triton is not importable in this environment")
    if not d_z.is_cuda or not x.is_cuda:
        raise RuntimeError("fixed_mask_dw_triton requires CUDA tensors")

    d_z_c = d_z.contiguous()
    x_c = x.contiguous()
    t_size = d_z_c.shape[0]
    e_size = d_z_c.shape[1]
    d_size = x_c.shape[1]
    d_w = _prepare_output(out, (e_size, d_size), x_c.device, "out")
    physical_block_e = _triton_dot_block_size(block_e)
    physical_block_d = _triton_dot_block_size(block_d)
    physical_block_t = _triton_dot_block_size(block_t)
    grid = (triton.cdiv(e_size, physical_block_e), triton.cdiv(d_size, physical_block_d))
    _fixed_mask_dw_kernel[grid](
        d_z_c,
        x_c,
        d_w,
        t_size,
        e_size,
        d_size,
        d_z_c.stride(0),
        d_z_c.stride(1),
        x_c.stride(0),
        x_c.stride(1),
        d_w.stride(0),
        d_w.stride(1),
        physical_block_e,
        physical_block_d,
        physical_block_t,
    )
    return d_w


def fixed_mask_dx_router_triton(
    d_z: torch.Tensor,
    w: torch.Tensor,
    *,
    out: torch.Tensor | None = None,
    block_t: int = 16,
    block_d: int = 16,
    block_e: int = 32,
) -> torch.Tensor:
    """Return the router-logit input gradient contribution ``dX = dZ @ W``."""

    _validate_dx_router_inputs(d_z, w)
    if not triton_available():
        raise RuntimeError("Triton is not importable in this environment")
    if not d_z.is_cuda or not w.is_cuda:
        raise RuntimeError("fixed_mask_dx_router_triton requires CUDA tensors")

    d_z_c = d_z.contiguous()
    w_c = w.contiguous()
    t_size = d_z_c.shape[0]
    e_size = d_z_c.shape[1]
    d_size = w_c.shape[1]
    d_x = _prepare_output(out, (t_size, d_size), w_c.device, "out")
    physical_block_t = _triton_dot_block_size(block_t)
    physical_block_d = _triton_dot_block_size(block_d)
    physical_block_e = _triton_dot_block_size(block_e)
    grid = (triton.cdiv(t_size, physical_block_t), triton.cdiv(d_size, physical_block_d))
    _fixed_mask_dx_router_kernel[grid](
        d_z_c,
        w_c,
        d_x,
        t_size,
        e_size,
        d_size,
        d_z_c.stride(0),
        d_z_c.stride(1),
        w_c.stride(0),
        w_c.stride(1),
        d_x.stride(0),
        d_x.stride(1),
        physical_block_t,
        physical_block_d,
        physical_block_e,
    )
    return d_x


def fixed_mask_dh_triton(
    a: torch.Tensor,
    d_y: torch.Tensor,
    *,
    out: torch.Tensor | None = None,
    block_e: int = 16,
    block_d: int = 16,
) -> torch.Tensor:
    """Return the fixed-mask expert-output gradient ``dH[t, e, d] = A[t, e] * dY[t, d]``."""

    _validate_dh_inputs(a, d_y)
    if not triton_available():
        raise RuntimeError("Triton is not importable in this environment")
    if not a.is_cuda or not d_y.is_cuda:
        raise RuntimeError("fixed_mask_dh_triton requires CUDA tensors")

    a_c = a.contiguous()
    d_y_c = d_y.contiguous()
    t_size = a_c.shape[0]
    e_size = a_c.shape[1]
    d_size = d_y_c.shape[1]
    d_h = _prepare_output(out, (t_size, e_size, d_size), d_y_c.device, "out")
    physical_block_e = _triton_dot_block_size(block_e)
    physical_block_d = _triton_dot_block_size(block_d)
    grid = (t_size, triton.cdiv(e_size, physical_block_e), triton.cdiv(d_size, physical_block_d))
    _fixed_mask_dh_kernel[grid](
        a_c,
        d_y_c,
        d_h,
        t_size,
        e_size,
        d_size,
        a_c.stride(0),
        a_c.stride(1),
        d_y_c.stride(0),
        d_y_c.stride(1),
        d_h.stride(0),
        d_h.stride(1),
        d_h.stride(2),
        physical_block_e,
        physical_block_d,
    )
    return d_h


def cap2_row_backward_triton(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    load: torch.Tensor,
    f: torch.Tensor,
    *,
    out_d_z: torch.Tensor | None = None,
    out_d_x_router: torch.Tensor | None = None,
    out_d_h: torch.Tensor | None = None,
    out_d_w: torch.Tensor | None = None,
    lambda_rec: float = 1.0,
    gamma: float = 0.0,
    tau_rank: float = 0.5,
    tau_gate: float = 0.5,
    tau_cap: float = 0.25,
    mu: float = 1.0,
    epsilon: float = 1e-12,
    block_e: int = 16,
    block_d: int = 16,
) -> dict[str, torch.Tensor]:
    """Return CAP2 backward outputs ``dZ``, ``dX_router``, ``dH``, and ``dW``.

    The row-local kernel computes ``dZ`` and ``dH``. The wrapper then reuses
    validated matrix kernels for ``dX_router = dZ @ W`` and ``dW = dZ^T @ X``.
    """

    _validate_cap2_inputs(x, w, h, load, f)
    if not triton_available():
        raise RuntimeError("Triton is not importable in this environment")
    if not all(tensor.is_cuda for tensor in (x, w, h, load, f)):
        raise RuntimeError("cap2_row_backward_triton requires CUDA tensors")
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

    x_c = x.contiguous()
    w_c = w.contiguous()
    h_c = h.contiguous()
    load_c = load.contiguous()
    f_c = f.contiguous()
    t_size = x_c.shape[0]
    e_size = w_c.shape[0]
    d_size = x_c.shape[1]
    d_z = _prepare_output(out_d_z, (t_size, e_size), x_c.device, "out_d_z")
    d_h = _prepare_output(out_d_h, (t_size, e_size, d_size), x_c.device, "out_d_h")
    physical_block_e = _triton_dot_block_size(max(block_e, e_size))
    physical_block_d = _triton_dot_block_size(block_d)
    _cap2_row_backward_kernel[(t_size,)](
        x_c,
        w_c,
        h_c,
        load_c,
        f_c,
        d_z,
        d_h,
        t_size,
        e_size,
        d_size,
        x_c.stride(0),
        x_c.stride(1),
        w_c.stride(0),
        w_c.stride(1),
        h_c.stride(0),
        h_c.stride(1),
        h_c.stride(2),
        d_z.stride(0),
        d_z.stride(1),
        d_h.stride(0),
        d_h.stride(1),
        d_h.stride(2),
        float(lambda_rec),
        float(gamma),
        float(tau_rank),
        float(tau_gate),
        float(tau_cap),
        float(mu),
        float(epsilon),
        physical_block_e,
        physical_block_d,
    )
    d_x_router = fixed_mask_dx_router_triton(
        d_z,
        w_c,
        out=out_d_x_router,
        block_t=block_d,
        block_d=block_d,
        block_e=physical_block_e,
    )
    d_w = fixed_mask_dw_triton(
        d_z,
        x_c,
        out=out_d_w,
        block_e=physical_block_e,
        block_d=block_d,
        block_t=block_d,
    )
    return {"d_z": d_z, "d_x_router": d_x_router, "d_h": d_h, "d_w": d_w}


def _triton_dot_block_size(requested: int) -> int:
    """Return a power-of-two tile size that satisfies Triton dot lower bounds."""

    if requested <= 0:
        raise ValueError("Triton block sizes must be positive")
    physical = max(16, requested)
    return 1 << (physical - 1).bit_length()


def _prepare_output(
    out: torch.Tensor | None,
    shape: tuple[int, ...],
    device: torch.device,
    name: str,
) -> torch.Tensor:
    if out is None:
        return torch.empty(shape, device=device, dtype=torch.float32)
    if tuple(out.shape) != shape:
        raise ValueError(f"{name} must have shape {shape}")
    if out.device != device:
        raise ValueError(f"{name} must be on the same device as the inputs")
    if out.dtype != torch.float32:
        raise ValueError(f"{name} must have dtype torch.float32")
    if not out.is_contiguous():
        raise ValueError(f"{name} must be contiguous")
    return out


def _validate_kernel_inputs(d_z: torch.Tensor, x: torch.Tensor) -> None:
    if d_z.ndim != 2:
        raise ValueError("d_z must have shape [T, E]")
    if x.ndim != 2:
        raise ValueError("x must have shape [T, D]")
    if d_z.shape[0] != x.shape[0]:
        raise ValueError("d_z and x must have matching token dimension T")
    if not d_z.is_floating_point() or not x.is_floating_point():
        raise ValueError("d_z and x must be floating point tensors")


def _validate_dx_router_inputs(d_z: torch.Tensor, w: torch.Tensor) -> None:
    if d_z.ndim != 2:
        raise ValueError("d_z must have shape [T, E]")
    if w.ndim != 2:
        raise ValueError("w must have shape [E, D]")
    if d_z.shape[1] != w.shape[0]:
        raise ValueError("d_z expert dimension must match w expert dimension E")
    if not d_z.is_floating_point() or not w.is_floating_point():
        raise ValueError("d_z and w must be floating point tensors")


def _validate_dh_inputs(a: torch.Tensor, d_y: torch.Tensor) -> None:
    if a.ndim != 2:
        raise ValueError("a must have shape [T, E]")
    if d_y.ndim != 2:
        raise ValueError("d_y must have shape [T, D]")
    if a.shape[0] != d_y.shape[0]:
        raise ValueError("a and d_y must have matching token dimension T")
    if not a.is_floating_point() or not d_y.is_floating_point():
        raise ValueError("a and d_y must be floating point tensors")


def _validate_cap2_inputs(
    x: torch.Tensor,
    w: torch.Tensor,
    h: torch.Tensor,
    load: torch.Tensor,
    f: torch.Tensor,
) -> None:
    if x.ndim != 2:
        raise ValueError("x must have shape [T, D]")
    if w.ndim != 2:
        raise ValueError("w must have shape [E, D]")
    if h.ndim != 3:
        raise ValueError("h must have shape [T, E, D]")
    if load.ndim != 1:
        raise ValueError("load must have shape [E]")
    if f.ndim != 1:
        raise ValueError("f must have shape [E]")
    t_size, d_size = x.shape
    e_size = w.shape[0]
    if t_size == 0:
        raise ValueError("x must contain at least one token")
    if e_size < 2:
        raise ValueError("CAP2 requires at least two experts")
    if w.shape[1] != d_size:
        raise ValueError("w rows must match x feature dimension")
    if h.shape != (t_size, e_size, d_size):
        raise ValueError("h must have shape [T, E, D]")
    if load.shape[0] != e_size:
        raise ValueError("load must have length E")
    if f.shape[0] != e_size:
        raise ValueError("f must have length E")
    if not all(tensor.is_floating_point() for tensor in (x, w, h, load, f)):
        raise ValueError("CAP2 inputs must be floating point tensors")


__all__ = [
    "cap2_row_backward_triton",
    "fixed_mask_dh_triton",
    "fixed_mask_dw_triton",
    "fixed_mask_dx_router_triton",
    "triton_available",
]
