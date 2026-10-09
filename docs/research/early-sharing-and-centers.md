# Earlier sharing and point-split central gates

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**The integrated conditional result remains kappa = 2^-31.** This bounded
pass tests two structural changes suggested by the previous mixed-point
round. Forward expansion and refactoring increases role counts. Splitting
the central gates gives a small, exactly certified local rank saving, but
no global tensor-network integration or stronger multiplication witness is
claimed here.

## 1. Earlier sharing: a bounded negative result

Starting from the previously factored intersection-one circuit, expose sums
one or two levels earlier by expanding intermediate nodes with bounded
fanout. Build the resulting reachable expression DAG, share repeated pairs
of terms greedily, and materialize a cancellation-free binary circuit.
All intermediate supports and every output coefficient, including zeros,
are checked exactly. This changes forward expressions; it is not another
iteration of the old adjoint factoring loop.

The budget is three expansion settings at h=10,12,20 and one conservative
full-size control. Here depth 2 expands one level below each retained gate,
while depth 3 expands two levels. Source circuits at small sizes have two
prior adjoint factoring rounds; the full-size source has four.

| h | Starting roles | depth 2, fanout 2 | depth 3, fanout 2 | depth 3, fanout 4 |
| --- | ---: | ---: | ---: | ---: |
| 10 | 1,779 | 1,856 | 1,855 | 2,021 |
| 12 | 3,652 | 3,879 | 3,960 | 4,339 |
| 20 | 22,830 | 24,785 | 25,914 | 26,752 |
| 50 | 447,488 | 510,700 | not run | not run |

The greedy pass fails to recover enough of the sharing destroyed by
expansion. There is no reason to spend a full-size frame audit on these
candidates. This rejects the tested heuristic, not early sharing in general,
and supplies no lower bound on circuit complexity.

## 2. Change the central gate grouping

The [earlier central optimality result](joint-frame-audit.md) retains four
grouped central gates, each with one common frame across the data bank and
all h central roles. Here each gather/scatter is refined into h point gates.
At point i the gather changes only z_i by the sum of X_T with i in T; the
scatter adds z_i only to Y_T with i in T. Gates in each sweep commute as
scalar maps, so their order may be chosen independently.

Every old invocation boundary, side gate and copy/injection frame is kept.
The first scatter D keeps frame zero, and the last gather B keeps frame I.
Only the first gather A and second scatter C change their point frames.
The full scalar schedule is still the transparent invocation

    L, J, inverse L, R, V, G, R, L, J, inverse L, G, V.

The change falls outside the old grouped-gate theorem. It neither
contradicts that theorem nor establishes a saving for arbitrary point frames.

## 3. Incident triples occupy a hyperplane

Let h>=6, h!=9, and use the rational form H=I-J/9. Triple indicators have
squared norm 2. For fixed i, the span E_i of triples containing i is

    E_i = {x : 3 x_i = sum_j x_j},     dim E_i = h-1.

Differences of these triples span the h-2 dimensional space of coordinate
differences off i, and any one incident triple supplies the remaining
dimension. A normal vector for E_i under H is

    n_i = 2 * 1 + (h-9) e_i.

Its squared norm is 4(9-h), which is nonzero. Thus both its line and E_i
are nondegenerate. Let Q_i be projection onto that normal line and write
the hyperplane projection as I-Q_i. If i in T, then

    P_T Q_i = Q_i P_T = 0.

Consequently replacing a first-gather frame I by I-Q_i does not cause an
extra data cost if this is the first point gate seen by each incident triple.
Likewise Q_i can replace a second-scatter frame zero without extra data
cost if it is the last point gate seen by each incident triple.

## 4. Two distinct points save four rank units

Choose distinct points i,j. Process i first in the first gather and give
its gate frame I-Q_i; all other first-gather gates have frame I. Process j
last in the second scatter and give its gate frame Q_j; all other
second-scatter gates have frame zero.

For X_T containing i, the relevant old path P_T -> I becomes

    P_T -> I-Q_i -> I.

Its charge is (h-2)+1=h-1, unchanged. For Y_T containing j, the path
0 -> I-P_T becomes

    0 -> Q_j -> I-P_T,

also with charge 1+(h-2)=h-1. Other data paths and every side edge retain
their old charge. The i-th central role now follows

    0 -> I-Q_i -> 0 -> I,

and the j-th follows

    0 -> I -> Q_j -> I.

Each costs 3h-2 instead of 3h. Thus the complete local rank charge is

    R h + 2 binom(h,3)(h-1) + 3h^2 - 4.

Terminals and their signed rank differences have not changed, so reducing
rank charge by four reduces the decreasing-dimension loss by two. The
point labels are all nested along each edge in one direction or the other;
projection-difference rank therefore retains its usual dimension accounting.

## 5. This hyperplane family cannot amplify the gain

Allow any set A of selected first-gather points and any set C of selected
second-scatter points. Use I-Q_i on A (I elsewhere), Q_i on C (zero
elsewhere), and keep D=0, B=I. Put all A points first and all C points last
in the respective sweeps. These orders minimize the data cost in this family.

Set s=|A|, t=|C|, u=|A intersect C|, v=binom(h,3), q=binom(h-1,2), and

    F(k) = k q - v + binom(h-k,3).

For a triple meeting A in k>0 points, its X path pays an extra 2(k-1).
If it starts with an unselected point instead, it pays an extra 2k, so
placing A first is optimal simultaneously for all triples. Summing gives
X excess 2F(s). The reversed argument gives Y excess 2F(t). Two different
normal-line projections differ by rank two, which accounts for transitions
between selected points.

A central role selected on only one sweep saves two units. A role selected
on both also saves only two: the middle transition I-Q_i -> Q_i has rank h.
The complete rank change is therefore exactly

    2 [ F(s) + F(t) - s - t + u ].

Now F(0)=F(1)=0, and, for 1<=k<h,

    F(k+1)-F(k) = q-binom(h-k-1,2) >= h-2.

For h>=6, F(k)-k is minimized uniquely at k=1, with value -1. Since u>=0,
the rank change is at least -4, attained by s=t=1 and distinct points.
This proves optimality only for the specified hyperplane choices and fixed
outer sweeps. It does not optimize arbitrary rational point-gate matrices,
different decompositions or boundaries across invocations.

## 6. Size of the opportunity and stopping decision

At h=50 the local decreasing loss falls from 2500 to 2498. If the saving
were carried through all 3v^2 invocations with the old tensor joins and
sharing unchanged, the global deficit would change from

    v^2 (v-6h^2)   to   v^2 (v-6h^2+12).

Its multiplier would be 4612/4600 = 1153/1150, about 1.002609. This is a
conditional sensitivity calculation; this pass does not supply the complete
tensor-stage integration, revise a global certificate, or claim a new kappa.
It is far too small to reach the next dyadic milestone. The side role count
is unchanged.

The result demonstrates that refining the grouped central gates can lower
their score. But repeating this particular hyperplane trick has a proved
local ceiling. Stop this family rather than launch a large parameter search.
For a larger gain, future central work must change another premise: different
point-frame matrices or a coupled schedule across invocation boundaries.
Future earlier-sharing work needs a construction that preserves existing
sharing while creating new shared sums, rather than this destructive
expansion followed by greedy repair.

## Verification and scope

Run `python3 scripts/audit_early_sharing.py` and
`python3 scripts/audit_split_centers.py`, or `make verify`.
The first verifies every full-size scalar coefficient. The second checks
complete physical edge graphs at h=6 for seven selections, and independent
rational path ranks at h=10, where the ambient form is indefinite. Formal
independent input bits verify forward and inverse scalar maps and restoration
of every arbitrary side and central input. The all-h formulas rely on the
proof above; small computations are controls, not substitutes for that proof.

Certificates: [early sharing](../../certificates/early-sharing-audit.json)
and [split centers](../../certificates/split-centers-audit.json).
Implementation: [forward refactoring](../../scripts/experiments/early_sharing.py)
and [central audit](../../scripts/audit_split_centers.py).
All retained multiplication witnesses and upstream files are unchanged.
