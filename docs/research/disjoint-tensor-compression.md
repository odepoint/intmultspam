# Complex-network headroom from tensor contractions

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: a new finite complex-network construction with a written transfer
proof and exact checks. **The retained conditional multiplication bound is
still κ = 2⁻³¹.** This work does not independently verify upstream #109.

The disjoint-triple side computation now shares intermediate sums across
both halves of a ground-set split. The previous rectangle cover shared only
inside each rectangle. Equal sums are interned globally. All additions have
disjoint supports, so the scalar map is checked over the integers, not merely
modulo two.

At ground size 26:

| Quantity | Retained complex circuit | New tensor circuit |
|---|---:|---:|
| Disjoint-triple roles | 491,956 | 60,372 |
| Intersection-two roles | 29,250 | 29,250 |
| Total side roles per invocation | 521,206 | 89,622 |
| A certified complex saving | 5 × 10⁻⁹ | 3 × 10⁻⁸ |

The smaller disjoint circuit has 57,772 additions and 2,600 outputs. Its
reversible embedding uses their sum in roles, including retired and fanout
roles. The complete signed invocation restores arbitrary independent scratch.

The main proof obligation is the phase geometry. Each node gets either its
single source line, its single target's orthogonal complement, or the
coordinate space on its ancestor ground points. Ancestor and reachable-target
families form a disjoint rectangle even though the full circuit is a DAG.
This gives nested frames with explicit norm-one residual witnesses. The
reverse orientation uses its own exchanged-family assignment. All physical
transitions are checked; small controls additionally construct every
residual's orthonormal basis.

See [the proof](../../notes/disjoint-tensor-compression.tex),
[the compiler](../../scripts/experiments/disjoint_tensor.py), and
[the certificate](../../certificates/disjoint-tensor-compression.json).
Run `python3 scripts/audit_disjoint_tensor.py` to reproduce it.

The certificate includes the scalar node-charge bound and stopped-depth
hypothesis. A bounded even-ground-size scan is a construction comparison,
not an optimality theorem. The bit network still limits the multiplication
exponent. The new complex headroom can be carried into a later bit-network
improvement; it alone is insufficient for κ ≥ 2⁻²⁵.
