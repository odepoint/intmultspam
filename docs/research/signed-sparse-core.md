# Signed sparse vectors: a constructive bit core and an unresolved side circuit

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new multiplication bound.** The integrated conditional witness remains
kappa=2^-31. This family supplies a positive bit-network construction through
the existing compiler, but its raw side circuit is much too large. The useful
output is a different positive-definite geometry and an exact side budget.
No novelty claim about the underlying orthogonality graph is made.

## Labels and central matrix

Let q>=2 be a power of two and h>=q. Take vectors in {0,+1,-1}^h with exactly
q nonzero coordinates, identifying each vector with its negative. Choose
the representative whose first nonzero coordinate is +1. There are

    n = 2^(q-1) C(h,q)

labels. Their ordinary rational Gram matrix has rank h: changing one sign
produces coordinate differences, and the signed-permutation orbit spans all
coordinates. Each label has norm q. Its orthogonal projection is xx^T/q.
All subspaces are nondegenerate for this positive-definite form.

Over F2 define C_xy=1 when x dot y is divisible by q. Since the dot product
lies in [-q,q] and the endpoints +/-q occur only on the same antipodal line,
C is precisely identity plus the orthogonality adjacency matrix. Thus its
off-diagonal ones satisfy both rational annihilation requirements.

## Explicit polynomial factor

Write p_i(x)=1 when x_i is nonzero and n_i(x)=1 when x_i=-1. In F2[[z]],

    (1+z)^(x_i y_i)
      = 1 + z p_i(x)p_i(y)
          + z^2/(1+z) [n_i(x)p_i(y)+p_i(x)n_i(y)].

This follows by checking the nine possible scalar pairs. Moreover

    C_xy = [z^(q-1)] (1+z)^(x dot y-1).

Indeed (1+z)^q=1+z^q, so the coefficient depends only on the exponent
modulo q, including for negative exponents. Among residues 0,...,q-1,
only exponent q-1 has a nonzero coefficient of z^(q-1).

Expand the product coordinate by coordinate. A term choosing r copies of
pp and s copies of np or pn has coefficient

    C(q-1-r-s,s) mod 2,

provided r+2s<=q-1; otherwise it is zero. Give p weight 1 and n weight 3.
Its two feature weights sum to 2r+4s<=2(q-1), so at least one side has
weight at most q-1. Assign terms with low left weight to the first factor
block; all other terms have low right weight and form the second block.
This is an explicit finite factorization of size at most 2M, where

    M = sum_b C(h,b) sum_{a=0}^{q-1-3b} C(h-b,a),
    0 <= b <= floor((q-1)/3).

The code expands these factors, including their coefficients, for small
controls. Large instances are justified by the general identity, not by
extrapolating those controls.

## Fixed-support refinement over F2

For a fixed negative-indicator set N of size b, the remaining support has
exactly k=q-b elements among H=h-b positions. Support monomials of degree
at most L=q-1-3b are rows of a stacked inclusion matrix. Its rank over Q is
at most C(H,min(L,k,H-k)). If L<=min(k,H-k), every degree-j monomial is the
sum of its degree-L extensions divided by C(k-j,L-j). Otherwise the number
of k-subsets itself bounds the rank. This proves the asserted upper bound
in both cases.

The matrix has integer entries, so reduction modulo 2 cannot increase its
rank: every larger minor is already the zero integer. Multiplication by
the common negative-indicator product and repetition over sign choices
cannot increase rank either. This avoids any division in F2.

Consequently the low-feature evaluation span has dimension at most

    M' = sum_b C(h,b) C(h-b,min(q-1-3b,q-b,h-q)),

and the central binary matrix factors through R=2M'. Finite binary
elimination of each feature block supplies a deterministic factor if
desired. R is an upper bound, not a claim of exact rank. The compiler
allows redundant central factors; using the stated upper bound is safe.

## Complete raw construction and hypothetical compression

The orthogonality degree is

    z = (1/2) sum over even j:
        C(q,j) C(h-q,q-j) C(j,j/2) 2^(q-j).

The signed permutation group is transitive on lines, so the orthogonality
bipartite graph is regular. Its positive degree gives a perfect matching
by Hall's condition, sufficient for the first/third-stage sharing theorem.
Using a separate side role for each ordered orthogonal pair gives S=nz.
The complete shared compiler charges

    m=h^3,
    W=2n^3+2n^2(S+R),
    Delta=n^3-6n^2 R h,
    s=Wm-Delta.

This includes every arbitrary scalar input and its restoration. Positive
deficit needs n>6Rh. At q=16,h=31 the certified factor has

    n=9,848,101,109,760,
    R=18,848,917,662,
    d=31.

The raw construction's bit saving is only about 7.83e-19, far below the
retained 2.96e-9. The hypothetical loss-preserving side budget for a_b>1.6e-7
is about 5.5555n roles. No side circuit attaining that budget is supplied.
Even granting the necessary storage floor S>=n-R is only a benchmark,
not a realizable construction.

The attraction is positive-definite frames and a larger side budget than
the earlier cube candidate. This does not settle whether any useful
compression exists. An XOR arithmetic shortcut alone is insufficient:
all internal frame transitions, stage sharing and arbitrary-input
restoration must fit the same ledger. Characteristic-zero realization
and routing obstructions continue to apply.

The audit scans exactly q in {2,4,8,16,32}, q<=h<=52, with these factor
bounds. Its maximizing budget is a result about that finite scan, not an
optimum over all signed-vector constructions. The complex interface and
the full multiplication assembly remain separate requirements.

Run `python3 -S scripts/audit_signed_sparse.py` and
`python3 -m unittest discover -s tests -p test_signed_sparse_core.py -v`.
