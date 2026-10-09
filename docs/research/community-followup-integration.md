# Integrating PRs #49, #45 and #26

This integration builds on the published PR #39 release at `0605a24`.
All three reviewed contributor heads are retained as ancestors through merge
commits, preserving their original authorship and history:

| PR | Contributor | Reviewed head | Integration merge |
|---|---|---|---|
| [49](https://github.com/CrocSwap/integer-mult-bounds/pull/49) | Rohan Arun | `f95d2910e027495983b53cae1693cf535abf2569` | `e1bda06` |
| [45](https://github.com/CrocSwap/integer-mult-bounds/pull/45) | Alejandro Zarzuelo Urdiales | `7f0764750f6c78b68a8f2c579c936ed377216ec4` | `1ddeeb8` |
| [26](https://github.com/CrocSwap/integer-mult-bounds/pull/26) | Ryan S / princezuda | `f764fb98208506354730f6f108a8c87fb679432e` | `9714ece` |

The selected conditional witness is **κ=4123863984/10^14**, 6.10% above the
previous release. The Gaussian and historical formal packages make no further
κ claim and do not formalize the whole multiplication theorem.

## Resolution and provenance

- Combine the Makefile targets for current and historical witnesses; retain
  all 20 historical patch checks and the older independent PR #39 audit.
- Preserve current main's portable `binary_io.hpp` includes. Update only that
  dependency hash in `research/copied-fixed/SOURCE.json` and regenerate its
  certificate's provenance fields. No numerical certificate value changes.
- Preserve main's reproducible numeric ordering in the historical
  `endpoint-gauge-network.json` histogram, resolving the pinned PR #49
  clean-diff issue. Parsed values are identical.
- The PR #49 certificate remains byte-identical to the reviewed input, and
  its independent arithmetic receipt is unchanged.
- Preserve the complete RaD source archive, all older results, original
  notices and AI-assistance disclosures.
- Update README, current status, citation metadata and CONTRIBUTORS.md
  together. Credit Chafik Boukhalfa's PRs #43/#46/#48 and RaD's #41 as well as
  Rohan's order/matching work and both formal contributors.

## Reproduction and continuous verification

The [pinned-head review](community-followup-review.md) records the mathematical
scope, independent arithmetic and the earlier successful standalone builds.
Its [validation receipt](community-followup-validation.json) is historical;
the integrated CI checks the combined tree separately.

```sh
make verify
git diff --exit-code -- certificates patches research/copied-fixed research/climbed-48
make formal-verify
```

For a fresh Lean installation, install elan and fetch Mathlib once with
`cd formal/lean && lake exe cache get`. Each formal project pins its own
toolchain (Lean 4.21.0/Mathlib v4.21.0 and Lean 4.31.0/Std respectively).

The GitHub workflow runs the complete arithmetic/circuit suite on Ubuntu 24.04
with Python 3.11, 3.13 and 3.14, plus separate historical and Gaussian formal
jobs. Each Python version runs five isolated groups in parallel, with a
20-minute allowance per group. All 94 leaf commands and their multiplicities
are preserved; local `make verify` remains sequential. See the
[CI timing and coverage note](../ci-verification.md). Formal jobs check the
proofs, all listed theorem axiom dependencies, source bindings and finite
reference computations. The historical package also rechecks the full h=50
paired circuit.

The independent follow-up check is part of `make verify`. Formal axiom checks
require every requested declaration to be reported and allow only `propext`,
`Classical.choice` and `Quot.sound` (386 historical theorems and 168 Gaussian
declarations). They do not replace review of the statements' scope.

See [workflow runs](https://github.com/CrocSwap/integer-mult-bounds/actions/workflows/verify.yml)
for the combined-tree Linux checks. Main is advanced only after those checks
pass; the prior release remains available under its existing tag.
