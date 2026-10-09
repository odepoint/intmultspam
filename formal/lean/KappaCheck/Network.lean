import Mathlib.Tactic

/-!
# Counting identities for the two finite networks (paper Section 3)

All quantities are functions of the ground-set size `h`.  We check

* the paper's closed forms for `h = 100` (so the formulas below are the paper's);
* the `h = 46` counts and deficits of `notes/parameter-note.tex` (a second data point);
* the per-wire rank bookkeeping of Lemma 7 / Proposition 8 as polynomial
  identities, which is where `s = W m - N + 2L` (bit) and
  `s = W m - 2N + 2L` (complex) come from.
-/

namespace KappaCheck.Network

/-- number of three-element subsets of `[h]` -/
def v (h : ℕ) : ℕ := h.choose 3
def N (h : ℕ) : ℕ := v h ^ 3
def m (h : ℕ) : ℕ := h ^ 3
/-- number of invocations `3 v^2` -/
def I (h : ℕ) : ℕ := 3 * v h ^ 2
/-- neighbours of a triple: bit network `|S ∩ T| = 1`, complex network distinct and even -/
def zb (h : ℕ) : ℕ := 3 * (h - 3).choose 2
def zc (h : ℕ) : ℕ := (h - 3).choose 3 + 3 * (h - 3)
def Wb (h : ℕ) : ℕ := 2 * N h + I h * (v h * zb h + h)
def Wc (h : ℕ) : ℕ := 2 * N h + I h * (v h * zc h + (h + 1))
def Lb (h : ℕ) : ℕ := I h * h * h
def Lc (h : ℕ) : ℕ := I h * (h + 1) * h
/-- rank sums, written so that natural subtraction is harmless -/
def sb (h : ℕ) : ℕ := Wb h * m h + 2 * Lb h - N h
def sc (h : ℕ) : ℕ := Wc h * m h + 2 * Lc h - 2 * N h

/-! ## The paper's numbers (h = 100) are reproduced exactly -/

theorem paper_h100 :
    v 100 = 161700 ∧ N 100 = 4227952113000000 ∧ m 100 = 1000000 ∧
    I 100 = 78440670000 ∧ zb 100 = 13968 ∧ zc 100 = 147731 ∧
    Wb 100 = 177176569091445000000 ∧ Wc 100 = 1873807244643542670000 ∧
    sb 100 = 177176569088785861287000000 ∧
    sc 100 = 1873807244636671267308000000 := by
  refine ⟨by decide, ?_⟩
  simp only [N, m, I, zb, zc, Wb, Wc, Lb, Lc, sb, sc, v]
  norm_num [Nat.choose]

theorem paper_h100_deficits :
    ((Wb 100 * m 100 - sb 100 : ℕ) : ℚ) / (Wb 100 * m 100) = 339 / 22587335000000 ∧
    ((Wc 100 * m 100 - sc 100 : ℕ) : ℚ) / (Wc 100 * m 100) = 73 / 19906842167500 := by
  simp only [N, m, I, zb, zc, Wb, Wc, Lb, Lc, sb, sc, v]
  norm_num [Nat.choose]

/-! ## The `h = 46` values of `notes/parameter-note.tex` -/

theorem parameter_note_h46 :
    v 46 = 15180 ∧ m 46 = 97336 ∧ N 46 = 3497963832000 ∧ I 46 = 691297200 ∧
    zb 46 = 2709 ∧ zc 46 = 12470 ∧ Lb 46 = 1462784875200 ∧ Lc 46 = 1494584546400 ∧
    Wb 46 = 28434979789999200 ∧ sb 46 = 2767747192266968049600 ∧
    Wc 46 = 130865855373752400 ∧ sc 46 = 12737958894652805035200 := by
  refine ⟨by decide, ?_⟩
  simp only [N, m, I, zb, zc, Wb, Wc, Lb, Lc, sb, sc, v]
  norm_num [Nat.choose]

/-- exact relative rank deficits of the two `h = 46` networks -/
theorem parameter_note_h46_deficits :
    ((Wb 46 * m 46 - sb 46 : ℕ) : ℚ) / (Wb 46 * m 46) = 9 / 43518487588 ∧
    ((Wc 46 * m 46 - sc 46 : ℕ) : ℚ) / (Wc 46 * m 46) = 7 / 22253827054 ∧
    sb 46 < Wb 46 * m 46 ∧ sc 46 < Wc 46 * m 46 := by
  simp only [N, m, I, zb, zc, Wb, Wc, Lb, Lc, sb, sc, v]
  norm_num [Nat.choose]

/-! ## Lemma 7 bookkeeping as polynomial identities (over ℤ)

At stage `j` put `a = h^(j-1)` and `f = h^(3-j)`, so `a * h * f = h^3 = m`.
The residual table of Lemma 7 gives the per-wire costs below. -/

/-- one stage of a data wire `X`: edges in→2 and 2→3 -/
def costX (a h : ℤ) : ℤ := (a - 1) * (h - 1) + (h - 1)
/-- one stage of a data wire `Y`: edges 0→1 and 4→5 -/
def costY (a h : ℤ) : ℤ := (a - 1) * (h - 1) + (h - 1)
/-- a central wire: source→1, 1→3, 3→4 (the only decrease), 4→6, last→sink -/
def costCenter (a h f : ℤ) : ℤ := (a - 1) * h + h + h + h + a * h * (f - 1)
/-- a side wire: source→0, 0→2, 2→5, 5→7, last→sink -/
def costSide (a h f : ℤ) : ℤ :=
  (a - 1) + ((a - 1) * (h - 1) + 1) + (h - 2) + 1 + a * h * (f - 1)

/-- Over the three stages the data wire `X` grows from dimension 1 to `h^3` and pays
one extra rank for its negative source projection; `Y` grows from `0` to `h^3 - 1`. -/
theorem data_wires (h : ℤ) :
    costX 1 h + costX h h + costX (h ^ 2) h + 1 = h ^ 3 ∧
    costY 1 h + costY h h + costY (h ^ 2) h = h ^ 3 - 1 := by
  constructor <;> simp only [costX, costY] <;> ring

/-- a central wire costs `m + 2h` at every stage; a side wire costs exactly `m` -/
theorem scratch_wires (a h f : ℤ) :
    costCenter a h f = a * h * f + 2 * h ∧ costSide a h f = a * h * f := by
  constructor <;> simp only [costCenter, costSide] <;> ring

/-- Assembling Lemma 7: with `N` pairs, `I` invocations, `c` central and `vz` side
wires per invocation, `W = 2N + I(vz + c)`.  Summing the per-wire costs gives the
bit-network rank sum `W m - N + 2L` and the complex one `W m - 2N + 2L`,
where `L = I c h`. -/
theorem rank_sums (N I c vz h m : ℤ) :
    let W := 2 * N + I * (vz + c)
    N * m + N * (m - 1) + I * c * (m + 2 * h) + I * vz * m = W * m - N + 2 * (I * c * h) ∧
    N * (m - 1) + N * (m - 1) + I * c * (m + 2 * h) + I * vz * m =
      W * m - 2 * N + 2 * (I * c * h) := by
  intro W; constructor <;> simp only [W] <;> ring

/-- the closed forms used above agree with `rank_sums` -/
theorem sb_eq (h : ℕ) (hm : N h ≤ Wb h * m h) :
    (sb h : ℤ) = (Wb h : ℤ) * m h - N h + 2 * Lb h := by
  unfold sb; push_cast [show N h ≤ Wb h * m h + 2 * Lb h by omega]; ring

theorem sc_eq (h : ℕ) (hm : 2 * N h ≤ Wc h * m h) :
    (sc h : ℤ) = (Wc h : ℤ) * m h - 2 * N h + 2 * Lc h := by
  unfold sc; push_cast [show 2 * N h ≤ Wc h * m h + 2 * Lc h by omega]; ring

end KappaCheck.Network
