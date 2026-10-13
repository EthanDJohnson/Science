"""M-EXAMINER-09 (SI): linear-channel vs fusion per-packet totals (order of magnitude, k uncomputed).
Inputs (lens / B&O): GW150914 bin E = 3.57e47 J at f = 150 Hz, sigma = 200 rad/s; GW170817 bin E = 1.8e44 W x 0.60 s,
f = 100 Hz, sigma = 0.1 x 2 pi x 100 rad/s. N = E/(hbar w), w = 2 pi f.
  P_lin/k = (hbar w / E_Pl)^2 N, E_Pl = sqrt(hbar c^5/G)
  P_BO   = c_tot (G hbar/c^5)^2 N^2 w^3 sigma, c_tot = 4/25 (= rate coefficient 3/(25 pi) x T_eff (4 pi/3)/sigma)
Claimed identity: P_BO / (P_lin/k) = c_tot G E sigma / c^5 (dimensionless).
Own derivation: (G hbar/c^5)^2 N^2 w^3 sigma / ((hbar w)^2 G/(hbar c^5) N) = G hbar N w sigma / c^5 = G E sigma / c^5."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, quantity, units, finish

Gs, hb, cs, Ns, w, sg = sp.symbols("G hbar c N omega sigma", positive=True)
ctot = sp.Rational(4, 25)
P_BO = ctot * (Gs * hb / cs ** 5) ** 2 * Ns ** 2 * w ** 3 * sg
P_lin = (hb * w) ** 2 / (hb * cs ** 5 / Gs) * Ns
identity(sp.simplify(P_BO / P_lin), ctot * Gs * (Ns * hb * w) * sg / cs ** 5)
identity(sp.Rational(3, 25) / sp.pi * (4 * sp.pi / 3), ctot)
units("G * 1 J * 1 Hz / c^5", "dimensionless")

G, hbar, c = 6.67430e-11, 1.054571817e-34, 299792458.0
EPl = math.sqrt(hbar * c ** 5 / G)
for name, E, f, sig, lens in (("GW150914", 3.57e47, 150.0, 200.0, (3.6e78, 5.1e-41, 9.3e-3, 2.9e-6, 3.2e-4)),
                              ("GW170817", 1.8e44 * 0.60, 100.0, 0.1 * 2 * math.pi * 100.0, (None, None, 1.9e-6, 5.6e-14, 3.0e-8))):
    om = 2 * math.pi * f
    N = E / (hbar * om)
    x = hbar * om / EPl
    Pl = x ** 2 * N
    Pb = 0.16 * (G * hbar / c ** 5) ** 2 * N ** 2 * om ** 3 * sig
    ratio = Pb / Pl
    print(f"{name}: N = {N:.3e}; hbar w/E_Pl = {x:.3e}; P_lin/k = {Pl:.3e}; P_BO = {Pb:.3e}; ratio = {ratio:.3e};"
          f" c_tot G E sigma/c^5 = {0.16 * G * E * sig / c ** 5:.3e}")
    got = (N, x, Pl, Pb, ratio)
    for g, l in zip(got, lens):
        if l is not None:
            identity(sp.Float(f"{g:.1e}"), sp.Float(f"{l:.1e}"))
quantity("0.16 * G * 3.57e47 J * 200 Hz / c^5", "3.13e-4", rel_tol=0.02)
raise SystemExit(finish())
