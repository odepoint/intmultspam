"""Exact scalar maps, physical ranks, and the point-hyperplane scope."""
from itertools import combinations
from math import comb
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_split_centers import (normal,complement,split_graph,scalar_check,
                                 excess,exact_path_score)
from audit_joint_frames import (eye,sub,rank,product,score_graph,matrix)
from audit_cancellation import line_projection
from audit_mixed_point import dirty_side_check
from experiments.mixed_point_circuit import build,factored_transpose
from experiments.early_sharing import refactor
from rational_span_frames import basis,dot,nondegenerate


class EarlySharingAndCenters(unittest.TestCase):
    def test_expansion_preserves_full_map_and_dirty_inputs(self):
        c=build(10,3,3,1)
        for _ in range(2):
            c,_=factored_transpose(c)
        for depth,fanout in ((1,1),(2,2),(3,2),(3,4)):
            candidate,_=refactor(c,depth,fanout)
            self.assertTrue(candidate.verify())  # independent entry-by-entry map
            self.assertEqual([candidate.support[x] for x in candidate.outputs],
                             [c.support[x] for x in c.outputs])
            self.assertTrue(dirty_side_check(candidate)['all_independent_scratch_inputs_restored'])
        unchanged,_=refactor(c,1,1)
        self.assertEqual(unchanged.additions,c.additions)

    def test_invalid_expansion_limits(self):
        c=build(6,3,3,1)
        for d,f in ((0,2),(2,0),(-1,2)):
            with self.assertRaises(ValueError):
                refactor(c,d,f)

    def test_incident_span_and_indefinite_normal(self):
        for h in (6,10,12):
            rows=tuple(tuple(int(j in t) for j in range(h))
                       for t in combinations(range(h),3) if 0 in t)
            U=basis(rows)
            self.assertEqual(len(U),h-1)
            self.assertTrue(nondegenerate(U))
            n=normal(h,0)
            self.assertEqual(dot(n,n),36*(9-h))  # scaled form 9I-J
            self.assertTrue(all(dot(n,row)==0 for row in rows))
            Q=complement(h,0)
            self.assertEqual(rank(Q),1)
            self.assertEqual(product(Q,Q),Q)
            self.assertEqual(rank(sub(eye(h),Q)),h-1)
            P=matrix(line_projection(h,(0,1,2)))
            self.assertEqual(rank(product(Q,P)),0)
            self.assertEqual(rank(product(P,Q)),0)
        with self.assertRaises(ValueError):
            normal(9,0)

    def test_four_rank_saving_on_all_physical_edges(self):
        baseline=score_graph(split_graph(6,(),()))
        graph=split_graph(6,(0,),(1,))
        scores=score_graph(graph)
        self.assertEqual(scores,dict(X=100,Y=100,side=984,center=104))
        self.assertEqual(sum(scores.values()),sum(baseline.values())-4)
        self.assertTrue(scalar_check(graph)['arbitrary_side_and_center_inputs_restored'])

    def test_extra_points_pay_for_data_transitions(self):
        graph=split_graph(6,(0,1),(2,))
        scores=score_graph(graph)
        self.assertEqual(scores['X'],108)
        self.assertEqual(scores['center'],102)
        self.assertEqual(sum(scores.values()),1294)  # worse than baseline 1292
        self.assertEqual(excess(6,2,1,0)['total'],2)
        self.assertTrue(scalar_check(graph)['forward_and_inverse_exact'])
        same=score_graph(split_graph(6,(0,),(0,)))
        self.assertEqual(same['center'],106)  # overlap does not save twice

    def test_independent_rational_paths_at_h10(self):
        for A,C in (((0,),(1,)),((0,1),(2,3)),((0,1),(1,2))):
            scores=exact_path_score(10,A,C)
            delta=excess(10,len(A),len(C),len(set(A)&set(C)))
            baseline=dict(X=comb(10,3)*9,Y=comb(10,3)*9,center=300)
            self.assertEqual({k:scores[k]-baseline[k] for k in scores},
                             {k:delta[k] for k in scores})

    def test_cardinality_family_optimum(self):
        for h in (6,10,12,40,50,60):
            winner=min((excess(h,s,t,max(0,s+t-h))['total'],s,t)
                       for s in range(h+1) for t in range(h+1))
            self.assertEqual(winner,(-4,1,1))
        with self.assertRaises(ValueError):
            excess(10,2,2,3)


if __name__ == '__main__':
    unittest.main()
