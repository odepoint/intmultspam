"""Focused exact controls; full producer reconstruction remains a make target."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
import importlib.util,json,unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'research/copied-reversed'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
w=load('test_copied_reversed_witness',HERE/'witness.py')
g=load('test_copied_reversed_geometry',HERE/'geometry.py')

class CopiedReversedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=w.run()
    def test_frozen_witness(self):
        self.assertEqual(w.js(self.result),json.loads((HERE/'certificate.json').read_text()))
    def test_full_constraints_and_margins(self):
        a=self.result['assembly']
        self.assertEqual(len(a['constraints']),47);self.assertEqual(len(a['margins']),7)
        self.assertTrue(all(v>0 for v in a['constraints'].values()))
        self.assertTrue(all(v>w.KAPPA for v in a['margins'].values()))
        self.assertEqual(self.result['finite_bridge']['rows']['degree'],2000)
    def test_disjoint_accounting(self):
        c=self.result['bit']['counts'];parts=c['parts']
        self.assertEqual(len(c['child_multiplicities']),16)
        self.assertEqual(dict(sum(parts.values(),Counter())),c['child_multiplicities'])
        self.assertEqual(parts['paid_correction'],{1:c['N']})
        self.assertEqual(sum(t*n for t,n in c['child_multiplicities'].items()),c['W']*c['m']-c['N']+c['L'])
        axes,_,_=w.inputs();old=w.counts(axes,False)
        delta=Counter(c['child_multiplicities']);delta.subtract(old['child_multiplicities'])
        self.assertEqual({t:n for t,n in delta.items() if n},{1:-4*c['N'],15:-2*c['N'],17:2*c['N']})
    def test_rank_preserving_child_mutation_fails(self):
        c=deepcopy(self.result['bit']['counts']);rows=c['child_multiplicities'];n=rows.pop(17);rows[1]+=17*n
        self.assertEqual(sum(t*n for t,n in rows.items()),c['total_rank'])
        self.assertGreater(w.moment(c['m'],c['W'],rows,w.AB)['lower'],1)
    def test_actual_next_bit_exclusion(self):
        self.assertGreater(self.result['next_bit_grid']['lower'],1)
    def test_source_pin_corruption(self):
        original=w.read
        def corrupt(path):
            d=original(path)
            if path.name=='SOURCE.json':d['files']['witness.py']='0'*64
            return d
        with patch.object(w,'read',side_effect=corrupt),self.assertRaises(AssertionError):w.verify_sources()
    def test_geometry_bad_source(self):
        with patch.object(g.json,'loads',return_value={'commit':'wrong'}),self.assertRaises(AssertionError):g.run()
    def test_geometry_bad_rankcut(self):
        c=g.load('test_reversed23_rankcut',HERE/'pr34/independent_controls.py')
        rows,cols=c.corner_labels(23);pivots=c.expected_pivots(23)
        # Removing an actual pivot creates an impossible northeast rank bound.
        with self.assertRaises(AssertionError):c.check_cuts(23,rows,cols,pivots[1:])
    def test_full_geometry(self):
        result=g.run()
        self.assertEqual(json.loads(json.dumps(result)),json.loads((HERE/'geometry-certificate.json').read_text()))
        self.assertTrue(result['both_trees'] and result['actual_null_corner'])
    def test_enlarged_E_and_row_failures(self):
        f=self.result['finite_bridge']
        self.assertEqual(f['semantic']['E'],64*(f['complex']['W']+f['complex']['m']+f['complex']['scalar_group_upper']+1)**3)
        for name in ('E','rows'):
            bad=deepcopy(f)
            if name=='E':bad['semantic']['E']=64*(f['complex']['W']+f['complex']['m']+1)**3
            else:bad['rows']['degree']=1
            with self.assertRaises(AssertionError):w.assembly(bad,w.AB,w.KAPPA,a_complex=w.AC)
    def test_float_rejected(self):
        with self.assertRaises(AssertionError):w.assembly(self.result['finite_bridge'],float(w.AB),w.KAPPA,a_complex=w.AC)
    def test_negative_controls(self):
        self.assertEqual(set(self.result['negative_controls']),{'old_guard','old_exposures','original_prefix','next_kappa_grid','old_semantic_E_without_G'})

if __name__=='__main__':unittest.main()
