#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-python}"
RUNNER_PYTHON_FILE=".cuda_runner_python"

probe_python() {
  "$PYTHON_BIN" - <<'PY'
import importlib.util
import torch

required = ["pytest", "numpy", "hypothesis", "torch", "triton"]
missing = [name for name in required if importlib.util.find_spec(name) is None]
if missing:
    raise SystemExit(f"missing modules: {missing}")
if not torch.cuda.is_available():
    raise SystemExit("torch.cuda.is_available is false")
PY
}

if ! probe_python; then
  echo "Python runner is missing required packages or CUDA visibility; preparing local .venv"
  if "$PYTHON_BIN" -m pip install --upgrade pip &&
    "$PYTHON_BIN" -m pip install pytest numpy hypothesis torch triton; then
    :
  else
    "$PYTHON_BIN" -m venv --system-site-packages .venv
    PYTHON_BIN=".venv/bin/python"
    "$PYTHON_BIN" -m pip install --upgrade pip
    "$PYTHON_BIN" -m pip install pytest numpy hypothesis torch triton
  fi
fi

printf '%s\n' "$PYTHON_BIN" > "$RUNNER_PYTHON_FILE"

"$PYTHON_BIN" - <<'PY'
import importlib.util
import shutil
import torch

print("torch", torch.__version__)
print("torch.cuda.is_available", torch.cuda.is_available())
print("triton_available", importlib.util.find_spec("triton") is not None)
print("nvidia-smi", shutil.which("nvidia-smi"))
PY
