"""M-EMPIRICIST-13: small arithmetic claims.
(a) empirical local-structure scatter 0.60% of H0 is 'about 0.4 km/s/Mpc' (H0 between 67.19 and 73.49);
(b) 7 of 8 non-SH0ES local point estimates lie above CMB-SPA 67.19;
(c) TDCOSMO 71.1 +2.4/-2.3 is 3.3%, and reaching 1.5% / 0.8% needs a 'two- to four-fold' improvement.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
from math_checks import quantity, units, finish
from _common import H, cmp

quantity("0.0060 * 67.19 km/s/Mpc", "0.4 km/s/Mpc", rel_tol=0.1)
quantity("0.0060 * 73.49 km/s/Mpc", "0.4 km/s/Mpc", rel_tol=0.11)
units("0.0060 * 73.49 km/s/Mpc", "km/s/Mpc")
pts = ["CCHP", "SBF", "TF", "TDCOSMO", "masers", "sirens", "H0pe", "Refsdal"]
above = sum(H[p][0] > H["CMB"][0] for p in pts)
print(f"  above CMB-SPA: {[p for p in pts if H[p][0] > H['CMB'][0]]}")
cmp("count above CMB-SPA of 8", above, 7, 0.01)
frac = 100 * H["TDCOSMO"][1] / H["TDCOSMO"][0]
cmp("TDCOSMO fractional error [%]", frac, 3.3, 0.06)
cmp("improvement factor to 1.5%", frac / 1.5, 2.0, 0.3)
cmp("improvement factor to 0.8%", frac / 0.8, 4.0, 0.2)
raise SystemExit(finish())
