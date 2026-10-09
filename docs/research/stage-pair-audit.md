# Two-invocation fusion: a model and a boundary-size screen

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**The integrated conditional witness remains kappa = 2^-31.** This pass
constructs an exact region crossing a stage boundary, then tests 64 joint
frame assignments. Six improve the tiny h=6 score, but explicit formulas
exclude those six in the retained positive-deficit range. Two structural observations
help size the next experiment: merely changing an increasing boundary cannot
save rank, and sharing subspaces across a single row/column intersection
provides only one dimension of overlap. Neither observation excludes general
fusion with different scalar schedules or arbitrary joint matrix frames.

## Region and exact outer contract

Suppress the fixed one-dimensional third-factor label. Work in F tensor F,
dimension h^2. A stage-one invocation fixes second triple b and varies the
first triple. A stage-two invocation fixes first triple a and varies the
second triple. They share exactly X_(a,b) and Y_(a,b). All other data roles
meet fixed external cuts. Both auxiliary banks remain separate.

Let P_t be the rational projection onto triple line t, and write

    E = I tensor P_b,       D = (I-P_a) tensor I.

Stage one uses the existing forward scalar invocation and lifts its active
frame M to M tensor P_b. Stage two reverses and inverts the scalar invocation,
exchanges the logical banks, and lifts the complementary active frame as

    D + P_a tensor (I-M).

This is the retained paired construction's reverse frame assignment. It
does not reuse the forward middle frames in the wrong orientation.

The cuts before stage one are P_t tensor P_b on X and zero on Y. Its cuts
afterwards are E on X and (I-P_t) tensor P_b on Y. Before stage two, the
cuts are I tensor P_t on X and (I-P_a) tensor P_t on Y; afterwards they
are I_(h^2) on X and I_(h^2)-P_a tensor P_t on Y. At the common data
position, the two intermediate prescriptions agree, so those artificial
terminals are removed and the physical edges are joined directly.

Stage-one auxiliaries have outer cuts zero and E. These are cuts around
the invocation, not a claim that the full network's scratch terminals are E.
Stage-two auxiliaries have cuts zero and I_(h^2). All outer cuts stay fixed
in the search. Transitions from outside this region and the suppressed
third-factor complement are unchanged. Candidates can mix the first two
factors, but do not vary that complement or the third factor.

At h=6, a=(0,1,2), b=(1,2,3), the graph has:

| Quantity | Value |
| --- | ---: |
| Ambient matrix dimension | 36 |
| Physical roles | 418 |
| Assigned vertices, including terminals | 1,996 |
| Physical wire segments | 4,082 |
| Exact rational rank sum | 8,684 |
| Signed rank sum | 8,540 |
| Rank excess | 144 |

Each of the 418 input roles gets an independent formal bit. The complete
scalar circuit agrees with the two successive shears, restores every dirty
auxiliary input, and inverts exactly. This is a region of the full network;
the two shears alone are not asserted to form its final role permutation.
The small ground size has no positive global deficit in the retained family.

## Boundary-only frame changes have no saving

For any rational matrices M_u,M_v, define edge excess by

    e(u,v) = rank(M_v-M_u) - rank(M_v) + rank(M_u) >= 0.

For a fixed scalar incidence graph the signed rank changes telescope at
every gate, since the same frame occurs on every incidence and a gate
preserves the number of physical roles. Thus fixed outer terminals fix the
signed total, even when internal matrices are arbitrary.

Every edge of the current graph has zero excess except the two central
returns. Each return touches h central roles and contributes total 2h^2.
The h=6 graph verifies all of these ranks directly over Q.

Consequently, any frame change that leaves every positive-excess edge and
its endpoints unchanged cannot lower the total charge: the old zero-excess
edges can only acquire nonnegative excess. This rules out changing just the
seam copy/injection/cleanup frames, regardless of how general their matrices
are. Introducing a freely chosen extra cut on a fixed edge is also useless,
by rank subadditivity. A promising fused region must reach a central return
or change the scalar graph itself.

This argument does not say that a region reaching a return can improve it.
It is a necessary screen and explains the variables included below.

## Bounded joint-frame experiment

The four central vertices A1,C1,A2,C2 are the endpoints of the two decreasing
returns. Candidate perturbations use four rational matrices Q:

1. P_a tensor P_b, rank one;
2. I tensor P_b, rank h;
3. P_a tensor I, rank h;
4. a rank-h conjugate of I tensor P_b under the coordinate permutation
   (i,j) -> (i,j+i mod h).

The fourth is a projector but is not a single Kronecker-product matrix.
Its reshuffled matrix has rank six at h=6, whereas a nonzero product has
reshuffle rank one. Thus this search includes genuine cross-factor frames.

Seven patterns subtract Q at selected A vertices or add Q at selected C
vertices: each vertex separately, A1/C2 together, C1/A2 together, and all
four. An eighth pattern sets each pair A,C to the same matrix, eliminating
its central return entirely while charging the surrounding edges. Each is
tested with and without correlated changes on the four data seam gates.
This gives 4 times 8 times 2 = 64 explicit candidates.

Every affected physical edge is charged once, including side roles incident
to the changed copy or injection gates. No boundary, cleanup or auxiliary
transition is credited as free. Fifty-eight candidates are rejected by lower
bounds exceeding the baseline. Six improve the h=6 score: four save 32 rank
units, one saves 24, and one saves 16. Their scaling is audited below.

Baseline ranks are exact over Q. Candidate ranks are first bounded below
by reduction modulo 101, which avoids every denominator encountered here.
An increased modular lower bound rigorously excludes a rational improvement;
it does not pretend to equal the rational rank. Inconclusive lower bounds
trigger exact rational ranks, which certify the six small improvements. No finite-field
solution is being promoted to a rational frame certificate.

This is a bounded family of correlated changes, not an optimization over
all internal matrices. Most side frames and the scalar gate schedule remain
fixed. Failure of these 64 candidates does not establish local optimality
of the two-invocation region.

## The six tiny winners do not scale to the retained network

Four winners simply erase one return inside one invocation: replace A=I by
zero or C=zero by I in its active factor. Each saves 2h^2 on central wires
but adds two rank units on each of the v data wires in the affected bank:

    delta_single = 2(v-h^2).

This is -32 at h=6 and -16 at h=8, but positive for every h>=10. At h=50
it costs an extra 34,200 units. It provides no evidence of a fusion benefit,
since the successful changes need no variable shared boundary. The earlier
grouped-gate optimality theorem starts at h=10 and is not contradicted.

The remaining central-only winner takes A=C=I-P_a in the first active
factor and A=C=P_b in the second. Write z=3 binom(h-3,2) for the number of
intersection-one neighbors of a triple. For either invocation its central
charge falls by 2h^2. Data paths add 2(v-z)+2(v-1), since the rank of
I-P_t-P_a is h-2 for orthogonal triple lines and h otherwise, while
rank(P_t-P_a)=2 for distinct lines. The pair's exact change is

    delta_pair = 8v-4z-4-4h^2.

It is -24 at h=6, but +68 at h=8. Half this expression increases from h
to h+1 by 2(h-2)(h-4), so it is positive for every h>=7. This candidate
also separates into two independent frame changes; its gain at h=6 is not
created by the boundary join.

Adding the four seam changes gives the sixth tiny winner, -16 at h=6.
For all h>=6, each source-copy gate touches one data and one side role;
each injection gate touches one data and three designated partial outputs.
Thus the four changed gates have a total of 24 incoming/outgoing incidences.
Each perturbation has rank one. Rank subadditivity bounds the total further
charge reduction by 24, including edges with both endpoints changed, whose
perturbation ranks are charged separately. Consequently this candidate has

    delta_pair_with_seam >= delta_pair - 24 > 0   for h>=8.

At h=50 the two bounds are 133,824 and 133,800, respectively. All six
tiny winners therefore fail throughout the retained positive-deficit range
(even h>=40), without a costly large graph search. These statements concern
the six explicit candidates; they do not exclude different matrices at larger h.

## Why a shared-subspace route needs a wider region

The active return spaces of the two invocations are

    F tensor line(b),       line(a) tensor F.

Their intersection is line(a) tensor line(b), dimension one. A proposed
mechanism that saves only by sharing a subspace contained in both return
spaces therefore has at most one such dimension available. This is a
restriction on that mechanism, not a bound on arbitrary coupled matrices.

For a block of r row invocations and c column invocations, let B be the
span of the r fixed row labels and A the span of the c fixed column labels.
Then

    (F tensor B) intersect (A tensor F) = A tensor B.

In particular, an individual row's active space meets the combined column
space in dimension dim A <= c. An individual column has at most dim B <= r
shared directions. These identities follow by choosing vector-space bases
adapted to A and B; they do not assume positive-definite forms.

Suppose a candidate pays for its rank reduction solely by eliminating the
return on such shared directions, and otherwise retains h central roles
per invocation. Its fraction of removed central decreasing loss is at most

    (r dim A + c dim B) / ((r+c)h).

For r=c=q with independent selected labels this optimistic fraction is q/h.
At h=50 a 1-by-1 block has only 2% overlap by this measure; a 5-by-5 block
has at most 10%, and 25-by-25 at most 50%. These are necessary capacity
screens, not achieved savings. Frames, scalar realization, restoration and
all induced data costs remain to be supplied. In particular, it is invalid
to add pairwise savings while charging the same shared edge repeatedly.

A related screen applies without a subspace ansatz. Perturb a central
return's endpoints by matrices of ranks r_A,r_C. Rank subadditivity implies
that its edge excess changes in absolute value by at most 2(r_A+r_C).
Across its h center roles, the possible improvement is at most
2h(r_A+r_C). All initially zero-excess edges can only hurt the total.
Thus bounded-rank tweaks at the grouped return endpoints cannot remove a
fixed fraction of the 2h^2 excess as h grows. Substantial saving requires
perturbation rank proportional to h, additional topology changes, or both.

## Decision and next experiment

Stop searching this two-invocation perturbation menu. It supplies an exact
boundary-crossing model, 58 rejected small candidates, and six small gains
whose scaling fails in the retained positive-deficit range. It supplies no
improved positive-deficit finite network or multiplication exponent.

The next useful fusion experiment should specify a structured block of rows
and columns, or change the central scalar schedule to share computations or
restoration across that block. Before materializing a large graph, its
proposed saving should survive the overlap and rank-budget screens above.
The immediate design problem is a parameterized mechanism that saves a
positive fraction of central loss after every external and auxiliary edge
is charged. Merely enlarging the same numerical perturbation search is not
supported by this pass.

Run `python3 scripts/audit_stage_pair.py` and the focused
`test_stage_pair.py` tests, or `make verify`. The
[certificate](../../certificates/stage-pair-audit.json) records all candidate
lower bounds and the full baseline's positive-excess edges. The
[implementation](../../scripts/audit_stage_pair.py) is independent of all
retained witness generators and leaves existing proof artifacts unchanged.
