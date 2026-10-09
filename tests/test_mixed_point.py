"""Scalar, frame and rejection controls for the bounded mixed-point audit."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_fused_block import rational_rank
from audit_mixed_point import (TARGET, dirty_side_check, enclosure_obstruction,
                              optimistic_score, scalar_check)
from experiments.mixed_point_circuit import (build, factored_transpose, kernel,
                                             plan, transpose)
from rational_span_frames import audit, basis, dot, join, nondegenerate, orthogonal


class MixedPoint(unittest.TestCase):
    def test_both_block_plans_against_complete_relation(self):
        for n,common in product((6,8,10,12),(False,True)):
            c = build(n,3,3,1,common=common)
            self.assertTrue(c.verify())
            self.assertTrue(scalar_check(c)['all_coefficients_exact'])
            self.assertLessEqual(c.additions,plan(n,3,3,1,common=common)[0])
        self.assertNotEqual(build(12,3,3,1,False).additions,
                            build(12,3,3,1,True).additions)

    def test_rectangular_transposes_and_factoring(self):
        for n,k,l,r in ((8,1,3,0),(8,2,1,0),(8,1,2,1),(8,2,2,0)):
            c = kernel(n,k,l,r)
            self.assertTrue(c.verify())
            for transform in (transpose,lambda c:factored_transpose(c)[0]):
                t = transform(c)
                self.assertTrue(t.verify())
                self.assertEqual((t.k,t.l,t.r),(l,k,r))
                self.assertLessEqual(t.additions+len(t.outputs),c.additions+len(c.outputs))

    def test_full_dirty_side_map_after_new_factoring(self):
        c = build(10,3,3,1)
        for step in range(2):
            before = c.additions
            c,_ = factored_transpose(c)
            self.assertLessEqual(c.additions,before)
            self.assertTrue(c.verify())
            result = dirty_side_check(c)
            self.assertTrue(result['all_independent_scratch_inputs_restored'])
            self.assertTrue(result['side_map_exact'])

    def test_integer_spaces_against_fraction_elimination(self):
        rng = random.Random(31031)
        for h in (4,6,8,10):
            for _ in range(12):
                rows = tuple(tuple(rng.randrange(-2,3) for _ in range(h))
                             for _ in range(rng.randrange(h+1)))
                U = basis(rows)
                self.assertEqual(len(U),rational_rank(rows))
                self.assertEqual(len(U),rational_rank(rows+U))
                gram = [[dot(a,b) for b in U] for a in U]
                self.assertEqual(nondegenerate(U),rational_rank(gram)==len(U))
                V = orthogonal(U,h)
                self.assertEqual(len(U)+len(V),h)
                self.assertTrue(all(dot(a,b)==0 for a in U for b in V))
                self.assertEqual(orthogonal(V,h),U)
        with self.assertRaises(ValueError):
            orthogonal((),9)

    def test_cut_repairs_degenerate_source_spans_in_compiled_circuits(self):
        for h,expected in ((10,16),(12,320)):
            c,_ = factored_transpose(build(h,3,3,1))
            result = audit(c)
            self.assertEqual(result['singular_source_spans'],expected)
            self.assertTrue(result['cut_certified'])
            self.assertTrue(result['compiled']['forward_nested'])
            self.assertTrue(result['compiled']['reverse_nested'])
            self.assertGreater(result['forced_dual_nodes'],expected)

    def test_orthogonal_rectangle_can_have_no_nondegenerate_enclosure(self):
        obstruction = enclosure_obstruction()
        c = SimpleNamespace(n=10,inputs=obstruction['sources'],
            targets=obstruction['targets'],args=[None,None,None,None,(1,2),(4,3)],
            active=[1,2,3,4,5],outputs=[5]*27,additions=2)
        result = audit(c)
        self.assertFalse(result['cut_certified'])
        self.assertIn(5,result['cut_failures'])
        self.assertGreater(result['local_nonzero_source_target_intersections'],0)
        self.assertNotIn('compiled',result)

    def test_optimistic_score_rejects_count_before_full_frame_work(self):
        result = optimistic_score(50,447488)
        self.assertLess(result['kappa_upper_if_no_extra_losses'],TARGET)
        budget = result['necessary_integer_role_budget']
        self.assertEqual(budget,317035)
        self.assertGreater(optimistic_score(50,budget)['kappa_upper_if_no_extra_losses'],TARGET)
        self.assertLess(optimistic_score(50,budget+1)['kappa_upper_if_no_extra_losses'],TARGET)


if __name__ == '__main__':
    unittest.main()
