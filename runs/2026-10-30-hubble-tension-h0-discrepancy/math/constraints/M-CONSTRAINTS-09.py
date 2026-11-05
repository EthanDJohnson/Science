"""M-CONSTRAINTS-09 (F9): varying m_e at background level: z_* proportional to m_e (recombination temperature ~ binding energy).
theta_* fixed at the CMB-SPA LCDM value of my model. Closures at H0 = 73.26:
(a) Omega_m = 0.3175 fixed -> lens delta = +6.25%;  (b) omega_b, omega_c proportional to m_e^2 -> lens +2.94%, Omega_m 0.282, omega_b 0.0237.
Exact symmetry check: scaling all omega_i (incl. radiation) and z_* by m_e leaves theta_* invariant at fixed h... is NOT exact because
Lambda and radiation are not scaled; we only check the numbers."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import finish
from _bg import Model, ONU, bisect, near

wb, Om, h0, h1 = 0.02237, 0.3175, 0.6719, 0.73264
wc0 = Om * h0**2 - wb - ONU
ref = Model(h0, wb, wc0).theta100()
near("delta=0 limit", Model(h0, wb, wc0, me=1.0).theta100(), ref, 1e-12)
da = bisect(lambda d: Model(h1, wb, Om * h1**2 - wb - ONU, me=1 + d).theta100() - ref, 0.0, 0.2, tol=1e-7)
print("Omega_m fixed: delta =", da)
near("delta (Omega_m fixed)", da, 0.0625, 0.004)
db = bisect(lambda d: Model(h1, wb * (1 + d)**2, wc0 * (1 + d)**2, me=1 + d).theta100() - ref, 0.0, 0.2, tol=1e-7)
m = Model(h1, wb * (1 + db)**2, wc0 * (1 + db)**2)
print(f"scaling: delta = {db:.4f}, Omega_m = {m.Om:.4f}, omega_b = {wb*(1+db)**2:.5f}")
near("delta (scaling)", db, 0.0294, 0.003)
near("Omega_m (scaling)", m.Om, 0.282, 0.003)
near("omega_b (scaling)", wb * (1 + db)**2, 0.0237, 0.0002)
near("Omega_m sigma vs DESI", (0.2975 - m.Om) / 0.0086, 1.8, 0.3)
near("Omega_m sigma vs SN", (0.322 - m.Om) / 0.012, 3.3, 0.3)
near("omega_b sigma vs BBN prior 0.02218+-0.00055", (wb * (1 + db)**2 - 0.02218) / 0.00055, 2.8, 0.3)
raise SystemExit(finish())
