#!/usr/bin/env python3
"""Task B (2a): the EXACT in-out S-matrix pair probability of B&O's state (no 2 pi delta(0) -> T step), and what it means.

For a free (Pauli-Jordan) coherent background the leading-order pair amplitude is
    A(q1,q2) = int dk1~ dk2~ f(k1) f(k2) M (2pi)^4 delta^4(q1+q2-k1-k2),  dk~ = d3k/((2pi)^3 2k)  (B&O eq. 7 measure)
and the total probability P = (1/2) sum_hel int dq1~ dq2~ |A|^2 is FINITE for any band of nonzero width: the remaining
energy delta function of B&O's S6 is integrated, not replaced by T/(2 pi). Two kernels:

  (i)  B&O's own eq. 7 kernel, A_{mu mu} = 4 pi G (s^2 - 2tu)/s delta_{mu1 mu2} = 2 pi G s (1 + x^2) (x = k^*.q^* in the CM),
       top-hat f = Theta, Theta^2 = 2 pi^2 N/(w sig): gives P_BO(exact). Dividing by their eq. 8 rate gives the effective
       duration T_eff = P_BO(exact) / (dP/dt)_eq8 that their delta(0) -> T step implicitly assumes.
  (ii) a scalar proxy with the validated gravity weight: J = psi^2, P = int d4Q/(2pi)^4 rho(s) |J~(Q)|^2,
       rho(s) = sigma_lin(s) s/2 = (pi/5) G^2 s^2 (taskB_luminosity_check.py), psi carrying the whole N.
Both are compared with the KINETIC (local, in-in) estimate for the same free field: gravitons on radial lines through the
origin, incoming and outgoing shells with passage-time distribution P(t0); head-on in x out collisions give
    P_kin = sigma(4w^2) N^2 int P(t0)^2 dt0 / (2 pi r_c)   (radial integrand ~ 1/r^2, i.e. dominated by the focus r -> r_c),
and r_c,eff is the cutoff that reproduces the exact number. Units: w = 1, G = 1; P quoted as P/(G^2 N^2 w^3 sig).
"""
import math

import numpy as np
from scipy import integrate, special

PI = math.pi
w = 1.0
xg, wg = np.polynomial.legendre.leggauss(64)


def P_toy(sig: float, profile: str) -> tuple[float, float]:
    """Exact P for the proxy (ii) with Theta = 1; returns (P, N)."""
    rho = lambda s: (PI / 5) * s * s

    if profile == "tophat":
        N = w * sig / (4 * PI * PI)

        def inner(d):
            Q0 = 2 * w + d
            a = sig - abs(d)
            f = lambda Q: 4 * PI * Q * Q * rho(Q0 * Q0 - Q * Q) * (min(1.0, a / Q) / (8 * PI)) ** 2 if Q > 0 else 0.0
            v1, _ = integrate.quad(f, 0, min(a, Q0), epsrel=1e-11, limit=200)
            v2, _ = integrate.quad(f, min(a, Q0), Q0, epsrel=1e-11, limit=200)
            return (v1 + v2) / (2 * PI) ** 4
        P, _ = integrate.quad(inner, -sig, sig, epsrel=1e-10, limit=200, points=[0.0])
        return P, N
    N = math.sqrt(PI) * sig * w / (4 * PI * PI)   # (1/4pi^2) int k exp(-(k-w)^2/sig^2) dk, k-range extended

    def inner(d):
        Q0 = 2 * w + d

        def f(Q):
            if Q <= 0:
                return 0.0
            J = (1 / (16 * PI)) * math.exp(-d * d / (4 * sig * sig)) * (2 * sig * math.sqrt(PI) / Q) * special.erf(Q / (2 * sig))
            return 4 * PI * Q * Q * rho(Q0 * Q0 - Q * Q) * J * J
        v, _ = integrate.quad(f, 0, Q0, epsrel=1e-11, limit=400, points=[4 * sig])
        return v / (2 * PI) ** 4
    P, _ = integrate.quad(inner, -8 * sig, 8 * sig, epsrel=1e-10, limit=200)
    return P, N


def P_BO_exact(sig: float) -> float:
    """B&O eq. 7 kernel, top hat, P per N^2 (G = 1), energy delta integrated exactly."""
    Theta2_perN = 2 * PI * PI / (w * sig)       # Theta^2 / N

    def inner(d):
        Q0 = 2 * w + d
        a = sig - abs(d)

        def f(Q):
            if Q <= 0:
                return 0.0
            s = Q0 * Q0 - Q * Q
            c0 = min(1.0, a / Q)
            cb = xg
            sb2 = 1 - cb * cb
            g = 2 * c0 * (1 + sb2 / 2) + (2 * c0 ** 3 / 3) * (cb * cb - sb2 / 2)
            A = 4 * PI * Theta2_perN * (s / 2) / (32 * PI * PI) * 2 * PI * g      # per N
            angq = 2 * PI * np.sum(wg * A * A)                                       # int dOmega_q |A|^2
            return 4 * PI * Q * Q * angq / (32 * PI * PI)
        v1, _ = integrate.quad(f, 0, min(a, Q0), epsrel=1e-11, limit=200)
        v2, _ = integrate.quad(f, min(a, Q0), Q0, epsrel=1e-11, limit=200)
        return (v1 + v2) / (2 * PI) ** 4
    P, _ = integrate.quad(inner, -sig, sig, epsrel=1e-10, limit=200, points=[0.0])
    return P


print("=== exact S-matrix totals for the Pauli-Jordan shell (free field incl. incoming part and focus) ===")
print(" profile  sig/w   P_toy/(G^2N^2w^3sig)   P_BO(exact)/(G^2N^2w^3sig)   T_eff*sig = P_BO/(eq.8)*sig   (4pi/3 = 4.18879)")
for sig in (0.1, 0.05, 0.02, 0.01):
    Pt, N = P_toy(sig, "tophat")
    PBO = P_BO_exact(sig)
    rate8 = 3 * w ** 3 * sig * sig / (25 * PI)      # eq. 8 per G^2 N^2
    print(f" tophat   {sig:5.3f}   {Pt/(N*N*sig):14.6e}          {PBO/sig:14.6e}               {PBO/rate8*sig:10.5f}")
for sig in (0.1, 0.05, 0.02):
    Pt, N = P_toy(sig, "gauss")
    print(f" gauss    {sig:5.3f}   {Pt/(N*N*sig):14.6e}")

print("\n=== kinetic (local in-in) estimate of the same free field: head-on in x out collisions, cut at r_c ===")
sig_cs = (8 * PI / 5) * w * w          # sigma_lin(s = 4 w^2) = (2/5) pi G^2 s
for prof, intP2 in (("tophat", lambda s_: s_ / (3 * PI)), ("gauss", lambda s_: s_ / math.sqrt(2 * PI))):
    for sig in (0.1, 0.05, 0.02):
        Pt, N = P_toy(sig, prof)
        coef = sig_cs * N * N * intP2(sig) / (2 * PI)        # P_kin = coef / r_c
        rc = coef / Pt
        print(f" {prof:6s} sig={sig:5.3f}: P_kin = {coef/(N*N*sig):.5f} G^2N^2w^3sig/(w r_c);  exact proxy needs w r_c,eff = {rc*w:.4f}"
              f"  (lambda = {2*PI:.3f}/w)")

print("\n=== where the kinetic in x out yield sits (top hat, sig = 0.05): fraction of int dr P(t-r)P(t+r)/r^2 from r > R ===")
sig = 0.05
# autocorrelation C(D) = int P(t) P(t + D) dt of the normalised passage-time density P = |D_0|^2/(2 pi sig); its Fourier
# transform is the normalised triangle (1 - |om|/sig), so C(D) = (1/pi) int_0^sig (1 - om/sig)^2 cos(om D) d om.
om = np.linspace(0, sig, 4001)
C = lambda D: np.trapezoid((1 - om / sig) ** 2 * np.cos(np.outer(np.atleast_1d(D), om)), om, axis=1) / PI
print(f"(check: C(0) = int P^2 = {C(0.0)[0]:.6e} vs sig/(3 pi) = {sig/(3*PI):.6e})")
rc = 0.61           # effective cutoff that reproduces the exact top-hat number (table above)
rs = np.concatenate([np.linspace(rc, 60, 6000), np.geomspace(60, 20000, 4000)[1:]])
dens = C(2 * rs) / rs ** 2          # kinetic in x out yield per unit radius (up to constants)
cum = np.concatenate([[0], np.cumsum(0.5 * (dens[1:] + dens[:-1]) * np.diff(rs))])
tot = cum[-1]
for R in (2 * PI, 3 * 2 * PI, 10 * 2 * PI, 1 / sig, 3 / sig):
    i = np.searchsorted(rs, R)
    print(f"  R*w = {R:8.2f} ({R/(2*PI):6.2f} lambda): fraction of kinetic in-out yield from r > R = {1 - cum[i]/tot:.4f}"
          f"   (r_c/R = {rc/R:.4f})")

print("\n=== B&O's 'effective volume' remark, decoded ===")
for eps in (0.1, 0.15):
    lam = 2 * PI
    Veff = 40 * PI * PI / (9 * w * (eps * w) ** 2)
    print(f" eps = {eps}: V_eff = 40 pi^2/(9 w sig^2) = {Veff:.2f}/w^3 = {Veff/lam**3:.2f} lambda^3 (= 5 lambda^3/(9 pi eps^2) ="
          f" {5/(9*PI*eps*eps):.2f} lambda^3) = {Veff*w*(eps*w)**2:.2f} x (1/w)(1/sig)^2")
print(" Reading: eq.8 = (8 pi/15) G^2 (N w)^2 / V_eff, i.e. N gravitons crossing isotropically inside V_eff. In the free field the")
print(" N gravitons sit on a shell of thickness ~1/sig; during the focus (|t| < ~1/sig) a fraction ~ (lambda sig) of them is inside")
print(" a wavelength of the origin crossing at all angles, and (N lambda sig)^2/lambda^3 = N^2 sig^2/lambda reproduces N^2/V_eff with")
print(" V_eff ~ lambda/sig^2: the 'coherence enhancement' IS the geometric focus of the source-free (incoming + outgoing) solution.")
