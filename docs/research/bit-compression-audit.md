# Bounded bit-network compression: stop before a larger search

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa. The integrated result remains `2^-31`.** This round tests
compression within the existing common-point side correction, with the same
central losses, source-span/complement frames and reversible compiler.

The best tested change reduces side roles per invocation from **509,194 to
509,146**: 48 roles, about 0.0094%. It retains the full scalar and frame
contracts, but the improvement is too small to justify replacing the current
witness. No new source patch or headline certificate is supplied.

The stronger finding is a **scoped obstruction**: independently relabeling the
existing paired local circuits and identifying equal intermediate sums cannot
reach `2^-30` at any admissible even ground size. This allows arbitrary choices
of which equal-sum decomposition to retain and subsequent pruning. It does not
rule out new local circuits, a different role compiler, mixed common-point
computations, changed central losses or another topology.

## Bounded experiment

The reproducible screen evaluates 73 distinct local configurations at `h=50`:

- Weighted recursive blocks of sizes 2, 3, 4, 6 and 8, with direct-sum cutoffs
  3, 4, 6 and 8 and three leave-one-out schedules.
- Three point orderings and four parenthesizations of the paired output sum.
- Two trees of source sums, filtered for each excluded pair.

The existing local circuit has 9,813 additions and 1,176 partial outputs.
The best local count is 9,812 additions. Larger blocks and the two source-tree
constructions are worse; the latter need 24,854 and 60,186 additions.
A smaller local count alone need not improve the global circuit, because
point ordering changes which sums can be shared across modules.

The screen therefore also builds 18 globally merged candidates, combining
pair blocks, cutoffs 3 and 4, the three vector schedules and three orderings.
The best is the original ordering and prefix/suffix schedule with cutoff 3.
All local coefficient maps are checked exactly, including their zero entries.
The winning merged circuit receives the retained full symbolic and both-frame
direction checks. Every intermediate sum still has disjoint input support
inside a common-point module. Thus its rational source span is positive
definite under `I-J/9`, and the existing reverse-complement argument applies.
There are no additional central or side rank losses.

The block extension includes the internal edges and vertex weights left
inside a larger block after deleting one or two vertices. Omitting these
terms would make the larger-block experiment incorrect. The exact support
checks catch such an error. All computations use the `c+q` reversible-role
compiler and restore arbitrary auxiliary inputs by the retained transparent
schedule; no zero-scratch or free-erasure assumption is introduced.

## A necessary role budget for the target

Retain the current final assembly. Because `lambda'>tau` and `epsilon<1/5`,
any witness has

    kappa < a_b/5.

Consequently `2^-30` requires `a_b>5*2^-30`, approximately `4.65661e-9`.
Write `v=C(h,3)`, `m=h^3`, and `R` for side roles per invocation. With the
retained central losses and full first/third-stage auxiliary sharing,

    W = 2*v^2*(v+R+h),
    D = W*m-s = v^2*(v-6*h^2),
    eta = D/(W*m).

If `ell <= log(m)` is an exact rational lower enclosure, then

    a_b <= -log(1-eta)/log(m) < eta/((1-eta)*ell).

This upper estimate is deliberately favorable to a proposed construction.
At `h=50`, the target requires **R <= 317,035** under this necessary screen.
The tested winner still has 509,146 roles. These are necessary budgets, not
sufficient certificates: layer and precision conditions would also need to pass.

## Why relabeling and equal-sum sharing alone cannot get there

In one local circuit, each input is an edge on the `h-1` points other than
its module's common point. Classify an addition by the intersection of the
edges in its formal support:

1. If that intersection is empty, its global triple support has exactly the
   module's common point. Call the node unshareable. No different module can
   produce the same formal sum.
2. If the intersection is a point, the global support is a pair-star: every
   triple contains that point and the module's common point. The same sum
   can occur in at most two modules.

A nontrivial addition cannot have a two-point local intersection: there is
only one input edge on those two points, and the summands are disjoint.
All local output sums are unshareable for the ground sizes considered.

Let `U` be the number of unshareable additions and `F` the number of distinct
pair-star additions that directly feed an unshareable addition. These are
mandatory boundary sums. Every active unshareable node remains necessary:
all nodes downstream from it also have empty intersection, and thus cannot
be identified with nodes in another module. Every one of its original input
sums is therefore still needed, including these `F` pair-stars.

Independent relabeling does not change `U` or `F`. Interning equal sums can
identify at most two of the mandatory pair-stars. Hence the retained compiler
has the lower bound

    R >= h*U + ceil(h*F/2) + h*C(h-1,2).

This bound credits **all other star subcircuits as free**. That distinction is
important: one cannot count half of all original star additions as mandatory.
Choosing another decomposition for a shared star can make its old children
unused, even when those children did not themselves have duplicates.

For the existing paired template at `h=50`,

    U = 4,389, F = 2,304,
    R >= 335,850 > 317,035.

Thus even this unrealistically generous sharing allowance misses the target.
Across all 73 screened local variants at `h=50`, the same optimistic bound
also stays below `2^-30`; none is rescued by arbitrary relabeling and merging
without changing its local gates.

### Ground-size coverage for the existing paired template

The certificate checks every even `h` from 40 through 110 with exact rational
logarithm enclosures and complete local coefficient checks. The largest
optimistic bit-saving upper bound is near `4.41046e-9` at `h=52`, still below
`5*2^-30`. This finite check applies to the existing paired template; it does
not assert an all-ground-size optimum over the new experimental templates.

For even `h<40`, `D=v^2*(v-6*h^2)` is nonpositive, so the retained accounting
has no positive deficit. For `h>=112`, a simpler bound covers the infinite tail.
There are `h*C(h-1,2)=3v` distinct unshareable partial outputs, each requiring
an addition, and the compiler retains `q=3v` output uses. Thus `R>=6v`,
`W>=14v^3`, and `eta<1/(14h^3)`. Consequently

    a_b < 1/((14*h^3-1)*log(h^3)).

The right side decreases with `h` and is already less than `5*2^-30` at 112.
Together these observations exclude the target for **every admissible even h
within the existing paired-template relabel/merge model**.

## Decision and next experiment

Stop this compression round. The 48-role saving is recorded, not promoted to
a new multiplication result. Further arrangement of the same paired modules
has an explicit target obstruction, so a large ordering search is unwarranted.

The next circuit experiment should change which intermediate sums are formed,
particularly by combining contributions from different common points, or
change the central/stage structure. A mixed-point circuit needs a new rational
nondegeneracy audit: the current positive-definite common-point span proof does
not transfer automatically. Scalar savings alone remain insufficient.

A less ambitious alternative is a genuinely different local pair-exclusion
circuit; the obstruction does not exclude it. This screen gives no evidence
that another small scheduling variation will provide the needed gain.

## Reproduction and verification boundary

Run `python3 scripts/audit_bit_compression.py`, the focused
`test_bit_compression.py` tests, or `make verify`. The code and exact comparisons
are in [the audit](../../scripts/audit_bit_compression.py), the candidate
families in [the experiment](../../scripts/experiments/bit_compression.py), and
the output in [the certificate](../../certificates/bit-compression-audit.json).

This is a bounded search and a written scoped counting argument. It does not
supply a general circuit lower bound, independent verification of the upstream
multiplication theorem, or a barrier to the general finite-network contract.
The published witnesses and patches remain unchanged.
