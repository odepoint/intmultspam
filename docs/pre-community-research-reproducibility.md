# Reproducing the result

> **Historical snapshot of unpublished research before community integration.**
> Retained for provenance; publication status, priorities, and numerical “current”
> claims below are superseded by [current status](research/current-status.md).

The primary artifacts are the [complex-network note](../artifacts/complex-compression-note.pdf),
[combined patch](../patches/complex-compression-31.patch), and
[exact certificate](../certificates/complex-compression.json).
They are conditional on the retained algorithmic interfaces and written
extensions identified in the [review guide](research/complex-compression-review.md).

## Requirements

The verification path needs Python 3.11 or newer, Git, and Make, with no
third-party Python packages. Run commands from the repository root. All input
source files are bundled, so verification runs without network access.

The local preparation checks used Python 3.14.6 and Tectonic 0.16.9. The supplied
GitHub workflow targets Python 3.11, 3.13, and 3.14 on Ubuntu 24.04; a workflow
configuration is not a claim that those hosted runs have already passed.

## Arithmetic, identities, and patches

The overnight research additions also run through `make verify`:
`audit_single_intersection.py` replays the bounded rank screens and finite
orbit witnesses; `audit_shared_core.py` checks general auxiliary reuse;
`audit_general_guard.py` checks the generalized conditional guard;
`audit_disjoint_tensor.py` checks the new complex side DAG, both phase-frame
directions, and its scalar node-charge ledger. Only the last of these
supplies a stronger finite complex interface (`a_c > 3e-8`); none changes
the retained multiplication exponent. Discovery C++ programs under `build/`
are not required for certificate replay.

`audit_core_limits.py` checks the sharper dimension threshold and local
incidence rigidity matrices. `audit_affine_vectors.py` replays nine exact
binary-rank rejection witnesses on explicitly generated rational vector
families. These are scoped research screens, not multiplication witnesses.

`audit_block_core.py` checks the higher-rank bit-interface extension, expanded
rank-two controls and a positive direct-sum regression. Its target budgets
are explicitly hypothetical until better block geometry and side frames
are supplied.

`audit_inplace_side.py` replays explicit path-excess certificates for the
specified in-place Gauss--Jordan side family. It checks the target-capable
ground sizes and the analytic exclusions outside that range; its rejection
allows arbitrary internal rational frames but retains the stated boundaries.

`audit_quadratic_affine.py` checks twelve specified orthogonality central
matrices on real and Gaussian quadratic-phase vectors. The Gaussian cases
use rank-two rational labels. Their exact binary minors exclude positive
deficit in the current compiler; no new multiplication result is claimed.

```sh
make verify
```

This command performs these steps:

1. `scripts/certify.py` checks the pinned source hashes and parameter inequalities,
   then writes `certificates/parameters.json`.
2. `scripts/search_network.py` encloses logarithms with exact rational arithmetic,
   checks finite candidates and the infinite tail, and writes
   `certificates/network-search.json`.
3. `scripts/make_patch.py` regenerates seven parameter-only patches against the
   unchanged upstream files.
   `scripts/nonadjacent.py` and `scripts/make_nonadjacent_patch.py` additionally
   generate the follow-up routing certificate and three scheduling patches.
   `scripts/tune_routing.py` generates the tuned 2^-76 certificate and combined patch.
   `scripts/reuse_network.py` and `scripts/make_reuse_patch.py` generate the
   stage-sharing 2^-75 certificate and standalone combined patch.
   `scripts/incidence_network.py` and `scripts/make_incidence_patch.py` generate
   the incidence-circuit 2^-67 certificate and standalone combined patch, including
   exhaustive verification of the underlying ordered-pair rectangle partition.
   `scripts/dag_network.py` and `scripts/make_dag_patch.py` generate the
   shared-computation 2^-63 certificate and standalone combined patch. They
   check the exact symbolic linear map and both support-frame directions of
   the reversible circuit compiled by `scripts/exclusion_circuit.py`.
   `scripts/shared_point_network.py` and `scripts/make_shared_point_patch.py`
   generate the cross-group sharing certificate and independent patch for
   kappa=13*2^-66. They check exact supports and both frame directions in the
   global graph compiled by `scripts/shared_point_circuit.py`.
   `scripts/paired_network.py` and `scripts/make_paired_patch.py` generate the
   h=50 paired-network certificate and independent patch for kappa=2^-59. They
   also check the stopped guard constants and revised Gaussian inequalities;
   these proof models are selected explicitly in the parameter checker.
   `scripts/prepare_layers.py` records generalized guard and unequal-exponent
   recurrence estimates, the independent complex-family search, and clearly
   marked hypothetical sparse-primitive targets in `layer-preparation.json`.
   This preparation pass does not change the published 2^-59 witness.
   `scripts/audit_sparse_fusion.py` records finite phase identities, a bounded
   central-frame screen, and the cost targets for future sparse primitives.
   Its output is a research audit, not a stronger multiplication certificate.
   `scripts/audit_fused_block.py` checks a complete parity-butterfly sandwich
   and records the cut-rank obstruction for coordinate-child/pointwise-only
   recursion. Its exact identity does not supply a faster multiplication bound.
   `scripts/audit_short_guards.py` records logarithmic working guards and a
   reduction to a still-unproved fast gathering routine. Exact address tests
   check the reduction's maps, not a new tape-time or multiplication bound.
   `scripts/audit_gather_schedules.py` checks a reversible merge tree, scoped
   interval-schedule obstructions, and optimistic round-reuse accounting.
   It does not rule out coded gatherers or certify a new multiplication bound.
   `scripts/audit_coded_carries.py` checks an exact but linear carry code and
   small controls for a scoped flat affine-circuit obstruction. The bounded
   attempt supplies no sublinear recurrence or new kappa.
   `scripts/audit_cancellation.py` checks the first cancellation circuit's
   scalar map and dirty-scratch restoration, then records nonorthogonal-path
   bounds rejecting two topologies under the retained data-stage frames.
   `scripts/audit_joint_frames.py` reproduces a complete small bit invocation's
   edge ranks and checks rational controls for the fixed-boundary local
   optimality proof. It does not certify a stronger multiplication bound.
   `scripts/audit_compact_controls.py` checks the compact dirty-control address
   maps, inverses and exceptional repair. `scripts/compact_control_layer.py`
   records the new conditional `83/10^12 > 2^-34` witness, with reservations,
   the revised recurrence, independently sized complex motif, generalized
   guards and all assembly margins. Its general tape claims depend on the
   written [compact-control proof](../notes/compact-control-note.tex).
   `scripts/make_compact_control_patch.py` generates the independent combined
   patch, including the changed global exceptional-stream accounting.
   `scripts/complex_compression.py` records the follow-up weighted complex
   circuit, binary phase-frame audit and conditional `2^-31` witness.
   `scripts/make_complex_compression_patch.py` integrates that interface and
   all downstream constants into an independent complete upstream patch.
   The earlier compact-control certificate and source patch remain unchanged;
   see the [construction and integration boundary](research/complex-compression.md).
   `scripts/audit_bit_compression.py` records a bounded local/global circuit
   screen and a scoped all-even-ground-size obstruction for relabeling and
   merging the retained paired template. It supplies no new kappa; see the
   [compression audit](research/bit-compression-audit.md).
   `scripts/audit_mixed_point.py` checks full-size scalar circuits formed by
   block decomposition and factored transposition. Small exact controls
   certify a source/target-span frame cut, including dirty-scratch restoration
   and both compiled frame directions. The full-size counts miss the next
   target even before new frame costs; no new kappa is supplied. See the
   [mixed-point audit](research/mixed-point-audit.md).
   `scripts/audit_early_sharing.py` verifies a bounded forward-expansion
   search, rejected on exact role counts. `scripts/audit_split_centers.py`
   certifies a local four-unit rank saving with point-split central gates,
   including complete physical edges and arbitrary-scratch scalar controls.
   The [joint record](research/early-sharing-and-centers.md) proves the scoped
   frame-family ceiling and distinguishes the local saving from an integrated
   multiplication bound; the headline remains unchanged.
   `scripts/audit_stage_pair.py` constructs a complete two-invocation region,
   checks its exact rational baseline and arbitrary-scratch scalar map, and
   screens 64 correlated frame changes with rational-rank lower bounds and
   exact ranks. Six tiny-size gains fail a separate all-large-h scaling audit. See
   the [stage-pair audit](research/stage-pair-audit.md) for the general
   boundary-only obstruction and the scoped block-overlap screen.
   `scripts/audit_block_carry.py` constructs a deferred-scatter scalar block
   schedule with arbitrary-scratch restoration and zero extra roles. Its
   [rank audit](research/block-carry-audit.md) rejects the coordinate-carry
   realization with retained column central frames, including a relaxation
   to arbitrary rational cleanup matrices. No new kappa is supplied.
   `scripts/audit_joint_return.py` moves readout before the column return and
   checks all necessary dirty-scratch corrections. Its
   [two-return screen](research/joint-return-audit.md) credits both coordinate
   returns simultaneously but still rejects every such block for h>=27.
   It supplies no complete improved frame assignment or new kappa.
   `scripts/audit_cyclic_topology.py` exercises the general exact checker in
   `scripts/finite_bit_contract.py` and emits explicit edge-disjoint routing
   certificates for cyclic seeds. Its [topology audit](research/cyclic-topology-audit.md)
   rules out all lengths on two/three roles by joint-state closure, and all
   four-role words through seven XOR gates. These are topology exclusions,
   not stronger multiplication bounds.
   `scripts/audit_rank_product_core.py` extracts the two-field core of the
   successful bit construction. Six small complete circuits check its
   general compiler against the exact frame verifier; compact triple-core
   certificates recover a positive example and a zero-deficit boundary.
   Dimension screens reject oversized candidates before circuit search.
   The positive networks are specified generatively, not fully expanded;
   no new kappa is supplied. See the [core audit](research/rank-product-core.md).
   `scripts/audit_stronger_screens.py` checks exact undirected fractional
   flow and characteristic-zero telescoping witnesses, and exhausts all
   assignments of six invertible binary local gates on the specified
   14-vertex balanced-Fano model. No admissible complete permutation exists
   in that model. See the [stronger screens](research/stronger-rank-screens.md).
   `scripts/audit_subset_cores.py` screens power-of-two subset cores and
   charges their side roles against the overnight target. It also records
   hypothetical assembly targets and a complex companion with unresolved
   phase-frame and guard obligations. Its [family screen](research/subset-core-family.md)
   distinguishes generative raw networks from unproved compressed counts.
   `scripts/audit_cube_cores.py` checks the binary-cube factorization and
   compiler ledger, and supplies exact rank lower bounds rejecting three
   specified quadratic-code subfamilies. The [cube screen](research/cube-core-family.md)
   records both hypothetical side budgets and characteristic-zero traps
   for tempting fast implementations. No improved kappa is supplied.
   `scripts/audit_fano_permutation.py` checks three rigid binary compute maps
   and 144 specified completions allowing arbitrary output-role permutations.
   Every full permutation has an independently replayed routing witness;
   72 terminal-preserving cases also have direct bypass certificates. See the
   [free-output completion audit](research/fano-permutation-audit.md).
   It runs without an SMT solver and supplies no new kappa.
   `scripts/audit_fano_completion.py` checks a nonroutable Fano coding seed,
   compares clean register realizations, and replays explicit routes for 15
   complete arbitrary-input implementations. Its
   [completion audit](research/fano-completion-audit.md) records shared-offset
   cancellation and the remaining completion obstruction. Replay uses only
   the standard library; the optional SMT discovery helper is not required.
   `scripts/research_networks.py` and `scripts/search_network_variants.py`
   record scoped family bounds and clearly marked exploratory scores.
4. The standard-library unittest suite checks certificate boundaries, selected
   finite identities, network counts, patch dependencies, and search bounds.
5. Git checks that each alternative patch applies to the pinned source.

The generators overwrite their output certificates and patches. To confirm
that the checked-in outputs reproduce exactly, run on a clean checkout:

```sh
git diff --exit-code -- certificates patches
```

The compact-control note builds with `make compact-note`. Its statement remains
conditional on the identified upstream interfaces and supplied written
extensions. See the
[current research status](research/current-status.md) before treating older
research pages or preparation certificates as current conclusions.

The theorem certificates and all-h bound comparisons use `fractions.Fraction`;
no floating-point result controls their acceptance. The separate exploratory
higher-subset screen uses floating point to select candidates, then encloses
their scores exactly; it certifies neither a new construction nor optimality.
Sampled finite identity tests use fixed random seeds.
Passing these checks does not prove the full multiplication-machine theorem.

## Apply one patch for review

The following creates a fresh local review directory and refuses to reuse an
existing one. It leaves the bundled source untouched:

```sh
mkdir -p build
mkdir build/review
cp -R upstream/build build/review/build
git apply --directory=build/review patches/ternary-30.patch
```

Read `build/review/build/main.tex` and its included sections. The other patches
are alternatives based on the same original manuscript, not successive commits.

## Build the note

With Tectonic installed:

```sh
make complex-note
```

The result is `artifacts/complex-compression-note.pdf`. Build the preceding
compact-control note with `make compact-note`. Build the earlier
parameter-only note with `make note`, producing `artifacts/parameter-note.pdf`.
Build the separate routing audit
with `make audit-note`, producing `artifacts/nonadjacent-axis-note.pdf`.
Build the tuning note with `make tuned-note`, producing
`artifacts/routing-tuned-note.pdf`. Build the preserved stage-sharing note with
`make reuse-note`, producing `artifacts/stage-reuse-note.pdf`.
Build the rectangle-circuit note with `make incidence-note`, producing
`artifacts/incidence-note.pdf`.
Build the shared-computation note with `make dag-note`, producing
`artifacts/dag-note.pdf`.
Build the cross-group and paired notes with `make shared-point-note` and
`make paired-note`, producing `artifacts/shared-point-note.pdf` and
`artifacts/paired-note.pdf`, respectively.
Build the local complex-network follow-up with `make complex-note`, producing
`artifacts/complex-compression-note.pdf`.
The first run may download fonts
and TeX packages; the numerical verification does not use them. PDF builds may
differ in metadata or typesetting across TeX environments. The exact-byte
reproducibility check covers JSON certificates and patches, not the PDF.

Full patched-manuscript previews were also compiled during preparation. With
Tectonic, the original pdfTeX-only metadata commands `pdfinfoomitdate`,
`pdftrailerid`, and `pdfsuppressptexinfo` must be commented out in a disposable
copy. Those preview-only edits are not included in the mathematical patches.

The additional `audit_complex_centers.py` verifies the h-center dyadic
factor with the full tensor side circuit and scalar guard charge, certifying
separate complex saving above 3.6e-8. It leaves the integrated kappa unchanged.

`audit_signed_sparse.py` verifies the signed-vector central factors, a complete
small compiler control with a redundant factor, and generative raw ledgers.
It records a hypothetical compression budget separately from the actual
uncompetitive construction. Six targeted tests also check the rational
contract, characteristic-two slice bound, degree formula and input limits.

`audit_positive_side.py` checks the complete compressed-side bit compiler
with positive-definite rational labels. It includes all-role tensor controls,
asymmetric cores, noninvolutive matching and shared output sums. Six small
signed-vector instances receive exact coefficient and dirty-input checks;
the frequent-pair candidates also receive both physical frame audits.

`audit_parity_side.py` checks the signed joint complex-side kernel, a
five-point obstruction to its nested binary frames, and an explicit
noncompetitive repair. It verifies the repaired signed coefficients and
355,600 nested frame incidences at h=26; no stronger bound is claimed.

## Source provenance

The pinned upstream revision is
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
[The manifest](../upstream/manifest.json) records each source URL and SHA-256
hash. `make fetch` downloads that exact revision and refuses to overwrite
changed source files. Fetching is optional and requires network access.

## Automation

[The verification workflow](../.github/workflows/verify.yml) runs `make verify`
and rejects changes to regenerated certificates or patches. It uses immutable
commit pins for the official [checkout](https://github.com/actions/checkout)
and [setup-python](https://github.com/actions/setup-python) actions, with
read-only repository permissions. The PDF is supplied for readers and can be
rebuilt locally using the command above.

Build the latest note with `make ternary-note`. The earlier notes and
patches remain available as independent witnesses.

## Ternary checkpoint

Run `python3 scripts/audit_ternary_side.py` to regenerate the complete h=29
aligned DAG, its source hashes and exact assembly certificate. This finite
construction allocates about 21 million addition nodes and a large dictionary
of shared sums; allow several minutes and multiple gigabytes of memory.
Small h=8,9 controls independently expand every coefficient map and verify
arbitrary-input scalar restoration and both rational frame directions.

Then run `python3 scripts/make_ternary_patch.py` and
`python3 -m unittest tests.test_prime_core tests.test_ternary_side tests.test_ternary_patch -v`.
The generator refuses stale construction source hashes. The new independent
patch is `patches/ternary-30.patch`; the source note builds with
`make ternary-note` into `artifacts/ternary-note.pdf`. Earlier patches are
alternatives against the same pinned original and must not be stacked.
