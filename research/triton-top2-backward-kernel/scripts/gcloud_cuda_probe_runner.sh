#!/usr/bin/env bash
set -euo pipefail

GCLOUD="${GCLOUD:-$HOME/.local/google-cloud-sdk/bin/gcloud}"
PROJECT_ID="${PROJECT_ID:-}"
REGION="${REGION:-us-central1}"
ZONE="${ZONE:-us-central1-a}"
GPU_TYPE="${GPU_TYPE:-nvidia-tesla-t4}"
MACHINE_TYPE="${MACHINE_TYPE:-n1-standard-4}"
IMAGE_FAMILY="${IMAGE_FAMILY:-pytorch-2-9-cu129-ubuntu-2204-nvidia-580}"
IMAGE_PROJECT="${IMAGE_PROJECT:-deeplearning-platform-release}"
RUN_ID="${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)}"
INSTANCE_NAME="${INSTANCE_NAME:-triton-probe-${RUN_ID,,}}"
BUCKET_NAME="${BUCKET_NAME:-${PROJECT_ID}-triton-probe-${RUN_ID,,}}"
EVIDENCE_DIR="${EVIDENCE_DIR:-development/task-sessions/${RUN_ID}-gcloud-cuda-probe}"
KEEP_RESOURCES="${KEEP_RESOURCES:-0}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "BLOCK: set PROJECT_ID to a Google Cloud project with billing and GPU quota." >&2
  exit 2
fi

if [[ ! -x "$GCLOUD" ]]; then
  echo "BLOCK: gcloud not found at $GCLOUD" >&2
  exit 2
fi

mkdir -p "$EVIDENCE_DIR"

cleanup() {
  if [[ "$KEEP_RESOURCES" == "1" ]]; then
    echo "KEEP_RESOURCES=1; not deleting instance or bucket."
    return
  fi
  "$GCLOUD" compute instances delete "$INSTANCE_NAME" \
    --project="$PROJECT_ID" \
    --zone="$ZONE" \
    --quiet >/dev/null 2>&1 || true
  "$GCLOUD" storage rm --recursive "gs://${BUCKET_NAME}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

"$GCLOUD" config set project "$PROJECT_ID" >/dev/null
"$GCLOUD" services enable compute.googleapis.com storage.googleapis.com --project="$PROJECT_ID"

ARCHIVE="$EVIDENCE_DIR/triton-top2-cuda-probe-${RUN_ID}.tar.gz"
tar \
  --exclude='.venv' \
  --exclude='.pytest_cache' \
  --exclude='__pycache__' \
  --exclude='*.pyc' \
  -czf "$ARCHIVE" \
  -C .. \
  triton-top2-backward-kernel

"$GCLOUD" storage buckets create "gs://${BUCKET_NAME}" \
  --project="$PROJECT_ID" \
  --location="$REGION" \
  --uniform-bucket-level-access
"$GCLOUD" storage cp "$ARCHIVE" "gs://${BUCKET_NAME}/triton-probe.tar.gz"

PROJECT_NUMBER="$("$GCLOUD" projects describe "$PROJECT_ID" --format='value(projectNumber)')"
COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
"$GCLOUD" storage buckets add-iam-policy-binding "gs://${BUCKET_NAME}" \
  --member="serviceAccount:${COMPUTE_SA}" \
  --role="roles/storage.objectViewer" >/dev/null

STARTUP_SCRIPT="$EVIDENCE_DIR/startup-script.sh"
cat > "$STARTUP_SCRIPT" <<EOF
#!/usr/bin/env bash
set -euxo pipefail
exec > >(tee /var/log/triton-probe.log | logger -t triton-probe -s 2>/dev/console) 2>&1

echo "TRITON_PROBE_BEGIN"
date -u
nvidia-smi || true

mkdir -p /opt/triton-probe
cd /opt/triton-probe
if command -v gcloud >/dev/null 2>&1; then
  gcloud storage cp "gs://${BUCKET_NAME}/triton-probe.tar.gz" .
else
  gsutil cp "gs://${BUCKET_NAME}/triton-probe.tar.gz" .
fi
tar -xzf triton-probe.tar.gz
cd triton-top2-backward-kernel

bash scripts/free_cuda_runner_bootstrap.sh
python scripts/cuda_runner_probe.py

echo "TRITON_PROBE_END"
date -u
EOF

"$GCLOUD" compute instances create "$INSTANCE_NAME" \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  --machine-type="$MACHINE_TYPE" \
  --image-family="$IMAGE_FAMILY" \
  --image-project="$IMAGE_PROJECT" \
  --accelerator="type=${GPU_TYPE},count=1" \
  --maintenance-policy=TERMINATE \
  --boot-disk-size=100GB \
  --service-account="$COMPUTE_SA" \
  --scopes=https://www.googleapis.com/auth/devstorage.read_only \
  --metadata-from-file=startup-script="$STARTUP_SCRIPT"

SERIAL_LOG="$EVIDENCE_DIR/serial-console.log"
for _ in $(seq 1 80); do
  "$GCLOUD" compute instances get-serial-port-output "$INSTANCE_NAME" \
    --project="$PROJECT_ID" \
    --zone="$ZONE" \
    --port=1 > "$SERIAL_LOG" || true

  if rg -q "PASS: CUDA/Triton runner is ready|BLOCK:|TRITON_PROBE_END" "$SERIAL_LOG"; then
    break
  fi
  sleep 30
done

if rg -q "PASS: CUDA/Triton runner is ready" "$SERIAL_LOG"; then
  echo "PASS: external GCloud CUDA/Triton probe passed."
  echo "Evidence: $SERIAL_LOG"
  exit 0
fi

echo "BLOCK: external GCloud CUDA/Triton probe did not pass."
echo "Evidence: $SERIAL_LOG"
exit 2
