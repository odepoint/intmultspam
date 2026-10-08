"""Failure modes at the new circuit / retained assembly interface."""
from dataclasses import replace
from fractions import Fraction as Q
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from compact_control_layer import allocation
from audit_short_guards import guard_width
from complex_pair_star_parameters import (
    BIT_SAVING, certificate, check, optimized_parameters, simple_parameters,
    supplied_counts, sharpened_parameters, sharpened_bit_certificate,
)


class PairStarParameterTests(unittest.TestCase):
    def test_switching_exponent_order_reaches_bit_bottleneck(self):
        result = certificate()
        for name in ('main', 'optimized', 'sharpened'):
            part = result[name]
            self.assertEqual(part['recurrence']['internal'], part['parameters']['tau'])
            self.assertLess(part['parameters']['sigma'], part['parameters']['tau'])
            self.assertGreater(part['parameters']['tau'], part['recurrence']['leaf'])
            self.assertEqual(part['recurrence']['preprocessing'], 0)
            self.assertEqual(part['minimum_margin'], part['margins']['g3'])

    def test_exact_retained_bit_ceiling_is_inadmissible(self):
        p = optimized_parameters()
        ceiling = BIT_SAVING/(5+4*BIT_SAVING)
        with self.assertRaisesRegex(ValueError, 'absorption gap'):
            check(replace(p, kappa=ceiling), supplied_counts())

    def test_gaussian_limit_cannot_be_used_as_epsilon(self):
        with self.assertRaisesRegex(ValueError, 'gaussian_cost'):
            check(replace(simple_parameters(), epsilon=Q(1, 5)), supplied_counts())

    def test_old_style_equal_savings_would_overclaim_new_complex_network(self):
        with self.assertRaisesRegex(ValueError, 'complex saving'):
            check(replace(simple_parameters(), sigma=1-Q(5, 10**9)), supplied_counts())

    def test_residual_formula_is_a_checked_interface(self):
        n = supplied_counts()
        n['sc'] -= 1
        with self.assertRaisesRegex(ValueError, 'Residual formula'):
            check(simple_parameters(), n)

    def test_spacing_c_one_has_complete_reservations(self):
        n = supplied_counts()
        # d=p^(1/5) at these integer values. K=d implements c=1.
        # The construction still reserves complete controls inside d axes.
        d, p = 10**6, 10**30
        a = allocation(d, d, d, guard_width(p), n['m'], n['Wc'])
        self.assertEqual(a['mode'], 'recursive')
        self.assertLess(a['reserved_chunks'], d)
        self.assertGreaterEqual(a['front_slack_bits'], 0)
        self.assertGreaterEqual(a['back_slack_bits'], 0)

    def test_sharper_bit_saving_requires_its_additional_certificate(self):
        p = sharpened_parameters()
        with self.assertRaisesRegex(ValueError, 'bit saving'):
            check(p, supplied_counts())
        check(p, supplied_counts(), sharpened_bit=True)

    def test_sharper_bit_saving_needs_the_second_logarithm_term(self):
        proof = sharpened_bit_certificate()
        # The old linear eta/log(m) comparison cannot certify this value.
        self.assertLess(proof['eta'], proof['saving']*proof['log_m_enclosure'][0])
        # The retained graph does support it under the stronger comparison.
        self.assertGreater(proof['proof_gap'], 0)
        self.assertLess(proof['saving'], proof['actual_saving_enclosure'][0])


if __name__ == '__main__':
    unittest.main()
