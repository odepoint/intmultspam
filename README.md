# Integer multiplication, just for fun

**Fork of [CrocSwap/integer-mult-bounds](https://github.com/CrocSwap/integer-mult-bounds)
by Douglas Colkitt.** The original Git history and credits are preserved.

A just-for-fun experiment to see how far AI can push an integer-multiplication
bound. This repo keeps the generated notes, code, and checks so the attempt is
easy to inspect and rerun. The math is largely unverified; this is a hobby
project, not a research paper.

## What this is based on

- **Douglas Colkitt, [A sharper exponent for integer multiplication](https://github.com/CrocSwap/integer-mult-bounds)**
  (`CrocSwap/integer-mult-bounds`), baseline commit
  [`6e564879f51ae16f23d392e9e196c605f36d90df`](https://github.com/CrocSwap/integer-mult-bounds/tree/6e564879f51ae16f23d392e9e196c605f36d90df).
  This supplies the existing code, compact-control construction, and earlier
  notes and checks. Its Git history and attribution are retained.
- **OpenAI, [Integer multiplication below n log n](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Integer-multiplication-below-n-log-n-September-23-2026/paper.pdf)**
  (September 23, 2026), pinned at
  `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. This is the underlying paper.
  Its bundled source and license remain unchanged in `upstream/`.

Citations are in [CITATION.cff](CITATION.cff) and [CITATION.bib](CITATION.bib).
Credit those sources for the underlying work. This experiment has no independent
review or endorsement from their authors.

## What the AI generated

The experiment tries a pair-star complex network on top of the baseline.
Its generated notes and exact-arithmetic scripts report the conditional value
`kappa = 5929220328/10^19 = 5.929220328e-10 > 2^-31`, about 7.14364 times the
baseline's exponent saving. This is the model's proposed improvement, and it
depends on the complete upstream theorem and the retained proof interfaces.
The scripts check finite identities and arithmetic; they do not validate the
full mathematical argument or measure a practical speedup.

At `h=24`, the generated circuit records 263 batches, 77,454 additions,
469,294 output uses, and 546,748 side roles per invocation. The files retain
the derivation and finite checks so the experiment can be inspected or rerun.

- [AI-generated experiment notes (PDF)](artifacts/complex-pair-star-note.pdf)
  and [editable TeX](notes/complex-pair-star-note.tex).
- [Circuit and frame checks](certificates/complex-pair-star.json) and
  [parameter output](certificates/complex_pair_star_parameters.json).
- [Experimental patch against the pinned source](patches/complex-pair-star-31.patch).
- [Verification transcript](artifacts/complex-pair-star-verification.txt).

### Latest: assembly refinements, `kappa > 2^-30`

A second AI-generated contribution, by William Porter's Claude agents, keeps
both finite networks unchanged and replaces two downstream components. It
bounds the layer coefficient guard linearly by charging completed children
with their exact kernels, and it solves the Gaussian resampling system by a
precomputed banded LU factorization. A diagonal similarity lets that solve use
the constant Gaussian width `alpha = 2`. The parameter supremum moves from
`Q/(5+4Q)` to `Q/(2+2Q)`, with `Q = min(a_b, a_c)`, and the exact witness is

`kappa = 296461013/(2*10^17) = 1.4823050650e-9 > 2^-30`,

about 2.5 times the pair-star value. Both independent adversarial AI audits
(Opus and Fable) judged it sound with minor issues; that is not a human
review, and everything stays conditional on the same retained interfaces.

- [Assembly notes (PDF)](artifacts/assembly-lu-note.pdf) and
  [editable TeX](notes/assembly-lu-note.tex).
- [Exact certificate](certificates/assembly-lu.json) and
  [summary](docs/research/assembly-lu.md).
- [Patch against the pinned source](patches/assembly-lu-30.patch).

Earlier notes and release drafts are preserved as background from the original
project. They describe that project's work and publication plans.

## Agent Note


## note that https://github.com/CrocSwap/integer-mult-bounds/pull/6
exists and is worth periodically checking, always look for updates


With Python 3.11 or newer, Git, and Make:

```sh
make verify-pair-star    # Checks for the pair-star experiment
make verify-assembly-lu  # Checks for the assembly refinements
make verify              # Also runs all inherited checks
git diff --exit-code -- certificates patches
```

These checks need no third-party Python packages or network access. The final
command checks that the generated certificates and patches match the checkout.
The existing GitHub Actions workflow runs the full checks on Python 3.11,
3.13, and 3.14. Finite checks and exact arithmetic are not a review of the full
mathematical argument.

To rebuild the experiment notes with pdfLaTeX, run `make pair-star-note`;
the assembly notes build with Tectonic via `make assembly-lu-note`.
See [reproduction instructions](docs/reproducibility.md) for details.

## Credits and license

Put together by **odepoint (Owen DePoint)**, using AI-generated material from
OpenAI models, out of curiosity and for fun. The notes document the attempt;
they make no claim to novelty or priority.

The assembly refinements (`*assembly-lu*` files) were contributed by
**William Porter** with Claude Opus 5.5 / Fable 5.1 agents via Hermes, in the
same just-for-fun spirit.

Original repository and baseline work: **Douglas Colkitt**. Underlying paper: **OpenAI**.
Licensed under [Apache-2.0](LICENSE), with original notices retained in
[NOTICE](NOTICE) and [upstream/LICENSE](upstream/LICENSE).
