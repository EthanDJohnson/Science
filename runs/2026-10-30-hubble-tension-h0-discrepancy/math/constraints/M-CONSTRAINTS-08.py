"""M-CONSTRAINTS-08 (F8): N_eff needed for H0 = 73.26 at fixed theta_* (background; z_* from the LCDM fit).
omega_r = omega_gamma (1 + 0.2271 N_eff). Closures: z_eq fixed (omega_m scaled with omega_r, omega_b fixed) -> lens 4.32;
Omega_m = 0.3175 fixed -> 4.41; omega_c fixed -> 3.56 (Omega_m ~0.26-0.267). sigma vs ACT 2.86 +- 0.13."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import finish
from _bg import Model, ONU, omega_r, bisect, near

wb, Om, h0, h1 = 0.02237, 0.3175, 0.6719, 0.73264
wm0 = Om * h0**2
ref = Model(h0, wb, wm0 - wb - ONU).theta100()
near("N_eff=3.044 limit, Om fixed, recovers h0", 100 * bisect(lambda h: Model(h, wb, Om*h*h - wb - ONU).theta100() - ref, 0.6, 0.8, tol=1e-8), 67.19, 0.01)
def solve(wm_of_N):
    return bisect(lambda N: Model(h1, wb, wm_of_N(N) - wb - ONU, neff=N).theta100() - ref, 3.0, 7.0, tol=1e-6)
Nz = solve(lambda N: wm0 * omega_r(N) / omega_r(3.044))
NO = solve(lambda N: Om * h1**2)
Nc = solve(lambda N: wm0)
for lab, N, want in [("z_eq fixed", Nz, 4.32), ("Omega_m fixed", NO, 4.41), ("omega_c fixed", Nc, 3.56)]:
    print(f"{lab}: N_eff = {N:.3f}, {(N-2.86)/0.13:.1f} sigma")
    near(lab, N, want, 0.08)
near("n sigma (z_eq)", (Nz - 2.86) / 0.13, 11.2, 0.8)
near("n sigma (omega_c fixed)", (Nc - 2.86) / 0.13, 5.4, 0.7)
raise SystemExit(finish())
