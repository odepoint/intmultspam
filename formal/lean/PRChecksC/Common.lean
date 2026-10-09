import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Data.Complex.ExponentialBounds

/-!
# Shared lemmas for the PR #9, #10 and #12 arithmetic checks

* `exponent_certificate`: copied verbatim from main's `KappaCheck/Certificates.lean`
  (branch `lean-certificate-check`): `x L ≤ η`, `log m < L` give `m (1 - η) < m ^ (1 - x)`.
* `moment_term`: the batched (mixed-width) analogue used by PR #10 and #12:
  `c/W · r^(1-a) ≤ (c r / W) / (1 - a ℓ)` when `log (1/r) ≤ ℓ` and `a ℓ < 1`,
  i.e. `r^(-a) = exp (a log (1/r)) ≤ exp (a ℓ) ≤ 1/(1 - a ℓ)`.
* rational logarithm enclosures from the series of `-log (1 - x)` (Mathlib's
  `Real.abs_log_sub_add_sum_range_le`, as in main's `CrocSwap.lean` section H), and the
  identities `2, 3, 5 = (16/15)^a (25/24)^b (81/80)^c`.
* `taylor_six_fifths`: `(1-t)^(6/5) ≤ 1 - 6t/5 + (3/25) t²/(1-t)` for `0 < t < 1`
  (PR #10, `notes/bulk-complex-guard.tex` line 99-100), proved by the substitution
  `w = (1-t)^(1/5)` and the factorization
  `3 - 11w⁵ + 33w¹⁰ - 25w¹¹ = (1-w)³ (3 + 9w + 18w² + 30w³ + 45w⁴ + 52w⁵ + 51w⁶ + 42w⁷ + 25w⁸)`.
-/

namespace PRChecksC

open Real

/-! ## The generic exponent certificate (main, `Certificates.lean`) -/

theorem exponent_certificate (m L x η r : ℝ) (hm : 0 < m) (hx : 0 < x)
    (hlog : Real.log m < L) (hxη : x * L ≤ η) (hr : r = m * (1 - η)) :
    r < m ^ (1 - x) := by
  have hpow : m ^ (1 - x) = m * Real.exp (-(Real.log m * x)) := by
    rw [Real.rpow_sub hm, Real.rpow_one, Real.rpow_def_of_pos hm, Real.exp_neg, div_eq_mul_inv]
  have hexp := Real.add_one_le_exp (-(Real.log m * x))
  have h1 : Real.log m * x < L * x := mul_lt_mul_of_pos_right hlog hx
  have h3 : 1 - η < Real.exp (-(Real.log m * x)) := by nlinarith
  rw [hpow, hr]
  exact mul_lt_mul_of_pos_left h3 hm

/-! ## The batched moment term -/

theorem exp_le_inv_one_sub (x : ℝ) (hx : x < 1) : Real.exp x ≤ 1 / (1 - x) := by
  rw [le_div_iff₀ (by linarith)]
  have h := Real.add_one_le_exp (-x)
  have h2 : Real.exp x * Real.exp (-x) = 1 := by rw [← Real.exp_add]; simp
  have hpos := Real.exp_pos x
  nlinarith

/-- one term of a mixed-width moment: a class of `c` children of normalized width `r`,
out of `W` parent wires, costs `c/W · r^(1-a)`; with `log (1/r) ≤ ℓ` this is at most
`w / (1 - a ℓ)` where `w = c r / W` is the class's rank-mass weight. -/
theorem moment_term (c W r a ℓ : ℝ) (hc : 0 ≤ c) (hW : 0 < W) (hr : 0 < r) (ha : 0 ≤ a)
    (hℓ : Real.log (1 / r) ≤ ℓ) (haℓ : a * ℓ < 1) :
    c / W * r ^ (1 - a) ≤ c * r / W / (1 - a * ℓ) := by
  have h1 : r ^ (1 - a) = r * Real.exp (a * Real.log (1 / r)) := by
    rw [Real.rpow_sub hr, Real.rpow_one, Real.rpow_def_of_pos hr, one_div, Real.log_inv,
      div_eq_mul_inv, ← Real.exp_neg, show a * -Real.log r = -(Real.log r * a) by ring]
  have h2 : Real.exp (a * Real.log (1 / r)) ≤ 1 / (1 - a * ℓ) :=
    (Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left hℓ ha)).trans (exp_le_inv_one_sub _ haℓ)
  have hcW : 0 ≤ c * r / W := by positivity
  rw [h1]
  calc c / W * (r * Real.exp (a * Real.log (1 / r)))
        = c * r / W * Real.exp (a * Real.log (1 / r)) := by ring
    _ ≤ c * r / W * (1 / (1 - a * ℓ)) := mul_le_mul_of_nonneg_left h2 hcW
    _ = c * r / W / (1 - a * ℓ) := by ring

/-- the singleton class in the note's form `S / (W m^τ)` -/
theorem singleton_form (S W m τ : ℝ) (hm : 0 < m) :
    S / (W * m ^ τ) = S / W * (1 / m) ^ τ := by
  rw [Real.div_rpow zero_le_one hm.le, Real.one_rpow]
  ring

/-! ## Logarithm enclosures from the series of `-log (1 - x)` -/

/-- partial sums of `-log(1 - x) = Σ x^(i+1)/(i+1)` (as in main's `CrocSwap.lean`) -/
noncomputable def ps (x : ℝ) (n : ℕ) : ℝ := ∑ i ∈ Finset.range n, x ^ (i + 1) / (i + 1)

/-- upper and lower enclosures of `-log (1 - x)` with `n` terms -/
noncomputable def Up (x : ℝ) (n : ℕ) : ℝ := ps x n + x ^ (n + 1) / (1 - x)
noncomputable def Lo (x : ℝ) (n : ℕ) : ℝ := ps x n - x ^ (n + 1) / (1 - x)

theorem neglog_bounds (x : ℝ) (hx0 : 0 ≤ x) (hx1 : x < 1) (n : ℕ) :
    Lo x n ≤ -Real.log (1 - x) ∧ -Real.log (1 - x) ≤ Up x n := by
  have h := Real.abs_log_sub_add_sum_range_le
    (show |x| < 1 by rw [abs_of_nonneg hx0]; exact hx1) n
  rw [abs_of_nonneg hx0] at h
  obtain ⟨h1, h2⟩ := abs_le.mp h
  unfold Lo Up ps; constructor <;> linarith

/-- `log (1/r) ≤ ℓ` for `r = 1 - x`, from `n` terms of the series -/
theorem log_inv_le (r x ℓ : ℝ) (n : ℕ) (hr : r = 1 - x) (hx0 : 0 ≤ x) (hx1 : x < 1)
    (h : Up x n ≤ ℓ) : Real.log (1 / r) ≤ ℓ := by
  have := (neglog_bounds x hx0 hx1 n).2
  rw [hr, one_div, Real.log_inv]; linarith

theorem neglog_eq (x : ℝ) (_hx : x < 1) : -Real.log (1 - x) = Real.log (1 / (1 - x)) := by
  rw [one_div, Real.log_inv]

/-- `2 = (16/15)^7 (25/24)^5 (81/80)^3` -/
theorem log_two_eq :
    Real.log 2 = 7 * -Real.log (1 - 1 / 16) + 5 * -Real.log (1 - 1 / 25) +
      3 * -Real.log (1 - 1 / 81) := by
  rw [neglog_eq _ (by norm_num), neglog_eq _ (by norm_num), neglog_eq _ (by norm_num)]
  have h : (2 : ℝ) = (1 / (1 - 1 / 16)) ^ 7 * (1 / (1 - 1 / 25)) ^ 5 * (1 / (1 - 1 / 81)) ^ 3 := by
    norm_num
  conv_lhs => rw [h]
  rw [Real.log_mul (by positivity) (by positivity), Real.log_mul (by positivity) (by positivity),
    Real.log_pow, Real.log_pow, Real.log_pow]
  push_cast; ring

/-- `3 = (16/15)^11 (25/24)^8 (81/80)^5` -/
theorem log_three_eq :
    Real.log 3 = 11 * -Real.log (1 - 1 / 16) + 8 * -Real.log (1 - 1 / 25) +
      5 * -Real.log (1 - 1 / 81) := by
  rw [neglog_eq _ (by norm_num), neglog_eq _ (by norm_num), neglog_eq _ (by norm_num)]
  have h : (3 : ℝ) = (1 / (1 - 1 / 16)) ^ 11 * (1 / (1 - 1 / 25)) ^ 8 * (1 / (1 - 1 / 81)) ^ 5 := by
    norm_num
  conv_lhs => rw [h]
  rw [Real.log_mul (by positivity) (by positivity), Real.log_mul (by positivity) (by positivity),
    Real.log_pow, Real.log_pow, Real.log_pow]
  push_cast; ring

/-- `5 = (16/15)^16 (25/24)^12 (81/80)^7` (main's `log5_identity`) -/
theorem log_five_eq :
    Real.log 5 = 16 * -Real.log (1 - 1 / 16) + 12 * -Real.log (1 - 1 / 25) +
      7 * -Real.log (1 - 1 / 81) := by
  rw [neglog_eq _ (by norm_num), neglog_eq _ (by norm_num), neglog_eq _ (by norm_num)]
  have h : (5 : ℝ) = (1 / (1 - 1 / 16)) ^ 16 * (1 / (1 - 1 / 25)) ^ 12 * (1 / (1 - 1 / 81)) ^ 7 := by
    norm_num
  conv_lhs => rw [h]
  rw [Real.log_mul (by positivity) (by positivity), Real.log_mul (by positivity) (by positivity),
    Real.log_pow, Real.log_pow, Real.log_pow]
  push_cast; ring

/-- 17-digit enclosures of `log 2`, `log 3`, `log 5` -/
theorem log_two_bounds :
    (69314718055994530 : ℝ) / 10 ^ 17 < Real.log 2 ∧
      Real.log 2 < (69314718055994531 : ℝ) / 10 ^ 17 := by
  have a := neglog_bounds (1 / 16) (by norm_num) (by norm_num) 16
  have b := neglog_bounds (1 / 25) (by norm_num) (by norm_num) 14
  have c := neglog_bounds (1 / 81) (by norm_num) (by norm_num) 10
  unfold Lo Up ps at a b c
  simp only [Finset.sum_range_succ, Finset.sum_range_zero] at a b c
  norm_num at a b c
  rw [log_two_eq]
  constructor <;> linarith [a.1, a.2, b.1, b.2, c.1, c.2]

theorem log_three_bounds :
    (109861228866810969 : ℝ) / 10 ^ 17 < Real.log 3 ∧
      Real.log 3 < (109861228866810970 : ℝ) / 10 ^ 17 := by
  have a := neglog_bounds (1 / 16) (by norm_num) (by norm_num) 16
  have b := neglog_bounds (1 / 25) (by norm_num) (by norm_num) 14
  have c := neglog_bounds (1 / 81) (by norm_num) (by norm_num) 10
  unfold Lo Up ps at a b c
  simp only [Finset.sum_range_succ, Finset.sum_range_zero] at a b c
  norm_num at a b c
  rw [log_three_eq]
  constructor <;> linarith [a.1, a.2, b.1, b.2, c.1, c.2]

theorem log_five_bounds :
    (160943791243410037 : ℝ) / 10 ^ 17 < Real.log 5 ∧
      Real.log 5 < (160943791243410038 : ℝ) / 10 ^ 17 := by
  have a := neglog_bounds (1 / 16) (by norm_num) (by norm_num) 16
  have b := neglog_bounds (1 / 25) (by norm_num) (by norm_num) 14
  have c := neglog_bounds (1 / 81) (by norm_num) (by norm_num) 10
  unfold Lo Up ps at a b c
  simp only [Finset.sum_range_succ, Finset.sum_range_zero] at a b c
  norm_num at a b c
  rw [log_five_eq]
  constructor <;> linarith [a.1, a.2, b.1, b.2, c.1, c.2]

/-- `log 21952 = 14 log 2 - log (1 - 87/343)`, since `21952 = 2^14 · 343/256` -/
theorem log_21952_lt : Real.log 21952 < (99966136 : ℝ) / 10 ^ 7 := by
  have h : Real.log 21952 = 14 * Real.log 2 + -Real.log (1 - 87 / 343) := by
    have e : (21952 : ℝ) = 2 ^ 14 * (1 / (1 - 87 / 343)) := by norm_num
    rw [e, Real.log_mul (by positivity) (by norm_num), Real.log_pow, neglog_eq _ (by norm_num)]
    push_cast; ring
  have a := (neglog_bounds (87 / 343) (by norm_num) (by norm_num) 16).2
  unfold Up ps at a
  simp only [Finset.sum_range_succ, Finset.sum_range_zero] at a
  norm_num at a
  have h2 := log_two_bounds.2
  rw [h]; linarith

/-- `log 28 = 5 log 2 + log (1 - 1/8)` -/
theorem log_28_lt : Real.log 28 < (33322046 : ℝ) / 10 ^ 7 := by
  have h : Real.log 28 = 5 * Real.log 2 - -Real.log (1 - 1 / 8) := by
    have e : (28 : ℝ) = 2 ^ 5 * (1 - 1 / 8) := by norm_num
    rw [e, Real.log_mul (by positivity) (by norm_num), Real.log_pow]
    push_cast; ring
  have a := (neglog_bounds (1 / 8) (by norm_num) (by norm_num) 12).1
  unfold Lo ps at a
  simp only [Finset.sum_range_succ, Finset.sum_range_zero] at a
  norm_num at a
  have h2 := log_two_bounds.2
  rw [h]; linarith

/-- `log 30 = log 2 + log 3 + log 5` -/
theorem log_30_lt : Real.log 30 < (340119738166215539 : ℝ) / 10 ^ 17 := by
  have h : Real.log 30 = Real.log 2 + Real.log 3 + Real.log 5 := by
    rw [← Real.log_mul (by norm_num) (by norm_num), ← Real.log_mul (by norm_num) (by norm_num)]
    norm_num
  rw [h]; linarith [log_two_bounds.2, log_three_bounds.2, log_five_bounds.2]

/-- `log 27000 = 3 log 30` -/
theorem log_27000_lt : Real.log 27000 < (1020359214498646617 : ℝ) / 10 ^ 17 := by
  have h : Real.log 27000 = 3 * Real.log 30 := by
    have e : (27000 : ℝ) = 30 ^ 3 := by norm_num
    rw [e, Real.log_pow]; push_cast; ring
  rw [h]; linarith [log_30_lt]

/-! ## The Taylor bound of PR #10's bulk complex guard -/

/-- `(1 - t)^(6/5) ≤ 1 - 6t/5 + (3/25) t²/(1 - t)` for `0 < t < 1` -/
theorem taylor_six_fifths (t : ℝ) (ht0 : 0 < t) (ht1 : t < 1) :
    (1 - t) ^ ((6 : ℝ) / 5) ≤ 1 - 6 / 5 * t + 3 / 25 * (t ^ 2 / (1 - t)) := by
  have hu0 : 0 < 1 - t := by linarith
  set w := (1 - t) ^ ((1 : ℝ) / 5) with hw
  have hw0 : 0 < w := Real.rpow_pos_of_pos hu0 _
  have hw5 : w ^ 5 = 1 - t := by
    rw [hw, ← Real.rpow_natCast, ← Real.rpow_mul hu0.le]; norm_num
  have hw6 : (1 - t) ^ ((6 : ℝ) / 5) = w ^ 6 := by
    rw [hw, ← Real.rpow_natCast, ← Real.rpow_mul hu0.le]; norm_num
  have hw1 : w ≤ 1 := Real.rpow_le_one hu0.le (by linarith) (by norm_num)
  have ht : t = 1 - w ^ 5 := by linarith
  rw [hw6, ← hw5, ht]
  have hw5pos : 0 < w ^ 5 := by positivity
  have key : 1 - 6 / 5 * (1 - w ^ 5) + 3 / 25 * ((1 - w ^ 5) ^ 2 / w ^ 5) - w ^ 6 =
      (1 - w) ^ 3 * (3 + 9 * w + 18 * w ^ 2 + 30 * w ^ 3 + 45 * w ^ 4 + 52 * w ^ 5 +
        51 * w ^ 6 + 42 * w ^ 7 + 25 * w ^ 8) / (25 * w ^ 5) := by
    field_simp; ring
  have hq : 0 ≤ (1 - w) ^ 3 * (3 + 9 * w + 18 * w ^ 2 + 30 * w ^ 3 + 45 * w ^ 4 + 52 * w ^ 5 +
        51 * w ^ 6 + 42 * w ^ 7 + 25 * w ^ 8) / (25 * w ^ 5) := by
    have : 0 ≤ 1 - w := by linarith
    positivity
  linarith

end PRChecksC
