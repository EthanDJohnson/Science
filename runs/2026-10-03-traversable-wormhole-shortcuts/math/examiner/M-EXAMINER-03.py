"""M-EXAMINER-03: Schwarzschild thin-shell (Visser) transit.

Two Schwarzschild exteriors r >= a, mass M, glued at r = a (> 2M). Geometric M = G M/c^2.
Radial null ray: c dt = dr / (1 - 2M/r)  ->  c t(a -> r_obs) = (r_obs - a) + 2M ln[(r_obs - 2M)/(a - 2M)].
T_thru (infinity clocks) = 2 t(a -> r_obs); observer clocks: x sqrt(1 - 2M/r_obs).
Proper length L = 2 int_a^{r_obs} dr / sqrt(1 - 2M/r); payload tau = L sqrt(1-v^2)/v at local v.
Exterior: two mouths, centres D apart, observers on facing sides at r_obs; flat path length D - 2 r_obs
plus the weak-field radial Shapiro terms of both masses (each 2M ln[(D - r_obs - 2M)/(r_obs - 2M)]).
SI units.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish
import sympy as sp
import mpmath as mp

r, a, M = sp.symbols("r a M", positive=True)
ct = (r - a) + 2 * M * sp.log((r - 2 * M) / (a - 2 * M))
# derivative check: d(ct)/dr == 1/(1-2M/r)
identity(sp.diff(ct, r), 1 / (1 - 2 * M / r), domain={"r": (30, 100), "a": (3, 29), "M": (0.1, 1)})
# Limit M -> 0: flat space, ct -> r - a
limit(ct, "M", 0, "r - a", direction="+")

G, c, Msun = 6.67430e-11, 299792458.0, 1.98840987e30
Mg = G * Msun / c**2
A, R = 1.0e4, 1.0e5
T = 2 * ((R - A) + 2 * Mg * math.log((R - 2 * Mg) / (A - 2 * Mg))) / c
Tobs = T * math.sqrt(1 - 2 * Mg / R)
Lp = 2 * mp.quad(lambda x: 1 / mp.sqrt(1 - 2 * Mg / x), [A, R])
print("M_geom =", Mg, "m; T_thru(inf) =", T, "s; T_thru(obs) =", Tobs, "s; L =", Lp, "m")
quantity(f"{T} s", "6.5209e-4 s", rel_tol=2e-4)
quantity(f"{Tobs} s", "6.42e-4 s", rel_tol=2e-3)
quantity(f"{float(Lp)} m", "1.8749e5 m", rel_tol=2e-4)
tau = float(Lp) * math.sqrt(1 - 0.01) / (0.1 * c)
quantity(f"{tau} s", "6.22e-3 s", rel_tol=2e-3)
AU, ly = 1.495978707e11, 9.4607304725808e15
maxshap = 0
for D, lens in [(1e7, 1.989e-2), (AU, 1.307e-6), (ly, 2.066e-11)]:
    shap = 2 * (2 * Mg * math.log((D - R - 2 * Mg) / (R - 2 * Mg))) / c
    maxshap = max(maxshap, shap)
    Text = (D - 2 * R) / c + shap
    ratio = T / Text
    print(f"D={D:.4g} m Shapiro={shap:.3g} s T_ext={Text:.6g} s ratio={ratio:.4g} (lens {lens})")
    identity(f"{ratio:.4g}", f"{lens}")
print("max Shapiro delay over listed D:", maxshap, "s")
identity(str(int(maxshap <= 5e-4)), "1")
units("2*1476.6 m / c", "s")
raise SystemExit(finish())
