"""M-CONSTRAINTS-03: cosmic injection by eq. 14 and the depletion time.
Natural units. Radiation era. Graviton energy w << T (stimulated): energy injected per pair
= 2 w (1 + 2 f), f = 1/(e^{w/T}-1) ~ T/w, so ~ 4T per pair.
d(Drho/rho_gamma)/dln a = 4 T Gamma / (rho_gamma H), Gamma = (8pi/15) G^2 r^2 rho_gamma^2, r = rho_GW/rho_gamma
(constant, both radiation). H^2 = (8 pi G/3) rho_tot, rho_tot = rho_gamma (1 + 0.6813) (3 nu, N_eff = 3.046 -> 0.6918;
use 3.046). Integrate from z = 1e5 to 3e6 (mu window). Claim: <= 4.3e-79.
Scale claim: (T/M_Pl)^3 = 1.9e-76 at z = 3e6, M_Pl = 1.2209e28 eV (non-reduced).
Depletion time (stimulated) today: tau = rho_GW/(4 kT Gamma) = 6.8e115 s at DeltaN_eff = 0.3.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, limit, finish

# symbolic: integrand per e-fold proportional to T^3; the integral over ln a from T_min to T_max -> value(T_max)/3
T, Gn, r, k = sp.symbols("T G r k", positive=True)
rho_g = sp.pi**2 / 15 * T**4
Nnu = 3.046
H = sp.sqrt(8 * sp.pi * Gn / 3 * rho_g * (1 + sp.Rational(7, 8) * (sp.Rational(4, 11))**sp.Rational(4, 3) * sp.Float(Nnu)))
integrand = 4 * T * sp.Rational(8, 15) * sp.pi * Gn**2 * r**2 * rho_g**2 / (rho_g * H)
ratio = sp.simplify(integrand / (r**2 * T**3 * Gn**sp.Rational(3, 2)))
print("integrand / (r^2 (T/M_Pl)^3) =", sp.N(ratio))
# exponent check: T*d ln(integrand)/dT = 3
identity(sp.simplify(T * sp.diff(sp.log(integrand), T)), 3)

# numbers
kB = 8.617333e-5      # eV/K
T0 = 2.7255
MPl = 1.220890e28     # eV
fac = 7 / 8 * (4 / 11)**(4 / 3)
rr = fac * 0.3
C = float(ratio)
def T_eV(z): return kB * T0 * (1 + z)
x3 = (T_eV(3e6) / MPl)**3
print("(T/M_Pl)^3 at z=3e6:", x3)
quantity(f"{x3}", "1.9e-76", rel_tol=0.03)
# integral over ln(1+z) from 1e5 to 3e6 of C r^2 (T/MPl)^3
val = C * rr**2 * ((T_eV(3e6) / MPl)**3 - (T_eV(1e5) / MPl)**3) / 3
print("Delta rho/rho (mu window, stimulated, plasma ignored):", val)
quantity(f"{val}", "4.3e-79", rel_tol=0.05)
# limit: stimulated factor 2w(1+2f) -> 4T as w/T -> 0
x = sp.symbols("x", positive=True)  # x = w/T
limit(2 * x * (1 + 2 / (sp.exp(x) - 1)), "x", 0, 4)

# depletion time today, SI
G, c, kJ = 6.67430e-11, 299792458.0, 1.380649e-23
rho_GW = fac * 0.3 * 7.5657e-16 * T0**4
Gam = 8 * math.pi / 15 * G**2 * rho_GW**2 / c**7
tau_st = rho_GW / (4 * kJ * T0 * Gam)
hw = 6.62607015e-34 * 25.0       # 25 Hz graviton
tau_un = rho_GW / (2 * hw * Gam)
print("tau stimulated =", tau_st, "s ; unstimulated (25 Hz) =", tau_un, "s ; t_H units:", tau_st / 4.36e17)
quantity(f"{tau_st} s", "6.8e115 s", rel_tol=0.05)
quantity(f"{tau_un} s", "3.1e125 s", rel_tol=0.05)
raise SystemExit(finish())
