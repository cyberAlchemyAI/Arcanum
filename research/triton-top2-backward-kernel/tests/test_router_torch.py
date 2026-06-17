import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    import torch  # type: ignore[import-not-found]  # noqa: E402
except ModuleNotFoundError:  # pragma: no cover - exercised by non-torch runners.
    torch = None  # type: ignore[assignment]

from reference.router_reference import (  # noqa: E402
    RouterContract,
    cap2_routing_reference,
    cap2_routing_weights_rows,
    convex_sparse_topk_mask_rows,
    convex_topk_mask_direct_reference,
    finite_difference_d_w,
    fixed_mask_manual_backward,
    fixed_mask_top2_reference,
    fixture,
    normalized_pair_weight_reference,
    relu_routing_reference,
    sparsemax_routing_reference,
)
if torch is not None:
    from reference.router_torch import (  # noqa: E402
        cap2_manual_backward,
        cap2_routing_torch,
        cap2_routing_weights_torch,
        convex_sparse_topk_mask_torch,
        convex_topk_mask_direct_torch,
        fixed_mask_top2_torch,
        normalized_relu_torch,
        normalized_pair_weight_torch,
        relu_routing_torch,
        sparsemax_routing_torch,
        sparsemax_torch,
        tensors_from_fixture,
    )


def assert_nested_close(testcase: unittest.TestCase, actual, expected, *, places: int = 12) -> None:
    if isinstance(expected, list):
        testcase.assertEqual(len(actual), len(expected))
        for actual_item, expected_item in zip(actual, expected):
            assert_nested_close(testcase, actual_item, expected_item, places=places)
        return

    testcase.assertAlmostEqual(float(actual), float(expected), places=places)


@unittest.skipIf(torch is None, "torch is not available in this environment")
class TorchFixedMaskReferenceTests(unittest.TestCase):
    def test_forward_matches_standard_library_oracle(self) -> None:
        x, w, h, m, f = fixture()
        expected = fixed_mask_top2_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture()

        actual = fixed_mask_top2_torch(x_t, w_t, h_t, m_t, f_t, lambda_rec=0.7, gamma=0.2)

        for key in ("loss", "l_rec", "l_aux"):
            self.assertAlmostEqual(float(actual[key]), float(expected[key]), places=12)
        for key in ("z", "p", "a", "y", "residual", "pbar"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key])

    def test_autograd_d_w_matches_manual_oracle(self) -> None:
        x, w, h, m, f = fixture()
        expected = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture(requires_grad_w=True)

        actual = fixed_mask_top2_torch(x_t, w_t, h_t, m_t, f_t, lambda_rec=0.7, gamma=0.2)
        actual["loss"].backward()

        self.assertIsNotNone(w_t.grad)
        assert_nested_close(self, w_t.grad.tolist(), expected["d_w"])

    def test_autograd_d_w_matches_finite_difference_oracle(self) -> None:
        x, w, h, m, f = fixture()
        expected = finite_difference_d_w(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture(requires_grad_w=True)

        actual = fixed_mask_top2_torch(x_t, w_t, h_t, m_t, f_t, lambda_rec=0.7, gamma=0.2)
        actual["loss"].backward()

        self.assertIsNotNone(w_t.grad)
        assert_nested_close(self, w_t.grad.tolist(), expected, places=7)

    def test_autograd_d_h_matches_manual_oracle(self) -> None:
        x, w, h, m, f = fixture()
        expected = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture(requires_grad_h=True)

        actual = fixed_mask_top2_torch(x_t, w_t, h_t, m_t, f_t, lambda_rec=0.7, gamma=0.2)
        actual["loss"].backward()

        self.assertIsNotNone(h_t.grad)
        assert_nested_close(self, h_t.grad.tolist(), expected["d_h"])

    def test_mask_is_fixed_data_not_differentiated(self) -> None:
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture(requires_grad_w=True)

        actual = fixed_mask_top2_torch(x_t, w_t, h_t, m_t, f_t, lambda_rec=0.7, gamma=0.2)
        actual["loss"].backward()

        self.assertFalse(m_t.requires_grad)
        self.assertIsNone(m_t.grad)

    def test_contract_validation_is_preserved(self) -> None:
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture()

        with self.assertRaisesRegex(ValueError, "relaxation"):
            fixed_mask_top2_torch(
                x_t,
                w_t,
                h_t,
                m_t,
                f_t,
                contract=RouterContract(relaxation="hard_top2_gradient"),
            )

    def test_supports_fp16_forward_on_cpu_for_shape_smoke_only(self) -> None:
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture(dtype=torch.float16)

        actual = fixed_mask_top2_torch(x_t, w_t, h_t, m_t, f_t, lambda_rec=0.7, gamma=0.2)

        self.assertEqual(actual["p"].dtype, torch.float16)
        self.assertEqual(tuple(actual["y"].shape), tuple(x_t.shape))

    def test_normalized_pair_weight_torch_matches_standard_library_oracle(self) -> None:
        x, w, h, m, f = fixture()
        expected = normalized_pair_weight_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture()

        actual = normalized_pair_weight_torch(
            x_t,
            w_t,
            h_t,
            m_t,
            f_t,
            lambda_rec=0.7,
            gamma=0.2,
        )

        for key in ("loss", "l_rec", "l_aux"):
            self.assertAlmostEqual(float(actual[key]), float(expected[key]), places=12)
        for key in ("p", "masked", "a", "y", "pbar"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key])

    def test_sparsemax_torch_matches_standard_library_rows(self) -> None:
        z = torch.tensor([[2.0, 0.0, -1.0], [0.2, 0.2, 0.2]], dtype=torch.float64)

        actual = sparsemax_torch(z)

        assert_nested_close(self, actual.detach().tolist(), [[1.0, 0.0, 0.0], [1.0 / 3.0] * 3])

    def test_sparsemax_routing_torch_matches_standard_library_oracle(self) -> None:
        x, w, h, _m, f = fixture()
        expected = sparsemax_routing_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture()

        actual = sparsemax_routing_torch(x_t, w_t, h_t, f_t, lambda_rec=0.7, gamma=0.2)

        for key in ("loss", "l_rec", "l_aux"):
            self.assertAlmostEqual(float(actual[key]), float(expected[key]), places=12)
        for key in ("p", "a", "y", "pbar"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key])

    def test_normalized_relu_torch_matches_expected_rows(self) -> None:
        z = torch.tensor([[2.0, 0.0, -1.0], [1.0, 3.0, -2.0]], dtype=torch.float64)

        actual = normalized_relu_torch(z)

        assert_nested_close(self, actual.detach().tolist(), [[1.0, 0.0, 0.0], [0.25, 0.75, 0.0]])

    def test_relu_routing_torch_matches_standard_library_oracle(self) -> None:
        x, w, h, _m, f = fixture()
        expected = relu_routing_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture()

        actual = relu_routing_torch(x_t, w_t, h_t, f_t, lambda_rec=0.7, gamma=0.2)

        for key in ("loss", "l_rec", "l_aux"):
            self.assertAlmostEqual(float(actual[key]), float(expected[key]), places=12)
        for key in ("p", "a", "y", "pbar"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key])

    def test_convex_sparse_topk_mask_torch_matches_standard_library_oracle(self) -> None:
        z = torch.tensor(
            [[4.0, 1.0, -2.0, 3.0], [0.1, 2.0, 0.7, -1.0]],
            dtype=torch.float64,
        )

        actual = convex_sparse_topk_mask_torch(z, k=2, lambda_smooth=1e-2)
        expected = convex_sparse_topk_mask_rows(z.tolist(), k=2, lambda_smooth=1e-2)

        assert_nested_close(self, actual.detach().tolist(), expected, places=12)

    def test_convex_sparse_topk_mask_score_gradient_matches_finite_difference(self) -> None:
        z = torch.tensor([[0.85, -0.25, 0.35, -1.2]], dtype=torch.float64, requires_grad=True)
        coeff = torch.tensor([[0.7, -0.2, 0.5, -0.3]], dtype=torch.float64)

        mask = convex_sparse_topk_mask_torch(z, k=2, lambda_smooth=0.5)
        loss = torch.sum(mask * coeff)
        loss.backward()

        self.assertIsNotNone(z.grad)
        expected = _finite_difference_convex_mask_score_gradient(z.detach().tolist(), coeff.tolist(), lambda_smooth=0.5)
        assert_nested_close(self, z.grad.tolist(), expected, places=5)

    def test_convex_sparse_topk_mask_tie_gradient_boundary_is_documented(self) -> None:
        z = torch.tensor([[1.0, 1.0, 0.0, -1.0]], dtype=torch.float64)

        mask = convex_sparse_topk_mask_torch(z, k=2, lambda_smooth=1e-2)

        self.assertEqual(tuple(mask.shape), tuple(z.shape))

    def test_convex_topk_mask_direct_torch_matches_standard_library_forward(self) -> None:
        x, w, h, _m, f = fixture()
        expected = convex_topk_mask_direct_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture()

        actual = convex_topk_mask_direct_torch(x_t, w_t, h_t, f_t, lambda_rec=0.7, gamma=0.2)

        for key in ("loss", "l_rec", "l_aux"):
            self.assertAlmostEqual(float(actual[key]), float(expected[key]), places=10)
        for key in ("relaxed_mask", "a", "y", "pbar"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key], places=10)

    def test_cap2_routing_weights_torch_matches_standard_library_oracle(self) -> None:
        z = torch.tensor([[3.0, 1.0, -2.0, 2.0], [0.2, 1.7, -0.4, 0.9]], dtype=torch.float64)
        load = torch.tensor([0.1, 0.4, 0.2, 0.8], dtype=torch.float64)
        expected = cap2_routing_weights_rows(
            z.tolist(),
            load.tolist(),
            tau_rank=0.3,
            tau_gate=0.4,
            tau_cap=0.25,
            mu=0.7,
        )

        actual = cap2_routing_weights_torch(
            z,
            load,
            tau_rank=0.3,
            tau_gate=0.4,
            tau_cap=0.25,
            mu=0.7,
        )

        for key in ("z_adjusted", "p", "soft_rank", "membership", "gated", "a"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key], places=12)
        assert_nested_close(self, actual["overload"].detach().tolist(), expected["overload"], places=12)

    def test_cap2_routing_torch_matches_standard_library_forward(self) -> None:
        x, w, h, _m, f = fixture()
        expected = cap2_routing_reference(x, w, h, f, f, lambda_rec=0.7, gamma=0.2)
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture()

        actual = cap2_routing_torch(x_t, w_t, h_t, f_t, f_t, lambda_rec=0.7, gamma=0.2)

        for key in ("loss", "l_rec", "l_aux"):
            self.assertAlmostEqual(float(actual[key]), float(expected[key]), places=12)
        for key in ("z_adjusted", "p", "soft_rank", "membership", "gated", "a", "y", "pbar"):
            assert_nested_close(self, actual[key].detach().tolist(), expected[key], places=12)

    def test_cap2_capacity_pressure_reduces_overloaded_expert_weight(self) -> None:
        z = torch.tensor([[2.0, 1.9, 0.0, -1.0]], dtype=torch.float64)
        no_pressure = cap2_routing_weights_torch(z, torch.zeros(4, dtype=torch.float64), tau_cap=0.25, mu=0.0)
        pressured = cap2_routing_weights_torch(
            z,
            torch.tensor([1.0, 0.0, 0.0, 0.0], dtype=torch.float64),
            tau_cap=0.25,
            mu=2.0,
        )

        self.assertLess(float(pressured["a"][0, 0]), float(no_pressure["a"][0, 0]))
        self.assertLess(float(pressured["z_adjusted"][0, 0]), float(no_pressure["z_adjusted"][0, 0]))

    def test_cap2_gradcheck_w_and_h_for_fixed_load_graph(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(
            dtype=torch.float64,
            requires_grad_w=True,
            requires_grad_h=True,
        )
        load_t = f_t.detach().clone()

        def loss_fn(w_arg, h_arg):
            return cap2_routing_torch(
                x_t,
                w_arg,
                h_arg,
                load_t,
                f_t,
                lambda_rec=0.7,
                gamma=0.2,
                tau_rank=0.6,
                tau_gate=0.7,
                tau_cap=0.4,
                mu=0.5,
            )["loss"]

        self.assertTrue(
            torch.autograd.gradcheck(
                loss_fn,
                (w_t, h_t),
                eps=1e-6,
                atol=1e-5,
                rtol=1e-4,
            )
        )

    def test_cap2_manual_backward_matches_autograd_w_and_h(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(
            dtype=torch.float64,
            requires_grad_w=True,
            requires_grad_h=True,
        )
        load_t = f_t.detach().clone()
        params = {
            "lambda_rec": 0.7,
            "gamma": 0.2,
            "tau_rank": 0.6,
            "tau_gate": 0.7,
            "tau_cap": 0.4,
            "mu": 0.5,
        }

        actual = cap2_routing_torch(x_t, w_t, h_t, load_t, f_t, **params)
        actual["loss"].backward()
        expected = cap2_manual_backward(x_t.detach(), w_t.detach(), h_t.detach(), load_t, f_t, **params)

        self.assertIsNotNone(w_t.grad)
        self.assertIsNotNone(h_t.grad)
        torch.testing.assert_close(expected["d_w"], w_t.grad, rtol=1e-10, atol=1e-10)
        torch.testing.assert_close(expected["d_h"], h_t.grad, rtol=1e-10, atol=1e-10)

    def test_cap2_manual_backward_d_z_matches_autograd_logits(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(dtype=torch.float64)
        load_t = f_t.detach().clone()
        params = {
            "lambda_rec": 0.7,
            "gamma": 0.2,
            "tau_rank": 0.6,
            "tau_gate": 0.7,
            "tau_cap": 0.4,
            "mu": 0.5,
        }
        z_t = (x_t @ w_t.transpose(0, 1)).detach().requires_grad_(True)

        cap2 = cap2_routing_weights_torch(
            z_t,
            load_t,
            tau_rank=params["tau_rank"],
            tau_gate=params["tau_gate"],
            tau_cap=params["tau_cap"],
            mu=params["mu"],
        )
        y_t = torch.einsum("te,ted->td", cap2["a"], h_t)
        residual = y_t - x_t
        l_rec = x_t.new_tensor(params["lambda_rec"]) * torch.sum(residual * residual)
        pbar = cap2["p"].mean(dim=0)
        l_aux = x_t.new_tensor(params["gamma"]) * x_t.new_tensor(w_t.shape[0]) * torch.sum(f_t * pbar)
        (l_rec + l_aux).backward()

        expected = cap2_manual_backward(x_t, w_t, h_t, load_t, f_t, **params)

        self.assertIsNotNone(z_t.grad)
        torch.testing.assert_close(expected["d_z"], z_t.grad, rtol=1e-10, atol=1e-10)

    def test_cap2_manual_backward_d_w_matches_finite_difference(self) -> None:
        x_t, w_t, h_t, _m_t, f_t = tensors_from_fixture(dtype=torch.float64)
        load_t = f_t.detach().clone()
        params = {
            "lambda_rec": 0.7,
            "gamma": 0.2,
            "tau_rank": 0.6,
            "tau_gate": 0.7,
            "tau_cap": 0.4,
            "mu": 0.5,
        }

        actual = cap2_manual_backward(x_t, w_t, h_t, load_t, f_t, **params)
        expected = _finite_difference_cap2_d_w(x_t, w_t, h_t, load_t, f_t, **params)

        torch.testing.assert_close(actual["d_w"], expected, rtol=1e-4, atol=1e-5)

    def test_gradcheck_w_and_h_for_fixed_mask_graph(self) -> None:
        x_t, w_t, h_t, m_t, f_t = tensors_from_fixture(
            dtype=torch.float64,
            requires_grad_w=True,
            requires_grad_h=True,
        )

        def loss_fn(w_arg, h_arg):
            return fixed_mask_top2_torch(
                x_t,
                w_arg,
                h_arg,
                m_t,
                f_t,
                lambda_rec=0.7,
                gamma=0.2,
            )["loss"]

        self.assertTrue(
            torch.autograd.gradcheck(
                loss_fn,
                (w_t, h_t),
                eps=1e-6,
                atol=1e-5,
                rtol=1e-4,
            )
        )


def _finite_difference_convex_mask_score_gradient(
    z,
    coeff,
    *,
    lambda_smooth: float,
    eps: float = 1e-6,
):
    grad = [[0.0 for _ in row] for row in z]

    def objective(z_rows) -> float:
        mask = convex_sparse_topk_mask_rows(z_rows, k=2, lambda_smooth=lambda_smooth)
        return sum(mask_tj * coeff_tj for mask_row, coeff_row in zip(mask, coeff) for mask_tj, coeff_tj in zip(mask_row, coeff_row))

    for row_idx, row in enumerate(z):
        for col_idx, _value in enumerate(row):
            z_plus = [r[:] for r in z]
            z_minus = [r[:] for r in z]
            z_plus[row_idx][col_idx] += eps
            z_minus[row_idx][col_idx] -= eps
            grad[row_idx][col_idx] = (objective(z_plus) - objective(z_minus)) / (2.0 * eps)
    return grad


def _finite_difference_cap2_d_w(
    x_t: "torch.Tensor",
    w_t: "torch.Tensor",
    h_t: "torch.Tensor",
    load_t: "torch.Tensor",
    f_t: "torch.Tensor",
    *,
    lambda_rec: float,
    gamma: float,
    tau_rank: float,
    tau_gate: float,
    tau_cap: float,
    mu: float,
    eps: float = 1e-6,
) -> "torch.Tensor":
    grad = torch.zeros_like(w_t)

    def objective(w_arg: "torch.Tensor") -> "torch.Tensor":
        return cap2_routing_torch(
            x_t,
            w_arg,
            h_t,
            load_t,
            f_t,
            lambda_rec=lambda_rec,
            gamma=gamma,
            tau_rank=tau_rank,
            tau_gate=tau_gate,
            tau_cap=tau_cap,
            mu=mu,
        )["loss"]

    for expert_idx in range(w_t.shape[0]):
        for dim_idx in range(w_t.shape[1]):
            w_plus = w_t.detach().clone()
            w_minus = w_t.detach().clone()
            w_plus[expert_idx, dim_idx] += eps
            w_minus[expert_idx, dim_idx] -= eps
            grad[expert_idx, dim_idx] = (objective(w_plus) - objective(w_minus)) / (2.0 * eps)
    return grad


if __name__ == "__main__":
    unittest.main()
