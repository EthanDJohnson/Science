#!/usr/bin/env python3
"""Task C(1), independent route: plain Monte Carlo of B&O's S6 in the ORIGINAL momentum variables (k1, k2, k1'), with the
energy delta function integrated exactly (no ring parameterisation, no analytic D/alpha integrals, no narrow-band step).

    P_tot = C0 int d^3k1 d^3k2 d^3k1' chi chi chi' chi'' Theta^4/(a b a' b') 2 pi delta(E - E') Psi,      k2' = K - k1'
    Psi   = int dOmega_gam h h' ,  h = (s/2)(1 + (n.x)^2),  h' = (s'/2)(1 + (m.x)^2)  =>  Psi = (2 pi s s'/15)(13 + (n.m)^2)
          (n, m: CM directions of k1 and k1' about K;  int (n.x)^2 (m.x)^2 dOmega = (4 pi/15)(1 + 2 (n.m)^2)).
    delta(E - E'): for a direction n' of k1', E' = a' + |K - a' n'| is monotonic in a', root a' = (E^2-K^2)/(2(E - n'.K)),
    Jacobian d^3k1' delta(.) = a'^2 dOmega'/|1 - n'.k2'/b'|.
B&O's replacement 2 pi delta(0) -> T (their dP/dt) is the same integral WITHOUT the delta and the 2 pi, k1' anywhere in the
shell:  R(0) = C0 int d^3k1 d^3k2 d^3k1' chi... Theta^4/(a b a' b') Psi.
C0 = G^2/(16384 pi^9), Theta^2 = 2 pi^2 N/(w sig).  Units w = G = N = 1.  Compare with taskC1 (quadrature) and the narrow-band
limits R(0) -> 3/(25 pi) sig^2, P_tot -> (4/25) sig.
"""
import math
import sys

import numpy as np

PI = math.pi
C0 = 1.0 / (16384 * PI ** 9)


def shell_sample(rng, n, sig):
    lo, hi = 1 - sig / 2, 1 + sig / 2
    r = (rng.uniform(lo ** 3, hi ** 3, n)) ** (1 / 3)
    v = rng.normal(size=(n, 3))
    v /= np.linalg.norm(v, axis=1)[:, None]
    return v * r[:, None]


def unit(n, rng):
    v = rng.normal(size=(n, 3))
    return v / np.linalg.norm(v, axis=1)[:, None]


def cm_dir(k, Kv, E):
    """CM direction of k (energy |k|) for total momentum Kv, energy E (boost along Kv)."""
    Kn = np.linalg.norm(Kv, axis=1)
    Kh = Kv / Kn[:, None]
    beta = Kn / E
    gam = 1 / np.sqrt(1 - beta ** 2)
    kn = np.linalg.norm(k, axis=1)
    kpar = np.sum(k * Kh, axis=1)
    kperp = k - kpar[:, None] * Kh
    kpar_s = gam * (kpar - beta * kn)
    v = kperp + kpar_s[:, None] * Kh
    return v / np.linalg.norm(v, axis=1)[:, None]


def run(sig, nsamp, chunk=1_000_000, seed=1):
    rng = np.random.default_rng(seed)
    lo, hi = 1 - sig / 2, 1 + sig / 2
    Vsh = 4 * PI * (hi ** 3 - lo ** 3) / 3
    Th4 = (2 * PI ** 2 / sig) ** 2
    accP, accP2, accR, accR2, n_tot = 0.0, 0.0, 0.0, 0.0, 0
    while n_tot < nsamp:
        n = min(chunk, nsamp - n_tot)
        k1 = shell_sample(rng, n, sig)
        k2 = shell_sample(rng, n, sig)
        a = np.linalg.norm(k1, axis=1)
        b = np.linalg.norm(k2, axis=1)
        Kv = k1 + k2
        E = a + b
        K2 = np.sum(Kv * Kv, axis=1)
        s = E * E - K2
        ok = s > 1e-12
        nvec = cm_dir(k1, Kv, E)
        # --- exact energy delta: k1' direction uniform, |k1'| fixed by E' = E
        npr = unit(n, rng)
        nK = np.sum(npr * Kv, axis=1)
        ap = s / (2 * (E - nK))
        k1p = ap[:, None] * npr
        k2p = Kv - k1p
        bp = np.linalg.norm(k2p, axis=1)
        gp = 1 - np.sum(npr * k2p, axis=1) / bp
        inb = (ap >= lo) & (ap <= hi) & (bp >= lo) & (bp <= hi) & ok
        m = cm_dir(k1p, Kv, E)
        Psi = (2 * PI * s * s / 15) * (13 + np.sum(nvec * m, axis=1) ** 2)
        fP = np.where(inb, ap ** 2 / gp * Th4 / (a * b * ap * bp) * 2 * PI * Psi, 0.0) * 4 * PI
        # --- B&O's replacement: k1' anywhere in the shell, no delta
        k1q = shell_sample(rng, n, sig)
        k2q = Kv - k1q
        aq = np.linalg.norm(k1q, axis=1)
        bq = np.linalg.norm(k2q, axis=1)
        Eq = aq + bq
        sq = Eq * Eq - K2
        inq = (bq >= lo) & (bq <= hi) & ok & (sq > 1e-12)
        mq = cm_dir(k1q, Kv, np.where(inq, Eq, E + 1.0))
        PsiR = (2 * PI * s * sq / 15) * (13 + np.sum(nvec * mq, axis=1) ** 2)
        fR = np.where(inq, Th4 / (a * b * aq * bq) * PsiR, 0.0) * Vsh
        accP += fP.sum()
        accP2 += (fP * fP).sum()
        accR += fR.sum()
        accR2 += (fR * fR).sum()
        n_tot += n
    mP = accP / n_tot
    eP = math.sqrt(max(accP2 / n_tot - mP * mP, 0) / n_tot)
    mR = accR / n_tot
    eR = math.sqrt(max(accR2 / n_tot - mR * mR, 0) / n_tot)
    norm = C0 * Vsh * Vsh
    return norm * mP, norm * eP, norm * mR, norm * eR


if __name__ == "__main__":
    nsamp = int(float(sys.argv[1])) if len(sys.argv) > 1 else 40_000_000
    print(f"Monte Carlo, {nsamp:.1e} samples per sigma (statistical 1-sigma errors shown)")
    print("columns: P_tot/(G^2N^2w^3 sig)  [taskC1 quadrature; limit 0.16]     R(0)/(G^2N^2w^3sig^2) [taskC1; limit 3/(25pi)=0.0381972]")
    ref = {0.2: (0.1461332, 0.0349178), 0.1: (0.1526480, 0.0365103), 0.05: (0.1562180, 0.0373422)}
    for sig in (0.2, 0.1, 0.05):
        P, eP, R, eR = run(sig, nsamp, seed=int(1000 * sig))
        print(f"   sig/w = {sig:4.2f}:  P_tot coeff = {P/sig:.5f} +- {eP/sig:.5f}  [{ref[sig][0]:.5f}]    "
              f"R(0) coeff = {R/sig**2:.6f} +- {eR/sig**2:.6f}  [{ref[sig][1]:.6f}]    sig P_tot/R(0) = {sig*P/R:.3f}")
