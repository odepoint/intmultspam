"""Free-output completions, rigidity proofs, and independent routing replay."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_fano_permutation import FIXTURE, replay, partial_bypass
from experiments.fano_completion import clean_prefix
from experiments.fano_permuted_completion import LAYOUTS, rows_after, refinement, complete, cases
from finite_bit_contract import scalar_permutation


class PermutedCompletion(unittest.TestCase):
    def test_three_compute_maps_have_rigid_bipartite_support(self):
        for name, compact, edge in LAYOUTS:
            p = clean_prefix(compact, edge)
            proof = refinement(rows_after(p['W'], p['gates']))
            self.assertTrue(proof['singleton_colors'], name)
            self.assertTrue(all(len(c) == 1 for c in proof['stable_classes']))
            sizes = [len(set(r)) for r in proof['rounds']]
            self.assertEqual(sizes, sorted(sizes))

    def test_refinement_does_not_certify_symmetric_controls(self):
        self.assertFalse(refinement([1, 2, 4, 8])['singleton_colors'])
        # Two identical independent CNOT blocks have a block-swap symmetry.
        self.assertFalse(refinement([1, 3, 4, 12])['singleton_colors'])
        with self.assertRaises(ValueError): refinement([1, 4])

    def test_all_independent_inputs_form_the_claimed_permutations(self):
        counts = Counter()
        for name, e in cases():
            p = e['program']
            rho = scalar_permutation(p['W'], p['gates'])
            values = rows_after(p['W'], p['gates'])
            self.assertEqual([values[rho[i]] for i in range(p['W'])],
                             [1 << i for i in range(p['W'])])
            counts['cases'] += 1
            counts['moved'] += any(rho[i] != i for i in range(6, p['W']))
            counts['mixed'] += any(rho[i] < 6 for i in range(6, p['W']))
            if e['keep_terminals']:
                self.assertEqual(rho[:3], (3, 4, 5))
                self.assertTrue(any(rho[i] != i for i in range(6, p['W'])))
                counts['terminals'] += 1
        self.assertEqual(counts, dict(cases=144, moved=126, mixed=122, terminals=72))

    def test_all_saved_routes_replay_without_solver(self):
        fixture = json.loads(FIXTURE.read_text())
        self.assertEqual(set(fixture), {n for n, e in cases()})
        with patch.dict(sys.modules, {'z3': None}):
            for name, e in cases():
                r = replay(e, fixture[name])
                self.assertEqual(r['check']['used_edges'], r['check']['total_edges'])

    def test_terminal_bypasses_are_checked_separately(self):
        for name, e in cases():
            if e['keep_terminals']:
                bypass = partial_bypass(e)
                self.assertEqual(len(set(bypass['crossing_gates'])), 3)
                self.assertTrue(bypass['original_three_demands_routable'])
                changed = deepcopy(e)
                changed['pivots'][0]['targets'].remove(0)
                with self.assertRaises(ValueError): partial_bypass(changed)

    def test_corrupted_or_mismatched_routing_witness_fails(self):
        fixture = json.loads(FIXTURE.read_text())
        name, e = next((n, e) for n, e in cases() if e['keep_terminals'])
        bad = deepcopy(fixture[name]); bad['program_sha256'] = '0'*64
        with self.assertRaises(ValueError): replay(e, bad)
        bad = deepcopy(fixture[name]); bad['switches'] = '0'*len(e['program']['gates'])
        with self.assertRaises(ValueError): replay(e, bad)
        bad = deepcopy(fixture[name]); bad['switches'] += '1'
        with self.assertRaises(ValueError): replay(e, bad)

    def test_completion_parameters_and_prefix_are_checked(self):
        p = clean_prefix()
        with self.assertRaises(ValueError): complete(p, 0, 'missing')
        # An identity prefix has no source-to-target coefficients to pivot on.
        with self.assertRaises(ValueError): complete(dict(W=6, gates=[]), 0, 'sparse', True)


if __name__ == '__main__':
    unittest.main()
