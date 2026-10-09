# Limits that narrow the next core search

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: necessary conditions and a scoped rigidity result. No new
multiplication exponent. These statements concern the rank-one, three-stage
[core compiler](rank-product-core.md), not all finite networks.

## Auxiliary storage cannot be free

In a transparent invocation the binary central map C has a factor of inner
size r. The side map is I+C and factors through its S auxiliary roles as
JLV. Rank subadditivity gives

```
n = rank(I) ≤ rank(C) + rank(I+C) ≤ r+S.
```

Consequently the shared compiler has W≥4n³, rather than merely its data-bank
floor W≥2n³. This is a necessary bound even with an ideal side implementation;
it does not assume a cancellation-free sum circuit. It retains the separate
central/side invocation architecture and the stated first/third-stage sharing.

Since Δ<n³ and m=d³, its bit saving satisfies

```
a_b < 1 / ((4d³−1) log(d³)).
```

The retained Gaussian assembly requires κ<a_b/5. Exact rational logarithm
bounds exclude every d≥53 for κ≥2⁻²⁵. Thus d≤52 is necessary within this
architecture. A dimension passing the test is not a construction. Earlier
free-side benchmarks remain valid optimistic bounds, but cannot be attained
by setting the actual side storage to zero.

## A positive core needs binary rank at least five

Factor C=UV with r=rank_F2(C). Every row u_i of U is nonzero. Partition labels
by that row: if u_i=u_j, then C_ij=u_i v_j=C_jj=1. The rational fitting matrix
F is therefore diagonal and nonsingular on each class, so every class has
at most d=rank_Q(F) members. There are at most 2^r−1 nonzero row types, hence

```
n ≤ (2^r−1)d.
```

For r≤4 this contradicts the positive-deficit requirement n>6rd. Padding a
factor does not evade the restriction: it only increases the central cost.
The argument permits nonsymmetric C and F.

## Fully symmetric subset fitting matrices reduce to the linear case

Suppose labels are all k-subsets of [h], and F_ST depends only on |S∩T|.
Complementing labels permits k≤h/2. Express its entries uniquely in the
binomial basis, F_ST=Σ_l b_l binom(|S∩T|,l). If D is the largest nonzero
index, the Johnson eigenspace of index D has nonzero eigenvalue
b_D binom(h−2D,k−D), and dimension
μ_D=binom(h,D)−binom(h,D−1).

For h≥12, all μ_i with 2≤i≤⌊h/2⌋ exceed 52. To check the entire infinite
range, the successive multiplicity ratios decrease with i, so the minimum
on that interval lies at an endpoint. The first endpoint is h(h−3)/2≥54;
the other is the Catalan number with index ceil(h/2), at least 132.
Thus a target-capable F cannot have D≥2.

For h<12, exact finite comparisons give binom(h,k)≤30 min_{i≥2} μ_i.
Since a positive core needs r≥5, any nonlinear F again has n≤6rd.
A constant F has no off-diagonal zeros and forces C=I, also nonpositive.
Therefore a surviving radial F must be linear in intersection size. Its root
must be a permitted integer intersection j; otherwise C=I. The central
binary matrix can still be arbitrary inside that zero pattern.

The Johnson eigenvalue formula used here is recorded in
[Ghareghani, Ghorbani and Mohammad-Noori, *Intersection matrices revisited*, Lemma 8 and Theorem 9](https://arxiv.org/html/0902.4367v4).
The compiler limits and their application here are separate deductions.
This result does not exclude breaking subset symmetry, changing the label
family, using higher-rank labels, or changing the compiler or assembly.

## The usual incidence row space cannot thin the side graph

Let q be a power of two, k=2q−1 and j=q−1. Suppose each row of C belongs to
the span of the j-subset incidence features, its diagonal is one, and it
vanishes off the intersection-j relation. Then **C is forced to be the
canonical full-support matrix**, for every h≥k+j.

Fix a source S and choose A=S∪B with |B|=j disjoint from S. On the k-subsets
of A, the j-incidence matrix U_A is square. For distinct such subsets T,T',
their intersection exceeds j, and
binom(|T∩T'|,j)=0 mod 2; on the diagonal it equals one. Hence U_A U_Aᵀ=I.
The required restriction of the chosen C row is the unit row at S, so its
feature coefficients on A are uniquely the incidence row of S. Every
j-subset of [h] lies in some such A. All global coefficients are consequently
forced, proving the claim. This includes nonsymmetric proposed C.

Therefore deleting side edges while retaining the old incidence row space
is not an available optimization. A different binary row space remains a
legitimate search direction; no minimum-rank uniqueness is asserted.

Reproduce the exact thresholds, finite exceptions, small fitting-pair
controls and local rigidity matrices with `python3 scripts/audit_core_limits.py`.
See [the certificate](../../certificates/core-limits.json).
