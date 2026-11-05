"""M-CONSTRAINTS-02 (F2): r_d needed by the inverse ladder.
BAO measures the product h*r_d (Mpc) [D-45: 101.54+-0.73]; r_d(needed) = (h r_d)/h with h = H0/100.
Errors in quadrature (fractional). Knox-Millea beta = c/(H0 r_d) (dimensionless) [D-03: 29.54+-0.406] -> r_d = c/(beta H0).
CMB-SPA r_d = 147.00+-0.24 Mpc, h = 0.6719 [D-44]."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import units, quantity, limit, finish
from _bg import near

H, sH = 73.264, 0.806
rd_cmb, s_cmb = 147.00, 0.24
c = 299792.458

r1 = 101.54 / (H / 100); s1 = r1 * math.hypot(0.73 / 101.54, sH / H)
near("r_d (DESI h r_d)", r1, 138.6, 0.06); near("sigma", s1, 1.8, 0.06)
near("fractional cut", 1 - r1 / rd_cmb, 0.057, 0.0006)
near("n sigma", (rd_cmb - r1) / math.hypot(s1, s_cmb), 4.6, 0.06)

hrd_cmb = 0.6719 * 147.00
near("CMB h r_d", hrd_cmb, 98.77, 0.006)
r2 = hrd_cmb / (H / 100); s2 = r2 * sH / H
near("r_d (CMB h r_d)", r2, 134.8, 0.06); near("sigma", s2, 1.5, 0.06)
near("fractional cut", 1 - r2 / rd_cmb, 0.083, 0.0006)
near("n sigma", (rd_cmb - r2) / math.hypot(s2, s_cmb), 8.1, 0.06)

beta, sb = 29.54, 0.406
print("check beta reproduces DESI: c/(100 * h r_d) =", c / (100 * 101.54))
r3 = c / (beta * H); s3 = r3 * math.hypot(sb / beta, sH / H)
near("r_d (beta)", r3, 138.5, 0.06); near("sigma", s3, 2.4, 0.06)
near("fractional cut", 1 - r3 / rd_cmb, 0.058, 0.0006)
near("n sigma", (rd_cmb - r3) / math.hypot(s3, s_cmb), 3.5, 0.06)

near("H0 from DESI h r_d with CMB r_d", 100 * 101.54 / 147.00, 69.07, 0.006)
spread = 101.54 / 98.77 - 1
print(f"  spread in h r_d DESI vs CMB = {spread:.4f}; (138.6-134.8)/147 = {(r1 - r2) / 147:.4f}; r1/r2-1 = {r1 / r2 - 1:.4f}")
units("299792.458 km/s / (29.54 * 73.26 km/s/Mpc)", "Mpc")
quantity("101.54 Mpc / 0.73264", "138.594 Mpc", rel_tol=1e-4)
limit("c/(b*H)*H", "H", 1, "c/b")  # trivial scaling check: r_d * H0 is constant along the BAO degeneracy
raise SystemExit(finish())
