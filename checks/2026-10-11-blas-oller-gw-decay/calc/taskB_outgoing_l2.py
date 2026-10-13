#!/usr/bin/env python3
"""Task B (3), realistic angular pattern: steady outgoing l = 2 (m = 0) wave psi = B h_2^(1)(w r) Y_20 e^{-iwt}, INCLUDING its
near-field terms (1/r^2, 1/r^3), versus the outgoing monopole, both switched on smoothly by S = exp(-(r_min/r)^2).
Direct radial quadrature with a far Gaussian taper exp(-(r/r_T)^2), r_T = max(30 r_min, 400/w) (it only removes pairs with
formation length > r_T, i.e. a share ~ (r_min/r_T)^3 of the yield). The monopole column is checked against the exact
closed form of taskB_outgoing.py (K values printed there for the same window).
Quantity: K defined by dP/dt = (16/pi^2) c L^2 w K (pairs per unit time; L = GW luminosity; c = rho/s^2 weight),
so K_l2/K_l0 = rate ratio at equal luminosity. Formation-length expectation for large r_min: K_l2/K_l0 = 4 pi int |Y_20|^4.
Units w = 1.
"""
import math
import sys

import numpy as np
from scipy.special import spherical_jn

sys.path.insert(0, "/home/user/Science/checks/2026-10-11-blas-oller-gw-decay/calc")
from taskB_common import gaunt_Y20sq  # noqa: E402

PI = math.pi
LAM = 2 * PI
cL = gaunt_Y20sq()
pattern = 4 * PI * sum(c * c for c in cL.values())
print(f"Gaunt c_L (Y_20^2 = sum c_L Y_L0): {cL};  4 pi int |Y_20|^4 = {pattern:.5f}")


def h_out(l, x):
    if l == 0:
        return -1j * np.exp(1j * x) / x
    return 1j * np.exp(1j * x) * (1 / x + 3j / x ** 2 - 3 / x ** 3)


def K_direct(l, rmin, rT_fac=30.0, dr=0.04):
    rT = max(rT_fac * rmin, 400.0)
    r = np.arange(dr / 2, 3 * rT, dr)
    W = np.exp(-(rmin / r) ** 2) * np.exp(-(r / rT) ** 2)
    base = r * r * h_out(l, r) ** 2 * W * dr
    Ls = (0,) if l == 0 else (0, 2, 4)
    c2 = {0: 1 / (4 * PI)} if l == 0 else {L: cL[L] ** 2 for L in Ls}
    xs = np.unique(np.concatenate([np.linspace(1e-3, 0.95, 200), 1 - np.geomspace(0.05, 1e-6, 160)]))
    tot = np.zeros(xs.size)
    for L in Ls:
        H = np.array([4 * PI * np.dot(spherical_jn(L, 2 * x * r), base) for x in xs])
        tot += c2[L] * np.abs(H) ** 2
    # dP/dt = (L^2/4)(2pi)^-3 int Q^2 dQ rho sum c_L^2 |H_L|^2, rho = c s^2, Q = 2x, s = 4 - Q^2 ; K = that/((16/pi^2) c L^2)
    integ = np.trapezoid((2 * xs) ** 2 * (4 - 4 * xs ** 2) ** 2 * tot * 2, xs)
    return integ / 4 / (2 * PI) ** 3 / (16 / PI ** 2)


for rm in (1.0, LAM, 2 * LAM, 5 * LAM, 10 * LAM):
    k0 = K_direct(0, rm)
    k2 = K_direct(2, rm)
    print(f"r_min = {rm/LAM:6.3f} lambda: K_l0 (direct) = {k0:.4e};  K_l2 = {k2:.4e};  K_l2/K_l0 = {k2/k0:.4f};"
          f"  K_l2 (w r_min)^3 = {k2*rm**3:.4e}", flush=True)
