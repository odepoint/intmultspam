import PRChecksA.Bit

/-!
# PR #3: compressed complex side circuit, `κ = 59/10¹¹`

Source: `certificates/complex-network.json` at PR head `dfe5b81`, produced by
`scripts/complex_network.py`; written chain in `notes/complex-circuit-note.tex`,
`notes/complex-circuit-construction.tex` and `docs/research/complex-circuit.md`.

Headline: `T(n) = O(n (log n)^(1-κ))`, `κ = 59/10¹¹ = 5.9e-10`, `2^-31 < κ < 2^-30`.

**Taken as given** (outputs of running `ComplexSideCircuit(25)`): `additions = 80595`,
`disjoint_additions = 68595`, `pair_star_additions = 12000`, `injections = 27600`,
`active_nodes = 82895`, and the side-role count `R = 108195`; also the bit network's
`R50` (see `PRChecksA.Bit`).  Everything else below is derived from the PR's formulas.
-/

namespace PRChecksA.PR3

open PRChecksA Real

/-! ## A. Circuit outputs (taken as given) and their bookkeeping -/

def additions : ℕ := 80595
def disjoint_additions : ℕ := 68595
def pair_star_additions : ℕ := 12000
def injections : ℕ := 27600
def active_nodes : ℕ := 82895
/-- side roles per invocation, `R = c + q` -/
def R : ℕ := 108195

/-- construction lines 67-78: `c = 68595 + 12000`, `R = c + q`, twelve pieces per target,
`active = inputs + additions`; pair stars use `2·(23-3)` additions per pair (the rule
splits `π₂₂` and `σ₂`); the original motif used `v z_c = 3693800` side wires -/
theorem circuit_bookkeeping :
    additions = disjoint_additions + pair_star_additions ∧ R = additions + injections ∧
    injections = 12 * v 25 ∧ active_nodes = v 25 + additions ∧
    pair_star_additions = (25 : ℕ).choose 2 * (2 * (23 - 3)) ∧ v 25 * zc 25 = 3693800 := by
  simp only [additions, disjoint_additions, pair_star_additions, injections, active_nodes, R,
    v, zc]
  norm_num [Nat.choose]

/-! ## B. Network counts, η, log bound and the exponent certificate -/

/-- `W_c = 2N + 3v²(R + h + 1)` -/
def W3 : ℕ := 2 * N 25 + I 25 * (R + 25 + 1)
/-- `L_c = 3v² h (h + 1)` -/
def L3 : ℕ := I 25 * (25 + 1) * 25
/-- `s_c = W_c m - 2N + 2L_c`, written so that natural subtraction is harmless -/
def s3 : ℕ := W3 * m 25 + 2 * L3 - 2 * N 25

theorem counts :
    v 25 = 2300 ∧ m 25 = 15625 ∧ N 25 = 12167000000 ∧ I 25 = 15870000 ∧
    W3 = 1741801270000 ∧ L3 = 10315500000 ∧ s3 = 27215641140750000 ∧
    W3 * m 25 - s3 = 3703000000 ∧ L3 < N 25 := by
  simp only [W3, L3, s3, R, N, m, I, v]; norm_num [Nat.choose]

theorem s3_eq : (s3 : ℤ) = (W3 : ℤ) * m 25 - 2 * N 25 + 2 * L3 := by
  obtain ⟨-, hm, hN, -, hW, hL, hs, -, -⟩ := counts
  rw [hs, hW, hm, hN, hL]; norm_num

theorem eta : ((W3 * m 25 - s3 : ℕ) : ℚ) / (W3 * m 25) = 28 / 205789375 := by
  obtain ⟨-, hm, -, -, hW, -, hs, hd, -⟩ := counts
  rw [hd, hW, hm]; norm_num

/-- `log m < 483/50` (`= 966/100`, `log_m_upper`), via `15625 = 2^14 · 15625/16384` -/
theorem log_15625 : Real.log 15625 < 483 / 50 := by
  have := log_split_upper 14 16 (15625 / 16384) (99703983 / 10 ^ 8)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  rw [show (2 : ℝ) ^ 14 * (15625 / 16384) = 15625 by norm_num] at this
  norm_num at this ⊢; linarith

/-- `complex_deficit_slack = η - a_c · 483/50` -/
theorem deficit_slack :
    (28 / 205789375 : ℚ) - 7 / 500000000 * (483 / 50) = 6761797 / 8231575000000000 ∧
    (0 : ℚ) < 6761797 / 8231575000000000 ∧ (7 / 500000000 : ℚ) = 14 / 10 ^ 9 := by
  norm_num

/-- construction line 216: `s_c/W_c < m^σ` with `1 - σ = 14/10⁹ = 7/500000000` -/
theorem exponent :
    ((s3 : ℕ) : ℝ) / (W3 : ℕ) < (15625 : ℝ) ^ (1 - (7 / 500000000 : ℝ)) := by
  obtain ⟨-, -, -, -, hW, -, hs, -, -⟩ := counts
  rw [hs, hW]
  apply exponent_certificate 15625 (483 / 50) (7 / 500000000) (28 / 205789375) _
    (by norm_num) (by norm_num) log_15625
  · norm_num
  · norm_num

/-! ## C. Gate count and the generalized guard -/

/-- four mixer passes, two copies, two injections, four central gates -/
def gates_per_invocation : ℕ := 4 * active_nodes + 4 * v 25 + 4
def E3 : ℕ := 64 * (W3 + m 25 + 1) ^ 3
def B3 : ℕ := s3 + E3
def ζ : ℚ := 1 / 10000
def C0 : ℕ :=
  321727027889740762489223803495350305328695729120143793284991524019954162292886152000000

theorem gate_bound :
    gates_per_invocation = 340784 ∧ I 25 * gates_per_invocation = 5408242080000 ∧
    12 * W3 = 20901615240000 ∧ I 25 * gates_per_invocation ≤ 12 * W3 := by
  obtain ⟨hv, -, -, hI, hW, -, -, -, -⟩ := counts
  simp only [gates_per_invocation, active_nodes, hv, hI, hW]; norm_num

theorem guard_constants :
    E3 = 338201706233372774319082463160146840064 ∧
    B3 = 338201706233372774319109678801287590064 ∧
    3 ≤ m 25 ∧ 2 ≤ s3 ∧ s3 < m 25 ^ 5 ∧ s3 * (8 + E3) ≤ 9 * B3 ^ 2 ∧
    -- `C0 = ⌈max(128 m B², 18 m B² (1 + 1/ζ))⌉` (the max is an integer) and the whole layer
    (C0 : ℚ) = max (128 * (m 25 : ℚ) * (B3 : ℚ) ^ 2) (18 * (m 25 : ℚ) * (B3 : ℚ) ^ 2 * (1 + 1 / ζ)) ∧
    9 * (m 25 : ℚ) * (B3 : ℚ) ^ 2 * (1 + 1 / ζ) + 18 ≤ C0 := by
  obtain ⟨-, hm, -, -, hW, -, hs, -, -⟩ := counts
  simp only [E3, B3, C0, ζ, hm, hW, hs]; norm_num

/-! ## D. Parameters, recurrence exponents, 31 slacks, 7 margins -/

def P : Params :=
  { tau := 12499999963 / 12500000000,
    sigma := 499999993 / 500000000,
    epsilon := 19999 / 100000,
    c := 999 / 1000,
    lam := 499999998521 / 500000000000,
    lamp := 249999999261 / 250000000000,
    kappa := 59 / 100000000000,
    beta := 1 / 1000,
    delta := 1 / 1000000,
    C1 := 49961 / 10000 }

/-- note lines 50-58: the parameters come from the certified savings -/
theorem parameter_origin :
    P.tau = 1 - 296 / 10 ^ 11 ∧ 1 - P.tau = 37 / 12500000000 ∧
    P.sigma = 1 - 14 / 10 ^ 9 ∧ 1 - P.sigma = 7 / 500000000 ∧
    P.lam = 1 - 2958 / 10 ^ 12 ∧ P.lamp = 1 - 2956 / 10 ^ 12 ∧ P.kappa = 59 / 10 ^ 11 ∧
    P.C1 = 5 - 4 * P.beta + ζ ∧ P.beta = 1 / 1000 := by
  simp only [P, ζ]; norm_num

theorem recurrence_values :
    P.internal = 12499999963 / 12500000000 ∧
    P.leaf = 499999993007 / 500000000000 ∧
    P.preprocessing = 1 / 1000 ∧
    P.layer = 12499999963 / 12500000000 := by
  simp only [P]; params_unfold; norm_num

theorem slack_values :
    P.K_dominates_log_p = 19979001 / 100000000 ∧
    P.K_smaller_than_ell = 60021999 / 100000000 ∧
    P.alpha_below_sqrt_p = 80001 / 400000 ∧
    P.beta_below_one = 999 / 1000 ∧
    P.beta_positive = 1 / 1000 ∧
    P.c_positive = 999 / 1000 ∧
    P.crt_layout = 2960037 / 1250000000000000 ∧
    P.delta_below_one_eighth = 124999 / 1000000 ∧
    P.delta_positive = 1 / 1000000 ∧
    P.dimension_upper_bound = 40003 / 300000 ∧
    P.epsilon_positive = 19999 / 100000 ∧
    P.gamma_sublinear = 40003 / 200000 ∧
    P.gaussian_cost = 23 / 2000000 ∧
    P.guard_width = 829961 / 1000000000 ∧
    P.kappa_positive = 59 / 100000000000 ∧
    P.lambda_above_sigma = 5521 / 500000000000 ∧
    P.lambda_above_tau = 1 / 500000000000 ∧
    P.lambda_below_one = 1479 / 500000000000 ∧
    P.lambda_prime_above_lambda = 1 / 500000000000 ∧
    P.lambda_prime_below_one = 739 / 250000000000 ∧
    P.leaf_cost = 1103 / 100000000000 ∧
    P.packed_overhead = 1 / 500000000000 ∧
    P.prefix_cost = 60021999 / 100000000 ∧
    P.prime_interval_growth = 30001 / 50000 ∧
    P.r_superpolynomial = 80001 / 100000 ∧
    P.reserved_axes = 249749999261 / 250000000000 ∧
    P.scalar_cost = 800009 / 1000000 ∧
    P.sigma_below_one = 7 / 500000000 ∧
    P.sigma_positive = 499999993 / 500000000 ∧
    P.tau_below_one = 37 / 12500000000 ∧
    P.tau_positive = 12499999963 / 12500000000 := by
  simp only [P]; params_unfold; norm_num

/-- all 31 constraint slacks are strictly positive -/
theorem constraint_slacks : P.AllSlacksPositive := by
  simp only [P]; params_unfold; norm_num

theorem margin_values :
    P.g1 = 60021999 / 100000000 ∧
    P.g2 = 739223037 / 1250000000000000000 ∧
    P.g3 = 14779261 / 25000000000000000 ∧
    P.g4 = 2960037 / 1250000000000000 ∧
    P.g5 = 23 / 2000000 ∧
    P.g6 = 800009 / 1000000 ∧
    P.g7 = 19999 / 100000 := by
  simp only [P]; params_unfold; norm_num

/-- note lines 86-97: `min g = g3 = 14779261/(25·10¹⁵) > κ`, gap `29261/(25·10¹⁵)`,
`2^-31 < κ < 2^-30`, and `κ / (83/10¹²) = 590/83` -/
theorem kappa_witness :
    P.gmin = P.g3 ∧ P.gmin = 14779261 / 25000000000000000 ∧ P.Absorbs ∧
    P.gmin - P.kappa = 29261 / 25000000000000000 ∧
    (1 : ℚ) / 2 ^ 31 < P.kappa ∧ P.kappa < 1 / 2 ^ 30 ∧ P.kappa / (83 / 10 ^ 12) = 590 / 83 := by
  simp only [P]; params_unfold; norm_num [min_def]

/-- note lines 60-78 and 86, construction line 218, docs §5 -/
theorem note_comparisons :
    P.sigma < P.tau ∧ P.internal = P.tau ∧
    max (max P.tau P.sigma) P.internal < P.lam ∧ P.lam < P.lamp ∧ P.lamp < 1 ∧
    max P.leaf (1 - P.c) < P.lamp ∧
    P.epsilon * P.C1 = 999170039 / 10 ^ 9 ∧ P.epsilon * P.C1 < 1 ∧
    1 / 4 + P.epsilon / 4 = 119999 / 400000 ∧ (1 + 3 * P.epsilon) / 2 = 159997 / 200000 ∧
    1 - 2 * P.epsilon = 30001 / 50000 ∧ P.epsilon * (1 + P.c) < 1 ∧
    -- "the former choice c = 1/5 would now make g2 binding": it would fall below κ
    P.epsilon * (1 / 5) * (1 - P.tau) < P.kappa ∧
    -- "33.49 times the previous complex saving 418/10¹²"
    (3349 : ℚ) / 100 < (14 / 10 ^ 9) / (418 / 10 ^ 12) ∧
    (14 / 10 ^ 9 : ℚ) / (418 / 10 ^ 12) < 3350 / 100 ∧
    -- "a_c exceeds a by a factor 4.7"
    (47 : ℚ) / 10 < (14 / 10 ^ 9) / (296 / 10 ^ 11) ∧
    (14 / 10 ^ 9 : ℚ) / (296 / 10 ^ 11) < 48 / 10 := by
  simp only [P]; params_unfold; norm_num

/-- note line 75-76: the retained Gaussian cutoff at `ε = 19999/100000` -/
theorem gaussian_cutoff (b : ℝ) (hb : (2 : ℝ) ^ 40 ≤ b) :
    46 * b ^ ((159997 : ℝ) / 200000) ≤ b / 4 := by
  have h := gaussian_cutoff_general (19999 / 100000) b (by norm_num) hb
  rwa [show (1 + 3 * (19999 / 100000 : ℝ)) / 2 = 159997 / 200000 by norm_num] at h

/-! ## E. The scoped "next ceiling" (note lines 100-111, docs §5, JSON `scoped_ceiling`) -/

/-- `upper = 37/62500000000 = bit_saving/5 < 2^-30`, the witness is above `99.6%` of it -/
theorem scoped_ceiling_values :
    (37 : ℚ) / 62500000000 = (37 / 12500000000) / 5 ∧
    (37 : ℚ) / 62500000000 = 296 / (5 * 10 ^ 11) ∧ (37 : ℚ) / 62500000000 < 1 / 2 ^ 30 ∧
    P.kappa < 37 / 62500000000 ∧ (996 : ℚ) / 1000 * (37 / 62500000000) < P.kappa ∧
    P.kappa / (37 / 62500000000) = 295 / 296 := by
  simp only [P]; norm_num

/-- docs/research/complex-circuit.md line 102 writes `kappa < a_b/5 < 5.92e-10`;
in fact `a_b/5 = 5.92e-10` exactly, so the middle `<` is an equality -/
theorem docs_line_102_is_equality :
    (296 : ℚ) / 10 ^ 11 / 5 = 592 / 10 ^ 12 ∧ ¬ ((296 : ℚ) / 10 ^ 11 / 5 < 592 / 10 ^ 12) := by
  norm_num

/-- non-vacuity: the witness meets every hypothesis of `Bit.ceiling_fixed_tau` -/
theorem witness_meets_fixed_tau_ceiling : ((P.kappa : ℚ) : ℝ) < 37 / 62500000000 := by
  refine (Bit.ceiling_fixed_tau (P.epsilon : ℝ) (P.delta : ℝ) (P.tau : ℝ) (P.lamp : ℝ)
    (P.kappa : ℝ) ?_ ?_ ?_ ?_ ?_ ?_).1 <;> simp only [P] <;> norm_num

/-- and of `Bit.ceiling_any_certified_tau` (its `τ` is certified by `Bit.bit50_exponent`) -/
theorem witness_meets_general_ceiling : ((P.kappa : ℚ) : ℝ) < 1 / 2 ^ 30 := by
  have hcert : ((Bit.sp : ℕ) : ℝ) / (Bit.Wp : ℕ) ≤ (125000 : ℝ) ^ ((P.tau : ℚ) : ℝ) := by
    have := Bit.bit50_exponent.le
    convert this using 2; simp only [P]; norm_num
  refine (Bit.ceiling_any_certified_tau (P.epsilon : ℝ) (P.delta : ℝ) (P.tau : ℝ) (P.lamp : ℝ)
    (P.kappa : ℝ) hcert ?_ ?_ ?_ ?_ ?_).2 <;> simp only [P] <;> norm_num

end PRChecksA.PR3
