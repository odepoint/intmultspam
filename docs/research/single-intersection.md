# Single-intersection two-field screens

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: exact rank facts and a bounded family screen. No new multiplication
exponent or competitive side circuit. The retained conditional bound is 2⁻³¹.

The family has all k-subsets of an h-point ground set as labels. Set
C_ST = 1 when S=T or |S∩T|=j, over F₂; its rational fitting matrix is
F_ST = |S∩T|−j. The latter has rank d=h, except when hj=k², when d=h−1.
The nonzero diagonal is k−j. These two matrices fit the general bit compiler.

The audit covers 4≤h≤64, 2≤k≤min(15,⌊h/2⌋), 0≤j<k: 5,257 cases. It checks
constructive incidence-factor rank upper bounds, identity-minor lower
bounds, integer-spectrum parity bounds, and selected explicit independent
binary rows. Every case receives a recorded status, including unresolved
cases. The screen does not search all binary matrices supported on the same
rational zero pattern.

The exact feature expansion is
C = Σ_l a_l B_l B_lᵀ over F₂, with a_l = (binom(l,j)+[l=k]) mod 2.
Inclusion identities contain the columns of B_l in those of B_t whenever
binom(k−l,t−l) is odd. This bounds rank by the sum of the retained incidence
level sizes. Binary elimination on that column span is a finite factorization
procedure; the audit does not claim to expand the large resulting network.

For the spectral screen, the integer Johnson eigenvalues and their rational
multiplicities determine the characteristic polynomial. Reducing that
polynomial modulo two bounds the binary nullity by the algebraic multiplicity
of zero, giving rank at least the total multiplicity of odd eigenvalues.
This does **not** assume that a rational eigenbasis survives modulo two.
The inclusion and eigenvalue formulas are standard; see Lemma 8 and Theorem 9
of [Ghareghani, Ghorbani and Mohammad-Noori, *Intersection matrices revisited*](https://arxiv.org/html/0902.4367v4).
The characteristic-polynomial rank deduction and its application here are
checked separately in the repository.

An exact orbit certificate improves on these bounds for several six-subset
cases. It supplies independent feature rows and checks closure of their span
under every adjacent ground-set transposition. Since these permutations act
transitively on labels, the supplied rows span all feature rows. Writing the
full feature matrix as T P, with T full column rank, gives
rank(T P Pᵀ Tᵀ)=rank(P Pᵀ), over F₂. The smaller Gram matrix therefore
certifies the rank of the entire unexpanded central matrix.

Selected exact ranks for k=6,j=2 are 970 at h=20, 4,496 at h=32, and 7,807
at h=38. The latter two have positive compiler numerators. Positive numerator
alone is insufficient: the side circuit is still uncompressed. These cases
also do not overtake the seven-subset family's best hypothetical free-side
benchmark in this screen. No formula for all h is inferred from these points.

A separate identity-minor observation excludes j=k−1 throughout this
compiler: color a subset by the sum of its elements modulo h. Adjacent
subsets have distinct colors, so a largest color class gives an identity
minor of size at least ceil(binom(h,k)/h). This exclusion applies to any
unit-diagonal binary matrix with off-diagonal support contained in that
nearest-neighbor relation. Other screens are scoped to the specified C.

Run `python3 scripts/audit_single_intersection.py`. The
[certificate](../../certificates/single-intersection.json) records every
status and the [fixture file](../../scripts/experiments/single_intersection_witnesses.json)
contains the exact finite witnesses. Free-side benchmarks assume zero side
cost and are upper-direction targets, not achieved algorithms. Shared-stage
budgets are discussed separately in [shared-core.md](shared-core.md).
