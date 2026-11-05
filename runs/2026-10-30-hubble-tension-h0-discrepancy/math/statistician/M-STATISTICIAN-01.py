"""M-STATISTICIAN-01: headline pairwise tensions (F1, table B, S1, S2).
z = |a-b| / sqrt(sa^2 + sb^2), uncorrelated, facing-side errors; p2 = erfc(z/sqrt2). km/s/Mpc."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
from _common import tension, p2_of_z, quad, close
from math_checks import limit, units, identity, finish

SH = (73.49, 0.93, 0.93); SPA = (67.19, 0.38, 0.38); PR4 = (67.64, 0.52, 0.52)
BB = (68.50, 0.58, 0.58); DC = (68.17, 0.28, 0.28); R22 = (73.04, 1.04, 1.04); PR3 = (67.36, 0.54, 0.54)
DN = (73.264, 0.806, 0.806); DNCMB = (67.24, 0.35, 0.35)
JAGB_S = (73.3, float(quad(1.4, 2.0)), float(quad(1.4, 2.0)))
SBF = (73.8, float(quad(0.7, 2.3)), float(quad(0.7, 2.3)))
WH = (70.59, 1.15, 1.15)
JAGB_C = (67.80, float(quad(2.17, 1.64)), float(quad(2.17, 1.64)))
TD = (71.1, 2.4, 2.3); MAS = (71.6, 3.7, 3.7); GW = (71.7, 9.4, 7.5)
CCHP_s = float(quad(1.22, 1.33, 0.70)); CC = (70.39, CCHP_s, CCHP_s)

print("Formula checks")
limit("d/sqrt(a**2 + b**2)", "b", 0, "d/a")          # reduces to single-error significance
identity("erfc(z/sqrt(2))", "2*(1 - (1 + erf(z/sqrt(2)))/2)")  # p2 = 2(1 - Phi(z))
units("6.30 km/s/Mpc / (1.0046 km/s/Mpc)", "dimensionless")

print("Finding 1")
z = tension(*SH, *SPA); close("SH0ES vs CMB-SPA z", z, 6.27, 0.01)
close("  p2 (x1e10)", p2_of_z(z) * 1e10, 3.6, 0.1)
close("SH0ES vs PR4", tension(*SH, *PR4), 5.49, 0.01)
close("SH0ES vs BAO+BBN", tension(*SH, *BB), 4.55, 0.01)
close("SH0ES vs DESI+CMB", tension(*SH, *DC), 5.48, 0.01)
close("R22 vs PR3", tension(*R22, *PR3), 4.85, 0.01)
close("H0DN vs CMB-SPA", tension(*DN, *SPA), 6.82, 0.01)
close("H0DN vs 67.24+-0.35", tension(*DN, *DNCMB), 6.86, 0.01)
close("H0DN vs BAO+BBN", tension(*DN, *BB), 4.80, 0.01)

print("Table B (vs CMB-SPA / vs BAO+BBN)")
for name, v, c1, c2 in [("SH0ES-side JAGB", JAGB_S, 2.47, 1.91), ("SBF", SBF, 2.72, 2.14),
                        ("Wojtak-Hjorth 70.59", WH, 2.81, 1.62), ("TDCOSMO", TD, 1.68, 1.10),
                        ("CCHP", CC, 1.62, 0.94), ("masers", MAS, 1.19, 0.83), ("sirens", GW, 0.60, 0.43),
                        ("CCHP JWST JAGB", JAGB_C, 0.22, 0.25)]:
    close(name + " vs SPA", tension(*v, *SPA), c1, 0.011)
    close(name + " vs BB", tension(*v, *BB), c2, 0.011)
close("H0DN-noCeph vs SPA", tension(72.509, 1.296, 1.296, *SPA), 3.94, 0.01)
raise SystemExit(finish())
