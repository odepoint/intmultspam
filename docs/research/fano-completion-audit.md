# Fano coding survives edge storage, but these completions become routable

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa. The integrated conditional witness remains 2^-31.** This
round tests a concrete characteristic-two coding seed against the all-role
finite-network contract. Its clean edge-level form has a certified routing
obstruction. Fifteen specified arbitrary-scratch completions, however, all
have explicit edge-disjoint routing certificates and therefore cannot yield
a rational rank deficit in any dimension.

The result concerns these completion methods. It does not exclude other Fano
constructions, all characteristic-dependent coding networks, or completions
that permit auxiliary roles to be permuted rather than individually restored.

## 1. Primary source and clean coding seed

The seed is the Fano network reproduced in Figure 1(a) of Das and Rai,
[Generalized Fano and non-Fano networks](https://arxiv.org/abs/1609.05815).
Their paper describes characteristic-two solvability and the obstruction in
other characteristics. We use the small characteristic-two code, not a claimed
conversion of that literature result into the bit-transfer theorem.

For three source bits a,b,c, the relevant XOR values are

    p=a+b, q=b+c, r=p+q, s=p+c, t=r+s,
    decoded a=s+q, decoded b=t, decoded c=r+a.

All additions here are XOR. Our implementation transcribes Figure 1(a),
contracting only the degree-two path marked e1 into a single capacity-one
edge. That preserves the terminal routing problem and gives 20 directed edges.
The source provenance is recorded in the certificate; the paper itself is not
bundled or modified.

The fixed all-plus code has integer transfer matrix

    [1 2 2]
    [2 3 2]
    [2 2 1],

which reduces to the identity in characteristic two. We check this exact code
and its failure as an identity over several odd characteristics. Those checks
do not independently establish the literature theorem about every possible
choice of coding coefficients.

## 2. The original routing obstruction is explicit

The graph has one a-to-its-terminal path, three b-to-its-terminal paths, and
one c-to-its-terminal path. A short certificate explains the incompatibility:

- Every a path must use edge u1->u3.
- Every c path must use the distinct edge u2->u4.
- Every b path must use at least one of those two edges.

Thus the three prescribed paths cannot be edge-disjoint. We verify the three
cut statements by exact reachability, and independently enumerate all path
options. The seed therefore has the coding-versus-routing property sought in
the preceding [topology round](cyclic-topology-audit.md).

This is still a clean network-coding instance with three independent sources.
It is not yet an all-role permutation circuit whose storage roles all begin
with independent arbitrary inputs.

## 3. Three reversible register realizations

We compare three ways to realize the same code using XOR updates:

| Realization | Auxiliary roles per invocation | Clean compute/inject XORs |
| --- | ---: | ---: |
| Compact | 5 intermediate-value registers; decode at injection | 15 |
| Decoded | 7 registers, including decoded a and c | 17 |
| Edge-explicit | 20 registers, one per original directed edge | 30 |

At this stage the auxiliaries are assumed zero and are not yet restored.
The partial routing test asks only for the three source-to-target paths.
The compact and decoded register graphs already admit such routes. Reusing
a value register for several outgoing uses does not preserve the original
network's capacity graph, even though it preserves the scalar formula.

The edge-explicit clean prefix retains exactly the path counts 1,3,1 and
the forced-cut obstruction. Its bottleneck segments are identified directly
in the physical XOR graph and checked by reachability. This gives a useful
control: loss of the original coding obstruction is not inevitable at the
storage-realization step.

## 4. Completing with arbitrary scratch

For one source-to-target addition, let the triangular computation act on its
auxiliary vector z as

    C_x(z)=A z+B x,

where A is invertible. Let C_0 be the same computation with source injections
omitted, so C_0(z)=Az. Let J inject the selected auxiliary outputs into the
target bank. Any direct source contribution Kx is handled separately.
The code identity is JB+K=I over F2.

The two blocks

    C_0 ; J ; inverse C_0,
    C_x ; J ; inverse C_x

add JAz and J(Az+Bx), respectively, to the target while restoring z. Together
with Kx, their net contribution is x, independently of every initial scratch
value. Either block order is valid. We test cancellation-first and signal-first.

Three such additions, X->Y, Y->X, X->Y, exchange the complete three-role data
banks and restore all auxiliaries. For each register realization we test
reusing one auxiliary bank across the three stages and allocating separate
banks. This gives twelve individually corrected complete circuits:

| Realization | Roles with shared / separate scratch | XORs in complete exchange |
| --- | ---: | ---: |
| Compact | 11 / 21 | 117 |
| Decoded | 13 / 27 | 150 |
| Edge-explicit | 26 / 66 | 294 |

Independent formal input variables verify the entire permutation, every
arbitrary auxiliary input, and inverse execution. Omitting C_0 from a single
addition works with zero scratch but fails to implement a clean addition on
arbitrary inputs. The complete three-stage exchange needs a more careful test.

### Shared offsets can cancel globally

That negative control exposes a useful simplification. With C_0 omitted,
one stage adds x+d, where d=JAz is independent of the source and target data.
If the three stages share the same auxiliary bank and coding maps, they have
the same offset d. The sequence

    y <- y+x+d;
    x <- x+y+d;
    y <- y+x+d

still exchanges x and y exactly. Every auxiliary is restored within its own
compute/inject/uncompute block. Thus the locally incorrect shears are globally
correct on arbitrary inputs; the cancellation-first blocks can be omitted.

More generally, with offsets d1,d2,d3 the outputs are y+d1+d2 and x+d2+d3.
Within this affine-shear model, complete exchange requires and is equivalent
to equality of all three offsets. Independent scratch banks do not satisfy
that condition in these constructions. This is checked as a negative control.

We therefore add three shorter shared-bank variants. Their complete XOR counts
are 75, 93 and 165 for compact, decoded and edge-explicit storage respectively,
instead of 117, 150 and 294. Their complete arbitrary-input permutations are
verified independently. The simplification is a reusable scalar identity;
it is not by itself a rank improvement.

## 5. All fifteen completions have routing certificates

An optional SMT search found a local straight-or-cross port choice at every
primitive gate for each completed circuit. The resulting W paths route the
actual full scalar permutation, including every restored auxiliary role.
All physical edges are accounted for and no two paths share an edge.

Discovery used the available Z3 solver, but acceptance and reproduction do
not depend on it. The saved fixtures contain switch choices and hashes of
their exact scalar programs. Standard-library code reconstructs the paths;
the separate checker from the general finite-network verifier checks all
endpoints, continuity and edge disjointness. Initial discovery timeouts were
not treated as nonroutability; every final case has a checked positive witness.

The routing theorem then forces

    sum_e rank_Q(M_head(e)-M_tail(e)) >= Wm

for every rational matrix assignment satisfying the endpoint identities,
in every m>=2. Free terminal frames, nonprojector matrices, and larger matrix
dimensions cannot rescue these particular completed circuits. Zero source and
gate frames with identity sink frames attain equality and are checked as
controls; none is an improving finite network.

The key comparison is therefore:

    original Fano graph: nonroutable;
    edge-explicit clean computation: nonroutable;
    tested dirty restoration plus three-stage exchange: routable.

We have isolated the loss to somewhere in the completion for the edge-explicit
version. This does not identify one uniquely culpable gate, prove that each
individual restoration operation causes the loss, or exclude every completion.

## 6. Research decision

Retain the edge-level coding seed and the exact verifier, but stop optimizing
frames or coefficients of these fifteen circuits. Their topological rejection
is independent of those parameters.

The next mechanism must preserve the coding obstruction while completing the
scalar network on every role. In particular, the transfer contract permits
auxiliary roles to end in a nontrivial permutation; all fifteen constructions
here impose the stronger condition of restoring each auxiliary individually.
Co-designing the output permutation and the completion, instead of adding
these transparent-restoration and three-exchange stages, remains untested.
Any such candidate still needs exact arbitrary-input scalar verification,
a routing screen, and then a full rational-frame certificate.

The result provides no improved network or multiplication exponent. It warns
against treating a clean coding advantage as one that automatically survives
reversible all-role completion, and supplies a small test case for improving
the completion method itself.

## Reproduction

Run `python3 scripts/audit_fano_completion.py` and
`python3 -m unittest discover -s tests -p test_fano_completion.py -v`.
Replay also works with `python3 -S scripts/audit_fano_completion.py`, without
site packages. The [certificate](../../certificates/fano-completion-audit.json)
contains the clean graph/cut checks, fifteen complete scalar checks, explicit
full routing paths, equality controls, and source hashes.

`scripts/routing_smt.py` is an optional discovery helper; its Z3 dependency is
imported only when discovery is requested. Saved routing witnesses are in
`scripts/experiments/fano_routing_witnesses.json`. Timeout or budget exhaustion
never certifies nonroutability. No preceding proof artifact or certificate is
changed by this pass.
