# Ternary five-subset construction: conditional 2^-30

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

The complete construction audit and exact downstream assembly support a new
conditional witness **kappa=2^-30**, pending publication. The independent
[patch](../../patches/ternary-30.patch) applies directly to the pinned original.
The [note](../../artifacts/ternary-note.pdf) and full patched manuscript build;
the three integration tests pass. This remains dependent on the upstream
multiplication theorem and retained compact-control/Gaussian extensions.

The new finite-alphabet transfer proof is in
`notes/finite-alphabet-transfer.tex`. The prime-scalar raw compiler in
`scripts/experiments/prime_core.py` passes four targeted tests, including
nonbinary coefficients, arbitrary field inputs, all endpoint identities
and all rational edge ranks. It corrects the signed bank exchange by a
final negation at the existing identity frame, adding no rank charge.

## Construction

Use scalar field F3 and rational labels indexed by five-subsets of [h]:

    C_ST = C(|S intersection T|,2) mod 3,
    H = I - (2/25) J,
    F_ST = indicator(S)^T H indicator(T) = |S intersection T|-2.

C has diagonal one and off-diagonal support exactly intersection two.
Its central factor is the incidence matrix of pairs against five-subsets
times its transpose, with r=C(h,2) coordinates. Rational label norms are
three. The side map is minus the intersection-two adjacency matrix over F3.

For each common pair J, compute disjoint triple sums on the remaining
points, inject each output with coefficient -1, and retain all ten partial
outputs per five-subset target. Every source sum in one such group lies
in a positive-definite subspace for H: its vectors satisfy equal coordinates
u_a=u_b for J={a,b} and sum(u)=5u_a, giving

    u^T H u = sum_{i outside J} u_i^2.

Sharing exactly equal sums across groups preserves those source spans.
Forward source-span and reverse complement frames are therefore available;
the complete twelve-operation and tensor-stage proof is supplied in
[the construction source](../../notes/ternary-five-subsets.tex).

The most successful current variant uses one common disjoint-triple DAG
on all h points. In group J, set source variables meeting J to zero, retain
only output triples disjoint from J, and prune. These zeros denote absent
formal inputs, not initialized scratch registers. Equal sums are interned
within each group and across groups. For cross-group sharing, the common
intersection of the full five-subset sources has size at least three:
encode a common triple plus a set of residual pairs, or a common four-set
plus a set of residual points. These signatures determine the complete
formal sum exactly. First-occurrence decompositions are retained, and all
unused nodes are pruned after the groups have been combined.

## Certified counts and conditional assembly at h=29

The reproducible implementation is
[scripts/experiments/ternary_side.py](../../scripts/experiments/ternary_side.py).
Its [audit](../../scripts/audit_ternary_side.py) regenerates the full h=29
integer DAG and records counts and hashes in the
[certificate](../../certificates/ternary-side.json). At h=8,9 it independently
reconstructs every formal source sum and partial output coefficient, verifies
both signed scalar directions on independent arbitrary inputs, and computes
every rational frame transition in both directions.

    n=118755, r=406, m=24389,
    active additions=19593239,
    partial output uses=1187550,
    side roles S=20780789,
    N=1674772079218875,
    W=589493540769997500,
    L=498137336383050,
    Delta=678497406452775,
    s=14377157287342062574725.

Using the shared compiler formula, the rational lower enclosure of the
bit saving is approximately 4.67167497984e-9, exceeding a_b=467/10^11.
The following parameter witness passes the existing exact numerical
constraints, with the compact-control overhead substitutions:

    a_b=467/10^11, a_c=5/10^9,
    epsilon=1999/10000, c=1, beta=1/100,
    delta=1/10^6, C1=4961/1000,
    lambda=1-4669/10^12,
    lambda'=1-4668/10^12,
    kappa=2^-30.

The minimum exponent margin is 2332833/2500000000000000. Its excess over
2^-30 is 296652863/163840000000000000000. The complete construction proof and integration accompany these numerical
checks. The retained complex network suffices; the larger separately banked
complex saving is not needed for this witness.

## Verification and scope

The audit passes the exact full construction counts, small complete coefficient
maps, signed invocation restoration, rational frame transitions, and all seven
assembly margins. Four prime-scalar tests cover nonbinary coefficients,
asymmetric maps and the final sign correction. Five side tests cover the
sharing and physical invocation interfaces. Three patch tests cover retained
proofs, changed parameters, derived powers, and all internal references.

All 358 repository tests pass. The new standalone and patched manuscript builds pass. The previous witnesses,
source files and certificates remain unchanged. These checks do not constitute
independent verification of the upstream multiplication theorem, a full
machine simulation, or a practical speedup claim. No commit or publication is
part of this unattended research pass.

Earlier compact-per-group sharing was screened at h=27,28,29,30. Its best
bit-saving lower bound was about 4.51695e-9 at h=29, below the 2^-30 target.
The aligned construction escapes that numerical limit. Follow-up parameter
searches must continue to charge all output uses, additions and central losses.
