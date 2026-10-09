# Stronger screens and the exhaustive balanced-Fano diagnostic

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

**No new kappa; the integrated conditional witness remains 2^-31.** Two
external research-agent assessments supplied by the user prompted this pass.
We checked the stronger rejection arguments, certified a fractional routing
of the clean Fano graph, and exhausted the specified balanced local model.
The results support making the [two-field core](rank-product-core.md) the
main constructive track rather than extending this small Fano completion.

## 1. Characteristic-zero coding is already enough to reject a topology

Fix an XOR permutation circuit, its actual permutation rho, and its graph of
common-frame gates and physical wire segments. Suppose the same gate
incidences admit rational linear local operations whose global matrix C is
monomial with that same rho: C sends input w to output rho(w) with a nonzero
coefficient c_w. The local rational operations need not be the original XOR
gates interpreted as additions. Then every rational frame assignment obeying
the endpoint identities has s>=Wm.

To prove this, let D_in and D_out be the block-diagonal matrices of source
and sink frames. The endpoint discrepancy is

    D_out (C tensor I_m) - (C tensor I_m) D_in.

After permuting output blocks, this has diagonal blocks c_w I_m, hence rank
Wm. Telescope the discrepancy through the circuit. At a gate, the local
scalar matrix commutes with the common frame on all its ports. Only edge
changes remain. For edge e the corresponding term is

    (b_e a_e^T) tensor (M_head(e)-M_tail(e)),

where a_e describes upstream scalar dependence and b_e downstream scalar
influence. The scalar outer product has rank at most one, so the term's
rank is at most the rank of that edge difference. Subadditivity gives

    Wm <= sum_e rank_Q(M_head(e)-M_tail(e)) = s.

The argument also holds for scalar realizations over a characteristic-zero
extension field: ranks of rational matrices do not change on extending the
field. The implementation checks rational witnesses only.

This strictly broadens the directed integral routing rejection mechanism:
a routing is itself such a realization, but rational linear coding may
succeed without that routing. Finding an exact monomial realization is a
rejection certificate. Failing to find one is not evidence of separation.

`rank_obstructions.py` checks supplied local matrices against the actual
binary circuit's permutation. An exact signed-swap control uses free,
nonsymmetric source/gate frames and verifies the entire telescoping matrix
identity, including every edge contribution. The written argument, rather
than that finite control, supplies the dimension-independent theorem.

## 2. Undirected fractional paths give another necessary screen

Write r_e=rank_Q(M_head(e)-M_tail(e)). Along any undirected path connecting
an input to its assigned output, signed matrix differences telescope to I_m.
Rank is unaffected by reversing an edge, so the path has total r-length
at least m. For any nonnegative rational path flow with physical edge loads
at most one, and total routed demand F,

    m F <= sum_e r_e load(e) <= s.

In particular, a unit fractional routing of all W demands rejects every
frame assignment, even if no directed or integral routing exists.
An exact feasible witness of rate R for each demand gives

    s/(Wm) >= R,  a <= -log(R)/log(m).

Total-flow and common-rate optima are different optimization objectives and
should not be interchanged. On our all-role physical graphs, input/output
terminals are leaves, so each individual rate is automatically at most one.
The maximum total flow F_* then also gives s/(Wm)>=F_*/W. Its usual distance
dual minimizes sum_e length(e), subject to nonnegative lengths and every
own-pair path having length at least one. Frame ranks divided by m form a
feasible dual; a cheap arbitrary dual metric need not be realizable by frames.

For a clean graph without leaf terminals or without all-role demands, extra
rate caps can change the LP and its dual. The three-demand Fano check below
asserts unit feasibility only, not an optimal total-flow value.

Discovery used an exact rational feasible solution from Z3. Reproduction
checks six rational path weights, connectivity in either edge direction,
all demand rates, and every shared edge load with the standard library.
No approximate LP solution or solver infeasibility status is treated as a
certificate. A general LP optimizer is not added by this pass.

## 3. The clean Fano seed fractionally routes at unit rate

The [previous clean graph](fano-completion-audit.md) has a directed routing
obstruction. Treat its 20 edges as undirected. Each of the following paths
has weight one half:

| Demand | Path |
| --- | --- |
| a to ta | a,u1,u3,u6,u8,ta |
| a to ta | a,tc,u7,u5,u4,ta |
| b to tb | b,u2,u4,u5,u7,u9,u10,tb |
| b to tb | b,u2,u4,ta,u8,u9,u10,tb |
| c to tc | c,u6,u3,u1,a,tc |
| c to tc | c,u6,u8,u9,u7,tc |

Every demand receives one unit, and no undirected edge carries more than
one unit. This eliminates the inference that the clean directed obstruction
alone is a useful rational rank obstruction.

**It does not prove that every completion fails.** A completion adds auxiliary
demands; their input values are independent and must also reach assigned
outputs. A feasible flow for the original three demands says nothing by
itself about whether all those additional demands can be accommodated.
This is a necessary correction to the stronger conclusion suggested in one
external assessment. We resolve the proposed balanced model separately.

## 4. The balanced 10-role model has no valid scalar completion

Balance the original DAG by adding auxiliary input stubs at branches and
auxiliary output stubs at merges, counting the original terminal stubs.
This produces ten independent input roles and fourteen two-port vertices.
One-port vertices carry identity. Assign physical output ports in edge-list
order; arbitrary local GL(2,F2) operations already include swapping them.

The chronological role pairs are

    (0,3), (1,4), (2,5), (0,1), (4,2), (0,6), (4,7),
    (0,4), (5,6), (0,8), (5,9), (0,5), (7,9), (3,8).

The original sources are roles 0,1,2. Their required terminal roles are
7,0,3 respectively. The other seven inputs may end in any permutation of
the remaining outputs. The graph builder derives this data from the retained
20-edge Fano graph; it is not an unrelated hand-picked interaction sequence.

Each two-port invertible binary operation has six possibilities. We exhaust
existence over all 6^14=78,364,164,096 full assignments by meeting in the middle:

1. Enumerate every seven-gate prefix A.
2. Enumerate every inverse seven-gate suffix B^{-1}.
3. A completion BA=P exists exactly when the columns of A are the columns
   of B^{-1} permuted according to P.
4. Keep the three prescribed source/output columns labeled, and sort only
   the other seven columns to leave the auxiliary permutation free.

All matrices are invertible, so their columns are distinct. Any matching key
recovers a unique column matching for those two matrices and a valid complete
word. Keeping one prefix per key is sufficient for **existence**; we do not
claim to enumerate all matching words or permutations.

Both halves contain 279,936 assignments. The prefix has 258,156 distinct
keys. There is **no matching suffix key**. This is a complete negative
result for the specified local model, reproduced by enumeration without an
SMT solver. Stream hashes record both complete enumerations. Independent
small dense-matrix brute-force tests check the matching algorithm and its
handling of prescribed terminals and free auxiliary outputs.

This closes this balanced model before fractional routing or matrix synthesis
on a complete candidate is needed. It does not exclude larger local blocks,
different graphs, different terminal obligations, or all Fano completions.

## 5. The new completion paper is relevant but not an immediate candidate

Zhang, Li, and Li's [October 7 preprint](https://arxiv.org/abs/2610.09367)
states an undirected coding-versus-routing separation. Section III-B builds
an arbitrary-workspace shear by a commutator and obtains the opposite shear
by inverse transposition, preserving interacting register pairs. Section
III-C budgets completion against a quantitatively amplified coding advantage.
The construction is valid over the integers. Therefore its signed-permutation
circuit, with that same underlying permutation, is excluded **as-is** by the
characteristic-zero obstruction above. This is an inference from its stated
integer identity, not a criticism of its different routing objective.

We checked the abstract and the relevant construction sections. We have not
built its Lean development or independently verified the paper's full result.
Its completion discipline may be useful for a characteristic-dependent seed;
its circuit is not automatically a rational rank-deficit certificate.

The [characteristic-dependent rank-inequality paper](https://arxiv.org/abs/1903.11587)
suggested by the external agent is another possible source of seeds. No
conversion from those networks into our full finite contract is supplied here.

## 6. Effect on the research plan

The main constructive target is a complete **characteristic-dependent**
permutation with a rational rank certificate. The core compiler already
makes the use of different fields explicit and now allows nonsymmetric
rational fitting matrices. It avoids inventing a cleanup procedure for each
new core. Its broadening does not reopen the previously excluded fixed-boundary,
grouped-central-gate optimization region.

Keep undirected fractional routing and characteristic-zero realizations as
cheap sufficient rejection screens for other topologies. An LP gap alone is
not a promise of useful frames. Kernel-first synthesis is a reasonable later
experiment on a surviving topology: fixed rational edge kernels turn the
frame and endpoint constraints into linear equations, but finding good kernel
patterns and paying their full rank budget remain open tasks.

The external suggestion about simultaneous triangularization has not been
implemented as a screen in this pass. In particular, the non-self-adjoint
control in the core audit is a negative example; its admission by the compiler
is not presented as evidence of a deficit. Improving Gaussian resampling
also remains an unproved alternative route, rather than a supplied saving.

## Reproduction

Run `python3 scripts/audit_stronger_screens.py` and
`python3 -m unittest discover -s tests -p test_stronger_screens.py -v`.
The audit also runs with `python3 -S`. The
[certificate](../../certificates/stronger-rank-screens.json) records the exact
flow, derived balanced graph, exhaustive half-enumeration hashes, signed lift,
telescoping control, and source hashes. Previous proof artifacts and research
certificates remain unchanged.
