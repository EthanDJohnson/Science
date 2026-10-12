#!/usr/bin/env python3
"""Challenge (spacetime, referee 1): is the physical (retarded) near zone negligible next to B&O's Pauli-Jordan (PJ) focus?

Independent code (no taskB_* imports). Steady fields psi(x) e^{-iwt}, scalar proxy J = psi^2 (one polarisation component),
gravity weight rho(s) = (pi/5) G^2 s^2 (as in the analysis; G = w = 1).  Pair rate (pairs per unit time):
    Gamma[psi] = int d3Q/(2pi)^3 rho(s) |J~(Q)|^2,  s = 4 - Q^2,  J~ = int d3x e^{-iQ.x} psi^2.
For psi = R(r) Y_l0:  psi^2 = R^2 sum_L c_L Y_L0  ->  int dOmega_Q |J~|^2 = (4pi)^2 sum_L c_L^2 |H_L(Q)|^2,
    H_L(Q) = int r^2 R^2 S(r) j_L(Qr) dr   (S = switch-on window, far taper T(r) for convergence).
Equal-luminosity comparison:  PJ standing wave R = 2 j_l(r)   (its outgoing half is h_l^(1))
                              physical outgoing  R = h_l^(1)(r) x S(r/r_min),  S = exp(-(r_min/r)^2)  (as in the analysis)
QUANTITY: ratio of pair rates at equal GW luminosity; for narrow-band bursts the same ratio holds for total yields
(the analysis' own table: burst P_out/P_PJ = steady ratio for l = 0).  Two numerical settings are compared for robustness.
"""
import math
import time

import numpy as np
from scipy.special import spherical_jn, eval_legendre

PI = math.pi
xl, wl = np.polynomial.legendre.leggauss(60)


def gaunt(l):
    Y = lambda L: np.sqrt((2 * L + 1) / (4 * PI)) * eval_legendre(L, xl)
    if l == 0:
        return {0: 1 / math.sqrt(4 * PI)}
    return {L: float(2 * PI * np.sum(wl * Y(2) ** 2 * Y(L))) for L in (0, 2, 4)}


def h1(l, x):
    if l == 0:
        return -1j * np.exp(1j * x) / x
    return 1j * np.exp(1j * x) * (1 / x + 3j / x ** 2 - 3 / x ** 3)


def rate(l, kind, rmin=None, dr=0.01, rT=300.0):
    r = np.arange(dr / 2, 3.2 * rT, dr)
    T = np.exp(-(r / rT) ** 2)
    if kind == "pj":
        R = 2 * spherical_jn(l, r)
        W = T
    else:
        R = h1(l, r)
        W = T * np.exp(-(rmin / r) ** 2)
    base = r * r * R * R * W * dr
    cL = gaunt(l)
    # Q nodes: Gauss-Legendre on [0, 2] in variable x = Q/2, clustered toward the s -> 0 end
    u, wu = np.polynomial.legendre.leggauss(160)
    y = 0.5 * (u + 1)                      # in (0,1)
    x = 1 - (1 - y) ** 2                   # cluster near x = 1
    wx = 0.5 * wu * 2 * (1 - y)
    Q = 2 * x
    tot = np.zeros(Q.size)
    for L, c in cL.items():
        H = np.array([np.dot(spherical_jn(L, q * r), base) for q in Q])
        tot += c * c * np.abs(H) ** 2
    integrand = Q ** 2 * (PI / 5) * (4 - Q ** 2) ** 2 * (4 * PI) ** 2 * tot / (2 * PI) ** 3
    return float(np.sum(integrand * 2 * wx))   # dQ = 2 dx


t0 = time.time()
print("=== field strength: PJ focus vs physical near field (steady, equal luminosity; |R| relative to outgoing far-field |h1| ~ 1/(w r)) ===")
xs = np.linspace(0.01, 12, 120000)
for l in (0, 2):
    pjmax = np.max(np.abs(2 * spherical_jn(l, xs)))
    print(f"  l={l}: max |R_PJ| = {pjmax:.3f} (at w r = {xs[np.argmax(np.abs(2*spherical_jn(l, xs)))]:.2f});"
          f"  |h_l^(1)| at w r = 1: {abs(h1(l, 1.0)):.3f}, at w r = 0.5: {abs(h1(l, 0.5)):.3f}")

for setting in ({"dr": 0.01, "rT": 300.0}, {"dr": 0.02, "rT": 600.0}):
    print(f"\n=== pair rates (proxy, G = w = 1, units G^2 B^4 w^...; only ratios matter), setting {setting} ===")
    res = {}
    for l in (0, 2):
        pj = rate(l, "pj", **setting)
        res[(l, "pj")] = pj
        line = f"  l={l}: PJ standing wave Gamma = {pj:.5e}"
        for rm in (0.5, 0.7, 1.0, 2.0, 2 * PI):
            g = rate(l, "out", rm, **setting)
            res[(l, rm)] = g
            line += f"\n        outgoing r_min = {rm:6.3f}/w: Gamma = {g:.5e}  Gamma_out/Gamma_PJ = {g/pj:.4e}"
        print(line, flush=True)
    for rm in (0.5, 0.7, 1.0, 2.0, 2 * PI):
        print(f"  K_l2/K_l0 at w r_min = {rm:6.3f}: {res[(2, rm)]/res[(0, rm)]*gaunt(0)[0]**-2/(4*PI):.2f}"
              f"  (ratio of outgoing rates per unit luminosity)")
    print(f"  PJ standing l=2 / l=0: {res[(2,'pj')]/res[(0,'pj')]:.4f}   [{time.time()-t0:.0f} s]")

# consequence for the analysis' merger and steady-source numbers (inputs: the analysis' printed table, taskB_outgoing.py)
print("\n=== consequence (uses taskB_outgoing.py printed values: B&O-applied 0.03820 G^2L^2w; monopole proxy at r_min = 1/w"
      " 6.426e-03; merger 1.909e-09 pairs; B&O rate x t_m = 6.987e-07 pairs) ===")
ratio = res[(2, 1.0)] / res[(0, 1.0)] / (gaunt(0)[0] ** 2 * 4 * PI)
Ccoh, g_bin = 0.40922, 0.03968
print(f"  l=2 (with near-field terms) / monopole at r_min = 1/w = {ratio:.1f}")
print(f"  steady: proxy l=2 at r_min = 1/w = {6.426e-3*ratio:.3e} G^2L^2w; x C_coh x g_binary = {6.426e-3*ratio*Ccoh*g_bin:.3e}"
      f" vs B&O-applied 0.0382  (ratio {6.426e-3*ratio*Ccoh*g_bin/0.0382:.2f})")
print(f"  merger: in-in beyond r_min = 1/w (318 km) rescaled to l=2: {1.909e-9*ratio:.2e} pairs vs B&O rate x t_m 6.99e-07"
      f" (ratio {1.909e-9*ratio/6.987e-7:.2f})")
