from fractions import Fraction as Q
from pathlib import Path
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_joint_frames import matrix,eye,zero,product
from experiments.block_core import check_block_projectors,check_block_pair,compile_block,block_counts,block_side_budget
from finite_bit_contract import inspect_candidate
from experiments.rank_product_core import counts


def coordinate_blocks():
    return [matrix([[int(i==j and i<2) for j in range(4)] for i in range(4)]),
            matrix([[int(i==j and i>=2) for j in range(4)] for i in range(4)])]


class BlockCore(unittest.TestCase):
    def test_expanded_rank_two_network_with_and_without_reuse(self):
        core=check_block_projectors([3,3],coordinate_blocks())
        for pi in (None,[1,0]):
            candidate,expected=compile_block(core,pi)
            checked=inspect_candidate(candidate,require_deficit=False)
            self.assertEqual(checked['s'],expected['s'])
            self.assertEqual(checked['deficit'],-320)
            self.assertEqual(expected['ell'],2)

    def test_block_pair_factorization(self):
        F=eye(4);core=check_block_pair([3,3],F,2)
        self.assertEqual(core['d'],4);self.assertEqual(core['ell'],2)
        self.assertEqual(core['projections'],coordinate_blocks())
        with self.assertRaises(ValueError):check_block_pair([3,3],eye(3),2)
        bad=[list(row) for row in F];bad[0][2]=1
        with self.assertRaises(ValueError):check_block_pair([3,3],bad,2)

    def test_rank_one_regression_and_direct_sum_scaling(self):
        old=counts(10,3,4,20)
        one=block_counts(10,3,4,1,20)
        for key in ('W','m','L','s','deficit'):self.assertEqual(old[key],one[key])
        doubled=block_counts(10,3,8,2,20)
        self.assertEqual(doubled['W'],one['W'])
        for key in ('m','L','s','deficit'):self.assertEqual(doubled[key],8*one[key])
        self.assertEqual(doubled['relative_deficit'],one['relative_deficit'])

    def test_reject_nonuniform_or_nonorthogonal_labels(self):
        P=coordinate_blocks()
        with self.assertRaises(ValueError):check_block_projectors([3,3],[P[0],P[0]])
        small=matrix([[int(i==j==0) for j in range(4)] for i in range(4)])
        with self.assertRaises(ValueError):check_block_projectors([1,2],[P[0],small])
        with self.assertRaises(ValueError):block_counts(2,1,2,3,2)

    def test_hypothetical_geometry_is_not_a_witness(self):
        from math import comb
        out=block_side_budget(comb(28,3),28,28,2,Q(16,10**8))
        self.assertGreater(out['sufficient_ratio'],10)
        self.assertFalse(out['geometry_and_compressed_side_frames_supplied'])


if __name__=='__main__':unittest.main()
