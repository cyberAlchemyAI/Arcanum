#!/usr/bin/env python3
"""Benchmark fixed-mask and CAP2 Triton backward paths on CUDA."""

from __future__ import annotations

import argparse
import json
import pathlib
import statistics
import sys
import time
from typing import Any, Callable

import torch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reference.router_triton import (  # noqa: E402
    cap2_row_backward_triton,
    fixed_mask_dh_triton,
    fixed_mask_dw_triton,
    fixed_mask_dx_router_triton,
    triton_available,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--iters", type=int, default=50)
    parser.add_argument("--json-out", type=pathlib.Path)
    parser.add_argument("--markdown-out", type=pathlib.Path)
    args = parser.parse_args()

    if not torch.cuda.is_available() or not triton_available():
        raise RuntimeError("CUDA and Triton are required for benchmarking")

    torch.manual_seed(20260614)
    device = torch.device("cuda")
    sizes = [
        {"name": "small", "t": 128, "e": 8, "d": 64},
        {"name": "medium", "t": 512, "e": 16, "d": 128},
    ]

    records: list[dict[str, Any]] = []
    for spec in sizes:
        t_size = spec["t"]
        e_size = spec["e"]
        d_size = spec["d"]
        x = torch.randn((t_size, d_size), device=device, dtype=torch.float32)
        w = torch.randn((e_size, d_size), device=device, dtype=torch.float32)
        h = torch.randn((t_size, e_size, d_size), device=device, dtype=torch.float32)
        d_z = torch.randn((t_size, e_size), device=device, dtype=torch.float32)
        a = torch.softmax(torch.randn((t_size, e_size), device=device, dtype=torch.float32), dim=-1)
        d_y = torch.randn((t_size, d_size), device=device, dtype=torch.float32)
        load = torch.rand((e_size,), device=device, dtype=torch.float32)
        f = torch.rand((e_size,), device=device, dtype=torch.float32)

        fixed_out = {
            "d_w": torch.empty((e_size, d_size), device=device, dtype=torch.float32),
            "d_x": torch.empty((t_size, d_size), device=device, dtype=torch.float32),
            "d_h": torch.empty((t_size, e_size, d_size), device=device, dtype=torch.float32),
        }
        cap2_out = {
            "d_z": torch.empty((t_size, e_size), device=device, dtype=torch.float32),
            "d_w": torch.empty((e_size, d_size), device=device, dtype=torch.float32),
            "d_x": torch.empty((t_size, d_size), device=device, dtype=torch.float32),
            "d_h": torch.empty((t_size, e_size, d_size), device=device, dtype=torch.float32),
        }

        def fixed_mask_backward() -> None:
            fixed_mask_dw_triton(d_z, x, out=fixed_out["d_w"])
            fixed_mask_dx_router_triton(d_z, w, out=fixed_out["d_x"])
            fixed_mask_dh_triton(a, d_y, out=fixed_out["d_h"])

        def cap2_backward() -> None:
            cap2_row_backward_triton(
                x,
                w,
                h,
                load,
                f,
                out_d_z=cap2_out["d_z"],
                out_d_x_router=cap2_out["d_x"],
                out_d_h=cap2_out["d_h"],
                out_d_w=cap2_out["d_w"],
                lambda_rec=0.7,
                gamma=0.2,
                tau_rank=0.6,
                tau_gate=0.7,
                tau_cap=0.4,
                mu=0.5,
            )

        records.append(_benchmark_path(spec, "fixed_mask", fixed_mask_backward, args.warmup, args.iters))
        records.append(_benchmark_path(spec, "cap2_fixed_load", cap2_backward, args.warmup, args.iters))

    payload = {
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "device": torch.cuda.get_device_name(0),
        "torch": torch.__version__,
        "cuda": torch.version.cuda,
        "warmup": args.warmup,
        "iters": args.iters,
        "records": records,
    }
    text = json.dumps(payload, indent=2, sort_keys=True)
    print(text)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")
    if args.markdown_out is not None:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(_to_markdown(payload), encoding="utf-8")
    return 0


def _benchmark_path(
    spec: dict[str, Any],
    path_name: str,
    fn: Callable[[], None],
    warmup: int,
    iters: int,
) -> dict[str, Any]:
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()

    timings: list[float] = []
    for _ in range(iters):
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        fn()
        end.record()
        torch.cuda.synchronize()
        timings.append(float(start.elapsed_time(end)))

    return {
        "name": spec["name"],
        "path": path_name,
        "tokens": spec["t"],
        "experts": spec["e"],
        "dim": spec["d"],
        "median_ms": statistics.median(timings),
        "mean_ms": statistics.fmean(timings),
        "min_ms": min(timings),
        "max_ms": max(timings),
    }


def _to_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Triton Path Benchmark",
        "",
        f"Timestamp: `{payload['timestamp_utc']}`",
        f"Device: `{payload['device']}`",
        f"PyTorch: `{payload['torch']}`",
        f"CUDA: `{payload['cuda']}`",
        f"Warmup/iters: `{payload['warmup']}` / `{payload['iters']}`",
        "",
        "| Size | Path | T | E | D | Median ms | Mean ms | Min ms | Max ms |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for record in payload["records"]:
        lines.append(
            "| {name} | {path} | {tokens} | {experts} | {dim} | {median_ms:.4f} | {mean_ms:.4f} | {min_ms:.4f} | {max_ms:.4f} |".format(
                **record
            )
        )
    lines.extend(
        [
            "",
            "Notes:",
            "",
            "- Fixed-mask timing includes Triton `dW`, `dX_router`, and `dH` kernels.",
            "- CAP2 timing includes row-local CAP2 `dZ`/`dH`, plus Triton `dX_router` and `dW` kernels.",
            "- These are implementation-path timings on the recorded RunPod GPU, not a production tuning claim.",
        ]
    )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
