"""Independent endpoint, rank, physical-edge and topological checks."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_joint_frames import eye, add, matrix
from finite_bit_contract import (xor_gate, scalar_permutation, physical_graph,
    rational_matrix, inspect_candidate, find_routing, check_routing_paths, zero_frame_candidate)
from audit_cyclic_topology import cyclic_seed, swap_word, routing_state_search


class FiniteBitContract(unittest.TestCase):
    def test_complete_role_permutation_and_orientation(self):
        gates = cyclic_seed(3)
        self.assertEqual(scalar_permutation(3,gates),(2,0,1))
        candidate = zero_frame_candidate(3,gates)
        score = inspect_candidate(candidate,require_deficit=False)
        self.assertEqual(score['s'],6)
        self.assertFalse(score['strict_transfer_contract'])
        with self.assertRaises(ValueError): inspect_candidate(candidate)
        candidate['rho'] = [1,2,0]
        with self.assertRaises(ValueError): inspect_candidate(candidate,require_deficit=False)

    def test_free_nonprojector_frames_and_gauge_invariance(self):
        gates = cyclic_seed(3,star=True)
        candidate = zero_frame_candidate(3,gates)
        A = [matrix(((0,Q(1,2)),(0,0))),matrix(((-1,0),(0,0))),matrix(((1,2),(3,4)))]
        candidate['source_frames'] = A
        for w,out in enumerate(candidate['rho']): candidate['sink_frames'][out] = add(A[w],eye(2))
        for i,g in enumerate(candidate['gates']): g['frame'] = A[i%3]
        score = inspect_candidate(candidate,require_deficit=False)
        self.assertGreaterEqual(score['s'],6)
        C = matrix(((Q(-2,3),1),(Q(5,7),0)))
        shifted = deepcopy(candidate)
        shifted['source_frames'] = [add(M,C) for M in candidate['source_frames']]
        shifted['sink_frames'] = [add(M,C) for M in candidate['sink_frames']]
        for g in shifted['gates']: g['frame'] = add(g['frame'],C)
        self.assertEqual(inspect_candidate(shifted,require_deficit=False)['edge_ranks'],score['edge_ranks'])

    def test_scratch_roles_and_untouched_wire_edges_are_not_omitted(self):
        candidate = zero_frame_candidate(3,swap_word(0,1))
        score = inspect_candidate(candidate,require_deficit=False)
        self.assertEqual(score['rho'],[1,0,2])
        self.assertEqual(score['s'],6)
        graph = physical_graph(3,candidate['gates'])
        self.assertIn((2,8,2),graph)
        candidate['sink_frames'][2] = matrix(((0,0),(0,0)))
        with self.assertRaises(ValueError): inspect_candidate(candidate,require_deficit=False)

    def test_nonpermutation_or_invalid_gate_cannot_be_scored(self):
        with self.assertRaises(ValueError): scalar_permutation(2,[xor_gate(0,1)])
        for gate in (dict(roles=[0,0],xors=[]),dict(roles=[0],xors=[[0,1]]),
                     dict(roles=[0,1],xors=[[0,0]]),dict(roles=[0,1],xors=[],incidence_frames=[])):
            with self.assertRaises(ValueError): scalar_permutation(2,[gate])

    def test_exact_rational_schema_and_all_terminal_dimensions(self):
        self.assertEqual(rational_matrix([['1/2',0],[0,1]],2)[0][0],Q(1,2))
        with self.assertRaises(ValueError): rational_matrix([[0.5,0],[0,1]],2)
        with self.assertRaises(ValueError): rational_matrix([[1]],2)
        c = zero_frame_candidate(2,[])
        self.assertEqual(inspect_candidate(c,require_deficit=False)['edge_ranks'],[2,2])
        c['source_frames'].pop()
        with self.assertRaises(ValueError): inspect_candidate(c,require_deficit=False)

    def test_routing_certificates_cover_every_physical_edge(self):
        for W in (3,4,5):
            gates = cyclic_seed(W,star=True)
            result = find_routing(W,gates)
            self.assertTrue(result['routable'])
            check = check_routing_paths(W,gates,result['paths'])
            self.assertEqual(check['used_edges'],len(physical_graph(W,gates)))
            self.assertEqual(check['rank_lower_bound'],'W*m')

    def test_tampered_routes_and_exhausted_search_budget_rejected(self):
        gates = cyclic_seed(3)
        route = find_routing(3,gates)
        bad = deepcopy(route['paths']); bad[1] = bad[0]
        with self.assertRaises(ValueError): check_routing_paths(3,gates,bad)
        bad = deepcopy(route['paths']); bad[0] = bad[0][1:]
        with self.assertRaises(ValueError): check_routing_paths(3,gates,bad)
        with self.assertRaises(ValueError): find_routing(3,gates,max_states=1)

    def test_small_role_closure_and_four_role_scope(self):
        two = routing_state_search(2,7); three = routing_state_search(3,7)
        self.assertTrue(two['all_lengths_excluded'])
        self.assertTrue(three['all_lengths_excluded'])
        self.assertEqual(three['distinct_joint_states'],235)
        self.assertEqual([x['new_states'] for x in three['layers']],[1,6,33,75,78,36,6,0])
        four = routing_state_search(4,4)
        self.assertEqual(four['distinct_joint_states'],9788)
        self.assertFalse(four['frontier_closed'])
        self.assertTrue(four['all_words_through_depth_excluded'])

    def test_short_word_search_against_independent_enumeration(self):
        alphabet = [(t,s) for t in range(3) for s in range(3) if t != s]
        terminals = 0
        for word in product(alphabet,repeat=4):
            values = [1,2,4]
            for t,s in word: values[t] ^= values[s]
            if set(values) != {1,2,4}: continue
            terminals += 1
            self.assertTrue(find_routing(3,[xor_gate(t,s) for t,s in word])['routable'])
        self.assertGreater(terminals,0)


if __name__ == '__main__':
    unittest.main()
