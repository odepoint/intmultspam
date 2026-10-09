"""Exact routing/lift witnesses and exhaustive local completion controls."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import permutations, product as words
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_stronger_screens import FANO_DEMANDS, FANO_FLOWS, lift_control
from experiments.fano_completion import FANO_EDGES
from experiments.balanced_fano import GL2, balanced_fano, existence, execute, inverse_choice
from rank_obstructions import check_fractional_paths, scalar_lift
from finite_bit_contract import xor_gate


def brute_permutations(W, pairs):
    """Independent dense binary row arithmetic, retaining every permutation."""
    found = set()
    for word in words(range(6), repeat=len(pairs)):
        rows = [[int(i == j) for j in range(W)] for i in range(W)]
        for (a, b), k in zip(pairs, word):
            p, q = GL2[k]; x, y = rows[a], rows[b]
            rows[a] = [((p & 1)*u+((p >> 1) & 1)*v) % 2 for u, v in zip(x, y)]
            rows[b] = [((q & 1)*u+((q >> 1) & 1)*v) % 2 for u, v in zip(x, y)]
        if all(sum(row) == 1 for row in rows):
            rho = [None]*W
            for out, row in enumerate(rows): rho[row.index(1)] = out
            if None not in rho: found.add(tuple(rho))
    return found


class StrongerScreens(unittest.TestCase):
    def test_fractional_fano_witness_uses_shared_undirected_capacities(self):
        result = check_fractional_paths(FANO_EDGES, FANO_DEMANDS, FANO_FLOWS)
        self.assertEqual(result['rates'], [1, 1, 1])
        self.assertTrue(all(x <= 1 for x in result['loads']))
        self.assertGreater(result['backward_traversals'], 0)

    def test_fractional_certificate_rejects_errors_and_floats(self):
        bad = deepcopy(FANO_FLOWS); bad[0][0]['weight'] = '1'
        with self.assertRaises(ValueError): check_fractional_paths(FANO_EDGES, FANO_DEMANDS, bad)
        bad = deepcopy(FANO_FLOWS); bad[0][0]['edges'][0] = 19
        with self.assertRaises(ValueError): check_fractional_paths(FANO_EDGES, FANO_DEMANDS, bad)
        bad = deepcopy(FANO_FLOWS); bad[0][0]['weight'] = 0.5
        with self.assertRaises(ValueError): check_fractional_paths(FANO_EDGES, FANO_DEMANDS, bad)
        bad = deepcopy(FANO_FLOWS); bad[0].pop()
        with self.assertRaises(ValueError): check_fractional_paths(FANO_EDGES, FANO_DEMANDS, bad)

    def test_signed_lift_and_exact_edge_discrepancy(self):
        result = lift_control()
        self.assertEqual(result['rho'], (1, 0))
        self.assertEqual(result['check']['monomial_coefficients'], [1, -1])
        self.assertEqual(result['check']['discrepancy_rank'], 4)
        self.assertTrue(result['check']['exact_telescope'])

    def test_wrong_characteristic_zero_action_is_not_a_certificate(self):
        gates = [xor_gate(1, 0), xor_gate(0, 1), xor_gate(1, 0)]
        plus = [[[1, 1], [0, 1]]]*3
        with self.assertRaises(ValueError): scalar_lift(2, gates, plus)
        with self.assertRaises(ValueError): scalar_lift(2, gates, [[[1, 0], [0, 1]]]*3)
        scaled = [[[0, Q(1, 2)], [3, 0]], [[1, 0], [0, 1]], [[1, 0], [0, 1]]]
        result = scalar_lift(2, gates, scaled)
        self.assertEqual(result['coefficients'], [Q(1, 2), 3])

    def test_six_local_operations_and_inverses(self):
        self.assertEqual(len(set(GL2)), 6)
        for i in range(6):
            self.assertEqual(execute(2, [(0, 1), (0, 1)], [i, inverse_choice(i)]), (1, 2))

    def test_meet_in_middle_matches_9294_dense_complete_assignments(self):
        topologies = [(2, [(0, 1)]), (3, [(0, 1), (1, 2), (0, 1)]),
                      (3, [(0, 1), (1, 2), (0, 2), (0, 1)]),
                      (4, [(0, 1), (1, 2), (2, 3), (0, 2), (1, 3)])]
        count = 0
        for W, pairs in topologies:
            found = brute_permutations(W, pairs); count += 6**len(pairs)
            constraints = [{}]+[{0: a, 1: b} for a, b in permutations(range(W), 2)]
            for prescribed in constraints:
                expected = any(all(rho[i] == j for i, j in prescribed.items()) for rho in found)
                result = existence(W, pairs, prescribed)
                self.assertEqual(result['exists'], expected)
                self.assertEqual(result['exhaustive_negative'], not expected)
                if result['exists']:
                    self.assertIn(tuple(result['witness']['rho']), found)
        self.assertEqual(count, 9294)

    def test_balanced_graph_and_exhaustive_negative(self):
        model = balanced_fano()
        self.assertEqual(model['prescribed'], {0: 7, 1: 0, 2: 3})
        self.assertEqual(len(model['auxiliary_inputs']), 7)
        self.assertEqual(len(model['auxiliary_outputs']), 7)
        result = existence(model['W'], model['pairs'], model['prescribed'])
        self.assertFalse(result['exists'])
        self.assertEqual(result['prefix_assignments'], 279936)
        self.assertEqual(result['suffix_assignments'], 279936)
        self.assertEqual(result['prefix_keys'], 258156)

    def test_search_budget_and_invalid_prescriptions_do_not_close_a_model(self):
        with self.assertRaises(ValueError): existence(2, [(0, 1)]*4, half_budget=35)
        with self.assertRaises(ValueError): existence(2, [(0, 1)], {0: 1, 1: 1})
        with self.assertRaises(ValueError): existence(2, [(0, 0)])


if __name__ == '__main__':
    unittest.main()
