# Complex compression: integration and review guide

The conditional witness is **kappa = 2^-31**. The [combined patch](../../patches/complex-compression-31.patch)
applies directly to the original pinned at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`; do not apply any earlier patch first.
This is an author-side consistency audit, not independent mathematical review.

The [new note](../../artifacts/complex-compression-note.pdf) supplies the finite
construction and accounting. The complete patch embeds it together with the
retained compact-control proofs and earlier bit/Gaussian refinements. The
[preceding review guide](compact-control-review.md) still identifies the
retained movement, reservation, repair and uniform tape-time obligations.
Its h=25 complex construction and numerical witness are superseded here.

## New obligations

| Boundary | Supplied argument and checks | Review target |
| --- | --- | --- |
| Scalar correction | Weighted rectangles and disjoint-support sums; exact rational linear maps on independent dirty variables | Signs and half coefficients must hold over characteristic zero, in both directions |
| Binary phase frames | Coordinate enclosures with singleton exceptions; explicit orthonormal completion for intersection-two sums | Every used residual must be nondegenerate and, unless zero, nonalternating |
| Signed inverse stage | Reachable-output frames in the inverse mixer | Forward ancestor frames cannot be reused blindly in the reverse direction |
| Auxiliary sharing | Bijection `(A,B) -> (B,pi(A))`, nested join and a norm-one witness | Arbitrary-input restoration, compatible physical role indices, tensor endpoints |
| Kernel count | `s=W*m-2*N+2*L`, with the original central losses | New side transitions and bank joins must introduce no decrease |
| Precision | Explicit scalar count bounded by the retained additive node charge | Mixers, half scalings, kernel corrections and endpoints must all be charged |
| Layer recurrence | Separate complex constants and `sigma<tau`, hence `chi=tau` | Use the general exponent ordering; preserve complete reserved fields and uniform tape costs |
| Assembly | Exact parameters, seven strict margins and derived powers | All costs must be included, including reservations and local exceptional repair |

The construction retains the upstream normalized phase interface, stream model,
analytic estimates, resampling, prime selection, synthetic transforms and final
rounding. The repository does not independently prove that entire theorem.

## Exact integration

The patch changes the motif, layer and assembly sections and the headline:

- The motif contains the full new construction, separate-arity argument and
  `prop:compressed-complex-interface` at `h=26`.
- The layer uses `m=17576`, `W=7082222160000`, `s=124477130005280000`,
  while swaps retain the bit arity `125000`. It includes the explicit new
  scalar-operation guard charge. The three compact-control proof sources
  remain verbatim.
- The assembly uses `epsilon=199/1000`, `c=1`, `beta=1/100`,
  `zeta=1/1000`, `delta=1/10000`, `lambda=1-293/10^11`,
  `lambda'=1-29/10^10` and `C1=4961/1000`.

The minimum margin is `5771/10^13>2^-31`. Derived powers are

| Quantity | Power of p |
| --- | ---: |
| d and K | `199/1000` |
| ell | `801/1000` |
| Gaussian alpha | `1199/4000` |
| gamma | `1597/2000` |
| guard | `987239/1000000` |
| prime-interval ratio | `301/500` |

The stopping comparison is `e^100<d`; the dimension comparison is
`d^1000<=b^199`. The constants in `C0` are recomputed with the new network.
There is no residual use of the preceding h=25 constants in the active layer
or preceding numerical parameters in the assembly.

The current ceiling `kappa<a_b/5<2^-30` follows from `lambda'>tau` and
`epsilon<1/5`. It applies to the retained certified bit saving and Gaussian
constraint. It does not constrain all bit networks or multiplication methods.

## Reproduce and verification limits

```sh
make verify
make complex-note
```

The suite checks exact rational arithmetic and source integration, including
unique/resolved labels and retained appendix contracts. The finite-network
certificate enumerates 4,604,600 ordered disjoint-triple pairs. Small scalar
controls check complete local linear maps, not the full tensor-indexed machine.
General tensor composition and phase-frame transfer remain written proofs.

The independent patch and certificate can be regenerated without changing the
previously published outputs. Full manuscript compilation tests typesetting
and reference consistency, not mathematical truth. See the
[reproduction instructions](../reproducibility.md) for the disposable preview
and its three pdfTeX metadata compatibility edits.

Completed integration checks: **176 tests**, **18 patch-application checks**,
byte-for-byte regeneration of the new certificate and patch, and builds of
the standalone note and full patched manuscript. The standalone note builds
without warnings. The manuscript retains one minor overfull line in the
unchanged introductory paragraph; no unresolved references were reported.
All 68 pre-existing pinned-source, retained-proof, certificate and patch files
checked against the preceding commit are byte-identical.
