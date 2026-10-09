# Maintainer audit of the PR39 community witness

Date: 2026-10-08. Reviewed by the project's Codex assistant for Douglas
Colkitt. Submitted candidate: `70ae24129649f6d6d4ec6360962a80c3c42a38f1`.
Integration code reviewed: `1b878ccd8132d9fefdc95a51f5eeceef0761cb9c`.
This is a maintainer mathematical assessment, not independent human peer
review or formal verification. Historical contributor files called
“independent review” do not change that distinction.

## Verdict

**Accept the submitted witness as a conditional research result:**

\[
T(n)=O\bigl(n(\log n)^{1-\kappa}\bigr),\qquad
\kappa=\frac{971668963}{25000000000000}
      =3.886675852\times10^{-5}>2^{-15}.
\]

The written extensions reviewed below support their required interfaces;
no unresolved additional construction or inequality was identified that
blocks this particular witness. This conclusion uses the general arguments,
physical call accounting and exact certificates together. Passing the test
suite alone would not support it.

The original OpenAI #109 framework, including its retained elementary stream,
native interchange and exact-recovery machinery, remains assumed. This audit
does not re-prove that manuscript or supply a complete executable or formalized
multitape multiplier. Constants and eventual thresholds are enormous; this
is an exponent-saving comparison, not a practical speedup or a priority claim.

The independently preserved public checkpoint remains `2^-30` at `1a74950`.
At completion this audit accepted the stronger integration candidate without
changing main. The subsequent [community release](../releases/community-kappa-15.md)
adopts the audited witness. PR40 and subsequent submissions are outside
this pinned review.

## Finite calls and the two recursive interfaces

The [first transfer review](community-transfer-review.md) establishes the
generic contiguous Schur block, mixed-width recurrence, complete-row padding
and semantic precision extension. Its then-outstanding selected-instance
obligations are discharged here.

For the partial-swap compiler, let P=L Pi R, C=RL, Qx=Pi Pi^t and
Qy=Pi^t Pi. Idempotence gives Pi C Pi=Pi. With K=Qy C-C Qx,
conjugation by diag(L,R^-1) followed by the lower block shear K yields
the stated cross-bank pivot swaps. In particular the lower-left block
reduces to Qy C Qx=Pi^t. This checks the nonsymmetric case; symmetry or
orthogonality in physical coordinates is not needed. Increasing contiguous
pivot runs give actual block interchanges, not uncharged pivot gathering.

The selected (23,25) construction has m=575, W=188181929,
N=4073300 and L=2226400. Its complete rank mass is
Wm-N+L=108202762275. The endpoint corrections remain N paid rank-one
calls. The largest child is 529, strictly below 575.

The [selected geometry proof](../../research/copied-fixed-reversed/geometry-proof.txt)
uses one family T_M(L23 tensor (I25+J25)). The exact physical first/last
corner contractions preserve the fixed second-axis profiles up to nonzero
diagonal scales. The 2300 middle triples supply nonzero modular witnesses
for every required prefix minor, at an admissible prime. Universal zeros
come from the separate all-weight incidence rank-cut identities, not from
observed modular zeros. The two runs 21 and 17 and the middle 481 are
disjoint physical intervals. All remaining data pivots are charged as
singletons.

For each first-axis source line the GL23 action can realize the witness
rank-one projector. Each required minor is therefore a nonzero rational
function on the same irreducible GL23 family. The finite product argument
supplies a single rational basis for all occurrences, including the new
center complements. Rational enumeration makes the choice constructive;
the address prime is chosen afterward to avoid the finite exceptional set.
It is not necessary to select a different basis at each gate.

The fixed h25 profiler reconstructs the actual original-envelope transition
multiset and oriented matching. A transition is a nested diagonal-mask
difference plus a correction of rank at most four. The
[bounded-minor argument](../../research/copied-fixed-reversed/review/fixed25-copied-crt-audit.txt)
uses each matrix's actual denominator; its uniform denominator upper bound
is not incorrectly treated as a common multiple. The 141-bit product of five
primes exceeds the 118-bit integer-minor bound, and all denominators are
invertible. Thus every northeast rational rank is the maximum of the five
modular ranks. Mixed differences of these ranks recover ordered pivots.
Taking a union of modular pivot sets would be invalid. The complete producer
replay covers all 96273 profiled transitions.

The copied-center schedule reproduces both former operands for arbitrary
dirty values: a paid transformed copy supplies the read-only scatter,
while the retained original goes to its cleanup frame. In the reverse
orientation the order and inverse phase are changed accordingly. Actual
terminal output-use vertices have no later producer consumers. This
restriction is essential and is present in the carrier construction.
Exactly 25 width-25 identity calls become width-one complement calls in
the fixed profile; the width-24 copied transforms and their actual profiles
remain. Copies have volume V/W and are processed sequentially. No new
independent row dimension or free cleanup operation is asserted.

## Complex residuals, precision and row stock

The general binary residual compiler in
[endpoint-gauge-complex.tex](../../notes/endpoint-gauge-complex.tex)
also covers alternating forms. For a nonsingular Gram matrix G the
mod-four quadratic phase q has polarization 2z^t G^-1 w. Completing
the square yields its scaled Walsh kernel. Odd one-dimensional and
alternating two-dimensional Gauss blocks show that S_q((1-i)/2)^r
is a fourth root of unity. Thus one rank-r child, paid binary adapters,
diagonal phases and a scalar unit suffice. This avoids the invalid
assumption that every nondegenerate binary space has an orthonormal basis.

For the selected h28 mixed-center circuit, the coefficient identity
uses denominator 6-2*19=-32, hence Gaussian-dyadic scalar arithmetic.
Its two-stage endpoint gives A=-Fy and B=F T^-2 x+Ey. Applying T^-1
to a paid copy of A cancels Ey. The weight-nine endpoint is normalized
by the stated Z and fourth-root phases. The auxiliary endpoint remains
C_I on every arbitrary input role. The actual complete child list has
m=784, W=537696432, rank mass s=421548223824 and largest child 756.

The literal grouped scalar upper count is G=4793351472, including copied
centers and endpoint additions. With E=64(W+m+G+1)^3, the stricter charge
2GW^2+8s+4W+4+32m is below E. This pays residual phases and tails, rather
than using role count as a surrogate for scalar gate count.

A completed child on u axes has denominator dividing 2^u and absolute
row sum at most 2^u. With B=s+E, the active-child recurrence
A(e)<=A(756 floor(e/784))+s floor(e/784)+E gives A(e)<=2Be.
Unfinished children stay local and other streams are parked. The proof
keeps one fixed fine grid throughout; it does not round on child return.
The additional outer charge fits C0=32mB^2 and C1=1.

The simultaneous row stock is the product of bit and complex depth stocks.
The halving degrees and wire bitlengths are (9,28) and (20,30), giving
coefficient 852. The checked inequality 2000>(51/25)*852 suffices for
p^2000. A physically preceding prefix is transformed elementarily once,
then its complete row count is padded once by a factor below two.
Descendants inherit it; nested bit adapters restore their temporary stock.
The completed all-role operation restores appended zero rows before removal.
No row field is borrowed from a suffix without paying for its placement.

## Arbitrary routing and balanced FFT layout

The [router](../../references/semantic-bulk/rad20/reports/compact-arbitrary-source-routing.md)
uses masked four-update identities. For a good address each completed
identity changes only its selected target bits; sources may lie in guard
fields but are read only after those guards have been restored. Loading
and unloading the source mask therefore uses the same source values.
The two parities of the dirty control digit differ by exactly the source
bit. Packed additions require the stated digit and segment guard tests.

Each actual rotation is a bijection, and the ideal shear preserves the
good set. Equality there implies the actual permutation also preserves
the bad set. Repair keys T S^-1 at current bad addresses consequently
correct exactly the exceptional records. Their density bound pays the
radix work and every extraction/reinsertion scan. Control arithmetic is
amortized over complete enlarged records, not charged as constant-time
random access.

Three disjoint reservoirs partition each matching into classes with an
untouched reservoir. Original paid chunk interchanges place and restore
it. Two matchings implement a coordinate permutation. Short coefficient
records borrow a complete untouched spectator through paid interchanges;
the small-width fallback requires epsilon>a and satisfies it. This gives
O(V p^tau polylog p) with its explicit polynomial setup term.

The [balanced layout](../../references/semantic-bulk/rad20/reports/review-balanced-transform.md)
partitions common named FFT levels into groups with widths in [K,2K).
Only one extra top position per long axis is treated elementarily.
Within a round all supplied widths are equal; complete spectators and
twiddle significance are preserved. The forward and inverse use the
same named levels in opposite chronology. Applying the paid arbitrary
router to the complete positional map and its inverse replaces the old
per-group transpose charge. The prefix saving is therefore 1-epsilon,
while epsilon(1+c)<1 still controls geometric feasibility. It is not
legitimate to obtain this improvement by substituting parameters into
the old prefix estimate.

## Gaussian inverse and bulk tape schedule

The chirped-correlation identity and its shifted input enclosure retain
O(p) work precision. Correlations are on polynomial-length blocks using
an unconditional conventional integer multiplier. The old Neumann-count
corollary assumes alpha^2 theta>=1; it is not used to justify the new
near-one-dimensional assembly, where that condition need not hold.
The replacement is the phase-cell inverse below.

The sharper nearest-neighbor estimate gives
||E||<exp(-2 pi u theta)+5 exp(-2 pi u), u=alpha^2.
For u>=ceil(log2(8p)) and theta>1/(4p), its gap is at least 1/(4p).
The truncated, rounded matrix H uses downward weights but exact rational
within-cell similarity ratios. Their possible upward error is bounded
explicitly; it is not ignored. H has diagonal one, gap at least 1/(8p),
and inverse norm at most 8p.

Within a phase cell, the inverse is a diagonal similarity of the symmetric
Toeplitz inverse. The Gohberg--Semencul factorization reduces it to four
short convolutions. Eliminating interiors preserves diagonal dominance
and row norm; the ordered Schur system has O(w) bandwidth and O(sw/d)
vertices. Triangular solve errors are bounded through residuals and
polynomial inverse norms, rather than by multiplying rowwise error
estimates along the entire line. Exact rational setup can be polynomial
in s and p and is reused; online factors have O(p) bits.

For bulk windows, principal restrictions are taken from the same fixed
global H. If a core is Jw from an artificial endpoint, the first J
Neumann powers agree there, giving error at most 32p*2^(-J/(16p)).
With J=512p^2, A=4096p^3 and L=2^ceil(8 log2 p), this is below 2^-16p.
The complement condition s>2(L+2A+2w) prevents hidden cyclic wrap edges.
Original physical seam cuts remain cell boundaries, preserving the
original rounded coefficients.

Near-one source halos fit into L slots. Target halo volume is bounded by
T(1+2A/L)^d=O(T). Only the currently moved short field is temporarily
dyadically padded; padding all d fields to 2L would be invalid. Tensor
contraction bounds make core errors add in the supremum norm. Cropping
each completed axis does not require refreshing other halo coordinates.

The [tape construction](../../references/semantic-bulk/rad20/reports/bulk-resampling-tape-transfer.md)
uses monotone overlapping windows, alternating tail buffers, and sequential
factor pages in coarse-coordinate order. Complete inner microboxes amortize
page copying and descriptor work. Only short inner fields move at each axis;
the large coarse order remains fixed. The resulting full cost is

    O(Tp [p^tau polylog p + d polylog p + d p^delta
          + w^2 p^delta + d w^2 p^delta/L]) + n^o(1).

All these terms occur in the final margins or the artificial-boundary
slack. Normalization includes d(2u+ceil(log2(32p))+1); epsilon+r<1
is retained. The proof does not silently reuse the old normalization.

Prime supply uses the interval theorem in Baker, Harman and Pintz,
[*The Difference Between Consecutive Primes, II*, Theorem 1](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/BakerHarmanPintz.pdf).
The primary statement supplies a prime in [x-x^(21/40),x] for sufficiently
large x. Packing d disjoint intervals is ensured eventually by
12d^2<x^(19/40). Since log x=Theta(p^(1-epsilon)) and epsilon<1 is fixed,
deterministic search and all fixed-polynomial axis/window setup are n^o(1).
This replaces the old prime restriction; it is an actual new input.

## Final accounting and independent numerical cross-check

The selected savings are a=3886826921/10^14 and b=717/10^7. With
h=10^-12, beta=1/20, q=a(1-2h), c=q+h/4 and
epsilon=(1-h)/(1+q), set G=epsilon*q, r=(G+1-epsilon)/2 and delta=h/8.
The complex stopped-leaf saving (1-beta)b exceeds a. The seven final
savings are

    1-epsilon, a, G, a,
    min(1-epsilon-delta,r-delta), 1-epsilon-delta, epsilon.

Their minimum is G. The identities 1-epsilon-G=h,
1-epsilon-r=h/2, and 1-epsilon(1+c)=h-epsilon*h/4 give the required
strict absorption, normalization and geometric separation. The 47
certificate constraints include the scalar charge, product row stock,
compact reservations, short records and artificial-boundary cost.
The all-interval cutoff argument uses monotonicity and exponential
versus affine growth; six sampled checkpoints alone would be insufficient.
Fixed basis/table, prime and logarithm-absorption thresholds remain
additional eventual thresholds, not practical input-size promises.

An additional [arithmetic check](../../scripts/audit_community_candidate.py)
imports no candidate producer or checker. It uses 80-term rational logarithm
bounds, 12-term exponential bounds and outward rounding at 10^-30. From
the submitted complete child lists it certifies strict moment gaps greater
than 2.32517e-15 for the bit primitive and
8.52696e-9 for the complex primitive. It reconstructs the
seven margins and obtains the identical exact final absorption gap,
approximately 6.2496798783e-15. Its
[receipt](community-audit-arithmetic.json) pins the certificate bytes.
An independently enclosed lower moment also exceeds one at the next bit
saving on the 10^-14 grid, providing a failing control for the same profile.
This independently checks arithmetic; it does not replace the physical
and analytic arguments above.

## Reproduction and audit fixes

The earlier full replay passed 218 tests, 20 upstream patch checks and
certificate regeneration in Ubuntu 24.04 Docker with GCC 13.3/Python 3.12.
The [GitHub Linux matrix](https://github.com/CrocSwap/integer-mult-bounds/actions/runs/37785896317)
also passed on Python 3.11, 3.13 and 3.14. The self-contained C++ header
fix changes no scientific field.

This pass found a packaging omission: 20 files already listed in the
vendored RaD manifest were absent, including the balanced-layout proof.
They were restored verbatim from pinned PR34 commit
`7fecbe3651e095fb0f450756afdeefd2a9ee80a2`. All 32 manifest entries now
match their pre-existing SHA256 values. No upstream mathematical source,
candidate certificate or claimed exponent was edited. Historical links
to campaign runs outside this selected archive are not newly executed
evidence.

Reproduce the additional arithmetic/source check with:

```sh
python3 scripts/audit_community_candidate.py
```

`make community-audit-check` also checks exact agreement with the saved
receipt and is included in `make verify`. The 17 focused algebra, phase,
batching and selected-witness tests were rerun during this final pass and
passed. The full Linux suite above was not needlessly repeated for the
unchanged scientific sources.

The construction credits remain with the contributors recorded in
[CONTRIBUTORS.md](../../CONTRIBUTORS.md), NOTICE and the individual source
files. In particular this assessment does not reassign the finite batching,
partial swaps, semantic guard, bulk resampling, copied centers, reversed
corners or fixed-profile improvements to the maintainer.
