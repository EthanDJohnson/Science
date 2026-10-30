"""M-CONSTRAINTS-06 (F6): ages t0 = int_0^1 da/(a H) in flat LCDM with radiation.
CMB-SPA: h = 0.6719, Omega_m = 0.3175 -> lens 13.804 Gyr (quoted 13.805). h = 0.73264, Omega_m 0.2975-0.3175 -> 12.66-12.89 Gyr;
sigma against t_U = 13.81 +- 0.25 +- 0.23 Gyr (quadrature 0.34) -> 2.7-3.4 sigma. Matter-dominated limit: t0 = 2/(3 H0)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import quantity, units, finish
from _bg import Model, ONU, near

wb = 0.02237
def age(h, Om):
    return Model(h, wb, Om * h * h - wb - ONU).age()

near("t0 CMB-SPA", age(0.6719, 0.3175), 13.805, 0.03)
sg = math.hypot(0.25, 0.23)
for Om, want in [(0.2975, 12.89), (0.3175, 12.66)]:
    t = age(0.73264, Om)
    print(f"Om={Om}: t0={t:.3f} Gyr, {(13.81-t)/sg:.2f} sigma")
    near("t0", t, want, 0.03)
near("n sigma (Om 0.2975)", (13.81 - age(0.73264, 0.2975)) / sg, 2.7, 0.1)
near("n sigma (Om 0.3175)", (13.81 - age(0.73264, 0.3175)) / sg, 3.4, 0.1)
# limit: Einstein-de Sitter (Omega_m -> 1, no radiation) t0 = 2/(3H0)
m = Model(0.7, 0.0, 0.49 - ONU, neff=0.0); m.wr = 0.0; m.wde = 0.0
near("EdS limit t0 / (2/(3H0))", m.age() / (2 / 3 * 977.792 / 70), 1.0, 1e-3)
quantity("2/3 / (70 km/s/Mpc)", "9.312 Gyr", rel_tol=1e-3)
units("1 / (73 km/s/Mpc)", "s")
raise SystemExit(finish())
