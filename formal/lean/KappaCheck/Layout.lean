import Mathlib.Tactic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# Row arithmetic of the compact-control layout (`notes/compact-control-layout.tex`)

The record-moving tape procedures are not modelled; this file proves the counting
facts the layout relies on.
-/

namespace KappaCheck.Layout

/-- **Line 30**: `R_row = 2^(q₀K) ≥ W^k₀` when `W ≤ 2^a`, `q₀ = a·b`, `k₀ ≤ b`, `K ≥ 1`. -/
theorem row_range (W a b k0 K : ℕ) (hW : 1 ≤ W) (ha : W ≤ 2 ^ a) (hk : k0 ≤ b) (hK : 1 ≤ K) :
    W ^ k0 ≤ 2 ^ (a * b * K) := by
  calc W ^ k0 ≤ W ^ b := Nat.pow_le_pow_right hW hk
    _ ≤ (2 ^ a) ^ b := Nat.pow_le_pow_left ha b
    _ = 2 ^ (a * b) := by rw [← pow_mul]
    _ ≤ 2 ^ (a * b * K) := Nat.pow_le_pow_right (by norm_num) (Nat.le_mul_of_pos_right _ hK)

/-- **Lines 31-35**: padding `R ≥ P = W^k₀` rows to the next multiple of `P` gives a
multiple of `P`, at least `R`, and below `2R`. -/
theorem pad (R P : ℕ) (hP : 0 < P) (hPR : P ≤ R) :
    let padded := (R + P - 1) / P * P
    P ∣ padded ∧ R ≤ padded ∧ padded < 2 * R := by
  intro padded
  obtain ⟨t, ht⟩ : ∃ t, t = R + P - 1 := ⟨_, rfl⟩
  have ht1 : t + 1 = R + P := by omega
  have hdm : P * (t / P) + t % P = t := Nat.div_add_mod t P
  have hr : t % P < P := Nat.mod_lt t hP
  have hpad : padded = P * (t / P) := by simp only [padded, ← ht]; rw [mul_comm]
  refine ⟨⟨t / P, hpad⟩, ?_, ?_⟩ <;> rw [hpad] <;> omega

/-- **Lines 37-41**: with `W · a` rows, role `w < W` receives exactly the `a` rows
`u = W g + w`. -/
theorem role_rows (W a w : ℕ) (hw : w < W) :
    ((Finset.range (W * a)).filter (fun u => u % W = w)).card = a := by
  have hW : 0 < W := by omega
  have himg : (Finset.range (W * a)).filter (fun u => u % W = w) =
      (Finset.range a).image (fun g => W * g + w) := by
    ext u
    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_image]
    constructor
    · rintro ⟨hu, hmod⟩
      refine ⟨u / W, (Nat.div_lt_iff_lt_mul hW).2 (by rw [mul_comm]; exact hu), ?_⟩
      have := Nat.div_add_mod u W
      rw [hmod] at this; exact this
    · rintro ⟨g, hg, rfl⟩
      refine ⟨?_, ?_⟩
      · have : g + 1 ≤ a := hg
        calc W * g + w < W * g + W := by omega
          _ = W * (g + 1) := by ring
          _ ≤ W * a := Nat.mul_le_mul_left W this
      · rw [Nat.add_comm, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hw]
  rw [himg, Finset.card_image_of_injective]
  · simp
  · intro g g' h; simp only at h; exact Nat.eq_of_mul_eq_mul_left hW (by omega)

/-- **Line 41**: if `W^(k+1)` divides the row count, each role's share is `n / W`, and
`W^k` divides it: the invariant survives one more split. -/
theorem split_invariant (W n k : ℕ) (h : W ^ (k + 1) ∣ n) :
    W * (n / W) = n ∧ W ^ k ∣ n / W := by
  have hWn : W ∣ n := (Dvd.intro_left _ (pow_succ W k).symm).trans h
  refine ⟨Nat.mul_div_cancel' hWn, ?_⟩
  rw [pow_succ, mul_comm] at h
  exact Nat.dvd_div_of_mul_dvd h

/-- **Lines 64-67**: `q_F + q_B ≤ 3dG/K + 2 ≤ 6 d^(1-c) G + 2` once `K ≥ d^c/2`. -/
theorem reserved_axes (d G K c : ℝ) (hd : 0 < d) (hG : 0 ≤ G) (hK : d ^ c / 2 ≤ K) :
    (⌈2 * (d * G) / K⌉₊ : ℝ) + ⌈d * G / K⌉₊ ≤ 3 * d * G / K + 2 ∧
    3 * d * G / K + 2 ≤ 6 * d ^ (1 - c) * G + 2 := by
  have hdc : 0 < d ^ c := Real.rpow_pos_of_pos hd c
  have hK0 : 0 < K := by linarith
  have hH : 0 ≤ d * G / K := div_nonneg (mul_nonneg hd.le hG) hK0.le
  have h1 : (⌈2 * (d * G) / K⌉₊ : ℝ) < 2 * (d * G) / K + 1 :=
    Nat.ceil_lt_add_one (div_nonneg (by positivity) hK0.le)
  have h2 : (⌈d * G / K⌉₊ : ℝ) < d * G / K + 1 := Nat.ceil_lt_add_one hH
  constructor
  · have : 2 * (d * G) / K + d * G / K = 3 * d * G / K := by ring
    linarith
  · have hpow : d ^ (1 - c) = d / d ^ c := by
      rw [Real.rpow_sub hd, Real.rpow_one]
    rw [hpow]
    have : 3 * d * G / K ≤ 6 * (d / d ^ c) * G := by
      rw [div_le_iff₀ hK0]
      have e : 6 * (d / d ^ c) * G * K = 3 * d * G * (2 * K / d ^ c) := by
        field_simp; ring
      rw [e]
      have : 1 ≤ 2 * K / d ^ c := by rw [le_div_iff₀ hdc]; linarith
      have h0 : 0 ≤ 3 * d * G := by positivity
      nlinarith
    linarith

end KappaCheck.Layout
