from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.rank_product_core import check_core, check_projector_core, _compile
from experiments.shared_core import compile_shared, check_matching, target_budget
from finite_bit_contract import inspect_candidate


class SharedCore(unittest.TestCase):
    def test_expanded_all_role_contract_and_rank_savings(self):
        for rows in ([3, 3], [3, 2], [1, 2]):
            core = check_core(rows, [[1, 0], [0, 1]], [[1, 0], [0, 1]])
            unshared, _ = _compile(core, 1000)
            before = inspect_candidate(unshared, require_deficit=False)
            candidate, expected = compile_shared(core, [1, 0])
            after = inspect_candidate(candidate, require_deficit=False)
            self.assertEqual(after['s'], expected['s'])
            self.assertEqual(after['deficit'], before['deficit'])
            self.assertEqual(before['s']-after['s'],
                             expected['removed_roles']*expected['m'])
        self.assertEqual(compile_shared(check_core([3, 3], [[1, 0], [0, 1]],
                         [[1, 0], [0, 1]]), [1, 0])[0]['W'], 40)

    def test_oblique_projectors_and_asymmetric_binary_factor(self):
        core = check_projector_core([3, 2], [[[1, 1], [0, 0]], [[0, -1], [0, 1]]])
        c, expected = compile_shared(core, [1, 0])
        self.assertEqual(inspect_candidate(c, require_deficit=False)['s'], expected['s'])

    def test_matching_need_not_preserve_central_map_or_be_an_involution(self):
        core = check_core([3, 6, 4], [[1,0,0],[0,1,0],[0,0,1]],
                          [[1,0,0],[0,1,0],[0,0,1]])
        c, expected = compile_shared(core, [1,2,0])
        self.assertEqual(inspect_candidate(c, require_deficit=False)['s'], expected['s'])

    def test_invalid_matching_and_expansion_budget(self):
        core = check_core([3, 3], [[1, 0], [0, 1]], [[1, 0], [0, 1]])
        for pi in ([0, 1], [1, 1], [1], [True, False]):
            with self.assertRaises(ValueError): check_matching(core, pi)
        with self.assertRaises(ValueError): compile_shared(core, [1, 0], 51)

    def test_budget_is_hypothetical_and_counts_all_auxiliary_banks(self):
        from math import comb
        b = target_budget(comb(28, 7), comb(28, 3), 28, Q(16, 10**8))
        self.assertGreater(b['sufficient_ratio'], 6)
        self.assertLess(b['necessary_ratio'], 7)
        self.assertTrue(b['loss_preserving_side_construction_required'])
        b = target_budget(2**31, 7144448, 32, Q(16, 10**8))
        self.assertGreater(b['sufficient_ratio'], 2)
        self.assertLess(b['necessary_ratio'], Q(5, 2))


if __name__ == '__main__': unittest.main()
