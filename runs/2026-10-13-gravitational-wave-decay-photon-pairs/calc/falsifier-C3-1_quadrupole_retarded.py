"""falsifier-C3-1: does the retarded (outgoing) field yield 'substantially less' than the time-symmetric
(Pauli-Jordan) field once the multipole is l = 2 (quadrupole) instead of the examiner's l = 0 monopole?

Natural units, c = 1, k = w = 1 (lengths in units of c/w = lambda/2pi). Dimensionless toy, same method as
M-EXAMINER-03 (scalar field, source j = psi^2, yield Y = Int d^4q theta(q0) theta(q^2) (q^2)^p |J(q)|^2), but
monochromatic (yield per unit time) and with angular structure.

psi(t, x) = Re[F(r) e^{-i t}] P_l(cos th).
  retarded (outgoing only):         F_ret = h_l^(1)(r) = j_l + i y_l
  time-symmetric, same outgoing part: F_sym = 2 j_l   (= h_l + conj h_l)
Sum-frequency part of psi^2: (1/4) F^2 P_l^2 e^{-2it}, so q0 = 2.
P_l^2 = sum_L c_L P_L. Plane-wave expansion gives
  Int dOmega_q |J|^2 = sum_L c_L^2 (4 pi)^2 (4 pi/(2L+1)) |I_L(q)|^2,  I_L(q) = Int_0^inf r^2 W(r) F(r)^2 j_L(q r) dr
  Y_p = Int_0^2 q^2 dq (4 - q^2)^p Int dOmega_q |J|^2      (common constants cancel in ratios)
W(r) = 1 - exp(-(r/a)^8): excises r < a, the region where a free field does not describe a real source
(source size). This *removes* near-zone contributions, so it is conservative for the retarded field.
Convergence factor exp(-eps r) for the oscillatory tail; eps varied to check convergence.
Validation: l = 0 must reproduce M-EXAMINER-03's 1/12 (p = 0) and 0.0200 (p = 2) as a -> 0."""
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import time

t0 = time.time()

def coeffs(l):
    # P_l^2 = sum c_L P_L, via Gauss-Legendre projection
    x, w = np.polynomial.legendre.leggauss(40)
    Pl = np.polynomial.legendre.legval(x, [0] * l + [1])
    out = {}
    for L in range(0, 2 * l + 1, 2):
        PL = np.polynomial.legendre.legval(x, [0] * L + [1])
        out[L] = (2 * L + 1) / 2 * np.sum(w * Pl * Pl * PL)
    return out

def rgrid(a, eps):
    rmin = max(a / 6, 1e-4) if a > 0 else 1e-4
    r1 = np.geomspace(rmin, 4.0, 40000)
    rmax = 14.0 / eps
    r2 = np.arange(4.0, rmax, 0.01)[1:]
    return np.concatenate([r1, r2])

def yields(l, a, eps, nq=160):
    r = rgrid(a, eps)
    W = (1 - np.exp(-(r / a) ** 8)) if a > 0 else np.ones_like(r)
    damp = np.exp(-eps * r)
    jl = spherical_jn(l, r); yl = spherical_yn(l, r)
    Fret2 = (jl + 1j * yl) ** 2
    Fsym2 = (2 * jl) ** 2
    cL = coeffs(l)
    # q grid: Gauss-Legendre on (0, 2)
    xq, wq = np.polynomial.legendre.leggauss(nq)
    q = 1.0 + xq; wq = wq
    dr = np.gradient(r)
    S = {"ret": np.zeros(nq), "sym": np.zeros(nq)}
    for L, c in cL.items():
        if abs(c) < 1e-14:
            continue
        for iq, qq in enumerate(q):
            jL = spherical_jn(L, qq * r)
            base = r ** 2 * W * damp * jL * dr
            Ir = np.sum(base * Fret2)
            Is = np.sum(base * Fsym2)
            pref = c ** 2 * (4 * np.pi) ** 3 / (2 * L + 1)
            S["ret"][iq] += pref * abs(Ir) ** 2
            S["sym"][iq] += pref * abs(Is) ** 2
    out = {}
    for p in (0, 2):
        wt = wq * q ** 2 * (4 - q ** 2) ** p
        out[p] = (np.sum(wt * S["ret"]), np.sum(wt * S["sym"]))
    return out

print("Validation, l = 0 (examiner monopole): expect ret/sym = 1/12 = 0.0833 (p=0), 0.0200 (p=2)")
for eps in (0.004, 0.002):
    y = yields(0, 0.0, eps)
    print(f"  eps={eps}: p=0 ret/sym = {y[0][0]/y[0][1]:.4f};  p=2 ret/sym = {y[2][0]/y[2][1]:.4f}")
print(f"[time {time.time()-t0:.0f}s]")

print("\nl = 2 (quadrupole), excision radius a in units of c/w; ratio = Y_ret / Y_sym (yield per unit time,")
print("same outgoing luminosity). Y_sym also excised at the same a.")
print(" k a   | p=0 ret/sym | p=2 ret/sym | (p=2: Y_ret, Y_sym raw)")
for a in (3.0, 2.0, 1.5, 1.0, 0.7, 0.5, 0.3, 0.2):
    y = yields(2, a, 0.003)
    print(f" {a:4.2f}  | {y[0][0]/y[0][1]:11.4g} | {y[2][0]/y[2][1]:11.4g} | {y[2][0]:.4g}, {y[2][1]:.4g}")
print(f"[time {time.time()-t0:.0f}s]")
print("\nconvergence check at k a = 1.0 and 0.5, eps = 0.0015:")
for a in (1.0, 0.5):
    y = yields(2, a, 0.0015)
    print(f"  a={a}: p=0 {y[0][0]/y[0][1]:.4g}; p=2 {y[2][0]/y[2][1]:.4g}")
print(f"[time {time.time()-t0:.0f}s]")
