#!/usr/bin/env python3
"""Exact complex pair-star circuit, reversible embedding and frame certificate.

This is a conditional extension of CrocSwap/integer-mult-bounds at
6e564879f51ae16f23d392e9e196c605f36d90df.  The exact finite checks do not
formally verify the upstream multiplication algorithm.  Prepared with AI
assistance; the written construction supplies the general proof obligations.

All arithmetic in the certificate is integral or rational.  No packages are
required outside the Python standard library.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import comb, factorial
from pathlib import Path
import json

from certify import require, verify_sources
from prepare_layers import serializable
from search_network import log_integer_bounds, log_ratio_bounds

ROOT = Path(__file__).resolve().parents[1]
H = 24
COMPLEX_SAVING = Q(4, 10**9)
BASELINE_COMMIT = "6e564879f51ae16f23d392e9e196c605f36d90df"


def indicator(t):
    return sum(1 << i for i in t)


def dot(u, v):
    return (u & v).bit_count() & 1


def paired_triple(t):
    """The fixed-point-free ground involution, lifted to triples."""
    return tuple(sorted(i ^ 1 for i in t))


class PairStarBatch:
    """Disjoint-support sums within one orthonormal family of indicators."""

    def __init__(self, h, anchor, leaves, triples=None):
        self.h = h
        self.anchor = tuple(anchor)
        self.leaves = tuple(leaves)
        require(len(self.anchor) == 2 and self.anchor[0] < self.anchor[1],
                "Invalid anchor")
        require(0 < len(self.leaves) <= h - 6,
                "A batch must leave room for a residual unit witness")
        require(all(self.anchor[1] < k < h for k in self.leaves),
                "Leaves must follow the two smallest points")
        self.triples = triples or list(combinations(range(h), 3))
        self.sources = [self.anchor + (k,) for k in self.leaves]
        self.source_vectors = [indicator(t) for t in self.sources]
        self.full = (1 << len(self.leaves)) - 1
        self.index = {k: i for i, k in enumerate(self.leaves)}
        self.args = {1 << i: None for i in range(len(self.leaves))}
        self.outputs = []  # (physical target index, support mask, twice weight)
        self.support_union = indicator(self.anchor + self.leaves)
        a, b = self.anchor
        for target_id, target in enumerate(self.triples):
            anchor_hits = int(a in target) + int(b in target)
            hits = sum(1 << self.index[k] for k in target if k in self.index)
            support = hits if anchor_hits == 1 else self.full ^ hits
            twice_weight = 1 if anchor_hits == 0 else -1
            if support:
                self._sum(support)
                self.outputs.append((target_id, support, twice_weight))
        self.order = sorted(self.args, key=lambda x: (x.bit_count(), x))
        self.additions = sum(a is not None for a in self.args.values())

    def _sum(self, mask):
        if mask in self.args:
            return
        low = (mask & -mask).bit_length() - 1
        high = mask.bit_length()
        split = (low + high) // 2
        left = mask & ((1 << split) - 1)
        right = mask ^ left
        require(left and right and not left & right, "Invalid disjoint split")
        self._sum(left)
        self._sum(right)
        self.args[mask] = (left, right)

    def compile(self):
        """One reversible role per addition or designated output use."""
        users = {mask: [] for mask in self.order}
        for mask in self.order:
            if self.args[mask] is not None:
                for port, parent in enumerate(self.args[mask]):
                    users[parent].append(("gate", mask, port))
        for out_id, (_, mask, _) in enumerate(self.outputs):
            users[mask].append(("output", out_id, 0))
        size = 0
        edges, sources, output_slots = {}, {}, {}
        gates = []
        for mask in self.order:
            require(users[mask], "Unused source or sum in circuit")
            if self.args[mask] is None:
                outs = list(range(size, size + len(users[mask])))
                size += len(outs)
                ins = [outs[0]]
                sources[mask.bit_length() - 1] = ins[0]
            else:
                ins = [edges[mask, 0], edges[mask, 1]]
                outs = [ins[0]] + list(range(size, size + len(users[mask]) - 1))
                size += len(users[mask]) - 1
            require(len(set(ins)) == len(ins), "Two live operands share a role")
            require(not set(ins[1:]) & set(outs), "Retired operand reused too early")
            gates.append((mask, ins, outs))
            for user, role in zip(users[mask], outs):
                if user[0] == "gate":
                    edges[user[1], user[2]] = role
                else:
                    output_slots[user[1]] = role
        require(size == self.additions + len(self.outputs), "Role formula failed")
        require(len(set(output_slots.values())) == len(self.outputs),
                "Simultaneous output uses share roles")
        return dict(roles=size, gates=gates, sources=sources, outputs=output_slots)

    @staticmethod
    def mix(values, code, inverse=False):
        gates = reversed(code["gates"]) if inverse else code["gates"]
        for _, ins, outs in gates:
            pivot = ins[0]
            if inverse:
                for role in reversed(outs[1:]):
                    values[role] -= values[pivot]
                for role in reversed(ins[1:]):
                    values[pivot] -= values[role]
            else:
                for role in ins[1:]:
                    values[pivot] += values[role]
                for role in outs[1:]:
                    values[role] += values[pivot]

    def verify(self):
        """All coefficients, every compiled frame edge, and norm-one witnesses."""
        code = self.compile()
        for i, u in enumerate(self.source_vectors):
            for j, v in enumerate(self.source_vectors):
                require(dot(u, v) == int(i == j), "Source Gram matrix is not I")
        require(self.support_union.bit_count() <= self.h - 4,
                "Source supports exceed the nonalternation budget")
        # Independent integer coefficient vectors: duplicates cannot disappear
        # through XOR or carry into another variable's bit-mask coordinate.
        width = len(self.sources)
        zero = (0,) * width
        vector = lambda mask: tuple(int(bool(mask & (1 << i))) for i in range(width))
        values = [zero] * code["roles"]
        frames = [0] * code["roles"]
        for i, role in code["sources"].items():
            values[role] = vector(1 << i)
            frames[role] = 1 << i
        for mask, ins, outs in code["gates"]:
            if self.args[mask] is not None:
                left, right = self.args[mask]
                require(not left & right and left | right == mask,
                        "Formal sum is not cancellation-free")
                require(values[ins[0]] == vector(left) and values[ins[1]] == vector(right),
                        "Compiled integer operands differ from formal supports")
            for role in set(ins + outs):
                require(not frames[role] & ~mask, "Forward frame decreases")
                frames[role] = mask
            for role in ins[1:]:
                values[ins[0]] = tuple(x+y for x, y in zip(values[ins[0]], values[role]))
            for role in outs[1:]:
                require(values[role] == zero, "Fresh fanout role is not initially zero")
                values[role] = tuple(x+y for x, y in zip(values[role], values[ins[0]]))
            require(all(values[role] == vector(mask) for role in outs),
                    "Compiled sum has a wrong integer coefficient")
        coefficients = 0
        for out_id, (target_id, mask, weight) in enumerate(self.outputs):
            role = code["outputs"][out_id]
            require(values[role] == vector(mask) and frames[role] == mask, "Incorrect output role")
            target = self.triples[target_id]
            target_vector = indicator(target)
            require(((1 << self.h) - 1) ^ (self.support_union | target_vector),
                    "No coordinate unit for a target complement residual")
            for i, source in enumerate(self.sources):
                actual = weight if mask & (1 << i) else 0
                intersection = len(set(source) & set(target))
                expected = (1 - intersection) if source != target and intersection % 2 == 0 else 0
                require(actual == expected, "Wrong signed side coefficient")
                if actual:
                    require(dot(self.source_vectors[i], target_vector) == 0,
                            "Source is not orthogonal to its target")
                coefficients += 1
        # Also check the zeros for target/batch combinations with no output.
        by_target = {target_id: (mask, weight) for target_id, mask, weight in self.outputs}
        for target_id, target in enumerate(self.triples):
            if target_id in by_target:
                continue
            for source in self.sources:
                intersection = len(set(source) & set(target))
                require(source == target or intersection % 2 == 1,
                        "A required correction output was omitted")
                coefficients += 1
        reverse = [0] * code["roles"]
        for out_id, (_, mask, _) in enumerate(self.outputs):
            reverse[code["outputs"][out_id]] = mask
        for mask, ins, outs in reversed(code["gates"]):
            for role in set(ins + outs):
                require(not reverse[role] or not mask & ~reverse[role],
                        "Reverse complement frame decreases")
                reverse[role] = mask
        for i, role in code["sources"].items():
            require(reverse[role] == 1 << i, "Wrong reversed source complement")
        digest = sha256()
        for mask in self.order:
            digest.update(json.dumps((mask, self.args[mask]), separators=(",", ":")).encode() + b"\n")
        for output in self.outputs:
            digest.update(json.dumps(output, separators=(",", ":")).encode() + b"\n")
        return dict(anchor=self.anchor, leaves=self.leaves, additions=self.additions,
                    output_uses=len(self.outputs), roles=code["roles"],
                    checked_coefficients=coefficients, source_gram_identity=True,
                    forward_frames_nested=True, reverse_complement_frames_nested=True,
                    complement_unit_witnesses=True, sha256=digest.hexdigest())


def batches(h=H):
    require(h >= 8 and h % 2 == 0, "Use even h>=8 for the shared binary motif")
    triples = list(combinations(range(h), 3))
    cap = h - 6
    for a, b in combinations(range(h - 1), 2):
        leaves = list(range(b + 1, h))
        for start in range(0, len(leaves), cap):
            yield PairStarBatch(h, (a, b), leaves[start:start + cap], triples)


def counts(h=H, side_roles=None):
    if side_roles is None:
        side_roles = sum(b.additions + len(b.outputs) for b in batches(h))
    v, m = comb(h, 3), h**3
    N = v**3
    W = 2*N + 2*v*v*(side_roles + h)
    L = 3*v*v*h*h
    s = W*m - 2*N + 2*L
    eta = Q(W*m - s, W*m)
    require(0 < eta < 1, "The complex motif has no positive deficit")
    return dict(h=h, v=v, m=m, N=N, R=side_roles, W=W, L=L, s=s, eta=eta)


def verify_center(h):
    """Exhaust the compressed dyadic factorization on all ordered pairs."""
    triples = list(combinations(range(h), 3))
    for source in triples:
        for target in triples:
            if h - 1 not in target:
                twice_center = sum(i in source for i in target) - 1
            else:
                twice_center = 2 - sum(i in source for i in range(h - 1) if i not in target)
            intersection = len(set(source) & set(target))
            require(twice_center == intersection - 1, "Compressed center differs")
            twice_side = (1 - intersection) if source != target and intersection % 2 == 0 else 0
            require(twice_center + twice_side == 2*int(source == target),
                    "The combined shear matrix is not the identity")
    return dict(ordered_pairs=len(triples)**2, gaussian_dyadic_coefficients=True,
                compressed_center_exact=True, side_plus_center_is_identity=True)


def verify_sharing(h):
    triples = list(combinations(range(h), 3))
    image = [paired_triple(t) for t in triples]
    require(set(image) == set(triples), "Triple matching is not a bijection")
    for t, u in zip(triples, image):
        require(dot(indicator(t), indicator(u)) == 0,
                "Matched triple indicators are not orthogonal")
        outside = ((1 << h) - 1) ^ (indicator(t) | indicator(u))
        require(outside, "No norm-one witness for a reused-role residual")
    return dict(triples_checked=len(triples), explicit_bijection=True,
                paired_indicators_orthogonal=True, joined_frames_nested=True,
                joined_residual_unit_witness=True,
                map="stage 1 at (A,B), local role r -> stage 3 at (B,pi(A)), role r; pi flips every paired ground point")


def certificate(h=H):
    reports = []
    seen = set()
    for batch in batches(h):
        require(not seen.intersection(batch.sources), "Source triple assigned twice")
        seen.update(batch.sources)
        reports.append(batch.verify())
    require(seen == set(combinations(range(h), 3)), "Source partition is incomplete")
    c = sum(r["additions"] for r in reports)
    q = sum(r["output_uses"] for r in reports)
    n = counts(h, c + q)
    lo, hi = log_integer_bounds(n["m"])
    require(n["eta"] > COMPLEX_SAVING*hi, "Certified complex exponent is too large")
    exp_argument = Q(48, 5)
    exp_lower = sum((exp_argument**j / factorial(j) for j in range(16)), Q(0))
    require(exp_lower > n["m"] and n["eta"] > COMPLEX_SAVING*exp_argument,
            "The short written exponential comparison failed")
    numerator_lo, numerator_hi = log_ratio_bounds(1/(1-n["eta"]), terms=4)
    actual = (numerator_lo/hi, numerator_hi/lo)
    require(sum(r["checked_coefficients"] for r in reports) == n["v"]**2,
            "Not every ordered matrix entry was checked")
    from complex_pair_star_parameters import certificate as parameter_certificate
    witnesses = parameter_certificate(n)
    scalar_depth = 3*n["v"]**2*(12*n["R"]+4*n["v"]*h+10*n["v"]) + 8*n["W"]
    edge_count = 2*scalar_depth + 9*n["W"]
    total_depth = scalar_depth + 4*n["s"]
    node_charge = 64*(n["W"]+n["m"]+1)**3
    require(edge_count < 100*n["W"], "The expanded edge count exceeds the written bound")
    require(total_depth < node_charge, "New scalar circuit and child corrections exceed guard allowance")
    proof_files = ["notes/complex-pair-star-construction.tex",
                   "notes/compact-control-movement.tex", "notes/compact-control-layout.tex",
                   "notes/compact-control-guard.tex"]
    return dict(status="CONDITIONAL COMPLEX PAIR-STAR IMPROVEMENT; NOT FORMAL VERIFICATION",
                baseline_repository_commit=BASELINE_COMMIT,
                upstream_commit=verify_sources(), counts=n,
                circuit=dict(batches=len(reports), additions=c, output_uses=q, roles=c+q,
                             all_sources_partitioned_once=True, checked_coefficients=n["v"]**2,
                             compiled_integer_coefficients_exact=True,
                             source_gram_matrices_identity=True,
                             forward_and_reverse_frames_checked=True,
                             batch_reports=reports),
                center=verify_center(h), sharing=verify_sharing(h),
                complex_saving=COMPLEX_SAVING,
                logarithm_enclosure=(lo, hi), actual_complex_saving_enclosure=actual,
                complex_exponent_slack=n["eta"]-COMPLEX_SAVING*hi,
                short_exponential_proof=dict(argument=exp_argument, terms=16,
                                             lower_bound=exp_lower,
                                             recurrence_slack=n["eta"]-COMPLEX_SAVING*exp_argument),
                witnesses=witnesses,
                coefficient_depth=dict(scalar_operations_upper=scalar_depth,
                                       edge_count_upper=edge_count,
                                       inverse_child_corrections=4*n["s"],
                                       total_node_depth_upper=total_depth,
                                       retained_node_charge=node_charge,
                                       node_charge_slack=node_charge-total_depth),
                proof_sha256={name:sha256((ROOT/name).read_bytes()).hexdigest()
                              for name in proof_files},
                scope="Retains pinned upstream analytic and algorithmic interfaces, paired h=50 bit network, compact-control tape/layout/repair proofs, stopped guard and tight Gaussian accounting. New finite complex circuit and both binary frame directions have supplied proofs. No unconditional integer multiplication theorem or practical runtime claim.")


if __name__ == "__main__":
    result = certificate()
    path = ROOT/"certificates/complex-pair-star.json"
    path.write_text(json.dumps(serializable(result), indent=2, sort_keys=True) + "\n")
    print("PASS conditional complex pair-star circuit and exact assembly")
    print("Counts:", result["counts"])
    print("Simple saving: 59/10^11; sharpened saving: 5929220328/10^19 > 2^-31")
