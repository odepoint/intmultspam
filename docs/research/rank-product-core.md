# Recovering the positive mechanism before searching new topologies

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**The integrated conditional bound remains kappa=2^-31.** This pass works
backward from the successful bit network. It extracts a general two-field
core, supplies an explicit small-network compiler, and recovers a smaller
positive core within the existing triple geometry. The extracted example is
much weaker quantitatively than the retained network; it is a reference
construction, not an exponent improvement.

The main design target is now explicit: find a binary matrix of low rank
and a compatible rational representation of low dimension, with enough
labels to outweigh central returns, then charge the full auxiliary cost.
This retains a known route from a core to a complete arbitrary-input
permutation, instead of discovering completion and frames separately.

## 1. A sufficient core contract

The most general version used here takes a binary n-by-n matrix C and a
rational n-by-n fitting matrix F. Require:

1. C has diagonal entries one and rank r over F2. Factor C=UV with inner
   dimension r over F2; C need not be symmetric.
2. F has nonzero diagonal and rank d over Q; F need not be symmetric.
3. If i differs from j and C_ij=1, then **both F_ij and F_ji vanish**.

Factor F=BA with inner dimension d over Q. If a_i is column i of A and
b_i is row i of B, put P_i=a_i b_i/F_ii. These are rational rank-one
idempotents, and every required pair mutually annihilates:

    P_i^2=P_i, rank(P_i)=1, P_i P_j=P_j P_i=0.

The older geometric version is a sufficient special case: use nonisotropic
vectors q_i in a nondegenerate symmetric bilinear form H, and take
F_ij=q_i^T H q_j. The general version requires no common symmetric form.
The fitting-matrix factorization and all projector identities are checked
exactly by the compiler. One-sided zeros alone do not suffice.

Let E be the number of off-diagonal ones of C. The edge-explicit compiler
uses E side roles and r central roles per invocation. For a forward
invocation, the central gather/scatter implements Cx; a side role for each
off-diagonal one implements (C+I)x. Their sum is x in characteristic two.

The existing transparent schedule cancels arbitrary initial side and central
values and restores them. Three invocations, forward X->Y, inverse Y->X,
forward X->Y, exchange the banks. They operate successively on the three
coordinates of an n-by-n-by-n array of labels. Thus N=n^3 and m=d^3.

When C is nonsymmetric, stage two reverses the actual physical side
connections. Mutual annihilation is a symmetric condition, so those
connections remain admissible. It is not necessary to impose C=C^T.

This is a sufficient structured subclass of the general finite contract.
It does not assert that every useful finite network must have such a core.

## 2. The full rank ledger

Retain the upstream three-stage label assignment, replacing each triple
line by the corresponding q_i line, h label coordinates by d, and h central
roles by r. Use a separate auxiliary bank for every invocation; no sharing
or compressed side circuit is assumed.

In the symmetric-form special case every data line is nondegenerate.
Tensor products, its orthogonal complement, and the orthogonal sum of
neighboring lines are nondegenerate. Along a side role the essential inclusion is

    span(q_j) subset q_i-perp, whenever C_ij=1 and i!=j.

All the old label inclusions therefore remain valid. There are 3n^2
invocations. Each of the r central roles loses d dimensions once in an
invocation; no other edge decreases. Hence

    W = 2n^3 + 3n^2(E+r),
    L = 3n^2rd.

The signed sum of label-dimension changes is Wm-2N. Charging decreasing
edges twice gives Wm-2N+2L. The negative source projection on each X input
adds N rank, so

    s = Wm-N+2L,
    Delta = Wm-s = n^3-6n^2rd.

For the general idempotent version, replace orthogonal sums by sums of
mutually annihilating idempotents and complements by I-P. If idempotents
P,Q satisfy PQ=QP=P, then Q-P is idempotent of rank rank(Q)-rank(P).
This follows from Q=P+(Q-P), where the two summands mutually annihilate
and have disjoint images. The tensor-stage frames use only this relation,
the corresponding complements, and side differences I-P_i-P_j. The latter
are idempotents of rank d-2 by mutual annihilation. Thus every edge rank
and the same signed-rank telescoping ledger remain valid without a
nondegenerate common bilinear form. The first negative-source difference
is still 2P, of rank one over Q.

The source matrices are -P on X, zero elsewhere; sink matrices are I on X,
I-P on Y, and I on every auxiliary. Thus the actual exchange has endpoint
difference I on every input role, including arbitrary auxiliaries.

The compiler has a positive deficit **if and only if n>6rd**. Its relative
deficit is

    eta = (1-6rd/n) / [d^3 (2+3(E+r)/n)],

and its supremal rank-derived saving is a=-log(1-eta)/log(d^3). The strict
transfer inequality uses a smaller certified saving. A large n/(rd) alone
does not guarantee a competitive a: rational dimension and side roles
remain in the denominator.

Replacing E by the cost R of a smaller side circuit requires its own common
frame proof. Sharing stages likewise requires compatible joins. Neither
optimization is granted automatically by the core contract.

## 3. Why the two fields matter

The rational fitting matrix F has nonzero diagonal, and its off-diagonal
support is disjoint from that of C. If both matrices
had ranks at most r and d over the **same** field, their entrywise product
would be a nonsingular diagonal matrix, but would have rank at most rd.
Indeed, expanding rank factorizations expresses that product as a sum of
at most rd rank-one matrices. This would force n<=rd, far short of n>6rd.

The successful construction escapes because C has low rank over F2 while
F has low rank over Q. One cannot silently measure both ranks in the same
field. This isolates the characteristic-dependent advantage that a new
core must reproduce in this template.

For the retained core, n=19600, r=d=50. Therefore

    n/(rd) = 196/25 = 7.84,
    Delta/N = 1-6rd/n = 23/98.

The existing paired side circuit and its stage matching reduce W but do
not change this numerator. Their counts reproduce the published deficit
1,767,136,000,000 and relative deficit 23/661055000 exactly. Approximately
23.47% of the gross N saving survives the central returns.

### Changing only the binary rank has little room on the retained graph

This core view gives a further inexpensive screen. Keep the rational triple
lines, but allow an arbitrary binary diagonal-one matrix C, with any subset
of the intersection-one entries nonzero. Fix two ground points. The h-2
triples containing that pair meet each other in two points, so C restricted
to those labels is exactly an identity matrix. Thus rank_F2(C)>=h-2.

Also partition as many ground points as possible into disjoint blocks of
four, and take all four triples from each block. Within a block intersections
have size two; between blocks they have size zero. This gives an identity
minor of order 4 floor(h/4). Consequently

    rank_F2(C) >= max(h-2, 4 floor(h/4)).

This allows nonsymmetric C and does not assume the original incidence
factorization. At h=50, rank can fall from 50 to at best 48. If the paired
side-role count is retained, even granting rank 48 does not reach 2^-30 under
the existing Gaussian accounting; the certificate encloses the optimistic
bit saving. No rank-48 construction is supplied. A joint change that also
compresses the side map remains outside this numerical rejection.

Together with the older point-additive rational-label obstruction, this
suggests changing the core's incidence/orthogonality structure or the compiler,
rather than optimizing one of the two ranks while holding the rest fixed.

## 4. A smaller positive core, with a transparent boundary

For triples S,T on h points, retain

    C_ST = |S intersection T| mod 2,
    q_T = indicator(T), H = 9I-J.

Then q_S^T H q_T=9(|S intersection T|-1), and each norm is 18.
The off-diagonal ones of C occur exactly at intersection one, where the
rational inner product is zero. H has eigenvalues 9 and 9-h, so it is
nondegenerate for h!=9. Full incidence rank gives r=d=h.

For the full triple family, positivity is C(h,3)>6h^2. The ratio
C(h,3)/h^2 = h/6-1/2+1/(3h) increases for integers h>=4. It first crosses
six at h=39:

    n=9139, r=d=39, n-6rd=13.

Now delete the last twelve triples in lexicographic order. Exact binary
elimination exhibits 39 independent retained incidence rows. The same
integer minor is odd and therefore nonzero over Q, certifying both full
incidence ranks. The resulting core has

    n=9127, r=d=39, n-6rd=1,
    m=59319,
    W=4,306,768,634,441,207,
    Delta=83,302,129,
    eta=1/3,066,826,882,977.

Deleting a thirteenth triple preserves both incidence ranks but gives
n=9126=6rd and exactly zero deficit. Thus twelve deletions reach the
smallest positive label count at these fixed ranks. This is not a minimum
over arbitrary cores or representations. The degenerate ambient h=9 case
can be quotiented, as discussed in the older additive-label audit; it does
not challenge this positive-family threshold.

The core is smaller than the retained h=50 core, but its raw side network
is enormous. Its saving is only about 2.97e-14, versus the retained certified
2.96e-9. Even the full h=39 uncompressed core gives only about 3.85e-13.
These examples deliberately expose why reaching positive deficit is only
the first test. They are not proposals to replace the working network.

The positive circuits are specified by the written compiler and finite
core data. Their trillions of roles and rational matrices have **not** been
expanded and checked individually. The positive claim uses the general
rank-ledger argument plus exact core checks, as distinct from the small
fully expanded controls below.

## 5. A dimension screen before spending effort on a new core

In this three-factor, rank-one-label template, even granting free auxiliary
computation and zero central losses gives eta<1/(2d^3). Therefore

    a < 1 / [(2d^3-1) log(d^3)].

The right side decreases with d. Exact rational log enclosures certify:

| Objective | Dimensions excluded even by this optimistic screen |
| --- | --- |
| Beat the retained bit saving 2.96e-9 | d>=219 |
| Support kappa=2^-30 under retained kappa<a/5 accounting | d>=190 |
| Support kappa=2^-24 under that accounting | d>=53 |
| Support kappa=2^-16 under that accounting | d>=10 |

Passing a dimension screen is not a construction or an achievability claim.
The complex interface and all other assembly inequalities would also need
to support the target. These are scoped bounds for this template and the
specified accounting, not for the full rational-matrix contract.

In particular, the remaining d^3 address dimension is distinct from the old
cubic or quadratic conversion of a into kappa, which has already been
removed. Tensoring a weak core might improve n/(rd), but must still be
charged for its growing d and side circuit; it is not automatic amplification
of the multiplication saving.

## 6. What the exact compiler checks

`scripts/experiments/rank_product_core.py` factors C exactly over F2, checks
every required rational inner product and nonzero norm, builds all source,
gate, and sink matrices, and compiles every XOR and physical role in small
instances. The existing general finite-contract checker then independently
checks the full scalar permutation, all endpoint identities, and every edge
rank. Role-budget exhaustion raises an error rather than returning a partial
network.

Six expanded controls cover diagonal, symmetric rank-one, nonsymmetric,
indefinite rational, unequal-rank, and non-self-adjoint examples. All reproduce the formula
exactly. Their deficits are negative and the strict verifier rejects them;
they validate the compiler and bookkeeping, not a positive small example.

The last control uses C with packed rows (5,2,5) and fitting matrix

    F = [[1,1,0], [1,1,1], [0,0,1]].

Its first two projections are [[1,0],[0,0]] and [[1,1],[0,0]]. Requiring
both to be self-adjoint under a symmetric matrix H forces H_00=H_01=0;
every such H is singular. Exact linear equations check this. Thus the
extension truly admits representations beyond a common nondegenerate
symmetric form. This negative-deficit control is simultaneously triangular;
it is not evidence that those particular projectors could produce a saving.

The compact positive certificate records its removed labels, independent
incidence rows, exact pair-type identities, side-edge count, and rational
log enclosures. Removing vertices from the regular triple graph gives
E'=E-2kz+E_removed; small explicit graphs check this formula independently.

## Research decision and reproduction

Make the core-and-compiler route the main search baseline. Seek a genuinely
different two-field matrix pair with low d, a better n/(rd), and an affordable
side map. Require either an explicit complete rational-frame certificate or
a proved compatible compiler; a clean code or small rank in only one field
is insufficient. Changes to point-additive triple labels remain excluded
by the [previous obstruction](additive-label-obstruction.md), so that ansatz
is not reopened here.

The subsequent [stronger-screen audit](stronger-rank-screens.md) exhausts
the specified balanced-Fano model and finds no admissible all-role permutation.
Other topologies and the wider transfer-interface question remain open.
The core criterion is a sufficient construction, not a characterization of
that wider interface.

Run `python3 scripts/audit_rank_product_core.py` and
`python3 -m unittest discover -s tests -p test_rank_product_core.py -v`.
The audit runs without site packages via `python3 -S`. The
[certificate](../../certificates/rank-product-core.json) distinguishes
expanded controls from compact positive constructions and records source
hashes. Prior proof artifacts and certificates are unchanged.
