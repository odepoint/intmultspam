# Ternary 2^-30 checkpoint: release summary

The package supplies a conditional witness kappa=2^-30 using an F3 five-subset
circuit, rational frames and a fixed-alphabet interchange extension. It
retains the compact-control and compressed complex proofs. The original
manuscript remains pinned and unchanged; the full upstream theorem is assumed.

This doubles the previous local 2^-31 exponent saving and is approximately
11.22 times the last published exact witness 83/10^12. The ratio to the
original 2^-182 saving is 2^152. These are exponent comparisons, not practical
speedups. The result is not presented as the strongest known algorithm.

The note and NOTICE acknowledge Zhihao Chen's earlier PR #7, which contains
the same motif with a different producer and a stronger claimed result, and
eumemic's related complex work in PR #3. Those contributions and newer
claims are pending review; their code is not silently incorporated here.

Release contents: updated README/citation/status, the proof note and PDF,
complete construction certificate, independent manuscript patch, focused
controls, verification targets and a contribution-review queue. Exploratory
nightly searches are excluded. Earlier witnesses remain unchanged.

See [the review guide](ternary-review.md) for evidence and limitations and
[the contribution queue](contribution-review.md) for the next review round.

## Completed release checks

- `make verify` passed: 188 tests and all 19 independent patch checks.
- The full h=29 construction audit passed. Its mathematical certificate
  agrees exactly with the previously checked overnight witness; the source
  manifest additionally covers the extracted exact tensor helper.
- Every earlier tracked certificate, patch, note, PDF and upstream file is
  unchanged. The new patch regenerates byte-for-byte.
- The standalone note and full patched manuscript build. The manuscript has
  only the retained introductory line-overflow warning; references resolve.
- Public documentation links and whitespace checks pass.

Verification took about 9.6 minutes and peaked near 1.6 GB resident memory
on the preparation machine. CI allows 30 minutes on each supported Python
version. No new multiplication-machine implementation or formal proof is
claimed. This document records the tested checkpoint; publication and subsequent integration
are tracked by Git commits and branches.

The [community record](../../CONTRIBUTORS.md) credits parallel and superseded
submissions, including the complex and ternary work submitted before this release.
