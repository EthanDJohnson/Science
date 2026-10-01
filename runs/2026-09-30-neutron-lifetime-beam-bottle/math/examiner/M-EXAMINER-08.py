"""M-EXAMINER-08: look-elsewhere (Sidak, k = 5) and minimum Bayes factor (F12).
p_glob = 1 - (1 - p_loc)^k with two-sided Gaussian p; Sellke bound B_min = 1/(-e p ln p) for p < 1/e. Dimensionless."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
from math_checks import inequality, limit, finish
from _h import cmp, z_of_p2, p2_of_z, chi2_sf

# local values taken from M-EXAMINER-01/02 (my own recomputation), chi2 with 1 dof
loc = {"proton vs rest": (21.8018, 4.33), "beam vs bottle": (16.4876, 3.67),
       "BL1 vs rest": (16.9992, 3.73), "material vs magnetic": (15.0718, 3.47)}
odds = {"proton vs rest": 9.6e3, "beam vs bottle": 7.6e2}
for k, (chi2, zc) in loc.items():
    p = chi2_sf(chi2, 1)
    pg = 1 - (1 - p) ** 5
    zg = z_of_p2(pg)
    B = 1 / (-math.e * p * math.log(p))
    print(f"{k}: p_loc {p:.3e} -> p_glob {pg:.3e}, z {zg:.3f}; Sellke max odds {B:.3g}; with p_glob {1/(-math.e*pg*math.log(pg)):.3g}")
    cmp(f"{k} z_glob", zg, zc, 0.006)
    if k in odds:
        cmp(f"{k} odds", B, odds[k], 50 if odds[k] > 1e3 else 5)
print(f"p_glob proton vs rest (lens 1.5e-5): {1-(1-chi2_sf(21.8018,1))**5:.3e}")
inequality("1 - (1 - p)**5", "<=", "5*p", domain={"p": (0, 1)})
inequality("1 - (1 - p)**5", ">=", "p", domain={"p": (0, 1)})
limit("(1 - (1 - p)**5)/p", "p", 0, "5")
raise SystemExit(finish())
