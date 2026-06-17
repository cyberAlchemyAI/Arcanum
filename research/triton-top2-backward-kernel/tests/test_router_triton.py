import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    import torch  # type: ignore[import-not-found]  # noqa: E402
except ModuleNotFoundError:  # pragma: no cover - exercised by non-torch runners.
    torch = None  # type: ignore[assignment]

from reference.router_reference import fixed_mask_manual_backward, fixture  # noqa: E402

if torch is not None:
    from reference.router_torch import cap2_manual_backward, tensors_from_fixture  # noqa: E402
    from reference.router_triton import (  # noqa: E402
        _triton_dot_block_size,
        cap2_row_backward_triton,
        fixed_mask_dh_triton,
        fixed_mask_dw_triton,
        fixed_mask_dx_router_triton,
        triton_available,
    )


def cuda_triton_ready() -> bool:
    return bool(torch is not None and torch.cuda.is_available() and triton_available())


@unittest.skipIf(torch is None, "PyTorch is not available in this environment")
class TritonLaunchShapeTests(unittest.TestCase):
    def test_tl_dot_block_size_uses_minimum_power_of_two_tile(self) -> None:
        self.assertEqual(_triton_dot_block_size(1), 16)
        self.assertEqual(_triton_dot_block_size(8), 16)
        self.assertEqual(_triton_dot_block_size(16), 16)
        self.assertEqual(_triton_dot_block_size(17), 32)

    def test_tl_dot_block_size_rejects_non_positive_sizes(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive"):
            _triton_dot_block_size(0)


@unittest.skipIf(not cuda_triton_ready(), "CUDA/Triton is not available in this environment")
class TritonFixedMaskDwTests(unittest.TestCase):
    def test_fixed_mask_d_w_kernel_matches_manual_reference_fixture(self) -> None:
        x, w, h, m, f = fixture()
        expected = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        d_z = torch.tensor(expected["d_z"], dtype=torch.float32, device="cuda")
        x_t = torch.tensor(x, dtype=torch.float32, device="cuda")

        actual = fixed_mask_dw_triton(d_z, x_t)

        expected_t = torch.tensor(expected["d_w"], dtype=torch.float32, device="cuda")
        torch.testing.assert_close(actual, expected_t, rtol=1e-5, atol=1e-6)

    def test_fixed_mask_d_w_kernel_matches_torch_matmul_for_rectangular_case(self) -> None:
        t_size = 37
        e_size = 5
        d_size = 9
        d_z = torch.randn((t_size, e_size), device="cuda", dtype=torch.float32)
        x = torch.randn((t_size, d_size), device="cuda", dtype=torch.float32)

        actual = fixed_mask_dw_triton(d_z, x, block_e=8, block_d=8, block_t=16)
        expected = d_z.transpose(0, 1) @ x

        torch.testing.assert_close(actual, expected, rtol=1e-5, atol=1e-5)

    def test_fixed_mask_d_w_kernel_accepts_fp16_inputs_and_accumulates_fp32(self) -> None:
        d_z = torch.randn((19, 4), device="cuda", dtype=torch.float16)
        x = torch.randn((19, 7), device="cuda", dtype=torch.float16)

        actual = fixed_mask_dw_triton(d_z, x, block_e=8, block_d=8, block_t=16)
        expected = d_z.float().transpose(0, 1) @ x.float()

        self.assertEqual(actual.dtype, torch.float32)
        torch.testing.assert_close(actual, expected, rtol=2e-3, atol=2e-3)


@unittest.skipIf(not cuda_triton_ready(), "CUDA/Triton is not available in this environment")
class TritonFixedMaskDxDhTests(unittest.TestCase):
    def test_fixed_mask_d_x_router_kernel_matches_manual_reference_fixture(self) -> None:
        x, w, h, m, f = fixture()
        expected = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        d_z = torch.tensor(expected["d_z"], dtype=torch.float32, device="cuda")
        w_t = torch.tensor(w, dtype=torch.float32, device="cuda")

        actual = fixed_mask_dx_router_triton(d_z, w_t)

        expected_t = torch.tensor(expected["d_x_router"], dtype=torch.float32, device="cuda")
        torch.testing.assert_close(actual, expected_t, rtol=1e-5, atol=1e-6)

    def test_fixed_mask_d_x_router_kernel_matches_torch_matmul_for_small_shape(self) -> None:
        t_size = 13
        e_size = 5
        d_size = 7
        d_z = torch.randn((t_size, e_size), device="cuda", dtype=torch.float32)
        w = torch.randn((e_size, d_size), device="cuda", dtype=torch.float32)

        actual = fixed_mask_dx_router_triton(d_z, w, block_t=8, block_d=8, block_e=8)
        expected = d_z @ w

        torch.testing.assert_close(actual, expected, rtol=1e-5, atol=1e-5)

    def test_fixed_mask_d_x_router_kernel_accepts_fp16_inputs_and_accumulates_fp32(self) -> None:
        d_z = torch.randn((17, 5), device="cuda", dtype=torch.float16)
        w = torch.randn((5, 9), device="cuda", dtype=torch.float16)

        actual = fixed_mask_dx_router_triton(d_z, w, block_t=8, block_d=8, block_e=8)
        expected = d_z.float() @ w.float()

        self.assertEqual(actual.dtype, torch.float32)
        torch.testing.assert_close(actual, expected, rtol=2e-3, atol=2e-3)

    def test_fixed_mask_d_h_kernel_matches_manual_reference_fixture(self) -> None:
        x, w, h, m, f = fixture()
        expected = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        forward = expected["forward"]
        a = torch.tensor(forward["a"], dtype=torch.float32, device="cuda")
        d_y = torch.tensor(expected["d_y"], dtype=torch.float32, device="cuda")

        actual = fixed_mask_dh_triton(a, d_y)

        expected_t = torch.tensor(expected["d_h"], dtype=torch.float32, device="cuda")
        torch.testing.assert_close(actual, expected_t, rtol=1e-5, atol=1e-6)

    def test_fixed_mask_d_h_kernel_accepts_fp16_inputs_and_outputs_fp32(self) -> None:
        a = torch.randn((11, 4), device="cuda", dtype=torch.float16)
        d_y = torch.randn((11, 6), device="cuda", dtype=torch.float16)

        actual = fixed_mask_dh_triton(a, d_y, block_e=8, block_d=8)
        expected = a.float().unsqueeze(-1) * d_y.float().unsqueeze(1)

        self.assertEqual(actual.dtype, torch.float32)
        torch.testing.assert_close(actual, expected, rtol=2e-3, atol=2e-3)


@unittest.skipIf(not cuda_triton_ready(), "CUDA/Triton is not available in this environment")
class TritonFixedMaskAllocationTests(unittest.TestCase):
    def test_preallocated_outputs_are_reused_without_measured_cuda_allocation(self) -> None:
        t_size = 32
        e_size = 8
        d_size = 16
        d_z = torch.randn((t_size, e_size), device="cuda", dtype=torch.float32)
        x = torch.randn((t_size, d_size), device="cuda", dtype=torch.float32)
        w = torch.randn((e_size, d_size), device="cuda", dtype=torch.float32)
        a = torch.randn((t_size, e_size), device="cuda", dtype=torch.float32)
        d_y = torch.randn((t_size, d_size), device="cuda", dtype=torch.float32)
        d_w_out = torch.empty((e_size, d_size), device="cuda", dtype=torch.float32)
        d_x_out = torch.empty((t_size, d_size), device="cuda", dtype=torch.float32)
        d_h_out = torch.empty((t_size, e_size, d_size), device="cuda", dtype=torch.float32)

        fixed_mask_dw_triton(d_z, x, out=d_w_out)
        fixed_mask_dx_router_triton(d_z, w, out=d_x_out)
        fixed_mask_dh_triton(a, d_y, out=d_h_out)
        torch.cuda.synchronize()

        torch.cuda.reset_peak_memory_stats()
        before = torch.cuda.memory_allocated()
        actual_d_w = fixed_mask_dw_triton(d_z, x, out=d_w_out)
        actual_d_x = fixed_mask_dx_router_triton(d_z, w, out=d_x_out)
        actual_d_h = fixed_mask_dh_triton(a, d_y, out=d_h_out)
        torch.cuda.synchronize()
        after = torch.cuda.memory_allocated()
        peak = torch.cuda.max_memory_allocated()

        self.assertEqual(actual_d_w.data_ptr(), d_w_out.data_ptr())
        self.assertEqual(actual_d_x.data_ptr(), d_x_out.data_ptr())
        self.assertEqual(actual_d_h.data_ptr(), d_h_out.data_ptr())
        self.assertEqual(after, before)
        self.assertEqual(peak, before)

    def test_output_buffer_contract_rejects_wrong_shape_or_dtype(self) -> None:
        d_z = torch.randn((4, 3), device="cuda", dtype=torch.float32)
        x = torch.randn((4, 5), device="cuda", dtype=torch.float32)
        wrong_shape = torch.empty((3, 4), device="cuda", dtype=torch.float32)
        wrong_dtype = torch.empty((3, 5), device="cuda", dtype=torch.float16)

        with self.assertRaisesRegex(ValueError, "shape"):
            fixed_mask_dw_triton(d_z, x, out=wrong_shape)
        with self.assertRaisesRegex(ValueError, "dtype"):
            fixed_mask_dw_triton(d_z, x, out=wrong_dtype)


@unittest.skipIf(not cuda_triton_ready(), "CUDA/Triton is not available in this environment")
class TritonCap2BackwardTests(unittest.TestCase):
    def test_cap2_row_backward_matches_manual_reference_fixture(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(dtype=torch.float32, device="cuda")
        expected = cap2_manual_backward(
            x_t.cpu(),
            w_t.cpu(),
            h_t.cpu(),
            f_t.cpu(),
            f_t.cpu(),
            lambda_rec=0.7,
            gamma=0.2,
            tau_rank=0.6,
            tau_gate=0.7,
            tau_cap=0.4,
            mu=0.5,
        )

        actual = cap2_row_backward_triton(
            x_t,
            w_t,
            h_t,
            f_t,
            f_t,
            lambda_rec=0.7,
            gamma=0.2,
            tau_rank=0.6,
            tau_gate=0.7,
            tau_cap=0.4,
            mu=0.5,
        )

        torch.testing.assert_close(actual["d_z"], expected["d_z"].cuda(), rtol=2e-4, atol=2e-4)
        torch.testing.assert_close(actual["d_x_router"], expected["d_x_router"].cuda(), rtol=2e-4, atol=2e-4)
        torch.testing.assert_close(actual["d_h"], expected["d_h"].cuda(), rtol=2e-4, atol=2e-4)
        torch.testing.assert_close(actual["d_w"], expected["d_w"].cuda(), rtol=2e-4, atol=2e-4)

    def test_cap2_row_backward_matches_manual_reference_rectangular_case(self) -> None:
        torch.manual_seed(12)
        t_size = 7
        e_size = 5
        d_size = 9
        x_t = torch.randn((t_size, d_size), device="cuda", dtype=torch.float32)
        w_t = torch.randn((e_size, d_size), device="cuda", dtype=torch.float32)
        h_t = torch.randn((t_size, e_size, d_size), device="cuda", dtype=torch.float32)
        load_t = torch.rand((e_size,), device="cuda", dtype=torch.float32)
        f_t = torch.rand((e_size,), device="cuda", dtype=torch.float32)
        expected = cap2_manual_backward(
            x_t.cpu(),
            w_t.cpu(),
            h_t.cpu(),
            load_t.cpu(),
            f_t.cpu(),
            lambda_rec=0.9,
            gamma=0.15,
            tau_rank=0.8,
            tau_gate=0.9,
            tau_cap=0.6,
            mu=0.4,
        )

        actual = cap2_row_backward_triton(
            x_t,
            w_t,
            h_t,
            load_t,
            f_t,
            lambda_rec=0.9,
            gamma=0.15,
            tau_rank=0.8,
            tau_gate=0.9,
            tau_cap=0.6,
            mu=0.4,
            block_e=8,
            block_d=8,
        )

        torch.testing.assert_close(actual["d_z"], expected["d_z"].cuda(), rtol=3e-4, atol=3e-4)
        torch.testing.assert_close(actual["d_x_router"], expected["d_x_router"].cuda(), rtol=3e-4, atol=3e-4)
        torch.testing.assert_close(actual["d_h"], expected["d_h"].cuda(), rtol=3e-4, atol=3e-4)
        torch.testing.assert_close(actual["d_w"], expected["d_w"].cuda(), rtol=3e-4, atol=3e-4)

    def test_cap2_backward_reuses_preallocated_outputs(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(dtype=torch.float32, device="cuda")
        d_z_out = torch.empty((x_t.shape[0], w_t.shape[0]), device="cuda", dtype=torch.float32)
        d_x_out = torch.empty_like(x_t)
        d_h_out = torch.empty_like(h_t)
        d_w_out = torch.empty_like(w_t)

        actual = cap2_row_backward_triton(
            x_t,
            w_t,
            h_t,
            f_t,
            f_t,
            out_d_z=d_z_out,
            out_d_x_router=d_x_out,
            out_d_h=d_h_out,
            out_d_w=d_w_out,
            lambda_rec=0.7,
            gamma=0.2,
            tau_rank=0.6,
            tau_gate=0.7,
            tau_cap=0.4,
            mu=0.5,
        )

        self.assertEqual(actual["d_z"].data_ptr(), d_z_out.data_ptr())
        self.assertEqual(actual["d_x_router"].data_ptr(), d_x_out.data_ptr())
        self.assertEqual(actual["d_h"].data_ptr(), d_h_out.data_ptr())
        self.assertEqual(actual["d_w"].data_ptr(), d_w_out.data_ptr())

    def test_cap2_backward_preallocated_outputs_do_not_increase_measured_allocation(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(dtype=torch.float32, device="cuda")
        d_z_out = torch.empty((x_t.shape[0], w_t.shape[0]), device="cuda", dtype=torch.float32)
        d_x_out = torch.empty_like(x_t)
        d_h_out = torch.empty_like(h_t)
        d_w_out = torch.empty_like(w_t)
        kwargs = {
            "out_d_z": d_z_out,
            "out_d_x_router": d_x_out,
            "out_d_h": d_h_out,
            "out_d_w": d_w_out,
            "lambda_rec": 0.7,
            "gamma": 0.2,
            "tau_rank": 0.6,
            "tau_gate": 0.7,
            "tau_cap": 0.4,
            "mu": 0.5,
        }

        cap2_row_backward_triton(x_t, w_t, h_t, f_t, f_t, **kwargs)
        torch.cuda.synchronize()

        torch.cuda.reset_peak_memory_stats()
        before = torch.cuda.memory_allocated()
        actual = cap2_row_backward_triton(x_t, w_t, h_t, f_t, f_t, **kwargs)
        torch.cuda.synchronize()
        after = torch.cuda.memory_allocated()
        peak = torch.cuda.max_memory_allocated()

        self.assertEqual(actual["d_z"].data_ptr(), d_z_out.data_ptr())
        self.assertEqual(actual["d_x_router"].data_ptr(), d_x_out.data_ptr())
        self.assertEqual(actual["d_h"].data_ptr(), d_h_out.data_ptr())
        self.assertEqual(actual["d_w"].data_ptr(), d_w_out.data_ptr())
        self.assertEqual(after, before)
        self.assertEqual(peak, before)


if __name__ == "__main__":
    unittest.main()
