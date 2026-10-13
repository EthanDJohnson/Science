"""M-MECHANIST-04: pairs made by an outgoing spherical GW shell beyond radius r (SI).

Own bookkeeping: shell energy E, thickness L = c/sigma_w, graviton density n(r) = E/(hbar w 4 pi r^2 L),
split into two half-density beams crossing at the local direction spread th(r). Rate per volume (M-MECHANIST-03)
Gamma = (n/2)^2 sigma_lin c (1 - cos th), sigma_lin = (2/5) pi lP^4 s, s = 2 (w/c)^2 (1 - cos th) (m^-2),
lP^2 = hbar G/c^3. Shell volume 4 pi r^2 L, time at radius r: dr/c. So dN/dr = Gamma 4 pi r^2 L / c.
Claims: dN/dr ~ r^-4 (th = (kr)^-1/2) or r^-6 (th = (kr)^-1); beyond r ~ r^-3 / r^-5; N(>1/k) = 6.8e-8 / 4.2e-8
(order of magnitude, O(1) bookkeeping); convergence 'for any spread falling faster than r^-1/2'.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, inequality, quantity, finish

# Scaling, symbolic: th = (k r)^(-a), small-angle (1 - cos th)^2 -> th^4/4
r, k, a = sp.symbols("r k a", positive=True)
dNdr = r**-2 * (k * r) ** (-4 * a)                     # n^2 ~ r^-4 times volume ~ r^2, times th^4
for aa, p in ((sp.Rational(1, 2), -4), (1, -6)):
    identity(sp.simplify(sp.diff(sp.log(dNdr.subs(a, aa)), r) * r), p)
    tail = sp.integrate(dNdr.subs(a, aa), (r, r, sp.oo))
    identity(sp.simplify(sp.diff(sp.log(tail), r) * r), p + 1)
# Sharp convergence condition: exponent -2 - 4a < -1  <=>  a > -1/4 (any non-growing spread converges)
inequality("2 + 4*a", ">", "1", domain={"a": (-0.2499, 5)})
tail0 = sp.integrate(r**-2, (r, r, sp.oo))
identity(tail0, 1 / r)                                  # constant spread: still convergent, ~ 1/r

# Numbers (SI)
c = 299792458.0; G = 6.67430e-11; hbar = 1.054571817e-34; Msun = 1.3271244e20 / G
E = 2 * Msun * c**2; w = 2 * math.pi * 150.0; sig = 200.0; L = c / sig; kk = w / c; lP4 = (hbar * G / c**3) ** 2


def dN(rr, model):
    th = (kk * rr) ** (-0.5) if model == "fresnel" else (kk * rr) ** (-1.0)
    th = min(th, math.pi)
    n = E / (hbar * w * 4 * math.pi * rr**2 * L)
    one = 1 - math.cos(th)
    s_ = 2 * (w / c) ** 2 * one
    Gam = (n / 2) ** 2 * 0.4 * math.pi * lP4 * s_ * c * one
    return Gam * 4 * math.pi * rr**2 * L / c


def tail(r0, model, decades=12, steps=4000):
    tot = 0.0; x0 = math.log(r0); dx = decades * math.log(10) / steps
    for i in range(steps):
        x = x0 + (i + 0.5) * dx; rr = math.exp(x); tot += dN(rr, model) * rr * dx
    return tot


AU = 1.495978707e11
for model, want in (("fresnel", "6.8e-8"), ("gradient", "4.2e-8")):
    N1 = tail(1 / kk, model); N10 = tail(10 / kk, model); NAU = tail(AU, model)
    print(f"{model}: N(>1/k) = {N1:.3e}, N(>10/k) = {N10:.3e}, N(>1 AU) = {NAU:.3e} pairs")
    quantity(f"{N1:.4e}", want, rel_tol=1.0)   # same order (factor < 2)
raise SystemExit(finish())
