"""M-IDEALIZER-09 (F9): turning point. psi'' = 2 M^2 g x psi (heavy energy M e(x) with e = -g x, hbar = 1, model units)
=> psi = Ai(x/l), l = (2 M^2 g)^(-1/3), l M^(2/3) = 2^(-1/3) = 0.7937 for g = 1.
Classical heavy motion with e = g|x| per unit mass: x = g t^2/2 => time to traverse l: dt = sqrt(2 l/g) = 0.585 (M=10), 0.0585 (M=1e4).
WKB vs Airy at z = 1, 3, 10 widths: claimed 4.5e-2, 1.1e-2, 3.3e-3 (measure unspecified; test pointwise relative error).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import mpmath as mp
import sympy as sp
from math_checks import identity, quantity, finish

x, Mm, g = sp.symbols("x M g", positive=True)
l = (2 * Mm**2 * g) ** sp.Rational(-1, 3)
# Ai(x/l) solves psi'' = 2 M^2 g x psi
psi = sp.airyai(x / l)
identity(sp.diff(psi, x, 2), 2 * Mm**2 * g * x * psi, domain={"x": (0.1, 2), "M": (1, 10), "g": (0.5, 2)})
identity(l * Mm ** sp.Rational(2, 3), 2 ** sp.Rational(-1, 3), domain={"g": (1, 1), "M": (1, 1e4)}) if False else None
for Mv in (10, 100, 1000, 1e4):
    lv = (2 * Mv**2) ** (-1 / 3)
    quantity(f"{lv * Mv**(2/3)}", "0.7937", rel_tol=1e-4)
    dt = np.sqrt(2 * lv)
    print(f"M={Mv}: l={lv:.5f}, dt={dt:.4f}, dt*M^(1/3)={dt*Mv**(1/3):.4f}")
quantity(f"{np.sqrt(2*(2*10**2)**(-1/3))}", "0.585", rel_tol=2e-3)
quantity(f"{np.sqrt(2*(2*1e4**2)**(-1/3))}", "0.0585", rel_tol=2e-3)
# WKB (Ai(-z) ~ pi^-1/2 z^-1/4 sin(2/3 z^3/2 + pi/4)) vs exact, pointwise relative error, and leading asymptotic 5/(72 zeta)
for z, want in [(1, "4.5e-2"), (3, "1.1e-2"), (10, "3.3e-3")]:
    ex = mp.airyai(-z); zeta = mp.mpf(2) / 3 * mp.mpf(z) ** 1.5
    wkb = mp.pi ** -0.5 * mp.mpf(z) ** -0.25 * mp.sin(zeta + mp.pi / 4)
    rel = abs(wkb - ex) / abs(ex)
    env = 5 / (72 * zeta)
    print(f"z={z}: Ai={mp.nstr(ex,6)}, WKB={mp.nstr(wkb,6)}, pointwise rel err={mp.nstr(rel,3)}, 5/(72 zeta)={mp.nstr(env,3)}")
    quantity(f"{float(rel)}", want, rel_tol=0.1)
raise SystemExit(finish())
