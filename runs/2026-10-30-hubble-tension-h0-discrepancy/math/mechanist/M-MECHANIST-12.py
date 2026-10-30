"""M-MECHANIST-12: G_eff transition sizing (finding 11).
Assumption (ASSUMED Arnett/Chandrasekhar): L_peak ∝ M_Ch ∝ G^(-3/2). Hubble-flow SNe must be Δm = 0.188 mag
brighter than calibrators: L_HF/L_loc = 10^(0.4 Δm). Then G_HF/G_loc = (L_HF/L_loc)^(-2/3).
Window: d = c z / H0 at z = 0.01 and 0.023 with H0 = 73.264 km/s/Mpc (Hubble law, z << 1).
Sign: brighter HF SNe (L ratio > 1) require G_HF < G_loc.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, sign, limit, quantity, finish
from mm_common import dmag, near

dm, k = sp.symbols("dm k", positive=True)
Lr = 10 ** (sp.Rational(2, 5) * dm)
Gr = Lr ** sp.Rational(-2, 3)
identity(sp.log(Gr), -sp.Rational(4, 15) * dm * sp.log(10))  # ln G ratio = -(4/15) ln10 Δm
sign(sp.log(Gr), "negative", domain={"dm": (1e-6, 1)})       # G_HF < G_loc
limit("10**(-4*dm/15)", "dm", 0, "1")
gap = dmag(73.264, 67.19)
near("L ratio", 10 ** (0.4 * gap), 1.189, 0.001)
near("G ratio", 10 ** (-4 * gap / 15), 0.891, 0.001)
quantity("299792.458 km/s * 0.01 / (73.264 km/s/Mpc)", "40.9 Mpc", rel_tol=2e-3)
near("inner edge Mpc", 299792.458 * 0.01 / 73.264, 41, 0.5)
near("outer edge Mpc", 299792.458 * 0.023 / 73.264, 94, 0.5)
raise SystemExit(finish())
