"""M-STATISTICIAN-10: lambda by route (F10). |lambda| dimensionless; stat (+) sys in quadrature; asymmetric sys symmetrized.
Inputs D-40..D-42 and the listing value in F10 (WIETFELDT 24 1.2712 +- 0.0061).
Lens: A route 1.27623 +- 0.00050, chi2 1.51/2; a route 1.26884 +- 0.00248, 3.58/1; swapped 1.26752 +- 0.00247, 0.44/1;
between-route chi2 8.56 (2.93 sigma), 11.96 (3.46 sigma); PERKEO III vs aSPECT 2024 3.49 sigma."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, finish

P3 = ("PERKEO III", 1.27641, q(0.00045, 0.00033))
UCNA = ("UCNA", 1.2772, 0.0020)
P2 = ("PERKEO II", 1.2748, q(0.0008, sym(0.0010, 0.0011)))
ASP = ("aSPECT24", 1.2668, 0.0027)
ACO = ("aCORN21", 1.2796, 0.0062)
WIE = ("WIETFELDT24", 1.2712, 0.0061)
A = wmean([P3, UCNA, P2]); a1 = wmean([ASP, ACO]); a2 = wmean([ASP, WIE])
for lab, r, lm, ls, lc in [("A", A, "1.27623", "0.00050", "1.51"), ("a", a1, "1.26884", "0.00248", "3.58"), ("a swapped", a2, "1.26752", "0.00247", "0.44")]:
    print(f"{lab}: {r[0]:.5f} +- {r[1]:.5f}, chi2 {r[2]:.2f}/{r[3]}  (lens {lm} +- {ls}, {lc})")
    identity(f"{r[0]:.5f}", lm); identity(f"{r[1]:.5f}", ls); identity(f"{r[2]:.2f}", lc)
for lab, b, lc, lz in [("A vs a", a1, "8.56", "2.93"), ("A vs a swapped", a2, "11.96", "3.46")]:
    c = (A[0] - b[0]) ** 2 / (A[1] ** 2 + b[1] ** 2); z = math.sqrt(c)
    print(f"{lab}: chi2 {c:.2f}, z {z:.2f} (lens {lc}, {lz})"); identity(f"{c:.2f}", lc); identity(f"{z:.2f}", lz)
z = (P3[1] - ASP[1]) / q(P3[2], ASP[2]); print("PERKEO III vs aSPECT", z); identity(f"{z:.2f}", "3.49")
raise SystemExit(finish())
