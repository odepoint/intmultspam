# A rank-h dyadic complex center

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

The [explicit factor](../../scripts/experiments/complex_centers.py) removes
one central role per invocation from the new disjoint-tensor construction.
At h=26 it certifies **complex saving a_c > 3.6e-8**, versus the separately
banked 3e-8 and the integrated 5e-9. The integrated conditional kappa remains
2^-31; the bit network is unchanged and remains limiting.

Fix a base triple T0={0,1,2}. The central matrix (|S intersection T|-1)/2
factors through h centers using an integral gather and a scatter with
coefficients in {0,1,-1/2,1/2}. The identity follows by expanding t_T-t_T0
in the basis e_i-e_0, i=1,...,h-1, of the coordinate-sum-zero hyperplane.
The [proof](../../notes/dyadic-central-factor.tex) gives both factors.

This is a scalar factor change, with all central gate incidences and common
frames retained. Each surviving center still has one downward transition
of dimension h. Every arbitrary center and side input is restored. The
three-stage and shared-bank proofs therefore apply with h centers:

    v = binom(h,3), m = h^3,
    W = 2v^3 + 2v^2(R+h), L = 3v^2 h^2,
    s = Wm - 2v^3 + 2L.

The [audit](../../scripts/audit_complex_centers.py) checks all 6,760,000
central coefficients at h=26, the existing full side map and phase ledger,
the complete scalar-operation charge, exact logarithm bounds and the
stopped-depth guard. Tests use independent formal dirty inputs in both
signed directions and reject corrupted factors.

Run `python3 scripts/audit_complex_centers.py` and
`python3 -m unittest discover -s tests -p test_complex_centers.py`.
The [certificate](../../certificates/dyadic-central-factor.json) hashes its
source dependencies. This supplements earlier artifacts without changing
their sources or integrating a new public multiplication claim.
