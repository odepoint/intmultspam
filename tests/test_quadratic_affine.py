from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.quadratic_affine import family,vector,inner,block_projector,rank_witness
from audit_joint_frames import product,zero


class QuadraticAffine(unittest.TestCase):
    def test_counts_uniqueness_and_norms(self):
        for t,real,complex_count in ((1,4,6),(2,24,60),(3,240,1080)):
            for phases,n in ((False,real),(True,complex_count)):
                f=family(t,phases);vectors=[vector(f,i) for i in range(n)]
                self.assertEqual(f['n'],n);self.assertEqual(len(set(vectors)),n)
                for v in vectors:self.assertEqual(inner(v,v),(v[0].bit_count(),0))
        for t,n in ((3,120),(4,2160),(5,73440)):
            self.assertEqual(family(t,False,0)['n'],n)
            self.assertEqual(family(t,False,1)['n'],n)
        self.assertEqual(family(5,True)['n'],2423520)

    def test_packed_phase_inner_product_against_integer_components(self):
        f=family(2,True);vectors=[vector(f,i) for i in range(f['n'])]
        def components(v):
            s,lo,hi=v
            return [((1,0),(0,1),(-1,0),(0,-1))[((lo>>i)&1)+2*((hi>>i)&1)]
                    if s>>i&1 else (0,0) for i in range(4)]
        for u in vectors:
            a=components(u)
            for v in vectors:
                b=components(v)
                expected=(sum(x*z+y*w for (x,y),(z,w) in zip(a,b)),
                          sum(x*w-y*z for (x,y),(z,w) in zip(a,b)))
                self.assertEqual(inner(u,v),expected)

    def test_realification_has_exact_orthogonality(self):
        f=family(2,True);vectors=[vector(f,i) for i in (0,1,4,5,10,13,30,45)]
        P=[block_projector(v,4) for v in vectors]
        for i,u in enumerate(vectors):
            for j,v in enumerate(vectors):
                self.assertEqual(product(P[i],P[j])==zero(8),inner(u,v)==(0,0))

    def test_exact_rank_witness_and_rejections(self):
        r=rank_witness(1,False,None,[0,1,2,3],[0,2])
        self.assertEqual(r['binary_rank_lower'],2)
        with self.assertRaises(ValueError):rank_witness(1,False,None,[0,0],[0])
        with self.assertRaises(ValueError):rank_witness(1,False,None,[0,1],[0,0])
        with self.assertRaises(ValueError):vector(family(2),-1)
        with self.assertRaises(ValueError):family(3,True,1)


if __name__=='__main__':unittest.main()
