# Community follow-up review — 8 October 2026

Published baseline: `0605a24a28836168ad29d6239b46064b892298fc`,
κ = `971668963/25000000000000` from PR #39. This document records review;
it does not promote a new witness or change the published theorem's scope.

## Pinned candidates

| PR | Contributor | Reviewed head | Scope |
|---|---|---|---|
| [49](https://github.com/CrocSwap/integer-mult-bounds/pull/49) | Rohan Arun | `f95d2910e027495983b53cae1693cf535abf2569` | Composed circuit changes through PR #48, then additional pinned summand/leave-one-out swaps |
| [45](https://github.com/CrocSwap/integer-mult-bounds/pull/45) | Alejandro Zarzuelo Urdiales | `7f0764750f6c78b68a8f2c579c936ed377216ec4` | Gaussian parity, finite tensor execution, precision accounting, mixed-center reference decoder |
| [26](https://github.com/CrocSwap/integer-mult-bounds/pull/26) | Ryan S / princezuda | `f764fb98208506354730f6f108a8c87fb679432e` | Historical certificate arithmetic and frame/movement/guard lemmas |

No GitHub approvals, contributor messages, merges, or publication were performed
as part of this review. Earlier intermediate PRs were examined through the
composed construction, source provenance and comparison certificates. This is
not a claim to have replayed every intermediate PR head separately.

## PR #49: scientific assessment

The proposed conditional witness is

\[
\kappa=4123863984/10^{14}=0.00004123863984.
\]

It improves the published exponent saving by **6.102596178%**, and PR #48 by
about **0.12719%**. The dyadic corollary remains **2^-15**; it does not reach
2^-14. These percentages concern the exponent saving, not practical speed.

The changed construction retains the audited transfer interfaces. Sorting
disjoint summands preserves their sum; restoring the original indexing after
building leave-one-out vectors preserves the required outputs. The pinned
adjacent swaps change which compatible carriers can be retained. Floating-point
matching is used for discovery only: the selected edges, finite circuit and
resulting exact rank profiles are replayed.

The complete scalar checks at h=23 and h=25 include disjoint global supports,
all output identities, rational envelope containment, matching legality,
an independent role/rank recount, and the entire physical timeline acting on
every dirty input basis vector in both orientations. The actual new graphs
have 36,382 and 48,255 auxiliary roles, giving W=177,284,805 and m=575.
The rank deficit is still 1,846,900. Paid center copies and endpoint corrections
remain in the complete child list.

The inherited data-corner sweep covers all 4,073,300 triple pairs. Ten failures
at the first modular prime are recovered by exact rational elimination,
checking all 47 pivots and 346 prescribed ordered zeros per pair. Modular zeros
are not treated as rational zeros. Internal rank profiles use explicit
bounded-minor CRT certificates; the written low-rank correction/denominator
bounds were checked against the implementation.

The complex circuit, semantic guard, balanced physical layout and analytic
transfer remain inherited dependencies. The new finite counts fit their
existing contracts; no smaller scalar guard or omitted movement cost is being
assumed. This review does not formally verify the upstream multiplication
theorem or all-size tape implementation.

An independent check using the maintainer's 80-term rational logarithm and
12-term exponential enclosures confirms both contracting moments, the rank
mass, the seven margins and the strict assembly arithmetic. It imports no
contributor checker. The bit moment gap is at least approximately
1.3535e-15, and the final absorption gap is approximately 4.3257e-15.
The next bit-saving grid point at spacing 10^-14 fails the moment condition.
See [the arithmetic receipt](community-followup-arithmetic.json).

The full pinned `make verify` completed successfully: 192 regression tests,
17 copied-fixed focused tests, five climbed-48 focused tests, fresh producers
and 18 historical patch-application checks. Focused tests are also included
in the regression collection; these counts should not be added as distinct
tests. All 21 entries in the new source manifest match. The separate
clean-diff gate has the ordering-only finding below.

Reproduce independently from this review tree:

```sh
python3 scripts/audit_followup_candidate.py \
  --candidate-root ../integerMult-review-49 \
  --check docs/research/community-followup-arithmetic.json
```

### Integration finding

**Fix before merging:** the pinned PR's `make verify` regenerates
`certificates/endpoint-gauge-network.json` with numeric key order in one nested
histogram, while the checked-in artifact has lexicographic key order.
Parsed JSON values are identical, but the workflow's
`git diff --exit-code -- certificates patches` would reject the checkout.
Retain the reproducible artifact when integrating; this is not a numerical
counterexample to the witness.

Integrate onto current main, preserving its portable C++ header includes,
30-minute CI allowance, complete RaD source archive, historical results and
release attribution. The pinned branch predates those maintenance changes.
Linux CI must run on the resulting merged tree; this review's local replay
uses macOS/Clang/Python 3.14.

## PR #45: formal scope and assessment

The pinned Lean 4.31.0 build passes. An additional build with the already
installed Lean 4.29.0 also passed. The Python endpoint/precision checks,
full regenerated h=28 mixed-center image audit and canonical-tag adapter
checks pass. The independent image check includes 10,732,176 source/target
coefficient pairs, dirty-input controls and off-image rejection.
Printed axiom dependencies contain only `propext`, `Classical.choice` and
`Quot.sound`; no project axiom or `sorryAx` appeared.

The formal development proves actual finite recursive tensor execution and
inverse restoration, Gaussian divisibility/parity and canonical tags, and the
all-width upper bound for the 29-class completed-child precision profile.
That profile equals the published main profile. The concrete producer/image
link is checked independently in Python; it is not a Lean refinement proof
of the entire producer.

The completed-child precision component drops from 421,548,223,824 f to at most
211,345,564,248 f. This is **not** a halving of total memory, runtime or the
global guard. The scalar E term and κ are unchanged. Dirty values must be
differenced before exploiting fresh-image divisibility, all ports must share
the promised scalar phase frame, and the standalone decoder checks the full
producer-image condition. The README and frame review state these boundaries.

Recommendation: integrate as a separately attributed verification/reference
package. Do not advertise a new multiplication bound or a fully formalized
multiplication algorithm from this PR.

## PR #26: formal scope and assessment

The pinned Lean 4.21.0/Mathlib build passes all four libraries. Source checks
cover 134 declarations and 241 references. The historical PR checks validate
404, 364 and 439 tagged references respectively, including the mutation
self-test and vendored source hashes. The original source checks also pass
when pointed at published main's notes and certificates.
A separately generated audit prints dependencies for all 386 named theorems
across the four libraries, checks that every requested theorem is reported,
and accepts only `propext`, `Classical.choice` and `Quot.sound`. It passes.

The independent h=50 paired-circuit checker reproduces 450,394 additions,
58,800 output roles and R=509,194, with exact disjoint supports and outputs.
Its small-case corruption controls pass.

These are valuable checks of the historical 2^-34-era witness and selected
early PRs, plus reusable algebraic lemmas. Count definitions are inputs to the
Lean arithmetic. The guard recurrences are hypotheses; physical tape costs
and the complete multiplication theorem are not formalized. The older
constants should remain explicitly historical.

Recommendation: integrate as formal verification of the stated historical
contracts. Preserve the author's scoped corrections to earlier ceiling and
documentation claims rather than presenting them as failures of the current
published bound.

## Credit for the composed increment

| PRs | Contributor | Contribution retained or recognized |
|---|---|---|
| 40, 42 | Rohan Arun | Both-fixed-basis data corners and composition with alternating producers |
| 41 | RaD / hipotures | Alternating pair order and independent physical role/timeline compiler |
| 43 | Chafik Boukhalfa | Changed graph/fixed-basis composition and independent finite checkers |
| 44 | Rohan Arun | Weighted carrier matching discovery and replay profiler |
| 46 | Chafik Boukhalfa | Exact rational recovery of ten modular failures and matching integration |
| 47 | Rohan Arun | Hill-climbing summand order |
| 48 | Chafik Boukhalfa | Reordered leave-one-out sums with restored output indexing |
| 49 | Rohan Arun | Joint pinned summand and leave-one-out hill climb |
| 45 | Alejandro Zarzuelo Urdiales | Gaussian parity, finite execution proofs and scalar reference checks |
| 26 | Ryan S / princezuda | Lean arithmetic, algebraic contracts and independent paired-circuit audit |

Retain all earlier credits, including icekylinx, James Chang, Dominik Scholz,
Zhihao Chen, Aurel Prosz, Swapnil Jain, eumemic, Andrew Barnes, David Leen,
Douglas Colkitt, OpenAI, and Harvey–van der Hoeven, as applicable to their
respective inherited components. Preserve contributors' AI-assistance
disclosures. Parallel or superseded contributions should be recognized even
when their exact numerical witness is not the final selected one.
