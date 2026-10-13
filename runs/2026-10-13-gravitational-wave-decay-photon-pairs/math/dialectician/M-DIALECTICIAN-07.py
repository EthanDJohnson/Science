"""M-DIALECTICIAN-07: luminosity-set rate (F6).

From the chirped-bin total P = 4 pi^2 c G_nat^2 N^2 w^3 / t_b (natural units, M-06), a source of
constant GW power L over t_b has N = L t_b/(hbar w). Restore units: G_nat = G/(hbar c^5),
energies hbar w; rate = (energy-rate)/hbar. Claim: P/t_b = 4 pi^2 c G^2 L^2 w / c^10 (SI).
Numbers: GW150914 L = 3.6e49 W, 150 Hz -> 1.4e-3 /s, photon power 2 R hbar w = 2.8e-34 W;
GW170817 L = 1.8e44 W, 100 Hz -> 2.3e-14 /s, 3.1e-45 W. B&O eq. 8 value 1.4e-4 /s (M-01).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import math
from math_checks import identity, units, quantity, finish
from unit_tools import Q

cr, G, hbar, cl, L, w, tb = sp.symbols("c_r G hbar c_l L w t_b", positive=True)
Nn = L * tb / (hbar * w)
# P is a number; in natural units 1/t_b is an energy hbar/t_b... build: P = 4 pi^2 c G_nat^2 N^2 W^3 / T_nat
# with W = hbar w (energy), T_nat = t_b/hbar (1/energy)
P = 4 * sp.pi**2 * cr * (G / (hbar * cl**5)) ** 2 * Nn**2 * (hbar * w) ** 3 / (tb / hbar)
identity(sp.simplify(P / tb), 4 * sp.pi**2 * cr * G**2 * L**2 * w / cl**10)
units("(6.674e-11 m^3/(kg s^2))^2 * (1 W)^2 * (1/s) / (2.998e8 m/s)^10", "frequency")
crv = 3 / (25 * math.pi)
Gv = Q("G").to("m^3/(kg s^2)"); cv = Q("c").to("m/s"); hb = Q("hbar").to("J s")
for label, Lv, f, rexp, wexp in (("GW150914", 3.6e49, 150.0, 1.4e-3, 2.8e-34), ("GW170817", 1.8e44, 100.0, 2.3e-14, 3.1e-45)):
    wv = 2 * math.pi * f
    R = 4 * math.pi**2 * crv * Gv**2 * Lv**2 * wv / cv**10
    Wph = 2 * R * hb * wv
    print(f"{label}: R = {R:.4e} pairs/s, photon power = {Wph:.4e} W")
    quantity(f"{R} / s", f"{rexp} / s", rel_tol=3e-2)
    quantity(f"{Wph} W", f"{wexp} W", rel_tol=3e-2)
print(f"ratio to B&O eq. 8 value 1.397e-4 /s: {4*math.pi**2*crv*Gv**2*3.6e49**2*2*math.pi*150/cv**10/1.397e-4:.2f}")
raise SystemExit(finish())
