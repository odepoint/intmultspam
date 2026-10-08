"""Source-integration checks for the independent pair-star witness patch."""
from pathlib import Path
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from make_complex_pair_star_patch import patched_files


class PairStarPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files={name:(old,new) for name,old,new in patched_files()}
        cls.motif=cls.files['build/sections/03-motifs.tex'][1]
        cls.layer=cls.files['build/sections/05-layers.tex'][1]
        cls.assembly=cls.files['build/sections/08-assembly.tex'][1]

    def test_pinned_inputs_and_integrated_construction(self):
        for name,(old,new) in self.files.items():
            self.assertEqual(old,(ROOT/'upstream'/name).read_text())
        self.assertIn((ROOT/'notes/complex-pair-star-construction.tex').read_text(),self.motif)
        self.assertNotIn((ROOT/'notes/independent-complex.tex').read_text(),self.motif)
        for name in ('compact-control-movement.tex','compact-control-layout.tex',
                     'compact-control-guard.tex'):
            self.assertIn((ROOT/'notes'/name).read_text(),self.layer)

    def test_current_complex_counts_and_exponent_order(self):
        self.assertIn(r'm=m_{\rm c}=13824',self.layer)
        self.assertIn(r'W=W_{\rm c}=4496369044992',self.layer)
        self.assertIn(r's=s_{\rm c}=62157803252796416',self.layer)
        self.assertIn(r'm_{\rm b}=125000',self.layer)
        self.assertIn('prop:pair-star-complex-interface',self.layer)
        self.assertNotIn('prop:compact-complex-interface',self.layer)
        self.assertIn(r'\sigma=1-4/10^9',self.layer)
        self.assertIn(r'\tau=1-29646101715649/10^{22}',self.layer)
        self.assertIn(r'\max\{\sigma-\tau,0\}=\tau',self.assembly)
        self.assertIn(r'$\sigma<\tau$',self.assembly)

    def test_recurrence_reservations_and_guard_follow_new_parameters(self):
        self.assertIn(r'c=1',self.assembly)
        self.assertIn(r'$K=d$',self.assembly)
        self.assertIn(r'$e^{10}<d$',self.assembly)
        self.assertIn(r'C_1=\frac{461}{100}',self.assembly)
        self.assertIn(r'$C_1=461/100$',self.assembly)
        self.assertIn(r'd^{2000000000}\le b^{399999999}',self.assembly)
        self.assertIn(r'$O(\log d+\log p)$',self.assembly)
        self.assertIn('volume-weighted recurrence',self.assembly)
        self.assertNotIn(r'49961',self.assembly)
        self.assertNotIn(r'e^{1000}',self.assembly)
        self.assertNotIn(r'=O(Vp^{A\prime}2^{-K})',self.assembly)

    def test_headline_and_absorption_gap_are_current(self):
        self.assertIn(r'\kappa=\frac{5929220328}{10^{19}}>2^{-31}',self.assembly)
        self.assertIn(r'\frac{601639843694386501715649}{2\cdot10^{43}}',self.assembly)
        self.assertIn(r'>\frac3{10^{20}}>0',self.assembly)
        for name in ('build/main.tex','build/sections/00-introduction.tex'):
            self.assertIn(r'\kappa=5929220328/10^{19}',self.files[name][1])
        main=self.files['build/main.tex'][1]
        self.assertIn('Earlier compact-control modifications: Douglas Colkitt',main)
        self.assertIn('Integer multiplication, just for fun',main)
        self.assertIn('not an OpenAI release',main)

    def test_sharper_bit_exponent_has_its_own_valid_comparison(self):
        self.assertIn(r'\label{lem:paired-bit-sharp-exponent}',self.motif)
        self.assertIn(r'\eta_{\rm b}+\eta_{\rm b}^2/2',self.motif)
        self.assertIn(r'\tau_0=1-\frac{296}{10^{11}}',self.motif)
        swap=self.files['build/sections/04-swap.tex'][1]
        self.assertIn(r'\tau=1-29646101715649/10^{22}',swap)
        self.assertIn('lem:paired-bit-sharp-exponent',swap)
        self.assertNotIn(r'We use the rational value $\tau=1-\frac{296}',swap)

    def test_no_dangling_or_duplicate_internal_labels(self):
        texts=[]
        for path in (ROOT/'upstream/build').rglob('*.tex'):
            name='build/'+str(path.relative_to(ROOT/'upstream/build'))
            texts.append(self.files[name][1] if name in self.files else path.read_text())
        all_text='\n'.join(texts)
        labels=re.findall(r'\\label\{([^}]+)\}',all_text)
        refs=re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}',all_text)
        self.assertEqual(len(labels),len(set(labels)))
        self.assertEqual(set(refs)-set(labels),set())


if __name__=='__main__':
    unittest.main()
