"""M-EXAMINER-10 (SI): plasma cutoffs.
(a) f_p = (1/2 pi) sqrt(n_e e^2/(eps0 m_e)) = 8980 Hz sqrt(n_e/cm^-3); a 150 Hz photon propagates only if f_p < 150 Hz,
    i.e. n_e < (150/8980)^2 cm^-3 = 2.8e-4 cm^-3.
(b) Early universe (assumption: fully ionised, n_e = n_e0 (1+z)^3, n_e0 = 2.2e-7 cm^-3 from Omega_b h^2 = 0.0224,
    X_e incl. He ~ 0.88): photon observed at 150 Hz has f = 150 (1+z) Hz; f_p ∝ (1+z)^(3/2). Evanescent when
    1+z > (150 Hz / f_p0)^2. Lens claim: ~1300. (Real ionisation falls below z ~ 1100; the claim is the threshold only.)"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, quantity, finish

e, eps0, me = 1.602176634e-19, 8.8541878128e-12, 9.1093837015e-31
coef = math.sqrt(1e6 * e ** 2 / (eps0 * me)) / (2 * math.pi)   # Hz per sqrt(cm^-3)
print(f"f_p coefficient = {coef:.1f} Hz per sqrt(n_e / cm^-3)")
identity(sp.Float(f"{coef:.3g}"), sp.Float("8980"))
nmax = (150 / coef) ** 2
print(f"n_e max for 150 Hz = {nmax:.3e} cm^-3")
identity(sp.Float(f"{nmax:.2g}"), sp.Float("2.8e-4"))
# n_e0 from Omega_b h^2
mp_, rho_c_h2 = 1.67262192e-27, 1.87834e-26      # kg; critical density / h^2 in kg m^-3
nb = 0.0224 * rho_c_h2 / mp_ / 1e6                # cm^-3 (baryons, as protons)
ne0 = 0.88 * nb
fp0 = coef * math.sqrt(ne0)
zz = (150 / fp0) ** 2
print(f"n_b = {nb:.3e} cm^-3; n_e0 = {ne0:.3e} cm^-3; f_p0 = {fp0:.2f} Hz; evanescent for 1+z > {zz:.0f}")
identity(sp.Float(f"{zz:.1g}"), sp.Float("1e3"))
# scaling limit: f/f_p ∝ (1+z)^(-1/2) -> 0 as z -> inf (always evanescent early enough)
z = sp.Symbol("z", positive=True)
print("f/f_p scaling:", sp.simplify((150 * (1 + z)) / (fp0 * (1 + z) ** sp.Rational(3, 2))))
raise SystemExit(finish())
