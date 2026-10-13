#!/usr/bin/env python3
"""Task D(3): B&O supplementary SA -- 'coherent intermediate gravitons drop out'.

B&O's claim: <f|T h(x) h(y)|f> = h_c(x) h_c(y) + <0|T h h|0>; the classical piece h_c(x) h_c(y) in the internal
graviton line of the s-channel diagram (three-graviton vertex at y, graviton-photon-photon vertex at x) carries an
ON-SHELL momentum K (K^2 = s = 0), forcing collinear kinematics, where the vertex/amplitude vanishes.

Checks:
 (a) displacement identity for a free field mode: <alpha|T x(t1) x(t2)|alpha> - x_c(t1) x_c(t2) = <0|T x x|0>
     (truncated Fock space, exact numerics) -- holds for ANY coherent state of a free field;
 (b) the classical piece factorises: [ int d^4y V3(h_c, h_c, h_c) ] x [ int d^4x h_c T_EM ] with no propagator,
     i.e. it is (classical cubic action, a c-number) x (first-order single-graviton -> gamma gamma amplitude).
     Momentum support: k1 + k2 = K, all null. The phase-space measure of this collinear set is NOT zero
     (int dOmega delta(|k1|+|k2|-|k1+k2|) is finite), so the cancellation must come from the vertices:
 (b1) <gamma(q1 e1) gamma(q2 e2)| T^{mu nu} |0> eps_{mu nu} = 0 for q1, q2 parallel to k and TT eps (numerical, random);
 (b2) on-shell 3-graviton amplitude for collinear real momenta: every Lorentz invariant k_i.k_j and eps_i.k_j
      vanishes (the vertex has two derivatives and is built from these and eps_i.eps_j) -> 0;
      spinor-helicity: all <ij>, [ij] vanish for collinear real momenta.
 (c) module (qft_second_order, full amplitude incl. s-channel pole): |M|/(8 pi G s) stays <= 1 as the incoming
     gravitons become collinear (s -> 0 at fixed energies): the 2 -> 2 amplitude itself -> 0 like s.
Usage: python3 taskD3_SA_coherent_intermediate.py
"""
import math
import os
import sys

import numpy as np
from scipy.linalg import expm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"))
import qft_second_order as q2  # noqa: E402

PI = math.pi
rng = np.random.default_rng(11)


def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


hdr("(a) displacement identity, single oscillator mode (w = 1), truncated Fock space n = 80")
n = 80
a = np.diag(np.sqrt(np.arange(1, n)), 1).astype(complex)
x = (a + a.conj().T) / math.sqrt(2)
H = a.conj().T @ a


def xH(t):
    U = expm(1j * H * t)
    return U @ x @ U.conj().T


def coh(al):
    v = np.zeros(n, complex)
    v[0] = 1
    for k in range(1, n):
        v[k] = v[k - 1] * al / math.sqrt(k)
    return v * math.exp(-abs(al) ** 2 / 2)


vac = coh(0)
for al in (1.3 + 0.4j, -0.7 + 2.0j):
    st = coh(al)
    for t1, t2 in ((0.3, 1.7), (2.1, 0.4)):
        X1, X2 = xH(t1), xH(t2)
        T = X1 @ X2 if t1 > t2 else X2 @ X1
        lhs = st.conj() @ T @ st
        xc1, xc2 = (st.conj() @ X1 @ st), (st.conj() @ X2 @ st)
        vac_part = vac.conj() @ T @ vac
        print(f"  alpha={al}, (t1,t2)=({t1},{t2}): <a|T x x|a> - x_c x_c = {lhs - xc1*xc2:.10f};  <0|T x x|0> = {vac_part:.10f}")

hdr("(b) collinear support: int dOmega_12 delta(|k1|+|k2|-|k1+k2|) is finite (not a measure-zero cancellation)")
for k1, k2 in ((1.0, 1.0), (0.7, 1.3)):
    # g(c) = k1 + k2 - sqrt(k1^2 + k2^2 + 2 k1 k2 c), root at c = 1 (endpoint); |dg/dc| there = k1 k2/(k1+k2)
    slope = k1 * k2 / (k1 + k2)
    # numerical: Gaussian-regularised delta, one-sided at the endpoint
    for w in (1e-3, 1e-4):
        c = np.linspace(-1, 1, 2_000_001)
        g = k1 + k2 - np.sqrt(k1 * k1 + k2 * k2 + 2 * k1 * k2 * c)
        d = np.exp(-g ** 2 / (2 * w * w)) / math.sqrt(2 * PI) / w
        val = 2 * PI * np.trapezoid(d, c)
        print(f"  k1={k1}, k2={k2}, width={w:g}: 2 pi int dc delta_w(g) = {val:.6f};  one-sided 2 pi (k1+k2)/(2 k1 k2) = {PI/slope:.6f}")

hdr("(b1) single on-shell graviton -> two collinear photons: eps_{mu nu} <gamma gamma|T^{mu nu}|0> = 0")
eta = np.diag([1.0, -1, -1, -1])


def F(q, e):
    return np.outer(q, e) - np.outer(e, q)   # upper indices F^{mu nu}


worst, ref = 0.0, 0.0
for trial in range(200):
    nhat = rng.normal(size=3); nhat /= np.linalg.norm(nhat)
    k = np.concatenate(([1.0], nhat))
    A, B = rng.uniform(0.1, 0.9), None
    q1, q2v = A * k, (1 - A) * k
    # transverse basis
    u = np.cross(nhat, rng.normal(size=3)); u /= np.linalg.norm(u)
    v = np.cross(nhat, u)
    e1 = np.concatenate(([0.0], np.cos(r := rng.uniform(0, PI)) * u + np.sin(r) * v))
    e2 = np.concatenate(([0.0], np.cos(r2 := rng.uniform(0, PI)) * u + np.sin(r2) * v))
    # TT graviton polarisation (upper), random combination of plus/cross
    ep = np.zeros((4, 4)); ep[1:, 1:] = np.outer(u, u) - np.outer(v, v)
    ex = np.zeros((4, 4)); ex[1:, 1:] = np.outer(u, v) + np.outer(v, u)
    eps = rng.normal() * ep + rng.normal() * ex
    F1, F2 = F(q1, e1), F(q2v, e2)
    # T^{mu nu} bilinear: F1^{mu a} F2^{nu}_a + (1<->2) - (1/2) eta^{mu nu} F1^{ab} F2_{ab}
    F2low = eta @ F2 @ eta
    F1low = eta @ F1 @ eta
    T = F1 @ eta @ F2.T + F2 @ eta @ F1.T - 0.5 * np.linalg.inv(eta) * np.sum(F1 * F2low)
    epsl = eta @ eps @ eta
    worst = max(worst, abs(np.sum(epsl * T)))
    # non-collinear control: rotate q2 off-axis
    m3 = rng.normal(size=3); m3 /= np.linalg.norm(m3)
    q2c = (1 - A) * np.concatenate(([1.0], m3))
    e2c3 = np.cross(m3, rng.normal(size=3)); e2c3 /= np.linalg.norm(e2c3)
    F2c = F(q2c, np.concatenate(([0.0], e2c3)))
    Tc = F1 @ eta @ F2c.T + F2c @ eta @ F1.T - 0.5 * np.linalg.inv(eta) * np.sum(F1 * (eta @ F2c @ eta))
    ref = max(ref, abs(np.sum(epsl * Tc)))
print(f"  200 random collinear configurations: max |eps.T| = {worst:.2e}   (non-collinear control, same eps: max {ref:.2e})")

hdr("(b2) on-shell 3-graviton kinematics for collinear real momenta: all building blocks vanish")
worst_kk, worst_ek, worst_br = 0.0, 0.0, 0.0
for trial in range(200):
    nhat = rng.normal(size=3); nhat /= np.linalg.norm(nhat)
    lam = rng.uniform(0.2, 2.0, 3)
    ks = [l * np.concatenate(([1.0], nhat)) for l in lam]
    u = np.cross(nhat, rng.normal(size=3)); u /= np.linalg.norm(u)
    v = np.cross(nhat, u)
    for i in range(3):
        for j in range(3):
            worst_kk = max(worst_kk, abs(ks[i] @ eta @ ks[j]))
            e = np.concatenate(([0.0], u if j % 2 else v))
            worst_ek = max(worst_ek, abs(e @ eta @ ks[i]))

    # spinor brackets: lambda_a for p = E(1, n): |<ij>|^2 = 2 p_i.p_j
    def lam_sp(p):
        E, px, py, pz = p
        return np.array([math.sqrt(E + pz), (px + 1j * py) / math.sqrt(E + pz)])
    L = [lam_sp(kk) for kk in ks]
    for i in range(3):
        for j in range(i + 1, 3):
            worst_br = max(worst_br, abs(L[i][0] * L[j][1] - L[i][1] * L[j][0]))
print(f"  max |k_i.k_j| = {worst_kk:.1e}; max |eps_i.k_j| = {worst_ek:.1e}; max |<ij>| = {worst_br:.1e}")
print("  -> the cubic vertex (two derivatives, contracted from k_i.k_j, eps.k, eps.eps) vanishes on this support;")
print("     the 3-point on-shell amplitude M3 ~ kappa <12>^6/(<23><31>)^2 (or [..]) is 0 for real collinear momenta.")

hdr("(c) module: full g g -> gamma gamma amplitude as incoming gravitons become collinear (energies fixed = 1)")
print("  physical helicities (+2,-2) and (+2,+2), photons summed; theta12 = opening angle of incoming gravitons")
for th12 in (1.0, 0.3, 0.1, 0.03, 0.01):
    s = 2 * (1 - math.cos(th12))  # k1 = k2 = 1
    mx = 0.0
    for thc in np.linspace(0.2, PI - 0.2, 7):
        amps = q2.helicity_amplitudes_cm(s, thc, 0.3, final="photon", G=1.0)
        mx = max(mx, max(abs(vv) for vv in amps.values()))
    print(f"  theta12={th12:5.2f}: s = {s:.3e}; max |M| over helicities/angles = {mx:.4e};  max|M|/(8 pi s) = {mx/(8*PI*s):.6f}")
print("  -> |M| <= 8 pi G s -> 0 at s = 0 (independent bound: |t|, |u| <= s so 8 pi G t^2/s <= 8 pi G s).")
