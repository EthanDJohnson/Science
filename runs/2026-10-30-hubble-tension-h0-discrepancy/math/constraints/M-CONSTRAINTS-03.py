"""M-CONSTRAINTS-03 (F3): theta_* budget. theta_* = r_s(z_*)/D_M(z_*) fixed.
Baseline CMB-SPA: h = 0.6719, Omega_m = 0.3175, omega_b = 0.02237 -> omega_c = Omega_m h^2 - omega_b - omega_nu.
(a) Omega_m fixed, h = 0.73264: required r_* change = D_M(new)/D_M(base) - 1; omega_c(new).
(b) omega_c fixed: same, and Omega_m(new). Lens: -8.23% (73.26), -8.51% (73.49), omega_c 0.1203->0.1474 (+22.5%);
fixed omega_c: -1.69%, Omega_m = 0.267."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import units, finish
from _bg import Model, ONU, near

wb, Om, h0 = 0.02237, 0.3175, 0.6719
wc0 = Om * h0**2 - wb - ONU
base = Model(h0, wb, wc0)
zs = base.zstar(); D0 = base.DM(zs); r0 = base.rs(zs)
print(f"baseline wc={wc0:.5f} z*={zs:.2f} D_M={D0:.2f} Mpc r*={r0:.3f} Mpc 100theta={100*r0/D0:.5f}")
near("baseline omega_c", wc0, 0.1203, 0.0002)

def req(h, wc):
    m = Model(h, wb, wc)
    return m.DM(m.zstar()) / D0 - 1, m

for h, want in [(0.73264, -0.0823), (0.7349, -0.0851)]:
    wc = Om * h**2 - wb - ONU
    d, m = req(h, wc)
    print(f"Om fixed h={h}: wc={wc:.5f} dr*/r* = {d:.5f}")
    near("r_* change (Om fixed)", d, want, 0.002)
    if h == 0.73264:
        near("omega_c new", wc, 0.1474, 0.0003)
        near("omega_c rise", wc / wc0 - 1, 0.225, 0.005)
d, m = req(0.73264, wc0)
print(f"wc fixed: dr*/r* = {d:.5f}, Om = {m.Om:.4f}")
near("r_* change (wc fixed)", d, -0.0169, 0.002)
near("Omega_m (wc fixed)", m.Om, 0.267, 0.002)
near("sigma vs DESI", (0.2975 - m.Om) / 0.0086, 3.5, 0.15)
near("sigma vs SPA", (0.3175 - m.Om) / 0.0055, 9.0, 0.3)
# limit: radiation-free, z_* fixed, Omega_m fixed -> D_M proportional to 1/h exactly
print("limit check, matter+Lambda only: 1 - h0/h =", 1 - h0 / 0.73264)
near("Om-fixed result vs pure 1/h scaling (radiation + z_* shift only)", d * 0 + req(0.73264, Om * 0.73264**2 - wb - ONU)[0], -(1 - h0 / 0.73264), 0.003)
units("299792.458 km/s / (67.19 km/s/Mpc)", "Mpc")
raise SystemExit(finish())
