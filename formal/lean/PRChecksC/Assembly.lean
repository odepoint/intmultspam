import Mathlib.Tactic

/-!
# The assembly constraints and margins shared by PRs #9, #10 and #12

All three PRs use `scripts/certify.py`'s `constraints(p, layout_model='nonadjacent',
assembly_model='tight-gaussian')` modified as in `scripts/fast_gaussian.py`
(`fast_constraints`, `fast_margins`; PR #9 inlines the same edits in
`research/prime-field-followup/verify.py` `witness`):

* drop `gaussian_cost`, `dimension_upper_bound`, `alpha_below_sqrt_p`, `gamma_sublinear`;
* add `gaussian_cost = 1 - δ - 2ε` and `alpha_squared_theta_growth = 1 - 2ε`;
* replace `packed_overhead` by `λ - internal` and add `reserved_axes = λ' - preprocessing`,
  with `compact_control_layer.layer_exponents` (θ = 0):
  `internal = τ + (1-β) max(σ-τ, 0)`, `leaf = σ + β(1-σ)`, `preprocessing = max(0, 1-c)`;
* margins `g1..g7` of `certify.margins` with `g5 = 1 - δ - 2ε`.

That is 29 constraints. Each definition below is named exactly as its key in the JSON
certificates, so `drift.py` can pair them automatically.
-/

namespace PRChecksC

/-- `scripts/certify.py` `Parameters` -/
structure Params where
  τ : ℚ
  σ : ℚ
  ε : ℚ
  c : ℚ
  lam : ℚ
  lamp : ℚ
  κ : ℚ
  β : ℚ
  δ : ℚ
  C1 : ℚ

namespace Params

variable (p : Params)

@[simp] def internal : ℚ := p.τ + (1 - p.β) * max (p.σ - p.τ) 0
@[simp] def leaf : ℚ := p.σ + p.β * (1 - p.σ)
@[simp] def preprocessing : ℚ := max 0 (1 - p.c)
@[simp] def layer : ℚ := max (max p.internal p.leaf) (max (1 - p.c) 0)

/-! ### The 29 constraint slacks -/
@[simp] def tau_positive : ℚ := p.τ
@[simp] def tau_below_one : ℚ := 1 - p.τ
@[simp] def sigma_positive : ℚ := p.σ
@[simp] def sigma_below_one : ℚ := 1 - p.σ
@[simp] def c_positive : ℚ := p.c
@[simp] def epsilon_positive : ℚ := p.ε
@[simp] def beta_positive : ℚ := p.β
@[simp] def beta_below_one : ℚ := 1 - p.β
@[simp] def lambda_above_tau : ℚ := p.lam - p.τ
@[simp] def lambda_above_sigma : ℚ := p.lam - p.σ
@[simp] def lambda_below_one : ℚ := 1 - p.lam
@[simp] def packed_overhead : ℚ := p.lam - p.internal
@[simp] def lambda_prime_above_lambda : ℚ := p.lamp - p.lam
@[simp] def leaf_cost : ℚ := p.lamp - (p.σ + p.β * (1 - p.σ))
@[simp] def lambda_prime_below_one : ℚ := 1 - p.lamp
@[simp] def guard_width : ℚ := 1 - p.ε * p.C1
/-- nonadjacent layout: degree 1 -/
@[simp] def crt_layout : ℚ := 1 - p.τ - p.ε * (1 - p.τ)
/-- fast Gaussian resampling -/
@[simp] def gaussian_cost : ℚ := 1 - p.δ - 2 * p.ε
@[simp] def prefix_cost : ℚ := 1 - p.ε * (1 + p.c)
@[simp] def scalar_cost : ℚ := 1 - p.δ - p.ε
@[simp] def delta_positive : ℚ := p.δ
@[simp] def delta_below_one_eighth : ℚ := 1 / 8 - p.δ
@[simp] def prime_interval_growth : ℚ := 1 - 2 * p.ε
@[simp] def alpha_squared_theta_growth : ℚ := 1 - 2 * p.ε
@[simp] def K_smaller_than_ell : ℚ := 1 - p.ε - p.ε * p.c
@[simp] def K_dominates_log_p : ℚ := p.ε * p.c
@[simp] def r_superpolynomial : ℚ := 1 - p.ε
@[simp] def kappa_positive : ℚ := p.κ
@[simp] def reserved_axes : ℚ := p.lamp - p.preprocessing

/-- all 29 slacks are strictly positive -/
def AllStrict : Prop :=
  0 < p.tau_positive ∧ 0 < p.tau_below_one ∧ 0 < p.sigma_positive ∧ 0 < p.sigma_below_one ∧
  0 < p.c_positive ∧ 0 < p.epsilon_positive ∧ 0 < p.beta_positive ∧ 0 < p.beta_below_one ∧
  0 < p.lambda_above_tau ∧ 0 < p.lambda_above_sigma ∧ 0 < p.lambda_below_one ∧
  0 < p.packed_overhead ∧ 0 < p.lambda_prime_above_lambda ∧ 0 < p.leaf_cost ∧
  0 < p.lambda_prime_below_one ∧ 0 < p.guard_width ∧ 0 < p.crt_layout ∧
  0 < p.gaussian_cost ∧ 0 < p.prefix_cost ∧ 0 < p.scalar_cost ∧ 0 < p.delta_positive ∧
  0 < p.delta_below_one_eighth ∧ 0 < p.prime_interval_growth ∧
  0 < p.alpha_squared_theta_growth ∧ 0 < p.K_smaller_than_ell ∧ 0 < p.K_dominates_log_p ∧
  0 < p.r_superpolynomial ∧ 0 < p.kappa_positive ∧ 0 < p.reserved_axes

/-! ### The seven margins -/
@[simp] def g1 : ℚ := 1 - p.ε * (1 + p.c)
@[simp] def g2 : ℚ := p.ε * p.c * (1 - p.τ)
@[simp] def g3 : ℚ := p.ε * (1 - p.lamp)
@[simp] def g4 : ℚ := 1 - p.τ - p.ε * (1 - p.τ)
@[simp] def g5 : ℚ := 1 - p.δ - 2 * p.ε
@[simp] def g6 : ℚ := 1 - p.δ - p.ε
@[simp] def g7 : ℚ := p.ε

/-- `g3` is the minimum margin and exceeds `κ` -/
def G3Min : Prop :=
  p.g3 ≤ p.g1 ∧ p.g3 ≤ p.g2 ∧ p.g3 ≤ p.g4 ∧ p.g3 ≤ p.g5 ∧ p.g3 ≤ p.g6 ∧ p.g3 ≤ p.g7 ∧
  p.κ < p.g3

end Params

end PRChecksC
