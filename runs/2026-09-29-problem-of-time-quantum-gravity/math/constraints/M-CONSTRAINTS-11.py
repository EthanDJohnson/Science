"""M-CONSTRAINTS-11: unimodular time uncertainty relation (SI).

Einstein-Hilbert action with Lambda, d^4x in m^4 (x^0 = ct): S = (c^3/(16 pi G)) int (R - 2 Lambda) sqrt(-g) d^4x.
Lambda term: -(c^3/(8 pi G)) Lambda V4. In unimodular gravity Lambda is canonically conjugate to V4 with
momentum P = -c^3 Lambda/(8 pi G). Robertson: Delta P Delta V4 >= hbar/2 => Delta Lambda Delta V4 >= 4 pi hbar G/c^3 = 4 pi l_P^2.
Claims (F11): 4 pi l_P^2 = 3.28e-69 m^2; resolving cosmic time to 1 s over a Hubble volume
(V_H = (4 pi/3)(c/H0)^3, H0 = 67.4 km/s/Mpc; Delta V4 = c * 1 s * V_H) needs Delta Lambda >= 1.0e-156 m^-2 = 9e-105 Lambda_obs
(Lambda_obs = 1.09e-52 m^-2); at 1e-15 s, 9e-90 Lambda_obs.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, limit, finish

hb, G, c = sp.symbols("hbar G c", positive=True)
# (hbar/2) / (c^3/(8 pi G)) = 4 pi hbar G / c^3
identity((hb / 2) / (c**3 / (8 * sp.pi * G)), 4 * sp.pi * hb * G / c**3)
units("c^3/(8*pi*G) * (1 1/m^2) * (1 m^4)", "J s")            # action units: Lambda term is an action
units("4*pi*hbar*G/c^3", "m^2")
quantity("4*pi*hbar*G/c^3", "3.28e-69 m^2", rel_tol=3e-3)
quantity("4*pi*l_P^2", "3.28e-69 m^2", rel_tol=3e-3)
VH = "(4*pi/3)*(c/(67.4 km/s/Mpc))^3"
dL1 = f"(4*pi*hbar*G/c^3)/(c*1 s*{VH})"
quantity(dL1, "1.0e-156 1/m^2", rel_tol=0.03)
quantity(f"{dL1}/(1.09e-52 1/m^2)", "9e-105", rel_tol=0.05)
quantity(f"(4*pi*hbar*G/c^3)/(c*1e-15 s*{VH})/(1.09e-52 1/m^2)", "9e-90", rel_tol=0.05)
# limit: hbar -> 0 removes the trade-off (classical unimodular gravity has sharp Lambda and V4)
limit(4 * sp.pi * hb * G / c**3, "hbar", 0, "0")
raise SystemExit(finish())
