import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# The generic exponent certificate

For a network with `W` wires, label dimension `m` and rank sum `s < W m`, the swap and
layer recursions need a rational exponent `1 - x` with `s / W < m ^ (1 - x)`.  Writing
`η = 1 - s / (W m)`, it suffices that `x * L ≤ η` for some `L > log m`, because
`m ^ (-x) = exp (-x log m) ≥ 1 - x log m`.  This is the argument of
`upstream/build/sections/03-motifs.tex` lines 686-691 and of
`notes/independent-complex.tex` lines 48-51.
-/

namespace KappaCheck.Certificates

open Real

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

end KappaCheck.Certificates
