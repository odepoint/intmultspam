# Complete compressed-side compiler for positive-definite labels

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa.** The retained integrated conditional witness remains 2^-31.
This extends the explicit two-field compiler to arbitrary cancellation-free
side sum DAGs with positive-definite rational label geometry. It supplies
the missing complete-circuit check for testing compression of the signed
sparse and cube cores; it does not supply a competitive large side circuit.

## Contract and scalar completion

Let the rational line labels have the ordinary dot product, with nonzero
norms. Let the binary central matrix C have diagonal one and off-diagonal
ones only between orthogonal labels, and choose a binary factor C=UV of
size r. The side DAG must implement I+C exactly, with disjoint supports at
every addition. Each of its n outputs is nonempty in this adapter. Identical
outputs are permitted, and input fanout and unused input columns are handled.

The retained gather/fanout embedding uses S=c+n side roles for c additions.
Its invertible map L, source copy V_s and output injection J satisfy
J L V_s=I+C. With the central gather G and scatter R, use

    L, J, L^-1, R, V_s, G, R, L, J, L^-1, G, V_s.

Over F2 this maps y to y+x, leaves x fixed, and restores every arbitrary
side and central input. The inverse schedule reverses the actual elementary
updates; it is not a cleanup obtained by a new elimination circuit.
The audit tracks an independent formal bit for every invocation role.

## Physical frames in both directions

Let E_v be the ordinary rational projection onto the span of the source
labels that reach DAG node v. The positive-definite dot product makes
every such span and every orthogonal complement nondegenerate. In a forward
middle mixer, labels grow along the DAG from the source lines through E_v
to the complements of the target lines. The last inclusion holds because
every path joins an allowed orthogonal source/target pair.

For the reverse middle mixer use I-E_v. Forward inclusions reverse under
orthogonal complementation, so the reversed physical edges are again
increasing. At an output, the target line lies in I-E_v; at an input, the
last frame is the complement of that input's line. Source spans reused
unchanged in this reversed schedule would be incorrect.

The local verifier includes each physical role's initial zero segment,
source/target line transitions, every gate incidence and final identity
segment. It checks both projection inclusions and the exact equality
rank(B-A)=rank(B)-rank(A) on every increasing transition.

## Tensor stages and sharing

Use the existing stage decomposition A=B orthogonal-sum P, with future line Q.
Write D0=B tensor I, D1=A tensor I, and
D(F)=D0+P tensor F, suppressing Q. The twelve forward frame choices are

    D0,D0,D0,D0,D(P_t),D1,D0,D(E_v),D(I-P_t),D1,D1,D1.

For the inverse invocation, with logical banks exchanged, the choices are

    D0,D0,D0,D(P_t),D(I-E_v),D1,D0,D(I-P_t),D1,D1,D1,D1.

Central gates retain all data and central ports, including zero coefficients.
The only decreasing segments are the central returns; each loses d dimensions.
All side roles start at D0 and end at D1. Thus an orthogonal label matching
permits the same first/third-stage auxiliary sharing, including centers.
Unlike the raw eight-operation implementation, this schedule already has
the widened initial side frame needed at the sharing boundary.

Including all arbitrary inputs, negative source frames and terminal edges,
the complete shared network has

    N=n^3, m=d^3,
    W=2n^3+2n^2(S+r),
    Delta=n^3-6n^2 r d,
    s=Wm-Delta.

The unshared network replaces the coefficient 2 on the auxiliary term by 3.
The expanded controls independently reconstruct the scalar permutation,
all endpoint identities and every physical edge rank. They include an
asymmetric central matrix, a noninvolutive matching and genuine shared sums
with repeated line labels and identical output sums. These are nonpositive
controls for the implementation, not claimed positive-deficit examples.

## Bounded signed-vector experiment

Two deterministic strategies are evaluated: balanced output sum trees with
equal-support interning, and repeated extraction of the most frequent pair
of current disjoint sum terms before forming the output trees. The latter
uses lexicographic tie breaking. This is a heuristic construction, not an
optimality or impossibility claim.

| h | q | labels | balanced side roles | frequent-pair side roles |
|---|---|---|---|---|
| 4 | 2 | 12 | 33 | 30 |
| 5 | 2 | 20 | 97 | 70 |
| 4 | 4 | 8 | 22 | 20 |
| 5 | 4 | 40 | 110 | 100 |
| 6 | 4 | 120 | 1,600 | 1,080 |
| 8 | 8 | 128 | 1,764 | 1,200 |

Every coefficient and invocation input is checked for both strategies;
every physical side frame is additionally checked for the frequent-pair
candidate. All these small central matrices fail n>6rd. Their compression
ratios do not predict the large positive q=16,h=31 instance. The fast growth
of these direct sharing experiments is reason to seek a structured recursive
construction, not evidence that all large side circuits are impossible.

Run `python3 -S scripts/audit_positive_side.py` and
`python3 -m unittest discover -s tests -p test_positive_side_core.py -v`.
The certificate records complete control edge ranks, exact small ledgers,
deterministic DAG hashes and source hashes. No previous proof is modified.
