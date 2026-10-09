# Current contracts and research status

> **Historical snapshot of unpublished research before community integration.**
> Retained for provenance; publication status, priorities, and numerical “current”
> claims below are superseded by [current status](current-status.md).

Updated October 8, 2026. Author: Douglas Colkitt. All results remain conditional
on the pinned upstream algorithmic interfaces and the identified written
extensions. Nothing here asserts formal or independent verification.

## Current and earlier results

| State | Exponent saving kappa | Artifacts |
| --- | --- | --- |
| Earlier published baseline | `2^-59` | [paired note](../../artifacts/paired-note.pdf), [patch](../../patches/h50-paired-59.patch) |
| Published compact-control checkpoint | `83/10^12 > 2^-34` | [note](../../artifacts/compact-control-note.pdf), [certificate](../../certificates/compact-control-layer.json), [patch](../../patches/compact-control-34.patch) |
| Earlier integrated follow-up, pending publication | `2^-31` | [note](../../artifacts/complex-compression-note.pdf), [certificate](../../certificates/complex-compression.json), [patch](../../patches/complex-compression-31.patch) |
| Latest independent integration, pending publication | `2^-30` | [ternary note](../../artifacts/ternary-note.pdf), [certificate](../../certificates/ternary-side.json), [patch](../../patches/ternary-30.patch) |

The newest witness doubles kappa relative to 2^-31. These compare exponent
savings, not practical runtime. The older certificates, patches and pinned
upstream remain unchanged.

## Current ternary witness

The [ternary five-subset construction](ternary-side-candidate.md) changes the
bit network's scalar alphabet to F3, while retaining rational address frames.
An explicit finite-alphabet transfer extension proves that intermediate
ternary symbols do not alter the recursive branching coefficient. Common-pair
side sums have positive-definite rational source spans; aligned tensor sums
share equal expressions across groups without increasing frame loss.

At h=29, the complete shared network has

    n=118755, r=406, side roles per invocation=20780789,
    m_b=24389, W_b=589493540769997500,
    s_b=14377157287342062574725,
    a_b=467/10^11, a_c=5/10^9.

The complex network and its precision node charge remain exactly those of the
2^-31 integration. The new parameters are

    epsilon=1999/10000, c=1, beta=1/100, zeta=1/1000,
    delta=1/10^6, C1=4961/1000,
    lambda=1-4669/10^12, lambda'=1-4668/10^12,
    kappa=2^-30.

All assembly inequalities are strict, with minimum margin
`2332833/2500000000000000 > 2^-30`. The retained Gaussian inequality gives
the scoped ceiling `kappa<a_b/5=9.34e-10` for this certified bit exponent;
that ceiling is slightly above 2^-30 and does not constrain other networks.

The full 358-test suite and new construction audit pass. Its small controls expand every
formal support and coefficient, arbitrary-input restoration, and physical
rational frame edge in both invocation directions. The independent patch
passes three integration tests, applies to the pinned original, and builds
as a complete manuscript. The standalone note also builds. These remain
conditional results, not independent verification of the upstream theorem.

The subsequent [prime-power family screen](prime-subset-limits.md) proves
that keeping all common-subset partial outputs cannot reach 2^-26, even
under optimistic sharing, across every prime power and ground size. Its
exact finite envelope and dimension-tail bound also exclude 2^-25 from that
specific representation. Other side circuits and topologies are not covered.

The eight-hour research target remains kappa>=2^-25. No new artifacts have
been committed or published during that goal. The sections below preserve
the preceding 2^-31 integration and the research route; their numerical
parameters and ceilings are historical unless explicitly identified as current.

## What changed and what is retained

The overnight research branch now supplies additional, separately checked
[complex-network headroom](disjoint-tensor-compression.md): a tensor sum DAG
supports `a_c > 3e-8` at ground size 26. A further
[dyadic central factor](dyadic-central-factor.md) reduces the centers from
27 to 26 and certifies `a_c > 3.6e-8`. It has a written phase-frame proof,
exact scalar and physical-transition checks, and a verified node charge.
This is not yet substituted into the integrated patch, and does not by
itself improve kappa because the bit network remains limiting. The table
and parameters below describe the retained integrated witness.

Other new preparation includes [general two-field stage reuse](shared-core.md),
[a bounded single-intersection rank screen](single-intersection.md), and
[a guard lemma for larger finite networks](general-network-guard.md).
Hypothetical family budgets and target parameters are not new bounds.

The next screening pass adds [necessary core limits](core-limits.md), including
the side-role rank floor and an incidence-row-space rigidity result, and
[nine exact vector-family rejections](affine-vector-screens.md). The radial
subset result is scoped to the rank-one compiler and retained assembly;
the vector rejections concern only their specified full-support binary maps.

The [higher-rank bit compiler](block-core.md) now accepts uniform block
idempotents with a verified revised rank ledger. Its controls include a
positive direct-sum construction, which does not improve the saving.
A better block representation and its compressed side frames remain missing.

The [in-place side audit](inplace-side.md) checks an exactly n-role scalar
implementation and rejects its specified Gauss--Jordan topology using
disjoint directed paths. The rejection reaches every target-capable ground
size for that family and permits arbitrary internal rational frames. Other
side topologies, auxiliary counts and invocation boundaries remain open.

The [quadratic-affine vector screen](quadratic-affine-vectors.md) tests real
and Gaussian phase families, including rank-two rational labels. Twelve
specified full-orthogonality central matrices fail the necessary binary-rank
ratio. This does not exclude other supported matrices on those graphs.

The [signed-sparse core](signed-sparse-core.md) supplies another generative
positive bit construction using ordinary positive-definite rational labels.
Its refined binary factor follows from a formal-series identity and an
integer inclusion-matrix rank bound. At q=16,h=31 a hypothetical
loss-preserving side circuit has a sufficient budget of about 5.5555 roles
per label for a_b>1.6e-7. The actual raw side circuit is far too large;
this is a construction target, not a stronger multiplication bound.

The [positive-definite side compiler](positive-side-core.md) now verifies
compressed cancellation-free DAGs inside the complete three-stage bit
network. It charges every role, restoration operation and frame transition,
including first/third-stage sharing. Small signed-vector sharing experiments
are certified but do not supply a competitive large side construction.

The [joint complex parity circuit](parity-side.md) reduces the scalar side
count to 82,720 at h=26 but fails a concrete five-point binary frame test.
A deterministic repair has valid source-span phase transitions and costs
308,336 roles, exceeding the retained 89,622. This closes that specified
construction/repair round, not all parity circuits or all frame choices.

The [complex-network construction](complex-compression.md) uses weighted
rectangles for disjoint triples, shared sums for intersection-two triples,
and binary phase frames valid in both signed directions. Transparent computation
restores arbitrary auxiliary inputs. A matching shares the complete first/third
auxiliary banks. At `h_c=26`, it has

    m_c = 17576, W_c = 7082222160000,
    s_c = 124477130005280000,
    a_c = 1-sigma = 5/10^9.

The bit network remains `h_b=50`, `m_b=125000`, with
`a_b=1-tau=296/10^11`. Thus the complex interface now has the larger saving.
The bit interface is the bottleneck.

The retained compact-control construction moves compact dirty fields instead
of spaced windows, at cost `O(V*((f log p)^tau+1))`. It reserves two front
fields and one back field from existing address coordinates, preserves complete
ranges in every recursive child, restores arbitrary values, and charges
exceptional-address repair at every node. All three movement/layout/guard
proof sources are embedded verbatim in the new patch.

## Previous 2^-31 parameters and bottleneck

The certificate uses

    epsilon = 199/1000, c = 1,
    beta = 1/100, zeta = 1/1000, delta = 1/10000,
    C1 = 4961/1000,
    lambda = 1-293/10^11,
    lambda' = 1-29/10^10,
    kappa = 2^-31.

The internal, leaf and reservation exponents are

    chi = tau+(1-beta)*max(sigma-tau,0) = tau,
    leaf = sigma+beta*(1-sigma),
    reserve = max(1-c,0) = 0.

All required comparisons are strict. The seven assembly margins have minimum

    G = g3 = 5771/10^13 = 5.771e-10 > 2^-31.

The explicit new scalar-operation count fits the generalized guard's node
charge `E=64*(W_c+m_c+1)^3`. The guard still has
`C1=5-4*beta+zeta`, and `epsilon*C1=987239/1000000<1`.
Reserved-axis processing costs `O(V log p)` for `c=1`.

The old quadratic restriction from `K^tau` is absent. With the **retained
certified bit exponent and Gaussian assembly inequality**, the current scoped
ceiling is `kappa<a_b/5=5.92e-10<2^-30`. This is not an all-network limitation.
The new complex saving provides numerical headroom for `2^-30` if a stronger
bit construction is supplied; that is not another established witness.

## Previous integration verification boundary

The [integration review guide](complex-compression-review.md) identifies each
new obligation and its tests. General arguments are supplied in:

- [compressed complex construction](../../notes/complex-compression.tex);
- [movement and deterministic repair](../../notes/compact-control-movement.tex);
- [reservations, row splitting and recurrence](../../notes/compact-control-layout.tex);
- [generalized guard](../../notes/compact-control-guard.tex).

The new certificate records all four source hashes. The combined patch applies
directly to the pinned original and includes the full retained refinements.
It updates every complex constant, the exponent ordering, scalar guard charge,
final parameters and derived powers. It preserves the legacy wide-slot lemma
for the appendix and retains the corrected local exceptional-stream sum.

Finite tests check exact signed scalar maps with independent dirty variables,
rectangle partitions, binary residual bases, phase identities, matching,
parameter inequalities and source integration. They do not simulate the entire
multiplication machine or replace independent proof review. The retained
compact-control arguments have the same review dependencies as before.

Completion checks passed: 176 tests, 18 patch-application checks, exact
certificate/patch regeneration, and both note and manuscript builds.

Reproduce with `make verify` and `make complex-note`. See the
[reproduction instructions](../reproducibility.md) for applying the patch and
building a manuscript preview without changing the pinned source.

## Next research priority

The complex construction is integrated. A subsequent
[bounded bit-compression round](bit-compression-audit.md) saves only 48 side
roles out of 509,194 and does not improve the headline. It also excludes
`2^-30` from independently relabeling and merging the existing paired modules
at any admissible even ground size, under the retained compiler and losses.
This is a scoped obstruction, not a lower bound on new local circuits.
The round passed all 183 repository tests and 18 patch-application checks;
its audit certificate regenerates byte-for-byte. Existing witnesses are unchanged.

A subsequent [mixed-point round](mixed-point-audit.md) changes the graph via
block decomposition and factored transposition. Four factoring rounds reduce
full-size scalar roles to 447,488 (12.1%), still short of the necessary 317,035
at h=50 even before any additional frame losses. No full-size frame certificate
or new kappa is claimed.

That round supplies a reusable **source/target-span cut criterion**. It repairs
degenerate source spans in small mixed-point circuits by switching a
forward-closed collection of nodes to target-span orthogonal complements.
Six exact small controls pass the complete compiled side-frame conditions in
both directions and arbitrary-scratch restoration. These small ground sizes
do not give a positive global deficit. A separate source/target-intersection
obstruction screens impossible nondegenerate subspace enclosures.
The combined repository passes 190 tests and 18 patch-application checks.
Both compression audit certificates regenerate byte-for-byte; all retained
proof artifacts and pinned upstream sources remain unchanged.

The next [bounded early-sharing and central-gate pass](early-sharing-and-centers.md)
finds that forward expansion/refactoring increases full-size roles to 510,700.
Point-split central gates do give an exact local rank saving of four, reducing
the per-invocation decreasing loss from 2500 to 2498. A proof bounds this
particular hyperplane-frame family to that small saving. Even if integrated
globally, the deficit gain would be only about 0.26%; no global integration
or stronger multiplication witness is claimed. The result changes gate
grouping and therefore lies outside the earlier grouped-gate obstruction.
Completion checks pass: 197 tests, 18 patch-application checks, and byte-for-byte
regeneration of both new audit certificates. Retained proof artifacts are unchanged.

The [two-invocation fusion seed](stage-pair-audit.md) then builds an exact
boundary-crossing physical graph and tests 64 correlated frame assignments,
including nonproduct rank-h changes. Six improve the tiny h=6 example but
fail in the retained positive-deficit range by explicit scaling formulas;
58 are rejected directly. A general rank-excess argument excludes
boundary-only changes that leave all central return endpoints fixed. The two
active return spaces overlap in only one dimension; a shared-subspace route
therefore needs a wider block to target a substantial fraction of central loss.
The pass does not prove optimality over arbitrary matrices or different scalar
schedules, and supplies no new network or kappa.
Completion checks pass: 205 tests, 18 retained patch-application checks, and
byte-for-byte regeneration of the new stage-pair certificate. The six tiny-size
gains are retained explicitly in its records and scaling audit.

The [deferred block-carry pass](block-carry-audit.md) supplies such a scalar
mechanism: defer selected row scatters through column invocations, compensate
the changed X entries, and restore the row centers with two gathers. Its exact
map restores arbitrary scratch with no new roles and 6 additional XORs per
selected cell. However, the coordinate-carry realization fails a rank budget
throughout the retained positive-deficit range. The rejection still holds
with arbitrary rational copy/cleanup/readout matrices when column central
frames remain fixed and readout retains the carried image. Keeping five
dimensions at h=50 defers 5,410 columns; the resulting net rank increase is
at least 4,460 per row even with other new costs credited as zero.

Completion checks pass: 212 repository tests, 18 retained patch-application
checks, and byte-for-byte regeneration of the block-carry certificate. Its
source hashes match; the five preceding research certificates and all retained
proof artifacts remain unchanged.

The [final joint-return test](joint-return-audit.md) moves readout before the
column return and exactly repairs the induced column auxiliary changes. It
restores arbitrary scratch using no new roles and 15 additional XORs per
selected cell. Both coordinate-complement returns may change simultaneously.
A whole-Y-wire argument still charges at least one rank unit per selected
cell; the combined return credits cannot pay for that charge for any coordinate
block at h>=27. For h=50 and one selected ground point in each factor, the
net rank increase is at least 917,280, even ignoring all other added costs.

Completion checks pass: 219 repository tests, 18 patch-application checks,
and byte-for-byte regeneration of the joint-return certificate. Its source
hashes match; the six preceding research certificates and retained proof
artifacts remain unchanged.

Close this coordinate-carry fusion branch. The screen retains high central
frames, specified outside-gate frames, carried images at readout, and outer
cuts; it is not an arbitrary-frame or all-topology impossibility result.
No complete improved frame certificate or new kappa is supplied. The next
priority becomes a small complete finite circuit and rational-frame certificate
with a different topology, scored against the full transfer contract.

The first [general-verifier/cyclic round](cyclic-topology-audit.md) supplies
an exact checker with free rational terminal/gate matrices and an arbitrary
all-role scalar permutation. A dimension-independent routing screen rejects
any gate graph with edge-disjoint paths for that same permutation: rank
subadditivity forces s>=Wm. All eight swap-based cyclic seeds have explicit
routing certificates. The joint scalar/routing-state search closes after 235
nonsaturated states on three roles (and also closes on two), excluding all
finite word lengths there. On four roles, 529,066 joint states exclude every
word through seven primitive XOR gates; that frontier does not close.

Completion checks pass: 228 repository tests, 18 patch-application checks,
byte-for-byte regeneration of the cyclic-topology certificate, and command-line
strict-versus-score controls. The source hashes match; all seven preceding
research certificates and retained proof artifacts remain unchanged.

The [Fano completion round](fano-completion-audit.md) next tests a concrete
characteristic-two coding seed. Its clean capacity graph has a simple
forced-edge nonroutability certificate. An edge-explicit register realization
preserves that obstruction, while compact node-register realizations do not.
Fifteen complete arbitrary-input exchange circuits all have explicit routing
certificates, including separate/shared scratch and two local correction
orders. Thus these completions cannot provide a rational rank deficit in any
dimension. Their route fixtures replay without an SMT solver.

A useful scalar simplification emerged: the same dirty-scratch offset in
each of three shears cancels over the complete exchange. This reduces the
edge-based realization from 294 to 165 XORs, but that shorter completion is
also routable. With general offsets d1,d2,d3 the final errors are d1+d2 and
d2+d3, so equal offsets are necessary and sufficient within this model.

Completion checks pass: 237 repository tests, 18 patch-application checks,
byte-for-byte regeneration of the Fano completion certificate, and replay
without site packages or an SMT solver. The source hashes match; all eight
preceding research certificates and retained proof artifacts remain unchanged.

The next [free-output completion round](fano-permutation-audit.md) allows
auxiliaries to move. Exact bipartite support-graph rigidity excludes every
nonidentity encoded permutation in three fixed compute/permute/inverse-compute
templates. All 144 specified Gaussian completions have independently checked
full routings; 126 move auxiliaries and 122 mix auxiliary and data roles.
All 72 terminal-preserving cases move auxiliaries, but their first three
elimination pivots force direct source/target gates. Separate partial-path
certificates show that those gates bypass the original Fano obstruction.
This is a scoped rejection of the tested completion methods, not all pivot
orders, all Fano completions, or the general transfer contract.

Completion checks pass: 244 repository tests, 18 patch-application checks,
byte-for-byte regeneration, source-hash checks, and solver-free replay.
All nine preceding research certificate snapshots and retained proof artifacts
remain unchanged. No stronger multiplication witness is supplied.

The [rank-product core pass](rank-product-core.md) now works backward from
the successful network. A binary central matrix C of rank r, with diagonal
one, is paired with a rational fitting matrix F of rank d. An off-diagonal
one of C requires both corresponding directed entries of F to vanish.
Nonsymmetric F and mutually annihilating rank-one idempotents are allowed.
The unshared edge-explicit compiler has W=2n^3+3n^2(E+r), m=d^3, and
deficit n^3-6n^2rd. Thus n>6rd is exactly its positivity threshold. Nonsymmetric
binary central matrices are allowed. Six small expanded controls check all
scalar inputs, endpoints and physical edge ranks against this formula.

A compact induced-triple core at n=9127, r=d=39 has positive deficit; deleting
one more label gives zero. Its enormous raw side circuit makes its saving
much weaker than the retained network. The positive network is specified by
the proved compiler and checked core data, not a full expansion of its
trillions of roles. This establishes a smaller positive reference core,
not a new kappa. The retained core has n/(rd)=7.84 and keeps 23/98 of its
gross saving after central returns.

The primary next search is for a better two-field core that can use this
known completion and frame construction. Score rational dimension and side
cost as well as n/(rd). An optimistic dimension screen already excludes
d>=190 from supporting 2^-30, and d>=10 from supporting 2^-16, within this
three-factor line-label template and retained Gaussian accounting. These
are not bounds on the general finite-network contract. Point-additive triple
relabelings remain subject to the earlier obstruction and are not reopened.

The [stronger-screen audit](stronger-rank-screens.md) now exhausts the
specified balanced-Fano topology: no all-role permutation retains the three
original demands among all 6^14 assignments of invertible two-port gates.
It checks 279,936 assignments in each half of a meet-in-the-middle search.
This closes that model, not all Fano completions. The clean three-demand
Fano graph has an exact undirected fractional routing; additional auxiliary
demands mean this fact alone cannot reject arbitrary completions.

For topologies outside the core compiler, both unit undirected fractional
routing and any characteristic-zero linear realization of the same terminal
permutation exclude a rational rank deficit. The latter includes signed or
scaled permutations. Failed searches for those witnesses do not prove a
useful separation. Generalizing the transfer interface remains open.
No stronger multiplication witness is supplied.
More complex-network tuning alone cannot cross the
present bit/Gaussian ceiling. Independent review remains valuable for both
the new phase-frame transfer and retained compact-control tape proof.

The previous [joint-frame obstruction](joint-frame-audit.md) remains scoped to
its fixed-boundary, grouped-gate model. Older research pages retain their
chronology; use this page when interpreting superseded targets and barriers.

Checkpoint verification: 263 repository tests and 18 patch-application checks
pass. All 38 preceding certificate hashes and retained tracked proof artifacts
are unchanged. The core and stronger-screen certificates replay without site
packages. The active research goal targets kappa>=2^-25; no such witness has
been established.

The first [overnight subset-family screen](subset-core-family.md) replaces
triples by (2q-1)-subsets, with central factors indexed by (q-1)-subsets for
q a power of two. Seven-subsets first give positive compiler deficit at h=23,
and have sufficient free-side headroom for the target. Their independent
intersection/rectangle implementation is far too expensive: at h=28 it uses
about 20,631 side roles per label against a sufficient budget below 4.412.
This count screen rejects that implementation, not the family or shared
cancellation circuits. A candidate opposite-field complex polynomial also
requires a new phase-frame proof and, for the main sizes, a guard beyond the
retained fifth-power size hypothesis. No improved kappa is established.

The second [overnight cube-family screen](cube-core-family.md) supplies a
constructive binary factor paired with ordinary rational sign vectors in
32 dimensions. Its raw compiler has positive deficit, but its raw side cost
is uncompetitive. The target requires a loss-preserving side circuit below
about 1.539 roles per label. Direct low-rank-update implementations can lose
the characteristic separation, so role counts alone are insufficient. Exact
rank witnesses reject the tested full-support quadratic-code subfamilies at
t=3,4,5. A new complex interface is still independently required.
