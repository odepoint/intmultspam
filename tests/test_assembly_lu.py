"""Checks for the linear guard, the constant-width banded solve and its patch."""
from dataclasses import replace
import difflib
from fractions import Fraction as Q
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import assembly_lu as A
from make_assembly_lu_patch import patched_files


class AssemblyCertificate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert = A.certificate()
        sv = cls.cert['savings']
        cls.q = min(sv['a_b'], sv['a_c'])
        cls.p = A.headline_parameters(sv['a_b'], sv['a_c'])

    def test_headline_witness_is_strict(self):
        w = self.cert['witness']
        self.assertEqual(self.cert['headline_kappa'], Q(296461013, 2*10**17))
        self.assertTrue(all(v > 0 for v in w['constraint_slacks'].values()))
        self.assertEqual(w['limiting'], ['g3'])
        self.assertEqual(w['absorption_gap'], Q(22306317521666189976715649, 25*10**41))
        self.assertTrue(Q(1, 2**30) < self.cert['headline_kappa'] < Q(1, 2**29))

    def test_supremum_is_not_attained(self):
        sup = self.q/(2+2*self.q)
        self.assertEqual(self.cert['suprema']['constant_width_supremum'], sup)
        with self.assertRaisesRegex(ValueError, 'absorption gap'):
            A.check_witness(replace(self.p, kappa=sup))
        with self.assertRaisesRegex(ValueError, 'Failed strict constraint'):
            A.check_witness(replace(self.p, epsilon=Q(1, 2)))

    def test_retained_rows_fail_at_the_new_epsilon(self):
        self.assertLess(A.constraints(replace(self.p, C1=Q(461, 100)))['guard_width'], 0)
        tight = A.constraints(self.p, 'tight')
        for name in ('gaussian_cost', 'dimension_upper_bound', 'gamma_sublinear'):
            self.assertLess(tight[name], 0)
        self.assertEqual(A.margins(self.p)['g5'], Q(3999, 10**12))

    def test_retained_model_transcription(self):
        self.assertEqual(self.cert['retained_constraint_names'], 31)
        self.assertEqual(self.cert['changed_constraints'], list(A.CHANGED))

    def test_guard_constants_follow_the_pair_star_circuit(self):
        g = self.cert['guard']
        self.assertEqual((g['m'], g['W'], g['s']), (13824, 4496369044992, 62157803252796416))
        self.assertLess(g['D_node'], g['E'])
        self.assertEqual(g['C0_star'], g['E']+2*g['s']+g['m']+26)

    def test_scaled_dominance_rows(self):
        r = self.cert['resampling']
        self.assertEqual(r['rho_2_upper'], Q(38, 10000))
        self.assertEqual(r['checked_rows'], 61+97+101+113+211+251)


class BandedSolveSimulation(unittest.TestCase):
    def test_non_dominant_alpha_two_instances(self):
        for s, t in ((61, 62), (83, 85)):
            r = A.banded_solve_simulation(s, t, 2, 101)
            self.assertGreater(r['unscaled_offdiag'], Q(46, 100))
            self.assertTrue(Q(9, 10) <= r['min_pivot'] <= r['max_pivot'] <= Q(11, 10))
            self.assertLess(r['worst_error_squared'], 4)

    def test_dominant_instances(self):
        for alpha in (2, 3):
            r = A.banded_solve_simulation(97, 128, alpha, 101)
            self.assertLess(r['unscaled_offdiag'], Q(1, 100))
            self.assertLess(r['worst_error_squared'], 4)

    def test_lemma_hypotheses_are_enforced(self):
        self.assertEqual(A.solve_parameters(61, 62, 2, 101), (70, 455, 11))
        with self.assertRaisesRegex(ValueError, 'hypotheses'):
            A.banded_solve_simulation(61, 62, 2, 60)


class AssemblyPatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = {name: (old, new) for name, old, new in patched_files()}
        cls.motif = cls.files['build/sections/03-motifs.tex'][1]
        cls.layer = cls.files['build/sections/05-layers.tex'][1]
        cls.resampling = cls.files['build/sections/07-resampling.tex'][1]
        cls.assembly = cls.files['build/sections/08-assembly.tex'][1]

    def test_pinned_inputs_and_integrated_proofs(self):
        for name, (old, new) in self.files.items():
            self.assertEqual(old, (ROOT/'upstream'/name).read_text())
        self.assertIn((ROOT/'notes/assembly-lu-guard.tex').read_text(), self.layer)
        self.assertIn((ROOT/'notes/assembly-lu-resampling.tex').read_text(), self.resampling)
        self.assertLess(self.resampling.index(r'\label{sec:banded-solve}'),
                        self.resampling.index(r'\label{lem:no-sort-resampling}'))

    def test_retained_guard_and_neumann_hypotheses_are_removed(self):
        self.assertNotIn('stopped-depth guard', self.layer)
        self.assertNotIn(r'\zeta', self.layer)
        self.assertNotIn(r'C_0d^{C_1}', self.layer+self.assembly)
        self.assertNotIn(' \\epsilon C_1<1.\n', self.layer)
        self.assertNotIn('C_1', self.assembly)
        self.assertIn(r'C_0^*=64(W_{\rm c}+m+1)^3+2s_{\rm c}+m+26', self.layer)
        self.assertNotIn(r'\theta:=t/s-1>p/\alpha^4', self.resampling)
        self.assertNotIn('Lemmas~4.8, 4.9 and 4.12', self.resampling)
        self.assertNotIn('Neumann evaluation also keeps', self.resampling)
        self.assertIn(r'P_sF_s=2^{2\alpha^2+L+1}B_0P_tF_tA', self.resampling)
        self.assertIn(r'\gamma=\sum_i(2\alpha^2+L_i+1)', self.resampling)
        self.assertNotIn('sA(e/m)', self.motif)
        self.assertIn(r'Section~\ref{sec:linear-guard}', self.motif)

    def test_assembly_rows_and_headline(self):
        self.assertIn(r'\kappa=\frac{296461013}{2\cdot10^{17}}>2^{-30}', self.assembly)
        self.assertIn(r'\epsilon=\frac{124999999}{250000000}', self.assembly)
        self.assertIn(r'\alpha=2,\qquad \eta=\frac1{4d}', self.assembly)
        self.assertIn(r'Gaussian line maps & $dp^{1/2+\delta}$ & $1/2+\delta+\epsilon$\\',
                      self.assembly)
        self.assertIn(r'g_5=1/2-\delta-\epsilon', self.assembly)
        self.assertIn(r'\frac{22306317521666189976715649}{25\cdot10^{41}}', self.assembly)
        self.assertIn(r'b\ge2^{541000000}', self.assembly)
        self.assertIn(r'd^{250000000}\le b^{124999999}', self.assembly)
        for gone in ('3/4+\\delta+5\\epsilon/4', '(32db)^{1/4}', 'b\\ge2^{40}',
                     '5929220328', '\\alpha^4\\theta_i'):
            self.assertNotIn(gone, self.assembly)
        for name in ('build/main.tex', 'build/sections/00-introduction.tex'):
            text = self.files[name][1]
            self.assertIn(r'\kappa=296461013/(2\cdot10^{17})', text)
            self.assertNotIn('5929220328', text)

    def test_committed_patch_matches(self):
        patch = ''.join(''.join(difflib.unified_diff(
            old.splitlines(keepends=True), new.splitlines(keepends=True),
            fromfile=f'a/{name}', tofile=f'b/{name}'))
            for name, (old, new) in self.files.items())
        self.assertEqual(patch, (ROOT/'patches/assembly-lu-30.patch').read_text())

    def test_no_dangling_or_duplicate_internal_labels(self):
        texts = []
        for path in (ROOT/'upstream/build').rglob('*.tex'):
            name = 'build/'+str(path.relative_to(ROOT/'upstream/build'))
            texts.append(self.files[name][1] if name in self.files else path.read_text())
        all_text = '\n'.join(texts)
        labels = re.findall(r'\\label\{([^}]+)\}', all_text)
        refs = re.findall(r'\\(?:eqref|ref|pageref)\{([^}]+)\}', all_text)
        self.assertEqual(len(labels), len(set(labels)))
        self.assertEqual(set(refs)-set(labels), set())


if __name__ == '__main__':
    unittest.main()
