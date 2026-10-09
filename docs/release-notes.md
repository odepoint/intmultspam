# Release notes

The current release is [Community result: conditional exponent saving above
2^-15](releases/community-kappa-15.md), incorporating Rohan Arun's PR #39
and its credited dependency chain after conditional maintainer review.

## Fork note, 2026-10-07 (8e739d5): archived baseline release draft

This is preserved text from Douglas Colkitt's original repository, describing
that project's release plans. This repository is a separate, just-for-fun
experiment with AI-generated math. The original draft follows for provenance.

## Historical compact-control release draft

Repository: [CrocSwap/integer-mult-bounds](https://github.com/CrocSwap/integer-mult-bounds)

Suggested repository description:

> Conditional integer-multiplication bound with κ > 2⁻³⁴: compact-control movement, written proofs, exact certificates, and reproducible source patches.

Suggested release title: **Compact controls: conditional exponent saving κ > 2⁻³⁴**

## Release body

This research draft gives the conditional bound

    T(n) = O(n (log n)^(1-kappa)),
    kappa = 83/10^12 = 8.3e-11 > 2^-34,

in the fixed finite-alphabet, fixed-tape Turing-machine model of OpenAI's
*Integer multiplication below n log n* (result family #109).

The new witness increases the exponent saving by approximately **47.85 million
fold** over our preceding published `2^-59` result. The convenient dyadic
corollary `2^-34` is exactly `2^25` times `2^-59`. These are exponent
comparisons, not measured or predicted practical speedups.

The structural change is to move **compact dirty-control fields instead of
entire spaced windows**. This removes the `K^tau` spacing penalty from the
simultaneous layer and the restriction behind the previous quadratic
conversion of finite-network savings into the multiplication exponent.

The proof supplies wider-control streaming with all offset work charged,
front/back temporaries carved from existing address space, complete ranges
through padding and recursion, exact temporary restoration, and deterministic
exceptional repair charged locally at every node. The bit network remains at
`h=50`; the original complex network is independently instantiated at `h=25`.
A generalized stopping-depth guard and exact assembly checks complete the
witness.

Artifacts:

- [Proof note (PDF)](../artifacts/compact-control-note.pdf) and [TeX source](../notes/compact-control-note.tex).
- [Exact layer certificate](../certificates/compact-control-layer.json) and [address checks](../certificates/compact-control-audit.json).
- [Combined patch](../patches/compact-control-34.patch), applied directly to the unchanged pinned upstream source.
- [Review guide](research/compact-control-review.md), [current status](research/current-status.md), and [reproduction instructions](reproducibility.md).
- Preserved historical proofs, certificates, patches and bounded research audits.

The complete upstream theorem remains an assumption. The new general claims
rest on written proofs, supported by finite tests and exact arithmetic; they
have not received independent mathematical review or formal verification.
The repository does not contain a full multiplication-machine implementation.

The remaining scoped ceiling, below `8.369598075e-11`, concerns the fixed
`h=25` complex motif and retained Gaussian/leaf inequalities. It is not a
limit on other networks or on integer multiplication generally.

Author: **Douglas Colkitt**, with assistance from OpenAI Codex. The initial
compact-control proposal came from a separate research agent. Apache-2.0
licensed. No independent endorsement, priority or unrestricted optimality
claim is made. Independent mathematical review is welcome.

## Publication details

This file is prepared release copy, not a record of a GitHub release.
Attach `artifacts/compact-control-note.pdf` when publishing. For a GitHub
release body, replace the relative artifact links above with links under
`https://github.com/CrocSwap/integer-mult-bounds/blob/<release-commit>/`.
Set release version/date metadata only when a release is actually published.
The accompanying [announcement](announcement.md) is draft copy for that time.
