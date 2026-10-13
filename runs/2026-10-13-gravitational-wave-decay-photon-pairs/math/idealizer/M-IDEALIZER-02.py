"""M-IDEALIZER-02: scalar channel 14/675, 7/(450 pi), tau_phi/tau = 54/7.

Natural units. Same coherent state as M-01. Scalar amplitude (real-sign sum over graviton helicities)
8 pi G (2 t u/s) = 4 pi G s sin^2(Th_cm), one final configuration, identical real scalars (factor 1/2).
Photon: 4 pi G s (1 + cos^2 Th_cm), two configurations, factor 1/2. Everything else is common, so
c_scalar/c_photon = [1 * Int dOmega R_s^2] / [2 * Int dOmega R_g^2], R = graviton-ring average at cos(axis,K) = 0.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, finish
import sympy as sp

t, u, s, ct, phi, G = sp.symbols("t u s ct phi G", real=True)
c = sp.symbols("c", real=True)
# amplitudes in terms of CM angle cos = c
tt, uu = -s * (1 - c) / 2, -s * (1 + c) / 2
identity(sp.expand(8 * sp.pi * G * (tt**2 + uu**2) / s), sp.expand(4 * sp.pi * G * s * (1 + c**2)), domain={"c": (-1, 1), "s": (0.1, 10), "G": (0.1, 10)})
identity(sp.expand(8 * sp.pi * G * 2 * tt * uu / s), sp.expand(4 * sp.pi * G * s * (1 - c**2)), domain={"c": (-1, 1), "s": (0.1, 10), "G": (0.1, 10)})
# graviton axis perpendicular to K: cos Th_cm = sin(th*) cos(phi)
st2 = 1 - ct**2
Rg = sp.integrate(1 + st2 * sp.cos(phi)**2, (phi, 0, 2 * sp.pi))
Rs = sp.integrate(1 - st2 * sp.cos(phi)**2, (phi, 0, 2 * sp.pi))
Jg = 2 * sp.pi * sp.integrate(Rg**2, (ct, -1, 1))
Js = 2 * sp.pi * sp.integrate(Rs**2, (ct, -1, 1))
ratio = sp.simplify(Js / (2 * Jg))
print("scalar/photon =", ratio)
identity(ratio, sp.Rational(7, 54))
identity(sp.Rational(4, 25) * ratio, sp.Rational(14, 675))
identity(3 / (25 * sp.pi) * ratio, 7 / (450 * sp.pi))
identity(1 / ratio, sp.Rational(54, 7))   # tau_phi/tau, tau defined from the corresponding photon/scalar rate
# limit check: if the ring average were isotropic-independent (ct -> poles) the two ring factors coincide (sin th* = 0)
limit(Rs / Rg, "ct", 1, 1)
raise SystemExit(finish())
