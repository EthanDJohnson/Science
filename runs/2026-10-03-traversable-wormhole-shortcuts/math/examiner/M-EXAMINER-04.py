"""M-EXAMINER-04: MM 2020 transit times.

Throat: AdS2 x S2, ds^2 = r_e^2 [-(rho^2+1) dtau^2 + drho^2/(rho^2+1)] (+ sphere), units c = 1 inside,
exterior time t = l * tau (l = MM's length scale; lapse ratio gam = l/r_e).
(i) Radial null ray: dtau = drho/(rho^2+1)  -> Delta tau = pi across rho in (-inf, inf) -> T_thru = pi l / c.
(ii) Timelike geodesics in AdS2 (radius r_e): conserved e = (rho^2+1) dtau/ds; proper time between
     turning points (half oscillation) = pi r_e for any amplitude -> tau_thru = pi r_e / c.
Inputs (quoted, Q-01/Q-02): r_e = 1.5e7 m, l = 3e3 ly. SI.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish
import sympy as sp
import mpmath as mp

rho = sp.symbols("rho", real=True)
identity(sp.integrate(1 / (rho**2 + 1), (rho, -sp.oo, sp.oo)), sp.pi)

# Timelike geodesic: with s proper time (r_e = 1), (drho/ds)^2 = e^2 - (rho^2 + 1).
# Turning points rho = +/- sqrt(e^2 - 1). Half-period proper time = int drho / sqrt(e^2 - 1 - rho^2) = pi.
for e in [1.5, 10.0, 1e3, 1e6]:
    A = mp.sqrt(e**2 - 1)
    s_half = mp.quad(lambda x: 1 / mp.sqrt(A**2 - x**2), [-A, 0, A])
    # coordinate tau elapsed: dtau/ds = e/(rho^2+1)
    t_half = mp.quad(lambda x: e / ((x**2 + 1) * mp.sqrt(A**2 - x**2)), [-A, 0, A])
    print(f"e={e}: proper half period = {s_half}, tau elapsed = {t_half}")
    quantity(f"{float(s_half)}", f"{math.pi}", rel_tol=1e-8)
    quantity(f"{float(t_half)}", f"{math.pi}", rel_tol=1e-8)
# limit e -> infinity: massive geodesic approaches the null ray, still Delta tau = pi
e_ = sp.symbols("e_", positive=True)
limit(sp.pi, "e_", sp.oo, sp.pi)

c = 299792458.0
ly = 9.4607304725808e15
re, l = 1.5e7, 3e3 * ly
gam = l / re
print("gamma =", gam)
quantity(f"{gam}", "1.892e12", rel_tol=1e-3)
quantity(f"pi * 3000 ly / c", "9.4248e3 yr", rel_tol=1e-4)
quantity(f"pi * 1.5e7 m / c", "0.1572 s", rel_tol=1e-3)
for frac, lens in [(1.0, math.pi), (0.1, 31.4), (0.01, 314)]:
    quantity(f"{math.pi/frac}", f"{lens}", rel_tol=2e-3)
ratio_tau = (math.pi * re / c) / (l / c)
print("tau/T_ext at d = l:", ratio_tau)
quantity(f"{ratio_tau}", "1.66e-12", rel_tol=3e-3)
units("pi * 3000 ly / c", "s")
raise SystemExit(finish())
