# Earlier readout with both coordinate returns changed

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa: the integrated conditional witness remains 2^-31.** This
final bounded continuation of the block-carry experiment moves the deferred
readout before the column central return and gives both row and column returns
credit for retaining coordinate-complement subspaces. The scalar schedule is
exact, with arbitrary scratch restored and no extra roles. An optimistic rank
budget nevertheless rejects every such coordinate block for h>=27, including
the retained positive-deficit range of even h>=40.

This is not a lower bound on unrestricted joint matrix frames or all fused
circuits. The high frames, specified early coordinate frames, outer cuts, and
the carried image at readout remain assumptions. The point is to test the
natural two-sided extension before moving research to a different topology.

## 1. Moving the readout earlier requires auxiliary corrections

Use the row prefixes from the [block-carry audit](block-carry-audit.md).
Selected row b retains centers z_b+Gx_b, while its selected Y entries lack
their central contribution. For selected column a, write delta_b for that
missing contribution. It is the XOR of the three retained row-center values
indexed by triple a; it need not be zero even on zero data because scratch
inputs are arbitrary.

The inverse column word, with logical source Y and target X, is

    V, G, L, J, inverse L, R | G, V, R, L, J, inverse L.

Insert the missing Y scatter at the displayed cut, just before the second
central gather. Split that gather into unselected and selected rows, in that
order. The split changes no scalar operation because all these XORs commute.

Let B map a source vector to the side compiler's input slots. Propagating a
source perturbation delta through the suffix produces

    Y: delta,   X: (RG+S)delta = delta,
    column centers: G delta,   side scratch: B delta.

The first two changes are exactly the desired late Y scatter and compensating
X scatter from the preceding experiment. The last two are unwanted. Repair
them after the column finishes by XORing G delta and B delta into their
existing roles. All delta values can still be read from the row centers.
No clean workspace is assumed or allocated.

After all columns, restore each row's centers by gathering current X over
the entire row and current Y over the selected columns, exactly as before.
The relation X_current=x+I_A Y_final proves that these two gathers add Gx.

In the retained compiler there is one side-source slot per triple. Per selected
cell the new corrections cost nine XORs into column centers, three into side
scratch, and three for the restricted final row gather. Relative to complete
unfused invocations, the total is **15 additional XORs per selected cell and
zero additional roles**. This is a scalar count, not a rank or tape speedup.

## 2. The two-sided coordinate candidate

Let F=Q^h, v=binom(h,3), with the retained form H=I-J/9. Work on two active
tensor factors; the third factor stays on its fixed line. Choose k ground
points in the first factor and ell in the second. Define

    A = triples meeting the first chosen set,
    B = triples meeting the second chosen set,
    q = |A| = binom(h,3)-binom(h-k,3),
    r = |B| = binom(h,3)-binom(h-ell,3).

Let U and V be the orthogonal complements of their respective outside
coordinate spaces, of dimensions k and ell. Where these subspaces are
degenerate, the projection candidate is unavailable; the numerical upper
credits below favor the candidate anyway.

The row's high frame is retained as E_b=I tensor P_b. Its early outside
scatter uses P_U tensor P_b on the h-k centers it touches. The other k
centers are unused by that scatter and may retain E_b. Thus an unavoidable
(h-k)^2 decreasing dimensions remain per row.

The column's high central frame is retained as I_(h^2). Change its outside
gather frame from D_a=(I-P_a) tensor I to

    Q_a = D_a + P_a tensor P_V.

The outside gather touches h-ell center roles. Each must travel from the
high frame to Q_a, a rank drop of h-ell. Hence (h-ell)^2 decreasing
dimensions remain per column. Unused centers may retain their high frames.
These are genuinely changes to both central returns, not merely new cleanup
frames around an unchanged column return.

Define the favorable decreasing-loss credit

    B(h,t) = h^2-(h-t)^2 = 2ht-t^2,  if h-t>=4;
    B(h,t) = h^2,                    otherwise.

The second case gives away the whole return, since the outside triples may
not span the outside coordinate space. The row and column returns together
can therefore save at most

    2r B(h,k) + 2q B(h,ell)

rank units. This already credits all subsequent central restoration as free.
It also credits every additional correction on X or side scratch as free.

## 3. A whole-wire readout charge survives the changed returns

For every selected cell (a,b), the physical Y wire begins this block at zero
frame and ends at the retained outer frame

    F_ab = I_(h^2)-P_a tensor P_b.

In the baseline it follows a nested path and its rank charge is rank(F_ab).
The new scatter reads a row center that retains U tensor line(b). Require
the common readout matrix M to contain this carried space in its image, as
in the preceding carry proposal. Since a meets the chosen k-point set, U is
not orthogonal to line(a). Consequently image(M) is not contained in
image(F_ab).

Rank subadditivity along the complete Y wire, both before and after that
readout, gives

    total Y charge >= rank(M)+rank(F_ab-M) >= rank(F_ab)+1.

For the last inequality, equality with rank(F_ab) would force the images of
M and F_ab-M to be contained in image(F_ab), contradicting the carried image.
This argument allows arbitrary rational M and arbitrary intervening matrices.
It uses neither the old column central frame D_a nor an intermediate cut
after the column. Moving the readout before its return therefore does not
remove this charge. Nonprojector matrices are allowed; only one extra unit
is claimed, as two would be false in general.

Different selected cells are distinct Y wires, giving at least qr new rank
units. Fixed outer cuts keep the total signed rank potential unchanged.
The baseline's only positive excess is 2h^2 per central invocation; its other
paths are nested. The row/column center paths above and these Y paths are
disjoint, so their lower bounds may be added without counting an edge twice.
The complete modified rank sum minus the baseline is therefore at least

    qr - 2r B(h,k) - 2q B(h,ell).                         (1)

This is an optimistic lower bound, not a full frame assignment. It charges
none of the extra auxiliary-repair operations from Section 1.

## 4. Every coordinate block fails in the retained size range

For h-t>=4, write q_t=binom(h,3)-binom(h-t,3). Direct expansion gives

    h^2 q_t - v(2ht-t^2)
      = ht(h-t)[h(h-t)-2]/6 >= 0.

Thus B(h,t)/q_t <= h^2/v. For h-t<=3 the favorable whole-return credit
satisfies B(h,t)/q_t <= h^2/(v-1). In all cases,

    (1) / (qr) >= 1-4h^2/(v-1) > 0  for every h>=27.

At h=27, v-1=2924>2916=4h^2; the difference increases thereafter.
This proves the all-size rejection for this candidate, beyond the finite
enumerations used as arithmetic controls.

At h=50:

| k, ell | Selected columns, rows | Y charge at least | Both return credits at most | Net increase at least |
| --- | ---: | ---: | ---: | ---: |
| 1, 1 | 1,176; 1,176 | 1,382,976 | 465,696 | 917,280 |
| 5, 5 | 5,410; 5,410 | 29,268,100 | 10,279,000 | 18,989,100 |

Increasing or unbalancing these coordinate blocks cannot reverse the result.

## 5. Scope and decision

This pass permits both specified returns to change and removes the prior
readout-timing restriction. It still retains:

- the row and column high central frames;
- the coordinate-complement outside-gate frames and incidence pattern;
- the row carry's image at readout;
- the block's outer data and auxiliary frames.

Recoding the carry, changing both high and low frames, using point-dependent
noncoordinate carries, changing outer contracts, or changing the scalar
topology can escape this screen. None is supplied or ruled out here.

Close this coordinate-carry fusion branch. The scalar identity remains useful,
but further size or cleanup searches within it cannot improve the rank budget.
The next research priority is a small complete finite circuit and rational-frame
certificate with a different topology, evaluated against the full transfer
contract. No new multiplication bound or complete improved network is claimed.

## Verification

Run `python3 scripts/audit_joint_return.py` and
`python3 -m unittest discover -s tests -p test_joint_return.py -v`.
The [certificate](../../certificates/joint-return-audit.json) records exact
formal-variable scalar controls, correction counts, inverse restoration,
full-size rank screens, and source hashes. Negative controls omit each of
the three necessary auxiliary repairs. Exact rational matrix checks and
finite arithmetic checks supplement, rather than replace, the arguments above.
All earlier certificates, proof notes, patches, artifacts and pinned upstream
sources are retained unchanged.
