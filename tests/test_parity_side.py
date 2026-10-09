from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from binary_phase_frames import basis,classify,contains,residual,orthonormal_basis
from experiments.parity_side import ParitySide
from experiments.parity_phase_repair import coarsen,characteristic,five_point_obstruction


class ParitySideTest(unittest.TestCase):
    def test_five_point_obstruction_exact_common_vector(self):
        w=five_point_obstruction()
        self.assertEqual(w['common_nonzero_vector'],15)
        self.assertTrue(contains(w['source_triples'],15))
        self.assertTrue(contains(w['target_triples'],15))

    def test_signed_scalar_kernel_and_frame_safe_coarsening(self):
        c=ParitySide(8);raw=c.verify();fixed=coarsen(c)
        self.assertEqual(raw['roles'],724)
        self.assertEqual(raw['local_obstructions'],66)
        self.assertEqual(fixed['repaired_roles'],938)
        self.assertTrue(fixed['exact_signed_coefficients_verified'])
        self.assertTrue(fixed['nonzero_residuals_nonalternating'])

    def test_characteristic_detects_alternating_residual(self):
        U=(1,2,4);self.assertEqual(characteristic(U),7)
        bad=residual((7,),U);good=residual((1,),U)
        self.assertFalse(classify(bad)['nonalternating'])
        self.assertTrue(classify(good)['nonalternating'])
        with self.assertRaises(AssertionError):orthonormal_basis(bad)
        self.assertEqual(len(orthonormal_basis(good)),2)
        with self.assertRaises(Exception):characteristic((3,))

    def test_invalid_ground_sizes(self):
        for h in (6,9,42,8.0):
            with self.assertRaises(Exception):ParitySide(h)


if __name__=='__main__':unittest.main()
