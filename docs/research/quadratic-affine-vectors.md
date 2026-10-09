# Quadratic-phase affine vectors: twelve exact core screens

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

The retained conditional kappa remains 2^-31. This search tests explicitly
defined vector families from quadratic phases on binary affine subspaces,
including genuinely rank-two rational labels from complex lines. Every
specified full-orthogonality central matrix fails the positive-deficit
condition before any side-circuit cost is charged.

Binary quadratic descriptions of stabilizer states motivate these families;
see [Dehaene and De Moor, *The Clifford group, stabilizer states, and linear
and quadratic operations over GF(2)*](https://arxiv.org/abs/quant-ph/0304125).
The finite families, counts and rank rejections below are checked directly
from their formulas. No lattice identification or quantum algorithm is
assumed by the certificate.

## Explicit labels and their rational dimensions

Let D=2^t. For every affine k-subspace A of F2^t, choose the deterministic
basis and least coset representative specified in the generator. Coordinates
y in F2^k enumerate A. A real label has entries zero off A and

    (-1)^(sum_i b_i y_i + sum_(i<j) q_ij y_i y_j)

on A, where all coefficients are binary. Also test the two subfamilies with
k of fixed parity. A Gaussian label instead has entries

    i^(sum_i c_i y_i + 2 sum_(i<j) q_ij y_i y_j),  c_i in Z/4.

The value at y=0 is one, fixing the global phase. The support determines A.
Evaluation on e_i and e_i+e_j then recovers all coefficients, so every label
is distinct even as a line. The number of labels at dimension k is

    [t choose k]_2 * 2^(t-k) * 2^(k(k+1)/2)       (real),
    [t choose k]_2 * 2^(t-k) * 2^(k(k+3)/2)       (Gaussian).

The generator enumerates all linear subspaces, checks their Gaussian-binomial
counts, and checks that their affine cosets partition the ground set.

Real labels give rank-one rational orthogonal projections in dimension D.
Their span has exactly that dimension: even-support-dimension families
contain every coordinate unit; odd families contain e_a+e_b and e_a-e_b
for every pair, also spanning the ambient space.

For a Gaussian vector v=a+ib, the two real columns (a,b) and (-b,a) have
Gram matrix ||v||^2 I_2. Their rational projection therefore has rank two
in ambient dimension 2D. Two such projections mutually annihilate exactly
when the Hermitian inner product of the original vectors vanishes.
Coordinate-unit complex lines certify the full ambient dimension 2D.
Thus these are legitimate block labels, not duplicated old scalar labels.

## Specified binary matrices and exact rejection threshold

In each case C is **I plus every orthogonality edge**. Its diagonal is one,
and each off-diagonal one connects annihilating rational projections.
If its binary rank is r, the block compiler needs n*ell>6*r*d. Here d/ell=D,
so an independent binary-row witness of size ceil(n/(6D)) excludes positivity.

| t | Real labels, either parity | Rank lower bound | All real labels | Rank lower bound | Gaussian labels | Rank lower bound |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 120 | 3 | 240 | 5 | 1,080 | 23 |
| 4 | 2,160 | 23 | 4,320 | 45 | 36,720 | 383 |
| 5 | 73,440 | 383 | 146,880 | 765 | 2,423,520 | 12,623 |

Each parity is checked separately, giving twelve cases. These are stopping
lower bounds, not assertions of the complete binary ranks. The largest
certificate uses 12,623 independent rows on an explicitly listed minor;
the full 2,423,520-square matrix is not expanded. Integer bit masks compute
real and imaginary inner products exactly, followed by binary elimination.

The [fixtures](../../scripts/experiments/quadratic_affine_witnesses.json)
specify all label indices and independent rows. Replay uses no randomness
or numerical ranks. Small controls independently compare every packed
inner product with integer real/imaginary arithmetic and check the rational
rank-two projections and their products.

This rejects only those twelve **full-support central matrices**. Different
binary matrices supported on the same orthogonality graphs, subfamilies,
other phase families, or a different compiler remain outside the screen.
There is no supplied positive network in this family and no stronger
multiplication bound.

Run `python3 scripts/audit_quadratic_affine.py` to regenerate
[the source-hashed certificate](../../certificates/quadratic-affine-vectors.json).
