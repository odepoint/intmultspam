from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.inplace_side import triple_side,central_type,compile_side,verify_prefix,invoke
from audit_joint_frames import matrix,eye,sub,rank
from audit_cancellation import line_projection
from finite_bit_contract import physical_graph
from rank_obstructions import check_fractional_paths


class InplaceSide(unittest.TestCase):
    def test_invertibility_classes_and_exact_side(self):
        for h in (6,8,10,12,14):
            self.assertEqual(central_type(h)['side_invertible'],h%4==2)
        with self.assertRaises(ValueError):compile_side(8)
        for h in (6,10):
            c=compile_side(h);self.assertEqual(c['roles'],len(c['triples']))
            for i,S in enumerate(c['triples']):
                self.assertEqual(c['rows'][i],sum(1<<j for j,T in enumerate(c['triples'])
                                                 if len(set(S)&set(T))==1))

    def test_all_independent_dirty_roles_in_both_directions(self):
        for h in (6,10):
            c=compile_side(h);n=c['roles']
            for inverse in (False,True):
                values=[1<<i for i in range(3*n+h)]
                x=values[:n];y=values[n:2*n];side=values[2*n:3*n];center=values[3*n:]
                old=[list(a) for a in (x,y,side,center)]
                invoke(x,y,side,center,c,inverse)
                self.assertEqual((x,side,center),(old[0],old[2],old[3]))
                self.assertEqual(y,[a^b for a,b in zip(old[0],old[1])])

    def test_exact_endpoint_rank_and_excess(self):
        h=6;T,_,_=triple_side(h);P=[matrix(line_projection(h,t)) for t in T]
        for i,S in enumerate(T):
            for j,U in enumerate(T):
                expected=h-2 if len(set(S)&set(U))==1 else h
                self.assertEqual(rank(sub(sub(eye(h),P[j]),P[i])),expected)

    def test_prefix_switches_are_actual_disjoint_physical_paths(self):
        c=compile_side(6);n=c['roles'];pivots=c['pivots'];indices={p:i for i,p in enumerate(pivots)}
        pairs=[];used=set()
        for t,s in c['gates']:
            j,k=indices[t],indices[s]
            if j<k and j not in used and k not in used:
                pairs.append((j,k));used.update((j,k))
                if len(pairs)==3:break
        result=verify_prefix(6,pivots,pairs)
        switch={(pivots[j],pivots[k]) for j,k in pairs}
        gates=[dict(roles=[t,s],xors=[[t,s]]) for t,s in c['gates']]
        tokens=list(c['initial']);paths=[[] for _ in range(n)];edge=0
        for t,s in c['gates']:
            for role in (t,s):paths[tokens[role]].append(edge);edge+=1
            if (t,s) in switch:tokens[t],tokens[s]=tokens[s],tokens[t]
        outputs=[None]*n
        for role,value in enumerate(tokens):paths[value].append(edge);edge+=1;outputs[value]=role
        demands=[(c['initial'].index(i),n+len(gates)+outputs[i]) for i in range(n)]
        check=check_fractional_paths([(u,v) for u,v,r in physical_graph(n,gates)],demands,
                                     [[dict(weight=1,edges=p)] for p in paths])
        self.assertEqual(check['backward_traversals'],0)
        bad=sum(len(set(c['triples'][i])&set(c['triples'][outputs[i]]))!=1 for i in range(n))
        self.assertEqual(bad,result['certified_nonorthogonal_paths'])
        with self.assertRaises(ValueError):verify_prefix(6,pivots,[(0,1),(0,2)])
        wrong=list(pivots);wrong[0],wrong[1]=wrong[1],wrong[0]
        with self.assertRaises(ValueError):verify_prefix(6,wrong,[])


if __name__=='__main__':unittest.main()
