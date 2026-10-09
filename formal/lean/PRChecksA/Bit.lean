import PRChecksA.Base

/-!
# The retained paired bit network (`h = 50`) and the bit-limited scoped ceiling

PRs #3, #4 and #8 all keep the paired bit network of `certificates/paired-network.json`
(unchanged in all three worktrees) with `τ = 1 - 296/10¹¹`.  Section A is main's
`KappaCheck.CrocSwap` section B, copied.  The side-role count `R = 509194` comes from
running the circuit `SharedPointCircuit(50, PairedExclusionCircuit(49))` and is
**taken as given**.

Section B checks the "next ceiling" that PRs #3 and #8 state once the complex network no
longer binds (`κ < a_b/5 = 296/(5·10¹¹) < 2^-30`):

* `ceiling_fixed_tau`: the stated bound holds when `1 - τ ≤ 296/10¹¹` (τ held at the
  retained value), as in `scripts/complex_network.py` ("With the bit exponent fixed");
* `ceiling_any_certified_tau`: for every `τ` that the published `h = 50` network certifies,
  `κ < 593/10¹²` and hence `κ < 2^-30`;
* `tau_2964_certified` and `beyond_fixed_tau_ceiling_*`: the published network also
  certifies `1 - τ = 2964/10¹²`, and then `κ = 5923/10¹³ > 296/(5·10¹¹)` meets all 31
  slacks and all seven margins, so `296/(5·10¹¹)` is a ceiling only for the fixed `τ`,
  not for the published network.
-/

namespace PRChecksA.Bit

open PRChecksA Real

/-! ## A. The paired bit network at `h = 50` (main's section B) -/

/-- side roles per invocation, **taken as given** (circuit output) -/
def R50 : ℕ := 509194
def Wp : ℕ := 2 * N 50 + 2 * v 50 ^ 2 * (R50 + 50)
def Lp : ℕ := 3 * v 50 ^ 2 * 50 ^ 2
def Dp : ℕ := N 50 - 2 * Lp
def sp : ℕ := Wp * m 50 - Dp

theorem bit50_counts :
    v 50 = 19600 ∧ m 50 = 125000 ∧ N 50 = 7529536000000 ∧ Wp = 406321422080000 ∧
    Lp = 2881200000000 ∧ Dp = 1767136000000 ∧ sp = 50790175992864000000 := by
  simp only [Wp, Lp, Dp, sp, R50, N, m, v]; norm_num [Nat.choose]

theorem bit50_eta : ((Dp : ℕ) : ℚ) / (Wp * m 50) = 23 / 661055000 := by
  simp only [Wp, Lp, Dp, R50, N, m, v]; norm_num [Nat.choose]

/-- their bound `log 125000 < 11.737`, with `125000 = 2^17 · 15625/16384` -/
theorem log_125000 : Real.log 125000 < 11737 / 1000 := by
  have := log_split_upper 17 16 (15625 / 16384) (99703983 / 10 ^ 8)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  rw [show (2 : ℝ) ^ 17 * (15625 / 16384) = 125000 by norm_num] at this
  norm_num at this ⊢; linarith

/-- `1 - τ = 296/10¹¹` is certified for the paired bit network -/
theorem bit50_exponent :
    ((sp : ℕ) : ℝ) / (Wp : ℕ) < (125000 : ℝ) ^ (1 - (296 / 10 ^ 11 : ℝ)) := by
  obtain ⟨-, -, -, hW, -, -, hs⟩ := bit50_counts
  rw [hs, hW]
  apply exponent_certificate 125000 (11737 / 1000) (296 / 10 ^ 11) (23 / 661055000) _
    (by norm_num) (by norm_num) log_125000
  · norm_num
  · norm_num

/-! ## B. The bit-limited scoped ceiling -/

/-- `125000 = 2^17 · 125000/131072` and `log y ≥ 1 - 1/y` give `log 125000 > 11.7349` -/
theorem log_125000_gt : (117349 : ℝ) / 10000 < Real.log 125000 := by
  have := log_split_lower 17 (125000 / 131072) (by norm_num)
  rw [show (2 : ℝ) ^ 17 * (125000 / 131072) = 125000 by norm_num] at this
  norm_num at this ⊢; linarith

/-- main's `certified_saving_le`: a certified `σ` has `(1-σ) log m ≤ (1 - r/m)/(r/m)` -/
theorem certified_saving_le (m r σ' : ℝ) (hm : 1 < m) (hr : 0 < r)
    (hcert : r ≤ m ^ σ') :
    (1 - σ') * Real.log m ≤ (1 - r / m) / (r / m) := by
  have hm0 : 0 < m := by linarith
  have hlog : Real.log r ≤ σ' * Real.log m := by
    have := Real.log_le_log hr hcert
    rwa [Real.log_rpow hm0] at this
  have hq : 0 < r / m := div_pos hr hm0
  have key : -Real.log (r / m) ≤ (1 - r / m) / (r / m) := by
    have := Real.log_le_sub_one_of_pos (inv_pos.mpr hq)
    rw [Real.log_inv] at this
    have e : (1 - r / m) / (r / m) = (r / m)⁻¹ - 1 := by field_simp
    rw [e]; linarith
  rw [Real.log_div hr.ne' hm0.ne'] at key
  nlinarith

/-- with `σ < τ` the layer needs `λ > τ`, so `κ < g3 = ε(1-λ') < ε(1-τ) < (1-τ)/5`,
the last step from the Gaussian margin `1/4 - δ - 5ε/4 > 0` -/
theorem kappa_lt_fifth_bit (ε δ τ lamp κ : ℝ) (hδ : 0 ≤ δ)
    (hgauss : 0 < 1 / 4 - δ - 5 / 4 * ε) (hτ : τ < lamp) (hlamp1 : lamp < 1)
    (hκ : κ < ε * (1 - lamp)) : κ < (1 - τ) / 5 := by
  have h1 : ε < 1 / 5 := by linarith
  have h2 : 0 < 1 - lamp := by linarith
  calc κ < ε * (1 - lamp) := hκ
    _ ≤ 1 / 5 * (1 - lamp) := by gcongr
    _ < 1 / 5 * (1 - τ) := by gcongr
    _ = (1 - τ) / 5 := by ring

/-- **The stated ceiling, for the retained `τ`**: with `1 - τ ≤ 296/10¹¹`,
`κ < 296/(5·10¹¹) = 37/62500000000 < 2^-30` -/
theorem ceiling_fixed_tau (ε δ τ lamp κ : ℝ) (hfix : 1 - τ ≤ 296 / 10 ^ 11) (hδ : 0 ≤ δ)
    (hgauss : 0 < 1 / 4 - δ - 5 / 4 * ε) (hτ : τ < lamp) (hlamp1 : lamp < 1)
    (hκ : κ < ε * (1 - lamp)) :
    κ < 37 / 62500000000 ∧ (37 / 62500000000 : ℝ) = 296 / (5 * 10 ^ 11) ∧
      (37 / 62500000000 : ℝ) < 1 / 2 ^ 30 := by
  have := kappa_lt_fifth_bit ε δ τ lamp κ hδ hgauss hτ hlamp1 hκ
  refine ⟨by linarith, by norm_num, by norm_num⟩

/-- **The ceiling for the published network**: for every `τ` with `s_b/W_b ≤ 125000^τ`,
the retained Gaussian margin and `τ < λ' < 1` give `κ < 593/10¹² < 2^-30` -/
theorem ceiling_any_certified_tau (ε δ τ lamp κ : ℝ)
    (hcert : ((sp : ℕ) : ℝ) / (Wp : ℕ) ≤ (125000 : ℝ) ^ τ) (hδ : 0 ≤ δ)
    (hgauss : 0 < 1 / 4 - δ - 5 / 4 * ε) (hτ : τ < lamp) (hlamp1 : lamp < 1)
    (hκ : κ < ε * (1 - lamp)) : κ < 593 / 10 ^ 12 ∧ κ < 1 / 2 ^ 30 := by
  have hk := kappa_lt_fifth_bit ε δ τ lamp κ hδ hgauss hτ hlamp1 hκ
  obtain ⟨-, -, -, hW, -, -, hs⟩ := bit50_counts
  rw [hs, hW] at hcert
  have hsv := certified_saving_le 125000 ((50790175992864000000 : ℝ) / 406321422080000) τ
    (by norm_num) (by norm_num) hcert
  have hl := log_125000_gt
  have hpos : 0 < 1 - τ := by linarith
  have : (1 - τ) * (117349 / 10000) < (1 - τ) * Real.log 125000 :=
    mul_lt_mul_of_pos_left hl hpos
  norm_num at hsv this ⊢
  constructor <;> linarith

/-- the published network certifies `1 - τ = 2964/10¹²` (`2964·11737/10¹⁵ ≤ η_b`) -/
theorem tau_2964_certified :
    ((sp : ℕ) : ℝ) / (Wp : ℕ) < (125000 : ℝ) ^ (1 - (2964 / 10 ^ 12 : ℝ)) := by
  obtain ⟨-, -, -, hW, -, -, hs⟩ := bit50_counts
  rw [hs, hW]
  apply exponent_certificate 125000 (11737 / 1000) (2964 / 10 ^ 12) (23 / 661055000) _
    (by norm_num) (by norm_num) log_125000
  · norm_num
  · norm_num

/-- a parameter choice with the re-certified `τ` and PR #3's complex `σ = 1 - 14/10⁹` -/
def Pbeyond3 : Params :=
  { tau := 1 - 2964 / 10 ^ 12, sigma := 1 - 14 / 10 ^ 9, epsilon := 19999 / 100000, c := 1,
    lam := 1 - 2963 / 10 ^ 12, lamp := 1 - 2962 / 10 ^ 12, kappa := 5923 / 10 ^ 13,
    beta := 1 / 1000, delta := 1 / 10 ^ 6, C1 := 49961 / 10000 }

/-- the same with PR #8's complex `σ = 1 - 4/10⁹` -/
def Pbeyond8 : Params :=
  { tau := 1 - 2964 / 10 ^ 12, sigma := 1 - 4 / 10 ^ 9, epsilon := 19999 / 100000, c := 1,
    lam := 1 - 2963 / 10 ^ 12, lamp := 1 - 2962 / 10 ^ 12, kappa := 5923 / 10 ^ 13,
    beta := 1 / 1000, delta := 1 / 10 ^ 6, C1 := 49961 / 10000 }

/-- negative control for the JSON's `scoped_ceiling.upper = 37/62500000000`: with the
published network's re-certified `τ`, all 31 slacks and all seven margins hold for a
`κ` above it (and below `593/10¹²`) -/
theorem beyond_fixed_tau_ceiling_3 :
    Pbeyond3.AllSlacksPositive ∧ Pbeyond3.Absorbs ∧ 37 / 62500000000 < Pbeyond3.kappa ∧
      Pbeyond3.kappa < 593 / 10 ^ 12 := by
  simp only [Pbeyond3]; params_unfold; norm_num

theorem beyond_fixed_tau_ceiling_8 :
    Pbeyond8.AllSlacksPositive ∧ Pbeyond8.Absorbs ∧ 37 / 62500000000 < Pbeyond8.kappa ∧
      Pbeyond8.kappa < 593 / 10 ^ 12 := by
  simp only [Pbeyond8]; params_unfold; norm_num

/-- non-vacuity: the re-certified `τ` really feeds `ceiling_any_certified_tau`, whose bound
`593/10¹²` the witness `κ = 5923/10¹³` approaches -/
theorem beyond_witness_meets_general_ceiling :
    ((5923 : ℚ) / 10 ^ 13 : ℝ) < 593 / 10 ^ 12 := by
  have := ceiling_any_certified_tau (19999 / 100000) (1 / 10 ^ 6) (1 - 2964 / 10 ^ 12)
    (1 - 2962 / 10 ^ 12) ((5923 : ℚ) / 10 ^ 13 : ℝ) tau_2964_certified.le
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  exact this.1

end PRChecksA.Bit
