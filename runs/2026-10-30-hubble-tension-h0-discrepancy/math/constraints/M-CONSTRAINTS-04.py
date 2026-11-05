"""M-CONSTRAINTS-04 (F4): CMB analysis systematic inside flat LCDM.
Fixed theta_*, omega_b = 0.02237: solve omega_c for H0 = 73.26 (lens 0.1045, Omega_m 0.238, -0.0155 = 13 sigma of 0.0012);
at fixed omega_c = 0.1200, 100theta_* for h = 0.7326 (lens 1.0585, 58 sigma of 0.0003).
My z_* fit (Hu-Sugiyama) + simple r_s gives an absolute 100theta_* ~0.2% below CAMB's, so (run 2) theta is calibrated:
target = my model's theta at the Planck 2018 best fit (h = 0.6736, omega_c = 0.1200), rescaled to 1.0411.
Run 1 (absolute 1.0411) is printed too, to show the normalisation sensitivity."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import finish
from _bg import Model, bisect, near

wb = 0.02237
ref = Model(0.6736, wb, 0.1200).theta100()
print(f"my 100theta at Planck best fit = {ref:.5f} (CAMB 1.04110); calibration factor {1.0411/ref:.5f}")
hb = bisect(lambda h: Model(h, wb, 0.1200).theta100() - 1.0411, 0.5, 0.9, tol=1e-7)
print("run 1 (uncalibrated) baseline H0 =", 100 * hb)
wc1 = bisect(lambda w: Model(0.73264, wb, w).theta100() - 1.0411, 0.06, 0.16, tol=1e-8)
print("run 1 omega_c needed =", wc1)

wc = bisect(lambda w: Model(0.73264, wb, w).theta100() - ref, 0.06, 0.16, tol=1e-8)
m = Model(0.73264, wb, wc)
print(f"run 2: omega_c needed {wc:.5f}; Omega_m {m.Om:.4f}; shift {wc-0.12:.5f} = {(0.12-wc)/0.0012:.1f} sigma")
near("omega_c needed", wc, 0.1045, 0.001)
near("Omega_m", m.Om, 0.238, 0.002)
near("n sigma(omega_c)", (0.12 - wc) / 0.0012, 13, 1.0)
t = Model(0.7326, wb, 0.1200).theta100() / ref * 1.0411
print("run 2: 100theta_* at h = 0.7326, omega_c fixed:", t, "n sigma", (t - 1.0411) / 0.0003)
near("100 theta_*", t, 1.0585, 0.0015)
near("n sigma theta", (t - 1.0411) / 0.0003, 58, 5)
raise SystemExit(finish())
