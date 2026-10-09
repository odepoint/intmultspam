# Reusing auxiliary banks for general two-field cores

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

Status: generative bit-network construction and expanded exact controls.
This extends the earlier first/third-stage reuse to the general
[two-field compiler](rank-product-core.md). It does not establish a better
multiplication exponent or supply a competitive compressed side circuit.

Let the core have n labels, rational dimension d, binary factor size r, and
rank-one idempotents P_i. Suppose a label permutation π satisfies
P_i P_π(i) = P_π(i) P_i = 0. It need not preserve the central binary matrix
or its factors and need not be an involution.

Share the auxiliary bank of stage-one invocation (A,B) with stage-three
invocation (B,π(A)), matching local auxiliary indices. Both invocations
restore arbitrary auxiliary inputs before reuse. The matching acts only on
fixed tensor coordinates, so the same local scalar program is used on both
sides without permuting its ports.

There is one necessary frame adjustment to the raw edge compiler: raise
the stage-three initial J frame from B₀ ⊗ P_t to B₀ ⊗ I, where
B₀ = I − P_u ⊗ P_v. All its incoming frames lie below the old frame and
its next incident frames contain the new frame. The data-role predecessor
is exactly the old frame; auxiliary predecessors are zero. Thus this
moves an existing monotone increase earlier without changing its total rank.
Simply merging the unadjusted compiler's auxiliary roles is not justified.

The two auxiliary boundary frames after this adjustment are

- E = I ⊗ P_A ⊗ P_B;
- H = (I − P_B ⊗ P_π(A)) ⊗ I.

Mutual annihilation gives EH = HE = E. For nested idempotents, rank(H−E)
equals rank(H)−rank(E); orthogonal projections or a common symmetric form
are unnecessary. The new join replaces the old E→I terminal segment and
0→H source segment, reducing rank by exactly m=d³. All other segments and
data endpoints retain their rank sums. This establishes

```
N = n³, m = d³, L = 3 n² r d
W = 2 n³ + 2 n² (S+r)
s = Wm − N + 2L
Δ = N − 2L.
```

Here S is the side-role count of a certified invocation. For the raw
compiler S is its ordered side-edge count. Applying the same ledger to
an unconstructed compressed side circuit is only a budget calculation;
its frames, restoration, and invocation boundaries must also be proved.

An orthogonal matching exists for the full single-intersection subset
family whenever the relation has positive degree: the bipartite double
cover is a regular graph with equal parts, so Hall's condition follows
by counting incident edges. A fixed deterministic matching algorithm is a
finite generative specification, not an assertion that we expanded the
large matching. For the binary cube, XOR with a fixed word of weight q is
an explicit orthogonal matching.

At target bit saving 1.6 × 10⁻⁷, the seven-subset h=28 family allows
about 6.62 side roles per label; the dimension-32 cube allows about 2.31.
These are hypothetical loss-preserving budgets. Existing tested side
circuits remain far too large. The cube allowance is now above the
simple 2n lower bound for a cancellation-free addition DAG with n distinct
nontrivial outputs and the c+q embedding. That observation only removes
one elementary exclusion; it does not supply a circuit.

Reproduce with `python3 scripts/audit_shared_core.py`. The certificate
includes exact all-role scalar, endpoint, and every-edge rank checks for
small controls, including a noninvolutive matching that does not preserve
the central matrix and an oblique-projector example. No large positive
network is expanded in this audit. The retained conditional κ is 2⁻³¹.
