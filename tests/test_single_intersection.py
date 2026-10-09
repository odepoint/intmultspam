from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.single_intersection import core_parameters,minor_rows,rank_of_rows,check_minor,spectral_parity_bound,intersecting_minor_bound,verify_feature_orbit
from audit_joint_frames import matrix,rank

class SingleIntersection(unittest.TestCase):
    def test_binomial_expansion_and_feature_factor(self):
        for h,k,j in ((5,2,0),(6,3,1),(8,4,2),(9,4,3)):
            p=core_parameters(h,k,j)
            labels=[sum(1<<a for a in S) for S in combinations(range(h),k)]
            features=[]
            for l,a in enumerate(p['binomial_coefficients']):
                if a:features.extend(sum(1<<v for v in S) for S in combinations(range(h),l))
            U=[sum(1<<a for a,T in enumerate(features) if S&T==T) for S in labels]
            for i,S in enumerate(labels):
                for b,T in enumerate(labels):
                    self.assertEqual((U[i]&U[b]).bit_count()%2,int(S==T or (S&T).bit_count()==j))

    def test_odd_inclusion_cover(self):
        for h in range(4,14):
            for k in range(2,h):
                for j in range(k):
                    p=core_parameters(h,k,j)
                    for level,parent in p['level_cover'].items():
                        self.assertIn(parent,p['retained_levels'])
                        self.assertGreaterEqual(parent,level)

    def test_small_spectra_match_exact_rational_matrices(self):
        for h,k,j in ((4,2,0),(4,2,1),(6,3,1),(7,3,2)):
            labels=[sum(1<<a for a in S) for S in combinations(range(h),k)]
            C=[[int(S==T or (S&T).bit_count()==j) for T in labels] for S in labels]
            spec=spectral_parity_bound(h,k,j)
            mult=Counter()
            for e,m in zip(spec['eigenvalues'],spec['multiplicities']):mult[e]+=m
            n=len(labels)
            for e,m in mult.items():
                shifted=matrix([[C[a][b]-int(a==b)*e for b in range(n)] for a in range(n)])
                self.assertEqual(n-rank(shifted),m)
            self.assertLessEqual(spec['binary_rank_lower'],rank_of_rows(minor_rows(labels,j)))

    def test_identity_minor_bounds_against_explicit_binary_rank(self):
        for h in range(4,9):
            for k in range(2,h//2+1):
                labels=[sum(1<<a for a in S) for S in combinations(range(h),k)]
                for j in range(k):
                    bound=intersecting_minor_bound(h,k,j)
                    self.assertLessEqual(bound['binary_rank_lower'],rank_of_rows(minor_rows(labels,j)))
                    if j==k-1:self.assertTrue(bound['positive_deficit_excluded'])

    def test_fitting_rank_and_degenerate_ambient_form(self):
        for h,k,j in ((4,2,1),(6,3,1),(8,4,2)):
            labels=[sum(1<<a for a in S) for S in combinations(range(h),k)]
            F=matrix([[(S&T).bit_count()-j for T in labels] for S in labels])
            self.assertEqual(rank(F),core_parameters(h,k,j)['d'])

    def test_exact_minor_witness_and_corruption(self):
        labels=[7,11,13,14]
        out=check_minor(4,3,1,labels,[0,1,2,3])
        self.assertEqual(out['binary_rank_lower'],4)
        with self.assertRaises(Exception):check_minor(4,3,1,labels,[0,0])
        with self.assertRaises(Exception):check_minor(4,3,1,[7,11,13,1],[0])

    def test_feature_orbit_matches_full_matrix(self):
        labels=[sum(1<<a for a in S) for S in combinations(range(4),2)]
        out=verify_feature_orbit(4,2,1,labels)
        self.assertEqual(out['exact_full_binary_rank'],rank_of_rows(minor_rows(labels,1)))
        with self.assertRaises(Exception):verify_feature_orbit(4,2,1,labels[:-1])
        with self.assertRaises(Exception):verify_feature_orbit(4,2,1,labels,feature_budget=2)

    def test_invalid_parameters(self):
        for args in ((4,4,1),(4,2,2),(4,1,0),(4,2,-1)):
            with self.assertRaises(Exception):core_parameters(*args)
        with self.assertRaises(Exception):spectral_parity_bound(5,3,1)

if __name__=='__main__':unittest.main()
