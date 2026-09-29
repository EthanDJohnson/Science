"""M-EXAMINER-01: redshift over 1 mm near Earth's surface: potential (first-order) vs tidal (second-order) term.

Claim (finding 5, premise 9): with g = GM/R^2 = 9.82 m/s^2, R = 6.371e6 m, dh = 1 mm (SI),
  first-order fractional rate difference g dh / c^2 = 1.093e-19 (dimensionless),
  second-order (tidal/curvature) term (1/2)(2GM/R^3) dh^2 / c^2 = 1.715e-29, ratio 1.57e-10 (= dh/R).
Also: time dilation exists without curvature (Rindler metric is flat, yet rates differ by 1 + g dh / c^2).

Independent derivation: weak-field static clocks, dtau/dt = sqrt(1 + 2 Phi/c^2) ~ 1 + Phi/c^2,
Phi(r) = -GM/r. Expand Phi(R + h) - Phi(R) in h.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, units, limit, finish
from gr_tensors import Spacetime

GM, R, h, c = sp.symbols("GM R h c", positive=True)
Phi = lambda r: -GM / r
dPhi = Phi(R + h) - Phi(R)
# Taylor: GM h/R^2 - GM h^2/R^3 + ...
series(dPhi, "h", 0, 3, GM * h / R**2 - GM * h**2 / R**3)
# ratio of second-order to first-order magnitude = h/R  (g h^2/R divided by g h)
identity((GM * h**2 / R**3) / (GM * h / R**2), h / R)
# tidal form used by lens: (1/2)(2GM/R^3) h^2 equals g h^2 / R with g = GM/R^2
identity(sp.Rational(1, 2) * (2 * GM / R**3) * h**2, (GM / R**2) * h**2 / R)
# flat-space limit: first-order term vanishes as GM -> 0
limit(GM * h / (R**2 * c**2), "GM", 0, 0)

# Numbers (SI), lens inputs
quantity("9.82 m/s^2 * 1 mm / c^2", "1.093e-19", rel_tol=1e-3)
quantity("9.82 m/s^2 * (1 mm)^2 / (6.371e6 m * c^2)", "1.715e-29", rel_tol=1e-3)
quantity("(1 mm) / (6.371e6 m)", "1.57e-10", rel_tol=3e-3)
quantity("(6.371e6 m) / (1 mm)", "6.4e9", rel_tol=1e-2)  # "dominates by 6e9"
# independent g from constants: G Mearth / (6.371e6 m)^2
quantity("G * Mearth / (6.371e6 m)^2", "9.82 m/s^2", rel_tol=2e-3)
units("9.82 m/s^2 * 1 mm / c^2", "dimensionless")

# Rindler: ds^2 = -(1 + a x)^2 dt^2 + dx^2 + dy^2 + dz^2 (geometric units), a = proper acceleration.
t, x, y, z, a = sp.symbols("t x y z a", positive=True)
g = sp.diag(-(1 + a * x)**2, 1, 1, 1)
st = Spacetime(g, [t, x, y, z])
Rm = st.riemann()
nonzero = [sp.simplify(Rm[i][j][k][l]) for i in range(4) for j in range(4) for k in range(4) for l in range(4)]
nonzero = [v for v in nonzero if v != 0]
print("Rindler nonzero Riemann components:", nonzero)
identity(sp.Integer(len(nonzero)), 0)
# rate ratio of static clocks at x = dh and x = 0: sqrt(-g_00) ratio = 1 + a dh (exact in Rindler)
dh = sp.symbols("dh", positive=True)
identity(sp.sqrt(-g[0, 0]).subs(x, dh) / sp.sqrt(-g[0, 0]).subs(x, 0), 1 + a * dh)

raise SystemExit(finish())
