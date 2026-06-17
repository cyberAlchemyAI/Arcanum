# Invoke Plan - GCloud Minimal-Secret CUDA Runner

Mode: `plan`
Status: `pass-with-user-auth-blocker`
Target: `TASK-W0-008`
Owner: `research/triton-top2-backward-kernel`

## Intent

Prepare a Google Cloud route for validating CUDA/Triton readiness while doing
everything that does not require user credentials, browser approval, billing
selection, or secret material.

## Completed By This Plan

- Installed Google Cloud CLI under `~/.local/google-cloud-sdk`.
- Disabled Google Cloud CLI usage reporting.
- Verified that no account is authenticated locally.
- Added a minimal-secret GCloud CUDA probe runner script.
- Added a runbook with authentication, project, quota, run, evidence, and
  cleanup steps.

## Explicit Non-Actions

The agent did not:

- run `gcloud init`;
- run `gcloud auth login`;
- create service-account keys;
- set `GOOGLE_APPLICATION_CREDENTIALS`;
- create a project;
- enable billing;
- create cloud resources.

## Plan Boundary

The next human step is account/project authentication. After authentication,
the runner script can create a temporary bucket and GPU VM, run the startup
probe, collect serial logs, and delete resources.

## Validation Surface

Local validation:

```text
gcloud --version
gcloud config list core.disable_usage_reporting
gcloud auth list
```

External pass evidence:

```text
PASS: CUDA/Triton runner is ready
```

from the serial console log produced by
`scripts/gcloud_cuda_probe_runner.sh`.

## Next Route

1. User authenticates with `gcloud auth login --no-browser`.
2. User sets `PROJECT_ID`.
3. Run `scripts/gcloud_cuda_probe_runner.sh`.
4. Run `task-session` for `TASK-W0-008` after pass evidence exists.
