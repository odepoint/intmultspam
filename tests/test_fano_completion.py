"""Clean coding advantage versus complete arbitrary-input permutations."""
from copy import deepcopy
from pathlib import Path
import json
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_fano_completion import seed_checks,replay,FIXTURE,integer_code_matrix,forced_cut_certificate
from experiments.fano_completion import FANO_EDGES,cases,code,addition,completed_swap,scalar_check
from experiments.partial_routing import partial_routing
from finite_bit_contract import scalar_permutation,inspect_candidate,zero_frame_candidate


def execute(W,gates,values=None):
    values = list(values) if values is not None else [1 << i for i in range(W)]
    for gate in gates:
        for t,s in gate['xors']: values[t] ^= values[s]
    return values


class FanoCompletion(unittest.TestCase):
    def test_original_coding_seed_and_edge_prefix_retain_obstruction(self):
        result = seed_checks()
        self.assertEqual(result['original_routing']['path_counts'],[1,3,1])
        self.assertTrue(result['original_forced_cut']['no_edge_disjoint_routing'])
        self.assertEqual([r['routing']['routable'] for r in result['clean_realizations']],[True,True,False])
        self.assertTrue(result['clean_realizations'][-1]['forced_cut']['no_edge_disjoint_routing'])

    def test_fixed_all_plus_code_uses_characteristic_two(self):
        for compact,edge in ((True,False),(False,False),(True,True)):
            M = integer_code_matrix(compact,edge)
            I = [[int(i == j) for j in range(3)] for i in range(3)]
            self.assertEqual([[x%2 for x in row] for row in M],I)
            for p in (3,5,7): self.assertNotEqual([[x%p for x in row] for row in M],I)

    def test_each_addition_handles_independent_dirty_inputs(self):
        for compact,edge in ((True,False),(False,False),(True,True)):
            W = 6+len(code(compact,edge)['nodes'])
            for first in (False,True):
                gates = addition(list(range(3)),list(range(3,6)),list(range(6,W)),compact,first,True,edge)
                expected = [1 << i for i in range(W)]
                for i in range(3): expected[3+i] ^= expected[i]
                self.assertEqual(execute(W,gates),expected)

    def test_all_fifteen_completions_are_exact_with_dirty_scratch(self):
        programs = list(cases()); self.assertEqual(len(programs),15)
        for name,p in programs:
            result = scalar_check(p)
            self.assertTrue(result['arbitrary_auxiliary_inputs_restored'])
            self.assertTrue(result['inverse_exact'])
        self.assertEqual(sorted({p['W'] for name,p in programs}),[11,13,21,26,27,66])

    def test_single_addition_and_separate_scratch_shortcuts_fail(self):
        W = 11
        gates = addition(list(range(3)),list(range(3,6)),list(range(6,W)),dirty=False)
        initial = [1 << i for i in range(6)]+[0]*(W-6)
        expected = list(initial)
        for i in range(3): expected[3+i] ^= expected[i]
        self.assertEqual(execute(W,gates,initial),expected)
        dirty_expected = [1 << i for i in range(W)]
        for i in range(3): dirty_expected[3+i] ^= dirty_expected[i]
        self.assertNotEqual(execute(W,gates),dirty_expected)
        p = completed_swap(dirty=False,shared=False)
        with self.assertRaises(ValueError): scalar_permutation(p['W'],p['gates'])

    def test_shared_offsets_cancel_globally_but_independent_ones_do_not(self):
        for compact,edge,expected in ((True,False,75),(False,False,93),(True,True,165)):
            p = completed_swap(compact=compact,edge_explicit=edge,dirty=False)
            self.assertTrue(scalar_check(p)['arbitrary_auxiliary_inputs_restored'])
            self.assertEqual(len(p['gates']),expected)
            separate = completed_swap(compact=compact,edge_explicit=edge,shared=False,dirty=False)
            with self.assertRaises(ValueError): scalar_permutation(separate['W'],separate['gates'])

    def test_saved_routings_replay_without_solver_and_rule_out_rank_gain(self):
        fixture = json.loads(FIXTURE.read_text())
        with patch.dict(sys.modules,{'z3':None}):
            for name,p in cases():
                result = replay(name,p,fixture)
                self.assertEqual(result['check']['used_edges'],result['check']['total_edges'])
                score = inspect_candidate(zero_frame_candidate(p['W'],p['gates']),require_deficit=False)
                self.assertEqual(score['s'],2*p['W'])
                self.assertFalse(score['strict_transfer_contract'])

    def test_wrong_program_or_switch_certificate_is_rejected(self):
        fixture = json.loads(FIXTURE.read_text()); name,p = next(cases())
        bad = deepcopy(fixture); bad[name]['program_sha256'] = '0'*64
        with self.assertRaises(ValueError): replay(name,p,bad)
        bad = deepcopy(fixture); bad[name]['switches'] = '0'*len(p['gates'])
        with self.assertRaises(ValueError): replay(name,p,bad)

    def test_partial_routing_controls_and_budget_failures(self):
        pairs = [('a','ta'),('b','tb'),('c','tc')]
        changed = list(FANO_EDGES)+[('a','ta')]
        self.assertTrue(partial_routing(changed,pairs)['routable'])
        with self.assertRaises(ValueError): forced_cut_certificate(changed,pairs,6,7)
        with self.assertRaises(ValueError): partial_routing(FANO_EDGES,pairs,max_paths=1)
        with self.assertRaises(ValueError): partial_routing(FANO_EDGES,pairs,max_branches=0)
        with self.assertRaises(ValueError): partial_routing([('a','b'),('b','a')],[('a','b')])


if __name__ == '__main__':
    unittest.main()
