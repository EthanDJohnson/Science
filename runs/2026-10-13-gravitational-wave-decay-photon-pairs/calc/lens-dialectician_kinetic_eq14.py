#!/usr/bin/env python3
"""Dialectician lens, K1/K2 synthesis: is the 'N^2 coherent enhancement' just the n^2 of two-body kinetics?

Independent route to B&O eq. 14: an isotropic, unpolarised, monochromatic graviton gas of number density n
(energy w, rho = n w). Pair rate per volume (natural units, hbar = c = 1):
    Gamma/V = (1/2) n^2 < sigma_unpol(s) (1 - cos theta) >_iso ,   s = 2 w^2 (1 - cos theta),
with the factor 1/2 because each unordered graviton pair is counted once. sigma from the toolkit's closed form
(qft_second_order.sigma_total_massless_closed_form, normalised to Bjerrum-Bohr et al. 2016), averaged over the
four helicity combinations (unpolarised). Compare with B&O eq. 14: 8 pi G^2 rho^2 / 15.
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2  # noqa: E402

PI = math.pi
G = 1.0
w = 1.0
n = 1.0

# unpolarised sigma(s)/s
s_test = 1.0
combos = [("R", "R"), ("R", "L"), ("L", "R"), ("L", "L")]
sig = [q2.sigma_total_massless_closed_form(s_test, a, b, "photon", G) for a, b in combos]
sig_unpol_over_s = np.mean(sig) / s_test
print("sigma(RR, RL, LR, LL)/s =", [f"{x:.6f}" for x in sig], " (closed form opposite = 4 pi/5 =", f"{4 * PI / 5:.6f})")
print(f"unpolarised sigma/s = {sig_unpol_over_s:.6f} vs 2 pi/5 = {2 * PI / 5:.6f}")
# numeric cross-check of sigma_total at one s for the opposite helicity (quadrature route)
num = q2.sigma_total(s_test, "R", "L", "photon", 0.0, G)
print(f"quadrature sigma_total(RL)/s = {num:.6f}")

# isotropic average of sigma(s)(1 - cos) with s = 2 w^2 (1 - c)
c, wc = np.polynomial.legendre.leggauss(64)
avg = np.sum(wc * sig_unpol_over_s * 2 * w**2 * (1 - c) * (1 - c)) / 2.0
rate = 0.5 * n**2 * avg
rho = n * w
print(f"Gamma/V (kinetic, pairs) = {rate:.8f} G^2 rho^2 ;  B&O eq. 14: 8 pi/15 = {8 * PI / 15:.8f}")
print(f"ratio kinetic / B&O eq. 14 = {rate / (8 * PI / 15):.8f}")

# Same kinetic formula for two beams crossing at angle theta vs the toolkit's in-in two-beam routine
for th in (PI / 2, PI):
    br = q2.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, th, "R", "L", G=1.0)
    s_ = 2 * (1 - math.cos(th))
    kin = q2.sigma_total_massless_closed_form(s_, "R", "L", "photon", 1.0) * br["n1"] * br["n2"] * (1 - math.cos(th))
    print(f"theta = {th:.4f}: beams_pair_rate = {br['pair_rate']:.6g}; sigma n1 n2 (1-cos) = {kin:.6g}; "
          f"ratio = {br['pair_rate'] / kin:.6f}")

# collinear limit: the local rate for nearly parallel momenta falls as theta^4 (s ~ theta^2, flux ~ theta^2)
print("small-angle scaling of sigma(s)(1-cos theta) for opposite helicities:")
for th in (1e-1, 1e-2, 1e-3):
    s_ = 2 * (1 - math.cos(th))
    val = q2.sigma_total_massless_closed_form(s_, "R", "L", "photon", 1.0) * (1 - math.cos(th))
    print(f"  theta = {th:g}: {val:.4e}   (theta^4 * 2 pi/5 = {th**4 * 2 * PI / 5:.4e}; "
          f"sigma = (4pi/5) theta^2, 1 - cos = theta^2/2)")
