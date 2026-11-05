"""M-DECOMPOSER-01: gap sizes and pairwise tensions (F1).

Claim: D = H_loc - H_early (km/s/Mpc), D/H_early in %, 5 log10(H_loc/H_early) mag,
z = D / sqrt(s_loc^2 + s_early^2) (uncorrelated Gaussian).
"""
import sys
import math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import num, tension, quad, finish, limit, units
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import series

H0DN = (73.264, 0.806)
SH0ES = (73.49, 0.93)
SPA = (67.19, 0.38)
BAO = (68.50, 0.58)
CCHP = (70.39, quad(1.22, 1.33, 0.70))
CCHPJ = (68.81, 2.25)

d = H0DN[0] - SPA[0]
num("H0DN-SPA gap km/s/Mpc", d, 6.07, 0.006)
num("H0DN-SPA gap sigma", math.hypot(H0DN[1], SPA[1]), 0.89, 0.006)
num("H0DN-SPA percent (of early value)", 100 * d / SPA[0], 9.0, 0.06)
num("H0DN-SPA mag", 5 * math.log10(H0DN[0] / SPA[0]), 0.188, 0.0006)
num("H0DN-SPA z", tension(*H0DN, *SPA), 6.8, 0.06)
num("SH0ES-SPA gap", SH0ES[0] - SPA[0], 6.30, 0.006)
num("SH0ES-SPA sigma", math.hypot(SH0ES[1], SPA[1]), 1.00, 0.006)
num("SH0ES-SPA mag", 5 * math.log10(SH0ES[0] / SPA[0]), 0.195, 0.0006)
num("SH0ES-SPA z", tension(*SH0ES, *SPA), 6.3, 0.06)
num("H0DN-BAO+BBN z", tension(*H0DN, *BAO), 4.8, 0.06)
num("SH0ES-BAO+BBN z", tension(*SH0ES, *BAO), 4.6, 0.06)
num("CCHP total sigma", CCHP[1], 1.94, 0.006)
num("CCHP-SPA z", tension(*CCHP, *SPA), 1.6, 0.06)
num("CCHP-BAO z", tension(*CCHP, *BAO), 0.9, 0.06)
num("CCHP JWST-SPA z", tension(*CCHPJ, *SPA), 0.7, 0.06)
num("CCHP JWST-BAO z", tension(*CCHPJ, *BAO), 0.1, 0.06)

# "factor ~7 in significance": max 6.8 / min 0.1 is ~68, 6.8/0.7 ~ 10, 6.8/1.0? report the ratio
print("  ratio of largest z (6.8) to CCHP-JWST vs SPA z:", tension(*H0DN, *SPA) / tension(*CCHPJ, *SPA))

# Structural checks: mag gap small-x series 5 log10(1+x) ~ (5/ln10) x; z -> D/s_a as s_b -> 0
x = sp.symbols("x", positive=True)
series(5 * sp.log(1 + x) / sp.log(10), "x", 0, 2, 5 * x / sp.log(10))
limit("D/sqrt(sa**2 + sb**2)", "sb", 0, "D/sa")
units("(73.264 km/s/Mpc - 67.19 km/s/Mpc) / (0.89 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
