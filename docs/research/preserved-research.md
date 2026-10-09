# Preserved research before the community improvements

Reconciled October 8, 2026, against main `64ed4cb`. Author: Douglas Colkitt,
with AI-assisted exploration and verification. These are the previously local
experiments between the conditional 2^-31 and ternary 2^-30 checkpoints.
They are historical research, not a new improvement to the selected release.
See [current status](current-status.md) for the authoritative bound and the
[contributor ledger](../../CONTRIBUTORS.md) for subsequent community work.

## What remains useful

- **Compression and fusion exclusions:** the bit-compression, mixed-point,
  split-center, stage-pair, block-carry, and joint-return notes record exact
  tests and the assumptions behind their failures. Their exclusions apply to
  the specified models, not to later carrier-reuse or different topologies.
- **Topology screens:** the finite-circuit checker, routing witnesses,
  characteristic-zero rank obstruction, and exhaustive balanced-Fano
  diagnostic provide reusable rejection tools. A failed search is not treated
  as a general impossibility proof.
- **Core construction tools:** rank-product, shared-core, block-label,
  positive-side and subset/cube experiments separate a promising core from a
  complete framed circuit. Optimistic free-side scores are not achieved bounds.
- **Complex-network and guard work:** disjoint tensor contraction, dyadic
  central factors and stopped-depth guard estimates preserve the intermediate
  calculations that preceded later community constructions.

The historical `a_b/5` assembly ceiling and references to a binding complex
network belong to their stated older interfaces. They must not be applied to
the current community assembly without checking its hypotheses.

## Reproduction and scope

```sh
make verify-research
make verify-tests
```

`verify-research` regenerates all 28 added audit outputs using standard-library
Python. It is also part of `make verify` and has a separate Linux CI group on
Python 3.11, 3.13 and 3.14. `verify-tests` includes the newly recovered controls
alongside the current release tests. CI checks that regenerated tracked files
are unchanged. Run these targets sequentially in a shared worktree.

The optional `scripts/routing_smt.py` discovery function needs `z3-solver`;
replaying the stored routing witnesses does not. No solver installation is
needed by the verification targets. Finite checks verify the encoded models;
they do not formalize the complete multiplication theorem or independently
prove every written lemma.

Current main's shared modules and previously published ternary artifacts were
retained. In particular, `rank_product_core.py` continues to import `kron` from
`rational_tensor.py`, rather than restoring the older audit-module dependency.
Recovered certificates are regenerated against these reconciled sources.

## Validation at integration

All 28 producers and 419 tests passed locally, along with all 20 historical
patch checks and the current follow-up arithmetic audit. All 135 recorded
source hashes match the reconciled files. Historical certificate payloads are
unchanged apart from source hashes; existing production artifacts are unchanged.
See the [local receipt](preserved-research-validation.json). Hosted CI checks the
same commit separately; the receipt records local verification only.

## Record of reconciliation

The [path manifest](preserved-research-manifest.json) records the original hashes
and dispositions of all 169 preserved files. Of these, 146 were absent from main,
12 already matched main exactly, and 11 differed. Old status prose and reproduction
instructions are retained separately; obsolete copies of published artifacts
are not substituted for the reviewed versions.

- [Intermediate research chronology](pre-community-research-history.md)
- [Historical contracts and experiment status](pre-community-research-status.md)
- [Historical reproduction instructions](../pre-community-research-reproducibility.md)
- [Overnight experiment log](overnight-25-progress.md) — completed historical log;
  its embedded “active” status describes the earlier session, not a running goal.

## Experiment index

- [Compact vector families: exact rank rejections](affine-vector-screens.md)
- [Bounded bit-network compression: stop before a larger search](bit-compression-audit.md)
- [A deferred-scatter block schedule and its readout cost](block-carry-audit.md)
- [Higher-rank labels in the bit core compiler](block-core.md)
- [Limits that narrow the next core search](core-limits.md)
- [Binary-cube orthogonality cores](cube-core-family.md)
- [General finite-bit verifier and a routing obstruction](cyclic-topology-audit.md)
- [Complex-network headroom from tensor contractions](disjoint-tensor-compression.md)
- [A rank-h dyadic complex center](dyadic-central-factor.md)
- [Earlier sharing and point-split central gates](early-sharing-and-centers.md)
- [Fano coding survives edge storage, but these completions become routable](fano-completion-audit.md)
- [Permuting auxiliary roles: two bounded completion tests](fano-permutation-audit.md)
- [Stopped depth beyond the fifth-power network hypothesis](general-network-guard.md)
- [An in-place side circuit: scalar success, rank-budget rejection](inplace-side.md)
- [Earlier readout with both coordinate returns changed](joint-return-audit.md)
- [Mixed-point circuits: a frame criterion, but no new exponent](mixed-point-audit.md)
- [Overnight research log: target kappa >= 2^-25](overnight-25-progress.md)
- [Joint complex-side computation: scalar gain lost to a frame repair](parity-side.md)
- [Complete compressed-side compiler for positive-definite labels](positive-side-core.md)
- [A ceiling for common-subset prime-power side circuits](prime-subset-limits.md)
- [Quadratic-phase affine vectors: twelve exact core screens](quadratic-affine-vectors.md)
- [Recovering the positive mechanism before searching new topologies](rank-product-core.md)
- [Reusing auxiliary banks for general two-field cores](shared-core.md)
- [Signed sparse vectors: a constructive bit core and an unresolved side circuit](signed-sparse-core.md)
- [Single-intersection two-field screens](single-intersection.md)
- [Two-invocation fusion: a model and a boundary-size screen](stage-pair-audit.md)
- [Stronger screens and the exhaustive balanced-Fano diagnostic](stronger-rank-screens.md)
- [First overnight screen: power-of-two subset cores](subset-core-family.md)
- [Ternary five-subset construction: conditional 2^-30](ternary-side-candidate.md)
