#!/usr/bin/env python3
"""Challenge delta-1 (TASK C, finding 1): an independent re-derivation of R(0) = (dP/dt)_BO and P_tot.

Independent of taskC1/taskC2: my own prefactor derivation and explicit 4-vectors with an explicit Lorentz boost.
I do not use the cos(theta_g*) = (a-b)/K identity or the closed-form p, q of taskC1.

Prefactor (own derivation from eq. 7, with dk~ = d^3k/((2pi)^3 2|k|)):
  A(Q) = (1/2) 8 pi G (2pi)^4/(2pi)^6 int d^3k1/(2a) d^3k2/(2b) f f h delta^4 = (G/(4pi)) int d^3k1 f f h/(a b) delta(a+b-Q0)
  P = (1/2) sum_mu int d^4Q/(2pi)^4 dOmega*/(32 pi^2) |A|^2,  sum_mu = 2
    = G^2/(8192 pi^8) int d^3K dE dOmega* H(E)^2,      H = int d^3k1 Theta^2 h/(ab) delta(a+b-E)
  This equals S6's C0 x 2 pi with C0 = G^2/(16384 pi^9), so S6 follows from eq. 7 as written.
  Without the delta(E-E') constraint (B&O's 2 pi delta(0) -> T):  (dP/dt)_BO = G^2/(16384 pi^9) int d^3K dOmega* (int dE H)^2.
Ring parametrisation: d^3k1 = (a b/K) da db dalpha (from b^2 = a^2 + K^2 - 2aK cos th).
h = (t^2+u^2)/s with t = -2 k1.q1, u = -2 k2.q1. q1 is the CM photon (sqrt(s)/2)(1, n*) boosted along K.
Units: w = G = N = 1.
"""
import math
import numpy as np

PI = math.pi


def gl(a, b, n):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (a + b), 0.5 * (b - a) * w


def nodes_pw(breaks, n):
    xs, ws = [], []
    for a, b in zip(breaks[:-1], breaks[1:]):
        if b - a > 1e-14:
            x, w = gl(a, b, n)
            xs.append(x); ws.append(w)
    return np.concatenate(xs), np.concatenate(ws)


def run(sig, nK=28, nE=20, na=16, nal=12, nct=10, nph=8):
    Th2 = 2 * PI ** 2 / sig
    lo, hi = 1 - sig / 2, 1 + sig / 2
    # photon CM directions: K along z; nph azimuths; use symmetry-free full grid
    ct, wct = gl(-1, 1, nct)
    ph = (np.arange(nph) + 0.5) * 2 * PI / nph
    wph = np.full(nph, 2 * PI / nph)
    CT, PH = np.meshgrid(ct, ph, indexing="ij")
    WO = np.outer(wct, wph).ravel()
    nst = np.stack([np.sqrt(1 - CT ** 2) * np.cos(PH), np.sqrt(1 - CT ** 2) * np.sin(PH), CT], -1).reshape(-1, 3)
    al = (np.arange(nal) + 0.5) * 2 * PI / nal
    wal = 2 * PI / nal
    Ks, wK = nodes_pw(sorted({1e-9, sig / 2, sig, 2 - sig, 2.0, 2 + sig}), nK)
    R0 = 0.0
    Pt = 0.0
    for K, wk in zip(Ks, wK):
        Elo, Ehi = max(2 - sig, K), 2 + sig
        if Ehi <= Elo:
            continue
        Es, wE = nodes_pw(sorted(x for x in ({Elo, 2.0, Ehi} | ({2 - sig + K, 2 + sig - K} if K < sig else set())) if Elo <= x <= Ehi), nE)
        HE = np.zeros((len(Es), nst.shape[0]))
        for iE, E in enumerate(Es):
            # a in [lo,hi], b = E - a in [lo,hi], and triangle |a-b| <= K
            amin = max(lo, E - hi, (E - K) / 2)
            amax = min(hi, E - lo, (E + K) / 2)
            if amax <= amin:
                continue
            A, wA = gl(amin, amax, na)
            B = E - A
            cth = (A ** 2 + K ** 2 - B ** 2) / (2 * A * K)
            cth = np.clip(cth, -1, 1)
            sth = np.sqrt(1 - cth ** 2)
            # k1 vectors (na x nal x 3)
            k1 = np.stack([A[:, None] * sth[:, None] * np.cos(al)[None, :],
                           A[:, None] * sth[:, None] * np.sin(al)[None, :],
                           np.broadcast_to((A * cth)[:, None], (na, nal))], -1)
            k2 = np.array([0, 0, K]) - k1
            s = E * E - K * K
            beta = K / E
            gam = E / math.sqrt(s)
            q0s = math.sqrt(s) / 2
            # boost photon along z
            q1 = np.empty((nst.shape[0], 4))
            q1[:, 0] = gam * (q0s + beta * q0s * nst[:, 2])
            q1[:, 1] = q0s * nst[:, 0]
            q1[:, 2] = q0s * nst[:, 1]
            q1[:, 3] = gam * (q0s * nst[:, 2] + beta * q0s)
            # t = -2 (a q0 - k1.q), u = -2 (b q0 - k2.q)
            t = -2 * (A[:, None, None] * q1[None, None, :, 0] - np.einsum("ijc,oc->ijo", k1, q1[:, 1:]))
            u = -2 * (B[:, None, None] * q1[None, None, :, 0] - np.einsum("ijc,oc->ijo", k2, q1[:, 1:]))
            h = (t ** 2 + u ** 2) / s
            # H = (Theta^2/K) int da dalpha h   (d^3k1 delta(a+b-E) Theta^2 h/(ab) = (ab/K) da dalpha Theta^2 h/(ab))
            HE[iE] = Th2 / K * np.einsum("i,ijo->o", wA, h) * wal
        intH = wE @ HE
        intH2 = wE @ HE ** 2
        R0 += wk * 4 * PI * K * K * (WO @ intH ** 2)
        Pt += wk * 4 * PI * K * K * (WO @ intH2)
    R0 *= 1 / (16384 * PI ** 9)
    Pt *= 1 / (8192 * PI ** 8)
    return R0, Pt


if __name__ == "__main__":
    print("Independent explicit-vector quadrature of B&O's top-hat model (exact kinematics, own prefactor).")
    print("Reference values from taskC1 (exact-kinematics quadrature): sig=0.1: R0 0.0365103, Ptot 0.1526480;  "
          "sig=0.05: 0.0373422, 0.1562180;  narrow-band limits 3/(25pi)=%.7f, 4/25=0.16, ratio 4pi/3=%.5f" % (3 / (25 * PI), 4 * PI / 3))
    for sig in (0.2, 0.1, 0.05):
        for grid in ((28, 20, 16, 12, 10, 8), (40, 28, 22, 16, 12, 10)):
            R0, Pt = run(sig, *grid)
            print(f"  sig/w={sig:4.2f} grid={grid}:  R(0)/(G^2N^2w^3sig^2) = {R0/sig**2:.7f}   "
                  f"P_tot/(G^2N^2w^3sig) = {Pt/sig:.7f}   sig P_tot/R(0) = {sig*Pt/R0:.5f}")
