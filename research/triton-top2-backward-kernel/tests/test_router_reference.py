import math
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from reference.router_reference import (  # noqa: E402
    RouterContract,
    cap2_routing_reference,
    cap2_routing_weights_rows,
    convex_topk_mask_direct_reference,
    convex_sparse_topk_mask_rows,
    convex_topk_normalized_masked_softmax_reference,
    finite_difference_d_w,
    fixed_mask_manual_backward,
    fixed_mask_top2_reference,
    fixture,
    max_abs_diff,
    normalized_pair_weight_reference,
    normalized_relu_rows,
    relu_routing_reference,
    sparsemax_routing_reference,
    sparsemax_rows,
    soft_routing_reference,
)


class RouterContractTests(unittest.TestCase):
    def test_v0_contract_accepts_explicit_defaults(self) -> None:
        RouterContract().validate()

    def test_contract_rejects_unresolved_relaxation(self) -> None:
        with self.assertRaisesRegex(ValueError, "relaxation"):
            RouterContract(relaxation="cap2_undefined").validate()

    def test_contract_rejects_capacity_gradient_claim(self) -> None:
        with self.assertRaisesRegex(ValueError, "capacity_mode"):
            RouterContract(capacity_mode="differentiable_penalty").validate()


class FixedMaskReferenceTests(unittest.TestCase):
    def test_forward_outputs_have_expected_shapes(self) -> None:
        x, w, h, m, f = fixture()
        out = fixed_mask_top2_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)

        self.assertEqual(len(out["z"]), len(x))
        self.assertEqual(len(out["p"][0]), len(w))
        self.assertEqual(len(out["a"]), len(x))
        self.assertEqual(len(out["y"][0]), len(x[0]))
        self.assertGreater(float(out["loss"]), 0.0)

    def test_softmax_rows_sum_to_one(self) -> None:
        x, w, h, m, f = fixture()
        out = fixed_mask_top2_reference(x, w, h, m, f)

        for row in out["p"]:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-12, abs_tol=1e-12))

    def test_masked_probabilities_match_a_equals_m_times_p(self) -> None:
        x, w, h, m, f = fixture()
        out = fixed_mask_top2_reference(x, w, h, m, f)

        for t_i, row in enumerate(out["a"]):
            for j, a_tj in enumerate(row):
                self.assertTrue(math.isclose(a_tj, m[t_i][j] * out["p"][t_i][j], abs_tol=1e-12))

    def test_manual_d_w_matches_finite_difference(self) -> None:
        x, w, h, m, f = fixture()
        backward = fixed_mask_manual_backward(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        fd = finite_difference_d_w(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)

        self.assertLess(max_abs_diff(backward["d_w"], fd), 1e-7)

    def test_auxiliary_gradient_into_p_matches_constant_coefficient(self) -> None:
        x, w, h, m, f = fixture()
        gamma = 0.2
        out = fixed_mask_top2_reference(x, w, h, m, f, lambda_rec=0.7, gamma=gamma)
        p = out["p"]
        assert isinstance(p, list)
        token_idx = 1
        expert_idx = 2
        epsilon = 1e-6
        expert_count = len(w)
        token_count = len(x)

        def aux_loss_with_coordinate(value: float) -> float:
            p_changed = [row[:] for row in p]
            p_changed[token_idx][expert_idx] = value
            pbar = [sum(row[j] for row in p_changed) / token_count for j in range(expert_count)]
            return gamma * expert_count * sum(f_j * pbar_j for f_j, pbar_j in zip(f, pbar))

        actual = (
            aux_loss_with_coordinate(p[token_idx][expert_idx] + epsilon)
            - aux_loss_with_coordinate(p[token_idx][expert_idx] - epsilon)
        ) / (2 * epsilon)
        expected = gamma * expert_count * f[expert_idx] / token_count

        self.assertAlmostEqual(actual, expected, places=10)

    def test_backward_does_not_mutate_or_differentiate_mask(self) -> None:
        x, w, h, m, f = fixture()
        m_before = [row[:] for row in m]
        fixed_mask_manual_backward(x, w, h, m, f)

        self.assertEqual(m, m_before)


class SoftRoutingBaselineTests(unittest.TestCase):
    def test_soft_routing_baseline_runs_on_same_fixture(self) -> None:
        x, w, h, _m, f = fixture()
        out = soft_routing_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)

        self.assertGreater(float(out["loss"]), 0.0)
        for row in out["a"]:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-12, abs_tol=1e-12))


class NormalizedPairWeightTests(unittest.TestCase):
    def test_normalized_pair_weights_renormalize_selected_probabilities(self) -> None:
        x, w, h, m, f = fixture()
        raw = fixed_mask_top2_reference(x, w, h, m, f)
        normalized = normalized_pair_weight_reference(x, w, h, m, f)

        for raw_row, normalized_row, mask_row in zip(raw["a"], normalized["a"], m):
            self.assertLess(sum(raw_row), 1.0)
            self.assertTrue(math.isclose(sum(normalized_row), 1.0, rel_tol=1e-12, abs_tol=1e-12))
            for normalized_value, mask_value in zip(normalized_row, mask_row):
                if mask_value == 0.0:
                    self.assertEqual(normalized_value, 0.0)

    def test_normalized_pair_weight_keeps_router_probabilities_and_aux_term(self) -> None:
        x, w, h, m, f = fixture()
        raw = fixed_mask_top2_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        normalized = normalized_pair_weight_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)

        self.assertEqual(raw["p"], normalized["p"])
        self.assertEqual(raw["pbar"], normalized["pbar"])
        self.assertTrue(math.isclose(raw["l_aux"], normalized["l_aux"], abs_tol=1e-12))
        self.assertNotEqual(raw["y"], normalized["y"])


class SparsemaxBaselineTests(unittest.TestCase):
    def test_sparsemax_rows_project_to_simplex_with_zeros(self) -> None:
        rows = sparsemax_rows([[2.0, 0.0, -1.0], [0.2, 0.2, 0.2]])

        self.assertEqual(rows[0], [1.0, 0.0, 0.0])
        for row in rows:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-12, abs_tol=1e-12))
            self.assertTrue(all(value >= 0.0 for value in row))

    def test_sparsemax_routing_baseline_runs_on_same_fixture(self) -> None:
        x, w, h, _m, f = fixture()
        out = sparsemax_routing_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)

        self.assertGreater(float(out["loss"]), 0.0)
        for row in out["p"]:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-12, abs_tol=1e-12))
            self.assertTrue(all(value >= 0.0 for value in row))


class ConvexSparseTopKExtractionTests(unittest.TestCase):
    def test_convex_sparse_topk_mask_matches_official_readme_shape(self) -> None:
        mask = convex_sparse_topk_mask_rows([[-5.0, -2.0, 3.0, 1.0]], k=2, lambda_smooth=1e-2)[0]

        self.assertAlmostEqual(mask[0], 0.0, places=12)
        self.assertAlmostEqual(mask[1], 0.0, places=12)
        self.assertAlmostEqual(mask[2], 0.99999714, places=5)
        self.assertAlmostEqual(mask[3], 0.99999714, places=5)

    def test_convex_sparse_topk_mask_has_k_positive_entries_without_boundary_ties(self) -> None:
        rows = [[4.0, 1.0, -2.0, 3.0], [0.1, 2.0, 0.7, -1.0]]

        masks = convex_sparse_topk_mask_rows(rows, k=2, lambda_smooth=1e-2)

        for row, mask in zip(rows, masks):
            selected = sorted(range(len(row)), key=lambda idx: row[idx], reverse=True)[:2]
            self.assertEqual(sum(value > 0.0 for value in mask), 2)
            for idx, value in enumerate(mask):
                if idx in selected:
                    self.assertGreater(value, 0.0)
                else:
                    self.assertEqual(value, 0.0)

    def test_convex_sparse_topk_mask_approaches_hard_topk_for_small_smoothing(self) -> None:
        mask = convex_sparse_topk_mask_rows([[4.0, 1.0, -2.0, 3.0]], k=2, lambda_smooth=1e-4)[0]

        self.assertLess(max(abs(actual - expected) for actual, expected in zip(mask, [1.0, 0.0, 0.0, 1.0])), 1e-3)


class ConvexSparseTopKRouterCompositionTests(unittest.TestCase):
    def test_mask_direct_router_uses_relaxed_mask_as_a(self) -> None:
        x, w, h, _m, f = fixture()

        out = convex_topk_mask_direct_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)

        self.assertGreater(float(out["loss"]), 0.0)
        self.assertEqual(out["a"], out["relaxed_mask"])
        self.assertEqual(out["p"], out["relaxed_mask"])
        for row in out["a"]:
            self.assertEqual(sum(value > 0.0 for value in row), 2)
            self.assertGreater(sum(row), 1.0)

    def test_normalized_masked_softmax_router_normalizes_selected_weights(self) -> None:
        x, w, h, _m, f = fixture()

        out = convex_topk_normalized_masked_softmax_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)

        self.assertGreater(float(out["loss"]), 0.0)
        for mask_row, masked_row, a_row in zip(out["relaxed_mask"], out["masked"], out["a"]):
            self.assertEqual(sum(value > 0.0 for value in mask_row), 2)
            self.assertTrue(math.isclose(sum(a_row), 1.0, rel_tol=1e-12, abs_tol=1e-12))
            for mask_value, masked_value, a_value in zip(mask_row, masked_row, a_row):
                if mask_value == 0.0:
                    self.assertEqual(masked_value, 0.0)
                    self.assertEqual(a_value, 0.0)

    def test_normalized_masked_softmax_keeps_softmax_auxiliary_probabilities(self) -> None:
        x, w, h, m, f = fixture()
        fixed = fixed_mask_top2_reference(x, w, h, m, f, lambda_rec=0.7, gamma=0.2)
        convex = convex_topk_normalized_masked_softmax_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)

        self.assertEqual(fixed["p"], convex["p"])
        self.assertEqual(fixed["pbar"], convex["pbar"])
        self.assertTrue(math.isclose(fixed["l_aux"], convex["l_aux"], abs_tol=1e-12))


class ReluRoutingBaselineTests(unittest.TestCase):
    def test_normalized_relu_rows_keep_positive_support_only(self) -> None:
        rows = normalized_relu_rows([[2.0, 0.0, -1.0], [1.0, 3.0, -2.0]])

        self.assertEqual(rows[0], [1.0, 0.0, 0.0])
        self.assertEqual(rows[1], [0.25, 0.75, 0.0])
        for row in rows:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-12, abs_tol=1e-12))
            self.assertTrue(all(value >= 0.0 for value in row))

    def test_normalized_relu_rows_reject_all_nonpositive_rows(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive logit"):
            normalized_relu_rows([[0.0, -1.0, -2.0]])

    def test_relu_routing_baseline_runs_on_same_fixture(self) -> None:
        x, w, h, _m, f = fixture()
        out = relu_routing_reference(x, w, h, f, lambda_rec=0.7, gamma=0.2)

        self.assertGreater(float(out["loss"]), 0.0)
        for row in out["p"]:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-12, abs_tol=1e-12))
            self.assertTrue(all(value >= 0.0 for value in row))


class CAP2ReferenceTests(unittest.TestCase):
    def test_cap2_weights_are_normalized_and_top2_shaped(self) -> None:
        z = [[3.0, 1.0, -2.0, 2.0]]
        load = [0.1, 0.1, 0.1, 0.1]

        out = cap2_routing_weights_rows(z, load, tau_rank=0.2, tau_gate=0.2, mu=0.0)

        self.assertTrue(math.isclose(sum(out["a"][0]), 1.0, rel_tol=1e-10, abs_tol=1e-10))
        selected = sorted(range(len(out["a"][0])), key=lambda idx: out["a"][0][idx], reverse=True)[:2]
        self.assertEqual(selected, [0, 3])
        self.assertGreater(out["membership"][0][0], out["membership"][0][1])
        self.assertGreater(out["membership"][0][3], out["membership"][0][1])

    def test_cap2_capacity_pressure_moves_weight_away_from_overloaded_expert(self) -> None:
        z = [[2.0, 1.9, 0.0, -1.0]]
        no_pressure = cap2_routing_weights_rows(z, [0.0, 0.0, 0.0, 0.0], tau_cap=0.25, mu=0.0)
        pressured = cap2_routing_weights_rows(z, [1.0, 0.0, 0.0, 0.0], tau_cap=0.25, mu=2.0)

        self.assertLess(pressured["a"][0][0], no_pressure["a"][0][0])
        self.assertLess(pressured["z_adjusted"][0][0], no_pressure["z_adjusted"][0][0])

    def test_cap2_reference_runs_on_fixture(self) -> None:
        x, w, h, _m, f = fixture()

        out = cap2_routing_reference(x, w, h, f, f, lambda_rec=0.7, gamma=0.2)

        self.assertGreater(float(out["loss"]), 0.0)
        self.assertEqual(len(out["soft_rank"]), len(x))
        for row in out["a"]:
            self.assertTrue(math.isclose(sum(row), 1.0, rel_tol=1e-10, abs_tol=1e-10))


if __name__ == "__main__":
    unittest.main()
