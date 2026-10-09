from fractions import Fraction as Q
from pathlib import Path
import re
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from make_ternary_patch import patched_files,construction
from ternary_assembly import assembly_control

ROOT=Path(__file__).resolve().parents[1]


class TernaryPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.files={n:(o,v) for n,o,v in patched_files()}

    def test_interface_and_retained_precision(self):
        motif=self.files['build/sections/03-motifs.tex'][1]
        swap=self.files['build/sections/04-swap.tex'][1]
        layer=self.files['build/sections/05-layers.tex'][1]
        self.assertIn(construction(),motif)
        self.assertIn('sec:finite-alphabet-transfer',swap)
        self.assertIn('prop:ternary-bit-interface',swap)
        self.assertIn('finite-alphabet gates',swap)
        self.assertIn(r'm_{\rm b}=24389',layer)
        self.assertIn(r'm=m_{\rm c}=17576',layer)
        self.assertIn(r'\tau=1-467/10^{11}',layer)
        for name in ('compact-control-movement.tex','compact-control-layout.tex','compact-control-guard.tex'):
            self.assertIn((ROOT/'notes'/name).read_text(),layer)

    def test_assembly_parameters_and_every_derived_power(self):
        text=self.files['build/sections/08-assembly.tex'][1];a=assembly_control()
        self.assertEqual(a['parameters']['kappa'],Q(1,2**30))
        for k in ('K','ell','alpha','gamma','prime_interval_ratio'):
            v=a['powers'][k];self.assertIn('p^{%s/%s}'%(v.numerator,v.denominator),text)
        self.assertIn(r'\frac{2332833}{2500000000000000}>2^{-30}=\kappa',text)
        self.assertIn(r'd^{10000}\le b^{1999}',text)
        for stale in ('296/10','293','5771','199/1000','1597/2000','801/1000','301/500','2^{-31}'):
            self.assertNotIn(stale,text)

    def test_all_pinned_inputs_and_internal_references(self):
        texts=[]
        for path in (ROOT/'upstream/build').rglob('*.tex'):
            name='build/'+str(path.relative_to(ROOT/'upstream/build'))
            if name in self.files:
                old,new=self.files[name];self.assertEqual(old,path.read_text());texts.append(new)
            else:texts.append(path.read_text())
        text='\n'.join(texts)
        labels=re.findall(r'\\label\{([^}]+)\}',text)
        refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',text)
        self.assertEqual(len(labels),len(set(labels)))
        self.assertEqual(set(refs)-set(labels),set())


if __name__=='__main__':unittest.main()
