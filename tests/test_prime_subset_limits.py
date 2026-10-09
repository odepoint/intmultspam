from pathlib import Path
from fractions import Fraction as Q
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.prime_subset_limits import characteristic,local_identity,partial_output_control,envelope,screen

class PrimeSubsetLimits(unittest.TestCase):
    def test_local_field_identity_and_factor_rank(self):
        for q in (2,3):self.assertTrue(local_identity(q,True)['expanded_local_gram_checked'])
        for q in (4,5,7,8,9,16,25):self.assertEqual(len(local_identity(q)['intersection_residues']),2*q)
        for q in (6,10,12,15):self.assertIsNone(characteristic(q))

    def test_distinct_partial_output_floor(self):
        for q,h in ((2,6),(3,9)):
            c=partial_output_control(q,h);self.assertGreater(c['minimum_terms'],1)
            self.assertTrue(c['exact_distinct_nonsingleton_supports_checked'])

    def test_all_parameter_envelope(self):
        out=screen();self.assertEqual(out['tail_dimension_exclusion']['first_excluded_dimension'],65)
        self.assertEqual(out['best_finite_upper']['q'],3)
        self.assertLess(out['best_finite_upper']['kappa_upper'],Q(1,2**26))
        self.assertFalse(envelope(3,9)['positive_deficit'])
        self.assertLess(envelope(3,29)['bit_saving_upper'],Q(8,10**8))
        with self.assertRaises(ValueError):local_identity(6)
        with self.assertRaises(ValueError):partial_output_control(3,8)

if __name__=='__main__':unittest.main()
