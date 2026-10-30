"""M-STATISTICIAN-02: CCHP total error, CCHP tensions, SH0ES-CCHP with correlation (F2, S6, S7).
Var(a-b) = sa^2 + sb^2 - 2 rho sa sb; km/s/Mpc."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import sympy as sp
from _common import tension, quad, close
from math_checks import sign, limit, units, finish

s = quad(1.22, 1.33, 0.70)
close("CCHP total sigma", s, 1.94, 0.005)
for name, b, cl in [("CMB-SPA", (67.19, .38, .38), 1.62), ("PR4", (67.64, .52, .52), 1.37), ("BAO+BBN", (68.50, .58, .58), 0.94)]:
    close("CCHP vs " + name, tension(70.39, s, s, *b), cl, 0.01)
for rho, cl in [(0, 1.44), (0.3, 1.65), (0.5, 1.85), (0.8, 2.36)]:
    close(f"SH0ES-CCHP rho={rho}", tension(73.49, .93, .93, 70.39, s, s, rho), cl, 0.01)
close("JAGB CCHP vs SH0ES-side diff/sigma", 5.5 / quad(quad(1.4, 2.0), quad(2.17, 1.64)), 1.5, 0.02)
close("  sigma of JAGB difference", quad(quad(1.4, 2.0), quad(2.17, 1.64)), 3.65, 0.01)

# Sign claim: positive rho raises z. dz/drho for z = d / sqrt(a^2+b^2-2 rho a b)
d, a, b, rho = sp.symbols("d a b rho", positive=True)
z = d / sp.sqrt(a**2 + b**2 - 2 * rho * a * b)
sign(sp.diff(z, rho), "positive", domain={"d": (0.1, 10), "a": (0.1, 10), "b": (0.1, 10), "rho": (0, 0.95)})
limit(z, "rho", 0, d / sp.sqrt(a**2 + b**2))
units("3.10 km/s/Mpc / (2.1475 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
