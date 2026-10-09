# Contributing to the experiment

This is a hobby project exploring integer multiplication with AI, just for fun.
Corrections to the generated math, code, and source attribution are welcome
through issues or pull requests. The mathematical claims remain unreviewed.

For a mathematical issue, identify the exact proposition, source label, or
inequality; give a counterexample or the missing implication when possible;
and distinguish numerical validation from an algorithmic proof obligation.
For the current pair-star result, start with the
[AI-generated experiment notes](notes/complex-pair-star-note.tex) and their
[construction](notes/complex-pair-star-construction.tex). For retained baseline
dependencies, consult the
[compact-control review guide](docs/research/compact-control-review.md).
For the current result, start with the
[ternary review guide](docs/research/ternary-review.md).
The [original audit](docs/audit.md) describes the retained upstream assumptions.

For a parameter improvement, supply exact rational choices, the full dependency
argument, and an updated patch against the pinned source. Explain whether the
change stays within the parameter ceiling or changes one of its hypotheses.

Keep `upstream/` unchanged. Edit the generators under `scripts/`, then run:

```sh
make verify
```

Include regenerated certificates and patches in the same change. If the note
changes, also run its corresponding PDF target (`make pair-star-note` for the
current result) and include the updated PDF. Review changes to
claims in the README and note together. Finite tests should address a mathematical
identity or a failure mode, rather than simply restating implementation details.

New contributions are under the repository's Apache-2.0 license. Retain source
attribution and disclose substantial AI assistance. Do not describe certificate
success as a formal verification of the full multiplication theorem.

Before building on pending work, consult the [contribution-review index](docs/research/contribution-review.md), pin its sources, and preserve contributor attribution.

Parallel approaches, small improvements, independent reproductions, review and
well-scoped negative results are welcome. Please identify predecessor work and
explain what your submission adds, even if a concurrent result has a stronger
headline. We preserve credit for useful contributions that are superseded or not
imported; see [CONTRIBUTORS.md](CONTRIBUTORS.md). Attribution corrections are
welcome too. State which proof obligations remain open rather than presenting
finite certificate checks as a complete theorem audit.

On `integration/community`, `make verify` also covers the imported candidate
chain. See [the integration ledger](docs/research/community-integration.md) for
remaining proof obligations and [the batching guide](docs/research/batched-review.md)
for the changed recursive interface. Preserve the historical checkpoint tests.
Imported CC0 proof sources retain their source-specific license and notice.
