"""Physical joins, general matrix charges, and fusion capacity screens."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_stage_pair import (stage_pair,scalar_check,baseline,candidate_score,
    candidates,directions,modular_rank,product_matrix_rank,overlap_control,small_winner_scaling)
from audit_joint_frames import rank,sub,add,product,matrix,zero,eye,central_score
from audit_cancellation import line_projection
from math import comb


class StagePair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=stage_pair();cls.base=baseline(cls.g)

    def test_true_physical_join_and_arbitrary_scratch(self):
        g=self.g;v=g['v'];first,second=g['maps']
        self.assertEqual(len(set(first[:2*v])&set(second[:2*v])),2)
        self.assertFalse(set(first[2*v:])&set(second[2*v:]))
        self.assertEqual(len(g['roles']),418)
        self.assertTrue(scalar_check(g)['forward_and_inverse_exact'])

    def test_full_rational_score_and_only_central_excess(self):
        g=self.g;F=g['frames']
        self.assertEqual(sum(self.base),8684)
        positive=[]
        for (u,v,_),cost in zip(g['edges'],self.base):
            e=cost-rank(F[v])+rank(F[u])
            self.assertGreaterEqual(e,0)
            if e:positive.append((u,v,e))
        self.assertEqual(len(positive),12)
        self.assertEqual(sum(e for _,_,e in positive),144)
        self.assertTrue(all(u[-1]==v[-1]=='central' for u,v,_ in positive))

    def test_modular_rank_is_only_a_lower_bound(self):
        M=matrix(((101,0),(0,Q(1,2))))
        self.assertEqual(modular_rank(M),1)
        self.assertEqual(rank(M),2)
        self.assertEqual(modular_rank(M,103),2)

    def test_cross_factor_direction_is_not_a_product(self):
        E=directions(self.g)['controlled_conjugate']
        self.assertEqual(rank(E),6)
        self.assertEqual(product(E,E),E)
        self.assertEqual(product_matrix_rank(E,6),6)

    def test_affected_edge_accounting_matches_full_recomputation(self):
        g=self.g
        selected=next((changes for desc,changes in candidates(g)
                       if desc==dict(direction='crossing_line',pattern='A1_C2',change_seam=True)))
        result=candidate_score(g,self.base,selected)
        F=g['frames']|selected
        total=sum(rank(sub(F[v],F[u])) for u,v,_ in g['edges'])
        self.assertGreaterEqual(total-sum(self.base),result['rank_change_lower_bound'])
        self.assertGreater(total,sum(self.base))
        with self.assertRaises(ValueError):
            candidate_score(g,self.base,{('in',0):zero(g['m'])})

    def test_boundary_only_general_frame_change_cannot_help(self):
        g=self.g;v=list(combinations(range(g['h']),3)).index(g['a'])
        key=(0,11,v)
        changes={key:add(g['frames'][key],directions(g)['controlled_conjugate'])}
        result=candidate_score(g,self.base,changes)
        self.assertTrue(result['improvement_excluded'])
        self.assertEqual(candidate_score(g,self.base,{})['rank_change_lower_bound'],0)

    def test_block_overlap_including_dependent_labels(self):
        h=6
        vectors=[tuple(int(i in t) for i in range(h)) for t in combinations(range(h),3)]
        for q in (1,2,3,5):
            c=overlap_control(h,vectors[:q],vectors[-q:])
            self.assertEqual(c['intersection'],c['column_label_span']*c['row_label_span'])
        a,b=vectors[:2]
        c=overlap_control(h,[a,b,tuple(x+y for x,y in zip(a,b))],[a,a])
        self.assertEqual(c['intersection'],2)
        self.assertEqual(c['column_label_span'],2)
        self.assertEqual(c['row_label_span'],1)

    def test_tiny_winners_have_unfavorable_scaling(self):
        for h in (6,8,10):
            I,Z=eye(h),zero(h)
            P=matrix(line_projection(h,(0,1,2)))
            S0=2*comb(h,3)*(h-1)+3*h*h
            predicted=small_winner_scaling(h)
            self.assertEqual(central_score(h,Z,Z,Z,I)-S0,predicted['erase_one_return'])
            self.assertEqual(central_score(h,Z,I,I,I)-S0,predicted['erase_one_return'])
            one=central_score(h,Z,sub(I,P),sub(I,P),I)-S0
            two=central_score(h,Z,P,P,I)-S0
            self.assertEqual(one+two,predicted['crossing_collapse_pair'])
        for h in range(10,101):
            p=small_winner_scaling(h)
            self.assertGreater(p['erase_one_return'],0)
            self.assertGreater(p['crossing_collapse_pair'],0)
            self.assertGreater(p['crossing_collapse_with_seam_lower_bound'],0)
        self.assertEqual(small_winner_scaling(50)['erase_one_return'],34200)


if __name__=='__main__':unittest.main()
