# Stopped depth beyond the fifth-power network hypothesis

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: a general conditional depth lemma and hypothetical parameter checks.
No new finite network or stronger multiplication exponent is established by
this certificate. The retained conditional witness remains κ=2⁻³¹.

The retained guard proof used s<m⁵. New finite families can have larger total
residual counts s even when s/W has a useful exponent. The same argument
works with any rational α≥1 satisfying s<m^α, provided the actual scalar
recurrence and additive node charge E have been verified. Its guard exponent
becomes C₁=α−(α−1)β+ζ. Rational α is checked by an integer-power comparison.

[The proof](../../notes/general-network-guard.tex) retains E as an additive
charge; it does not insert E into the recursive branching factor. It includes
base-m pieces, stopped leaves, and the outer allowance. At α=5, the audit
reproduces the retained guard constants exactly.

Larger α requires more complex-network headroom. From selected necessary
assembly constraints, writing t=1−β gives

```
κ < min(a_b, t a_c) / max(5, 1+(α−1)t).
```

Optimizing this subsystem retains the bit/Gaussian cap a_b/5 when
 a_c/a_b ≥ max(1,(α−1)/4). This is a necessary-constraint ceiling, not proof
that the entire system attains it. For example, α=7 with a_b=1.6×10⁻⁷,
a_c=3.2×10⁻⁷ admits a numerical assembly witness for κ=2⁻²⁵. No finite
networks achieving those interfaces are supplied by this calculation.

Run `python3 scripts/audit_general_guard.py` to reproduce the
[certificate](../../certificates/general-network-guard.json), including a
negative hypothetical control, retained-constant regression, and unproved
complex-family size profiles. Scalar coefficients and phase kernels of a
new network must still satisfy the full transfer interface.
