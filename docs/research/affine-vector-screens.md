# Compact vector families: exact rank rejections

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: nine finite negative results for explicitly specified central
matrices. These do not exclude other supported matrices, induced subfamilies,
block representations, or different finite networks. The retained conditional
multiplication exponent remains 2⁻³¹.

The test is C=I plus every off-diagonal pair satisfying the stated rational
zero relation. A binary rank lower bound r with n≤6rd already rules out a
positive deficit in the current compiler, independently of side compression.
The computation stops at that rejection threshold: its reported lower bound
is **not an estimate of the actual rank**.

## Lattice-vector and affine variants

The explicit generator enumerates 98,280 antipodal line representatives in
24 rational coordinates, all of squared norm 32. It uses a cyclic generator
for the extended Golay code and checks its complete weight distribution,
all vector counts, norms, distinctness, and a full rational spanning minor.
The coordinates follow the minimal-vector construction summarized in
[Brouwer and Van Maldeghem, *Strongly Regular Graphs*, §6.3.1](https://homepages.cwi.nl/~aeb/math/srg/rk3/srgw.pdf#page=179).
The screen itself depends only on the explicitly checked vectors.

For F_uv=u·v, the rational rank is 24. A 715-column finite minor gives 683
independent binary rows, enough to reject the full specified central matrix.
Four further cases use all 196,560 signed vectors with
F_uv=u·v−c, for c∈{−16,−8,8,16}. Their rational rank is 25, verified using
augmented vectors and a nonsingular diagonal form. Each case has 1,311
independent binary rows on a 1,343-column minor, again sufficient to reject.
The full matrices are not materialized.

## Enlarged quadratic polynomial codes

Take sign vectors of constant-free Boolean polynomials in five variables.
Include every monomial of degrees one and two, then test these cubic additions:

- x₀x₁x₂;
- x₀x₁x₂ and x₀x₁x₃;
- x₀x₁x₂ and x₀x₃x₄;
- x₀x₁x₂, x₀x₁x₃ and x₀x₁x₄.

The families have 65,536, 131,072, 131,072 and 262,144 labels, respectively,
and rational dimension 32. The linear-polynomial subfamily is a full Walsh
basis, certifying that dimension. Orthogonality is Hamming distance 16.
The explicit binary row witnesses have ranks at least 342, 683, 683 and 1,366,
respectively. All four specified central matrices fail n>6rd.

The generator checks linear independence of its polynomial evaluations,
enumerates the exact Cayley row, and reconstructs each certified row by an
XOR translation. No floating-point ranks or heuristic solver statuses enter
the rejection certificate.

Run `python3 scripts/audit_affine_vectors.py`. The
[certificate](../../certificates/affine-vector-screens.json) records verified
ranks and hashes; the [fixtures](../../scripts/experiments/affine_vector_witnesses.json)
contain the finite row and column indices. Randomness was used only in discovery,
not in certificate replay. No new scalar completion or phase-frame theorem
is inferred from these negative rank screens.
