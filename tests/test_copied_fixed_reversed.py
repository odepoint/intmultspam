"""Independent failure controls for fixed-middle/copied profile composition."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
import importlib.util,json,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'research/copied-fixed-reversed'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
w=load('test_fixed_reversed_witness',HERE/'witness.py')
class FixedReversedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=w.run()
    def test_exact_frozen_certificate(self):
        self.assertEqual(w.js(self.result),json.loads((HERE/'certificate.json').read_text()))
    def test_all_constraints_and_margins(self):
        a=self.result['assembly'];self.assertEqual(len(a['constraints']),47);self.assertEqual(len(a['margins']),7)
        self.assertTrue(all(v>0 for v in a['constraints'].values()))
        self.assertTrue(all(v>w.KAPPA for v in a['margins'].values()))
        self.assertEqual(self.result['finite_bridge']['rows']['degree'],2000)
    def test_whole_profile_replaced_once(self):
        c=self.result['bit']['counts'];axes,_,_=w.prior.inputs();old=w.prior.counts(list(reversed(axes)))
        for key,value in c['parts'].items():
            if key!='internal_25':self.assertEqual(value,old['parts'][key])
        self.assertEqual(dict(sum(c['parts'].values(),Counter())),c['child_multiplicities'])
        self.assertEqual(c['parts']['paid_correction'],{1:c['N']})
        self.assertEqual(c['total_rank'],c['W']*c['m']-c['N']+c['L'])
    def test_only_identity_cleanup_changes(self):
        c=self.result['bit']['counts']['fixed_middle'];before=c['profile']['blocks'];after=c['copied_blocks']
        self.assertEqual({i:b-a for i,(a,b) in enumerate(zip(before,after)) if a!=b},{1:25,25:-25})
        self.assertEqual(sum(i*n for i,n in enumerate(after)),1283075)
    def test_data_block_split_loses_candidate(self):
        c=deepcopy(self.result['bit']['counts']);rows=c['child_multiplicities'];n=2*c['N']
        rows[17]-=n;rows[1]+=17*n
        self.assertEqual(sum(t*n for t,n in rows.items()),c['total_rank'])
        self.assertGreater(w.moment(c['m'],c['W'],rows,w.AB)['lower'],1)
    def test_bad_fixed_profile_is_rejected(self):
        original=w.read
        def corrupt(path):
            d=original(path)
            if path.name=='profile-25.json':d['blocks'][25]-=1
            return d
        with patch.object(w,'read',side_effect=corrupt),self.assertRaises(AssertionError):w.counts()
    def test_bad_source_pin_is_rejected(self):
        original=w.read
        def corrupt(path):
            d=original(path)
            if path.name=='producer-source.json':d['sha256']['research/copied-fixed-reversed/witness.py']='0'*64
            return d
        with patch.object(w,'read',side_effect=corrupt),self.assertRaises(AssertionError):w.verify_sources()
    def test_independent_crt_bound_and_failure_controls(self):
        audit=load('test_fixed_reversed_crt',HERE/'review/fixed25_copied_crt_audit.py');r=audit.run()
        self.assertGreater(r['prime_product'],r['all_minor_integer_bound'])
        self.assertEqual(len(r['negative_controls']),3)
    def test_next_bit_grid_actually_excluded(self):
        self.assertLess(self.result['bit']['upper'],1);self.assertGreater(self.result['next_bit_grid']['lower'],1)
    def test_stale_semantic_envelope_rejected(self):
        f=deepcopy(self.result['finite_bridge']);f['semantic']['E']=64*(f['complex']['W']+f['complex']['m']+1)**3
        with self.assertRaises(AssertionError):w.balanced.assembly(f,w.AB,w.KAPPA,a_complex=w.AC)
if __name__=='__main__':unittest.main()
