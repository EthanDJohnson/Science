"""M-CONSTRAINTS-07 (F7): EDE fluid (n = 3, w_n = 1/2, rho ~ a^-4.5 after z_c), background only.
f = rho_EDE(z_c)/rho_tot(z_c). theta_* held at its CMB-SPA LCDM value (my model, h = 0.6719, Omega_m = 0.3175);
closure Omega_m = 0.3175 (omega_c = Omega_m h^2 - omega_b - omega_nu). z_* from the LCDM fit (EDE ignored there, as in the lens).
Lens: f = 0.124 (z_c 3500), 0.137 (1e4), 0.188 (1500) for H0 = 73.26; omega_c ~0.146; omega_c-fixed closure f = 0.052, Omega_m ~0.27;
at f = 0.06-0.07 (Omega_m fixed) H0 ~ 70-70.5."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import finish
from _bg import Model, ONU, bisect, near

wb, Om = 0.02237, 0.3175
mk = lambda h, **k: Model(h, wb, Om * h * h - wb - ONU, **k)
ref = mk(0.6719).theta100()
# limit: f -> 0 recovers LCDM baseline
near("f -> 0 limit theta", mk(0.6719, f_ede=1e-9, zc=3500).theta100(), ref, 1e-7)
# check the fluid definition: rho_EDE(a_c) / rho_tot(a_c) = f
m = mk(0.73264, f_ede=0.12, zc=3500); ac = m.ac
near("f definition", m._ede(ac) / m.E2(ac), 0.12, 1e-9)
for zc, want in [(3500, 0.124), (1e4, 0.137), (1500, 0.188)]:
    f = bisect(lambda f: mk(0.73264, f_ede=f, zc=zc).theta100() - ref, 1e-4, 0.5, tol=1e-6)
    print(f"z_c={zc:g}: f needed {f:.4f}; omega_c {Om*0.73264**2-wb-ONU:.4f}")
    near(f"f needed z_c={zc:g}", f, want, 0.012)
# omega_c-fixed closure
wc0 = Om * 0.6719**2 - wb - ONU
f = bisect(lambda f: Model(0.73264, wb, wc0, f_ede=f, zc=3500).theta100() - ref, 1e-4, 0.5, tol=1e-6)
print(f"omega_c fixed: f {f:.4f}, Omega_m {Model(0.73264, wb, wc0).Om:.4f}")
near("f (omega_c fixed)", f, 0.052, 0.008)
for f in (0.06, 0.07):
    h = bisect(lambda h: mk(h, f_ede=f, zc=3500).theta100() - ref, 0.6, 0.8, tol=1e-7)
    print(f"f={f}: H0 = {100*h:.2f}")
    near(f"H0 at f={f}", 100 * h, 70.25, 0.6)
raise SystemExit(finish())
