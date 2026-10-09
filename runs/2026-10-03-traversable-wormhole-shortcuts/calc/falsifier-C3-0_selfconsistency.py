"""Falsifier C3-0 (physics angle): can a self-consistent semiclassical
quantum-field ANEC violation hold open a SHORT (single-scale) throat whose
radial geodesic is achronal?

Units: geometric (G = c = 1, lengths in m) unless marked; l_P = sqrt(G hbar/c^3).

Step 1 (required, exact): for the Ellis-type throat r(l) = sqrt(l^2 + b0^2),
Phi = 0, the radial ANEC from the by-parts identity (M-CONSTRAINTS-02) is
   8*pi * Int T_kk dlambda = -2 E Int (r'/r)^2 dl = -pi E / b0.
We recompute Int (r'/r)^2 dl numerically and symbolically.

Step 2 (supply, scaling): N free/conformal quantum fields whose state has no
structure below the curvature radius R give |<T_kk>| <= alpha N hbar c / R^4
(SI energy density) for E = 1, i.e. 8 pi |G T_kk / c^4| <= 8 pi alpha N l_P^2 / R^4
(geometric), over an affine extent eta * R. Supply: 8 pi alpha eta N l_P^2 / R^3.

Self-consistency (G = 8 pi <T>) with R = b0 requires
   8 pi alpha eta N l_P^2 / R^3 >= pi / R   =>   R <= sqrt(8 alpha eta N) l_P.
Compare with the species length l_sp = sqrt(N) l_P, below which semiclassical
gravity with N species is not controlled (Dvali species bound).
"""
import math
import sympy as sp

lP = 1.616255e-35  # m (CODATA 2018)

# ---- Step 1: required ANEC, exact
l, b0 = sp.symbols('l b0', positive=True)
r = sp.sqrt(l**2 + b0**2)
integrand = sp.simplify((sp.diff(r, l) / r) ** 2)
I = sp.integrate(integrand, (l, -sp.oo, sp.oo))
print("Step 1: integrand (r'/r)^2 =", integrand)
print("Step 1: Int (r'/r)^2 dl =", sp.simplify(I), " (geometric, 1/m)")
req = sp.simplify(-2 * I)  # 8 pi * ANEC per unit E
print("Step 1: 8*pi*ANEC = ", req, "; ANEC =", sp.simplify(req / (8 * sp.pi)),
      " (geometric, per unit E; matches -E/(8 b0))")
# numeric cross-check at b0 = 1 m
import scipy.integrate as si
val, err = si.quad(lambda x: (x / (x**2 + 1)) ** 2, -math.inf, math.inf)
print(f"Step 1: numeric Int at b0=1 m: {val:.12f} vs pi/2 = {math.pi/2:.12f}")

# ---- Step 2: self-consistency bound
print("\nStep 2: R_max = sqrt(8 alpha eta N) l_P ; ratio R_max / l_sp = sqrt(8 alpha eta)")
alphas = {
    "1/(2880 pi^2) (curved-space anomaly/Page-type coefficient)": 1 / (2880 * math.pi**2),
    "1/(1440 pi^2)": 1 / (1440 * math.pi**2),
    "pi^2/1440 (scalar Casimir, plates)": math.pi**2 / 1440,
    "pi^2/720 (EM Casimir, plates; generous)": math.pi**2 / 720,
}
for name, a in alphas.items():
    for eta in (1, 10):
        ratio = math.sqrt(8 * a * eta)
        print(f"  alpha={a:.3e} [{name}], eta={eta:>2}: R_max/l_sp = {ratio:.3e}")

print("\nStep 2b: N needed for a self-consistent single-scale throat of radius R")
a_gen, eta_gen = math.pi**2 / 720, 10  # most generous pair above
for R in (lP, 1e-19, 1e-15, 1e-3, 1.0, 1.5e7):
    N = R**2 / (8 * a_gen * eta_gen * lP**2)
    print(f"  R = {R:.3e} m: N >= {N:.3e} species (alpha={a_gen:.4f}, eta={eta_gen}); "
          f"species length sqrt(N) l_P = {math.sqrt(N)*lP:.3e} m = {math.sqrt(N)*lP/R:.3f} R")

print("\nStep 2c: N = 1 (single field), most generous alpha, eta:")
print(f"  R_max = {math.sqrt(8*a_gen*eta_gen)*lP:.3e} m = {math.sqrt(8*a_gen*eta_gen):.3f} l_P")

# ---- Step 3: what a C3 shortcut would buy at that size
print("\nStep 3: for R ~ l_sp, signal quantum must fit: lambda <= R, E_sig >= hbar c / R")
hbar, c, G = 1.054571817e-34, 2.99792458e8, 6.67430e-11
for N in (1.0, 1e40, 1e69):
    R = math.sqrt(N) * lP
    Esig = hbar * c / R
    Mthroat = R * c**2 / G  # ~ mass scale of a throat of radius R (geometric b0 -> kg)
    print(f"  N={N:.0e}: R={R:.3e} m, E_sig >= {Esig:.3e} J, throat mass scale {Mthroat:.3e} kg,"
          f" E_sig/(M c^2) = {Esig/(Mthroat*c**2):.3e} (= 1/N)")
