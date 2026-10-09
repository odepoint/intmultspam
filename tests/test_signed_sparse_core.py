from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))

from experiments.signed_sparse_core import specification,expand_factor,ledger,budget,redundant_factor_control
from experiments.rank_product_core import binary_factor,check_core
from audit_joint_frames import eye


class SignedSparseCore(unittest.TestCase):
    def test_redundant_factor_all_role_completion(self):
        c=redundant_factor_control()
        self.assertEqual(c['complete_contract']['s'],c['expected']['s'])

    def test_complete_small_factors_and_rational_contract(self):
        for h,q in ((3,2),(5,4)):
            f=expand_factor(h,q)
            core=check_core(f['C'],f['labels'],eye(h))
            self.assertEqual(core['d'],h)
            self.assertLessEqual(core['r'],f['specification']['central_factor_size'])
            self.assertEqual(core['r'],len(f['reduced_V']))

    def test_slice_bound_in_characteristic_two(self):
        # All degrees must be included: a single homogeneous incidence rank
        # can drop modulo two. This tests the exact integer-minor argument.
        for H in range(2,9):
            for k in range(H+1):
                supports=[sum(1<<i for i in s) for s in combinations(range(H),k)]
                for L in range(H+1):
                    rows=[sum(1<<i for i,s in enumerate(supports) if p&s==p)
                          for degree in range(L+1)
                          for P in combinations(range(H),degree)
                          for p in [sum(1<<j for j in P)]]
                    basis={}
                    for row in rows:
                        while row:
                            p=row.bit_length()-1
                            if p not in basis:
                                basis[p]=row;break
                            row^=basis[p]
                    self.assertLessEqual(len(basis),comb(H,min(L,k,H-k)))

    def test_large_counts_and_actual_vs_hypothetical(self):
        s=specification(31,16)
        self.assertEqual(s['n'],9848101109760)
        self.assertEqual(s['central_factor_size'],18848917662)
        self.assertTrue(s['positive_numerator'])
        self.assertLess(s['central_factor_size'],s['coarse_factor_size'])
        self.assertLess(ledger(31,16)['saving_upper'],Q(1,10**15))
        self.assertGreater(budget(31,16)['sufficient_ratio'],Q(5555,1000))
        self.assertTrue(budget(31,16)['loss_preserving_side_construction_required'])

    def test_all_small_orthogonality_degrees(self):
        for h,q in ((2,2),(4,2),(4,4),(6,4)):
            f=expand_factor(h,q)
            self.assertTrue(all(row.bit_count()-1==f['specification']['orthogonality_degree']
                                for row in f['C']))

    def test_invalid_and_expansion_limits(self):
        for h,q in ((3,4),(4,3),(2,1),(4.0,2)):
            with self.assertRaises(Exception):specification(h,q)
        with self.assertRaises(Exception):expand_factor(31,16)
        with self.assertRaises(Exception):ledger(31,16,-1)


if __name__=='__main__':unittest.main()
