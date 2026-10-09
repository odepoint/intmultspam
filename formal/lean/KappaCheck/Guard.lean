import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Complex.ExponentialBounds
import KappaCheck.CrocSwap

/-!
# The generalized stopped-depth guard (`notes/compact-control-guard.tex`)

The note assumes a dependency-depth bound `A` with

* `A(e) ≤ s A(e/m) + E` at an internal node (`e ≥ d^β`),
* `A(e) ≤ 8e` at a leaf (`e < d^β`),

and derives `A(e) ≤ s(8+E) d^(5-4β) ≤ 9B² d^(5-4β)` for every root `e ≤ d`, then the
whole-layer bound `A_layer ≤ 9mB²(1+1/ζ)d^C₁ + 18d ≤ C₀ d^C₁`.  Here both derivations
are proved for every function `A` satisfying the two hypotheses; that the tape
algorithm satisfies them is the retained upstream guard argument (an assumption).
-/

namespace KappaCheck.Guard

open Real Finset

/-- `Σ_{i<k} s^i ≤ s^k` for `s ≥ 2` -/
theorem geom_le (s : ℝ) (hs : 2 ≤ s) (k : ℕ) : ∑ i ∈ range k, s ^ i ≤ s ^ k := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [sum_range_succ, pow_succ]
    have : 0 ≤ s ^ k := pow_nonneg (by linarith) k
    nlinarith

/-- unrolling `k` internal levels: below `t · m^k`, `A(e) ≤ s^k · 8t + E Σ_{i<k} s^i` -/
theorem unroll (A : ℝ → ℝ) (s m E t : ℝ) (hs : 1 ≤ s) (hm : 1 < m) (hE : 0 ≤ E)
    (ht : 0 < t)
    (hint : ∀ e, t ≤ e → A e ≤ s * A (e / m) + E)
    (hleaf : ∀ e, 0 < e → e < t → A e ≤ 8 * e) :
    ∀ k : ℕ, ∀ e, 0 < e → e < t * m ^ k →
      A e ≤ s ^ k * (8 * t) + E * ∑ i ∈ range k, s ^ i := by
  intro k
  induction k with
  | zero =>
    intro e he het
    simp only [pow_zero, mul_one, one_mul, range_zero, sum_empty, mul_zero, add_zero] at het ⊢
    linarith [hleaf e he het]
  | succ k ih =>
    intro e he het
    have hsum : 0 ≤ ∑ i ∈ range (k + 1), s ^ i :=
      sum_nonneg (fun i _ => pow_nonneg (by linarith) i)
    have hsk : 1 ≤ s ^ (k + 1) := one_le_pow₀ hs
    by_cases hlt : e < t
    · have := hleaf e he hlt
      nlinarith
    · push_neg at hlt
      have hm0 : 0 < m := by linarith
      have hchild : e / m < t * m ^ k := by
        rw [div_lt_iff₀ hm0]; calc e < t * m ^ (k + 1) := het
          _ = t * m ^ k * m := by ring
      have hrec := ih (e / m) (div_pos he hm0) hchild
      have hstep := hint e hlt
      have hgeom : ∑ i ∈ range (k + 1), s ^ i = s * ∑ i ∈ range k, s ^ i + 1 := by
        rw [sum_range_succ', mul_sum]; simp [pow_succ, mul_comm]
      rw [hgeom, pow_succ]
      have hs0 : 0 ≤ s := by linarith
      calc A e ≤ s * A (e / m) + E := hstep
        _ ≤ s * (s ^ k * (8 * t) + E * ∑ i ∈ range k, s ^ i) + E := by gcongr
        _ = s ^ k * s * (8 * t) + E * (s * ∑ i ∈ range k, s ^ i + 1) := by ring

/-- `log 3 > 1`, so `m ≥ 3` gives `log m > 1` -/
theorem one_lt_log_three : 1 < Real.log 3 := by
  rw [Real.lt_log_iff_exp_lt (by norm_num)]
  have := Real.exp_one_lt_d9
  norm_num at this ⊢; linarith

/-- **Note lines 23-28**: for a root `0 < e ≤ d`, `A(e) ≤ s(8+E) d^(5-4β)`. -/
theorem root_bound (A : ℝ → ℝ) (s m E d β : ℝ) (hs : 2 ≤ s) (hsm : s < m ^ 5)
    (hm : 1 < m) (hE : 0 ≤ E) (hd : 1 ≤ d) (hβ0 : 0 ≤ β) (hβ1 : β ≤ 1)
    (hint : ∀ e, d ^ β ≤ e → A e ≤ s * A (e / m) + E)
    (hleaf : ∀ e, 0 < e → e < d ^ β → A e ≤ 8 * e)
    (e : ℝ) (he : 0 < e) (hed : e ≤ d) :
    A e ≤ s * (8 + E) * d ^ (5 - 4 * β) := by
  have hd0 : 0 < d := by linarith
  have hm0 : 0 < m := by linarith
  have hlogm : 0 < Real.log m := Real.log_pos hm
  have hlogd : 0 ≤ Real.log d := Real.log_nonneg hd
  set t := d ^ β with ht_def
  have ht : 0 < t := Real.rpow_pos_of_pos hd0 β
  set x := (1 - β) * Real.log d / Real.log m with hx_def
  have hx0 : 0 ≤ x := div_nonneg (mul_nonneg (by linarith) hlogd) hlogm.le
  set k := ⌊x⌋₊ + 1 with hk_def
  -- `d < t · m^k`
  have hmk : d ^ (1 - β) < m ^ k := by
    have h1 : m ^ x = d ^ (1 - β) := by
      rw [Real.rpow_def_of_pos hm0, Real.rpow_def_of_pos hd0, hx_def]
      congr 1; field_simp; ring
    rw [← h1, ← Real.rpow_natCast]
    exact (Real.rpow_lt_rpow_left_iff hm).2 (by push_cast [hk_def]; exact Nat.lt_floor_add_one x)
  have hcover : e < t * m ^ k := by
    have : d = t * d ^ (1 - β) := by
      rw [ht_def, ← Real.rpow_add hd0]; simp
    calc e ≤ d := hed
      _ = t * d ^ (1 - β) := this
      _ < t * m ^ k := by gcongr
  have hA := unroll A s m E t (by linarith) hm hE ht hint hleaf k e he hcover
  -- `s^k ≤ s · d^(5(1-β))`
  have hsk : s ^ k ≤ s * d ^ (5 * (1 - β)) := by
    have hs1 : 1 ≤ s := by linarith
    have hs0 : 0 < s := by linarith
    have hfl : s ^ ⌊x⌋₊ ≤ s ^ x := by
      rw [← Real.rpow_natCast]; exact Real.rpow_le_rpow_of_exponent_le hs1 (Nat.floor_le hx0)
    have hlogs : Real.log s < 5 * Real.log m := by
      have := Real.log_lt_log hs0 hsm
      rwa [Real.log_pow] at this
    have hsx : s ^ x ≤ d ^ (5 * (1 - β)) := by
      rw [Real.rpow_def_of_pos hs0, Real.rpow_def_of_pos hd0]
      apply Real.exp_le_exp.2
      have : Real.log s * x ≤ 5 * Real.log m * x := mul_le_mul_of_nonneg_right hlogs.le hx0
      calc Real.log s * x ≤ 5 * Real.log m * x := this
        _ = Real.log d * (5 * (1 - β)) := by rw [hx_def]; field_simp; ring
    calc s ^ k = s * s ^ ⌊x⌋₊ := by rw [hk_def, pow_succ, mul_comm]
      _ ≤ s * d ^ (5 * (1 - β)) := by gcongr; exact hfl.trans hsx
  have hgeom := geom_le s hs k
  have hD : d ^ (5 * (1 - β)) * d ^ β = d ^ (5 - 4 * β) := by
    rw [← Real.rpow_add hd0]; congr 1; ring
  have hDle : d ^ (5 * (1 - β)) ≤ d ^ (5 - 4 * β) :=
    Real.rpow_le_rpow_of_exponent_le hd (by linarith)
  have hsk0 : 0 ≤ s ^ k := pow_nonneg (by linarith) k
  have hDpos : 0 ≤ d ^ (5 * (1 - β)) := (Real.rpow_pos_of_pos hd0 _).le
  calc A e ≤ s ^ k * (8 * t) + E * ∑ i ∈ range k, s ^ i := hA
    _ ≤ s ^ k * (8 * t) + E * s ^ k := by gcongr
    _ = s ^ k * (8 * t + E) := by ring
    _ ≤ s * d ^ (5 * (1 - β)) * (8 * t + E) := by gcongr
    _ = 8 * s * (d ^ (5 * (1 - β)) * t) + E * s * d ^ (5 * (1 - β)) := by ring
    _ ≤ 8 * s * d ^ (5 - 4 * β) + E * s * d ^ (5 - 4 * β) := by
        rw [ht_def, hD]; gcongr
    _ = s * (8 + E) * d ^ (5 - 4 * β) := by ring

/-- **Note lines 29-31** (with the upstream count `(m-1)(1 + ⌊log_m d⌋)`,
`05-layers.tex` line 673): at most `m(1+1/ζ)d^ζ` base-`m` pieces. -/
theorem pieces_le (m d ζ : ℝ) (hm : 3 ≤ m) (hd : 1 ≤ d) (hζ : 0 < ζ) :
    (m - 1) * (1 + ⌊Real.log d / Real.log m⌋₊) ≤ m * (1 + 1 / ζ) * d ^ ζ := by
  have hd0 : 0 < d := by linarith
  have hlogm : 1 < Real.log m :=
    lt_of_lt_of_le one_lt_log_three (Real.log_le_log (by norm_num) hm)
  have hlogd : 0 ≤ Real.log d := Real.log_nonneg hd
  have hfl : (⌊Real.log d / Real.log m⌋₊ : ℝ) ≤ Real.log d := by
    calc (⌊Real.log d / Real.log m⌋₊ : ℝ) ≤ Real.log d / Real.log m :=
          Nat.floor_le (div_nonneg hlogd (by linarith))
      _ ≤ Real.log d := div_le_self hlogd hlogm.le
  have hlog : Real.log d ≤ d ^ ζ / ζ := Real.log_le_rpow_div hd0.le hζ
  have hdζ : 1 ≤ d ^ ζ := Real.one_le_rpow hd hζ.le
  have hfl0 : (0 : ℝ) ≤ ⌊Real.log d / Real.log m⌋₊ := Nat.cast_nonneg _
  calc (m - 1) * (1 + ⌊Real.log d / Real.log m⌋₊)
      ≤ m * (1 + ⌊Real.log d / Real.log m⌋₊) := by gcongr; linarith
    _ ≤ m * (d ^ ζ + d ^ ζ / ζ) := by gcongr; linarith
    _ = m * (1 + 1 / ζ) * d ^ ζ := by ring

/-- **Note lines 29-37**: pieces of width at most `d`, individually processed axes
(`≤ 8d`) and outer phases (`≤ ⌊D/2⌋ + 9`, `D ≤ d`) give the whole-layer bound. -/
theorem layer_bound (A : ℝ → ℝ) (s m E B d β ζ C0 : ℝ) (hs : 2 ≤ s) (hsm : s < m ^ 5)
    (hm : 3 ≤ m) (hE : 0 ≤ E) (hd : 1 ≤ d) (hβ0 : 0 ≤ β) (hβ1 : β < 1) (hζ : 0 < ζ)
    (hB : s * (8 + E) ≤ 9 * B ^ 2)
    (hC0 : 9 * m * B ^ 2 * (1 + 1 / ζ) + 18 ≤ C0)
    (hint : ∀ e, d ^ β ≤ e → A e ≤ s * A (e / m) + E)
    (hleaf : ∀ e, 0 < e → e < d ^ β → A e ≤ 8 * e)
    (pieces : List ℝ) (hpos : ∀ e ∈ pieces, 0 < e ∧ e ≤ d)
    (hcount : (pieces.length : ℝ) ≤ (m - 1) * (1 + ⌊Real.log d / Real.log m⌋₊))
    (individual outer D : ℝ) (hind : individual ≤ 8 * d) (hD : D ≤ d)
    (hout : outer ≤ D / 2 + 9) :
    (pieces.map A).sum + individual + outer ≤ 9 * m * B ^ 2 * (1 + 1 / ζ) * d ^ (5 - 4 * β + ζ) + 18 * d ∧
    9 * m * B ^ 2 * (1 + 1 / ζ) * d ^ (5 - 4 * β + ζ) + 18 * d ≤ C0 * d ^ (5 - 4 * β + ζ) := by
  have hd0 : 0 < d := by linarith
  set P := 9 * B ^ 2 * d ^ (5 - 4 * β) with hP
  have hpiece : ∀ e ∈ pieces, A e ≤ P := by
    intro e he
    obtain ⟨he0, hed⟩ := hpos e he
    have := root_bound A s m E d β hs hsm (by linarith) hE hd hβ0 hβ1.le hint hleaf e he0 hed
    have hDp : 0 ≤ d ^ (5 - 4 * β) := (Real.rpow_pos_of_pos hd0 _).le
    calc A e ≤ s * (8 + E) * d ^ (5 - 4 * β) := this
      _ ≤ 9 * B ^ 2 * d ^ (5 - 4 * β) := by gcongr
  have hsum : (pieces.map A).sum ≤ pieces.length * P := by
    have := List.sum_le_card_nsmul (pieces.map A) P (by
      intro x hx; obtain ⟨e, he, rfl⟩ := List.mem_map.1 hx; exact hpiece e he)
    simpa [nsmul_eq_mul] using this
  have hP0 : 0 ≤ P := by positivity
  have hcnt := pieces_le m d ζ hm hd hζ
  have hpow : d ^ ζ * d ^ (5 - 4 * β) = d ^ (5 - 4 * β + ζ) := by
    rw [← Real.rpow_add hd0]; ring_nf
  have hC1 : 1 ≤ 5 - 4 * β + ζ := by linarith
  have hdC : d ≤ d ^ (5 - 4 * β + ζ) := by
    calc d = d ^ (1 : ℝ) := (Real.rpow_one d).symm
      _ ≤ d ^ (5 - 4 * β + ζ) := Real.rpow_le_rpow_of_exponent_le hd hC1
  constructor
  · calc (pieces.map A).sum + individual + outer
        ≤ pieces.length * P + 8 * d + (d / 2 + 9) := by linarith
      _ ≤ m * (1 + 1 / ζ) * d ^ ζ * P + 8 * d + (d / 2 + 9) := by
          gcongr; linarith
      _ = 9 * m * B ^ 2 * (1 + 1 / ζ) * (d ^ ζ * d ^ (5 - 4 * β)) + 8 * d + (d / 2 + 9) := by
          rw [hP]; ring
      _ ≤ 9 * m * B ^ 2 * (1 + 1 / ζ) * d ^ (5 - 4 * β + ζ) + 18 * d := by
          rw [hpow]; linarith
  · have hdC0 : 0 ≤ d ^ (5 - 4 * β + ζ) := (Real.rpow_pos_of_pos hd0 _).le
    nlinarith

open KappaCheck.Network KappaCheck.CrocSwap in
/-- The note's instance: `h = 25` complex network, `β = 1/1000`, `ζ = 1/10000`.  Every
hypothesis on the constants is discharged by `guard_constants`. -/
theorem guard_instance (A : ℝ → ℝ) (d : ℝ) (hd : 1 ≤ d)
    (hint : ∀ e, d ^ ((1 : ℝ) / 1000) ≤ e → A e ≤ (sc 25 : ℝ) * A (e / 15625) + (Eg : ℝ))
    (hleaf : ∀ e, 0 < e → e < d ^ ((1 : ℝ) / 1000) → A e ≤ 8 * e)
    (pieces : List ℝ) (hpos : ∀ e ∈ pieces, 0 < e ∧ e ≤ d)
    (hcount : (pieces.length : ℝ) ≤ (15625 - 1) * (1 + ⌊Real.log d / Real.log 15625⌋₊))
    (individual outer D : ℝ) (hind : individual ≤ 8 * d) (hD : D ≤ d)
    (hout : outer ≤ D / 2 + 9) :
    (pieces.map A).sum + individual + outer ≤
      (C0n : ℝ) * d ^ ((5 : ℝ) - 4 * (1 / 1000) + 1 / 10000) := by
  obtain ⟨hE, hB, -, h2, h5, h9, -, -, hC0⟩ := guard_constants
  have hs : (2 : ℝ) ≤ (sc 25 : ℝ) := by exact_mod_cast h2
  have hsm : (sc 25 : ℝ) < (15625 : ℝ) ^ 5 := by
    have : (sc 25 : ℝ) < ((m 25 ^ 5 : ℕ) : ℝ) := by exact_mod_cast h5
    simp only [m] at this; push_cast at this; norm_num at this ⊢; exact this
  have hBq : (sc 25 : ℝ) * (8 + (Eg : ℝ)) ≤ 9 * (Bg : ℝ) ^ 2 := by exact_mod_cast h9
  have hC0r : 9 * 15625 * (Bg : ℝ) ^ 2 * (1 + 1 / (1 / 10000)) + 18 ≤ (C0n : ℝ) := by
    have : ((9 * 15625 * (Bg : ℚ) ^ 2 * (1 + 1 / ζq) + 18 : ℚ) : ℝ) ≤ ((C0n : ℚ) : ℝ) := by
      exact_mod_cast hC0
    simpa [ζq] using this
  have := layer_bound A (sc 25) 15625 Eg Bg d (1 / 1000) (1 / 10000) C0n hs hsm
    (by norm_num) (by positivity) hd (by norm_num) (by norm_num) (by norm_num) hBq hC0r
    hint hleaf pieces hpos hcount individual outer D hind hD hout
  linarith [this.1, this.2]

end KappaCheck.Guard
