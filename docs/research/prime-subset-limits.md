# A ceiling for common-subset prime-power side circuits

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

This is a necessary bound for one explicitly specified construction family,
not a limit on finite alphabets or general rational-frame networks. It does
not change the conditional 2^-30 witness.

Let q be a prime power with characteristic p, k=2q-1, j=q-1, and take all
k-subsets of [h]. The scalar center is the j-subset incidence matrix B times
its transpose over Fp. Lucas's identity gives

    C(t,j) mod p = 1 for t=j,k, and 0 otherwise, 0<=t<=k.

Thus the side map is minus the intersection-j relation. Rational indicator
labels have form H=I-(j/k^2)J, inner product |S intersection T|-j, and norm q.
Retain the shared three-stage rank ledger, with n=C(h,k), r=C(h,j), d=h:

    W=2n^3+2n^2(S+r),  Delta=n^3-6n^2*r*h,  m=h^3.

Here S is the side-role count in the c+u-role cancellation-free sum compiler.
No different center, stage boundaries, output encoding or side compiler is
included in this screen.

## The center factor cannot be reduced within this map

On a ground set of size 3q-2, the incidence matrix B is square. Two distinct
k-subsets intersect in at least q points, so the Lucas support identity makes
BB^T=I. On every larger ground set, a linear dependence among the columns
of B restricts to a dependence on the j-subsets of any such smaller ground
set, and is therefore zero there. Every j-subset is contained in one of
those ground sets. Hence B has full column rank r; B^T is surjective and B
injective, so BB^T has rank exactly r. This permits arbitrary factorizations
of this same central map; none has fewer coordinates.

## The partial-output representation already uses too many roles

For every target T and common subset J contained in T, the partial sum has
source support

    {A: |A|=k and A intersection T=J}.

There are M=C(k,j) such outputs per target, hence u=M*n partial outputs.
If Delta>0, necessarily h>=3q: for h<=3q-1,
C(h,k)/C(h,j)<=C(3q-1,k)/C(3q-1,j)=2, whereas positive deficit requires
that ratio to exceed 6h.

At h>=3q each partial support has C(h-k,q)>1 terms. Its source-label
intersection is exactly J, and the complement of its source-label union
is exactly T minus J. Thus the support reconstructs (T,J), so all u outputs
are distinct nonsingleton sums. A cancellation-free binary addition DAG
must have at least u addition nodes, even after arbitrary equal-sum sharing.
Consequently c>=u and

    S=c+u >= 2*M*n.

This bound does not apply to a side circuit that combines or changes the
partial-output representation, or uses a different reversible embedding.

## Exact envelope and infinite tail

For each positive-deficit case substitute S=2*M*n, which is optimistic, and
put

    eta_max=(n-6*r*h)/(2*h^3*(n+2*M*n+r)).

The bit saving is bounded above by
`eta_max/((1-eta_max)*log(h^3))`, since `-log(1-x)<x/(1-x)` for 0<x<1.
The retained Gaussian assembly requires kappa<a_b/5. Rational logarithm
enclosures show that every prime-power q with 2q-1<=h<65 has ceiling below
2^-26. For h>=65, the general rank-one side-rank bound W>=4n^3 already
excludes that target; its explicit upper bound decreases with h. This covers
all prime powers and all ground sizes, not merely a sampled range.

The strongest finite upper envelope occurs in the ternary q=3 family.
Its precise rational enclosure and maximizing ground size are recorded in
[the certificate](../../certificates/prime-subset-limits.json). Even the
optimistic envelope cannot reach 2^-26, and therefore cannot reach 2^-25.
This does not rule out further improvements from 2^-30 inside the family.

Reproduce with `python3 scripts/audit_prime_subset_limits.py`. The audit
also expands the square incidence identities for q=2,3 and checks every
partial output support for (q,h)=(2,6),(3,9). The support-reconstruction proof
above establishes the general statement; the small checks are independent
controls. This screen says the next large jump must change the partial-output
representation, the network compiler, or the two-field geometry.
