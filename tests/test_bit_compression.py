"""Exact circuit controls and boundaries of the scoped compression screen."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_bit_compression import (TARGET, bound, classify_nodes, local_configs,
                                   verify_local)
from experiments.bit_compression import Blocked, FilterTree
from paired_exclusion_circuit import PairedExclusionCircuit
from search_network import log_integer_bounds
from shared_point_circuit import SharedPointCircuit


class BitCompression(unittest.TestCase):
    def test_small_variant_maps_against_independent_pair_enumeration(self):
        for n, k, vec in product((7,8,11), (2,3,4,6), ('prefix','tree','paired')):
            c = Blocked(n, k=k, leaf=3, vec=vec)
            self.assertTrue(verify_local(c))
            # Retained checker enumerates all allowed pairs for each output,
            # independently of this audit's incident-mask comparison.
            self.assertTrue(c.verify()['all_output_supports_exact'])
        for kind in ('balanced','vertex'):
            self.assertTrue(FilterTree(11,kind).verify()['all_output_supports_exact'])

    def test_reordered_and_reassociated_maps(self):
        for order, assoc in product(range(3), range(4)):
            self.assertTrue(Blocked(11,order=order,assoc=assoc).verify()['all_output_supports_exact'])
        c = Blocked(7)
        target = next(iter(c.outputs))
        c.outputs[target] = c.variables[target]
        with self.assertRaises(ValueError):
            verify_local(c)

    def test_frontier_is_computed_from_actual_source_intersections(self):
        c = PairedExclusionCircuit(11)
        cores = {}
        for node in c.active:
            if c.args[node]:
                edges = [set(edge) for i,edge in enumerate(c.inputs)
                         if c.support[node] & (1 << i)]
                cores[node] = set.intersection(*edges)
        unique = {node for node,core in cores.items() if not core}
        stars = set(cores)-unique
        frontier = {child for node in unique for child in c.args[node] if child in stars}
        self.assertEqual(classify_nodes(c), dict(unshareable=len(unique),
            stars=len(stars), mandatory_frontier_stars=len(frontier)))
        # Non-frontier stars must not be silently counted as mandatory.
        self.assertLess(len(frontier),len(stars))

    def test_changed_cutoff_retains_both_global_frame_directions(self):
        for h in (8,10,12):
            c = SharedPointCircuit(h,Blocked(h-1,leaf=3))
            self.assertTrue(c.verify()['all_partial_outputs_exact'])
            frames = c.verify_frames()
            self.assertTrue(frames['forward_frames_nested'])
            self.assertTrue(frames['reverse_complement_frames_nested'])
            classes = classify_nodes(c.local)
            lower = h*classes['unshareable']+(h*classes['mandatory_frontier_stars']+1)//2+len(c.outputs)
            self.assertLessEqual(lower,frames['roles'])

    def test_optimistic_role_budget_still_misses_target(self):
        row = bound(50,PairedExclusionCircuit(49))
        self.assertEqual(row['unshareable'],4389)
        self.assertEqual(row['mandatory_frontier_stars'],2304)
        self.assertEqual(row['side_roles_lower'],335850)
        self.assertEqual(row['necessary_integer_role_budget'],317035)
        self.assertLess(row['kappa_upper'],TARGET)
        with self.assertRaises(ValueError):
            bound(49,PairedExclusionCircuit(48))
        self.assertEqual(len(local_configs()),73)

    def test_lower_bound_survives_independent_relabeling_and_pruning(self):
        rng = random.Random(31030)
        for h in (8,10):
            c = PairedExclusionCircuit(h-1)
            classes = classify_nodes(c)
            lower = h*classes['unshareable']+(h*classes['mandatory_frontier_stars']+1)//2+h*len(c.outputs)
            triples = list(combinations(range(h),3))
            index = {triple:i+1 for i,triple in enumerate(triples)}
            for trial in range(8):
                masks = [0]+[1 << i for i in range(len(triples))]
                args = [None]*len(masks)
                lookup = {mask:i for i,mask in enumerate(masks)}
                outputs = []
                modules = list(range(h))
                rng.shuffle(modules)
                for common in modules:
                    points = [p for p in range(h) if p != common]
                    rng.shuffle(points)
                    mapping = {}
                    for node in sorted(c.active):
                        if c.args[node] is None:
                            a,b = c.inputs[node-1]
                            mapping[node] = index[tuple(sorted((common,points[a],points[b])))]
                            continue
                        a,b = (mapping[x] for x in c.args[node])
                        self.assertFalse(masks[a] & masks[b])
                        mask = masks[a] | masks[b]
                        if mask not in lookup:
                            lookup[mask] = len(masks)
                            masks.append(mask)
                            args.append((a,b))
                        mapping[node] = lookup[mask]
                    outputs.extend(mapping[node] for node in c.outputs.values())
                active = set()
                stack = list(outputs)
                while stack:
                    node = stack.pop()
                    if node in active:
                        continue
                    active.add(node)
                    if args[node]:
                        stack.extend(args[node])
                roles = sum(args[node] is not None for node in active)+len(outputs)
                self.assertGreaterEqual(roles,lower)

    def test_tail_bound_has_room_and_improves_with_ground_size(self):
        upper = []
        for h in (112,114,128,256):
            lo,_ = log_integer_bounds(h**3)
            upper.append(Q(1,(14*h**3-1))/lo)
        self.assertLess(upper[0],5*TARGET)
        self.assertTrue(all(a>b for a,b in zip(upper,upper[1:])))


if __name__ == '__main__':
    unittest.main()
