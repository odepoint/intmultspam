from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.ternary_side import build,verify_invocation,verify_invocation_frames,f3add
from ternary_assembly import counts,assembly_control,KAPPA


class TernarySideTest(unittest.TestCase):
    def test_packed_field_arithmetic_exhaustive(self):
        for a in range(3):
            for b in range(3):
                for coefficient in range(-2,3):
                    A=(int(a==1),int(a==2));B=(int(b==1),int(b==2))
                    c=(a+coefficient*b)%3
                    self.assertEqual(f3add(A,B,coefficient),(int(c==1),int(c==2)))

    def test_global_signature_and_arbitrary_input_controls(self):
        for h,S in ((8,560),(9,3344)):
            c=build(h,retain_graph=True)
            self.assertEqual(c['side_roles'],S)
            self.assertTrue(c['full_small_coefficient_maps_checked'])
            self.assertTrue(verify_invocation(c)['every_auxiliary_input_restored'])

    def test_complete_rational_frame_edges(self):
        c=build(9,retain_graph=True);f=verify_invocation_frames(c)
        self.assertEqual([x['rank_sum'] for x in f['orientations']],[33084,33084])
        self.assertEqual([x['decreasing_dimensions'] for x in f['orientations']],[324,324])

    def test_exact_assembly_and_guard_reuse(self):
        n=counts();a=assembly_control(n)
        self.assertGreater(n['saving_lower'],Q(467,10**11))
        self.assertEqual(a['minimum_margin'],Q(2332833,2500000000000000))
        self.assertGreater(a['minimum_margin'],KAPPA)
        self.assertTrue(all(v>0 for v in a['constraint_slacks'].values()))
        self.assertEqual(a['guard_C1'],Q(4961,1000))
        wrong=dict(n);wrong['side_roles_per_invocation']+=1
        with self.assertRaises(Exception):assembly_control(wrong)

    def test_resource_limits(self):
        for h in (7,31,9.0):
            with self.assertRaises(Exception):build(h)
        with self.assertRaises(Exception):build(29,retain_graph=True)


if __name__=='__main__':unittest.main()
