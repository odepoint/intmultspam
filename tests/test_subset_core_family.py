from fractions import Fraction as Q
from itertools import combinations
from math import comb
import unittest
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from audit_subset_cores import hypothetical_assembly,INTERFACE_TARGET
from experiments.rank_product_core import check_projector_core, _compile, counts
from experiments.subset_core_family import specification, ledger, side_budget, small_core, disjoint_plan, rational_companion, complex_count_screen
from finite_bit_contract import inspect_candidate
from incidence_rectangles import rectangles


class SubsetCoreFamily(unittest.TestCase):
    def test_binary_support_for_four_sizes(self):
        for q in (2,4,8,16):
            k=2*q-1;j=q-1
            spec=specification(2*k+1,q)
            self.assertEqual([t['intersection'] for t in spec['pair_types'] if t['binary_coefficient']],[j,k])
            for t in range(k+1):
                # Independent parity calculation by subset enumeration at q<=4.
                if q<=4:
                    self.assertEqual(sum(1 for _ in combinations(range(t),j))%2,int(t in (j,k)))
            self.assertEqual(spec['norm'],q)

    def test_explicit_factor_and_rational_projectors(self):
        for h,q in ((5,2),(8,4),(9,4)):
            core=small_core(h,q)
            self.assertEqual(core['r'],comb(h,q-1))
            for i,u in enumerate(core['U']):
                row=0
                for j,v in enumerate(core['V']):
                    if u>>j&1:row^=v
                self.assertTrue(row>>i&1)
            self.assertEqual(core['d'],h)

    def test_redundant_center_is_charged_by_complete_compiler(self):
        core=check_projector_core([1,2],[[[1,0],[0,0]],[[0,0],[0,1]]])
        core['r']+=1;core['V'].append(0)
        candidate,expected=_compile(core,1000)
        checked=inspect_candidate(candidate,require_deficit=False)
        self.assertEqual(checked['s'],expected['s'])
        self.assertEqual(expected,counts(2,3,2,0))

    def test_existing_triple_counts_recovered(self):
        h=50;n=comb(h,3)
        found=ledger(h,2)
        self.assertEqual(found['side_roles_per_invocation'],n*3*comb(h-3,2))
        self.assertEqual(found['deficit'],n**3-6*n*n*h*h)

    def test_seven_subset_positive_boundary(self):
        self.assertFalse(ledger(22,4)['positive'])
        self.assertTrue(ledger(23,4)['positive'])
        self.assertEqual(ledger(28,4)['deficit'],888376917657715200)

    def test_budget_brackets_direct_rank_saving(self):
        b=side_budget(28,4,INTERFACE_TARGET)
        low=b['sufficient_strict_upper_on_side_roles']
        high=b['necessary_strict_upper_on_side_roles']
        self.assertLess(low,high)
        Rlow=low.numerator//low.denominator
        Rhigh=high.numerator//high.denominator+1
        self.assertGreater(ledger(28,4,Rlow)['saving_lower'],INTERFACE_TARGET)
        self.assertLess(ledger(28,4,Rhigh)['saving_upper'],INTERFACE_TARGET)
        self.assertGreater(b['sufficient_ratio'],4)
        self.assertLess(b['necessary_ratio'],5)

    def test_hypothetical_targets_need_both_interfaces(self):
        result=hypothetical_assembly(INTERFACE_TARGET,INTERFACE_TARGET)
        self.assertTrue(result['parameter_system_passes'])
        self.assertFalse(result['finite_networks_verified'])
        self.assertFalse(result['new_guard_verified'])
        self.assertFalse(hypothetical_assembly(INTERFACE_TARGET,Q(5,10**9))['parameter_system_passes'])

    def test_disjoint_rectangle_partitions(self):
        for n,a,b in ((6,2,2),(7,3,3),(8,4,4),(9,4,4)):
            plan=disjoint_plan(n,a,b);seen=set();left=right=number=0
            for S,T in rectangles(plan):
                number+=1;left+=len(S);right+=len(T)
                for s in S:
                    for t in T:
                        self.assertFalse(set(s)&set(t))
                        self.assertNotIn((s,t),seen);seen.add((s,t))
            expected={(s,t) for s in combinations(range(n),a) for t in combinations(range(n),b) if not set(s)&set(t)}
            self.assertEqual(seen,expected)
            self.assertEqual((number,left,right),(plan.count,plan.left,plan.right))

    def test_complex_companion_support_and_guard_charge(self):
        p=rational_companion(4)
        self.assertEqual(p['values'],[Q(-5,16),0,Q(1,16),0,Q(-1,16),0,Q(5,16),1])
        for q in (2,4,8):
            p=rational_companion(q)
            self.assertEqual(p['values'][-1],1)
            self.assertTrue(all(not p['values'][t] for t in p['odd_roots']))
        for R in (None,0):
            c=complex_count_screen(28,4,R)
            power=c['strict_residual_power']
            self.assertLess(c['s'],c['m']**power)
            self.assertGreaterEqual(c['s'],c['m']**(power-1))
            self.assertFalse(c['complete_complex_frame_certificate'])
            self.assertFalse(c['original_fifth_power_guard_applies'])

    def test_invalid_and_oversized_inputs(self):
        for args in ((10,3),(7,4),(9,2),(3,1)):
            with self.assertRaises(Exception):specification(*args)
        with self.assertRaises(Exception):small_core(28,4)
        with self.assertRaises(Exception):side_budget(28,4,1.6e-7)
        with self.assertRaises(Exception):side_budget(22,4,INTERFACE_TARGET)
        with self.assertRaises(Exception):hypothetical_assembly(0.1,Q(1,10))


if __name__=='__main__':unittest.main()
