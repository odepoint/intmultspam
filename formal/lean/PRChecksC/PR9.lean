import PRChecksC.Common
import PRChecksC.Assembly

/-!
# PR #9: refined ternary star templates, conditional κ = 19/(5·10⁹) = 3.8·10⁻⁹

Source: `research/prime-field-followup/` at PR head `cfd6a2b` (worktree `/home/user/prs/pr9`):
`README.md`, `verify.py` (`witness`, `guard`), `certificate.json` (`witness.*`) and the
vendored PR #7 certificate `vendor/prime-field28.json`.

**Taken as given** (outputs of running the circuits, not re-derived here):
* `c_add = 10687362` producer additions and `q_out = 983178` designated output uses of the
  refined h = 28 bit producer (`certificate.json` `independent_cpp_check`), hence
  `R = c + q = 11670540` roles per invocation;
* PR #7's numbers `10857762` additions and the star counts `2623060 → 2452660`;
* the retained PR #7 complex network: `Rc = 93838` side roles and `61022` additions
  (`vendor/prime-field28.json` `witness.complex`).
The count formulas are PR #7's (`scripts/prime_field_network.py` `bit_counts`,
`complex_counts`), restated in `verify.py`; their network proofs are not checked here.
-/

namespace PRChecksC.PR9

open PRChecksC Real

/-! ## Bit network: h = 28, five-subsets -/

/-- TAKEN AS GIVEN: additions `c` of the refined producer (circuit output) -/
def c_add : ℕ := 10687362
/-- TAKEN AS GIVEN: designated output uses `q` (circuit output) -/
def q_out : ℕ := 983178
/-- auxiliary roles per invocation, `R = c + q` -/
def R : ℕ := c_add + q_out

def v : ℕ := Nat.choose 28 5
def m : ℕ := 28 ^ 3
def N : ℕ := v ^ 3
def W : ℕ := 2 * v ^ 2 * (v + R)
def L : ℕ := 3 * v ^ 2 * Nat.choose 28 2 * (28 - 2)
def D : ℕ := N - 2 * L
def s : ℕ := W * m - D

/-- README table: `R = c + q`, the 170400 saved additions, PR #7's `R = 11840940` -/
theorem roles :
    Nat.choose 28 4 = 20475 ∧ R = 11670540 ∧ 10857762 + q_out = 11840940 ∧ 10857762 - 170400 = c_add ∧
    2623060 - 170400 = 2452660 ∧ 11840940 - 170400 = R := by
  norm_num [R, c_add, q_out, Nat.choose]

theorem bit_counts :
    v = 98280 ∧ m = 21952 ∧ N = 949282431552000 ∧ W = 227349085594176000 ∧
    L = 284784729465600 ∧ D = 379712972620800 ∧ s = 4990766747250378931200 := by
  simp only [v, m, N, W, L, D, s, R, c_add, q_out]; norm_num [Nat.choose]

theorem bit_eta : ((D : ℕ) : ℚ) / ((W : ℕ) * (m : ℕ)) = 117 / 1537792480 := by
  simp only [v, m, N, W, L, D, R, c_add, q_out]; norm_num [Nat.choose]

/-- `log 21952 < 9.9966136`, and `(761/10¹¹) · 9.9966136 ≤ η` -/
theorem bit_log : Real.log 21952 < 99966136 / 10 ^ 7 ∧
    (761 / 10 ^ 11 : ℝ) * (99966136 / 10 ^ 7) ≤ 117 / 1537792480 :=
  ⟨log_21952_lt, by norm_num⟩

/-- the certified bit saving `a_b = 761/10¹¹`: `s/W < m^(1 - a_b)` -/
theorem bit_exponent :
    ((s : ℕ) : ℝ) / (W : ℕ) < (21952 : ℝ) ^ (1 - (761 / 10 ^ 11 : ℝ)) := by
  obtain ⟨-, -, -, hW, -, -, hs⟩ := bit_counts
  rw [hs, hW]
  apply exponent_certificate 21952 (99966136 / 10 ^ 7) (761 / 10 ^ 11) (117 / 1537792480) _
    (by norm_num) (by norm_num) log_21952_lt (by norm_num)
  norm_num

/-! ## Retained PR #7 complex network: h = 28, triples -/

/-- TAKEN AS GIVEN: side roles of PR #7's paired complex producer (circuit output) -/
def Rc : ℕ := 93838
/-- TAKEN AS GIVEN: additions of that producer (circuit output) -/
def additions_c : ℕ := 61022

def vc : ℕ := Nat.choose 28 3
def Nc : ℕ := vc ^ 3
def Ic : ℕ := 3 * vc ^ 2
def Wc : ℕ := 2 * vc ^ 2 * (vc + Rc + 28 + 1)
def Lc : ℕ := Ic * 28 * (28 + 1)
def Dc : ℕ := 2 * Nc - 2 * Lc
def sc : ℕ := Wc * m - Dc
def gates : ℕ := Ic * (4 * (additions_c + vc) + 4 * vc + 4)

theorem complex_counts :
    vc = 3276 ∧ Nc = 35158608576 ∧ Ic = 32196528 ∧ Wc = 2085111546336 ∧
    Lc = 26143580736 ∧ Dc = 18030055680 ∧ sc = 45772350635112192 ∧
    gates = 8702721518400 ∧ gates ≤ 12 * Wc := by
  simp only [vc, Nc, Ic, Wc, Lc, Dc, sc, gates, m, Rc, additions_c]; norm_num [Nat.choose]

theorem complex_eta : ((Dc : ℕ) : ℚ) / ((Wc : ℕ) * (m : ℕ)) = 5 / 12693352 := by
  simp only [vc, Nc, Ic, Wc, Lc, Dc, m, Rc]; norm_num [Nat.choose]

/-- the retained complex saving `a_c = 39/10⁹`, with `log 21952 < 10` -/
theorem complex_exponent :
    ((sc : ℕ) : ℝ) / (Wc : ℕ) < (21952 : ℝ) ^ (1 - (39 / 10 ^ 9 : ℝ)) := by
  obtain ⟨-, -, -, hW, -, -, hs, -, -⟩ := complex_counts
  rw [hs, hW]
  have hlog : Real.log 21952 < 10 := by have := log_21952_lt; linarith
  apply exponent_certificate 21952 10 (39 / 10 ^ 9) (5 / 12693352) _
    (by norm_num) (by norm_num) hlog (by norm_num)
  norm_num

/-! ## Guard (`verify.py` `guard`, main's guard formula with the PR #7 complex network) -/

def E : ℕ := 64 * (Wc + m + 1) ^ 3
def B : ℕ := sc + E
def ζq : ℚ := 1 / 10000
def C0 : ℕ :=
  1330227007428750171975003167066483053874539349448633868671027791264533942584236249186304

theorem guard_constants :
    E = 580186831374453739191483276086074980416 ∧
    B = 580186831374453739191529048436710092608 ∧
    3 ≤ m ∧ 2 ≤ sc ∧ sc < m ^ 5 ∧ sc * (8 + E) ≤ 9 * B ^ 2 ∧
    -- `C0 = ⌈max(128 m B², 18 m B² (1 + 1/ζ))⌉` (an integer) and the layer inequality
    (C0 : ℚ) = max (128 * 21952 * (B : ℚ) ^ 2) (18 * 21952 * (B : ℚ) ^ 2 * (1 + 1 / ζq)) ∧
    9 * 21952 * (B : ℚ) ^ 2 * (1 + 1 / ζq) + 18 ≤ C0 ∧
    36 * Wc ^ 3 + 4 * sc + 4 * Wc + 4 < E ∧
    (5 : ℚ) - 4 * (19 / 25) + ζq = 19601 / 10000 := by
  simp only [E, B, C0, ζq, vc, Nc, Ic, Wc, Lc, Dc, sc, m, Rc]
  norm_num [Nat.choose]

/-! ## Assembly -/

/-- `verify.py` `witness`: τ = 1 - 761/10¹¹, σ = 1 - 39/10⁹, ... -/
def P : Params where
  τ := 99999999239 / 100000000000
  σ := 999999961 / 1000000000
  ε := 4999 / 10000
  c := 9999 / 10000
  lam := 999999992391 / 1000000000000
  lamp := 124999999049 / 125000000000
  κ := 19 / 5000000000
  β := 19 / 25
  δ := 1 / 1000000
  C1 := 19601 / 10000

/-- the README's parameter table -/
theorem parameter_origin :
    P.τ = 1 - 761 / 10 ^ 11 ∧ P.σ = 1 - 39 / 10 ^ 9 ∧ P.lam = 1 - 7609 / 10 ^ 12 ∧
    P.lamp = 1 - 7608 / 10 ^ 12 ∧ P.κ = 38 / 10 ^ 10 ∧ P.C1 = 5 - 4 * P.β + ζq := by
  norm_num [P, ζq]

theorem recurrence_values :
    P.internal = 99999999239 / 100000000000 ∧ P.leaf = 12499999883 / 12500000000 ∧
    P.preprocessing = 1 / 10000 ∧ P.layer = 99999999239 / 100000000000 := by
  norm_num [P]

theorem slack_values :
    P.tau_positive = 99999999239 / 100000000000 ∧
    P.tau_below_one = 761 / 100000000000 ∧
    P.sigma_positive = 999999961 / 1000000000 ∧
    P.sigma_below_one = 39 / 1000000000 ∧
    P.c_positive = 9999 / 10000 ∧
    P.epsilon_positive = 4999 / 10000 ∧
    P.beta_positive = 19 / 25 ∧
    P.beta_below_one = 6 / 25 ∧
    P.lambda_above_tau = 1 / 1000000000000 ∧
    P.lambda_above_sigma = 31391 / 1000000000000 ∧
    P.lambda_below_one = 7609 / 1000000000000 ∧
    P.packed_overhead = 1 / 1000000000000 ∧
    P.lambda_prime_above_lambda = 1 / 1000000000000 ∧
    P.leaf_cost = 219 / 125000000000 ∧
    P.lambda_prime_below_one = 951 / 125000000000 ∧
    P.guard_width = 2014601 / 100000000 ∧
    P.crt_layout = 3805761 / 1000000000000000 ∧
    P.gaussian_cost = 199 / 1000000 ∧
    P.prefix_cost = 24999 / 100000000 ∧
    P.scalar_cost = 500099 / 1000000 ∧
    P.delta_positive = 1 / 1000000 ∧
    P.delta_below_one_eighth = 124999 / 1000000 ∧
    P.prime_interval_growth = 1 / 5000 ∧
    P.alpha_squared_theta_growth = 1 / 5000 ∧
    P.K_smaller_than_ell = 24999 / 100000000 ∧
    P.K_dominates_log_p = 49985001 / 100000000 ∧
    P.r_superpolynomial = 5001 / 10000 ∧
    P.kappa_positive = 19 / 5000000000 ∧
    P.reserved_axes = 124987499049 / 125000000000 := by
  norm_num [P]

theorem constraints_strict : P.AllStrict := by
  unfold Params.AllStrict; norm_num [P]

theorem margin_values :
    P.g1 = 24999 / 100000000 ∧
    P.g2 = 38038585761 / 10000000000000000000 ∧
    P.g3 = 4754049 / 1250000000000000 ∧
    P.g4 = 3805761 / 1000000000000000 ∧
    P.g5 = 199 / 1000000 ∧
    P.g6 = 500099 / 1000000 ∧
    P.g7 = 4999 / 10000 := by
  norm_num [P]

/-- **Headline**: `min g = g3 = 4754049/(1.25·10¹⁵) > κ = 19/(5·10⁹)`, gap
`4049/(1.25·10¹⁵)`, `2⁻²⁸ < κ`, `κ / (373/10¹¹) = 380/373`, and the bit/complex savings used
by the parameters are exactly the certified ones. -/
theorem kappa_witness :
    P.G3Min ∧ P.g3 - P.κ = 4049 / 1250000000000000 ∧
    (1 : ℚ) / 2 ^ 28 < P.κ ∧ P.κ / (373 / 10 ^ 11) = 380 / 373 ∧
    P.g3 = 38032392 / 10 ^ 16 ∧ 1 - P.τ = 761 / 10 ^ 11 ∧ 1 - P.σ = 39 / 10 ^ 9 := by
  unfold Params.G3Min; norm_num [P]

end PRChecksC.PR9
