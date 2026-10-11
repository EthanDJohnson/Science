"""M-DECOMPOSER-03: arithmetic on the generator's apparent-gamma grid (calc A, B, C; F2, F3, F4, F11).

Inputs (generator outputs, quoted from the lens): apparent gamma (dimensionless)
  A: f_triple 0.1/0.2/0.3 -> CAL 1.055/1.097/1.137, TEST 1.061/1.180/1.282 (f=0 -> 1 by construction)
  C: ecc truth vs HTZ template: alpha=2 CAL 0.865 TEST 0.935; thermal 0.997/1.063; uniform 1.246/1.305
Claims: differentials 1.006/1.075/1.128; 1.080/1.067/1.048; "freed f(e) absorbs <= 7%" (1/0.935);
B: under Newton a CAL-calibrated estimator gives 1.368 only if Delta f = f_TEST - f_cal ~ +0.37
(f_cal = 0) to +0.43 (f_cal = 0.2), linear extrapolation beyond the grid.
Independent reading of B: the calibrated template carries f_cal triples modelled correctly in the
TEST bin, so gam_meas = T(f_test)/T(f_cal), T = TEST-bin apparent gamma vs f. Solve T(f_test) =
1.368 T(f_cal) with T linear: (i) least-squares line through all 4 points, (ii) last-segment slope.
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, finish

CAL = {0.0: 1.0, 0.1: 1.055, 0.2: 1.097, 0.3: 1.137}
TEST = {0.0: 1.0, 0.1: 1.061, 0.2: 1.180, 0.3: 1.282}
for f, claim in ((0.1, 1.006), (0.2, 1.075), (0.3, 1.128)):
    r = TEST[f] / CAL[f]
    print("diff f", f, r)
    quantity(f"{r}", f"{claim}", rel_tol=1.5e-3)
for name, c, t, claim in (("alpha2", 0.865, 0.935, 1.080), ("thermal", 0.997, 1.063, 1.067),
                          ("uniform", 1.246, 1.305, 1.048)):
    r = t / c
    print("ecc", name, r)
    quantity(f"{r}", f"{claim}", rel_tol=1.5e-3)
quantity(f"{1/0.935}", "1.07", rel_tol=2e-3)

fs = np.array(sorted(TEST)); Ts = np.array([TEST[f] for f in fs])
k_ls, c_ls = np.polyfit(fs, Ts, 1)
k_last = (TEST[0.3] - TEST[0.2]) / 0.1
quad = np.polyfit(fs, Ts, 2)
print("LS slope", k_ls, "intercept", c_ls, "last-segment slope", k_last, "quadratic", quad)
res = {}
for fcal in (0.0, 0.2):
    target = 1.368 * TEST[fcal]
    f_ls = (target - c_ls) / k_ls
    f_last = 0.3 + (target - TEST[0.3]) / k_last
    roots = np.roots([quad[0], quad[1], quad[2] - target]); roots = roots[np.isreal(roots)].real
    f_quad = roots[roots > 0].min() if np.any(roots > 0) else float("nan")
    res[fcal] = (f_ls - fcal, f_last - fcal, f_quad - fcal)
    print(f"f_cal={fcal}: target T={target:.4f}; Delta f LS={f_ls-fcal:.3f}, last-seg={f_last-fcal:.3f}, quad={f_quad-fcal:.3f}")
# the lens's +0.37 / +0.43: compare with the least-squares line (the most neutral linear choice)
# The lens's point values depend on the extrapolation; check the claim's substance instead:
# every linear/quadratic extrapolation needs Delta f between 0.3 and 0.46 (i.e. "~ +0.4"),
# and the lens's numbers lie inside the span of the extrapolations.
from math_checks import inequality
for fcal in (0.0, 0.2):
    for d in res[fcal]:
        inequality(f"{d}", ">", "0.30")
        inequality(f"{d}", "<", "0.46")
inequality("0.37", ">=", f"{min(res[0.0])}"); inequality("0.37", "<=", f"{max(res[0.0])}")
inequality("0.43", ">=", f"{min(res[0.2])}"); inequality("0.43", "<=", f"{max(res[0.2])}")
# alternative reading (template does NOT model TEST triples: gam = T(f_test)/CAL(f_cal))
for fcal in (0.0, 0.2):
    target = 1.368 * CAL[fcal]
    print(f"alt reading f_cal={fcal}: Delta f LS={(target - c_ls)/k_ls - fcal:.3f}")
raise SystemExit(finish())
