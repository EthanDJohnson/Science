"""M-MECHANIST-04: gravitational conversion (finding 8).
Independent derivation: Schwarzschild metric ds^2 = -(1-2m/r)dt^2 + ... (G=c=1, m = GM/c^2).
Circular geodesic: Omega^2 = m/r^3 (Kepler, exact in Schwarzschild coordinates), so
dtau/dt = sqrt(1 - 2m/r - r^2 Omega^2) = sqrt(1 - 3m/r). Lag rate vs a clock at infinity: 1 - sqrt(1 - 3 phi).
Static clock: dtau/dt = sqrt(1 - 2 phi).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, finish

m, r = sp.symbols("m r", positive=True)
Om2 = m / r**3   # circular geodesic angular velocity squared, derived below from the effective potential
# derive Omega^2 from geodesic equation: for equatorial circular orbits d/dr[(1-2m/r)] tdot^2 = d/dr[r^2] phidot^2
f = 1 - 2 * m / r
Om2_derived = sp.simplify(sp.diff(f, r) / sp.diff(r**2, r))
identity(Om2_derived, Om2)
rate = sp.sqrt(f - r**2 * Om2_derived)
phi = sp.symbols("phi", positive=True)
identity(rate**2, (1 - 3 * phi).subs(phi, m / r), domain={"m": (0.1, 1), "r": (3.5, 100)})
# weak-field limit: lag ~ 1.5 phi
series(1 - sp.sqrt(1 - 3 * phi), "phi", 0, 2, "3*phi/2")

lag_orb = lambda p: 1 - math.sqrt(1 - 3 * p)
lag_st = lambda p: 1 - math.sqrt(1 - 2 * p)
# ISCO r = 6m: phi = 1/6
quantity(f"{lag_orb(1/6)}", "0.293", rel_tol=0.002)
# Sgr A*: M = 4.3e6 Msun (lens input), r = 0.01 pc
import importlib
U = importlib.import_module("unit_tools")
phi_sgr = U.Q("G * 4.3e6 Msun / (c^2 * 0.01 pc)").si
if phi_sgr is None:
    phi_sgr = float(U.Q("G * 4.3e6 Msun / (c^2 * 0.01 pc)").to(""))
quantity(f"{lag_orb(phi_sgr)}", "3.1e-5", rel_tol=0.01)
# Earth's surface, static
phi_E = U.Q("G * Mearth / (c^2 * Rearth)").si
quantity(f"{lag_st(phi_E)}", "7.0e-10", rel_tol=0.01)
# conversion times
quantity(f"(8 kpc / c) / {lag_orb(phi_sgr)}", "8.5e8 yr", rel_tol=0.01)
quantity("8 kpc / c", "2.6e4 yr", rel_tol=0.01)
quantity(f"(1 au / c) / {lag_st(phi_E)}", "2.3e4 yr", rel_tol=0.02)
Tw = math.pi * 3000
quantity(f"{Tw - 1e3} yr / {lag_orb(1/6)}", "2.9e4 yr", rel_tol=0.02)
quantity(f"{Tw + 1e3} yr / {lag_orb(1/6)}", "3.6e4 yr", rel_tol=0.02)
# flat rotation curve: Phi = v^2 ln r, so Delta phi between 1 and 8 kpc = (v/c)^2 ln 8; equal speeds cancel SR dilation
dphi = (220e3 / 299792458.0)**2 * math.log(8)
quantity(f"{dphi}", "1.1e-6", rel_tol=0.03)
# time to D/c: separation between mouths at 1 and 8 kpc lies between 7 and 9 kpc
quantity(f"(7 kpc / c) / {dphi}", "2.0e10 yr", rel_tol=0.03)
print(f"INFO separation range: 7 kpc -> {float(U.Q(f'(7 kpc / c) / {dphi}').to('yr')):.3g} yr, "
      f"8 kpc -> {float(U.Q(f'(8 kpc / c) / {dphi}').to('yr')):.3g} yr, 9 kpc -> {float(U.Q(f'(9 kpc / c) / {dphi}').to('yr')):.3g} yr")
raise SystemExit(finish())
