# Reviewing the conditional 2^-30 checkpoint

This package is a separate, reproducible F3 five-subset implementation. It
acknowledges the earlier related motif and stronger claimed construction in
[Zhihao Chen's PR #7](https://github.com/CrocSwap/integer-mult-bounds/pull/7).
That submission and its descendants are not imported or certified here.
The full upstream multiplication theorem and the retained analytic extensions
remain assumptions. No priority or strongest-known-bound claim is made.

## New obligations

| Obligation | General argument | Executable evidence |
| --- | --- | --- |
| Fixed F3 payloads preserve the bit interchange recurrence | [Finite-alphabet transfer](../../notes/finite-alphabet-transfer.tex): induct on all symbol arrays, retain logical volume V, and distinguish scalar and address primes | Prime-scalar compiler controls; source integration tests |
| Central and side maps sum to identity | [Five-subset construction](../../notes/ternary-five-subsets.tex): pair incidence mod 3 and the unique common pair | Complete small coefficient maps and full local disjoint-sum template |
| Cross-group sharing is exact | Full common-intersection/residual-set signatures and deterministic tensor recursion | Full h=29 integer DAG construction, pruning, counts and hashes; independent complete h=8,9 support reconstruction |
| Arbitrary side and center inputs are restored | Signed twelve-operation schedule and its inverse | Exact F3 bit-plane linear forms on every small-instance independent input |
| Rational frames satisfy the complete contract | Common-pair positivity, forward spans/reverse complements, tensor boundaries, orthogonal matching and final sign correction | Every physical small invocation edge in both directions; complete small three-stage prime controls |
| The new bit interface composes with the retained complex one | [Assembly in the note](../../notes/ternary-five-subsets.tex) and independent source patch | Exact constraints, seven strict margins, all changed derived powers and retained proof texts |

## Counts and witness

At h=29, n=118755, r=406 and m=24389. The DAG has 19,593,239 active additions
and 1,187,550 partial output uses, giving 20,780,789 side roles per invocation.
The shared complete network has

    W = 589493540769997500
    Delta = 678497406452775
    s = 14377157287342062574725

The exact logarithm comparison certifies a_b=467/10^11. The complex saving
remains a_c=5/10^9; its circuit, scalar node charge and precision constants
are unchanged. The final parameters are

    epsilon=1999/10000, c=1, beta=1/100, zeta=1/1000,
    delta=1/10^6, C1=4961/1000,
    lambda=1-4669/10^12, lambda'=1-4668/10^12,
    kappa=2^-30.

The minimum margin is `2332833/2500000000000000`. Its excess over 2^-30 is
`296652863/163840000000000000000`, about 0.194% of the claimed saving.
The strict gap absorbs polylogarithmic factors asymptotically; it is not an
estimate of practical runtime or the size at which the bound becomes useful.

## What the checks do not establish

The full h=29 scalar network is specified generatively rather than expanded
as W physical roles. The full side DAG is generated, but every rational
matrix on that enormous complete network is not materialized. The general
frame and sharing arguments establish those counts; smaller exact controls
test their implementation. The large orthogonal label matching is proved
by regularity and Hall's condition, with a deterministic finite algorithm,
rather than listed explicitly.

There is no formal verification of the complete theorem, full multiplication
machine simulation, or independent mathematical review. In particular,
passing arithmetic and finite tests does not independently prove the upstream
stream, transform, resampling, or error-transfer interfaces.

## Reproduction

Run `make verify` and `make ternary-note`. The independent
[patch](../../patches/ternary-30.patch) applies directly to the original pinned
manuscript, not to another patch. The
[certificate](../../certificates/ternary-side.json) records source hashes;
the patch generator rejects stale sources. See
[reproducibility](../reproducibility.md) for manuscript preview instructions.
