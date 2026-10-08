"""Mathematical failure-mode tests for the new complex side computation."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from random import Random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from complex_pair_star import PairStarBatch, batches, counts, dot, indicator, verify_sharing


@lru_cache(maxsize=1)
def small_program():
    h = 8
    triples = list(combinations(range(h), 3))
    ids = {t: i for i, t in enumerate(triples)}
    pieces = [(batch, batch.compile()) for batch in batches(h)]
    return h, triples, ids, pieces


def apply_invocation(source, target, sides, center, inverse=False):
    """Execute the complete signed 12-phase circuit on Gaussian dyadic data."""
    h, triples, ids, pieces = small_program()

    def mixer(sign):
        for values, (batch, code) in zip(sides, pieces):
            batch.mix(values, code, inverse=sign < 0)

    def inject(sign):
        for values, (batch, code) in zip(sides, pieces):
            for out_id, (target_id, _, twice_weight) in enumerate(batch.outputs):
                target[target_id] += sign * Q(twice_weight, 2) * values[code['outputs'][out_id]]

    def scatter(sign):
        for i, triple in enumerate(triples):
            if h - 1 not in triple:
                value = Q(sum(center[j] for j in triple) - center[-1], 2)
            else:
                value = center[-1] - Q(sum(center[j] for j in range(h - 1) if j not in triple), 2)
            target[i] += sign * value

    def copy(sign):
        for values, (batch, code) in zip(sides, pieces):
            for i, role in code['sources'].items():
                values[role] += sign * source[ids[batch.sources[i]]]

    def gather(sign):
        for i, triple in enumerate(triples):
            value = sign * source[i]
            for j in triple:
                if j < h - 1:
                    center[j] += value
            center[-1] += value

    operations = [(mixer, 1), (inject, -1), (mixer, -1), (scatter, -1),
                  (copy, 1), (gather, 1), (scatter, 1), (mixer, 1),
                  (inject, 1), (mixer, -1), (gather, -1), (copy, -1)]
    if inverse:
        operations = [(operation, -sign) for operation, sign in reversed(operations)]
    for operation, sign in operations:
        operation(sign)


class ComplexPairStarTests(unittest.TestCase):
    def test_every_small_matrix_entry_and_every_compiled_frame(self):
        h, triples, _, pieces = small_program()
        entries = 0
        for batch, _ in pieces:
            entries += batch.verify()['checked_coefficients']
        self.assertEqual(entries, len(triples)**2)
        verify_sharing(h)

    def test_dirty_invocation_and_inverse_over_dyadic_rationals(self):
        rng = Random(20261007)
        h, triples, _, pieces = small_program()
        sample = lambda: Q(rng.randrange(-1000, 1001), 1 << rng.randrange(0, 6))
        source = [sample() for _ in triples]
        target = [sample() for _ in triples]
        sides = [[sample() for _ in range(code['roles'])] for _, code in pieces]
        center = [sample() for _ in range(h)]
        before_source, before_target = source[:], target[:]
        before_sides, before_center = [values[:] for values in sides], center[:]
        apply_invocation(source, target, sides, center)
        self.assertEqual(source, before_source)
        self.assertEqual(target, [x+y for x, y in zip(before_source, before_target)])
        self.assertEqual(sides, before_sides)
        self.assertEqual(center, before_center)
        apply_invocation(source, target, sides, center, inverse=True)
        self.assertEqual(target, before_target)
        self.assertEqual(sides, before_sides)
        self.assertEqual(center, before_center)

    def test_signed_three_stage_exchange_with_reused_dirty_scratch(self):
        rng = Random(109)
        h, triples, _, pieces = small_program()
        sample = lambda: Q(rng.randrange(-30, 31), 8)
        x, y = [sample() for _ in triples], [sample() for _ in triples]
        first = [[sample() for _ in range(code['roles'])] for _, code in pieces]
        second = [[sample() for _ in range(code['roles'])] for _, code in pieces]
        ca, cb = [sample() for _ in range(h)], [sample() for _ in range(h)]
        x0, y0 = x[:], y[:]
        a0, b0, ca0, cb0 = [v[:] for v in first], [v[:] for v in second], ca[:], cb[:]
        apply_invocation(x, y, first, ca)
        apply_invocation(y, x, second, cb, inverse=True)
        apply_invocation(x, y, first, ca)
        self.assertEqual(x, [-value for value in y0])
        self.assertEqual(y, x0)
        self.assertEqual((first, second, ca, cb), (a0, b0, ca0, cb0))

    def test_mixer_inverse_restores_arbitrary_scratch(self):
        rng = Random(73)
        for batch, code in small_program()[3]:
            values = [rng.randrange(-10**5, 10**5) for _ in range(code['roles'])]
            original = values[:]
            batch.mix(values, code)
            batch.mix(values, code, inverse=True)
            self.assertEqual(values, original)

    def test_reject_batch_without_nonalternation_budget(self):
        with self.assertRaisesRegex(ValueError, 'residual unit'):
            PairStarBatch(8, (0, 1), (2, 3, 4))

    def test_complements_have_norm_one_vectors_not_only_positive_rank(self):
        for batch, _ in small_program()[3]:
            for target_id, mask, _ in batch.outputs:
                target = indicator(batch.triples[target_id])
                outside = ((1 << batch.h) - 1) ^ (target | batch.support_union)
                unit = outside & -outside
                self.assertEqual(dot(unit, unit), 1)
                self.assertEqual(dot(unit, target), 0)
                for i, vector in enumerate(batch.source_vectors):
                    if mask & (1 << i):
                        self.assertEqual(dot(unit, vector), 0)

    def test_residual_count_is_positive_only_with_proved_center_bound(self):
        n = counts(24, 546748)
        self.assertEqual(n['W']*n['m']-n['s'], 2*(n['N']-n['L']))
        self.assertEqual(n['eta'], Q(37, 948319488))
        self.assertLess(n['L'], n['N'])


if __name__ == '__main__':
    unittest.main()
