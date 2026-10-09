from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.complex_centers import factor, verify_factor, counts, invoke
from experiments.disjoint_tensor import DisjointTensor, scalar_program, complex_counts
from complex_compression import saving_bounds
from test_complex_compression import Linear


class ComplexCenters(unittest.TestCase):
    def test_integer_factor_all_entries(self):
        for h in (8,10,12):
            result=verify_factor(factor(h))
            self.assertTrue(result['integer_product_verified'])
            self.assertEqual(result['central_roles'],h)

    def test_dirty_inputs_both_signed_directions(self):
        h=8;f=factor(h);code=scalar_program(DisjointTensor(h))
        n=len(f['triples']);R=code['roles']
        for inverse in (False,True):
            values=[Linear({i:1}) for i in range(2*n+R+h)]
            x=values[:n];y=values[n:2*n];side=values[2*n:2*n+R];center=values[2*n+R:]
            old=[list(b) for b in (x,y,side,center)]
            invoke(x,y,side,center,code,f,inverse)
            self.assertEqual(x,old[0]);self.assertEqual(side,old[2]);self.assertEqual(center,old[3])
            self.assertEqual(y,[b+(-1 if inverse else 1)*a for a,b in zip(old[0],old[1])])

    def test_corrupt_factor_and_role_counts_rejected(self):
        f=factor(8);f['gather'][0]=((0,-1),)
        with self.assertRaises(ValueError):verify_factor(f)
        with self.assertRaises(ValueError):factor(9)
        f=factor(8);f['scatter'][0]=(Q(1,2),)*8
        with self.assertRaises(ValueError):verify_factor(f)
        code=scalar_program(DisjointTensor(8))
        with self.assertRaises(ValueError):invoke([],[],[],[],code,factor(8))

    def test_exact_network_saving_and_old_ledger_difference(self):
        R=60372;old=complex_counts(26,R);new=counts(26,R);n=new['v']
        self.assertEqual(old['W']-new['W'],2*n*n)
        self.assertEqual(new['deficit']-old['deficit'],6*n*n*26)
        self.assertEqual(new['central_roles'],26)
        self.assertGreater(saving_bounds(new)[0],Q(36,10**9))
        self.assertLess(new['s'],new['m']**5)


if __name__=='__main__':unittest.main()
