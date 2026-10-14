"""falsifier-C3-0: l = 2 contact toy, retarded yield from beyond radius R (smooth window), relative to the
whole-space time-symmetric (Pauli-Jordan) yield with the same late-time wave. Natural units, omega = 1, r in 1/k.
Window W_R(r) = compact quintic smoothstep rising over [R - 2D, R + 2D], D = R/8 (a tanh ramp leaks the r^-6 near zone of l = 2), applied to the source j = phi^2.
Also repeats the l = 0 case for comparison with M-EXAMINER-04 (F(wR=1..5) = 0.60, 0.21, 0.030 for p = 2, D = R/8;
note M-EXAMINER-04 normalises to the whole-space RETARDED yield, here we normalise to the whole-space PJ yield).
"""
import sys
import numpy as np
from scipy.special import spherical_jn, spherical_yn
from numpy.polynomial.legendre import leggauss, legval

Q0 = 2.0

def coeffs(l):
    x, w = leggauss(40)
    Pl = legval(x, [0] * l + [1])
    return {L: (2 * L + 1) / 2 * np.sum(w * Pl ** 2 * legval(x, [0] * L + [1])) for L in range(0, 2 * l + 1, 2)}

def rate(l, state, p, eps, R=None, nq=120):
    rmax = 25.0 / eps
    r_in = np.linspace(1e-6, 2.5, 40001)
    r_out = np.linspace(2.5, rmax, int((rmax - 2.5) / 0.04) + 1)[1:]
    r = np.concatenate([r_in, r_out])
    if state == "PJ":
        A = 2j * spherical_jn(l, r)
    else:
        A = spherical_jn(l, r) + 1j * spherical_yn(l, r)
    j = A ** 2 * np.exp(-eps * r)
    if R is not None:
        D = R / 8.0
        x = np.clip((r - (R - 2 * D)) / (4 * D), 0.0, 1.0)  # compact C2 quintic ramp over [0.75R, 1.25R]
        j = j * (x ** 3 * (10 - 15 * x + 6 * x ** 2))
    u, wu = leggauss(nq)
    s = 0.5 * (u + 1)
    q = Q0 * (1 - (1 - s) ** 2)
    dq = Q0 * 2 * (1 - s) * 0.5 * wu
    tot = 0.0
    for qi, dqi in zip(q, dq):
        acc = 0.0
        for L, cL in coeffs(l).items():
            IL = np.trapezoid(r ** 2 * j * spherical_jn(L, qi * r), r)
            acc += cL ** 2 * (4 * np.pi) ** 3 / (2 * L + 1) * abs(IL) ** 2
        tot += dqi * qi ** 2 * (Q0 ** 2 - qi ** 2) ** p * acc
    return tot

eps = 0.01
for l in (0, 2):
    for p in (0, 2):
        pj = rate(l, "PJ", p, eps)
        vals = []
        for R in (1.0, 2.0, 5.0):
            vals.append(rate(l, "ret", p, eps, R=R) / pj)
        print(f"l = {l}, p = {p}: retarded yield beyond kR = 1, 2, 5 / whole-space PJ yield = "
              + ", ".join(f"{v:.3g}" for v in vals))
        sys.stdout.flush()
