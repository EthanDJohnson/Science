"""M-DIALECTICIAN-02: T_eff = 2 pi J_f / I_f^4 for top hat and Gaussian.

Definitions (stated, own reading): f(a) the normalised spectral amplitude, int |f|^2 da = 1;
C(K0) = int f(a) f(K0 - a) da; J_f = int |C|^2 dK0; I_f = int f(a) da (so I_f^4 = (int f)^4).
Top hat f = sigma^(-1/2) on a band of width sigma: claim T_eff = 4 pi/(3 sigma).
Gaussian amplitude f ~ exp(-(a-w)^2/(2 sigma^2)): claim T_eff = sqrt(pi/2)/sigma.
Consistency check: B&O total coefficient 4/25 over T_eff gives rate coefficient 3/(25 pi).
Physical check: J_f/(2 pi) = int |a(t)|^4 dt (Parseval), the local-collision picture.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from math_checks import identity, quantity, finish

s, x, y, a = sp.symbols("sigma x y a", positive=True)
xr, yr = sp.symbols("x_r y_r", real=True)
# top hat centred at 0 (centre irrelevant): f = s^-1/2 on [-s/2, s/2]
# C(y) = overlap length / s = (s - |y|)/s for |y| < s
Cth = (s - yr) / s
J_th = 2 * sp.integrate(Cth**2, (yr, 0, s))
I_th = s / sp.sqrt(s)
T_th = sp.simplify(2 * sp.pi * J_th / I_th**4)
print("top hat J_f =", J_th, " T_eff =", T_th)
identity(T_th, 4 * sp.pi / (3 * s))
# norm check
identity(sp.integrate((1 / sp.sqrt(s))**2, (xr, -s / 2, s / 2)), 1)

# Gaussian amplitude
fg = (sp.pi * s**2) ** sp.Rational(-1, 4) * sp.exp(-xr**2 / (2 * s**2))
identity(sp.integrate(fg**2, (xr, -sp.oo, sp.oo)), 1)
Cg = sp.simplify(sp.integrate(fg * fg.subs(xr, yr - xr), (xr, -sp.oo, sp.oo)))
J_g = sp.simplify(sp.integrate(Cg**2, (yr, -sp.oo, sp.oo)))
I_g = sp.integrate(fg, (xr, -sp.oo, sp.oo))
T_g = sp.simplify(2 * sp.pi * J_g / I_g**4)
print("Gaussian C =", Cg, " J_f =", J_g, " T_eff =", T_g)
identity(T_g, sp.sqrt(sp.pi / 2) / s)

# coefficient consistency: (4/25)/(4 pi/3) = 3/(25 pi)
identity(sp.Rational(4, 25) / (4 * sp.pi / 3), 3 / (25 * sp.pi))

# Parseval numeric check for top hat: J_f/(2 pi) = int |a(t)|^4 dt, a(t) = (2pi)^-1/2 int f e^{-i a t} da
sv = 1.0
t = np.linspace(-4000, 4000, 2_000_001)
at = np.sqrt(sv / (2 * np.pi)) * np.sinc(sv * t / (2 * np.pi))  # |a(t)| for top hat
num = np.trapezoid(np.abs(at) ** 4, t)
print(f"top hat int|a|^4 dt = {num:.6f}, J_f/(2pi) = {float(J_th.subs(s, sv))/(2*np.pi):.6f}")
quantity(f"{num}", f"{float(J_th.subs(s, sv)) / (2 * np.pi)}", rel_tol=1e-4)
raise SystemExit(finish())
