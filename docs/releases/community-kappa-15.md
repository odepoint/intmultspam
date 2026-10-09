# Community result: conditional exponent saving above 2^-15

Release: `community-kappa-15-2026-10-08`.

This release incorporates the reviewed community witness

\[
T(n)=O\bigl(n(\log n)^{1-\kappa}\bigr),\qquad
\kappa=971668963/25000000000000=3.886675852\times10^{-5}>2^{-15}.
\]

**The final contribution is by Rohan Arun (@rohanarun),
[PR #39](https://github.com/CrocSwap/integer-mult-bounds/pull/39).**
It fixes the middle basis in the copied reversed-corner construction,
certifies every required physical profile and supplies the common-basis
proof and final composition. The imported PR is pinned at
`70ae24129649f6d6d4ec6360962a80c3c42a38f1`.

The result is a community effort. Its incorporated dependencies credit:

- **icekylinx:** batching, partial swaps, fixed profiles, copied centers and
  the selected complex circuit.
- **Zhihao Chen (@jacklightChen):** controlled bases, translated frames,
  semantic/bulk compatibility and two-stage integration.
- **RaD (@hipotures):** semantic precision, coordinate routing, phase-cell
  inversion and bulk resampling.
- **James Chang (@jamesyc):** reversed geometry and exact certificates.
- **Aurel Prosz (@Paureel), Swapnil Jain:** attributed two-stage development
  and paid copied-stream endpoint work.
- **Dominik Scholz (@DominikScholz):** dimension, parameter and fixed-basis refinements.
- **eumemic, Bortlesboat and dleen:** earlier complex, Gaussian, source-frame,
  pairing, retained-total and sharing contributions.

Douglas Colkitt maintains the original project and its review/integration,
with OpenAI Codex assistance. The [full contribution record](../../CONTRIBUTORS.md)
also preserves parallel, incremental, superseded and pending work; credit is
not restricted to the final winning parameter set. Source-specific authorship,
AI-assistance disclosures and licenses remain in [NOTICE](../../NOTICE).

The [completed audit](../research/community-final-audit.md) accepts the new
arguments conditionally on the original OpenAI #109 framework. Validation
includes 218 tests, 20 historical patch checks, fresh producers, exact
profiles, Linux/GCC reproduction and a three-version Linux Python matrix.
An additional arithmetic checker independently encloses both recursive moments,
reconstructs all seven final margins and rejects the next bit-saving grid point.
Missing pinned reference files were restored with their original hashes.

This is a conditional research release, without full formal verification or
independent human peer review. It makes no practical runtime, worldwide
priority or strongest-known-algorithm claim. The value is 27.36% above 2^-15
as an exponent saving. The former 2^-30 checkpoint and all historical
scientific artifacts are retained. PR #40 and later contributions remain
outside this pinned review.

Start with the [proof and reproduction guide](../../research/copied-fixed-reversed/README.md)
and [exact certificate](../../research/copied-fixed-reversed/certificate.json).
Run `make verify` for the full suite or `make community-audit-check` for
the additional arithmetic/source check. Requires Python 3.11+, Git, Make
and GCC/Clang with C++17 and unsigned 128-bit integer support.

Project license: Apache-2.0; selected bundled RaD sources retain CC0.
The original OpenAI manuscript and Harvey–van der Hoeven analytic machinery
retain their existing attribution. This is not an official OpenAI release.
