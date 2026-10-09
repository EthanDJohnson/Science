"""Crux C4: re-check of the verdicts' ghost-scalar e-fold numbers, and C7-style
clock-offset thresholds for C4's designer shortcuts. SI units throughout.

Inputs (all traced):
- e-folding time tau = 0.846 b0/c for the massless ghost-scalar Ellis throat
  (Gonzalez, Guzman & Sarbach 2009, Table I, as quoted in verdicts C4-0/1/2).
- crossing length pi*b0 (verdict C4-2's assumption).
- seed budget ln(1/delta) = 58 to 80 e-folds (verdict C4-0 log lines).
- Ellis b0 = 1 m observer-to-observer T_thru = 6.64e-8 s (C4 / M-EXAMINER-02).
- Delta_s = T_thru - d/c, Delta_CTC = T_thru + d/c (C7, six verified checks).
- clock drift rate v^2/(2c^2) for relative mouth speed v (verdict C4-2 section 5).
"""
import math

c = 2.99792458e8          # m/s
yr = 3.15576e7            # s (Julian year)
AU = 1.495978707e11       # m
ly = 9.4607304725808e15   # m
T = 0.846                 # tau_unstable / (b0/c)

print("== Ghost-scalar e-folds during a crossing (independent of b0) ==")
for v in (1.0e4, 0.03 * c, 0.05 * c, 0.1 * c, 0.9 * c):
    N = math.pi * c / (T * v)
    print(f"v = {v:.3e} m/s ({v/c:.3g} c): N = pi c/(0.846 v) = {N:.4g} e-folds")

print("== Minimum crossing speed for seed budgets ==")
for budget in (58.0, 70.0, 80.0):
    vmin = math.pi / (T * budget)
    print(f"ln(1/delta) = {budget:.0f}: v_min = {vmin:.4f} c")

print("== C7 thresholds for C4's Ellis b0 = 1 m designer shortcut ==")
T_thru = 6.64e-8  # s
for name, d in (("1 km", 1.0e3), ("1 AU", AU), ("1 ly", ly)):
    Text = d / c
    ds = T_thru - Text
    dctc = T_thru + Text
    print(f"d = {name}: T_ext = {Text:.4e} s, Delta_s = {ds:.4e} s (negative => shortcut already at Delta = 0), "
          f"Delta_CTC = {dctc:.4e} s")

print("== Drift time to Delta_CTC (1 ly) for relative mouth speed v ==")
for v in (3.0e4, 2.2e5):
    rate = v**2 / (2 * c**2)
    t = (T_thru + ly / c) / rate
    print(f"v = {v:.3e} m/s: drift rate = {rate:.3e} s/s, time to Delta_CTC = {t/yr:.3e} yr")
