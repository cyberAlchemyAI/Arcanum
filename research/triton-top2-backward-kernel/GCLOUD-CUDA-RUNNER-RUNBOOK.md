# GCloud CUDA Runner Runbook - Minimal Secret Exposure

Status: `ready-for-user-auth`
Date: 2026-06-14

## Goal

Run `TASK-W0-008` on Google Cloud without service-account key files, without
committing secrets, and without SSHing into the VM.

The design is:

```text
local gcloud user login -> temporary GCS bucket -> GPU VM startup script ->
serial console evidence -> automatic local cleanup
```

## What Is Already Done Locally

- Google Cloud CLI installed at:

```text
~/.local/google-cloud-sdk/bin/gcloud
```

- Installed version:

```text
Google Cloud SDK 572.0.0
```

- Usage reporting disabled:

```text
core.disable_usage_reporting = true
```

- No Google account is authenticated in this checkout session.
- No service-account key file was created.
- No `GOOGLE_APPLICATION_CREDENTIALS` flow was used.

## Minimal Secret Policy

Do:

- use user OAuth with `gcloud auth login --no-browser` or run from Google Cloud
  Shell;
- use a project with billing enabled and a short-lived GPU VM;
- use the VM's attached service account for temporary GCS object read access;
- capture proof from serial console logs;
- delete the VM and bucket immediately after the probe.

Avoid:

- service account JSON keys;
- `gcloud auth activate-service-account --key-file ...`;
- committing `.config/gcloud`, `.boto`, SSH keys, access tokens, or JSON keys;
- leaving a GPU VM running after the probe.

## User Setup Steps

These steps require your browser/account and cannot be done safely by the agent.

1. Authenticate the local CLI with user OAuth:

```sh
~/.local/google-cloud-sdk/bin/gcloud auth login --no-browser
```

2. Pick or create a Google Cloud project with billing enabled.

3. Set the project:

```sh
~/.local/google-cloud-sdk/bin/gcloud config set project PROJECT_ID
```

4. Confirm no service-account key path is set:

```sh
printenv GOOGLE_APPLICATION_CREDENTIALS
```

Expected output is empty.

5. Check that your account is active:

```sh
~/.local/google-cloud-sdk/bin/gcloud auth list
```

6. Check that the target zone has the desired accelerator:

```sh
~/.local/google-cloud-sdk/bin/gcloud compute accelerator-types list \
  --filter='name=nvidia-tesla-t4 AND zone:us-central1-a'
```

If the zone has no T4 quota or availability, try another zone/region and pass
`ZONE=... REGION=...` to the runner script.

## Run The Probe

From the tower root:

```sh
cd <repo>/research/triton-top2-backward-kernel
PROJECT_ID=your-project-id \
ZONE=us-central1-a \
REGION=us-central1 \
bash scripts/gcloud_cuda_probe_runner.sh
```

The script:

1. enables Compute Engine and Cloud Storage APIs;
2. creates a small temporary GCS bucket;
3. uploads a tarball of this tower without `.venv`, caches, or bytecode;
4. creates a PyTorch Deep Learning VM with one NVIDIA T4 GPU;
5. runs the probe from a startup script;
6. saves serial console output under `development/task-sessions/...`;
7. deletes the VM and temporary bucket unless `KEEP_RESOURCES=1`.

## Expected Pass Evidence

The serial log must include:

```text
torch.cuda.is_available True
triton_available True
nvidia-smi <non-empty path>
PASS: CUDA/Triton runner is ready
```

After a pass, run a `task-session` for `TASK-W0-008` to synchronize
`WORK-PACK.md`.

## If It Blocks

Common blockers:

- project has no billing;
- Compute Engine API not enabled;
- GPU quota is missing for the selected region;
- selected zone has no T4 availability;
- organization policy blocks external IPs, default service account use, or GCS;
- startup script cannot read the temporary bucket;
- the Deep Learning VM image family changed.

Safe retries:

```sh
ZONE=us-central1-b REGION=us-central1 PROJECT_ID=your-project-id bash scripts/gcloud_cuda_probe_runner.sh
ZONE=us-west1-b REGION=us-west1 PROJECT_ID=your-project-id bash scripts/gcloud_cuda_probe_runner.sh
```

## Cleanup Check

After any failed or interrupted run:

```sh
~/.local/google-cloud-sdk/bin/gcloud compute instances list \
  --filter='name~triton-probe'

~/.local/google-cloud-sdk/bin/gcloud storage buckets list \
  --filter='name~triton-probe'
```

Delete leftovers:

```sh
~/.local/google-cloud-sdk/bin/gcloud compute instances delete INSTANCE_NAME --zone ZONE --quiet
~/.local/google-cloud-sdk/bin/gcloud storage rm --recursive gs://BUCKET_NAME
```

## Source Notes

This plan follows Google Cloud's documented patterns:

- install and initialize the Google Cloud CLI;
- create PyTorch Deep Learning VM instances from the command line;
- use Deep Learning VM GPU image families;
- attach GPUs with `--accelerator`;
- set GPU instances to terminate/stop for host maintenance;
- avoid service-account key files for this workflow.
