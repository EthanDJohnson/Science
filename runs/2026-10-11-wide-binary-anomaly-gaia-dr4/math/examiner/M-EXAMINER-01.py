"""M-EXAMINER-01/02 helper + check: MOND boost at g_N = 1e-10 m/s^2 (SI), independent re-derivation.

Definitions (QUMOND, interpolating family from mu_n(x) = x / (1 + x^n)^(1/n)):
  y = g_N/a0, x = g/a0, x mu_n(x) = y  ->  nu_n(y) = x/y.
  K(y) = dln nu / dln y.
  Newtonian-equivalent external field y_e solves y_e nu(y_e) = x_e  <=>  y_e = x_e mu(x_e).
  One-body Chae-2024-eq-22 form (as the lens states it): gamma = nu(y_b)[1 + tanh(beta y_e/y)^p K(y_b)/3],
  y_b = sqrt(y^2 + (beta y_e)^2).
Presets as the lens's finding names them: chae2024 (n=1, beta=1.1, p=1.2, x_e=1.90), bz18 simple/standard
(n=1/2, beta=1, p=1.2, g_ext = (232.8 km/s)^2/8.2 kpc), isolated (x_e = 0). a0 = 1.2e-10 m/s^2.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, limit, quantity, units, finish

y, x, n = sp.symbols("y x n", positive=True)

# nu_n by inverting x mu_n(x) = y : x^2/(1+x^n)^(1/n) = y. Solve for n = 1 and n = 2 symbolically.
nu = {}
for nn in (1, 2):
    sols = sp.solve(sp.Eq(x**2 / (1 + x**nn)**sp.Rational(1, nn), y), x)
    pos = [s for s in sols if s.is_positive is not False]
    # pick the positive real root
    root = [s for s in pos if sp.N(s.subs(y, 0.7)).is_real and sp.N(s.subs(y, 0.7)) > 0][0]
    nu[nn] = sp.simplify(root / y)
    print(f"n={nn}: nu(y) = {nu[nn]}")

closed = lambda nn: ((1 + sp.sqrt(1 + 4 * y**(-nn))) / 2)**sp.Rational(1, nn)
for nn in (1, 2):
    identity(nu[nn], closed(nn))

K = {nn: sp.simplify(sp.diff(sp.log(nu[nn]), y) * y) for nn in (1, 2)}
for nn in (1, 2):
    w = sp.sqrt(1 + 4 * y**(-nn))
    identity(K[nn], -2 * y**(-nn) / (w * (1 + w)))
# limits: K -> -1/2 deep MOND, -> 0 Newtonian; nu -> 1 Newtonian
limit(K[1], "y", 0, "-1/2")
limit(K[1], "y", "oo", "0")
limit(nu[1], "y", "oo", "1")
limit(nu[2] * sp.sqrt(y), "y", 0, "1")   # deep MOND nu ~ y^-1/2 -> g = sqrt(a0 gN)

mp.mp.dps = 30
a0 = mp.mpf("1.2e-10")
kpc = mp.mpf("3.0856775814913673e19")
gext_bz = (mp.mpf("232.8e3"))**2 / (mp.mpf("8.2") * kpc)
print("g_ext BZ18 =", mp.nstr(gext_bz, 6), "m/s^2 =", mp.nstr(gext_bz / a0, 6), "a0")

def num(expr, yy):
    return mp.mpf(str(sp.N(expr.subs(y, sp.Float(str(yy), 40)), 30)))

def ye_from_xe(xe, nn):
    return xe**2 / (1 + xe**nn)**(mp.mpf(1) / nn)

def gamma(gN, nn, beta, p, xe):
    yy = gN / a0
    if xe == 0:
        return num(nu[nn], yy)
    ye = ye_from_xe(xe, nn)
    # check y_e nu(y_e) = x_e
    assert abs(ye * num(nu[nn], ye) - xe) < mp.mpf("1e-20")
    yb = mp.sqrt(yy**2 + (beta * ye)**2)
    t = mp.tanh(beta * ye / yy)**p
    return num(nu[nn], yb) * (1 + t * num(K[nn], yb) / 3)

gN = mp.mpf("1e-10")
res = {
    "chae2024": gamma(gN, 1, mp.mpf("1.1"), mp.mpf("1.2"), mp.mpf("1.90")),
    "bz18_simple": gamma(gN, 1, 1, mp.mpf("1.2"), gext_bz / a0),
    "bz18_standard": gamma(gN, 2, 1, mp.mpf("1.2"), gext_bz / a0),
    "isolated": gamma(gN, 1, 1, mp.mpf("1.2"), 0),
}
lens = {"chae2024": 1.333, "bz18_simple": 1.375, "bz18_standard": 1.061, "isolated": 1.704}
for k, v in res.items():
    print(f"gamma({k}) at 1e-10 m/s^2 = {mp.nstr(v, 6)}  (lens {lens[k]})")
    identity(sp.Float(round(float(v), 3)), sp.Float(lens[k]))

# isolated simple by hand: y = 1/1.2, nu = 1/2 + sqrt(1/4 + 1.2)
identity(sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + sp.Rational(6, 5)), nu[1].subs(y, sp.Rational(5, 6)))

# Newtonian limit of the full one-body form, chae2024 preset, g_N = 1e-6 m/s^2
gnewt = gamma(mp.mpf("1e-6"), 1, mp.mpf("1.1"), mp.mpf("1.2"), mp.mpf("1.90"))
print("chae2024 gamma at 1e-6 m/s^2 =", mp.nstr(gnewt, 8))
identity(sp.Float(round(float(gnewt), 3)), 1)
# deep plateau chae2024 at 1e-12 -> ~1.37 (Chae's stated deep G_eff)
print("chae2024 gamma at 1e-12 =", mp.nstr(gamma(mp.mpf("1e-12"), 1, mp.mpf("1.1"), mp.mpf("1.2"), mp.mpf("1.90")), 6))

# spread of (gamma - 1) among the EFE templates (finding 1: "factor ~1.3 in (gamma - 1)")
r = (res["bz18_simple"] - 1) / (res["chae2024"] - 1)
print("(gamma-1) ratio bz18_simple/chae2024 =", mp.nstr(r, 5),
      "; bz18_simple/standard =", mp.nstr((res["bz18_simple"] - 1) / (res["bz18_standard"] - 1), 5))

units("1.2e-10 m/s^2", "acceleration")
quantity("(232.8 km/s)^2 / (8.2 kpc)", "2.142e-10 m/s^2", rel_tol=1e-3)
raise SystemExit(finish())
