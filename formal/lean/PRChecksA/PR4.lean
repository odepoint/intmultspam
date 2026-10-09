import PRChecksA.Bit

/-!
# PR #4: retained-total complex layer, `κ = 591/10¹²`

Source: `certificates/retained-complex-layer.json` at PR head `8c225e6`, produced by
`scripts/retained_complex.py`; written chain in `docs/research/shared-retained-complex.md`
and the proposition `prop:shared-retained-complex-interface` of
`patches/retained-complex-31.patch` (lines 1011-1040).

Headline: `T(n) = O(n (log n)^(1-κ))`, `κ = 591/10¹² = 5.91e-10 > 2^-31` (bit-limited).

**Taken as given** (outputs of running `RetainedComplexCircuit(24)`, which imports PR #3's
`ComplexSideCircuit(24)`): `base_additions = 66518`, `new_ancestors = 120`,
`side_outputs = 24288` (with `zero_output_uses = two_output_uses = 12144`), and the role
count `R = 90950`; also the bit network's `R50`.

Section F checks the *preceding rectangle variant* that `notes/retained-complex-construction.tex`
(lines 165-202) and `notes/retained-complex-note.tex` (abstract) still describe: it is
internally consistent but it is not the construction in the certificate.  Its circuit counts
`123855`, `205956`, `27600` are taken as given.
-/

namespace PRChecksA.PR4

open PRChecksA Real

/-! ## A. Circuit outputs (taken as given) and their bookkeeping -/

def base_additions : ℕ := 66518
def new_ancestors : ℕ := 120
def side_outputs : ℕ := 24288
def zero_output_uses : ℕ := 12144
def two_output_uses : ℕ := 12144
/-- `R_aux = C + q` -/
def R : ℕ := 90950

/-- doc lines 63-67: `C = 66518 + 120 = 66638`, `q = 24288 + h = 24312`, `R = C + q`;
the base outputs are PR #3's twelve pieces per target at `h = 24` -/
theorem circuit_bookkeeping :
    base_additions + new_ancestors = 66638 ∧ side_outputs + 24 = 24312 ∧
    R = (base_additions + new_ancestors) + (side_outputs + 24) ∧
    side_outputs = zero_output_uses + two_output_uses ∧ side_outputs = 12 * v 24 := by
  simp only [base_additions, new_ancestors, side_outputs, zero_output_uses, two_output_uses, R,
    v]
  norm_num [Nat.choose]

/-! ## B. Network counts, η, log bound and the exponent certificate -/

/-- local loss per invocation, `ℓ = (h-1)² + h` -/
def ell : ℕ := (24 - 1) ^ 2 + 24
/-- stage sharing: `W = 2N + 2v² R_aux` -/
def W4 : ℕ := 2 * N 24 + 2 * v 24 ^ 2 * R
/-- `L_loss = 3 v² ℓ` -/
def L4 : ℕ := 3 * v 24 ^ 2 * ell
/-- `D = 2N - 2 L_loss` -/
def D4 : ℕ := 2 * N 24 - 2 * L4
/-- `s = W m - D` -/
def s4 : ℕ := W4 * m 24 - D4

theorem counts :
    v 24 = 2024 ∧ m 24 = 13824 ∧ N 24 = 8291469824 ∧ ell = 553 ∧
    W4 = 761750114048 ∧ L4 = 6796219584 ∧ D4 = 2990500480 ∧ s4 = 10530430586099072 ∧
    L4 < N 24 := by
  simp only [W4, L4, D4, s4, ell, R, N, m, v]; norm_num [Nat.choose]

theorem s4_eq : (s4 : ℤ) = (W4 : ℤ) * m 24 - 2 * N 24 + 2 * L4 := by
  obtain ⟨-, hm, hN, -, hW, hL, -, hs, -⟩ := counts
  rw [hs, hW, hm, hN, hL]; norm_num

theorem eta : ((D4 : ℕ) : ℚ) / (W4 * m 24) = 365 / 1285272576 := by
  obtain ⟨-, hm, -, -, hW, -, hD, -, -⟩ := counts
  rw [hD, hW, hm]; norm_num

/-- `log m < 477/50` (`log_upper`), via `13824 = 2^14 · 27/32` -/
theorem log_13824 : Real.log 13824 < 477 / 50 := by
  have := log_split_upper 14 16 (27 / 32) (98943749 / 10 ^ 8)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  rw [show (2 : ℝ) ^ 14 * (27 / 32) = 13824 by norm_num] at this
  norm_num at this ⊢; linarith

/-- `deficit_slack = η - (2970/10¹¹)(477/50)` -/
theorem deficit_slack :
    (365 / 1285272576 : ℚ) - 297 / 10000000000 * (477 / 50) =
      406952569 / 627574500000000000 ∧
    (0 : ℚ) < 406952569 / 627574500000000000 ∧ (297 / 10000000000 : ℚ) = 2970 / 10 ^ 11 := by
  norm_num

/-- `s/W < m^σ` with `1 - σ = 2970/10¹¹ = 297/10¹⁰` -/
theorem exponent :
    ((s4 : ℕ) : ℝ) / (W4 : ℕ) < (13824 : ℝ) ^ (1 - (297 / 10000000000 : ℝ)) := by
  obtain ⟨-, -, -, -, hW, -, -, hs, -⟩ := counts
  rw [hs, hW]
  apply exponent_certificate 13824 (477 / 50) (297 / 10000000000) (365 / 1285272576) _
    (by norm_num) (by norm_num) log_13824
  · norm_num
  · norm_num

/-! ## C. Gate count and the generalized guard -/

/-- `3v²(8v + 4C + 4 + 2(h-6))` scalar gates -/
def scalar_gates : ℕ := 3 * v 24 ^ 2 * (8 * v 24 + 4 * (base_additions + new_ancestors) + 4 + 2 * (24 - 6))
def E4 : ℕ := 64 * (W4 + m 24 + 1) ^ 3
def B4 : ℕ := s4 + E4
def ζ : ℚ := 1 / 10000
def C0 : ℕ :=
  1991520678995416584576942400432086873082564105960158546941478349741058754716840755200

theorem gate_bound :
    scalar_gates = 3475338442752 ∧ scalar_gates < 12 * W4 ∧
    36 * W4 ^ 3 + 4 * s4 + 4 * W4 + 4 < E4 := by
  obtain ⟨hv, hm, -, -, hW, -, -, hs, -⟩ := counts
  simp only [scalar_gates, base_additions, new_ancestors, E4, hv, hm, hW, hs]; norm_num

theorem guard_constants :
    E4 = 28288999069398280989721709640799207488 ∧
    B4 = 28288999069398280989732240071385306560 ∧
    3 ≤ m 24 ∧ 2 ≤ s4 ∧ s4 < m 24 ^ 5 ∧ s4 * (8 + E4) ≤ 9 * B4 ^ 2 ∧
    (C0 : ℚ) = max (128 * (m 24 : ℚ) * (B4 : ℚ) ^ 2) (18 * (m 24 : ℚ) * (B4 : ℚ) ^ 2 * (1 + 1 / ζ)) ∧
    9 * (m 24 : ℚ) * (B4 : ℚ) ^ 2 * (1 + 1 / ζ) + 18 ≤ C0 := by
  obtain ⟨-, hm, -, -, hW, -, -, hs, -⟩ := counts
  simp only [E4, B4, C0, ζ, hm, hW, hs]; norm_num

/-! ## D. Parameters, recurrence exponents, 31 slacks, 7 margins -/

def P : Params :=
  { tau := 12499999963 / 12500000000,
    sigma := 9999999703 / 10000000000,
    epsilon := 1999 / 10000,
    c := 1,
    lam := 999999997041 / 1000000000000,
    lamp := 499999998521 / 500000000000,
    kappa := 591 / 1000000000000,
    beta := 1 / 1000,
    delta := 1 / 1000000,
    C1 := 49961 / 10000 }

/-- patch lines 81-96 -/
theorem parameter_origin :
    P.tau = 1 - 296 / 10 ^ 11 ∧ P.sigma = 1 - 2970 / 10 ^ 11 ∧
    P.lam = 1 - 2959 / 10 ^ 12 ∧ P.lamp = 1 - 2958 / 10 ^ 12 ∧ P.kappa = 591 / 10 ^ 12 ∧
    P.C1 = 5 - 4 * P.beta + ζ := by
  simp only [P, ζ]; norm_num

theorem recurrence_values :
    P.internal = 12499999963 / 12500000000 ∧
    P.leaf = 9999999703297 / 10000000000000 ∧
    P.preprocessing = 0 ∧
    P.layer = 12499999963 / 12500000000 := by
  simp only [P]; params_unfold; norm_num

theorem slack_values :
    P.K_dominates_log_p = 1999 / 10000 ∧
    P.K_smaller_than_ell = 3001 / 5000 ∧
    P.alpha_below_sqrt_p = 8001 / 40000 ∧
    P.beta_below_one = 999 / 1000 ∧
    P.beta_positive = 1 / 1000 ∧
    P.c_positive = 1 ∧
    P.crt_layout = 296037 / 125000000000000 ∧
    P.delta_below_one_eighth = 124999 / 1000000 ∧
    P.delta_positive = 1 / 1000000 ∧
    P.dimension_upper_bound = 4003 / 30000 ∧
    P.epsilon_positive = 1999 / 10000 ∧
    P.gamma_sublinear = 4003 / 20000 ∧
    P.gaussian_cost = 31 / 250000 ∧
    P.guard_width = 127961 / 100000000 ∧
    P.kappa_positive = 591 / 1000000000000 ∧
    P.lambda_above_sigma = 26741 / 1000000000000 ∧
    P.lambda_above_tau = 1 / 1000000000000 ∧
    P.lambda_below_one = 2959 / 1000000000000 ∧
    P.lambda_prime_above_lambda = 1 / 1000000000000 ∧
    P.lambda_prime_below_one = 1479 / 500000000000 ∧
    P.leaf_cost = 267123 / 10000000000000 ∧
    P.packed_overhead = 1 / 1000000000000 ∧
    P.prefix_cost = 3001 / 5000 ∧
    P.prime_interval_growth = 3001 / 5000 ∧
    P.r_superpolynomial = 8001 / 10000 ∧
    P.reserved_axes = 499999998521 / 500000000000 ∧
    P.scalar_cost = 800099 / 1000000 ∧
    P.sigma_below_one = 297 / 10000000000 ∧
    P.sigma_positive = 9999999703 / 10000000000 ∧
    P.tau_below_one = 37 / 12500000000 ∧
    P.tau_positive = 12499999963 / 12500000000 := by
  simp only [P]; params_unfold; norm_num

theorem constraint_slacks : P.AllSlacksPositive := by
  simp only [P]; params_unfold; norm_num

theorem margin_values :
    P.g1 = 3001 / 5000 ∧
    P.g2 = 73963 / 125000000000000 ∧
    P.g3 = 2956521 / 5000000000000000 ∧
    P.g4 = 296037 / 125000000000000 ∧
    P.g5 = 31 / 250000 ∧
    P.g6 = 800099 / 1000000 ∧
    P.g7 = 1999 / 10000 := by
  simp only [P]; params_unfold; norm_num

/-- `min g = g3 = 2956521/(5·10¹⁵) > κ`, gap `1521/(5·10¹⁵)`, `2^-31 < κ < 2^-30`,
`κ/(83/10¹²) = 591/83` (`ratio_over_compact_witness`) -/
theorem kappa_witness :
    P.gmin = P.g3 ∧ P.gmin = 2956521 / 5000000000000000 ∧ P.Absorbs ∧
    P.gmin - P.kappa = 1521 / 5000000000000000 ∧
    (1 : ℚ) / 2 ^ 31 < P.kappa ∧ P.kappa < 1 / 2 ^ 30 ∧ P.kappa / (83 / 10 ^ 12) = 591 / 83 := by
  simp only [P]; params_unfold; norm_num [min_def]

/-- patch lines 81-96, 270-290 and 1787-1800; README "2.12 times" and "≈ 7.12" -/
theorem note_comparisons :
    P.sigma < P.tau ∧ P.internal = P.tau ∧ P.preprocessing = 0 ∧
    max (max P.tau P.sigma) P.internal < P.lam ∧ P.lam < P.lamp ∧ P.lamp < 1 ∧
    max (max P.leaf (1 - P.c)) 0 < P.lamp ∧
    P.epsilon * P.C1 = 99872039 / 10 ^ 8 ∧ P.epsilon * P.C1 < 1 ∧
    1 / 4 + P.epsilon / 4 = 11999 / 40000 ∧ (1 + 3 * P.epsilon) / 2 = 15997 / 20000 ∧
    P.epsilon * P.c = 1999 / 10000 ∧ 1 - P.epsilon = 8001 / 10000 ∧
    1 - 2 * P.epsilon = 3001 / 5000 ∧ P.epsilon * (1 + P.c) < 1 ∧
    (212 : ℚ) / 100 < (2970 / 10 ^ 11) / (14 / 10 ^ 9) ∧
    (2970 / 10 ^ 11 : ℚ) / (14 / 10 ^ 9) < 213 / 100 ∧
    (712 : ℚ) / 100 < 591 / 83 ∧ (591 : ℚ) / 83 < 713 / 100 := by
  simp only [P]; params_unfold; norm_num

theorem gaussian_cutoff (b : ℝ) (hb : (2 : ℝ) ^ 40 ≤ b) :
    46 * b ^ ((15997 : ℝ) / 20000) ≤ b / 4 := by
  have h := gaussian_cutoff_general (1999 / 10000) b (by norm_num) hb
  rwa [show (1 + 3 * (1999 / 10000 : ℝ)) / 2 = 15997 / 20000 by norm_num] at h

/-! ## E. Consistency with the bit-limited ceiling (no new ceiling is claimed) -/

theorem witness_below_fixed_tau_ceiling : ((P.kappa : ℚ) : ℝ) < 37 / 62500000000 := by
  refine (Bit.ceiling_fixed_tau (P.epsilon : ℝ) (P.delta : ℝ) (P.tau : ℝ) (P.lamp : ℝ)
    (P.kappa : ℝ) ?_ ?_ ?_ ?_ ?_ ?_).1 <;> simp only [P] <;> norm_num

/-! ## F. The preceding rectangle variant still described by the `.tex` notes

`notes/retained-complex-construction.tex` lines 166-193 (and patch lines 910-946):
`C = 123855 + 8325`, `q = 205956 + 27600 + h`, `R_aux = 365760`, `W = 3013310215168`,
`s = 41655997423981952`, `η = 365/5084246016`, `1 - σ = 750/10¹¹`, `6696869422848 < 12W`.
-/

def rect_additions : ℕ := 123855
def rect_q0 : ℕ := 205956
def rect_q2 : ℕ := 27600
/-- retained-tree additions `(v-1) + C(h,2)(h-3) + (h-1)(h-2)` -/
def rect_retained : ℕ := (v 24 - 1) + (24 : ℕ).choose 2 * (24 - 3) + (24 - 1) * (24 - 2)
def rect_C : ℕ := rect_additions + rect_retained
def rect_R : ℕ := rect_C + (rect_q0 + rect_q2 + 24)
def rect_W : ℕ := 2 * N 24 + 2 * v 24 ^ 2 * rect_R
def rect_s : ℕ := rect_W * m 24 + 2 * L4 - 2 * N 24

theorem rect_counts :
    rect_retained = 8325 ∧ rect_C = 132180 ∧ rect_q0 + rect_q2 + 24 = 233580 ∧
    rect_R = 365760 ∧ rect_W = 3013310215168 ∧ rect_s = 41655997423981952 ∧
    ((rect_W * m 24 - rect_s : ℕ) : ℚ) / (rect_W * m 24) = 365 / 5084246016 ∧
    3 * v 24 ^ 2 * (8 * v 24 + 4 * rect_C + 4) = 6696869422848 ∧
    3 * v 24 ^ 2 * (8 * v 24 + 4 * rect_C + 4) < 12 * rect_W ∧
    36 * rect_W ^ 3 + 4 * rect_s + 4 * rect_W + 4 < 64 * (rect_W + m 24 + 1) ^ 3 ∧
    2 ≤ rect_s ∧ rect_s < m 24 ^ 5 := by
  obtain ⟨hv, hm, hN, -, -, hL, -, -, -⟩ := counts
  simp only [rect_s, rect_W, rect_R, rect_C, rect_retained, rect_additions, rect_q0, rect_q2,
    hv, hm, hN, hL]
  norm_num [Nat.choose]

theorem rect_slack :
    (365 / 5084246016 : ℚ) - 750 / 10 ^ 11 * (477 / 50) = 11935523 / 49650840000000000 := by
  norm_num

theorem rect_exponent :
    ((rect_s : ℕ) : ℝ) / (rect_W : ℕ) < (13824 : ℝ) ^ (1 - (750 / 10 ^ 11 : ℝ)) := by
  obtain ⟨-, -, -, -, hW, hs, -⟩ := rect_counts
  rw [hs, hW]
  apply exponent_certificate 13824 (477 / 50) (750 / 10 ^ 11) (365 / 5084246016) _
    (by norm_num) (by norm_num) log_13824
  · norm_num
  · norm_num

/-- the variant's saving `750/10¹¹` differs from the certificate's `2970/10¹¹` -/
theorem rect_differs_from_certificate :
    rect_R ≠ R ∧ (750 / 10 ^ 11 : ℚ) ≠ 1 - P.sigma := by
  obtain ⟨-, -, -, hR, -⟩ := rect_counts
  refine ⟨by rw [hR]; simp [R], by simp only [P]; norm_num⟩

end PRChecksA.PR4
