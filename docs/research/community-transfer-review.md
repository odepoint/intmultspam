# Maintainer review: batched transfer and semantic guard

Historical first pass. The remaining selected-instance and analytic gates
listed here are addressed by the [final audit](community-final-audit.md).

Review date: 2026-10-08. Candidate pinned to PR #39 at
`70ae24129649f6d6d4ec6360962a80c3c42a38f1`; integration `fd8c563`.
This is a bounded mathematical review by the project's Codex assistant,
not independent external peer review or a formal proof. The prior executable
replay is recorded separately in `community-integration-validation.json`.

## Verdict and scope

The generic projector batching lemma, its mixed-width moment recurrence and
row-padding extension are supported by the written argument, conditional on
the retained elementary-stream and fixed-tape interfaces. The semantic guard's
larger-child induction also checks algebraically under its stated exact
completed-child contract and paid scalar charge.

This does not yet accept the selected >2^-15 network or multiplication bound.
The selected partial-swap block profiles require their own controlled-basis
proof; the generic shear lemma cannot establish those profiles by rank alone.
The bulk resampling, arbitrary-coordinate routing, analytic recovery and
complete integration of those interfaces remain under review.

## Generic projector batching

Sources: `notes/projector-batching.tex`, `notes/batched-algorithms.tex`, and
upstream `build/sections/04-swap.tex`, lower-triangular factorization and
power-width interchange proofs.

For a rational idempotent P of rank a with m/2<a<m, let r=m-a. A rational
similarity can make the first-r-row/last-r-column corner nonsingular: pair
those coordinates into rank-one 2-by-2 blocks and put identity in the middle.
All rank-a rational idempotents are similar. Each corner determinant is
therefore a nonzero rational function on GL_m. Finitely many requirements
can hold together, because clearing denominators gives a nonzero polynomial
over an infinite field. Enumerating integer invertible matrices is effective;
the nonzero polynomial cannot vanish on every integer tuple either. The
prime is chosen after these fixed matrices and factors are constructed.

With I-P=UV, VU=I_r, the invertible corner is -U_L V_R. Eliminating it leaves
middle Schur block

    I-U_M V_M - (-U_M V_R)(-V_R^-1 U_L^-1)(-U_L V_M) = I.

The upstream top-row/rightmost-pivot order consumes the corner columns first,
then this ordered middle identity. Its width is t=m-2r=2a-m, strictly between
zero and m. Thus it is an actual contiguous ordered block, not merely a
rank count or an arbitrary permutation of t pivots.

For this block the chronological operations D+=H, swap(H,D), D=H-D return
(H_old+D_old,D_old). The two arithmetic passes act separately modulo q^b
on each field; they do not add the concatenated integer with cross-field
carries. There are a fixed number of fields. Controls have width b and
precede their targets, as required by upstream `lem:ordered-affine-streams`.
The single recursive swap has width tb. Nonselected pivots retain their paid
singleton calls. Full-rank edges cannot silently become same-width children.

At tau=1 batching preserves sum(t_i)/(Wm); below one it changes the recursive
moment. This explains how it can cross a singleton-call ceiling without
claiming a larger rank deficit.

## Mixed widths, logical volume and tape cost

Sources: `notes/batched-bit-rows.tex` and upstream
`build/sections/04-swap.tex`, fixed-tape depth-first schedule.

For a fixed list 1<=t_i<m and a child operating on exactly V/W, the normalized
recurrence is

    F(e) <= (1/W) sum_i F(t_i floor(e/m)) + C.

If Psi(tau)=(1/W)sum_i(t_i/m)^tau<1 and 0<tau<1, choose a constant A covering
the finite base cases and C/(1-Psi(tau)). Strong induction then proves
F(e)<=A e^tau. This requires both the claimed child list and the actual 1/W
logical volume. A histogram detached from the physical calls is insufficient.

The maximum-child depth D(e) is monotone and O(log e), since t_max/m<1 is
fixed. Rows divisible by W^D(e) therefore support every unequal child path.
The fewer than m high remainder digits can be exchanged and gathered with a
fixed number of elementary digit moves; the other digits remain complete
spectators. No per-level padding factor is introduced.

For arbitrary rows, borrowing rho=O(log e) digits from each target supplies
q^(2rho)>=W^D(e). Padding that complete row range once to its next required
multiple costs a factor below two. The completed interchange fixes row
indices, so added zero rows may be removed afterward. All remaining target
ranges stay present in every descendant. Therefore their exponential volume
absorbs polynomial descriptor work, just as in the retained proof.

The scheduler parks inactive parent streams only at the stack top. A fixed
number of child calls costs O(V) total push/pop overhead per node; its
possibly enormous constant is independent of input length. The mixed widths
do not require additional tape heads or scans through parked ancestors.
This review accepts that extension conditional on the retained stream
primitives; it is not a new verification of all upstream tape lemmas.

## Larger-child semantic guard

Sources: `references/semantic-bulk/pr23/semantic-bulk-17-note.tex`, section
“Linear semantic precision for this actual circuit”, and
`references/semantic-bulk/rad20/reports/downstream-semantic-child-guard.md`.

A completed u-axis forward/inverse phase child has Gaussian-dyadic entries
with denominator dividing 2^u and absolute row sum at most 2^u. Address
permutations and unit phase/sign wrappers preserve those bounds. Thus a
completed child adds at most u to denominator and magnitude exponents,
regardless of its temporary internal excess. All arithmetic remains on the
same fine grid: there is no uncharged rounding or representation rewrite.

For mixed-width children, the PR23 adaptation correctly replaces the earlier
single-width recurrence by

    A(e) <= A(r floor(e/m)) + s floor(e/m) + E,   r<m.

Here s is the sum of all child widths in slot units, and E must cover the
actual scalar gates, wrappers and remainders. Let B=s+E. With f=floor(e/m)>=1,

    2B*r*f + s*f + E <= 2B*m*f <= 2B*e

follows from 2B(m-r)>=s+E. The leaf bound 8e is covered when B>=4.
For disjoint root pieces the widths sum to at most d; adding the retained
outer contribution gives (2B+18)d. C1=1 is therefore a valid conditional
induction bound. It does not justify using a stale E from a smaller circuit:
the selected copied-center scalar charge must still be tied to its actual
schedule, including copies and corrections.

## Remaining gates

1. Validate the selected partial-swap and fixed/generic basis family against
   every physical edge, ordered pivot and copied-center occurrence.
2. Finish the exact completed complex operator and literal scalar-charge audit
   for the selected graph, rather than substituting a prior graph's constants.
3. Audit the arbitrary-source router and bulk resampling's locality, inverse,
   precision, periodic boundaries, sequential factor traffic and row reserves.
4. Connect the reviewed interfaces to every final assembly inequality and
   constructive eventual threshold before promoting a stronger release claim.

Original construction credits remain with icekylinx (batching and mixed-width
transfer), RaD/hipotures (semantic completed-child precision), Zhihao Chen
(larger-child compatibility and composition), and their cited predecessors.
This review contributes an assessment, not authorship of those constructions.
