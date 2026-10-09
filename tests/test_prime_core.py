from copy import deepcopy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_joint_frames import eye
from experiments.prime_core import prime_factor,compile_prime,inspect_prime


class PrimeCoreTest(unittest.TestCase):
    def test_nonbinary_coefficients_and_complete_shared_contract(self):
        for p,C in ((3,[[1,2],[2,1]]),(5,[[1,2],[3,1]]),(7,[[1,2],[4,1]])):
            U,V=prime_factor(C,p)
            self.assertEqual(len(V),1)
            self.assertEqual([[sum(x*y for x,y in zip(a,b))%p for b in zip(*V)] for a in U],C)
            candidate,expected=compile_prime(C,p,eye(2),eye(2),[1,0])
            actual=inspect_prime(candidate,require_deficit=False)
            self.assertTrue(actual['all_independent_field_inputs_checked'])
            self.assertEqual(actual['s'],expected['s'])
            self.assertEqual(actual['deficit'],expected['deficit'])

    def test_asymmetric_map_and_unshared_control(self):
        candidate,expected=compile_prime([[1,2],[0,1]],3,eye(2),eye(2))
        self.assertEqual(inspect_prime(candidate,require_deficit=False)['s'],expected['s'])

    def test_signed_exchange_correction_is_required(self):
        candidate,_=compile_prime([[1,1],[1,1]],3,eye(2),eye(2),[1,0])
        bad=deepcopy(candidate);bad['final_negated_roles']=[]
        with self.assertRaises(Exception):inspect_prime(bad,require_deficit=False)
        bad=deepcopy(candidate)
        weights=next(row for row in bad['field_coefficients'] if row)
        weights[0]=(weights[0]+1)%3
        with self.assertRaises(Exception):inspect_prime(bad,require_deficit=False)

    def test_invalid_fields_and_matrices(self):
        for p in (1,4,9):
            with self.assertRaises(Exception):prime_factor([[1,1],[1,1]],p)
        with self.assertRaises(Exception):prime_factor([[1,3],[1,1]],3)


if __name__=='__main__':unittest.main()
