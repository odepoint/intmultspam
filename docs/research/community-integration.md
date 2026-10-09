# Community integration ledger

## Pinned inputs and acceptance boundary

- Preserved conditional 2^-30 checkpoint: `1a74950` (`release/ternary-30`).
- Community candidate: [PR #39](https://github.com/CrocSwap/integer-mult-bounds/pull/39),
  `70ae24129649f6d6d4ec6360962a80c3c42a38f1`.
- Contributor's tested research commit: `50e54ece17afa4bd3cccd1927e9cdea5098038c2`.
- Submitted saving: `971668963/25000000000000`, approximately `3.886675852e-5`.
- Status: **conditionally accepted after maintainer mathematical audit**.
  The [final report](community-final-audit.md) accepts the written extensions
  under the retained original #109 interfaces. This is not formal verification
  or independent human peer review. The community release adopts this witness and preserves the prior
  checkpoint.

The merge preserves contributor Git history and scientific source files.
The regenerated `endpoint-gauge-network.json` differs from its incoming snapshot
only in numeric-key ordering; exact parsed JSON equality is checked. Keeping the
generator's serialization makes the combined CI reproducibility check pass.
Root documentation distinguishes checkpoint evidence from candidate claims.
The Makefile takes the union of both verification suites and patch checks.
Original notices, Apache-2.0/CC0 files and AI-assistance disclosures are retained.
No separate contributor comments or manual bulk PR closures are part of this
release; publishing the preserved ancestry may mark incorporated PRs merged.

## Attribution and parallel work

[CONTRIBUTORS.md](../../CONTRIBUTORS.md) covers all 39 submissions at the checkpoint,
including parallel implementations and closed #11/#30. It distinguishes credit
from acceptance. Imported source-specific credits in NOTICE, SOURCES.json and
references/ are additive to that record. A stronger final PR does not displace
credit to the people who supplied its constituent ideas or earlier checkpoints.

## Review gates

| Gate | Required evidence | Maintainer status |
| --- | --- | --- |
| Combined repository | Fresh producer rebuilds, both checkpoint/candidate tests, source hashes and all independent patch checks | Passed: 218 tests, 20 patch checks; Docker and three-version Linux CI |
| Fast Gaussian resampling | Correlation packing, shifted input enclosure and sequential tape cost | Accepted; new phase-cell inverse replaces the old restricted Neumann-count argument |
| Batched transfer | One common controlled basis, contiguous physical blocks, exact child widths/volumes and remainders | Accepted under retained elementary-stream interfaces |
| Semantic/bulk interface | Completed-child induction, scalar charge, routing, precision, primes and product row reserves | Accepted; normalization, seam cuts, locality and factor-page traffic included |
| Two-stage/copy schedules | Arbitrary scratch restoration, paid endpoint corrections, copied-center transforms and both orientations | Accepted; terminal-use and paid-copy conditions tied to the selected schedule |
| Selected basis/rank profile | Rational nonvanishing, universal zeros, bounded-minor CRT and all physical transitions | Accepted; modular nonvanishing distinguished from universal-zero and CRT proofs |
| Final assembly | Strict exact margins using reviewed interfaces and constructive eventual cutoffs | Accepted; additional independent moment/margin cross-check agrees |

A failed gate should isolate the strongest surviving earlier checkpoint rather
than trigger an unsupported all-or-nothing acceptance of the latest number.
The independent 2^-30 checkpoint remains available throughout review.

## Bounded mathematical inspection

The sections below retain the history of the initial review. Their pending
items are superseded by the final report and gate statuses above.

The projector-batching argument explicitly obtains a contiguous identity Schur
block from the idempotent equation, rather than treating every matrix of a given
rank as batchable. The mixed-width recurrence requires a strict weighted moment
and every child width strictly below the parent. These are the changed interfaces
that must carry through the full selected construction.

The copied-center argument uses two physical streams: a paid transformed copy
supplies read-only scatter, while the original goes directly to its cleanup
frame. This reproduces both old scalar inputs for arbitrary dirty values. Its
use on every actual producer terminal, and the complete sequential tape schedule,
remain separate obligations; this local algebra is not an end-to-end audit.

The semantic guard argues from the exact completed child operator, with only
one active child's temporary precision overhead. It keeps the fine-grid encoding
and does not insert intermediate rounding. Its composition with the bulk
resampling and routing arguments still requires a full dependency review.

## Initial observations

The incoming batching and two-stage changes alter hypotheses of the previous
singleton-call and three-stage ceilings. Stronger submitted exponents are not
by themselves contradictions of those scoped ceilings.

The copied-center lemma explicitly pays a rank-r transform on the temporary
stream; it does not simply delete the original return cost. Its sequential
copy/read/discard interface and complete role volume remain proof dependencies.
The shifted Gaussian approximation includes the F=2^ceil(1.14 alpha^2) enclosure
correction. These observations identify what to audit, not a completed proof.

## Subsequent submissions

PR #40 arrived during this replay and is credited in the community record.
It remains queued; this pass keeps #39 pinned rather than changing the scientific
input underneath a running verification.

## Maintainer validation

`make verify` passed on the combined tree: **217 tests and 20 independent
upstream patch checks**, plus the candidate's 10- and 12-test focused runs.
Fresh producer, label, geometry, CRT, moment and assembly rebuilding ran as part
of that command. All checkpoint scientific files remain byte-identical. The
[validation receipt](community-integration-validation.json) records source pins,
file counts, the sole JSON serialization change and the complete log hash.
The selected candidate's general mathematical dependencies remain under review;
these results support a reproducible integration candidate, not acceptance of
its stronger multiplication bound.

## Mathematical review in progress

The [first transfer review](community-transfer-review.md) records the checked
projector/block algebra, mixed-width induction, row-padding and scheduler
extension, and larger-child semantic precision induction. Its scope is explicit:
the selected geometry and the bulk analytic/tape composition are not yet accepted.

## Linux portability follow-up

The initial integration CI failed under GCC because `binary_io.hpp` used
`std::reverse` without including `<algorithm>`. It also relied on caller includes
for array, integer, stream and vector declarations. The header now includes its
own dependencies; a standalone-header compilation regression checks this in the
normal suite. Existing source notices remain unchanged.

The original label-audit failure was reproduced in an isolated Ubuntu 24.04
Linux aarch64 Docker container (GCC 13.3, Python 3.12). The fixed header and
actual label-audit program compile there. Full Linux replay and the GitHub
Python matrix are tracked by the fix commit's CI. Source-hash certificates
were regenerated; their mathematical fields compare exactly with the preceding
commit. This portability correction does not change the exponent or the
outstanding mathematical review obligations.
