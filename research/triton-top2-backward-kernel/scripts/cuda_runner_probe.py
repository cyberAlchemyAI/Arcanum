from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str], *, cwd: Path = ROOT) -> int:
    print("$", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=cwd, text=True)
    print("exit", completed.returncode)
    return completed.returncode


def main() -> int:
    try:
        import torch
    except Exception as exc:
        print(f"BLOCK: torch import failed: {exc}")
        return 2

    print("python", sys.version)
    print("torch", torch.__version__)
    print("torch.cuda.is_available", torch.cuda.is_available())
    print("triton_available", importlib.util.find_spec("triton") is not None)
    print("nvidia-smi", shutil.which("nvidia-smi"))

    if not torch.cuda.is_available():
        print("BLOCK: CUDA is not available to PyTorch")
        return 2
    if importlib.util.find_spec("triton") is None:
        print("BLOCK: Triton is not importable")
        return 2
    if shutil.which("nvidia-smi") is None:
        print("BLOCK: nvidia-smi is not available")
        return 2

    nvidia_status = run(["nvidia-smi"])
    if nvidia_status != 0:
        return nvidia_status

    pytest_status = run([sys.executable, "-m", "pytest", "tests", "-q"])
    if pytest_status != 0:
        return pytest_status

    print("PASS: CUDA/Triton runner is ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
