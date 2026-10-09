"""Independent scalar, phase and partition checks for complex compression."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from binary_phase_frames import (basis, classify, dot, nullspace, residual,
                                 orthonormal_basis, certify_chain)
from complex_compression import (LeaveOneCircuit, assembly_control, counts,
    disjoint_plan, invoke, mask, matching, phase_controls, rectangle_frame,
    saving_bounds, scalar_program, verify_disjoint_partition)
from incidence_rectangles import rectangles


class Linear:
    """Sparse exact rational linear form, including independent dirty inputs."""
    def __init__(self, coefficients):
        self.coefficients={k:Q(v) for k,v in coefficients.items() if v}
    def __add__(self, other):
        if other==0:return self
        c=dict(self.coefficients)
        for k,v in other.coefficients.items():c[k]=c.get(k,Q(0))+v
        return Linear(c)
    __radd__=__add__
    def __mul__(self, scalar):
        return Linear({k:v*scalar for k,v in self.coefficients.items()})
    __rmul__=__mul__
    def __sub__(self, other):return self+(-1)*other
    def __eq__(self, other):
        return isinstance(other,Linear) and self.coefficients==other.coefficients


class ComplexCompression(unittest.TestCase):
    def test_binary_basis_and_rejection_of_alternating_residual(self):
        # The even-weight plane is nondegenerate, but has no unit vector.
        full=(1,2,4)
        plane=nullspace((7,),3)
        self.assertEqual(classify(plane),dict(dimension=2,nondegenerate=True,nonalternating=False))
        with self.assertRaises(AssertionError):orthonormal_basis(plane)
        with self.assertRaises(AssertionError):certify_chain(((7,),full))
        with self.assertRaises(AssertionError):orthonormal_basis((7,4))
        self.assertEqual(len(orthonormal_basis((*plane,8))),3)
        self.assertEqual(len(orthonormal_basis(iter(full))),3)
        with self.assertRaises(AssertionError):residual((1,),(2,))
        with self.assertRaises(AssertionError):nullspace((8,),3)
        with self.assertRaises(AssertionError):basis((-1,))

    def test_local_frames_and_phase_identity(self):
        self.assertTrue(phase_controls(8)['all_local_residual_bases_constructed'])
        full=tuple(1<<i for i in range(8))
        # A source star, a target star, and a genuine coordinate rectangle.
        examples=[(((0,1,2),),((3,4,5),(3,4,6))),
                  (((3,4,5),(3,4,6)),((0,1,2),)),
                  (((0,1,2),(0,1,3)),((4,5,6),(4,5,7)))]
        def project(space,x):
            result=0
            for v in orthonormal_basis(space):
                if dot(v,x):result^=v
            return result
        for S,T in examples:
            U=rectangle_frame(S,T,8)
            for s in S:
                lower=(mask(s),)
                rb=orthonormal_basis(residual(lower,U))
                for x in range(256):
                    actual=(project(U,x).bit_count()-project(lower,x).bit_count())%4
                    expected=sum(v.bit_count()*dot(v,x) for v in rb)%4
                    self.assertEqual(actual,expected)
            self.assertEqual(len(basis(U))+len(nullspace(U,8)),8)

    def test_partitions_cover_each_relation_once(self):
        for h in (8,10,26):
            result=verify_disjoint_partition(h)
            self.assertTrue(result['every_ordered_disjoint_pair_once'])
        self.assertEqual(disjoint_plan(26).score(),491956)

    def test_leave_one_compiler_and_integer_coefficients(self):
        for n in range(3,30):
            self.assertEqual(LeaveOneCircuit(n).verify()['roles'],4*n-6)

    def test_exact_signed_invocations_restore_all_independent_scratch(self):
        code=scalar_program(8);v=len(code['triples']);R=code['roles'];h=code['h']
        for inverse in (False,True):
            all_values=[Linear({i:1}) for i in range(2*v+R+h+1)]
            x=all_values[:v];y=all_values[v:2*v]
            scratch=all_values[2*v:2*v+R];center=all_values[2*v+R:]
            original=[list(bank) for bank in (x,y,scratch,center)]
            invoke(x,y,scratch,center,code,inverse)
            self.assertEqual(x,original[0])
            sign=-1 if inverse else 1
            self.assertEqual(y,[b+sign*a for a,b in zip(original[0],original[1])])
            self.assertEqual(scratch,original[2]);self.assertEqual(center,original[3])

    def test_three_signed_stages_and_reused_dirty_bank(self):
        # Complete local bank exchange, with the stage-1 auxiliaries reused
        # after stage 2. General tensor scheduling is a separate written proof.
        code=scalar_program(8);v=len(code['triples']);R=code['roles']
        x=[Q(i-7,8) for i in range(v)];y=[Q(2*i+3,4) for i in range(v)]
        side=[Q(i%17-8,16) for i in range(R)];center=[Q(i-3,8) for i in range(9)]
        middle_side=[Q(i%13+2,8) for i in range(R)];middle_center=[Q(i+2,4) for i in range(9)]
        old=[list(b) for b in (x,y,side,center,middle_side,middle_center)]
        invoke(x,y,side,center,code)
        invoke(y,x,middle_side,middle_center,code,inverse=True)
        invoke(x,y,side,center,code)
        self.assertEqual(x,[-z for z in old[1]]);self.assertEqual(y,old[0])
        self.assertEqual([side,center,middle_side,middle_center],old[2:])

    def test_matching_and_join_residual_unit_witness(self):
        for h in (8,24,26):
            triples,pi=matching(h)
            for A,j in zip(triples,pi):
                P=triples[j]
                # e_i tensor e_k tensor e_l has norm one and belongs to
                # H intersect E-perp whenever k is outside A union pi(A).
                k=next(k for k in range(h) if k not in A and k not in P)
                self.assertEqual(dot(1<<k,mask(A)),0)
                self.assertEqual(dot(1<<k,mask(P)),0)
            self.assertTrue(all(pi[pi[i]]==i for i in range(len(pi))))
        with self.assertRaises(AssertionError):matching(25)

    def test_counts_and_conditional_assembly(self):
        n=counts(26)
        self.assertEqual(n['side_roles'],521206)
        self.assertEqual(n['deficit'],6678880000)
        self.assertGreater(saving_bounds(n)[0],Q(5,10**9))
        control=assembly_control()
        self.assertEqual(control['minimum_margin'],Q(5771,10**13))
        self.assertGreater(control['absorption_gap'],0)
        with self.assertRaises(ValueError):assembly_control(22)


if __name__=='__main__':unittest.main()
