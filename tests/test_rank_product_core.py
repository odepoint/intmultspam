"""Two-field core, complete arbitrary-input compilation, and scoped counts."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_rank_product_core import controls, triple_core, dimension_screens, fixed_graph_rank_floor, nonselfadjoint_control
from experiments.rank_product_core import binary_factor, check_core, compile_core, counts, check_fitting_pair, compile_fitting_pair
from finite_bit_contract import inspect_candidate, scalar_permutation


class RankProductCore(unittest.TestCase):
    def test_binary_factorization_all_three_by_three_matrices(self):
        for packed in range(1 << 9):
            rows = [(packed >> (3*i)) & 7 for i in range(3)]
            U, V = binary_factor(rows, 3)
            for row, coefficients in zip(rows, U):
                rebuilt = 0
                for i, basis in enumerate(V):
                    if coefficients >> i & 1: rebuilt ^= basis
                self.assertEqual(row, rebuilt)
            pivots = [(v & -v).bit_length()-1 for v in V]
            self.assertEqual(len(set(pivots)), len(V))

    def test_expanded_controls_check_all_inputs_endpoints_and_edge_ranks(self):
        for name, rows, vectors, form in controls():
            c, expected = compile_core(rows, vectors, form)
            result = inspect_candidate(c, require_deficit=False)
            self.assertEqual(result['s'], expected['s'], name)
            self.assertEqual(result['deficit'], expected['deficit'], name)
            self.assertFalse(result['strict_transfer_contract'])
            self.assertEqual(list(scalar_permutation(c['W'], c['gates'])), c['rho'])
            with self.assertRaises(ValueError): inspect_candidate(c)

    def test_invalid_core_hypotheses_and_float_entries_are_rejected(self):
        vectors = [[1, 0], [0, 1]]; H = [[1, 0], [0, 1]]
        with self.assertRaises(ValueError): check_core([0, 2], vectors, H)
        with self.assertRaises(ValueError): check_core([3, 3], [[1, 0], [1, 1]], H)
        with self.assertRaises(ValueError): check_core([1, 2], vectors, [[1, 1], [0, 1]])
        with self.assertRaises(ValueError): check_core([1, 2], vectors, [[1, 0], [0, 0]])
        with self.assertRaises(ValueError): check_core([1, 2], [[1, 1], [0, 1]], [[1, 0], [0, -1]])
        with self.assertRaises(ValueError): check_core([1, 2], [[1.0, 0], [0, 1]], H)
        with self.assertRaises(ValueError): binary_factor([1, 4], 2)

    def test_wrong_endpoint_and_wrong_scalar_completion_fail(self):
        c, _ = compile_core([3, 2], [[1, 0], [0, 1]], [[1, 0], [0, 1]])
        wrong = deepcopy(c)
        wrong['source_frames'][0] = wrong['sink_frames'][0]
        with self.assertRaises(ValueError): inspect_candidate(wrong, require_deficit=False)
        wrong = deepcopy(c)
        gate = next(g for g in reversed(wrong['gates']) if g['xors'])
        gate['xors'].pop()
        with self.assertRaises(ValueError): inspect_candidate(wrong, require_deficit=False)

    def test_expansion_budget_is_a_failure_not_a_partial_certificate(self):
        with self.assertRaises(ValueError):
            compile_core([3, 3], [[1, 0], [0, 1]], [[1, 0], [0, 1]], maximum_roles=51)

    def test_induced_side_edge_count_matches_explicit_small_graphs(self):
        for h in (5, 6, 7):
            for removed in (0, 1, 2):
                core = triple_core(h, removed)
                labels = list(combinations(range(h), 3))[:core['n']]
                edges = sum(len(set(s) & set(t)) == 1 for s in labels for t in labels)
                self.assertEqual(edges, core['ordered_side_edges'])

    def test_positive_core_and_exact_zero_boundary(self):
        positive = triple_core(39, 12)
        boundary = triple_core(39, 13)
        self.assertEqual(positive['n'], 9127)
        self.assertEqual(positive['accounting']['deficit'], 9127**2)
        self.assertEqual(positive['accounting']['relative_deficit'], Q(1, 3066826882977))
        self.assertEqual(boundary['accounting']['deficit'], 0)
        self.assertEqual(len(positive['independent_labels']), 39)
        self.assertFalse(positive['full_network_expanded'])
        with self.assertRaises(ValueError): triple_core(9)
        with self.assertRaises(ValueError): triple_core(5, 9)

    def test_dimension_thresholds_and_retained_density(self):
        self.assertEqual([r['first_excluded_dimension'] for r in dimension_screens()], [219, 190, 53, 10])
        n = counts(19600, 50, 50, 509194)
        self.assertEqual(n['density'], Q(196, 25))
        self.assertEqual(Q(n['deficit'], n['N']), Q(23, 98))
        for r in dimension_screens():
            self.assertFalse(r['achievability_established'])

    def test_fixed_graph_binary_rank_identity_minors(self):
        for h in range(4, 53):
            c = fixed_graph_rank_floor(h)
            self.assertEqual(c['rank_lower_bound'], max(h-2, 4*(h//4)))
        c = fixed_graph_rank_floor()
        self.assertEqual(c['rank_lower_bound'], 48)
        self.assertTrue(c['fixed_side_accounting']['below_2_to_minus_30'])
        self.assertLess(c['fixed_side_accounting']['kappa_upper'], Q(1, 2**30))

    def test_nonsymmetric_fitting_matrix_needs_no_common_form(self):
        c = nonselfadjoint_control()
        self.assertFalse(c['common_nondegenerate_symmetric_form_exists'])
        self.assertEqual(c['checked']['deficit'], -189)
        rows = [5, 2, 5]; fitting = [[2, 2, 0], [-3, -3, -3], [0, 0, Q(1, 2)]]
        candidate, expected = compile_fitting_pair(rows, fitting)
        actual = inspect_candidate(candidate, require_deficit=False)
        self.assertEqual(actual['s'], expected['s'])
        self.assertEqual(actual['deficit'], -189)

    def test_fitting_matrix_requires_both_zero_directions(self):
        with self.assertRaises(ValueError): check_fitting_pair([3, 2], [[1, 0], [1, 1]])
        with self.assertRaises(ValueError): check_fitting_pair([1, 2], [[0, 1], [1, 1]])
        with self.assertRaises(ValueError): check_fitting_pair([1, 2], [[1.0, 0], [0, 1]])


if __name__ == '__main__':
    unittest.main()
