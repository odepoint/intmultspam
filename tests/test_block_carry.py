"""Scalar carry compensation, dirty restoration, and rank readout screens."""
from itertools import combinations
from math import comb
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_block_carry import (block_program,execute,scalar_check,coordinate_geometry,rank_screen)
from audit_joint_frames import (matrix,eye,zero,sub,rank,product,span_projection)
from audit_cancellation import line_projection
from audit_stage_pair import kron
from rational_span_frames import orthogonal


class BlockCarry(unittest.TestCase):
    def test_full_map_with_dirty_scratch_and_no_new_roles(self):
        for columns,rows in (([0,3,7],[1,4]),([],[0]),([1,2],[]),(list(range(20)),[0,1])):
            c=scalar_check(6,columns,rows)
            self.assertTrue(c['full_map_and_dirty_restoration_exact'])
            self.assertEqual(c['additional_roles'],0)
            self.assertEqual(c['extra_xors'],6*len(columns)*len(rows))

    def test_compensating_scatter_is_necessary(self):
        good=block_program(6,[0,2,5],[1,4])
        bad=block_program(6,[0,2,5],[1,4],omit='compensating_scatter')
        initial=[1<<i for i in range(good['roles'])]
        expected=execute(good,initial);got=execute(bad,initial)
        self.assertNotEqual(got[:good['v']**2],expected[:good['v']**2])

    def test_restricted_second_gather_restores_dirty_centers(self):
        good=block_program(6,[0,2,5],[1,4])
        bad=block_program(6,[0,2,5],[1,4],omit='restoration_correction')
        initial=[1<<i for i in range(good['roles'])]
        expected=execute(good,initial);got=execute(bad,initial)
        data=2*good['v']**2
        self.assertEqual(got[:data],expected[:data])
        self.assertNotEqual(got[data:],initial[data:])
        self.assertEqual(expected[data:],initial[data:])

    def test_coordinate_space_and_degenerate_exception(self):
        for h,k in ((6,1),(8,2),(10,2),(50,5)):
            g=coordinate_geometry(h,k)
            self.assertTrue(g['nondegenerate'])
            self.assertEqual(g['deferred_targets'],comb(h,3)-comb(h-k,3))
        self.assertFalse(coordinate_geometry(10,1)['nondegenerate'])

    def test_late_projector_readout_has_a_real_rank_loop(self):
        h=6;k=2;I=eye(h);J=eye(h*h)
        U=orthogonal(tuple(tuple(int(i==j) for i in range(h)) for j in range(k,h)),h)
        PU=span_projection(U,h);Pb=matrix(line_projection(h,(1,2,3)))
        carry=kron(PU,Pb)
        for t in combinations(range(h),3):
            P=matrix(line_projection(h,t));F=sub(J,kron(P,Pb))
            contained=product(F,carry)==carry
            self.assertEqual(contained,not any(i<k for i in t))
            if not contained:
                self.assertEqual(2*rank(sub(J,F)),2)
                self.assertGreaterEqual(2*rank(sub(carry,F)),2)

    def test_arbitrary_matrix_readout_penalty_is_one_not_two(self):
        D=zero(3);F=matrix(((1,0,0),(0,1,0),(0,0,0)))
        M=matrix(((1,0,0),(0,0,0),(1,0,0)))
        self.assertEqual(rank(sub(M,D))+rank(sub(F,M))-rank(sub(F,D)),1)
        self.assertNotEqual(product(F,M),M)
        rng=random.Random(10931)
        for n in range(3,7):
            f=n-1;d=1
            D=matrix([[int(i==j and i<d) for j in range(n)] for i in range(n)])
            F=matrix([[int(i==j and i<f) for j in range(n)] for i in range(n)])
            for _ in range(12):
                M=matrix([[rng.randrange(-1,2) for _ in range(n)] for _ in range(n)])
                if any(M[-1]):
                    self.assertGreaterEqual(rank(sub(M,D))+rank(sub(F,M)),f-d+1)
            self.assertEqual(rank(sub(F,D))+rank(sub(F,F)),f-d)

    def test_all_large_h_coordinate_screens_and_small_outside_relaxation(self):
        for h in range(10,81):
            for k in range(1,h+1):
                r=rank_screen(h,k)
                self.assertGreater(r['net_rank_increase_lower_bound'],0)
                if h>=15:self.assertGreater(r['flexible_cleanup_net_increase_lower_bound'],0)
                if h-k<=3:self.assertEqual(r['maximum_return_rank_saving'],2*h*h)
        r=rank_screen(50,5,3)
        self.assertEqual(r['deferred_columns'],5410)
        self.assertEqual(r['maximum_return_rank_saving'],3*950)
        self.assertEqual(r['flexible_cleanup_net_increase_lower_bound'],3*4460)


if __name__=='__main__':unittest.main()
