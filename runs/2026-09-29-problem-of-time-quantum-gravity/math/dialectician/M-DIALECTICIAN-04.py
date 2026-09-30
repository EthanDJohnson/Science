"""M-DIALECTICIAN-04: GPP exponent (3/2) t_P^(4/3) T^(2/3) w^2 equals sigma^2 w^2/2 with sigma = sqrt(3) dT, dT = t_P (T/t_P)^(1/3).

Symbols: t_P Planck time (s, > 0), T elapsed time (s, > 0), w = omega_12 Bohr angular frequency (rad/s, > 0).
Numbers (SI): w = 2 pi x 429 THz; dT(1 s) = 1.427e-29 s; exponent 2.219e-27 at T = 1 s, 1.275e-15 at T = 13.8 Gyr.
The GPP exponent and dT formula are quoted from the literature ([Q-15], [Q-14]); only the algebra/arithmetic is checked.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, units, finish, Result, _done

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric (float, SI)", note=note), True)

tP, T, w = sp.symbols("t_P T omega", positive=True)
dT = tP * (T / tP) ** sp.Rational(1, 3)
sigma = sp.sqrt(3) * dT
identity(sigma**2 * w**2 / 2, sp.Rational(3, 2) * tP ** sp.Rational(4, 3) * T ** sp.Rational(2, 3) * w**2,
         domain={"t_P": (0.1, 10), "T": (0.1, 1000), "omega": (0.1, 10)})
identity(dT, tP ** sp.Rational(2, 3) * T ** sp.Rational(1, 3))
limit(dT / T, "T", sp.oo, "0")        # relative clock error shrinks for long runs
# dimensions: t_P^(2/3) T^(1/3) is a time; exponent dimensionless
units("(5.391e-44 s)^(2/3) * (1 s)^(1/3)", "s")
units("(5.391e-44 s)^(4/3) * (1 s)^(2/3) * (1 rad/s)^2", "dimensionless")

# numbers from CODATA constants, computed independently
hbar, G, c = 1.054571817e-34, 6.67430e-11, 299792458.0
tp = math.sqrt(hbar * G / c**5)
om = 2 * math.pi * 429e12
yr = 365.25 * 86400
def dTf(T):
    return tp ** (2 / 3) * T ** (1 / 3)
def expo(T):
    return 1.5 * tp ** (4 / 3) * T ** (2 / 3) * om**2
print(f"t_P = {tp:.6e} s; dT(1 s) = {dTf(1):.4e} s; exp(1 s) = {expo(1):.4e}; exp(13.8 Gyr) = {expo(13.8e9*yr):.4e}")
report("dT(1 s) = 1.427e-29 s", abs(dTf(1) / 1.427e-29 - 1) < 1e-3, f"{dTf(1):.4e} s")
report("exponent(1 s) = 2.219e-27", abs(expo(1) / 2.219e-27 - 1) < 1e-3, f"{expo(1):.4e}")
report("exponent(13.8 Gyr) = 1.275e-15", abs(expo(13.8e9 * yr) / 1.275e-15 - 1) < 2e-3, f"{expo(13.8e9*yr):.4e}")
report("route 2: (sqrt3 dT)^2 w^2/2 at 1 s equals route 1", abs((math.sqrt(3) * dTf(1)) ** 2 * om**2 / 2 / expo(1) - 1) < 1e-12)
quantity("(hbar * G / c^5)^(1/2)", "5.391e-44 s", rel_tol=1e-3)
raise SystemExit(finish())
