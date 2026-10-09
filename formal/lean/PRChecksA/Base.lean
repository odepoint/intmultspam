import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Complex.ExponentialBounds

/-!
# Shared definitions for the PR #3 / #4 / #8 checks

Copied or generalized from main's Lean check (`formal/lean/KappaCheck`, branch
`lean-certificate-check`, commit `f99d715`):

* `v, N, m, I, zc` are `KappaCheck.Network`'s count formulas;
* `exponent_certificate` is `KappaCheck.Certificates.exponent_certificate` verbatim;
* `log_le_of_pow` is `KappaCheck.CrocSwap.log_le_of_pow`; `log_split_upper` generalizes
  `log_split` to any `y ≤ q^n`, and `log_split_lower` generalizes `log_15625_gt`;
* `gaussian_cutoff_general` generalizes `gaussian_cutoff` from `ε = 1999/10000` to every
  `ε ≤ 1/5`;
* `Params` and its fields `g1 … g7`, the recurrence exponents and the 31 constraint slacks
  transcribe `scripts/certify.py` `constraints`/`margins` with
  `layout_model='nonadjacent'`, `assembly_model='tight-gaussian'`, and with
  `packed_overhead` and `reserved_axes` replaced as in `scripts/compact_control_layer.py`
  (the base scripts are unchanged in all three PRs).  Each slack has the JSON key's name.
-/

namespace PRChecksA

open Real

/-! ## Count formulas (main's `Network.lean`) -/

/-- number of three-element subsets of `[h]` -/
def v (h : ℕ) : ℕ := h.choose 3
def N (h : ℕ) : ℕ := v h ^ 3
def m (h : ℕ) : ℕ := h ^ 3
/-- number of invocations `3 v^2` -/
def I (h : ℕ) : ℕ := 3 * v h ^ 2
/-- the original complex motif's side wires per target, `C(h-3,3) + 3(h-3)` -/
def zc (h : ℕ) : ℕ := (h - 3).choose 3 + 3 * (h - 3)

/-! ## The generic exponent certificate (main's `Certificates.lean`, verbatim) -/

/-- General certificate: if `x > 0`, `x * L ≤ η`, `log m < L`, `m > 0` and
`r = m (1 - η)`, then `r < m ^ (1 - x)`. -/
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

/-! ## Logarithm bounds -/

/-- `log y < n (q - 1)` whenever `y ≤ q^n`, `n > 0` and `q ≠ 1` (main's `log_le_of_pow`) -/
theorem log_le_of_pow (y q : ℝ) (n : ℕ) (hy : 0 < y) (hq : 0 < q) (hq1 : q ≠ 1) (hn : 0 < n)
    (h : y ≤ q ^ n) : Real.log y < n * (q - 1) := by
  calc Real.log y ≤ Real.log (q ^ n) := Real.log_le_log hy h
    _ = n * Real.log q := by rw [Real.log_pow]
    _ < n * (q - 1) := by
        gcongr; exact Real.log_lt_sub_one_of_pos hq hq1

/-- `log (2^k y) < k · 0.6931471808 + n (q - 1)` whenever `0 < y ≤ q^n` -/
theorem log_split_upper (k n : ℕ) (y q : ℝ) (hy : 0 < y) (hq : 0 < q) (hq1 : q ≠ 1)
    (hn : 0 < n) (h : y ≤ q ^ n) :
    Real.log (2 ^ k * y) < k * (6931471808 / 10 ^ 10) + n * (q - 1) := by
  have hy' := log_le_of_pow y q n hy hq hq1 hn h
  have h2 : Real.log 2 < 0.6931471808 := Real.log_two_lt_d9
  rw [Real.log_mul (by positivity) hy.ne', Real.log_pow]
  have : (k : ℝ) * Real.log 2 ≤ k * (6931471808 / 10 ^ 10) := by
    have : Real.log 2 ≤ 6931471808 / 10 ^ 10 := by norm_num at h2 ⊢; linarith
    exact mul_le_mul_of_nonneg_left this (by positivity)
  linarith

/-- `k · 0.6931471803 + (1 - 1/y) < log (2^k y)` for `y > 0` -/
theorem log_split_lower (k : ℕ) (y : ℝ) (hy : 0 < y) :
    k * (6931471803 / 10 ^ 10) + (1 - 1 / y) ≤ Real.log (2 ^ k * y) := by
  have h2 : 0.6931471803 < Real.log 2 := Real.log_two_gt_d9
  have hl : 1 - 1 / y ≤ Real.log y := by
    have := Real.log_le_sub_one_of_pos (show 0 < 1 / y by positivity)
    rw [one_div, Real.log_inv] at this
    rw [one_div]; linarith
  rw [Real.log_mul (by positivity) hy.ne', Real.log_pow]
  have : (k : ℝ) * (6931471803 / 10 ^ 10) ≤ k * Real.log 2 := by
    have : (6931471803 / 10 ^ 10 : ℝ) ≤ Real.log 2 := by norm_num at h2 ⊢; linarith
    exact mul_le_mul_of_nonneg_left this (by positivity)
  linarith

/-! ## The Gaussian cutoff for every `ε ≤ 1/5` -/

/-- `b ≥ 2^40` implies `46 b^((1+3ε)/2) ≤ b/4` whenever `ε ≤ 1/5` (generalizes main's
`gaussian_cutoff`; the retained Gaussian setup needs exactly this) -/
theorem gaussian_cutoff_general (ε b : ℝ) (hε : ε ≤ 1 / 5) (hb : (2 : ℝ) ^ 40 ≤ b) :
    46 * b ^ ((1 + 3 * ε) / 2) ≤ b / 4 := by
  have hb0 : 0 < b := lt_of_lt_of_le (by norm_num) hb
  have hb1 : 1 ≤ b := le_trans (by norm_num) hb
  have hmono : b ^ ((1 + 3 * ε) / 2) ≤ b ^ ((4 : ℝ) / 5) :=
    Real.rpow_le_rpow_of_exponent_le hb1 (by linarith)
  have hsplit : b ^ ((4 : ℝ) / 5) = b / b ^ ((1 : ℝ) / 5) := by
    rw [show (4 : ℝ) / 5 = 1 - 1 / 5 by norm_num, Real.rpow_sub hb0, Real.rpow_one]
  have hX : (256 : ℝ) ≤ b ^ ((1 : ℝ) / 5) := by
    have h1 : ((2 : ℝ) ^ 40) ^ ((1 : ℝ) / 5) ≤ b ^ ((1 : ℝ) / 5) :=
      Real.rpow_le_rpow (by positivity) hb (by norm_num)
    have h2 : ((2 : ℝ) ^ 40) ^ ((1 : ℝ) / 5) = 256 := by
      rw [show ((2 : ℝ) ^ 40) = (256 : ℝ) ^ (5 : ℕ) by norm_num, ← Real.rpow_natCast,
        ← Real.rpow_mul (by norm_num)]
      norm_num
    linarith
  have hXpos : 0 < b ^ ((1 : ℝ) / 5) := Real.rpow_pos_of_pos hb0 _
  calc 46 * b ^ ((1 + 3 * ε) / 2) ≤ 46 * b ^ ((4 : ℝ) / 5) := by gcongr
    _ = 46 * (b / b ^ ((1 : ℝ) / 5)) := by rw [hsplit]
    _ ≤ 46 * (b / 256) := by gcongr
    _ ≤ b / 4 := by linarith

/-! ## Parameters, recurrence exponents, slacks and margins (`scripts/certify.py`) -/

structure Params where
  tau : ℚ
  sigma : ℚ
  epsilon : ℚ
  c : ℚ
  lam : ℚ
  lamp : ℚ
  kappa : ℚ
  beta : ℚ
  delta : ℚ
  C1 : ℚ

namespace Params

variable (p : Params)

/-! Recurrence exponents (`compact_control_layer.layer_exponents`, `theta = 0`) -/
def internal : ℚ := p.tau + (1 - p.beta) * max (p.sigma - p.tau) 0
def leaf : ℚ := p.sigma + p.beta * (1 - p.sigma)
def preprocessing : ℚ := max 0 (1 - p.c)
def layer : ℚ := max (max p.internal p.leaf) (max (1 - p.c) 0)

/-! The 31 constraint slacks, named as in the certificates -/
def tau_positive : ℚ := p.tau
def tau_below_one : ℚ := 1 - p.tau
def sigma_positive : ℚ := p.sigma
def sigma_below_one : ℚ := 1 - p.sigma
def c_positive : ℚ := p.c
def epsilon_positive : ℚ := p.epsilon
def beta_positive : ℚ := p.beta
def beta_below_one : ℚ := 1 - p.beta
def lambda_above_tau : ℚ := p.lam - p.tau
def lambda_above_sigma : ℚ := p.lam - p.sigma
def lambda_below_one : ℚ := 1 - p.lam
/-- compact controls: `λ - internal` replaces `λ - τ(1 + c/β)` -/
def packed_overhead : ℚ := p.lam - p.internal
def lambda_prime_above_lambda : ℚ := p.lamp - p.lam
def leaf_cost : ℚ := p.lamp - (p.sigma + p.beta * (1 - p.sigma))
def lambda_prime_below_one : ℚ := 1 - p.lamp
def guard_width : ℚ := 1 - p.epsilon * p.C1
def dimension_upper_bound : ℚ := 1 / 3 - p.epsilon
/-- nonadjacent layout: degree 1 -/
def crt_layout : ℚ := 1 - p.tau - p.epsilon * (1 - p.tau)
/-- tight Gaussian: `5/4` -/
def gaussian_cost : ℚ := 1 / 4 - p.delta - 5 / 4 * p.epsilon
def prefix_cost : ℚ := 1 - p.epsilon * (1 + p.c)
def scalar_cost : ℚ := 1 - p.delta - p.epsilon
def delta_positive : ℚ := p.delta
def delta_below_one_eighth : ℚ := 1 / 8 - p.delta
def prime_interval_growth : ℚ := 1 - 2 * p.epsilon
def alpha_below_sqrt_p : ℚ := 1 / 4 - p.epsilon / 4
def gamma_sublinear : ℚ := 1 / 2 - 3 / 2 * p.epsilon
def K_smaller_than_ell : ℚ := 1 - p.epsilon - p.epsilon * p.c
def K_dominates_log_p : ℚ := p.epsilon * p.c
def r_superpolynomial : ℚ := 1 - p.epsilon
def kappa_positive : ℚ := p.kappa
/-- compact controls: `λ' - preprocessing` -/
def reserved_axes : ℚ := p.lamp - p.preprocessing

/-! The seven assembly margins (nonadjacent, tight Gaussian) -/
def g1 : ℚ := 1 - p.epsilon * (1 + p.c)
def g2 : ℚ := p.epsilon * p.c * (1 - p.tau)
def g3 : ℚ := p.epsilon * (1 - p.lamp)
def g4 : ℚ := 1 - p.tau - p.epsilon * (1 - p.tau)
def g5 : ℚ := 1 / 4 - p.delta - 5 / 4 * p.epsilon
def g6 : ℚ := 1 - p.delta - p.epsilon
def g7 : ℚ := p.epsilon

/-- `min g_i` -/
def gmin : ℚ := min (min (min p.g1 p.g2) (min p.g3 p.g4)) (min (min p.g5 p.g6) p.g7)

/-- all 31 slacks are positive -/
def AllSlacksPositive : Prop :=
  0 < p.tau_positive ∧ 0 < p.tau_below_one ∧ 0 < p.sigma_positive ∧ 0 < p.sigma_below_one ∧
  0 < p.c_positive ∧ 0 < p.epsilon_positive ∧ 0 < p.beta_positive ∧ 0 < p.beta_below_one ∧
  0 < p.lambda_above_tau ∧ 0 < p.lambda_above_sigma ∧ 0 < p.lambda_below_one ∧
  0 < p.packed_overhead ∧ 0 < p.lambda_prime_above_lambda ∧ 0 < p.leaf_cost ∧
  0 < p.lambda_prime_below_one ∧ 0 < p.guard_width ∧ 0 < p.dimension_upper_bound ∧
  0 < p.crt_layout ∧ 0 < p.gaussian_cost ∧ 0 < p.prefix_cost ∧ 0 < p.scalar_cost ∧
  0 < p.delta_positive ∧ 0 < p.delta_below_one_eighth ∧ 0 < p.prime_interval_growth ∧
  0 < p.alpha_below_sqrt_p ∧ 0 < p.gamma_sublinear ∧ 0 < p.K_smaller_than_ell ∧
  0 < p.K_dominates_log_p ∧ 0 < p.r_superpolynomial ∧ 0 < p.kappa_positive ∧
  0 < p.reserved_axes

/-- the final absorption: every margin exceeds `κ` -/
def Absorbs : Prop :=
  p.kappa < p.g1 ∧ p.kappa < p.g2 ∧ p.kappa < p.g3 ∧ p.kappa < p.g4 ∧ p.kappa < p.g5 ∧
  p.kappa < p.g6 ∧ p.kappa < p.g7

theorem absorbs_iff_gmin : p.Absorbs ↔ p.kappa < p.gmin := by
  simp only [Absorbs, gmin, lt_min_iff]; tauto

end Params

/-- unfold every `Params` exponent, slack, margin and predicate (then call `norm_num`) -/
macro "params_unfold" : tactic => `(tactic| (simp only [Params.AllSlacksPositive,
  Params.Absorbs, Params.gmin, Params.internal, Params.leaf, Params.preprocessing,
  Params.layer, Params.tau_positive, Params.tau_below_one, Params.sigma_positive,
  Params.sigma_below_one, Params.c_positive, Params.epsilon_positive, Params.beta_positive,
  Params.beta_below_one, Params.lambda_above_tau, Params.lambda_above_sigma,
  Params.lambda_below_one, Params.packed_overhead, Params.lambda_prime_above_lambda,
  Params.leaf_cost, Params.lambda_prime_below_one, Params.guard_width,
  Params.dimension_upper_bound, Params.crt_layout, Params.gaussian_cost, Params.prefix_cost,
  Params.scalar_cost, Params.delta_positive, Params.delta_below_one_eighth,
  Params.prime_interval_growth, Params.alpha_below_sqrt_p, Params.gamma_sublinear,
  Params.K_smaller_than_ell, Params.K_dominates_log_p, Params.r_superpolynomial,
  Params.kappa_positive, Params.reserved_axes, Params.g1, Params.g2, Params.g3, Params.g4,
  Params.g5, Params.g6, Params.g7]))

end PRChecksA
