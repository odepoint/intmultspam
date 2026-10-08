# Archived baseline announcement draft

This is preserved text from Douglas Colkitt's
[integer-mult-bounds](https://github.com/CrocSwap/integer-mult-bounds/tree/6e564879f51ae16f23d392e9e196c605f36d90df).
It describes the original project's work. This repository is a separate hobby
project exploring integer multiplication with AI, just for fun. The original
draft follows for provenance.

Prepared for publication after the repository is updated. Nothing has been
posted by preparing this file. Each numbered paragraph is a separate post.

**1/4**

New conditional integer-multiplication result: κ > 2⁻³⁴ in O(n (log n)^(1−κ)), building on OpenAI #109.

Our exact witness, κ = 8.3 × 10⁻¹¹, is ~48 million times our previous 2⁻⁵⁹ exponent saving. This compares exponents, not practical runtimes.

**2/4**

The key: move compact control bits instead of entire spaced windows. We construct the temporary fields from existing address space and restore them exactly. Removing the spacing penalty breaks the quadratic bottleneck in our previous analysis.

**3/4**

This is a structural proof extension. The note covers tape costs, recursive layout, exceptional repair and precision. The upstream theorem remains assumed; our new arguments await independent review. Exact arithmetic and finite tests support the written proof.

**4/4**

Proof note, certificates, source patch and a focused review guide:
https://github.com/CrocSwap/integer-mult-bounds

The complex finite network now limits this construction. Improving it is the next research target. Developed with OpenAI Codex; independent review welcome.

## Claim boundaries

- The strongest witness is `83/10^12`, strictly between `2^-34` and `2^-33`.
- The approximately 48-million-fold comparison uses that exact witness.
  Comparing only `2^-34` to `2^-59` gives exactly `2^25`, about 33.55 million.
- The result is conditional on retained upstream interfaces and the new written
  arguments. Tests and PDF builds are not independent mathematical review.
- The scoped ceiling applies only to the fixed `h=25` complex motif and retained
  Gaussian/leaf inequalities. It is not a general limit on integer multiplication.
- No practical benchmark, best-known claim, priority claim or unrestricted
  optimality claim is made.

Author: Douglas Colkitt. See the [proof note](../artifacts/compact-control-note.pdf)
and [review guide](research/compact-control-review.md) for the precise scope.
