"""M-DIALECTICIAN-03: hbar counting (F3).

SI pair rate R = 3 G^2 E^2 w sigma^2/(25 pi c^10) (from M-01). Photon power W = 2 R hbar w
(two photons of energy hbar w per pair). Rayleigh-Jeans stimulation factor 1 + 2 f ~ 2 f with
f = kT/(hbar w) for kT >> hbar w. Claims: d ln R/d ln hbar = 0; d ln W/d ln hbar = 1;
W * 2kT/(hbar w) = 12 G^2 E^2 kT w sigma^2/(25 pi c^10), hbar-free.
Limit: full Bose factor 2/(exp(x)-1) -> 2/x as x = hbar w/kT -> 0.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, units, finish

G, hbar, c, E, w, sig, k, T, x = sp.symbols("G hbar c E w sigma k T x", positive=True)
R = 3 * G**2 * E**2 * w * sig**2 / (25 * sp.pi * c**10)
W = 2 * R * hbar * w
Wst = W * 2 * k * T / (hbar * w)
identity(hbar * sp.diff(sp.log(R), hbar), 0)
identity(hbar * sp.diff(sp.log(W), hbar), 1)
identity(Wst, 12 * G**2 * E**2 * k * T * w * sig**2 / (25 * sp.pi * c**10))
identity(hbar * sp.diff(sp.log(Wst), hbar), 0)
# RJ limit of the Bose factor 2 f = 2/(e^x - 1) -> 2/x (x = hbar w / kT)
limit(x * 2 / (sp.exp(x) - 1), "x", 0, 2)
# units: W in watts, stimulated W in watts
units("(6.674e-11 m^3/(kg s^2))^2 * (1 J)^2 * (1/s)^4 * (1 J s) / (2.998e8 m/s)^10", "power")
units("(6.674e-11 m^3/(kg s^2))^2 * (1 J)^2 * (1 J) * (1/s)^3 / (2.998e8 m/s)^10", "power")
raise SystemExit(finish())
