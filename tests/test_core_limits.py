from itertools import product,combinations
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.core_limits import binary_type_bound,dimension_limit,radial_scope,incidence_rigidity,multiplicities
from experiments.rank_product_core import binary_factor
from experiments.single_intersection import rank_of_rows


class CoreLimits(unittest.TestCase):
    def test_exhaustive_small_compatible_fitting_pairs(self):
        # For each unordered pair choose a binary directed support pattern,
        # then permit rational binary entries only if neither direction is used.
        n=3;seen=0
        choices=[(0,0,a,b) for a,b in product((0,1),repeat=2)]+[(1,0,0,0),(0,1,0,0),(1,1,0,0)]
        for assignment in product(choices,repeat=3):
            rows=[1<<i for i in range(n)];F=[[int(i==j) for j in range(n)] for i in range(n)]
            for (i,j),(a,b,c,d) in zip(combinations(range(n),2),assignment):
                rows[i]|=a<<j;rows[j]|=b<<i;F[i][j]=c;F[j][i]=d
            out=binary_type_bound(rows,F);self.assertLessEqual(n,out['universal_upper_on_n']);seen+=1
        self.assertEqual(seen,343)

    def test_side_rank_floor_for_every_four_by_four_unit_diagonal_matrix(self):
        pairs=[(i,j) for i in range(4) for j in range(4) if i!=j]
        for mask in range(1<<12):
            rows=[1<<i for i in range(4)]
            for b,(i,j) in enumerate(pairs):rows[i]|=((mask>>b)&1)<<j
            self.assertGreaterEqual(rank_of_rows(rows)+rank_of_rows([row^(1<<i) for i,row in enumerate(rows)]),4)

    def test_exact_dimension_threshold_and_radial_cases(self):
        self.assertEqual(dimension_limit()['first_excluded_dimension'],53)
        self.assertEqual(dimension_limit(auxiliary_floor=False)['first_excluded_dimension'],65)
        self.assertEqual(radial_scope()['minimum_positive_binary_rank'],5)
        for h in range(12,100):
            self.assertTrue(all(m>52 for m in multiplicities(h,h//2)[2:]))
        with self.assertRaises(ValueError):dimension_limit(0.1)

    def test_incidence_rigidity_local_matrices_and_infinite_parameters(self):
        for q in (2,4,8,16):
            out=incidence_rigidity(q,expand=q<=4)
            self.assertTrue(out['local_incidence_times_transpose_is_identity'])
            self.assertEqual(out['rigid_for_all_h_at_least'],3*q-2)
        with self.assertRaises(ValueError):incidence_rigidity(3)
        with self.assertRaises(ValueError):incidence_rigidity(8,expand=True)

    def test_bad_fitting_pairs_rejected(self):
        with self.assertRaises(ValueError):binary_type_bound([3,3],[[1,1],[0,1]])
        with self.assertRaises(ValueError):binary_type_bound([0,2],[[1,0],[0,1]])


if __name__=='__main__':unittest.main()
