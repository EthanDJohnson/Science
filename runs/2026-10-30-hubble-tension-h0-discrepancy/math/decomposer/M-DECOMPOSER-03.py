"""M-DECOMPOSER-03: tensions with blocks of local evidence removed (F3).

Inverse-variance mean of a local block, then z = |m - H_early| / sqrt(s_m^2 + s_early^2),
uncorrelated, against CMB-SPA 67.19 +- 0.38 and DESI BAO+BBN 68.50 +- 0.58 km/s/Mpc.
"""
import sys
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import TEN, wmean, tension, num, finish, limit, units

SPA, BAO = TEN["CMB"], TEN["BAOBBN"]
blocks = {
    "one-step": (["TD", "MASER", "SIREN"], 71.27, 1.93, 2.1, 1.4),
    "all local except SH0ES": (["CCHP", "SBF", "TD", "MASER", "SIREN"], 71.56, 1.19, 3.5, 2.3),
    "SBF + one-step": (["SBF", "TD", "MASER", "SIREN"], 72.26, 1.51, 3.3, 2.3),
    "all local": (["SH0ES", "CCHP", "SBF", "TD", "MASER", "SIREN"], 72.76, 0.73, 6.7, 4.6),
}
for label, (names, m_l, s_l, z1, z2) in blocks.items():
    m, s = wmean([TEN[n] for n in names])
    num(f"{label} mean", m, m_l, 0.006)
    num(f"{label} sigma", s, s_l, 0.006)
    num(f"{label} z vs SPA", tension(m, s, *SPA), z1, 0.06)
    num(f"{label} z vs BAO+BBN", tension(m, s, *BAO), z2, 0.06)

# weighted mean -> the precise point as its error goes to zero
limit("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "s1", 0, "x1", domain={"x1": (60, 80), "x2": (60, 80)})
units("(72.76 km/s/Mpc - 67.19 km/s/Mpc)/(0.83 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
