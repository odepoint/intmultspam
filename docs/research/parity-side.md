# Joint complex-side computation: scalar gain lost to a frame repair

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new finite saving or kappa is claimed.** This bounded experiment combines
the complex network's disjoint and intersection-two corrections. Its scalar
circuit is smaller, but the specified topology has a binary frame obstruction.
A deterministic repair has valid source-span phase transitions and uses too
many roles. Neither result excludes other parity circuits or other repairs.

## The joint scalar kernel

On triples S,T, twice the required side matrix is

    cos(pi |S intersection T| / 2).

Its coefficients are +1 at intersection zero, -1 at intersection two and
zero at odd intersections. For general source/target subset sizes the
experiment carries two kernels: even intersection with coefficient
(-1)^(intersection/2), and odd intersection with coefficient
(-1)^((intersection-1)/2). On a split ground set,

    E = E_left tensor E_right - O_left tensor O_right,
    O = O_left tensor E_right + E_left tensor O_right.

For each split and each pair of left source/target sizes, the planner chooses
the cheaper tensor contraction order. It compares against separate exact
intersection computations, including common-intersection/disjointness
factorizations. Equal signed sums are interned up to a common sign. All
additions have disjoint source supports, so no zero coefficient is obtained
by cancelling two unwanted paths. The audit checks every output coefficient.

The existing c+q reversible embedding generalizes to signed sums by signed
gather gates and ordinary fanout. Every elementary operation is invertible;
the transparent twelve-operation schedule still restores arbitrary inputs.
This explains the scalar role count, but it does not supply cheap frames.

At h=26 the joint circuit uses **82,720 side roles**, versus **89,622** in the
retained separately certified complex construction. The roughly 7.7% scalar
reduction is unusable with the proposed frames.

## A five-point obstruction to sharing

For distinct a,b,c,d,e, consider source triples ace and bde and target triples
abe and cde. Every cross intersection has size two, so each individual
connection is allowed by the complex side relation. But over F2,

    indicator(ace)+indicator(bde)
      = indicator(abe)+indicator(cde)
      = indicator(abcd) != 0.

Suppose a shared node has both source lines among its ancestors and both
target lines among its descendants. A nested nondegenerate frame U would
have to contain their source span and lie in the orthogonal complement of
their target span. Their common nonzero vector would then lie in both U
and U^perp, a contradiction.

This rejects arbitrary nondegenerate intermediate subspaces at that node,
not merely one chosen projector. It remains scoped to these source/target
labels and the nested-frame interface; it does not reject arbitrary scalar
topologies or every possible phase transfer theorem.

The h=26 circuit has 59 nodes with nonzero source/target span intersection.
Its first recorded witness contains exactly the five-point pattern on
points 21,22,23,24,25 (zero-based). A simple source-span/complement cut also
fails at many more nodes; that heuristic failure is not an impossibility
certificate and is not used to prove the scoped obstruction.

## A deterministic, expensive repair

For each nondegenerate source span U, compute its characteristic vector w_U,
defined by w_U dot v = v dot v for all v in U. If A is a nondegenerate
subspace of U, the nonzero residual U intersect A^perp is alternating
exactly when w_U belongs to A. Thus testing this vector certifies whether
the upstream orthonormal residual interface applies.

The repair removes degenerate source-span nodes. It also removes a node
of dimension greater than one when its characteristic vector is one of
its actual source labels: the edge from that source line could not have a
nonalternating residual. At each retained node, it expands old children
until every incoming retained source span has zero residual or a
nonalternating residual. Expanding only substitutes an existing signed
expression; it does not change any coefficient. The expanded inputs are
combined in a single multi-input gate at the retained source-span frame.

The audit checks every signed expression, every nested span edge and the
characteristic-vector criterion. Output spans are exactly target-line
complements. Every active source span is orthogonal to an odd target,
so it cannot contain the ambient all-ones characteristic vector; its
ambient complement is therefore nonalternating. These observations also
check fresh and retired role boundaries and the reverse complement frames.

If a retained gate has k inputs, it contributes k-1 to the reversible
addition count. With q output uses the side role count is

    S = q + sum_g (k_g-1).

At h=26 this specific repair uses **308,336** roles. It restores the frame
conditions at more than three times the retained side budget, so it cannot
improve the current complex saving. This is a cost of the specified repair,
not a lower bound on every repair of the scalar circuit.

| h | original parity side roles | repaired side roles |
|---|---|---|
| 8 | 724 | 938 |
| 10 | 2,271 | 3,283 |
| 26 | 82,720 | 308,336 |

The useful outcome is a sharper design rule: forbid the five-point shared
rectangle while constructing the DAG, rather than discovering it after
optimizing only scalar additions. A phase-aware recursive planner is still
an open option. This bounded round does not justify a broad search over
repairs of the existing scalar winner.

Run `python3 -S scripts/audit_parity_side.py` and
`python3 -m unittest discover -s tests -p test_parity_side.py -v`.
All retained multiplication proofs and the separately certified a_c>3.6e-8
construction remain unchanged.
