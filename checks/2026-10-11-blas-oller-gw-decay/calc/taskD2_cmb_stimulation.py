#!/usr/bin/env python3
"""Task D(2): the CMB stimulated-emission factor for g g -> gamma gamma (B&O: W_gamma -> W_gamma (1 + 2 f_gamma(omega_s))).

Claim to test: with two final photons in an isotropic, unpolarised thermal bath of occupation f(q), the net rate of
g g -> gamma gamma minus the inverse gamma gamma -> g g is the vacuum rate times (1 + 2 f(omega_s)).

Derivation (two graviton modes a1, a2, two photon modes b1, b2, energy-conserving coupling V = g(a1 a2 b1+ b2+ + h.c.)):
  d^2<n_b1>/dt^2 |_0 = 2 g^2 <X+X - X X+>,  X = a1 a2 b1+ b2+  (first derivative vanishes for phase-random photons), so
  Delta<n_b1> = (g t)^2 [ N1 N2 (1+f1)(1+f2) - (1+N1)(1+N2) f1 f2 ]
              = (g t)^2 [ N1 N2 (1 + f1 + f2) - f1 f2 (1 + N1 + N2) ]
  for any product state with <n_a1 n_a2> = N1 N2 (coherent OR thermal gravitons).  For N >> 1, f:  N1 N2 (1 + f1 + f2).
  Classical-pump limit (N -> infinity at fixed coupling x amplitude): a two-mode squeeze of a thermal state gives
  Delta<n_1> = sinh^2 r (1 + f1 + f2) exactly (all orders in r).
  -> the correct factor is 1 + f(q1) + f(q2) with q1, q2 the two photon energies; B&O's 1 + 2 f(omega_s) is this at
     q1 = q2 = omega_s.
(a) numerical check of both statements (truncated Fock space, exact evolution);
(b) the average of 1 + f(q1) + f(q2) over (i) B&O's own kinematics (their isotropic narrow-band model, eq. S6 weight)
    and (ii) an incoherent isotropic monochromatic gas with the physical amplitudes, relative to 1 + 2 f(omega_s);
(c) size of the inverse-process correction f1 f2 (1 + N1 + N2) / [N1 N2 (1 + f1 + f2)] for GWs in the CMB.
Usage: python3 taskD2_cmb_stimulation.py [--part a|b|c]
"""
import argparse
import math

import numpy as np
import scipy.sparse as sps
from scipy import constants as K_
from scipy import integrate
from scipy.linalg import expm
from scipy.sparse.linalg import expm_multiply

PI = math.pi
ap = argparse.ArgumentParser()
ap.add_argument("--part", default="all", choices=["a", "b", "c", "all"])
args = ap.parse_args()
run = lambda p: args.part in (p, "all")  # noqa: E731


def hdr(t):
    print("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)


def ann(n):
    return sps.diags(np.sqrt(np.arange(1, n)), 1, format="csr")


def kron(*ops):
    out = ops[0]
    for o in ops[1:]:
        out = sps.kron(out, o, format="csr")
    return out


def coherent(alpha, n):
    v = np.zeros(n, dtype=complex)
    v[0] = 1.0
    for k in range(1, n):
        v[k] = v[k - 1] * alpha / math.sqrt(k)
    return v * math.exp(-abs(alpha) ** 2 / 2)


def thermal_p(f, n):
    k = np.arange(n)
    return (f / (1 + f)) ** k / (1 + f)


if run("a"):
    hdr("(a) exact short-time evolution: Delta<n_b1> vs N1 N2 (1+f1)(1+f2) - (1+N1)(1+N2) f1 f2")
    na, nb = 13, 15
    a, b = ann(na), ann(nb)
    Ia, Ib = sps.identity(na, format="csr"), sps.identity(nb, format="csr")
    A1, A2 = kron(a, Ia, Ib, Ib), kron(Ia, a, Ib, Ib)
    B1, B2 = kron(Ia, Ia, b, Ib), kron(Ia, Ia, Ib, b)
    X = A1 @ A2 @ B1.T @ B2.T
    V = (X + X.T.conj()).tocsr()
    nB1 = (B1.T @ B1).tocsr()
    g, t = 1.0, 2e-3
    for (al1, al2, f1, f2, grav) in ((1.2, 0.9, 0.3, 0.8, "coherent"), (1.0, 1.1, 0.6, 0.2, "coherent"),
                                     (1.2, 0.9, 0.3, 0.8, "thermal")):
        N1, N2 = al1 ** 2, al2 ** 2
        p1, p2 = thermal_p(f1, nb), thermal_p(f2, nb)
        if grav == "coherent":
            gstates = [(1.0, np.kron(coherent(al1, na), coherent(al2, na)))]
        else:  # thermal gravitons: mixture of Fock states
            q1, q2 = thermal_p(N1, na), thermal_p(N2, na)
            gstates = []
            for i in range(na):
                for j in range(na):
                    if q1[i] * q2[j] > 1e-9:
                        v = np.zeros(na * na)
                        v[i * na + j] = 1.0
                        gstates.append((q1[i] * q2[j], v))
        dn, norm = 0.0, 0.0
        for wgt, gv in gstates:
            for i in range(nb):
                for j in range(nb):
                    w = wgt * p1[i] * p2[j]
                    if w < 1e-11:
                        continue
                    ph = np.zeros(nb * nb)
                    ph[i * nb + j] = 1.0
                    psi0 = np.kron(gv, ph).astype(complex)
                    psi = expm_multiply(-1j * g * t * V, psi0)
                    dn += w * (np.vdot(psi, nB1 @ psi).real - i * np.vdot(psi0, psi0).real)
                    norm += w * np.vdot(psi0, psi0).real
        dn /= norm
        if grav == "thermal":   # truncation renormalised: use the truncated moments
            q1, q2 = thermal_p(N1, na), thermal_p(N2, na)
            N1, N2 = float(np.arange(na) @ q1 / q1.sum()), float(np.arange(na) @ q2 / q2.sum())
        exact = (g * t) ** 2 * (N1 * N2 * (1 + f1) * (1 + f2) - (1 + N1) * (1 + N2) * f1 * f2)
        lead = (g * t) ** 2 * N1 * N2 * (1 + f1 + f2)
        bo = (g * t) ** 2 * N1 * N2 * (1 + 2 * 0.5 * (f1 + f2))
        print(f"  {grav:8s} gravitons N=({N1:.3f},{N2:.3f}), photons f=({f1},{f2}): Delta<n_b1>/(g t)^2 = {dn/(g*t)**2:.6f};"
              f" formula = {exact/(g*t)**2:.6f}; N1N2(1+f1+f2) = {lead/(g*t)**2:.6f}; vacuum N1N2 = {N1*N2:.6f}")

    print("\n  classical-pump limit: two-mode squeeze S(r) = exp(r (b1+ b2+ - b1 b2)) of a thermal state (dense, n = 60)")
    n = 60
    bb = ann(n).toarray()
    I = np.eye(n)
    B1, B2 = np.kron(bb, I), np.kron(I, bb)
    for r, f1, f2 in ((0.05, 0.3, 0.8), (0.4, 0.5, 0.5), (0.8, 0.2, 1.1)):
        S = expm(r * (B1.T @ B2.T - B1 @ B2))
        rho0 = np.kron(np.diag(thermal_p(f1, n)), np.diag(thermal_p(f2, n)))
        rho = S @ rho0 @ S.T
        n1 = np.trace(rho @ (B1.T @ B1)).real
        print(f"   r={r}, f=({f1},{f2}): Delta<n1> = {n1 - f1:.8f};  sinh^2 r (1 + f1 + f2) = {math.sinh(r)**2*(1+f1+f2):.8f}")

if run("b"):
    hdr("(b) average of 1 + f(q1) + f(q2) over the photon energies, relative to B&O's 1 + 2 f(omega_s)")
    print("  (i) B&O's isotropic narrow-band model: pair momentum K = 2 w x, photon CM polar angle c (w.r.t. K);")
    print("      eq. S6 integrand ~ dK s^2 (2 + sin^2 theta)^2 (ring volumes 2 pi (w sigma)^2/K each), s = 4w^2(1 - x^2);")
    print("      lab photon energies q = w (1 +- x c).  Check of this weight: its normalisation reproduces 3/(25 pi):")
    J, _ = integrate.dblquad(lambda c, x: (1 - x * x) ** 2 * (3 - c * c) ** 2, 0, 1, -1, 1)
    # P/T = G^2 Theta^4 sigma^4/(16384 pi^9) * 4 pi int dK * 2 pi int dc [ (pi s/2)(2 + sin^2) ]^2 ; Theta^2 = 2 pi^2 N/(w sigma)
    coef = 4 * PI ** 4 / (16384 * PI ** 9) * 4 * PI * 2 * PI * (PI / 2) ** 2 * 16 * 2 * J   # x (2w)^... see below
    # int dK s^2 = int 2w dx 16 w^4 (1-x^2)^2 -> 32 w^5 ; collect: coefficient of G^2 N^2 w^3 sigma^2
    coef = (4 * PI ** 4) / (16384 * PI ** 9) * 4 * PI * 2 * PI * (PI / 2) ** 2 * 32 * J
    print(f"      coefficient from this weight = {coef:.12f};  3/(25 pi) = {3/(25*PI):.12f}")

    def fB(y):
        return 1.0 / np.expm1(y) if y > 1e-300 else np.inf

    def avg_BO(wT):
        num, _ = integrate.dblquad(lambda c, x: (1 - x * x) ** 2 * (3 - c * c) ** 2 *
                                   (1 + fB(wT * (1 + x * c)) + fB(wT * (1 - x * c))), 0, 1, -1, 1,
                                   epsabs=1e-13, epsrel=1e-10)
        return num / J

    def rj_BO():
        num, _ = integrate.dblquad(lambda c, x: (1 - x * x) ** 2 * (3 - c * c) ** 2 / (1 - x * x * c * c), 0, 1, -1, 1,
                                   epsabs=1e-13, epsrel=1e-11)
        return num / J

    print(f"      Rayleigh-Jeans limit: <f(q1)+f(q2)>/(2 f(w)) = <1/(1 - x^2 c^2)> = {rj_BO():.6f}")
    for wT in (1e-4, 1e-2, 0.3, 1.0, 3.0, 10.0):
        aBO = avg_BO(wT)
        print(f"      w/T = {wT:7.0e}: <1 + f1 + f2> = {aBO:.6e};  1 + 2 f(w) = {1 + 2 * fB(wT):.6e};  ratio = {aBO/(1+2*fB(wT)):.6f}")

    print("  (ii) incoherent isotropic monochromatic gas, physical amplitudes: pair weight ~ sigma v ~ (1 - c12)^2,")
    print("       boost beta = cos(theta12/2), CM photon distribution ~ (1 - cos g)^4 + (1 + cos g)^4 about the graviton")
    print("       axis (perpendicular to K), cos g = sin chi cos phi; q = w (1 +- beta cos chi).")
    rng = np.random.default_rng(3)
    nmc = 4_000_000
    c12 = rng.uniform(-1, 1, nmc)
    cx = rng.uniform(-1, 1, nmc)
    phi = rng.uniform(0, 2 * PI, nmc)
    beta = np.sqrt((1 + c12) / 2)
    cg = np.sqrt(1 - cx * cx) * np.cos(phi)
    wgt = (1 - c12) ** 2 * ((1 - cg) ** 4 + (1 + cg) ** 4)
    rj = np.sum(wgt / (1 - beta ** 2 * cx ** 2)) / np.sum(wgt)
    sem = np.std(wgt / (1 - beta ** 2 * cx ** 2)) / np.mean(wgt) / math.sqrt(nmc)
    print(f"       Rayleigh-Jeans: <f(q1)+f(q2)>/(2 f(w)) = {rj:.4f} +- {sem:.4f}")
    for wT in (1e-2, 1.0, 3.0):
        q1, q2 = wT * (1 + beta * cx), wT * (1 - beta * cx)
        val = np.sum(wgt * (1 + 1 / np.expm1(q1) + 1 / np.expm1(q2))) / np.sum(wgt)
        print(f"       w/T = {wT:5.0e}: <1 + f1 + f2>/(1 + 2 f(w)) = {val/(1+2/math.expm1(wT)):.4f}")

if run("c"):
    hdr("(c) inverse-process correction f1 f2 (1 + N1 + N2)/[N1 N2 (1 + f1 + f2)] ~ f/N")
    hb, kB, T0, c = K_.hbar, K_.k, 2.7255, K_.c
    Msun = 1.98892e30
    for name, nu, E_J, R_m in (("GW150914 merger (E ~ 3 Msun c^2, nu ~ 150 Hz)", 150.0, 3 * Msun * c ** 2, 2 * K_.G * 65 * Msun / c ** 2),):
        w = 2 * PI * nu
        N0 = E_J / (hb * w)
        fg = 2 * PI * N0 / max(w * R_m / c, 1.0) ** 2      # phase-space density (Liouville), diffraction-limited source
        fgam = 1 / math.expm1(hb * w / (kB * T0))
        print(f"  {name}: N0 = {N0:.2e}; graviton phase-space occupation ~ 2 pi N0/max(w R, 1)^2 = {fg:.1e};"
              f" CMB f(150 Hz) = {fgam:.2e}; correction ~ f/N = {fgam/fg:.1e}")
    print("  (estimate: phase-space density conserved along rays; emission region ~ max(R_source, 1/omega))")
