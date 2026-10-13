"""M-DIALECTICIAN-01: eq. 8 in SI, and the GW150914 numbers of F1/F2.

Claim: natural-units pair rate R = 3 G^2 N^2 w^3 sigma^2/(25 pi) with N = E/(hbar w)
becomes, in SI, R = 3 G^2 E^2 w sigma^2/(25 pi c^10). With E = 2 Msun c^2, f = 150 Hz,
sigma = 200 rad/s: R = 1.397e-4 /s, tau = 1/(2R) = 3578 s, T_eff = 4 pi/(3 sigma) = 0.0209 s,
P = R T_eff = 2.9e-6, t_prop(410 Mpc) = 4.22e16 s, R t_prop = 5.9e12, t_prop/T_eff = 2.0e18,
tau sigma = 7.2e5.
Independent route: restore hbar and c by dimensional analysis (G_nat -> hbar G/c^5, rate in 1/s),
then evaluate with CODATA constants.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, finish, limit
from unit_tools import Q

G, hbar, c, E, w, sig = sp.symbols("G hbar c E w sigma", positive=True)
Nn = E / (hbar * w)
# natural-units expression with G -> hbar G / c^5 (G_nat has dimension energy^-2, hbar=c=1)
# natural G = 1/E_Planck^2 = G/(hbar c^5) in 1/J^2; energies hbar w, hbar sigma
R_energy = sp.Rational(3, 25) / sp.pi * (G / (hbar * c**5)) ** 2 * Nn**2 * (hbar * w) ** 3 * (hbar * sig) ** 2
# R_energy has units of energy (rate x hbar); rate = R_energy / hbar
R_si = sp.simplify(R_energy / hbar)
claimed = 3 * G**2 * E**2 * w * sig**2 / (25 * sp.pi * c**10)
identity(R_si, claimed)
identity(sp.diff(sp.log(R_si), hbar) * hbar, 0)  # hbar-independent
units("(6.674e-11 m^3/(kg s^2))^2 * (1 J)^2 * (1/s) * (1/s)^2 / (2.998e8 m/s)^10", "frequency")

# numbers
Esi = Q("2 * Msun * c^2").to("J")
wv = 2 * 3.141592653589793 * 150.0
sv = 200.0
Gv = Q("G").to("m^3/(kg s^2)")
cv = Q("c").to("m/s")
R = 3 * Gv**2 * Esi**2 * wv * sv**2 / (25 * 3.141592653589793 * cv**10)
print(f"E = {Esi:.4e} J, R = {R:.4e} pairs/s")
quantity(f"{R} / s", "1.397e-4 / s", rel_tol=3e-3)
tau = 1 / (2 * R)
print(f"tau = 1/(2R) = {tau:.1f} s")
quantity(f"{tau} s", "3578 s", rel_tol=3e-3)
Teff = 4 * 3.141592653589793 / (3 * sv)
P = R * Teff
print(f"T_eff = {Teff:.5f} s, P = {P:.4e}")
quantity(f"{Teff} s", "0.0209 s", rel_tol=3e-3)
quantity(f"{P}", "2.9e-6", rel_tol=2e-2)
tprop = Q("410 Mpc / c").to("s")
print(f"t_prop = {tprop:.4e} s, R t_prop = {R*tprop:.4e}, t_prop/T_eff = {tprop/Teff:.4e}, tau sigma = {tau*sv:.4e}")
quantity(f"{tprop} s", "4.22e16 s", rel_tol=3e-3)
quantity(f"{R*tprop}", "5.9e12", rel_tol=1e-2)
quantity(f"{tprop/Teff}", "2.0e18", rel_tol=2e-2)
quantity(f"{tau*sv}", "7.2e5", rel_tol=1e-2)
# limit: sigma -> 0 (monochromatic) the rate vanishes
limit(claimed, "sigma", 0, 0)
raise SystemExit(finish())
