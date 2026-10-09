import Mathlib.Tactic

/-!
# The address algebra of the compact-control movement (`notes/compact-control-movement.tex`)

The tape-level claims (fixed tapes, streaming, `O(V)` cost) are not modelled here.
This file proves the arithmetic that those constructions rely on:

* the four-step identity that toggles a target parity and restores a dirty temporary;
* the later-source variant: two passes with control parities `u mod 2` and
  `(u + x) mod 2` toggle the target by exactly `x`;
* the guard interval prevents every carry or borrow, so one packed modular rotation
  acts as independent updates of the selected segments;
* the repair permutation: if `S = T` off a bad set that `T` preserves, then `S`
  preserves it and `T S⁻¹` is the identity off it.
-/

namespace KappaCheck.Movement

/-- XOR of two bits, as integers -/
def bxor (a z : ℤ) : ℤ := a + z - 2 * a * z

/-- **Lines 47-55**: `v ← v+2zw; w ← w+(v mod 2); v ← v+z(1-2w); w ← w-((v mod 2) ⊕ z)`
gives `v + z(1 - 2a)` with `a = v mod 2`, and restores `w`. -/
theorem four_step (v w z : ℤ) (hz : z = 0 ∨ z = 1) :
    let v1 := v + 2 * z * w
    let w1 := w + v1 % 2
    let v2 := v1 + z * (1 - 2 * w1)
    let w2 := w1 - bxor (v2 % 2) z
    v2 = v + z * (1 - 2 * (v % 2)) ∧ w2 = w := by
  intro v1 w1 v2 w2
  simp only [v1, w1, v2, w2, bxor]
  rcases hz with rfl | rfl <;> constructor <;> omega

/-- the four-step result toggles exactly the parity when `z = 1` -/
theorem four_step_parity (v z : ℤ) (hz : z = 0 ∨ z = 1) :
    (v + z * (1 - 2 * (v % 2))) % 2 = bxor (v % 2) z ∧
    (v + z * (1 - 2 * (v % 2))) / 2 = v / 2 := by
  rcases hz with rfl | rfl <;> simp only [bxor] <;> constructor <;> omega

/-- **Lines 72-78**: with no overflow, `(u + x) mod 2 = (u mod 2) ⊕ x`, so the two
earlier-source passes toggle the target by `(u mod 2) ⊕ ((u+x) mod 2) = x`. -/
theorem later_source (a u x : ℤ) (ha : a = 0 ∨ a = 1) (hx : x = 0 ∨ x = 1) :
    bxor (bxor a (u % 2)) ((u + x) % 2) = bxor a x := by
  have hu := Int.emod_two_eq_zero_or_one u
  rcases hx with rfl | rfl
  · rw [add_zero]
    rcases hu with h | h <;> rw [h] <;> rcases ha with rfl | rfl <;> norm_num [bxor]
  · have h1 : (u + 1) % 2 = 1 - u % 2 := by omega
    rw [h1]
    rcases hu with h | h <;> rw [h] <;> rcases ha with rfl | rfl <;> norm_num [bxor]

/-- **Lines 86-94**: a segment `2g + a` with `2B ≤ g < 2^(K-1) - 2B` stays in
`[0, 2^K)` (here `P = 2^(K-1)`) under any displacement of size at most `2B`. -/
theorem guard_no_carry (g a d B P : ℤ) (ha : a = 0 ∨ a = 1)
    (hlo : 2 * B ≤ g) (hhi : g < P - 2 * B) (hd : |d| ≤ 2 * B) :
    0 ≤ 2 * g + a + d ∧ 2 * g + a + d < 2 * P := by
  rw [abs_le] at hd
  rcases ha with rfl | rfl <;> constructor <;> linarith [hd.1, hd.2]

/-- base-`b` partial sums are below `b^n` -/
theorem digits_lt (b : ℕ) (hb : 0 < b) (c : ℕ → ℕ) (hc : ∀ i, c i < b) (n : ℕ) :
    ∑ i ∈ Finset.range n, c i * b ^ i < b ^ n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, pow_succ]
    have := hc n
    calc ∑ i ∈ Finset.range n, c i * b ^ i + c n * b ^ n
        < b ^ n + c n * b ^ n := by omega
      _ ≤ b ^ n + (b - 1) * b ^ n := by gcongr; omega
      _ = b ^ n * b := by
          have : b ^ n + (b - 1) * b ^ n = (1 + (b - 1)) * b ^ n := by ring
          rw [this, Nat.add_sub_cancel' hb, mul_comm]

/-- digit extraction: segment `k < n` of `Σ_{i<n} cᵢ bⁱ + bⁿ H` is `c_k` -/
theorem digit_extract (b : ℕ) (hb : 0 < b) (c : ℕ → ℕ) (hc : ∀ i, c i < b) :
    ∀ n (H : ℕ) k, k < n → (∑ i ∈ Finset.range n, c i * b ^ i + b ^ n * H) / b ^ k % b = c k := by
  intro n
  induction n with
  | zero => intro H k hk; omega
  | succ n ih =>
    intro H k hk
    rw [Finset.sum_range_succ]
    rcases Nat.lt_succ_iff_lt_or_eq.1 hk with hk | rfl
    · -- the new top digit and `H` are multiples of `b^(k+1)`
      have e : ∑ i ∈ Finset.range n, c i * b ^ i + c n * b ^ n + b ^ (n + 1) * H =
          ∑ i ∈ Finset.range n, c i * b ^ i + b ^ n * (c n + b * H) := by ring
      rw [e]; exact ih (c n + b * H) k hk
    · have hlow := digits_lt b hb c hc k
      have e : ∑ i ∈ Finset.range k, c i * b ^ i + c k * b ^ k + b ^ (k + 1) * H =
          ∑ i ∈ Finset.range k, c i * b ^ i + b ^ k * (c k + b * H) := by ring
      rw [e, Nat.add_mul_div_left _ _ (pow_pos hb k), Nat.div_eq_of_lt hlow, zero_add,
        Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt (hc k)]

/-- **Lines 57-63 and 91-94**: when every displaced segment stays in `[0, b)` (the
guard), adding the packed offset `Σ dᵢ bⁱ` to `Σ sᵢ bⁱ + bⁿ H` changes segment `k`
to exactly `s_k + d_k` and leaves the higher part `H`: no carries or borrows. -/
theorem packed_rotation (b : ℕ) (hb : 0 < b) (s d : ℕ → ℤ) (H : ℕ) (n : ℕ)
    (hs : ∀ i, 0 ≤ s i + d i ∧ s i + d i < b) :
    ∃ c : ℕ → ℕ, (∀ i, (c i : ℤ) = s i + d i) ∧
      (∑ i ∈ Finset.range n, s i * (b : ℤ) ^ i + (b : ℤ) ^ n * H) +
        ∑ i ∈ Finset.range n, d i * (b : ℤ) ^ i =
        ((∑ i ∈ Finset.range n, c i * b ^ i + b ^ n * H : ℕ) : ℤ) ∧
      ∀ k < n, (∑ i ∈ Finset.range n, c i * b ^ i + b ^ n * H) / b ^ k % b = c k := by
  refine ⟨fun i => (s i + d i).toNat, ?_, ?_, ?_⟩
  · intro i; exact Int.toNat_of_nonneg (hs i).1
  · push_cast
    rw [add_comm (∑ i ∈ Finset.range n, s i * (b : ℤ) ^ i), add_assoc, ← Finset.sum_add_distrib]
    rw [add_comm]
    congr 1
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [Int.toNat_of_nonneg (hs i).1]; ring
  · intro k hk
    apply digit_extract b hb _ _ n H k hk
    intro i
    have := hs i
    have h := Int.toNat_of_nonneg this.1
    omega

/-- **Lines 104-108 and 119**: if `S = T` off `Bad` and `T` preserves `Bad`, then `S`
preserves `Bad`, and `T S⁻¹` fixes every good address and permutes `Bad`. -/
theorem repair_permutation {α : Type*} (S T : α ≃ α) (Bad : Set α)
    (hT : ∀ x, x ∈ Bad ↔ T x ∈ Bad) (hST : ∀ x, x ∉ Bad → S x = T x) :
    (∀ x, x ∈ Bad ↔ S x ∈ Bad) ∧ (∀ y, y ∉ Bad → T (S.symm y) = y) ∧
      (∀ y, y ∈ Bad ↔ T (S.symm y) ∈ Bad) := by
  have hS : ∀ x, x ∈ Bad ↔ S x ∈ Bad := by
    intro x; constructor
    · intro hx; by_contra hy
      -- `S x` is good, so it is `T x'` for a good `x'`, and then `S x' = S x`
      set x' := T.symm (S x)
      have hx' : x' ∉ Bad := by
        intro h; exact hy (by simpa [x'] using (hT x').1 h)
      have : S x' = S x := by rw [hST x' hx']; simp [x']
      exact hx' (S.injective this ▸ hx)
    · intro h; by_contra hx; rw [hST x hx] at h; exact hx ((hT x).2 h)
  refine ⟨hS, ?_, ?_⟩
  · intro y hy
    have hg : S.symm y ∉ Bad := by
      intro h; exact hy (by simpa using (hS (S.symm y)).1 h)
    rw [← hST _ hg]; simp
  · intro y
    rw [← hT, hS (S.symm y)]; simp

end KappaCheck.Movement
