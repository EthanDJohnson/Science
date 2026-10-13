#!/usr/bin/env python3
"""Task B (2b): WHERE and WHEN in space-time the S-matrix fusion probability of B&O's state is generated.

Exact second-order amplitude (scalar proxy with the validated gravity weight, see taskB_luminosity_check.py):
    J(x) = psi(x)^2 W(x),   J~(Q) = int d4x e^{iQx} J(x),   P[W] = int d4Q/(2pi)^4 rho(Q^2) |J~(Q)|^2,  rho = (pi/5) G^2 s^2,
psi = the free (Pauli-Jordan) field of the narrow-band spherical state (taskB_common.radial_free), evaluated on a (t, r) grid;
W = 1 gives the full S-matrix probability (validated against the momentum-space closed form of taskB_pj_exact.py).
Inserting smooth space-time windows W shows where the amplitude is built:
    inside-R   W = exp(-(r/R)^2)           (only the region within ~R of the origin is allowed to interact)
    outside-R  W = 1 - exp(-(r/R)^2)       (the focal region is switched off)
    time       W = exp(-((t - t_c)/T_w)^2) (rate around t_c: P[W]/(T_w sqrt(pi/2)))
Windows smooth on scales >> 1/w only smear s by O(w/R) or O(w/T_w), negligible against the s ~ w^2 of the pairs that matter.
Gaussian band, sig = 0.1 w (B&O's eps = 0.1), units w = 1, G = 1; results quoted as P/(G^2 N^2 w^3 sig).
l = 0: B&O's isotropic state; l = 2 (m = 0): quadrupole angular pattern, J = R_2^2 Y_20^2 = sum_L c_L R_2^2 Y_L0.
"""
import math
import sys
import time

import numpy as np
from scipy.special import spherical_jn

sys.path.insert(0, "/home/user/Science/checks/2026-10-11-blas-oller-gw-decay/calc")
from taskB_common import Band, gaunt_Y20sq, radial_free  # noqa: E402

PI = math.pi
LAM = 2 * PI
sig = 0.1
b = Band("gauss", 1.0, sig)
T = 9.0 / sig
dt, dr = 0.15, 0.1
t = np.arange(-T, T + dt / 2, dt)
r = (np.arange(int((T + 9 / sig) / dr)) + 0.5) * dr
Qg = np.arange(0.0, 2.95, 0.006)
Q0 = 2.0 + np.linspace(-0.9, 0.9, 301)
taper = np.ones_like(t)
edge = np.abs(t) > 0.6 * T
taper[edge] = np.cos(0.5 * PI * (np.abs(t[edge]) - 0.6 * T) / (0.4 * T)) ** 2
rho = lambda s: np.where(s > 0, (PI / 5) * s * s, 0.0)
S = Q0[:, None] ** 2 - Qg[None, :] ** 2
RHO = rho(S)
Ft = np.exp(1j * np.outer(Q0, t)) * dt                     # time DFT at the needed Q0 only

spatial = {"full": np.ones_like(r)}
for R in (0.5, 1.0, 2.0, 4.0, 8.0):
    spatial[f"in {R:g}lam"] = np.exp(-(r / (R * LAM)) ** 2)
for R in (1.0, 2.0, 4.0, 8.0):
    spatial[f"out {R:g}lam"] = 1 - np.exp(-(r / (R * LAM)) ** 2)


def run(l: int):
    Ls = (0,) if l == 0 else (0, 2, 4)
    cL2 = {0: 4 * PI} if l == 0 else {L: c * c for L, c in gaunt_Y20sq().items()}
    N = b.number_iso() if l == 0 else b.number_lm()
    M = {L: 4 * PI * (r * r * dr)[None, :] * spherical_jn(L, np.outer(Qg, r)) for L in Ls}
    H = {(k, L): np.zeros((Qg.size, t.size), complex) for k in spatial for L in Ls}
    ch = 200
    for i in range(0, t.size, ch):
        tt = t[i:i + ch]
        RR = radial_free(b, l, r[:, None], tt[None, :])
        J = RR * RR * taper[None, i:i + ch]
        for k, Wr in spatial.items():
            JW = J * Wr[:, None]
            for L in Ls:
                H[(k, L)][:, i:i + ch] = M[L] @ JW

    def prob(Hd, wt=None):
        tot = np.zeros_like(RHO)
        for L in Ls:
            Hx = Hd[L] if wt is None else Hd[L] * wt[None, :]
            Jt = Ft @ Hx.T                          # (Q0, Q)
            tot += cL2[L] * np.abs(Jt) ** 2
        integrand = RHO * Qg[None, :] ** 2 * tot / (2 * PI) ** 3
        return np.trapezoid(np.trapezoid(integrand, Qg, axis=1), Q0) / (2 * PI)

    unit = N * N * sig
    res = {}
    for k in spatial:
        res[k] = prob({L: H[(k, L)] for L in Ls}) / unit
    full = {L: H[("full", L)] for L in Ls}
    Tw = 8.0
    rates = []
    for tc in np.arange(-60.0, 60.1, 5.0):
        wt = np.exp(-((t - tc) / Tw) ** 2)
        rates.append((tc, prob(full, wt) / unit / (Tw * math.sqrt(PI / 2))))
    return res, rates


for l in (0, 2):
    t0 = time.time()
    res, rates = run(l)
    print(f"\n=== l = {l}: Pauli-Jordan field of the Gaussian shell, sig = {sig} w; P in units of G^2 N^2 w^3 sig ===")
    if l == 0:
        print(f"full grid P = {res['full']:.5f}   (momentum-space closed form, taskB_pj_exact.py: 0.46763)")
    else:
        print(f"full grid P = {res['full']:.5f}   (quadrupole pattern; no closed form)")
    for k, v in res.items():
        if k != "full":
            print(f"  window {k:10s}: P = {v:.5f}   = {v/res['full']:.4f} of full")
    print("  time-resolved rate (Gaussian time window T_w = 8/w around t_c), units G^2 N^2 w^3 sig^2:")
    tot = 0.0
    for tc, rr in rates:
        tot += rr * 5.0
        print(f"     t_c*w = {tc:6.1f} (t_c*sig = {tc*sig:5.2f}):  dP/dt = {rr/sig:.5f}")
    print(f"  sum dP/dt * 5 = {tot:.5f} (vs full P = {res['full']:.5f});  B&O eq.8 rate for comparison: 3/(25 pi) = {3/(25*PI):.5f}"
          f" (their kernel/top hat; proxy kernel differs by O(1))")
    print(f"  [{time.time()-t0:.0f} s]")
