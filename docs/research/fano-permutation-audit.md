# Permuting auxiliary roles: two bounded completion tests

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa. The integrated conditional witness remains 2^-31.** This
round removes the requirement that each auxiliary return to its original
role. It tests two completion mechanisms for the three register realizations
from the [Fano completion audit](fano-completion-audit.md).

The first mechanism is excluded for all encoded-register permutations by
an exact symmetry argument. The second produces 144 complete arbitrary-input
scalar permutations; every one has an independently checked routing witness.
This does not exclude other completions or other all-role coding topologies.

## 1. Compute, permute encoded registers, decode

Let A be the invertible binary matrix of the clean compute/inject prefix,
now evaluated on independent arbitrary inputs on **all** roles. Consider
executing that prefix, a register permutation P, and the exact inverse prefix.
For the resulting scalar map to be a register permutation Q, it is necessary
and sufficient that

    A^{-1} P A = Q, equivalently P A Q^{-1} = A.

Thus P and Q give an automorphism of the bipartite support graph of A, with
row vertices distinguished from column vertices. This is a binary scalar
matrix argument, not a restriction on the permitted rational frame matrices.

We use exact color refinement: initially distinguish rows and columns; then
replace each color by its old color together with the multiset of neighbor
colors. Every graph automorphism preserves every refinement round. If all
vertices eventually have distinct colors, the only automorphism is identity.

For each complete compute/inject prefix (compact: 11 roles; decoded: 13;
edge-explicit: 26), refinement gives singleton colors for all vertices.
Consequently **only P=Q=I works in these three conjugation templates**.
Choosing more complicated encoded-register permutations cannot rescue this
particular method. This does not address different encoders, different
decoders, or several intervening coding stages.

The certificate contains the exact binary rows and every refinement round.
The implementation does not require a graph-isomorphism package or infer
rigidity from a failed search. Nonsingleton refinement would be inconclusive;
we would not treat it as a rigidity certificate.

## 2. Choose the decoding and output permutation together

The second mechanism completes the same prefix using binary Gauss-Jordan
elimination with freely located pivots. We do not swap rows into prescribed
pivot locations. At termination every row is a distinct unit vector, so the
actual input-to-output assignment defines the final permutation. Auxiliaries
may exchange with each other or with the six data roles.

The fixed bounded sweep has:

- Three layouts: compact, decoded, edge-explicit.
- Two output constraints: fully free; or original inputs a,b,c required at
  their original Fano target roles 3,4,5, with all other assignments free.
- Three pivot policies: smallest row support, largest row support, shuffled.
- Eight deterministic seeds for column order, tie-breaking, and update order.

This gives 144 specified circuits, not exhaustive coverage of all elimination
orders. SHA-256 ordering makes the sweep deterministic without a solver or
random-number-library dependency. Every circuit is checked on independent
formal input variables, including all original auxiliary inputs.

| Layout | Cases | Cases moving auxiliaries | Cases mixing auxiliary/data roles |
| --- | ---: | ---: | ---: |
| Compact | 48 | 43 | 42 |
| Decoded | 48 | 43 | 40 |
| Edge-explicit | 48 | 40 | 40 |
| Total | 144 | 126 | 122 |

All 72 cases preserving the three original Fano terminal assignments move
auxiliaries. The remaining identity/fixed-auxiliary cases are retained controls.
Thus this test actually exercises the weaker endpoint requirement; it does
not merely reproduce the prior fixed-scratch circuits under new names.

## 3. All 144 circuits are routable

For each circuit a saved straight-or-cross choice at every XOR gate defines
W edge-disjoint paths realizing its **actual complete scalar permutation**.
Reproduction reconstructs those paths and calls the independent endpoint,
continuity, and edge-disjointness checker in `finite_bit_contract.py`.
The fixtures are tied to the exact programs by hashes. Optional Z3 discovery
found the witnesses; replay uses only the Python standard library.

The existing routing obstruction therefore proves s>=Wm for every permitted
rational matrix frame assignment, in every dimension, on these 144 circuits.
There is no reason to optimize their frames. The obstruction is independent
of any orthogonal-projection or tensor-label ansatz.

## 4. Why terminal-preserving elimination loses the bottleneck

There is a simple mechanism beyond the numerical sweep. In these prefixes,
the original source roles retain their individual input values, and the
three target rows have an identity block in those three source columns.
The target rows also contain arbitrary target and auxiliary contributions.

To place input c at target role 3+c, our constrained elimination first chooses
that target row as pivot for column c, for c=0,1,2. Eliminating this column
from the original source row necessarily performs

    role[c] ^= role[3+c].

Earlier pivots have not changed that source row: its other source-column
entries were zero. Thus each of the three source/target pairs receives a
direct common gate during completion, regardless of the subsequent pivot
policy, seed, or output assignments on the other roles.

Route straight through the entire coding prefix, cross at precisely these
three gates, and route straight everywhere else. This routes the three
original Fano demands on disjoint paths. Separate exact partial-path checks
confirm this for all 72 constrained cases, independently of their full
routing fixtures.

This argument shows why this terminal-first elimination construction cannot
preserve the seed's **three-demand routing obstruction**. It does not prove
that every possible completion has a full all-role routing, nor that losing
this particular partial obstruction rules out all other full obstructions.
Full all-role rejection here rests on the 144 explicit witnesses.

## 5. Research decision

Stop extending generic permutation/inverse-computation and Gaussian-completion
sweeps on these three fixed prefixes. More output freedom alone has not
preserved the coding advantage. The concrete next design problem is a
balanced all-role gate topology whose local reversible operations and final
permutation are chosen together, without first appending a general decoder
to a clean code.

A useful first constraint is to retain a specified routing obstruction in
the full graph as it is built. The scalar permutation must satisfy that
obstruction's terminal requirements on independent arbitrary inputs. A
complete nonroutable circuit would justify a matrix-frame search; it would
still not establish a positive rank deficit. None is supplied by this round.

One bounded next experiment is to balance the original Fano DAG locally.
At each one-to-two branch add an independent auxiliary input; at each
two-to-one merge add an auxiliary output. Count the original source and
terminal stubs when balancing. This requires seven auxiliary inputs and
seven auxiliary outputs: ten roles in total, with fourteen two-port vertices.
Choose one of the six invertible binary 2-by-2 maps at each such vertex, and
require the full scalar map to be a permutation with the original three
terminal assignments and a free assignment of the other seven inputs.
The added stubs introduce no new path between the original sources and
terminals, so the three-demand routing obstruction is retained. Existence
of a compatible all-role scalar permutation is **untested**, not assumed.
If none exists in this bounded model, enlarging local gates or changing the
seed graph would be a substantive next step; ordinary completion cannot
be silently added without rechecking the obstruction.

These are scoped negative results about completion methods. They do not
establish a limitation on the general transfer contract, a lower bound for
integer multiplication, or the impossibility of a different Fano completion.

## Reproduction

Run `python3 scripts/audit_fano_permutation.py` and
`python3 -m unittest discover -s tests -p test_fano_permutation.py -v`.
The audit also runs with `python3 -S scripts/audit_fano_permutation.py`.
The [certificate](../../certificates/fano-permutation-audit.json) records all
scalar permutations, rigidity proofs, replayed routing checks, partial bypass
paths, and source hashes. No preceding research certificate, retained proof
artifact, or pinned upstream source is changed.
