# Research between the 2^-31 and ternary checkpoints

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

The subsequent [bounded bit-compression audit](bit-compression-audit.md)
tested 73 local configurations and 18 merged circuits. Its best change saves
48 side roles and leaves the headline unchanged. A separate counting argument
excludes `2^-30` from relabeling and equal-sum merging of the existing paired
template at every admissible even ground size; new local gates and mixed-point
circuits remain outside that obstruction.

The next [mixed-point round](mixed-point-audit.md) obtains 447,488 scalar roles
at h=50, still short of the next target even with optimistic frame accounting.
Its reusable source/target-span cut lemma certifies small mixed-point examples
whose raw source spans are degenerate. The full-size frame problem is not
claimed solved, and the headline remains unchanged.

The [early-sharing and split-center pass](early-sharing-and-centers.md)
rejects forward expansion followed by greedy pair factoring on role counts.
It obtains a small local rank improvement by splitting central gates into
point gates: the decreasing loss falls from 2500 to 2498. This escapes the
grouped-gate obstruction but has its own proved ceiling within the tested
hyperplane-frame family. No global integration or new kappa is supplied.

The [two-invocation fusion seed](stage-pair-audit.md) joins physical data wires
across two stages and checks 64 joint frame assignments, including matrices
mixing tensor factors. Six improve the h=6 score but fail the explicit
scaling audit in the retained positive-deficit range; 58 fail directly. General
rank-excess and shared-subspace overlap screens explain why boundary-only
changes and small shared-direction regions are inadequate for a large gain;
arbitrary fusion and changed scalar schedules remain open.

The [deferred block-carry pass](block-carry-audit.md) then constructs an exact
scalar schedule across a row/column block, with no new roles and arbitrary
scratch restoration. Its coordinate-subspace implementation fails a readout
rank budget, even with general rational cleanup matrices if the column
central frames are retained. The scalar mechanism is reusable, but no complete
improved frame assignment or multiplication witness is supplied.

The [final joint-return pass](joint-return-audit.md) moves the deferred readout
ahead of the column return and supplies exact repairs for the resulting column
auxiliary changes. It uses no new roles and 15 additional XORs per selected
cell. Even crediting both coordinate-complement returns, a whole-Y-wire rank
charge rejects every such block for h>=27. This closes the tested coordinate
carry branch; different high frames, carry representations and scalar topologies
remain outside the screen. The integrated bound stays at 2^-31.

The [general verifier and cyclic-topology round](cyclic-topology-audit.md)
then frees the endpoint frames and scalar role permutation. A graph admitting
edge-disjoint routes for that same permutation necessarily costs at least Wm
in rational rank, in every dimension. Eight swap-based cyclic seeds have
explicit routing certificates. A joint scalar/routing-state search closes on
two and three roles, excluding every finite XOR word there, and excludes
four-role words through seven gates. The next necessary target is a complete
scalar permutation circuit that escapes this routing screen; no improved
finite network or new kappa is supplied.

The [Fano completion round](fano-completion-audit.md) then starts from a
characteristic-two coding seed with an explicit forced-edge routing
obstruction. Separate storage for each original edge preserves the clean
obstruction, while two compact register realizations lose it. Fifteen tested
all-role completions admit independently checked routings and therefore cannot
yield a rank deficit. Three of them use a new shared-offset cancellation
identity across the full exchange, reducing the edge-based scalar count from
294 to 165 XORs without creating a rank saving. Other completions, particularly
ones permitting auxiliary role permutations, remain outside this test.

The [free-output completion round](fano-permutation-audit.md) then tests that
freedom. Exact support-graph rigidity excludes every nonidentity encoded
permutation in the three fixed compute/permute/inverse-compute templates.
144 specified Gaussian completions have complete scalar and routing
certificates; 126 move auxiliary inputs and 122 mix auxiliary and data roles.
All 72 cases preserving the three original Fano demands introduce direct
source/target gates that bypass the seed's obstruction. This rejects the
tested completion methods, not every completion or different coding topology.
The integrated bound remains 2^-31.

The [rank-product core pass](rank-product-core.md) then changes the emphasis
from failed completion variants to the mechanism of the successful network.
It generalizes the three-stage compiler to a binary central map of rank r
and a compatible rational fitting matrix of rank d, with positive deficit
exactly when n>6rd. Nonsymmetric matrices and mutually annihilating
rank-one idempotents are permitted. Six small expanded controls verify arbitrary-input
permutations, endpoints and edge ranks. An induced triple family gives a
compact positive core at n=9127, r=d=39, and a zero-deficit boundary at n=9126.
Its raw network is quantitatively much weaker than the retained construction;
it is a reference example, not a new exponent. The pass supplies exact
dimension screens and makes new two-field core pairs the main search target.

The [stronger-screen pass](stronger-rank-screens.md) adds undirected fractional
routing and characteristic-zero linear realizations as dimension-independent
rank obstructions. The clean Fano seed admits a three-demand fractional
routing; this alone does not exclude all completions with additional demands.
An exhaustive meet-in-the-middle search rejects the specified 10-role,
14-two-port balanced model with the original three terminal demands retained.
The integrated witness remains 2^-31.

The first [overnight subset-family screen](subset-core-family.md) supplies
a new generative positive bit core using seven-subsets and triple-incidence
central factors. It improves the core numerator and rational dimension,
but the tested side implementation overwhelms those gains. The screen
records a concrete side-role budget for 2^-25 and flags both the complex
phase-frame and larger-guard obligations; no new bound is claimed.

