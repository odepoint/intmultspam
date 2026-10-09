"""Adversarial controls for the locally prepared fixed/copy composition."""
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'research/copied-fixed'
spec=importlib.util.spec_from_file_location('copied_fixed_verify',HERE/'verify.py')
v=importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class CopiedFixedTests(unittest.TestCase):
    def test_frozen_certificate(self):
        self.assertEqual(v.js(v.run()),v.read(HERE/'certificate.json'))

    def test_all_strict_constraints_and_dyadic_bracket(self):
        result=v.run()
        a=result['assembly']
        self.assertEqual(len(a['constraints']),47)
        self.assertEqual(len(a['margins']),7)
        self.assertTrue(all(x>0 for x in a['constraints'].values()))
        self.assertGreater(v.KAPPA,Q(1,2**15))
        self.assertLess(v.KAPPA,Q(1,2**14))

    def test_independent_cost_rows(self):
        result=v.run();a=result['assembly'];p=a['parameters']
        e,c,r,delta=p['epsilon'],p['c'],p['alpha_squared_power'],p['delta']
        costs=[e,p['tau'],1-e*(1-p['lambda_prime']),p['tau'],
               max(e+delta,1-r+delta),e+delta,1-e]
        self.assertEqual([1-x for x in costs],list(a['margins'].values()))
        self.assertTrue(all(1-x>v.KAPPA for x in costs))
        self.assertEqual(p['q'],v.AB*(1-2*p['h']))
        self.assertEqual(a['margins']['g1']-a['minimum_margin'],p['h'])

    def test_real_lower_bound_exclusions(self):
        result=v.run()
        self.assertGreater(result['controls']['old_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR40_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR41_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR42_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR43_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR44_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR46_bit_at_new_lower'],1)
        self.assertGreater(result['controls']['PR47_bit_at_new_lower'],1)

    def test_recovery_and_every_pair_charged(self):
        c=v.data_corners()
        self.assertEqual((c['good'],c['fallback'],c['pairs']),(4073300,0,4073300))
        p=v.profile();data=p['parts']['data']
        self.assertEqual(data[1],2*(9*c['good']+47*c['fallback']))
        self.assertEqual(data[21],2*c['good'])
        self.assertEqual(data[17],2*c['good'])
        self.assertEqual(sum(t*n for t,n in data.items()),2*p['N']*528)

    def test_changed_graphs_reduce_physical_roles(self):
        p=v.profile()
        self.assertEqual([axis['original']['R'] for axis in p['axes']],[36432,48329])
        self.assertEqual([axis['original']['matched'] for axis in p['axes']],[6002,7715])
        self.assertEqual(p['W'],178378409-253*2300-150*1771)
        self.assertEqual(p['deficit'],1846900)

    def test_exact_recovery_explains_primary_modular_failures(self):
        c=v.data_corners();prime=c['prime']
        self.assertEqual((c['primary_good'],c['primary_fallback']),(4073290,10))
        self.assertEqual(len(c['exact_recovery']),10)
        for row in c['exact_recovery']:
            self.assertEqual(len(row['pivots']),47)
            self.assertEqual(row['ordered_zero_checks'],346)
            for i,value in enumerate(row['pivots']):
                q=Q(value)
                self.assertNotEqual(q,0)
                if i<=row['primary_failed_row']:
                    self.assertNotEqual(q.denominator%prime,0)
                    self.assertEqual(q.numerator%prime==0,i==row['primary_failed_row'])

    def test_zero_recovered_pivot_rejected(self):
        import data_recovery
        bad=deepcopy(v.data_corners()['exact_recovery']);bad[0]['pivots'][0]='0'
        with patch.object(data_recovery,'recover',return_value=bad):
            with self.assertRaisesRegex(ValueError,'Incomplete rational pivot proof'):v.data_corners()

    def test_corrupted_pair_coverage_rejected(self):
        original_read=v.read
        def corrupt(path):
            result=deepcopy(original_read(path))
            if path.name=='data-corners.json':result['records'][0][3]-=1
            return result
        with patch.object(v,'read',side_effect=corrupt):
            with self.assertRaisesRegex(ValueError,'Pair coverage gap'):v.data_corners()

    def test_mass_corruption_rejected(self):
        original_read=v.read
        def corrupt(path):
            result=deepcopy(original_read(path))
            if path.name=='profiles-23.json':result['blocks'][1]+=1
            return result
        with patch.object(v,'read',side_effect=corrupt):
            with self.assertRaisesRegex(ValueError,'Fixed profile mass'):v.profile()

    def test_omitted_paid_copy_detected(self):
        p=v.profile();rows=p['child_multiplicities'].copy()
        rows[1]-=p['N']
        self.assertNotEqual(sum(t*n for t,n in rows.items()),p['total_rank'])
        self.assertEqual(sum(t*n for t,n in p['parts']['paid_endpoint_copy'].items()),4073300)

    def test_mismatched_source_hash_rejected(self):
        original_read=v.read
        def corrupt(path):
            result=deepcopy(original_read(path))
            if path.name=='SOURCE.json':result['files']['scripts/copied_centers_network.py']='0'*64
            return result
        with patch.object(v,'read',side_effect=corrupt):
            with self.assertRaisesRegex(ValueError,'Pinned source changed'):v.check_sources()

    def test_assembly_boundary_rejected(self):
        result=v.run()
        with self.assertRaises(AssertionError):
            v.assembly(result['finite_bridge'],v.AB,result['assembly']['minimum_margin'],a_complex=v.AC)

    def test_balanced_transfer_negative_controls(self):
        r=v.run()
        for kw in ({'original_prefix':True},{'old_guard':True},{'old_exposures':True}):
            with self.assertRaises(AssertionError):
                v.assembly(r['finite_bridge'],v.AB,v.KAPPA,a_complex=v.AC,**kw)

    def test_float_saving_rejected(self):
        with self.assertRaises(ValueError):v.moment(2,2,{1:1},0.01)

    def test_restriction_tree_mutation_rejected(self):
        g=v.geometry();edges=g['row_tree'][:];edges[-1]=edges[0]
        with self.assertRaises(ValueError):v.tree(edges,48)

    def test_deterministic_prime_and_minor_gaps(self):
        for h in (23,25):
            e=v.exactness(h)
            self.assertTrue(all(x>0 for x in e['modulus_gaps'].values()))
            self.assertEqual(e['prime_product'],2596143476298333157846630848266239)


if __name__=='__main__':unittest.main()
