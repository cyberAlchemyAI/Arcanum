import importlib.util
import shutil
import subprocess
import sys
import unittest


def module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def command_available(name: str) -> bool:
    return shutil.which(name) is not None


def torch_cuda_available() -> bool | None:
    if not module_available("torch"):
        return None
    import torch  # type: ignore[import-not-found]

    return bool(torch.cuda.is_available())


class EnvironmentGateTests(unittest.TestCase):
    def test_python_version_is_supported_for_reference_work(self) -> None:
        self.assertGreaterEqual(sys.version_info, (3, 10))

    def test_optional_dependency_report_is_structured(self) -> None:
        report = {
            "pytest": module_available("pytest"),
            "numpy": module_available("numpy"),
            "hypothesis": module_available("hypothesis"),
            "torch": module_available("torch"),
            "triton": module_available("triton"),
            "nvidia_smi": command_available("nvidia-smi"),
            "nvcc": command_available("nvcc"),
            "torch_cuda": torch_cuda_available(),
        }

        self.assertEqual(set(report), {
            "pytest",
            "numpy",
            "hypothesis",
            "torch",
            "triton",
            "nvidia_smi",
            "nvcc",
            "torch_cuda",
        })

    def test_nvidia_smi_runs_when_present(self) -> None:
        if not command_available("nvidia-smi"):
            self.skipTest("nvidia-smi is not available in this environment")

        completed = subprocess.run(
            ["nvidia-smi"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
