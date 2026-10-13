#!/usr/bin/env python3
"""Challenge (spacetime, referee 1): independent HAND derivation (sympy) of B&O eq. 8 from eq. 7 + S6, and of the exact
in-out total (energy delta kept) -> T_eff = 4 pi/(3 sig).  No use of the analysis' code.

Derivation (narrow band, top hat f = Theta on |k - w| < sig/2, Theta^2 = 2 pi^2 N/(w sig)):
  eq.7: A = 4 pi G (2pi)^-6 int dk1~ dk2~ f f (s^2-2tu)/s (2pi)^4 delta^4 ; two-body graviton phase space int d3k1 d3k2/(2k1 2k2)
  delta^4 = dOmega*/8 ; in the CM (s^2-2tu)/s = s(1+x^2)/2 ; lab energies k1,2 = (Q0 +- Q c)/2, so the band condition is
  |c| <= c0 = (sig - |d|)/Q, d = Q0 - 2w.  Hence A(d,Q,photon) = (G Theta^2 s/(16 pi)) 2pi [2c0(1+sb^2/2) + (2c0^3/3)(cb^2-sb^2/2)].
  Exact:  P = int d3Q dQ0/(2pi)^4 int dOmega_gamma/(32 pi^2) |A|^2   (x 1/2 identical photons x 2 helicities = 1)
  B&O:    2 pi delta(E-E') -> T  <=>  int dQ0 |A|^2 -> (T/2pi) |int dQ0 A|^2.   Leading order in sig/Q (c0^3 terms dropped).
"""
import sympy as sp

G, N, w, sig, Q, d, cb = sp.symbols('G N w sigma Q d c_b', positive=True)
Theta2 = 2 * sp.pi ** 2 * N / (w * sig)
s = 4 * w ** 2 - Q ** 2
sb2 = 1 - cb ** 2
c0 = (sig - d) / Q                     # d >= 0 half; symmetric
Aang = 2 * sp.pi * 2 * c0 * (1 + sb2 / 2)          # leading order (c0 << 1)
A = G * Theta2 * s / (16 * sp.pi) * Aang
Abar = 2 * sp.integrate(A, (d, 0, sig))            # int dQ0 A
A2int = 2 * sp.integrate(A ** 2, (d, 0, sig))      # int dQ0 |A|^2
photon = lambda F: 2 * sp.pi * sp.integrate(F, (cb, -1, 1)) / (32 * sp.pi ** 2)
rate = sp.integrate(4 * sp.pi * Q ** 2 * photon(Abar ** 2), (Q, 0, 2 * w)) / (2 * sp.pi) ** 4 / (2 * sp.pi)
exact = sp.integrate(4 * sp.pi * Q ** 2 * photon(A2int), (Q, 0, 2 * w)) / (2 * sp.pi) ** 4
rate, exact = sp.simplify(rate), sp.simplify(exact)
print("hand rate dP/dt  =", rate, "   B&O eq.8 = 3 G^2 N^2 w^3 sig^2/(25 pi):", sp.simplify(rate - 3 * G**2 * N**2 * w**3 * sig**2 / (25 * sp.pi)) == 0)
print("exact total P    =", exact, " = ", sp.N(exact / (G**2 * N**2 * w**3 * sig)), "G^2 N^2 w^3 sig  (sig -> 0 limit)")
print("T_eff = P/rate   =", sp.simplify(exact / rate), " -> T_eff*sig =", sp.N(sp.simplify(exact / rate) * sig), "(4 pi/3 =", sp.N(4 * sp.pi / 3), ")")
print("Interpretation: B&O's own state yields a FINITE total of 4/25 G^2N^2w^3 sig pairs; eq.8 x T reproduces it only for T = 4pi/(3 sig).")
