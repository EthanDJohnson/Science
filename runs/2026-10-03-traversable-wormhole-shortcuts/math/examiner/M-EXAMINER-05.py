"""M-EXAMINER-05: MM proper radial length between static observers at r = 2 r_e on both sides.

Exterior: extremal RN, g_rr = 1/(1 - r_e/r)^2, g_tt = -(1 - r_e/r)^2. Near horizon, x = r - r_e << r_e:
  ds^2 ~ -(x/r_e)^2 dt^2 + r_e^2 dx^2 / x^2.
Throat: ds^2 = r_e^2[-(rho^2+1) dtau^2 + drho^2/(rho^2+1)].  Large rho: -r_e^2 rho^2 dtau^2 + r_e^2 drho^2/rho^2.
Matching with t = l tau requires x/r_e * l = r_e rho  ->  x = r_e^2 rho / l = r_e rho / gam.
Proper length L = 2 [ r_e asinh(rho_c) + int_{x_c}^{r_e} (x + r_e)/x dx ],  x_c = r_e rho_c / gam.
Lens claim: L = 2 r_e [ln(2 gam) + 1] for 1 << rho_c << gam; = 8.99e8 m for r_e = 1.5e7 m, gam = 1.892e12.
SI.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish
import sympy as sp
import mpmath as mp

x, re, rc, t, l = sp.symbols("x r_e rho_c t l", positive=True)
g = sp.symbols("g", positive=True)   # gam = l / r_e
# metric matching: exterior lapse x/r_e times dt = l dtau equals throat lapse r_e*rho dtau
rho = sp.symbols("rho", positive=True)
identity((re * rho / g) / re * (g * re), re * rho)   # (x/r_e)*l with x = r_e rho/g, l = g r_e
# radial parts: r_e dx/x with x = r_e rho / g  ==  r_e drho/rho
identity(re * sp.diff(re * rho / g, rho) / (re * rho / g), re / rho)

# exact exterior integral of dr/(1 - r_e/r) from r_e + x_c to 2 r_e
ext = sp.integrate((x + re) / x, (x, re * rc / g, re))
total = 2 * (re * sp.asinh(rc) + ext)
target = 2 * re * (sp.log(2 * g) + 1)
# in the overlap limit, total - target -> 0 relative: difference = 2r_e[asinh(rc) - ln(2 rc)] - 2 r_e^2 rc/g * (1/r_e)
diff = sp.simplify(total - target)
print("total - target =", diff)
# leading behaviour: rc -> oo with g = rc^3 (so rc/g -> 0): difference -> 0
limit(sp.simplify((total - target).subs(g, rc**3) / re), "rho_c", sp.oo, 0)

c = 299792458.0
ly = 9.4607304725808e15
Re, gam = 1.5e7, 3e3 * ly / 1.5e7
f = sp.lambdify((re, rc, g), total, "mpmath")
for rcv in [1e3, 1e6, 1e9]:
    Lv = f(Re, rcv, gam)
    print(f"rho_c={rcv:g}: L = {mp.nstr(Lv, 8)} m")
    quantity(f"{float(Lv)} m", "8.9886e8 m", rel_tol=1e-4)
closed = 2 * Re * (math.log(2 * gam) + 1)
print("closed form:", closed, "m =", closed / c, "light-s; l / L =", 3e3 * ly / closed)
quantity(f"{closed} m / c", "2.998 s", rel_tol=1e-3)
# Limit check: flat-ish exterior far from horizon: integrand (x+r_e)/x -> 1 as r_e -> 0 (Minkowski radial length)
limit((x + re) / x, "r_e", 0, 1)
units("8.9886e8 m / c", "s")
raise SystemExit(finish())
