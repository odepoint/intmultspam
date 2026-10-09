import PRChecksA.Bit

/-!
# PR #8: geometric complex-network candidate, `κ = 59/10¹¹`

Source: `research/geometric-complex/certificate.json` at PR head `428bb21`, produced by
`research/geometric-complex/verify.py` (counts and assembly from `explore.py`); written chain
in `research/geometric-complex/geometric-note.tex`.

Headline: `T(n) = O(n (log n)^(1-κ))`, `κ = 59/10¹¹ = 5.9e-10 > 2^-31` (ties PR #3).

The construction uses `n = 25` ground points and an extra label coordinate, so `h = 26`,
`m = 26³ = 17576`, while `v = C(25,3) = 2300`.

**Taken as given** (outputs of running `Circuit(25, 'disjoint')` and
`Circuit(25, 'intersection_two')`): additions `212737` / `36620`, outputs `2300` / `6900`
and roles `215037` / `43520`; and the small-size physical role counts `224` (n = 6) and
`554` (n = 7) of `audit.py`.  The note states no rational log bound; `log_17576` uses
`9775/1000`, which is our choice.
-/

namespace PRChecksA.PR8

open PRChecksA Real

/-! ## A. Circuit outputs (taken as given) and their bookkeeping -/

def disjoint_additions : ℕ := 212737
def disjoint_outputs : ℕ := 2300
def disjoint_roles : ℕ := 215037
def two_additions : ℕ := 36620
def two_outputs : ℕ := 6900
def two_roles : ℕ := 43520

/-- side roles per invocation -/
def R : ℕ := disjoint_roles + two_roles

/-- note lines 94-104 and 263-267: roles `= c + q` per circuit, `R = 258557`, outputs
`q = v + 3v = 4v`, the loose per-invocation operation bound
`8R + 4v + 4q + 18v ≤ 32(R + v + n + 1)`, and the baseline `v(C(22,3) + 66) = 3693800` -/
theorem circuit_bookkeeping :
    disjoint_roles = disjoint_additions + disjoint_outputs ∧
    two_roles = two_additions + two_outputs ∧ R = 258557 ∧
    disjoint_outputs = v 25 ∧ two_outputs = 3 * v 25 ∧
    disjoint_outputs + two_outputs = 4 * v 25 ∧
    8 * R + 4 * v 25 + 4 * (4 * v 25) + 18 * v 25 ≤ 32 * (R + v 25 + 25 + 1) ∧
    v 25 * zc 25 = 3693800 := by
  simp only [R, disjoint_additions, disjoint_outputs, disjoint_roles, two_additions, two_outputs,
    two_roles, v, zc]
  norm_num [Nat.choose]

/-! ## B. Network counts, η, log bound and the exponent certificate -/

/-- `W = 2N + 3v²(R + n + 1)` -/
def W8 : ℕ := 2 * N 25 + I 25 * (R + 25 + 1)
/-- `L_dec = 3v²(n + 1)h` with `h = n + 1 = 26` -/
def L8 : ℕ := I 25 * (25 + 1) * 26
/-- `s = W m - 2N + 2L_dec` with `m = 26³` -/
def s8 : ℕ := W8 * m 26 + 2 * L8 - 2 * N 25

theorem counts :
    v 25 = 2300 ∧ m 26 = 17576 ∧ N 25 = 12167000000 ∧ I 25 = 15870000 ∧
    W8 = 4128046210000 ∧ L8 = 10728120000 ∧ s8 = 72554537309200000 ∧ L8 < N 25 := by
  simp only [W8, L8, s8, R, disjoint_roles, two_roles, N, m, I, v]; norm_num [Nat.choose]

theorem s8_eq : (s8 : ℤ) = (W8 : ℤ) * m 26 - 2 * N 25 + 2 * L8 := by
  obtain ⟨-, hm, hN, -, hW, hL, hs, -⟩ := counts
  rw [hs, hW, hm, hN, hL]; norm_num

theorem eta : ((W8 * m 26 - s8 : ℕ) : ℚ) / (W8 * m 26) = 68 / 1714426753 := by
  obtain ⟨-, hm, -, -, hW, -, hs, -⟩ := counts
  rw [hW, hm, hs]; norm_num

/-- `log 17576 < 9775/1000`, via `17576 = 2^14 · 2197/2048` (our bound; true value 9.7743) -/
theorem log_17576 : Real.log 17576 < 9775 / 1000 := by
  have := log_split_upper 14 16 (2197 / 2048) (100439897 / 10 ^ 8)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  rw [show (2 : ℝ) ^ 14 * (2197 / 2048) = 17576 by norm_num] at this
  norm_num at this ⊢; linarith

/-- `η > (4/10⁹) log m`, with room: `(4/10⁹)(9775/1000) ≤ η` -/
theorem saving_slack :
    (1 / 250000000 : ℚ) * (9775 / 1000) < 68 / 1714426753 ∧ (1 / 250000000 : ℚ) = 4 / 10 ^ 9 := by
  norm_num

/-- the proposition's `s/W < m^(1 - 4·10⁻⁹)` -/
theorem exponent :
    ((s8 : ℕ) : ℝ) / (W8 : ℕ) < (17576 : ℝ) ^ (1 - (1 / 250000000 : ℝ)) := by
  obtain ⟨-, -, -, -, hW, -, hs, -⟩ := counts
  rw [hs, hW]
  apply exponent_certificate 17576 (9775 / 1000) (1 / 250000000) (68 / 1714426753) _
    (by norm_num) (by norm_num) log_17576
  · norm_num
  · norm_num

/-! ## C. Coefficient guard (note lines 260-279) -/

def scalar_depth_bound : ℕ := 32 * I 25 * (R + v 25 + 25 + 1)
def E8 : ℕ := 64 * (W8 + m 26 + 1) ^ 3
def B8 : ℕ := s8 + E8
def ζ : ℚ := 1 / 10000
def C0 : ℕ :=
  64130294840276912774725352938289728105607858968597929848820159508267994713089753730056192

theorem guard_constants :
    scalar_depth_bound = 132486822720000 ∧
    scalar_depth_bound + 4 * s8 + 4 * W8 + 4 < E8 ∧
    E8 = 4502084376669118574298921305012335938112 ∧
    B8 = 4502084376669118574298993859549645138112 ∧
    3 ≤ m 26 ∧ 2 ≤ s8 ∧ s8 < m 26 ^ 5 ∧ s8 * (8 + E8) ≤ 9 * B8 ^ 2 ∧
    (C0 : ℚ) = max (128 * (m 26 : ℚ) * (B8 : ℚ) ^ 2) (18 * (m 26 : ℚ) * (B8 : ℚ) ^ 2 * (1 + 1 / ζ)) ∧
    9 * (m 26 : ℚ) * (B8 : ℚ) ^ 2 * (1 + 1 / ζ) + 18 ≤ C0 := by
  obtain ⟨hv, hm, -, hI, hW, -, hs, -⟩ := counts
  simp only [scalar_depth_bound, E8, B8, C0, ζ, R, disjoint_roles, two_roles, hv, hm, hI, hW, hs]
  norm_num

/-! ## D. Parameters, recurrence exponents, 31 slacks, 7 margins -/

def P : Params :=
  { tau := 12499999963 / 12500000000,
    sigma := 249999999 / 250000000,
    epsilon := 1999 / 10000,
    c := 1,
    lam := 999999997041 / 1000000000000,
    lamp := 499999998521 / 500000000000,
    kappa := 59 / 100000000000,
    beta := 1 / 1000,
    delta := 1 / 1000000,
    C1 := 49961 / 10000 }

/-- note lines 285-293 -/
theorem parameter_origin :
    P.tau = 1 - 296 / 10 ^ 11 ∧ P.sigma = 1 - 4 / 10 ^ 9 ∧
    P.lam = 1 - 2959 / 10 ^ 12 ∧ P.lamp = 1 - 2958 / 10 ^ 12 ∧ P.kappa = 59 / 10 ^ 11 ∧
    P.C1 = 5 - 4 * P.beta + ζ := by
  simp only [P, ζ]; norm_num

theorem recurrence_values :
    P.internal = 12499999963 / 12500000000 ∧
    P.leaf = 249999999001 / 250000000000 ∧
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
    P.kappa_positive = 59 / 100000000000 ∧
    P.lambda_above_sigma = 1041 / 1000000000000 ∧
    P.lambda_above_tau = 1 / 1000000000000 ∧
    P.lambda_below_one = 2959 / 1000000000000 ∧
    P.lambda_prime_above_lambda = 1 / 1000000000000 ∧
    P.lambda_prime_below_one = 1479 / 500000000000 ∧
    P.leaf_cost = 519 / 500000000000 ∧
    P.packed_overhead = 1 / 1000000000000 ∧
    P.prefix_cost = 3001 / 5000 ∧
    P.prime_interval_growth = 3001 / 5000 ∧
    P.r_superpolynomial = 8001 / 10000 ∧
    P.reserved_axes = 499999998521 / 500000000000 ∧
    P.scalar_cost = 800099 / 1000000 ∧
    P.sigma_below_one = 1 / 250000000 ∧
    P.sigma_positive = 249999999 / 250000000 ∧
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

/-- note lines 310-323 and 334: `G* = g3 = 2956521/(5·10¹⁵) = 5.913042·10⁻¹⁰`,
`G* - κ = 1.3042·10⁻¹²`, `2^-31 < κ < 2^-30`, `κ/(83/10¹²) = 590/83 ≃ 7.10843` -/
theorem kappa_witness :
    P.gmin = P.g3 ∧ P.gmin = 2956521 / 5000000000000000 ∧
    P.gmin = 5913042 / 10 ^ 16 ∧ P.Absorbs ∧
    P.gmin - P.kappa = 6521 / 5000000000000000 ∧ P.gmin - P.kappa = 13042 / 10 ^ 16 ∧
    (1 : ℚ) / 2 ^ 31 < P.kappa ∧ P.kappa < 1 / 2 ^ 30 ∧ P.kappa / (83 / 10 ^ 12) = 590 / 83 ∧
    (710843 : ℚ) / 100000 < 590 / 83 ∧ (590 : ℚ) / 83 < 710844 / 100000 := by
  simp only [P]; params_unfold; norm_num [min_def]

/-- note lines 294-302 -/
theorem note_comparisons :
    P.sigma < P.tau ∧ P.internal = P.tau ∧ P.leaf = 1 - 3996 / 10 ^ 12 ∧
    P.preprocessing = 0 ∧
    max (max P.tau P.sigma) P.internal < P.lam ∧ P.lam < P.lamp ∧ P.lamp < 1 ∧
    max (max P.leaf (1 - P.c)) 0 < P.lamp ∧
    P.epsilon * (1 + P.c) = 3998 / 10000 ∧ P.epsilon * (1 + P.c) < 1 ∧
    P.epsilon * P.C1 = 99872039 / 10 ^ 8 ∧ P.epsilon * P.C1 < 1 := by
  simp only [P]; params_unfold; norm_num

theorem gaussian_cutoff (b : ℝ) (hb : (2 : ℝ) ^ 40 ≤ b) :
    46 * b ^ ((15997 : ℝ) / 20000) ≤ b / 4 := by
  have h := gaussian_cutoff_general (1999 / 10000) b (by norm_num) hb
  rwa [show (1 + 3 * (1999 / 10000 : ℝ)) / 2 = 15997 / 20000 by norm_num] at h

/-! ## E. The stated scoped ceiling (note lines 334-339) -/

/-- `κ < (296/10¹¹)/5 = 5.92·10⁻¹⁰` for the retained bit saving; the witness is above
`99.6%` of it -/
theorem scoped_ceiling_values :
    (296 : ℚ) / 10 ^ 11 / 5 = 592 / 10 ^ 12 ∧ P.kappa < 296 / 10 ^ 11 / 5 ∧
    (996 : ℚ) / 1000 * (296 / 10 ^ 11 / 5) < P.kappa := by
  simp only [P]; norm_num

theorem witness_meets_fixed_tau_ceiling : ((P.kappa : ℚ) : ℝ) < 37 / 62500000000 := by
  refine (Bit.ceiling_fixed_tau (P.epsilon : ℝ) (P.delta : ℝ) (P.tau : ℝ) (P.lamp : ℝ)
    (P.kappa : ℝ) ?_ ?_ ?_ ?_ ?_ ?_).1 <;> simp only [P] <;> norm_num

/-! ## F. The physical-audit rank formula (note lines 352-362, `physical_phase_audit`) -/

/-- per-invocation physical-edge sum at stage `j`, `a = h^(j-1)` -/
def auditRank (R h v a : ℤ) : ℤ := (R + h) * h ^ 3 + 2 * v * a * (h - 1) + 2 * h ^ 2

/-- "multiplying by `v²` and summing the three stages recovers `W m - 2N + 2L_dec`" -/
theorem audit_sums_to_rank_sum (R h v : ℤ) :
    v ^ 2 * (auditRank R h v 1 + auditRank R h v h + auditRank R h v (h ^ 2)) =
      (2 * v ^ 3 + 3 * v ^ 2 * (R + h)) * h ^ 3 - 2 * v ^ 3 + 2 * (3 * v ^ 2 * h * h) := by
  simp only [auditRank]; ring

/-- physical roles per invocation at `n = 6, 7` (data `2v`, side `R`, center `h`) -/
def phys6 : ℕ := 224
def phys7 : ℕ := 554

/-- the twelve audited rank sums and decreasing dimensions `h²` -/
theorem audit_small :
    auditRank ((phys6 : ℤ) - 2 * v 6 - 7) 7 (v 6) 1 = 63450 ∧
    auditRank ((phys6 : ℤ) - 2 * v 6 - 7) 7 (v 6) 7 = 64890 ∧
    auditRank ((phys6 : ℤ) - 2 * v 6 - 7) 7 (v 6) (7 ^ 2) = 74970 ∧
    auditRank ((phys7 : ℤ) - 2 * v 7 - 8) 8 (v 7) 1 = 248426 ∧
    auditRank ((phys7 : ℤ) - 2 * v 7 - 8) 8 (v 7) 8 = 251856 ∧
    auditRank ((phys7 : ℤ) - 2 * v 7 - 8) 8 (v 7) (8 ^ 2) = 279296 ∧
    (7 : ℕ) ^ 2 = 49 ∧ (8 : ℕ) ^ 2 = 64 := by
  simp only [auditRank, phys6, phys7, v]; norm_num [Nat.choose]

end PRChecksA.PR8
