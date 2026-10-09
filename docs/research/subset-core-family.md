# First overnight screen: power-of-two subset cores

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

These families are newly analyzed in this repository; no priority claim about
their underlying graph or rank mechanisms is made.

**The integrated conditional bound remains kappa=2^-31.** This is a new
family of generatively specified bit cores and a quantitative research
screen toward kappa>=2^-25. It supplies no improved multiplication witness.
The direct networks are valid instances of the factored core compiler but
have much worse savings than the retained network. The promising numbers
below explicitly grant side computations that we do not know how to build.

## Target and assembly boundary

With the retained Gaussian accounting, kappa<a_b/5. Therefore the target
requires a_b>5/2^25, approximately 1.49012e-7, over fifty times the retained
2.96e-9. Both finite interfaces matter. A hypothetical pair

    a_b = a_c = 1.6e-7

passes the existing compact-movement parameter system for kappa=2^-25.
The audit supplies exact epsilon, beta, lambda, lambda-prime, all constraint
slacks and final margins. Keeping a_c=5e-9 fails, even with that improved
bit saving. These are parameter checks conditioned on the interfaces and
current guard hypothesis. They do not prove either new finite network,
its complex residual hypotheses, its scalar charge, or its guard constant.

## A larger label family with smaller useful rational dimension

Let q>=2 be a power of two, k=2q-1, and j=q-1. Use all k-subsets of an h-point
ground set, with h>k and h!=k^2/j. Define

    n=C(h,k), R=C(h,j),
    C_ST=C(|S intersection T|,j) mod 2,
    F_ST=|S intersection T|-j.

The binary central factor is explicit: let B be the incidence matrix from
k-subsets to j-subsets. Then C=B B^T over F2. Its inner size R suffices for
the compiler whether or not it is minimal.

In F2[x], (1+x)^t is the product of (1+x^(2^b)) over the set bits of t.
Consequently the coefficient of x^(q-1) is one precisely when the low
log2(q) bits of t are all one. For 0<=t<=2q-1 this means t=j or t=k.
Thus the central matrix has diagonal one and its only nonzero off-diagonal
entries occur at intersection j. The rational fitting matrix vanishes
there in both directions.

For the rational representation take the incidence vectors u_S and

    H=I-(j/k^2) J.

Their inner products are F_ST and their norms are k-j=q. The eigenvalues
of H are 1 and 1-jh/k^2, so the excluded case is exactly its degeneracy.
The k-subset incidence vectors span Q^h: their differences span the
coordinate-sum-zero subspace, and any one has nonzero coordinate sum.
Therefore this fitting matrix has rank h. No numerical rank test is needed
for the generative construction.

The retained compiler proof uses a central factor U V, not minimality of
its inner size. Charge all R central roles. The scalar identity, frame
inclusions, endpoint restoration, and central-loss count are unchanged.
A small complete control with an extra zero central factor independently
checks that this otherwise redundant role is charged rather than ignored.
Hence, with edge-explicit side roles,

    E=n C(k,j) C(h-k,q),
    m=h^3,
    W=2n^3+3n^2(E+R),
    Delta=n^3-6n^2 R h.

Positive deficit is equivalent to n>6Rh for this specified factorization.
These gigantic positive networks are specified by the compiler argument;
they have not been expanded into all their roles and matrices.

The q=2 case recovers the triple construction. The q=4 case uses seven-subsets
and triple-incidence central factors. It first has positive deficit at h=23.
At h=28:

    n=1,184,040, R=3,276, d=28,
    n/(R d)=12.908163...,
    Delta=888,376,917,657,715,200.

The retained h=50 triple core instead has n/(r d)=7.84. This improves the
core's central-loss ratio and rational dimension, while making its raw side
implementation prohibitively expensive.

## Screen the full side cost before optimizing

With a hypothetical loss-preserving side circuit using S roles per invocation,
replace E by S in the ledger. There is no stage sharing in this screen. Put

    f=1-6Rh/n,
    eta=f/[h^3 (2+3(S+R)/n)].

The rank-derived saving lies between eta/log(m) and
eta/[(1-eta)log(m)]. Exact rational logarithm enclosures give both sufficient
and necessary side-role budgets; their distinction is recorded explicitly.
At h=28, a sufficient budget for a_b>1.6e-7 requires

    S/n < approximately 4.41134.

This is a target for a new circuit and frame proof, not a result from
substituting an arbitrary role count. With S=0, the family would have enough
headroom; S=0 is not a supplied implementation.

The first concrete count baseline fixes the common j-subset J and partitions
disjoint q-subsets of the remaining h-j coordinates into rectangles. A finite
dynamic program chooses only row stars, column stars, and recursive ground-set
splits; it makes no global optimality claim. Each rectangle is charged
|sources|+|targets|-1 roles. The full count multiplies by C(h,j).

At h=28, q=4 this gives approximately 20,631.44 side roles per label, thousands
of times the target budget. The best saving in the tested h=23,...,40 range
is about 4.50e-11 at h=26, even granting loss-preserving frames. This is below
the retained bit saving. The complete new side-frame certificate is not
needed to reject this count baseline, and is not asserted.

A useful diagnostic is that materializing a separate input copy for every
fixed J already requires

    C(h,3) C(h-3,4)=35 C(h,7)=35n

roles. This applies to that independent-input model only. It is not a lower
bound on circuits that share roles or work across different J. Any serious
attempt on this family must avoid that replication and improve the frame
accounting for shared computation. Local optimization of the displayed
rectangle dynamic program is not a credible route to the overnight target.

The certificate also screens q=2,4,8,16 with h<=96. It records every positive
raw ledger and a hypothetical free-side benchmark. The best free-side point
for q=4 is near h=28. These finite scans do not exclude other h, different
binary central matrices, induced subfamilies, or nonsymmetric fitting pairs.

## Opposite-field companion and its additional obligations

For complex computation, a related candidate uses odd-weight binary label
vectors u_S in F2^h and the normalized rational central polynomial

    P(t)=product over odd v<k of (t-v)/(k-v).

P(k)=1, and its off-diagonal support lies at even intersections, where the
binary labels are orthogonal. For seven-subsets its values at t=0,...,7 are

    -5/16, 0, 1/16, 0, -1/16, 0, 5/16, 1.

Its degree is j. Expanding in binomial polynomials yields a rational factor
of inner size at most C(h,j). Indeed, if B_l is the incidence matrix from
k-subsets to l-subsets, then B_l=B_j D_jl/C(k-l,j-l), where D_jl records
containment of l-subsets in j-subsets. Every column space for l<=j is
therefore contained in that of B_j. Applying this to the binomial expansion
of P gives the claimed factor without assuming ranks over different fields
are interchangeable.

This checks a candidate scalar/label core, not the complete complex transfer.
The accompanying count screen provisionally uses its usual complex ledger

    Delta_c=2n^3-6n^2 R h.

It requires a new signed-schedule, binary phase-frame and residual-basis
argument before this ledger can certify a complex saving. Ground sizes in
the screen exceed 2k, leaving a spare coordinate outside each pair of labels;
that observation is useful for residual bases but is not a full proof.

There is a further quantitative obligation: the new role counts do not
satisfy the retained s_c<m_c^5 guard hypothesis, even with free side work at
h=28. The audit computes the least integer L with s_c<m_c^L for both raw and
free-side ledgers. A generalized stopping-depth estimate or a different
construction is required. It would be incorrect to combine a prospective
saving from this family with the current C1=5-4 beta+zeta without that check.

## Next decision

The seven-subset family is a useful new positive core with sufficient
optimistic headroom. It is not yet a competitive finite network. Retain it
as a target for shared, cancellation-aware side computation, while screening
other low-dimensional two-field families. Do not spend the main budget tuning
its independent-intersection rectangle circuit. The complex interface and
guard size must be scored alongside every prospective bit improvement.

Run `python3 -S scripts/audit_subset_cores.py` and
`python3 -m unittest discover -s tests -p test_subset_core_family.py -v`.
The [certificate](../../certificates/subset-core-family.json) contains exact
counts, outward saving bounds, hypothetical interface parameters, size screens,
and source hashes. It distinguishes actual raw compiler instances from
hypothetical side costs and unproved complex extensions.
