# A deferred-scatter block schedule and its readout cost

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**The integrated conditional multiplication witness remains kappa = 2^-31.**
This pass constructs an exact scalar schedule that carries row centers
through a block of column invocations. It restores arbitrary scratch and
uses no additional roles. Its natural coordinate-subspace implementation,
however, loses more rank at the late data readout than it can save on central
returns when canonical column-output frames are retained. A stronger screen
allows arbitrary cleanup and readout matrices and still rejects the candidate
if the column central frames remain unchanged and readout retains the carry.

This is a new scalar mechanism with a scoped rejection of its proposed frame
realization. It is not a proof that general block fusion is impossible.

## 1. Scalar construction

Let X and Y be v-by-v banks indexed by triples, v=binom(h,3). A row invocation
fixes second index b, updates Y[:,b] by X[:,b], and restores its auxiliaries.
A column invocation fixes first index a and updates X[a,:] by Y[a,:].
Let A be the chosen column indices and B the chosen row indices. The target
operation performs all rows in B first, then all columns in A.

For one row write G for triple-to-point gathering, R for point-to-triple
scattering, and S for the side map. Over F2,

    S + R G = I.

The retained transparent row schedule is

    L, J, inverse L, R, V, G, R, L, J, inverse L, G, V.

Its first scatter uses the arbitrary initial center vector z. Replace its
second scatter by one restricted to targets outside A. Defer its final
gather, but perform its final side copy immediately: this commutes with the
deferred central operations while X is still unchanged. The resulting prefix
is

    L, J, inverse L, R, V, G, R_outside_A, L, J, inverse L, V.

Every side auxiliary is restored at this point. For an original row source x
and target y, the centers hold z+Gx. Outside A the target is already y+x.
Inside A the target still equals y+Rz+Sx, lacking R(z+Gx).

Execute every selected column invocation completely, using the retained
inverse scalar schedule with logical banks exchanged. Then for each row b
perform:

1. Scatter its centers into X[A,b], compensating the column computation for
   the row contribution that was still missing when it read Y.
2. Scatter its centers into Y[A,b], completing the original row update.
3. Gather all of the current X[:,b] into the row centers.
4. Gather the selected entries Y[A,b] into those centers.

After the two scatters, Y is the required completed row result and

    X_current[:,b] = x + I_A Y_final[:,b].

The two gathers therefore add Gx to z+Gx, restoring z exactly. This reasoning
allows arbitrary initial z and arbitrary side/column auxiliary inputs. The
column routines restore their own scratch as usual. Different selected rows
have separate auxiliary banks and the late operations act on different cells,
so the argument applies to the entire block.

The new operations beyond the original program are one compensated scatter
and one restricted gather per selected cell. A triple has three incidences,
so the cost is exactly 6|A||B| additional primitive XORs and **zero additional
roles**. This is a finite scalar count, not a tape-time or rank-saving bound.
The selected center values are correlated sums of independent arbitrary
inputs; they are never assumed to be clean workspace.

## 2. A natural coordinate block

Choose a k-point subset K of the ground set and let A contain exactly the
triples meeting K. Thus

    q = |A| = binom(h,3)-binom(h-k,3).

The early scatter now handles triples disjoint from K. Their coordinate
span is the (h-k)-dimensional outside coordinate space when h-k>=4.
Let U be its orthogonal complement for H=I-J/9. It has dimension k and is
orthogonal to all early targets. It is nondegenerate unless h-k=9 (the
ambient h=9 is already excluded). The degenerate case cannot supply the
proposed projection frame and is not promoted to a construction.

Suppressing the third tensor line, the row active space is

    E_b = F tensor line(b).

After gathering, give the early scatter the projection onto
U tensor line(b). There are h-k center roles that it actually uses; each
loses h-k dimensions from E_b. The k centers indexed by K are unused by
this scatter, so they can keep their entire old frame E_b. It would be
incorrect to charge them an unnecessary transition through U.

Even crediting every subsequent center operation as free, this leaves
(h-k)^2 decreasing dimensions instead of h^2. The maximum saving is

    B(h,k) = h^2-(h-k)^2 = 2hk-k^2.

If h-k<=3, the outside targets do not necessarily span their coordinate
space. Our rejection screen instead gives away the entire return, taking
B(h,k)=h^2. This relaxation favors the candidate.

The proposed carry keeps U on all active centers until the late readout and
allows the unused centers to keep E_b. Partial contraction to another
representation, point-dependent carry subspaces, and different intermediate
data frames are outside the candidate audited here.

## 3. Late readout pays more than the saved return

Retain the canonical physical Y frame after each selected column invocation:

    F_(a,b) = I_(h^2) - P_a tensor P_b.

Require that frame again at the outer block cut. The candidate late operations
therefore take the physical Y_(a,b) wire on a path from F_(a,b) through its
late scatter frame M and back to F_(a,b), possibly through further gates.

For a in A, its triple meets K and is not orthogonal to U. A projector
frame whose image contains U tensor line(b) cannot equal F_(a,b). Hence

    rank(M-F_(a,b)) >= 1.

Rank subadditivity on the path before and after M gives a total charge of
at least two. This remains true if further restoration gates lie on the
path. Distinct selected cells are distinct physical Y wires, so these
charges may be summed without counting any edge twice. Retaining full E_b
on unused centers only strengthens their readout obligation.

The lower bound is consistent with an explicit frame: M=I_(h^2) makes the
loop charge exactly two, since I-F_(a,b) is rank one. This observation
does not certify the center or other wire transitions of a full assignment.

The late Y paths have zero signed rank change. Their charge is therefore
new excess in the rank-potential accounting. Fixed outer cuts keep the
total signed rank change unchanged. The column invocations' central frames
and returns are unchanged, and all baseline noncentral edges have zero
excess. Consequently, even granting free compensation on X, free final
gathers, and no other new loss, the net rank change for r selected rows is
bounded below by

    2r [ q-B(h,k) ].

For h>=10 this is strictly positive for every 1<=k<=h. When h-k>=4,

    q-(2hk-k^2)
      = (k/6) [3h^2-3hk+k^2-18h+9k+2].

The bracket decreases with k on 1<=k<=h for h>=10, and its value at k=h
is h^2-9h+2>0. When h-k<=3, q>=v-1>h^2=B(h,k) for h>=10. Thus the screen
covers the retained positive-deficit range (even h>=40), including favorable
relaxations for the degenerate or very small outside spaces.

At h=50, per selected row:

| k | Deferred columns q | Maximum central rank saving | Late Y charge at least | Net increase at least |
| --- | ---: | ---: | ---: | ---: |
| 1 | 1,176 | 198 | 2,352 | 2,154 |
| 5 | 5,410 | 950 | 10,820 | 9,870 |
| 10 | 9,720 | 1,800 | 19,440 | 17,640 |
| 25 | 17,300 | 3,750 | 34,600 | 30,850 |

Increasing the number of rows multiplies both sides of this comparison.
It does not make this realization profitable.

### Freeing column cleanup frames is insufficient by itself

The canonical cut immediately after a column invocation is not essential
to a weaker but sufficient rejection. Keep its second central scatter frame

    D_a = (I-P_a) tensor I,

and its outer Y cut F_(a,b). Between these cuts, allow arbitrary rational
matrices at copy, cleanup and late readout gates. At a readout from a center
retaining the carry, require that the reading matrix M have image containing
U tensor line(b). No self-adjointness, idempotence or tensor factorization is
assumed for M. As before, for a in A its image is not contained in the image
of F_(a,b).

For any matrices D,F with image(D) contained in image(F), equality in

    rank(M-D)+rank(F-M) >= rank(F-D)

would force the images of M-D and F-M to lie in image(F-D). Indeed their
combined column span has dimension at most the sum of their ranks, while
it contains image(F-D); under equality those dimensions coincide. Then
image(M) would lie in image(F), a contradiction. Therefore the rank sum
exceeds rank(F-D) by at least one. Applying triangle inequalities to any
intervening paths gives the same bound.

Here rank(F_(a,b)-D_a)=h-1 is the old increasing-path charge. Thus the
modified Y path has at least one additional rank unit per deferred target,
even after removing the canonical intermediate cut. Column central returns
remain unchanged. With all other new costs credited as zero, the block's
net rank increase is at least

    r [ q-2 B(h,k) ].

This is positive for every h>=15 and 1<=k<=h. For h-k>=4,

    q-2(2hk-k^2)
      = (k/6) [3h^2-3hk+k^2-30h+15k+2].

For h>=15 the bracket decreases with k<=h and is at least
h^2-15h+2>0. For h-k<=3, q>=v-1>2h^2 when h>=15. Thus this weaker bound
still covers every retained positive-deficit size. At h=50,k=5 it gives
5,410-950=4,460 extra rank units per row even with those favorable freedoms.

The one-unit bound cannot simply be replaced by two for arbitrary matrices.
For example, in dimension three take D=0, F=diag(1,1,0), and let M map e1
to e1+e3 and kill e2,e3. Its image leaves image(F), but the two ranks are
one and two, respectively: excess one. The implementation tests this control.

This strengthened screen still requires that the late reading matrix retain
the carried image and that the column central frames stay fixed. Dropping
or recoding that image before readout, changing those central frames jointly,
or changing the outer terminal contract is outside the theorem.

## 4. The complement of a block matters

The previous fusion screen measured overlap between selected row and column
spans. Keeping a subspace U through the *early, unselected* scatter imposes
another condition: U must be orthogonal to those unselected triple labels.
A handful of selected independent labels does not provide that property.

For any k-dimensional U, the triples orthogonal to U lie in a subspace of
dimension h-k. The triple indicators span F. Choose a basis of h triple
indicators and average its coordinate permutations. Each triple appears
equally often, and any (h-k)-dimensional subspace contains at most h-k
members of each basis. Therefore at most v(h-k)/h triples are orthogonal
to U, so at least vk/h targets must be deferred if all early targets are
to be orthogonal to U.

This is a necessary size bound for that common-carry mechanism, not for
all fused circuits. At h=50, keeping k=5 dimensions already requires at
least 1,960 selected column invocations by this bound; the concrete
coordinate family uses 5,410. The prior 5-by-5 overlap capacity screen was
only optimistic. It did not check compatibility with the unselected targets.

## 5. What remains useful and what is missing

The delayed block schedule is an exact reusable scalar identity with dirty
scratch restoration and no new roles. A matrix-frame realization that improves
rank is still missing. This pass rejects the realization that retains the
column central frames while reading the stored coordinate carry into the
old outer Y frames. Merely freeing column copy and cleanup frames does not suffice.

A continuation must remove a stated assumption: redesign the column central
returns jointly with the delayed readout, move readout before those returns
with all necessary scalar corrections, change the carried representation,
or use a different scalar topology. Merely
enlarging the coordinate block or reordering the two late scatters does not
remove the displayed cost. No all-frame impossibility theorem follows.

## Verification

`scripts/audit_block_carry.py` constructs every primitive XOR in both the
original and deferred schedules. Independent formal input variables check
the complete maps, unchanged exterior data, every arbitrary side and central
input, and inverse execution. Controls include coordinate blocks, an arbitrary
non-geometric selection, and empty selections. Rational geometry checks verify
the carried subspace and its exact nonorthogonal target set, including a
degenerate negative control. No full frame certificate is claimed.

Run `python3 scripts/audit_block_carry.py`, the `test_block_carry.py` tests,
or `make verify`. The [certificate](../../certificates/block-carry-audit.json)
records scalar programs, operation counts, rational geometry controls and
optimistic rank screens. All retained multiplication artifacts are unchanged.
