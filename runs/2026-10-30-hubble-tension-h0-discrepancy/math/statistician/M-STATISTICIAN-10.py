"""M-STATISTICIAN-10: EDE scoring (F17, S10) and cosmic-variance multiples (F18).
Delta chi2 with k extra parameters -> p = chi2_sf(dchi2, k) -> two-sided z.
Gap fraction = (H_model - 67.19)/(73.49 - 67.19). Residual = tension with SH0ES 73.49 +- 0.93, facing-side errors.
Cosmic-variance multiple = gap / 0.31 km/s/Mpc."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
from _common import chi2_sf, z_of_p2, tension, close
from math_checks import limit, units, finish

for d, cl_p, cl_z in [(4.3, 0.23, 1.2), (6.6, 0.086, 1.7)]:
    p = chi2_sf(d, 3)
    close(f"dchi2 = {d}, 3 dof: p", p, cl_p, 0.003)
    close(f"  z", z_of_p2(p), cl_z, 0.03)
SH = (73.49, .93, .93)
models = [("PMF", (69.1, .5, .5), 30, 4.2), ("e-density (D-95)", (69.3, .5, .5), 33, 4.0),
          ("mod. recombination", (69.6, 1.0, 1.0), 38, 2.9), ("ACT EDE P-ACT-LB", (69.9, .8, 1.5), 43, 2.9),
          ("Poulin EDE", (71.0, 1.1, 1.1), 60, 1.7), ("eROSITA EDE (D-94)", (71.4, 1.4, 1.4), 67, 1.2)]
for name, v, frac, res in models:
    close(name + " gap fraction %", 100 * (v[0] - 67.19) / (73.49 - 67.19), frac, 0.6)
    close(name + " residual vs SH0ES (tol 0.06: lens rounds to 1 decimal)", tension(*v, *SH), res, 0.06)
print("Cosmic-variance multiples (sigma_loc = 0.31)")
close("SH0ES - CMB-SPA", (73.49 - 67.19) / 0.31, 20.3, 0.05)
close("local late mean - early mean", (72.7723 - 67.5834) / 0.31, 16.7, 0.05)
close("CCHP - CMB-SPA", (70.39 - 67.19) / 0.31, 10.3, 0.05)
limit("(h - a)/(b - a)", "h", "b", "1", domain={"a": (60, 68), "b": (70, 80)})
units("6.30 km/s/Mpc / (0.31 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
