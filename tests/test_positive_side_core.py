from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_joint_frames import eye
from experiments.positive_side_core import PositiveSide,compile_positive_side
from experiments.signed_sparse_core import vectors
from finite_bit_contract import inspect_candidate


class PositiveSideCore(unittest.TestCase):
    def test_shared_sums_complete_all_role_contract(self):
        c=PositiveSide([13,14,7,11],[[1,0],[1,0],[0,1],[0,1]],'frequent-pairs')
        self.assertEqual(c.verify()['side_roles'],6)
        self.assertTrue(c.verify_invocation()['all_auxiliary_inputs_restored'])
        self.assertTrue(c.verify_frames()['all_side_rank_changes_monotone'])
        for matching in (None,[2,3,0,1]):
            network,expected=compile_positive_side(c,matching)
            actual=inspect_candidate(network,require_deficit=False)
            self.assertEqual(actual['s'],expected['s'])
            self.assertEqual(actual['deficit'],expected['deficit'])

    def test_asymmetric_central_map_and_noninvolutive_matching(self):
        c=PositiveSide([3,6,5],eye(3))
        network,expected=compile_positive_side(c,[1,2,0])
        actual=inspect_candidate(network,require_deficit=False)
        self.assertEqual(actual['s'],expected['s'])

    def test_small_signed_sharing_coefficients_and_both_frames(self):
        labels=list(vectors(4,2))
        rows=[sum(1<<j for j,y in enumerate(labels) if i==j or sum(a*b for a,b in zip(x,y))==0)
              for i,x in enumerate(labels)]
        c=PositiveSide(rows,labels,'frequent-pairs')
        self.assertEqual(c.verify()['side_roles'],30)
        self.assertTrue(c.verify_frames()['all_side_rank_changes_monotone'])
        self.assertTrue(c.verify_invocation()['forward_and_inverse_shear_verified'])

    def test_wrong_relation_and_resource_limits(self):
        with self.assertRaises(Exception):PositiveSide([3,3],[[1,0],[1,1]])
        with self.assertRaises(Exception):PositiveSide([1,2],eye(2))
        with self.assertRaises(Exception):PositiveSide([3,3],eye(2),'unknown')
        c=PositiveSide([3,3],eye(2))
        with self.assertRaises(Exception):compile_positive_side(c,[0,1])
        with self.assertRaises(Exception):compile_positive_side(c,[1,0],maximum_roles=2)


if __name__=='__main__':unittest.main()
