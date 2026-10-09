from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.disjoint_tensor import DisjointTensor, plan, complex_counts, scalar_program
from complex_compression import invoke, saving_bounds
from test_complex_compression import Linear


class TensorDisjointness(unittest.TestCase):
    def test_exact_coefficient_maps_and_embedding(self):
        for h,k in ((4,1),(6,2),(8,3),(10,3)):
            c=DisjointTensor(h,k); result=c.verify()
            self.assertTrue(result['integer_coefficient_map_verified'])
            self.assertTrue(result['embedding_verified'])
            self.assertEqual(result['roles'],c.additions+len(c.outputs))
        self.assertEqual(DisjointTensor(8).additions,318)
        self.assertEqual(plan(26,3,3)[0],74162)

    def test_every_small_physical_phase_transition_in_both_directions(self):
        for h in (8,10):
            c=DisjointTensor(h);result=c.verify_frames(exact_bases=True)
            self.assertTrue(result['all_physical_transitions_checked'])
            self.assertTrue(result['exact_residual_bases_constructed'])

    def test_corrupted_output_and_support_are_rejected(self):
        c=DisjointTensor(8);T=next(iter(c.outputs));c.outputs[T]=1
        with self.assertRaises(ValueError):c.verify()
        c=DisjointTensor(8);c.support[-1]^=1
        with self.assertRaises(ValueError):c.verify()
        with self.assertRaises(ValueError):DisjointTensor(26,maximum_inputs=100)
        with self.assertRaises(ValueError):DisjointTensor(6).verify_frames()

    def test_all_independent_dirty_inputs_restored_by_signed_schedule(self):
        code=scalar_program(DisjointTensor(8));n=len(code['triples']);R=code['roles'];h=8
        for inverse in (False,True):
            all_values=[Linear({i:1}) for i in range(2*n+R+h+1)]
            x=all_values[:n];y=all_values[n:2*n]
            side=all_values[2*n:2*n+R];center=all_values[2*n+R:]
            old=[list(b) for b in (x,y,side,center)]
            invoke(x,y,side,center,code,inverse)
            self.assertEqual(x,old[0]);self.assertEqual(side,old[2]);self.assertEqual(center,old[3])
            self.assertEqual(y,[b+(-1 if inverse else 1)*a for a,b in zip(old[0],old[1])])

    def test_large_candidate_and_finite_ledger(self):
        c=DisjointTensor(26);result=c.verify();frames=c.verify_frames()
        self.assertEqual(result['roles'],60372)
        self.assertTrue(frames['all_physical_transitions_checked'])
        n=complex_counts(26,result['roles'])
        self.assertEqual(n['side_roles'],89622)
        self.assertEqual(n['deficit'],6678880000)
        self.assertGreater(saving_bounds(n)[0],Q(3,10**8))


if __name__=='__main__':unittest.main()
