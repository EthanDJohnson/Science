"""M-EXAMINER-02: EF-dominated simple-nu anisotropy (dimensionless boosts).
Quoted law (BZ18 via dossier D-02, not re-derived from field equations): g_r/g_N,r = nu_e (1 + K0 sin^2(th)/2).
Derived here: nu_e, K0 from the true field x_e = g_ext/a0 = 1.785 (simple mu(x) = x/(1+x)),
the parallel (th = 0), perpendicular (th = pi/2) and isotropic-sphere-average values.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, finish

xe, th, K0, nue = sp.symbols("x_e theta K_0 nu_e", positive=True)
# simple: Newtonian-equivalent field y_e = x_e mu(x_e) = x_e^2/(1+x_e); nu_e = x_e/y_e = (1+x_e)/x_e
ye = xe**2 / (1 + xe)
nu_e = sp.simplify(xe / ye)
yy = sp.symbols("y", positive=True)
nu_y = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / yy)
identity(nu_y.subs(yy, ye), nu_e, domain={"x_e": (0.1, 10)})     # consistency nu(y_e) = x_e/y_e
K_y = sp.diff(sp.log(nu_y), yy) * yy
K0v = sp.simplify(K_y.subs(yy, ye))
print("K0(x_e) =", K0v)
# sphere average of sin^2 theta is 2/3 -> eta = nu_e (1 + K0/3)
avg = sp.integrate(sp.sin(th)**2 * sp.sin(th), (th, 0, sp.pi)) / 2
identity(avg, sp.Rational(2, 3))
law = nue * (1 + K0 * sp.sin(th)**2 / 2)
identity(sp.integrate(law * sp.sin(th), (th, 0, sp.pi)) / 2, nue * (1 + K0 / 3))
sign(K0v, "negative", domain={"x_e": (0.01, 100)})   # boost largest along the EF
limit(K0v, "x_e", 0, "-1/2")                           # deep-MOND EF -> K0 = -1/2
limit(K0v, "x_e", "oo", "0")                           # Newtonian EF -> no anisotropy

x0 = sp.Rational(1785, 1000)
vals = dict(nu=nu_e.subs(xe, x0), K0=K0v.subs(xe, x0))
vals["eta"] = vals["nu"] * (1 + vals["K0"] / 3)
vals["perp"] = vals["nu"] * (1 + vals["K0"] / 2)
for k, v in vals.items():
    print(k, sp.N(v, 8))
lens = dict(nu=1.5602, K0=-0.2642, eta=1.4228, perp=1.3541)
for k in lens:
    identity(sp.Float(round(float(sp.N(vals[k])), 4)), sp.Float(lens[k]))
# anisotropy (par - perp)/eta, finding 1 / D-02 "about 15%"
print("anisotropy (par-perp)/eta =", sp.N((vals["nu"] - vals["perp"]) / vals["eta"], 5))
raise SystemExit(finish())
