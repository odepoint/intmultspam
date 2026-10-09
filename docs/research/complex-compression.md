# Reusable complex-network compression

This local follow-up supplies a weighted circuit construction with compatible
binary phase frames. At `h=26` it supports **complex saving `a_c=5e-9`**,
about twelve times the `4.18e-10` used in the published compact-control result.
The bit network remains unchanged. It is now the tighter interface.

- [Written proof (PDF)](../../artifacts/complex-compression-note.pdf)
- [Reusable construction source](../../notes/complex-compression.tex)
- [Combined upstream patch](../../patches/complex-compression-31.patch)
- [Integration review guide](complex-compression-review.md)
- [Exact certificate](../../certificates/complex-compression.json)
- [Circuit and accounting implementation](../../scripts/complex_compression.py)
- [Binary frame checker](../../scripts/binary_phase_frames.py)

The supplied parameters support **`kappa=2^-31`** in an independent complete
upstream patch. The finite-network proof, new complex constants, scalar guard
charge, recurrence ordering and assembly are integrated. The preceding
`83/10^12 > 2^-34` certificate and patch remain unchanged. No independent or
formal verification is asserted.

## Why this is more than a stage-reuse trick

The original complex side map has two parts: coefficient `+1/2` for disjoint
triples, and `-1/2` for triples sharing exactly two points. We now compress
them through two different reusable frame constructions.

**Disjoint triples use coordinate enclosures.** A rectangle's source and
target ground-point unions are disjoint. When both families have multiple
triples, the coordinate space on the source union supplies a nondegenerate
intermediate frame. Each required residual has a spare coordinate of norm
one. For singleton source or target families, use the source line or target
orthogonal complement instead. This exception matters: a nondegenerate
binary residual can be alternating and lack the orthonormal basis the
upstream kernel interface requires.

The construction works for any exact disjoint-triple rectangle partition.
Its larger intermediate frames incur no extra loss because every side
transition stays increasing. The role count, rather than the intermediate
dimension, therefore determines the improvement in the telescoping budget.

**Intersection-two sums use an explicit orthonormal family.** For a fixed
common pair `{i,j}`, the labels `e_i+e_j+e_a` are mutually orthonormal.
When `h` is even they extend to an explicit orthonormal basis of the whole
space using two additional vectors. Consequently any cancellation-free
sum circuit for the leave-one-out relation has valid nested support frames
in both directions. We use a simple prefix/suffix circuit initially.

The scalar compiler uses characteristic-zero sums, signed injections and
half coefficients. It does not reuse XOR arithmetic incorrectly. A signed
twelve-operation transparent schedule restores all arbitrary auxiliary
values. The reverse stage uses reachable-output frames, not forward-source
frames in the wrong direction.

Finally, flipping every point to its partner in an even ground set maps
each triple to an orthogonal triple. This permits complete first/third-stage
auxiliary-bank reuse, including centers. The joining residual also has a
norm-one witness, so reuse saves exactly `m` kernel factors per removed role.

## Exact counts and the new bottleneck

At `h=26`:

| Quantity | Value |
| --- | ---: |
| Disjoint-triple rectangles | 24,870 |
| Disjoint-triple side roles per invocation | 491,956 |
| Intersection-two side roles per invocation | 29,250 |
| Total side roles per invocation | 521,206 |
| Dimension `m` | 17,576 |
| Total roles `W` | 7,082,222,160,000 |
| Residual count `s` | 124,477,130,005,280,000 |
| Preserved deficit `W*m-s` | 6,678,880,000 |

The relative deficit is `19/354111108`. Exact logarithm enclosures put the
actual complex saving near `5.48945e-9`, and support the simpler strict
choice `5e-9`. The even-`h` screen covers 22 through 40; it is not an all-`h`
optimality claim.

With the published bit saving `a_b=2.96e-9`, take

    epsilon=199/1000, c=1, beta=1/100, zeta=1/1000,
    delta=1/10000, C1=4961/1000,
    lambda=1-293/10^11, lambda'=1-29/10^10.

The minimum assembly margin is exactly `5771/10^13 = 5.771e-10 > 2^-31`.
All compact-movement, reservation, stopping, precision and final parameter
inequalities pass with strict gaps. An explicit scalar-operation count fits
the generalized guard's additive node charge.

The internal movement exponent now binds through the bit interface. With
that bit saving and the retained Gaussian constraint, `kappa<a_b/5=5.92e-10`,
which is below `2^-30`. Improving only this complex network further cannot
cross that boundary. The new complex interface already has the numerical
headroom needed for `2^-30` if the bit interface becomes sufficiently strong;
this is an accounting observation, not another construction.

## Verification and scope

Run:

```sh
python3 scripts/complex_compression.py
python3 scripts/make_complex_compression_patch.py
python3 -m unittest discover -s tests -p test_complex_compression.py -v
make complex-note
```

The certificate enumerates all **4,604,600 ordered disjoint-triple pairs**
at the construction size, checks the rectangle frame conditions, verifies
integer coefficients and both frame directions of the shared-sum compiler,
and checks the full triple matching. Small controls explicitly construct
orthonormal residual bases and verify phase identities modulo four.

The scalar tests use independent formal rational variables for every data,
side and central input in an `h=8` invocation, checking the complete linear
map in both signed directions. A further exact rational test composes three
stages while reusing dirty scratch. That local composition does not simulate
the entire tensor-indexed network; the general role matching and tensor
frame argument are supplied in the proof note. Negative tests reject
degenerate frames and nonzero alternating residuals.

The integration review also checks separate bit/complex arities, the changed
ordering `sigma<tau`, derived powers, legacy appendix references and the local
exceptional-repair sum. Previously published certificates, patches and the
pinned source remain unchanged. See the [review guide](complex-compression-review.md)
for verification results and the precise dependency boundary.

The next bottleneck is the bit network. More complex compression is worthwhile
chiefly when it develops methods transferable to new topologies or supplies
headroom for a stronger bit construction.
