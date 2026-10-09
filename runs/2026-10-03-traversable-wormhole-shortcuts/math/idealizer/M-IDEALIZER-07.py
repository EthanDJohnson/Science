"""M-IDEALIZER-07: does the Ellis tidal bound b0 >= gamma v sqrt(xi/a_max) reproduce MM's 1.5e7 m in the
ultra-relativistic limit?

Claim (F6): "Ultra-relativistic travel reproduces MM's 1.5e7 m (0.5 m, 20 g) and gives 1.35e8 m for 2 m at 1 g".
Independent check: the bound (verified in M-IDEALIZER-06) scales as gamma v; evaluate it as v -> c, and
compute the boosted transverse and longitudinal tides of MM's throat geometry (AdS2 x S2, equal radii r_e,
the near-horizon region of an extremal magnetically charged RN black hole) to see where 1.5e7 m comes from.
SI for numbers; c = 1 in the symbolic geometry.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime
from math_checks import identity, limit, sign, quantity, finish

c = 299792458.0
g0 = 9.80665
xi, amax = 0.5, 20 * g0
def bmin_of(beta, xi=xi, amax=amax):
    return beta / math.sqrt(1 - beta**2) * c * math.sqrt(xi / amax)
print("c sqrt(xi/a) =", c * math.sqrt(xi / amax), "m")
for beta in [0.5, 1 / math.sqrt(2), 0.99, 0.999999]:
    print(f"  v = {beta:.6f} c: Ellis b0_min = {bmin_of(beta):.4g} m")
# 1.5e7 m is the bound at gamma v = c, i.e. v = c/sqrt(2), not an ultra-relativistic limit
quantity(f"{bmin_of(1/math.sqrt(2))} m", "1.5e7 m", rel_tol=0.02)
quantity(f"{bmin_of(1/math.sqrt(2), 2.0, g0)} m", "1.35e8 m", rel_tol=0.01)
print("Ellis bound at MM's crossing gamma = 2e12:", 2e12 * c * math.sqrt(xi / amax), "m")
quantity(f"{2e12 * c * math.sqrt(xi / amax)} m", "3.0e19 m", rel_tol=0.02)
v = sp.symbols("v", positive=True)
bnd = v / sp.sqrt(1 - v**2)    # gamma v / c
sign(sp.diff(bnd, v), "positive", domain={"v": (0.01, 0.999)})   # monotone increasing
limit(bnd, "v", 1, sp.oo, direction="-", domain={"v": (0.01, 0.999)})

# MM-type throat: AdS2 x S2, equal radii
tau, x, th, ph = sp.symbols("tau x theta phi", real=True)
re = sp.symbols("r_e", positive=True)
ads = Spacetime(sp.diag(-re**2 * sp.cosh(x)**2, re**2, re**2, re**2 * sp.sin(th)**2), [tau, x, th, ph])
Ra = ads.riemann()
Rtt, Rxx = sp.simplify(Ra[2][0][2][0]), sp.simplify(Ra[2][1][2][1])
Rlong = sp.simplify(Ra[1][0][1][0] / (-ads.g[0, 0]))   # orthonormal R^x_{0 x 0}
print("AdS2xS2: R^th_tau th tau =", Rtt, "; R^th_x th x =", Rxx, "; orthonormal R^x_0x0 =", Rlong)
identity(Rtt, 0)          # no transverse tide for any boost (product metric)
identity(Rxx, 0)
identity(Rlong, 1 / re**2)   # longitudinal tide magnitude xi/r_e^2 (c^2 xi / r_e^2 in SI), boost-invariant in 2D
# hence MM-type bound r_e >= c sqrt(xi/a_max) independent of the crossing speed:
quantity(f"{c * math.sqrt(xi / amax)} m", "1.5e7 m", rel_tol=0.02)
raise SystemExit(finish())
