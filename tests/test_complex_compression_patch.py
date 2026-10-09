"""Checks at the finite-interface/layer/assembly integration boundary."""
from fractions import Fraction as Q
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from complex_compression import assembly_control
from make_complex_compression_patch import patched_files, construction, guard_accounting

ROOT = Path(__file__).resolve().parents[1]


class ComplexCompressionPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = {name:(old,new) for name,old,new in patched_files()}
        cls.layer = cls.files['build/sections/05-layers.tex'][1]
        cls.assembly = cls.files['build/sections/08-assembly.tex'][1]

    def test_pinned_inputs_and_retained_movement_proofs(self):
        for name,(old,new) in self.files.items():
            self.assertEqual(old, (ROOT/'upstream'/name).read_text())
        for name in ('compact-control-movement.tex','compact-control-layout.tex',
                     'compact-control-guard.tex'):
            self.assertIn((ROOT/'notes'/name).read_text(), self.layer)
        motif = self.files['build/sections/03-motifs.tex'][1]
        self.assertIn(construction(), motif)
        self.assertNotIn('prop:compact-complex-interface', motif)

    def test_new_interface_constants_and_node_guard(self):
        self.assertIn(r'm=m_{\rm c}=17576', self.layer)
        self.assertIn(r'm_{\rm b}=125000', self.layer)
        self.assertIn(r'W=W_{\rm c}=7082222160000', self.layer)
        self.assertIn(r's=s_{\rm c}=124477130005280000', self.layer)
        self.assertIn(guard_accounting(), self.layer)
        self.assertIn('prop:compressed-complex-interface', self.layer)
        self.assertNotIn('prop:compact-complex-interface', self.layer)
        self.assertIn(r'\sigma=1-5/10^9', self.layer)

    def test_changed_ordering_and_exact_derived_powers(self):
        result = assembly_control()
        p = result['parameters']
        self.assertLess(p['sigma'], p['tau'])
        self.assertEqual(result['internal_exponent'], p['tau'])
        self.assertIn(r'$\chi=\tau$, because $\sigma<\tau$', self.assembly)
        powers = result['derived_powers']
        self.assertEqual(powers, dict(d=Q(199,1000),K=Q(199,1000),
            ell=Q(801,1000),alpha=Q(1199,4000),gamma=Q(1597,2000),
            prime_interval_ratio=Q(301,500),guard=Q(987239,1000000)))
        for key in ('K','ell','alpha','gamma','prime_interval_ratio'):
            value = powers[key]
            self.assertIn('p^{%s/%s}' % (value.numerator,value.denominator), self.assembly)
        self.assertIn(r'e^{100}<d', self.assembly)
        self.assertIn(r'd^{1000}\le b^{199}', self.assembly)
        self.assertIn(r'\frac{5771}{10^{13}}>2^{-31}=\kappa', self.assembly)
        self.assertGreater(result['minimum_margin'], Q(1,2**31))

    def test_legacy_appendix_and_local_repair_contracts(self):
        self.assertEqual(self.layer.count(r'\label{lem:packed-selected-bit-rectangle}'),1)
        batching = self.layer[self.layer.index(r'\subsection{Batching a common layer'):]
        self.assertNotIn(r'(eK)^\tau', batching)
        self.assertIn('volume-weighted recurrence', self.assembly)
        self.assertIn(r"1-c<\lambda'", self.assembly)
        for stale in ('1999/10000','49961','15997','1671','418/10',
                      '333833','8001/10000','3001/5000'):
            self.assertNotIn(stale, self.assembly)

    def test_no_dangling_or_duplicate_internal_labels(self):
        texts = []
        for path in (ROOT/'upstream/build').rglob('*.tex'):
            name = 'build/'+str(path.relative_to(ROOT/'upstream/build'))
            texts.append(self.files[name][1] if name in self.files else path.read_text())
        text = '\n'.join(texts)
        labels = re.findall(r'\\label\{([^}]+)\}',text)
        refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',text)
        self.assertEqual(len(labels),len(set(labels)))
        self.assertEqual(set(refs)-set(labels),set())


if __name__ == '__main__':
    unittest.main()
