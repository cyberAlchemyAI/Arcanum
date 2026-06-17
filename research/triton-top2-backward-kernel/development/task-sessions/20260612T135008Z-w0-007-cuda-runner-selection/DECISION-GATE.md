# Decision Gate - CUDA Runner Path

Status: block
Date: 2026-06-12

## Blocker Question

Which CUDA runner path should this project use for Triton kernel validation?

## Option 1 - Remote GPU Host

Use an existing SSH-accessible machine that already has an NVIDIA GPU and driver.

- Benefit: fastest rigorous path if a GPU box already exists.
- Cost/risk: requires SSH access and workspace transfer or git checkout.
- When to choose: choose this if you already have a trusted GPU machine.
- Downstream impact: `TASK-W0-008` can validate with SSH, `uv`, `torch`, `triton`,
  `nvidia-smi`, and project pytest.

Recommended if available.

## Option 2 - Cloud GPU Instance

Rent a short-lived CUDA-capable instance and run validation there.

- Benefit: clean and reproducible if no existing GPU host exists.
- Cost/risk: requires account, budget approval, region/GPU choice, and teardown.
- When to choose: choose this if no trusted remote GPU host is available.
- Downstream impact: `TASK-W0-007` must record provider, instance type, setup
  commands, spending cap, and teardown rule before provisioning.

Recommended fallback.

## Option 3 - Local NVIDIA Docker Setup

Try to make this current host a CUDA runner by installing/configuring NVIDIA
drivers and NVIDIA Container Toolkit.

- Benefit: keeps validation local if this machine has hidden/disabled NVIDIA
  hardware.
- Cost/risk: system-level driver work, possible reboot, and currently no detected
  NVIDIA device or runtime.
- When to choose: choose only if you know this host has an NVIDIA GPU.
- Downstream impact: needs driver/toolkit install outside this repo before
  `TASK-W0-008`.

Not recommended based on current diagnostics.

## Option 4 - Managed Notebook

Use a notebook/runtime service for early Triton smoke validation.

- Benefit: fastest manual experiment path.
- Cost/risk: weaker repository evidence, harder task-session reproduction.
- When to choose: choose only for an exploratory smoke test, not final evidence.
- Downstream impact: final W5-W7 validation should still move to a reproducible
  remote or cloud runner.

Not recommended for final validation.

## Recommendation

Choose Option 1 if you have SSH access to a GPU host. Otherwise choose Option 2
with an explicit spending cap and teardown rule.
