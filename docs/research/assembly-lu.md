# Conditional kappa = 296461013/(2*10^17) > 2^-30

The new witness is **296461013/(2·10^17) ≈ 1.4823·10^-9**, about **2.5** times
the pair-star witness 5929220328/10^19. Both finite networks and their
certified savings are unchanged. Two downstream components change, each with a
written proof. The computational model and the retained upstream interfaces
remain assumptions, and the new proofs have not been independently reviewed.

- [Proof note (PDF)](../../artifacts/assembly-lu-note.pdf)
- [Proof source](../../notes/assembly-lu-note.tex), with the fragments
  [linear guard](../../notes/assembly-lu-guard.tex) and
  [banded solve](../../notes/assembly-lu-resampling.tex)
- [Independent upstream patch](../../patches/assembly-lu-30.patch)
- [Exact certificate](../../certificates/assembly-lu.json)

## 1. A linear coefficient guard

The simultaneous butterfly layer is evaluated exactly before one final
truncation, so its intermediate widths must be bounded. The retained guard
used a dependency-depth recurrence `A(e) <= s A(e/m) + E`. It charges each of
the `s` consecutive child calls of a node with the child's whole internal
depth, which gives widths `p + O(d^{5-4beta+zeta})` and the condition
`eps (5 - 4 beta + zeta) < 1`.

A completed child acts exactly as `C^{(x)f}` or its inverse. Every entry is a
unit times `(1+i)^{f mod 2} 2^{-ceil(f/2)}`, and every row has absolute sum
`2^{f/2}`. Charging completed children by this exact action makes the growth
add over the recursion levels instead of multiplying. The widths become
`p + C_0^* d` with `C_0^* = 64(W+m+1)^3 + 2s + m + 26`, evaluated with the
pair-star constants. The guard condition becomes `eps < 1`, and the stopping
exponent `beta` no longer enters any width condition.

## 2. Gaussian resampling with a constant width

The retained one-dimensional resampling lemma solves its square Gaussian
system by a Neumann series. That needs `theta > p/alpha^4`; with the retained
separations `theta_i ~ 1/d` it forces `alpha ~ (pd)^{1/4}`, and the Gaussian
row of the cost table has power `3/4 + delta + 5 eps/4`. Harvey and van der
Hoeven remark that a precomputed LU decomposition would relax this to
`theta > 1/alpha^2`, but did not use it because its error analysis is "considerably
more intricate".

The note proves a precomputed banded solve with a complete fixed-point error
analysis and tape cost. The system matrix itself need not be diagonally
dominant for small `alpha^2 theta`. An explicit periodic quadratic potential
gives a diagonal similarity after which every off-diagonal row sum is below
`0.0038`, for every `theta` and every `alpha >= 2`. Gaussian elimination
without pivoting then works in fixed point with `O(d)` extra bits. With
`alpha = 2` the Gaussian row has power `1/2 + delta + eps`, and the source
scale is `gamma = O(d^2)`.

## 3. Parameters and the ceiling

For certified savings `a_b`, `a_c` the parameter supremum moves from
`Q/(5+4Q)` to `Q/(2+2Q)`, with `Q = min(a_b, a_c)`. The certificate uses

    beta = 1/10, c = 1, delta = 10^-12, eps = 124999999/250000000,
    lambda' = 1 - a_b(1 - 10^-12), kappa = 296461013/(2*10^17).

All 31 strict conditions hold. The limiting margin is `g_3 = eps(1 - lambda')`,
with exact gap `22306317521666189976715649/(25*10^41)`. The eventual cutoffs
are astronomically large because `eps` is within `4*10^-9` of `1/2`; for
example `gamma <= b/4` needs `b >= 2^541000000`. Any fixed `eps < 1/2` gives
smaller cutoffs; `eps = 2/5` already gives about twice the previous witness.

This assembly cannot exceed `Q/2`: the retained margins `g_2`, `g_3`, the
transform layout condition `K <= ell - 1` and the prime-interval argument give
`kappa < eps min(q, c a_b)` with `eps < 1/2`. The new supremum is within the
factor `1 + Q` of that ceiling.

## 4. Checks

    make verify-assembly-lu
    make assembly-lu-note

`scripts/assembly_lu.py` re-derives `a_b` and `a_c` with the existing
paired-bit and pair-star functions, recomputes the node allowance from the
pair-star circuit, checks every rational constant of the written lemmas, both
scaled-exponent inequalities on every row of six instances, and every
constraint and margin of the witness. The tests also run the fixed-point
factorization and solve exactly on small instances, including two `alpha = 2`
systems whose unscaled off-diagonal row sums exceed `0.46`, and compare with a
high-precision reference solve. The patch generator builds on the pair-star
patch, and the tests check its pinned inputs, labels and references.

These checks support the written arguments. They do not verify the proofs, the
multitape implementation or the upstream theorem.

## 5. Audit status

Before publication, two independent adversarial AI reviews (Claude Opus 5.5
and Claude Fable 5.1, run separately, each with full `make verify` and its own
exact re-checks) examined this branch. Both returned *sound with minor
issues* and found no step that changes the claimed `kappa`. Their independent
checks include an exact test of the scaled-dominance inequalities on more than
4.7 million rows of 101 adversarial `(s, t)` instances, and an independent
fixed-point implementation of the `alpha = 2` banded solve with dynamic range up
to `2^192`.

Open minor items, none affecting `kappa`:

- Harvey and van der Hoeven state Lemmas 4.8 and 4.9 under the hypotheses of
  their Proposition 4.7, including `theta > p/alpha^4`, which fails at
  `alpha = 2`. Both reviews confirmed that the proofs of those lemmas (and the
  norm estimates of Proposition 4.7(i)) never use `theta`, so the use here
  rests on proof inspection. A follow-up will restate them with `theta`-free
  hypotheses and reproduce their short proofs.
- The reviews disagree on whether four quoted inequalities read `>` or `>=`
  in the printed manuscript. Either reading suffices at `alpha = 2`.
- The eventual cutoffs are astronomically large but fixed: about
  `b >= 2^(5.7*10^8)` for the prime intervals and for `gamma <= b/4`, and
  `p >= 10^79` for the guard. At the supremum the margins `g2` and `g4` are
  within a relative `O(a_b)` of binding.
