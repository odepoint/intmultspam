# Higher-rank labels in the bit core compiler

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: an exact finite-interface extension and small controls. **No improved
block geometry or multiplication exponent is supplied.** The retained
conditional bound remains 2⁻³¹.

The scalar binary core C still has n labels, diagonal one, and a factor of
inner size r. Replace the rank-one rational idempotents by rank-ℓ idempotents
P_i in dimension d. Require mutual annihilation P_i P_j=P_j P_i=0 on every
side edge. No symmetric form is required.

A rational block fitting matrix gives such labels: normalize every diagonal
ℓ×ℓ block to I_ℓ and require both cross blocks to vanish wherever C_ij=1.
Factor F=BA with inner dimension d=rank_Q(F), partitioning its rows and
columns by labels. Then P_i=A_i B_i is idempotent of rank ℓ. The exact
checker verifies the factorization, ranks, and all annihilation constraints.
This block fitting formulation is the fractional-Haemers representation
framework; see [Bukh and Cox, §2.1](https://arxiv.org/html/1802.00476v2).
The network compilation and accounting below are additional obligations.

The existing three tensor stages work with these idempotents. Nested
idempotent differences still have rank equal to the difference of ranks.
The source tensor has rank ℓ³, and a central return loses dℓ² dimensions.
All scalar inputs, including auxiliary inputs, remain arbitrary and restored.
Consequently, for S side roles per invocation,

```
N = n³, m = d³
L = 3 n² r d ℓ²
Δ = N ℓ³ − 2L = n² ℓ² (nℓ−6rd)
s = Wm − Δ.
```

Without sharing, W=2N+3n²(S+r). With an orthogonal label matching and the
initial-gate adjustment of [shared-core.md](shared-core.md), W=2N+2n²(S+r).
The join still saves exactly m rank per removed auxiliary role. The complete
raw side-edge compiler is implemented and checked on expanded rank-two
controls, with and without sharing. ℓ=1 reproduces the earlier ledger.

For compressed side circuits, these counts are conditional on proving their
new frames and invocation boundaries. A block fitting matrix does not
supply that proof automatically. In particular, the old common-point span
argument must not simply be assumed to survive a different block geometry.

The dimension that helps is d/ℓ, but the logarithm remains log(d³).
Taking ℓ identical copies of an old scalar representation multiplies m and
s by ℓ³, preserves the relative deficit, and worsens the exponent saving.
The certificate checks this on the positive retained paired construction.
A useful block construction must improve the representation itself.

As a quantitative research target, rank-two labels for the triple relation
in ambient dimension h around 26–28 would permit approximately 31 side roles
per label at bit saving 1.6×10⁻⁷. **Those labels have not been constructed.**
Their compressed side frames would also need proof, and the complex interface
would need further improvement to assemble κ≥2⁻²⁵.

Run `python3 scripts/audit_block_core.py`. See
[the certificate](../../certificates/block-core.json) and
[the implementation](../../scripts/experiments/block_core.py).
The unrestricted finite transfer theorem already accepts rational frames;
this work verifies a new structured way of supplying them, not the upstream
multiplication theorem itself.
