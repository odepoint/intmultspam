from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.cube_core_family import cube_spec,cube_ledger,expand_factor,quadratic_code_base,quadratic_rank_screen,xor_permute
from experiments.rank_product_core import binary_factor,check_core


class CubeCoreFamily(unittest.TestCase):
    def test_expanded_factors_and_actual_small_ranks(self):
        for q,r in ((2,2),(4,16)):
            core=expand_factor(q)
            self.assertEqual(len(core['V']),r)
            _,basis=binary_factor(core['C'],core['specification']['n'])
            self.assertEqual(len(basis),r)

    def test_rational_cube_lines_match_compiler_contract(self):
        spec=cube_spec(2);core=expand_factor(2)
        n=spec['n'];d=spec['d']
        vectors=[[1]+[1-2*((s>>j)&1) for j in range(d-1)] for s in range(n)]
        checked=check_core(core['C'],vectors,[[int(i==j) for i in range(d)] for j in range(d)])
        self.assertEqual(checked['r'],2)
        self.assertEqual(checked['d'],4)

    def test_first_positive_tested_power_and_factor_counts(self):
        self.assertFalse(cube_spec(8)['positive_numerator'])
        s=cube_spec(16)
        self.assertTrue(s['positive_numerator'])
        self.assertEqual(s['central_factor_size'],7144448)
        self.assertEqual(s['n'],2147483648)
        self.assertEqual(s['d'],32)

    def test_square_zero_support_identity(self):
        for q in (2,4,8,16,32):
            s=cube_spec(q)
            self.assertEqual(sum(s['monomial_multiplication_coefficients']),1)
            self.assertEqual(s['monomial_multiplication_coefficients'][q],1)

    def test_raw_vs_free_side_are_distinct(self):
        raw=cube_ledger(16);free=cube_ledger(16,0)
        self.assertGreater(free['saving_lower'],raw['saving_upper'])
        self.assertEqual(free['deficit'],raw['deficit'])
        self.assertLess(raw['saving_upper'],Q(1,10**10))

    def test_xor_row_permutation_matches_independent_bit_loop(self):
        for n in (8,16,64):
            row=sum(1<<i for i in range(n) if i%3==0)
            for shift in range(n):
                expected=sum(1<<(i^shift) for i in range(n) if row>>i&1)
                self.assertEqual(xor_permute(row,shift,n),expected)

    def test_quadratic_code_generation_independent_dense_control(self):
        data=quadratic_code_base(3);basis=data['basis']
        for i in range(data['n']):
            values=[sum((truth>>x)&1 for j,truth in enumerate(basis) if i>>j&1)%2 for x in range(data['d'])]
            self.assertEqual((data['base']>>i)&1,int(i==0 or sum(values)==data['d']//2))
        screen=quadratic_rank_screen(3)
        self.assertTrue(screen['specified_core_positive_deficit_excluded'])

    def test_quadratic_screens_reject_specified_full_support_cores(self):
        for t in (4,5):
            screen=quadratic_rank_screen(t)
            self.assertTrue(screen['specified_core_positive_deficit_excluded'])
        limited=quadratic_rank_screen(5,maximum_rows=1)
        self.assertFalse(limited['specified_core_positive_deficit_excluded'])

    def test_invalid_and_oversized_inputs(self):
        for q in (1,3,0):
            with self.assertRaises(Exception):cube_spec(q)
        with self.assertRaises(Exception):expand_factor(8)
        with self.assertRaises(Exception):quadratic_code_base(7)
        with self.assertRaises(Exception):quadratic_rank_screen(3,maximum_rows=0)
        with self.assertRaises(Exception):xor_permute(0,-1,8)

if __name__=='__main__':unittest.main()
