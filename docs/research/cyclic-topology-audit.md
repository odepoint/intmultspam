# General finite-bit verifier and a routing obstruction

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa. The integrated conditional witness remains 2^-31.** This
round builds a general exact checker for the finite bit-transfer contract,
without the old bank exchange, stage cuts, geometric labels, or projection
assumptions. The first cyclic-routing experiment is rejected by a stronger
topological screen before matrix optimization is needed.

## 1. What the verifier accepts and checks

The input to `scripts/finite_bit_contract.py` consists of:

- W>=2 arbitrary-input roles, including every auxiliary role;
- a finite sequence of gates, each listing its physical ports and primitive
  XOR updates on those ports;
- m>=2 and one exact rational m-by-m matrix at every source, gate and sink;
- a declared permutation rho mapping input roles to output roles.

Every incidence of a gate has its one common matrix. The matrices may be
singular, non-idempotent, non-self-adjoint, nonproduct, or negative. All terminal
frames are free subject to the actual endpoint identities. A role previously
called scratch may participate in the final permutation: the verifier imposes
no separate scratch-restoration restriction.

Independent formal bits certify that the complete scalar map is exactly rho,
on all roles. Every physical wire segment is then constructed, including
untouched wires and source/sink segments. The checker verifies

    M_out(rho(w)) - M_in(w) = I_m  for every role w,
    s = sum_e rank_Q(M_head(e)-M_tail(e)).

The strict finite transfer condition is s<Wm. `inspect_candidate` requires
this by default. Its explicit `require_deficit=False` mode scores equality or
worse controls, and records that they fail the strict transfer contract.
Floating-point entries are rejected; integers, rational strings and exact
Fractions are accepted. The default does not certify a bound from a modular
rank computation or an approximate matrix.

For a saved JSON candidate, run `python3 scripts/finite_bit_contract.py
candidate.json`. Use `--score-only` for equality or worse controls. The schema
has top-level `W`, `m`, `rho`, `source_frames`, `sink_frames`, and `gates`;
each gate has `roles`, `xors` (target/control pairs), and its single `frame`.
Rational entries can be written as strings such as `"-2/3"`.

This is the contract in pinned upstream
[Section 4](../../upstream/build/sections/04-swap.tex), equation
`finite-shear-contract`. Passing the checker would verify the finite data,
conditional on the upstream transfer theorem; it would not by itself supply
a complex network or a new assembled multiplication witness.

## 2. Edge-disjoint routing rules out every matrix assignment

Collapse each common-frame gate to one vertex, with all its incoming and
outgoing physical wire segments incident to that vertex. A routing is a
collection of W directed paths, one from input w to output rho(w), with
no physical edge shared between paths. Paths may share gate vertices.
They need not follow the actual XOR dependencies: equality of the gate frame
is sufficient for the following telescoping argument.

For any one path, its edge differences sum to

    M_out(rho(w))-M_in(w)=I_m.

Rank subadditivity therefore charges that path at least m. Summing over
edge-disjoint paths gives

    s >= Wm.

This excludes a strict deficit for **every rational frame assignment and
every m>=2**, including completely free endpoint frames satisfying the
contract. No assumption about nested projections or the old tensor geometry
is used. Unused graph edges, if any, have nonnegative cost.

`find_routing` searches possible bijections between ports of each gate.
It emits explicit lists of physical edge indices for all paths. A separate
checker verifies their continuity, correct routed endpoints, and disjointness.
Search-budget exhaustion raises an error; it is never reported as a proof of
nonroutability. A routing is a sufficient rejection certificate. Failure to
find one within an incomplete search is not evidence of a useful network.

## 3. The cyclic seed family

We test full cycles on three through six roles, in adjacent-swap and star-swap
orders. Each swap is expanded into its three primitive XOR gates. All eight
circuits have explicit routing certificates for their actual scalar
permutations. Their rational frames therefore cannot beat Wm in any dimension.

The reason extends beyond the eight examples: route tokens through the middle
gate of each three-XOR swap as a swap, and through its other gates straight.
Composition routes the complete permutation. Merely expressing a longer cycle
as a sequence of these swaps cannot provide a deficit.

For each seed, zero source and gate matrices with identity sink matrices give
the equality control s=Wm. This is a valid scalar/endpoint control, not an
improved network. The general verifier also tests nonprojector rational
matrices and freely assigned source frames, rather than only this zero frame.

## 4. A broader joint-state search

To avoid restricting the experiment to visible swap words, enumerate arbitrary
two-port XOR words. For each prefix retain the joint state

    (A, R),

where A is the complete invertible scalar matrix over F2 and R is the set of
permutations routable through its gate graph. Initially A=I and R contains
only the identity. A gate t ^= s updates row t of A, while R becomes the union
of itself and the set obtained by swapping physical positions t and s.

Two optimizations preserve exhaustive coverage:

1. Merge identical joint states. Equal scalar matrices alone are insufficient;
   their routing sets can differ and are kept distinct.
2. Discard any state with R=S_W. Every future prefix still has all permutations
   routable, so that branch can never yield a nonroutable scalar permutation.

Whenever A is a permutation matrix, check whether that same permutation is
in R. If so, the routing theorem rules out every rational frame assignment.

For W=3 the numbers of newly reached, nonsaturated joint states by depth are

    1, 6, 33, 75, 78, 36, 6, 0.

There are 235 states total. The frontier closes, with no nonroutable scalar
permutation. Because both the scalar action and routing set determine every
continuation, closure proves exclusion for **all finite lengths** of three-role
two-port XOR words. The W=2 search also closes.

For W=4, the search is deliberately capped at seven primitive XOR gates.
It visits 529,066 distinct nonsaturated joint states and finds no nonroutable
scalar permutation. Its frontier does **not** close. This excludes all such
words through seven gates, not arbitrary four-role circuits.

The small-role conclusion also applies to grouped XOR gates in our verifier:
refine each grouped gate into its primitive two-port updates, assigning the
same matrix to each. Intermediate same-frame edges cost zero. A listed port
unused by those updates may retain a unary identity gate with that matrix.
Refinement preserves the rank charge and scalar action. Thus a grouped circuit
on at most three roles cannot evade the all-length exclusion.

These are exhaustive finite-state computations with a stated reduction to
arbitrary word lengths in the closed cases, not formalized proofs. The
certificate records each frontier size and hash; regeneration recomputes the
search. A separate short-word test enumerates raw words and checks routings
without using the joint-state pruning.

## 5. Decision and next milestone

Do not spend matrix-search budget on a topology with a routing certificate.
The necessary structural target is now a complete, arbitrary-input scalar
permutation circuit whose prescribed terminal pairs cannot be routed by
edge-disjoint paths through the common-frame graph.

That target does not demand a better multiplication exponent immediately,
but it is substantially more informative than a short XOR word or a cheap
local identity. Nonroutability would still be only a necessary condition:
the rational endpoint identities and strict rank deficit must then be solved
and checked independently.

The next candidate family should exploit cancellation in characteristic two
and change the incidence/topology, rather than hide a chain of ordinary swaps
inside a longer word. Any proposed coding construction must be converted to
the complete all-role permutation contract before it is accepted as a seed;
restoration or completion may restore routability or erase its advantage.
The complex interface remains a separate downstream obligation.

No improved finite network or rational-frame witness is supplied this round.
The contribution is the general verifier, a reusable dimension-independent
rejection certificate, and a more selective target for the next experiment.

## Reproduction

Run `python3 scripts/audit_cyclic_topology.py` and
`python3 -m unittest discover -s tests -p test_finite_bit_contract.py -v`.
The [certificate](../../certificates/cyclic-topology-audit.json) includes
the eight scalar seed circuits and explicit routes, equality rank controls,
the three joint-state searches, and source hashes. Tests also reject malformed
gates, wrong permutation orientation, missing auxiliary endpoint obligations,
floating-point frames, shared/disconnected paths, and exhausted search budgets.
No retained certificate, manuscript patch, proof note or upstream source is
changed by this round.
