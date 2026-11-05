"""M-CONSTRAINTS-10 (F10): late-time dark energy at fixed theta_*, omega_b = 0.02237, omega_c = 0.1200 (Planck best fit, my model's
theta at h = 0.6736 as the target). Constant w reaching H0 = 73.26 (lens w = -1.194, Omega_m 0.266, NEC violated since w < -1);
BAO D_M shift vs LCDM at z = 0.295 (lens -4.9%) and 0.51 (-3.4%) with the same r_d; SN shape Delta mu(z) - Delta mu(0.05) (lens -0.10 mag at z >= 0.3);
CPL (w0, wa) = (-0.42, -1.75) -> lens H0 = 63.7. NEC for a fluid: rho + p = rho (1 + w) >= 0 <=> w >= -1."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import sign, limit, finish
from _bg import Model, bisect, near

wb, wc = 0.02237, 0.1200
base = Model(0.6736, wb, wc); ref = base.theta100()
near("w=-1 limit recovers base h", 100 * bisect(lambda h: Model(h, wb, wc, w0=-1.0).theta100() - ref, 0.6, 0.8, tol=1e-8), 67.36, 0.01)
w = bisect(lambda w: Model(0.73264, wb, wc, w0=w).theta100() - ref, -2.0, -1.0, tol=1e-7)
m = Model(0.73264, wb, wc, w0=w)
print(f"w = {w:.4f}, Omega_m = {m.Om:.4f} ({(0.2975-m.Om)/0.0086:.1f} sigma)")
near("w", w, -1.194, 0.01); near("Omega_m", m.Om, 0.266, 0.002)
for z, want in [(0.295, -0.049), (0.51, -0.034)]:
    d = m.DM(z) / base.DM(z) - 1
    print(f"D_M shift z={z}: {d:.4f}")
    near(f"D_M shift z={z}", d, want, 0.004)
mu = lambda mod, z: 5 * math.log10((1 + z) * mod.DM(z, n=2000))
d05 = mu(m, 0.05) - mu(base, 0.05)
for z in (0.3, 0.5, 1.0):
    print(f"SN shape z={z}: {mu(m, z) - mu(base, z) - d05:.4f} mag")
shape = 0.5 * (mu(m, .3) - mu(base, .3) + mu(m, .5) - mu(base, .5)) - d05
print("NOTE: in the (w-model minus LCDM, matched at z=0.05) convention the shape term is POSITIVE (high-z SNe fainter);")
print("the first check below tests the lens's signed -0.10 literally, the second tests its size.")
near("SN shape at z=0.3-0.5 (mean), signed", shape, -0.10, 0.03)
near("SN shape size |.|, z=0.3-1.0 range 0.06-0.13", abs(shape), 0.10, 0.03)
h = bisect(lambda h: Model(h, wb, wc, w0=-0.42, wa=-1.75).theta100() - ref, 0.5, 0.8, tol=1e-7)
print("CPL H0 =", 100 * h)
near("CPL H0", 100 * h, 63.7, 0.5)
sign("rho*(1 + w)", "negative", domain={"rho": (0.1, 10), "w": (-2, -1.0001)})
limit("(1+z)**(3*(1+w))", "w", -1, "1", domain={"z": (0, 3)})
raise SystemExit(finish())
