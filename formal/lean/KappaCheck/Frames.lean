import Mathlib.Tactic
import Mathlib.LinearAlgebra.Span.Basic

/-!
# The two algebraic facts behind the paired bit circuit's frames

`notes/paired-construction.tex` uses the rational form `I - J/9` on `ℚ^h`,
`B(u, w) = Σ uⱼ wⱼ - (Σ u)(Σ w)/9`, and the triple indicators `t_S`.

* neighbors are orthogonal: `B(t_S, t_T) = |S ∩ T| - 1`, so `|S ∩ T| = 1` gives `0`;
* a span of indicators of triples sharing a point `i` satisfies `Σ u = 3 uᵢ`, hence
  `B(u, u) = Σ_{j ≠ i} uⱼ² > 0` for `u ≠ 0`: the label is anisotropic, so nondegenerate.
-/

namespace KappaCheck.Frames

open Finset

variable {h : ℕ}

/-- the form `I - J/9` -/
def form (u w : Fin h → ℚ) : ℚ := (∑ j, u j * w j) - (∑ j, u j) * (∑ j, w j) / 9

/-- the indicator of a set of points -/
def ind (S : Finset (Fin h)) : Fin h → ℚ := fun j => if j ∈ S then 1 else 0

theorem sum_ind (S : Finset (Fin h)) : ∑ j, ind S j = S.card := by
  simp [ind, Finset.sum_ite_mem]

theorem sum_ind_mul (S T : Finset (Fin h)) : ∑ j, ind S j * ind T j = (S ∩ T).card := by
  simp only [ind, mul_ite, mul_one, mul_zero]
  rw [← Finset.sum_filter, ← Finset.sum_filter]
  simp [Finset.filter_mem_eq_inter, Finset.filter_filter, Finset.inter_comm]

/-- **neighbors are orthogonal**: for triples, `B(t_S, t_T) = |S ∩ T| - 1` -/
theorem form_ind (S T : Finset (Fin h)) (hS : S.card = 3) (hT : T.card = 3) :
    form (ind S) (ind T) = (S ∩ T).card - 1 := by
  rw [form, sum_ind_mul, sum_ind, sum_ind, hS, hT]; norm_num

theorem neighbors_orthogonal (S T : Finset (Fin h)) (hS : S.card = 3) (hT : T.card = 3)
    (h1 : (S ∩ T).card = 1) : form (ind S) (ind T) = 0 := by
  rw [form_ind S T hS hT, h1]; norm_num

/-- vectors with `Σ u = 3 uᵢ` -/
def common (i : Fin h) : Submodule ℚ (Fin h → ℚ) where
  carrier := {u | ∑ j, u j = 3 * u i}
  add_mem' := by
    intro a b ha hb; simp only [Set.mem_setOf_eq, Pi.add_apply, Finset.sum_add_distrib] at *
    rw [ha, hb]; ring
  zero_mem' := by simp
  smul_mem' := by
    intro c a ha; simp only [Set.mem_setOf_eq, Pi.smul_apply, smul_eq_mul] at *
    rw [← Finset.mul_sum, ha]; ring

/-- every span of indicators of triples through `i` lies in `common i` -/
theorem span_le_common (i : Fin h) (F : Set (Finset (Fin h)))
    (hF : ∀ S ∈ F, S.card = 3 ∧ i ∈ S) :
    Submodule.span ℚ (ind '' F) ≤ common i := by
  rw [Submodule.span_le]
  rintro _ ⟨S, hS, rfl⟩
  obtain ⟨h3, hi⟩ := hF S hS
  show ∑ j, ind S j = 3 * ind S i
  rw [sum_ind, h3]; simp [ind, hi]

/-- on `common i`, `B(u, u) = Σ_{j ≠ i} uⱼ²` -/
theorem form_self_common (i : Fin h) (u : Fin h → ℚ) (hu : u ∈ common i) :
    form u u = ∑ j ∈ univ.erase i, u j ^ 2 := by
  have hs : ∑ j, u j = 3 * u i := hu
  rw [form, hs, ← Finset.add_sum_erase _ _ (mem_univ i)]
  have : ∀ j, u j * u j = u j ^ 2 := fun j => by ring
  simp only [this]; ring

/-- **nondegeneracy**: the form is positive definite on `common i` -/
theorem form_pos_common (i : Fin h) (u : Fin h → ℚ) (hu : u ∈ common i) (hne : u ≠ 0) :
    0 < form u u := by
  rw [form_self_common i u hu]
  by_contra hle; push_neg at hle
  have hz : ∑ j ∈ univ.erase i, u j ^ 2 = 0 :=
    le_antisymm hle (Finset.sum_nonneg fun j _ => sq_nonneg _)
  have hj : ∀ j ∈ univ.erase i, u j = 0 := by
    intro j hj
    have := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg (u j))).1 hz j hj
    exact pow_eq_zero_iff (n := 2) (by norm_num) |>.1 this
  have hs : ∑ j, u j = 3 * u i := hu
  rw [← Finset.add_sum_erase _ _ (mem_univ i), Finset.sum_eq_zero hj] at hs
  have hi : u i = 0 := by linarith
  apply hne; funext j
  by_cases hji : j = i
  · rw [hji, hi]; rfl
  · exact hj j (Finset.mem_erase.2 ⟨hji, mem_univ j⟩)

/-- the label of any node of the paired circuit (a span of triples through a common
point) is anisotropic, hence nondegenerate, for the form `I - J/9` -/
theorem label_anisotropic (i : Fin h) (F : Set (Finset (Fin h)))
    (hF : ∀ S ∈ F, S.card = 3 ∧ i ∈ S) (u : Fin h → ℚ)
    (hu : u ∈ Submodule.span ℚ (ind '' F)) (hne : u ≠ 0) : 0 < form u u :=
  form_pos_common i u (span_le_common i F hF hu) hne

end KappaCheck.Frames
