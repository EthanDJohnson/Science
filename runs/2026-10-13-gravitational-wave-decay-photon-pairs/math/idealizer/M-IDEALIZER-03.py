"""M-IDEALIZER-03: eqs. 9-12 from eq. 8, and hbar counting.

Natural units: pair rate dP/dt = 3 G^2 N^2 w^3 sig^2/(25 pi); N = E/w (hbar = 1).
Claims: photon rate = 2 dP/dt; tau = 1/(photon rate) = 25 pi/(6 G^2 E^2 w sig^2); W = w * photon rate
= 6 G^2 E^2 w^2 sig^2/(25 pi); eq. 12: W = (3/(50 pi)) (r_m/l)^2 (hbar w)^2/hbar with r_m = 2 G E/c^4, l = c/sig.
SI restoration: G_nat = G hbar/c^5 (time^2 per hbar... used as G_nat -> G/(hbar c^5) in 1/J^2), N = E/(hbar w).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, units, quantity, finish
import sympy as sp

G, Ee, w, sig, hb, c = sp.symbols("G E_ w sigma hbar c", positive=True)
N = Ee / w
pair_rate = 3 * G**2 * N**2 * w**3 * sig**2 / (25 * sp.pi)
ph_rate = 2 * pair_rate
identity(1 / ph_rate, 25 * sp.pi / (6 * G**2 * Ee**2 * w * sig**2))
identity(w * ph_rate, 6 * G**2 * Ee**2 * w**2 * sig**2 / (25 * sp.pi))

# SI restoration with explicit hbar, c: G_nat = G/(hbar c^5) [1/J^2], energies in J, rates in 1/s need /hbar
# pair number per packet (natural): (4/25) G^2 N^2 w^3 sig with w, sig as energies hbar*w, hbar*sig
Gn = G / (hb * c**5)
P_SI = sp.Rational(4, 25) * Gn**2 * (Ee / (hb * w))**2 * (hb * w)**3 * (hb * sig)
print("pair number per packet (SI):", sp.simplify(P_SI))
identity(P_SI, sp.Rational(4, 25) * G**2 * Ee**2 * w * sig / c**10)    # hbar-free
# luminosity: energy per time = (hbar w) * photon number rate; rate (natural, energy units) / hbar -> 1/s
rate_SI = (3 * Gn**2 * (Ee / (hb * w))**2 * (hb * w)**3 * (hb * sig)**2 / (25 * sp.pi)) / hb
W_SI = hb * w * 2 * rate_SI
r_m, l = 2 * G * Ee / c**4, c / sig
identity(W_SI, sp.Rational(3, 50) / sp.pi * (r_m / l)**2 * (hb * w)**2 / hb)
print("dW/dhbar * hbar/W =", sp.simplify(sp.diff(W_SI, hb) * hb / W_SI), "(1 = linear in hbar)")
identity(sp.diff(W_SI, hb) * hb / W_SI, 1)
# units
units("(6.674e-11 m^3/(kg s^2))^2 * (1 J)^2 * (1/s) * (1/s) / (299792458 m/s)^10", "dimensionless")
units("(2*6.674e-11 m^3/(kg s^2) * 1 J / (299792458 m/s)^4 / (299792458 m/s / (1/s)))^2 * hbar * (1/s)^2", "W")
# limit: sigma -> 0 gives zero rate (no band, no fusion)
identity(W_SI.subs(sig, 0), 0)
raise SystemExit(finish())
