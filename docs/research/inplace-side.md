# An in-place side circuit: scalar success, rank-budget rejection

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

The retained conditional exponent remains kappa=2^-31. This bounded experiment
replaces the sum-DAG side embedding by an invertible circuit on exactly n side
roles. Its scalar action and arbitrary-scratch restoration work. Exact path
witnesses reject the specified elimination construction, allowing arbitrary
rational matrices at its internal gates while retaining its external frames.

## The scalar construction

For triples of an even h-point set let U be point incidence, C=UU^T over F2,
and A=I+C the intersection-one side map. The point Gram U^T U is zero when
h=2 mod 4 and is I when h=0 mod 4. Thus A is an involution in the former
case. In the latter it is singular, since AU=0 and U is nonzero, and cannot
be realized with exactly n side roles and permutation input/output maps.
This singularity does not exclude adding extra roles.

For h=2 mod 4, eliminate A by columns in lexicographic triple order, selecting
the smallest unused row with a nonzero pivot. Clear that column on every
other row without swapping physical rows. The final matrix is a permutation
P; if E is the row-operation sequence, EA=P and A=E^-1 P. Copy input j into
the role of its pivot, apply the reversed XOR sequence E^-1, then inject each
physical role into its correspondingly indexed target. This realizes A.

Inserted into the twelve-operation transparent invocation, the side contributes
Ax, the central map contributes Cx, and every arbitrary side and central input
is restored. Small checks give every role an independent formal bit and verify
both signed directions. The scalar role count would be n, versus 509,194 side
roles in the retained h=50 construction. This is not a rank improvement.

## Directed paths charge excess without choosing internal frames

For an edge u->v define

    excess(e)=rank(M_v-M_u)-rank(M_v)+rank(M_u) >= 0.

Along a directed path these signed rank changes telescope. A middle-mixer
path from copied triple S to injected triple T has endpoint matrices P_S
and I-P_T in the active factor. Their ranks differ by h-2. Under the retained
form I-J/9, the line product is proportional to |S intersection T|-1, and

    rank(I-P_T-P_S) = h-2  if |S intersection T|=1,
                     h    otherwise.

The latter follows by restricting to the two line images: when their product
is nonzero that two-dimensional block is invertible; the equal-line case is
I-2P_S. Consequently each directed nonorthogonal path charges at least two
units of excess. Edge-disjoint paths add their charges even if they share
gate vertices. Unused edges still have nonnegative excess.

The tensor lifting and complementary reverse invocation preserve this endpoint
rank calculation. With k such paths per invocation, the three n^2 invocations
therefore incur at least 6kn^2 excess in addition to the retained central
returns. The fixed negative-source edge costs remain charged. Hence

    Delta <= n^2 (n - 6h^2 - 6k).

The middle side paths are disjoint from the central-return edges. First/third
auxiliary reuse does not alter these local paths or their data boundaries.
Changing those boundaries or central frames would be a different experiment.

## Compact exact witnesses at the target-capable sizes

An elimination prefix fixes the source labels on its pivot roles. An actual
two-role XOR gate can route the two corresponding physical paths across
instead of straight. Choose vertex-disjoint pairs of physical roles and cross
each pair at one witnessed gate. This yields edge-disjoint directed paths
regardless of all later elimination steps. Every other gate uses straight
routes. No solver result or floating-point rank is used by the checker.

| Ground size h | Checked pivot columns | Single switches | Nonorthogonal paths k | n-6h^2-6k |
| --- | ---: | ---: | ---: | ---: |
| 42 | 191 | 73 | 151 | -10 |
| 46 | 767 | 196 | 415 | -6 |
| 50 | 1091 | 366 | 767 | -2 |

The [witness file](../../scripts/experiments/inplace_side_witnesses.json) lists
the exact pivots and switches. The checker regenerates the matrix, replays
each pivot, verifies the switch gates, verifies disjoint physical roles, and
counts the endpoint intersections. Invertibility guarantees every prefix can
be completed, but its unavoidable excess already exhausts the rank saving.

This rules out kappa>=2^-25 for the entire **specified even-h elimination
family with identical tensor factors and retained boundaries**. Below h=40
the retained central loss already prevents a positive deficit. For h=40,44,48,52,
A is singular. The three remaining cases up to 52 are rejected above. For
h>=54, the [core dimension bound](core-limits.md) excludes the target even
with more favorable side computation. It is not a rejection of all in-place
algorithms, other pivot schedules, extra side roles, or other frames at the
invocation boundaries.

Run `python3 scripts/audit_inplace_side.py` and
`python3 -m unittest discover -s tests -p test_inplace_side.py`.
The [certificate](../../certificates/inplace-side.json) records the scoped
claims and source hashes. The useful next target would need a different
side topology with a small nonorthogonal-path budget, rather than another
frame optimization inside these rejected circuits.
