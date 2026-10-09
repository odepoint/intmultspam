"""Early-readout corrections and a two-return coordinate rank rejection."""
from math import comb
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_joint_return import early_program, scalar_check, joint_screen, return_credit, selected_count
from audit_block_carry import execute
from audit_joint_frames import eye, matrix, add, sub, product, rank, span_projection
from audit_cancellation import line_projection
from audit_stage_pair import kron
from rational_span_frames import orthogonal


class JointReturn(unittest.TestCase):
    def test_complete_scalar_map_and_dirty_restoration(self):
        for columns, rows in (([0,3,7],[1,4]), ([],[0]), ([1],[]), (list(range(20)),[1,4])):
            result = scalar_check(6, columns, rows)
            self.assertTrue(result['full_map_and_dirty_restoration_exact'])
            self.assertEqual(result['additional_xors'], 15*len(columns)*len(rows))
            self.assertEqual(result['additional_roles'], 0)

    def test_omitted_repairs_leave_data_right_but_scratch_wrong(self):
        good = early_program(6, [0,3,7], [1,4])
        initial = [1 << i for i in range(good['roles'])]
        expected = execute(good, initial); cut = 2*good['v']**2
        self.assertEqual(expected[cut:], initial[cut:])
        for omission in ('center_repair', 'side_repair', 'row_repair'):
            with self.subTest(omission=omission):
                bad = early_program(6, [0,3,7], [1,4], omit=omission)
                actual = execute(bad, initial)
                self.assertEqual(actual[:cut], expected[:cut])
                self.assertNotEqual(actual[cut:], initial[cut:])

    def test_both_low_frames_change_and_readout_leaves_outer_image(self):
        h = 6; k = 1; ell = 2
        I = eye(h); J = eye(h*h)
        Pa = matrix(line_projection(h, (0,1,2)))
        Pb = matrix(line_projection(h, (0,1,3)))
        def complement(t):
            outside = tuple(tuple(int(i == j) for i in range(h)) for j in range(t,h))
            return span_projection(orthogonal(outside,h),h)
        PU, PV = complement(k), complement(ell)
        E = kron(I,Pb); carry = kron(PU,Pb)
        D = kron(sub(I,Pa),I); Q = add(D,kron(Pa,PV))
        self.assertEqual(rank(sub(E,carry)), h-k)
        self.assertEqual(rank(sub(J,Q)), h-ell)
        self.assertEqual(rank(sub(Q,D)), ell)
        F = sub(J,kron(Pa,Pb))
        before_column = kron(sub(I,Pa),Pb)
        self.assertEqual(rank(before_column)+rank(sub(D,before_column))+rank(sub(F,D)),rank(F))
        self.assertNotEqual(product(F,carry), carry)
        self.assertGreaterEqual(rank(carry)+rank(sub(F,carry)), rank(F)+1)

    def test_whole_wire_charge_allows_arbitrary_rational_frames(self):
        F = matrix(((1,0,0),(0,1,0),(0,0,0)))
        M = matrix(((1,0,0),(0,0,0),(1,0,0)))
        self.assertNotEqual(product(F,M),M)
        self.assertEqual(rank(M)+rank(sub(F,M))-rank(F),1)
        # Extra intermediate cuts cannot erase the charge.
        for A in (eye(3), F, M, matrix(((0,1,0),(0,0,1),(1,0,0)))):
            self.assertGreaterEqual(rank(A)+rank(sub(M,A))+rank(sub(F,M)),rank(F)+1)

    def test_all_size_credit_identity_and_small_outside_relaxation(self):
        for h in range(6,81):
            v = comb(h,3)
            for t in range(1,h+1):
                q = selected_count(h,t)
                self.assertEqual(6*(h*h*q-v*(2*h*t-t*t)),h*t*(h-t)*(h*(h-t)-2))
                self.assertLessEqual(return_credit(h,t)*(v-1),h*h*q)
                if h-t <= 3: self.assertEqual(return_credit(h,t),h*h)
            if h >= 27: self.assertGreater(v-1,4*h*h)

    def test_every_coordinate_pair_in_retained_range(self):
        for h in (27,28,40,46,50,60):
            for k in range(1,h+1):
                for ell in range(1,h+1):
                    self.assertGreater(joint_screen(h,k,ell)['net_rank_increase_lower_bound'],0)
        # Below the sufficient threshold, the screen can fail; do not promote
        # that to a frame construction or a universal impossibility result.
        self.assertFalse(joint_screen(26,26,26)['excluded'])

    def test_full_size_numbers_credit_both_returns(self):
        one = joint_screen(50,1,1)
        self.assertEqual(one['global_Y_excess_lower_bound'],1382976)
        self.assertEqual(one['maximum_row_return_rank_credit'],232848)
        self.assertEqual(one['maximum_column_return_rank_credit'],232848)
        self.assertEqual(one['net_rank_increase_lower_bound'],917280)
        five = joint_screen(50,5,5)
        self.assertEqual(five['net_rank_increase_lower_bound'],18989100)


if __name__ == '__main__':
    unittest.main()
