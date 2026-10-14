"""falsifier-C3-0: does the 'retarded yields less' ratio of the scalar toy survive for an l = 2 (quadrupole) field?

Natural units (hbar = c = 1), omega = 1, so r is measured in units of 1/k = lambda/2pi. Dimensionless toy.

Same toy as M-EXAMINER-03 (contact vertex j = phi^2, massless pair, two-body phase space constant), but
monochromatic and with angular structure:
  phi = Re[ A(x) e^{-i w t} ],  A = R(r) P_l(cos theta)   (m = 0 multipole)
  sum-frequency (q0 = 2w) source component: A^2 / 2.
  pair rate  ∝  Int_{|q|<q0} d^3q (q0^2 - q^2)^p |J(q)|^2,   J(q) = FT_x[A^2](q).
  With P_l^2 = sum_L c_L P_L:
     J(q) = sum_L c_L 4 pi (-i)^L P_L(cos th_q) I_L(q),   I_L(q) = Int_0^inf r^2 R(r)^2 j_L(q r) dr
     Int d^3q |J|^2 (...) = Int q^2 dq (...) sum_L c_L^2 (4 pi)^2 (4 pi/(2L+1)) |I_L(q)|^2.
States, both with the SAME late-time outgoing wave h_l^(1)(kr) P_l (same luminosity, same N per unit time):
  retarded (real source):        R_ret = h_l^(1)(r)       outside the source radius a;
                                 inside r < a: regular continuation R_ret(a) (r/a)^l  (extended source), or a hole (R = 0)
  time-symmetric (Pauli-Jordan): R_PJ  = h^(1) - h^(2) = 2 i j_l(r)   (free, regular everywhere)
Check: l = 0, a -> 0 must give ret/PJ = 1/12 (p = 0) and 0.020 (p = 2) [M-EXAMINER-03].
Conditionally convergent r-integrals are regulated with exp(-eps r) and checked for eps -> 0.
"""
import numpy as np
from scipy.special import spherical_jn, spherical_yn
from numpy.polynomial.legendre import leggauss

Q0 = 2.0

def legendre_square_coeffs(l):
    # coefficients c_L of P_l(x)^2 = sum_L c_L P_L(x), by Gauss-Legendre projection
    x, w = leggauss(40)
    from numpy.polynomial.legendre import legval
    Pl = legval(x, [0] * l + [1])
    out = {}
    for L in range(0, 2 * l + 1, 2):
        PL = legval(x, [0] * L + [1])
        out[L] = (2 * L + 1) / 2 * np.sum(w * Pl ** 2 * PL)
    return out

def radial(l, r, state, a, interior):
    if state == "PJ":
        return 2j * spherical_jn(l, r)
    R = spherical_jn(l, r) + 1j * spherical_yn(l, np.maximum(r, 1e-12))
    if a > 0:
        ra = spherical_jn(l, a) + 1j * spherical_yn(l, a)
        inside = r < a
        if interior == "regular":
            R = np.where(inside, ra * (r / a) ** l, R)
        else:  # hole
            R = np.where(inside, 0.0, R)
    return R

def rate(l, state, a, p, eps, interior="regular", rmax=None, nq=120):
    if rmax is None:
        rmax = 25.0 / eps
    # radial grid: fine near the source, uniform outside
    r_in = np.linspace(1e-6, max(a, 1e-6) * 4 + 2.0, 40001)
    r_out = np.linspace(r_in[-1], rmax, int((rmax - r_in[-1]) / 0.04) + 1)[1:]
    r = np.concatenate([r_in, r_out])
    R2 = radial(l, r, state, a, interior) ** 2 * np.exp(-eps * r)
    coeffs = legendre_square_coeffs(l)
    # q grid: Gauss-Legendre on (0, Q0) after substitution concentrating near Q0 (log-type peak for ret)
    u, wu = leggauss(nq)
    s = 0.5 * (u + 1)              # s in (0,1)
    q = Q0 * (1 - (1 - s) ** 2)     # cluster near Q0
    dq = Q0 * 2 * (1 - s) * 0.5 * wu
    tot = 0.0
    for qi, dqi in zip(q, dq):
        acc = 0.0
        for L, cL in coeffs.items():
            if abs(cL) < 1e-14:
                continue
            integrand = r ** 2 * R2 * spherical_jn(L, qi * r)
            IL = np.trapezoid(integrand, r)
            acc += cL ** 2 * (4 * np.pi) ** 2 * (4 * np.pi / (2 * L + 1)) * abs(IL) ** 2
        tot += dqi * qi ** 2 * (Q0 ** 2 - qi ** 2) ** p * acc
    return tot

if __name__ == "__main__":
    import time
    t0 = time.time()
    print("== check: monopole l = 0, a = 0.01 (regular interior); expect 1/12 = 0.08333 (p=0), 0.0200 (p=2)")
    for eps in (0.02, 0.01):
        for p in (0, 2):
            rr = rate(0, "ret", 0.01, p, eps) / rate(0, "PJ", 0.0, p, eps)
            print(f"  eps = {eps}: p = {p}: ret/PJ = {rr:.4f}")
    print(f"  [time {time.time()-t0:.0f} s]")
    eps = 0.01
    for l in (1, 2):
        print(f"== l = {l}: ratio ret/PJ of whole-space pair rate vs source radius a (units 1/k), eps = {eps}")
        PJ0 = rate(l, "PJ", 0.0, 0, eps)
        PJ2 = rate(l, "PJ", 0.0, 2, eps)
        for a in (1.0, 0.7, 0.5, 0.3, 0.2, 0.1):
            r0 = rate(l, "ret", a, 0, eps) / PJ0
            r2 = rate(l, "ret", a, 2, eps) / PJ2
            h0 = rate(l, "ret", a, 0, eps, interior="hole") / PJ0
            print(f"  ka = {a:4.2f}: p=0 ret/PJ = {r0:10.4g}  (hole interior {h0:10.4g});  p=2 ret/PJ = {r2:10.4g}")
        print(f"  [time {time.time()-t0:.0f} s]")
    # eps convergence spot-check for l = 2
    print("== eps convergence, l = 2, ka = 0.3 and 1.0, p = 0")
    for a in (0.3, 1.0):
        for e in (0.02, 0.01, 0.005):
            print(f"  ka = {a}, eps = {e}: ret/PJ = {rate(2, 'ret', a, 0, e) / rate(2, 'PJ', 0.0, 0, e):.4g}")
    print(f"  [time {time.time()-t0:.0f} s]")
