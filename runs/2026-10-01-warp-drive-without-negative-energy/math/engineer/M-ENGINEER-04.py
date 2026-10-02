"""M-ENGINEER-04 (F8): at fixed compactness C = 2GM/(c^2 R2) with R1 = R2/2:
M = C c^2 R2/(2G) (prop. R2); rho_mean = M/((4/3)pi(R2^3 - R1^3)) = 3 C c^2/(7 pi G R2^2) (prop. C/R2^2);
characteristic stress ~ G M rho/R2 prop. C^2/R2^2. Exact GR statement: the TOV system is invariant under
r -> L r, m -> L m, rho -> rho/L^2, P -> P/L^2. Numbers: rho_mean = nuclear (0.16 fm^-3) at R2 = 15 km,
M = 1.7 M_sun; rho_mean = osmium (2.26e4 kg/m^3) at R2 = 5.2e10 m, M = 5.9e6 M_sun. C = 0.335. SI."""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, limit, units, quantity, finish

Cc, cc, Gg, R, L, r, m, rho, P = sp.symbols("C_c c_c G_g R L r m rho P", positive=True)
Mexpr = Cc * cc**2 * R / (2 * Gg)
rho_mean = Mexpr / (sp.Rational(4, 3) * sp.pi * (R**3 - (R / 2)**3))
identity(rho_mean, 3 * Cc * cc**2 / (7 * sp.pi * Gg * R**2))
identity(Gg * Mexpr * rho_mean / R, 3 * Cc**2 * cc**4 / (14 * sp.pi * Gg * R**2))
# TOV right-hand side dP/dr scales as L^-3 under the self-similar map (so P scales as L^-2)
def tov(r, m, rho, P):
    return -Gg * (rho + P / cc**2) * (m + 4 * sp.pi * r**3 * P / cc**2) / (r**2 * (1 - 2 * Gg * m / (cc**2 * r)))
identity(tov(L * r, L * m, rho / L**2, P / L**2), tov(r, m, rho, P) / L**3,
         domain={"r": (1, 10), "m": (0.01, 0.1), "rho": (0.1, 10), "P": (0.01, 1), "L": (0.1, 10),
                 "G_g": (0.1, 1), "c_c": (1, 3), "C_c": (0.1, 1)})
limit(rho_mean, "R", "oo", "0")
C = 0.335
def R_at(rho_target):
    return math.sqrt(3 * C * c**2 / (7 * math.pi * G * rho_target))
Rn, Ro = R_at(RHO_NUC), R_at(RHO_OS)
Mn, Mo = C * c**2 * Rn / (2 * G), C * c**2 * Ro / (2 * G)
rel("R2 at nuclear mean density (m)", Rn, 1.5e4, 0.03)
rel("M there (M_sun)", Mn / Msun, 1.7, 0.03)
rel("R2 at osmium mean density (m)", Ro, 5.2e10, 0.02)
rel("M there (M_sun)", Mo / Msun, 5.9e6, 0.02)
units("c^2/(G*1 m^2)", "kg/m^3")
quantity("0.335*c^2*15.2 km/(2*G)", "1.72 Msun", rel_tol=0.02)
raise SystemExit(finish())
