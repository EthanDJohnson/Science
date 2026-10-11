#!/usr/bin/env python3
"""Task B (3, ingredient): how the gravitational amplitude adds COHERENTLY over the ring of graviton pairs that feed one
total momentum Q in a smooth, locally plane, linearly polarised wave (the situation of an outgoing GW at radius r).

For fixed Q (CM energy^2 s) the on-shell pairs (k1, k2) with k1 + k2 = Q and |k1| = |k2| form a ring: in the lab both
gravitons are at half-opening angle a around Q^, at azimuth phi_k; in the CM they are back to back along n* ⊥ Q^.
In a smooth wave all of them carry the SAME lab polarisation tensor (TT projection of the local field's e_ij), so the
pair amplitude for one final photon state is the ring average <M>_ring. The proxy calculation (taskB_outgoing.py) treats
the vertex as constant on the ring (coherence factor 1). Here we compute, with the module amplitude
(qft_second_order.amplitude_gg_to_photons, all diagrams),
    C_coh = int dPhi2 sum_hel |<M>_ring|^2  /  < int dPhi2 sum_hel |M|^2 >_ring
and check it against an independent closed form: if the ring rotation adds no phase (argued from J_Q = lambda1 + lambda2 = 0
for opposite helicities collinear along Q, and mu1 + mu2 = 0 for the photons), |M| = (kappa/2)^2 t^2/s or u^2/s gives
    C_coh = int dc ((3 - c^2)/2)^2 / int dc [1 + 3(1 - c^2) + (3/8)(1 - c^2)^2] = 3.6/6.4 = 0.5625.
Also checked: <int dPhi2 sum |M|^2>_ring / 2 = 2 s sigma_lin = (4/5) pi G^2 s^2 for unit-normalised linear states.
"""
import math
import sys

import numpy as np

sys.path.insert(0, "/home/user/Science/.claude/skills/conundrum/scripts")
import qft_second_order as q2  # noqa: E402

PI = math.pi
G = 1.0


def tt_project(n, e):
    P = np.eye(3) - np.outer(n, n)
    m = P @ e @ P
    m = m - 0.5 * P * np.trace(m)
    return m / math.sqrt(np.sum(np.abs(m) ** 2))


def boost_z(beta):
    g = 1 / math.sqrt(1 - beta * beta)
    L = np.eye(4)
    L[0, 0] = L[3, 3] = g
    L[0, 3] = L[3, 0] = -g * beta
    return L


def coherence(a, lab_pol="plus", n_ring=48, n_c=24, n_phi=40):
    w = 1.0
    e3 = {"plus": np.diag([1.0, -1.0, 0.0]) / math.sqrt(2),
          "cross": (np.outer([1, 0, 0], [0, 1, 0]) + np.outer([0, 1, 0], [1, 0, 0])) / math.sqrt(2),
          "R": None}[lab_pol]
    beta = math.cos(a)
    L = boost_z(beta)
    Linv = np.linalg.inv(L)
    s = 4 * w * w * math.sin(a) ** 2
    E = 0.5 * math.sqrt(s)
    c, wc = np.polynomial.legendre.leggauss(n_c)
    ph = (np.arange(n_phi) + 0.37) * 2 * PI / n_phi
    C, P = np.meshgrid(c, ph, indexing="ij")
    Sn = np.sqrt(1 - C * C)
    nq = np.stack([Sn * np.cos(P), Sn * np.sin(P), C], axis=-1)
    p1 = np.concatenate([np.full(C.shape + (1,), E), E * nq], axis=-1)
    p2 = np.concatenate([np.full(C.shape + (1,), E), -E * nq], axis=-1)
    Msum = {hh: np.zeros(C.shape, complex) for hh in [(1, 1), (1, -1), (-1, 1), (-1, -1)]}
    M2sum = np.zeros(C.shape)
    for j in range(n_ring):
        phk = (j + 0.5) * 2 * PI / n_ring
        nk1 = np.array([math.sin(a) * math.cos(phk), math.sin(a) * math.sin(phk), math.cos(a)])
        nk2 = np.array([-math.sin(a) * math.cos(phk), -math.sin(a) * math.sin(phk), math.cos(a)])
        ks, eps = [], []
        for nk in (nk1, nk2):
            k = np.concatenate([[w], w * nk])
            if lab_pol == "R":
                epsl = q2.graviton_polarization(k, "R")
            else:
                ee = tt_project(nk, e3)
                epsl = np.zeros((4, 4), complex)
                epsl[1:, 1:] = ee          # lower spatial components = e_i e_j convention of the module
            kc = L @ k
            epsc = Linv.T @ epsl @ Linv
            ks.append(kc)
            eps.append(epsc)
        for (h1, h2) in Msum:
            e1 = q2._pol_array(p1, h1)
            e2 = q2._pol_array(p2, h2)
            M = q2.amplitude_gg_to_photons(ks[0], eps[0], ks[1], eps[1], p1, e1, p2, e2, G)
            Msum[(h1, h2)] += M / n_ring
            M2sum += np.abs(M) ** 2 / n_ring
    dOm = (wc[:, None] * np.ones_like(P)) * (2 * PI / n_phi)
    inc = 0.5 * np.sum(M2sum * dOm) / (32 * PI * PI)
    coh = 0.5 * np.sum(sum(np.abs(v) ** 2 for v in Msum.values()) * dOm) / (32 * PI * PI)
    return s, inc, coh


print("closed form (no ring phase): C_coh = 3.6/6.4 =", 3.6 / 6.4)
for a in (0.6, 0.2, 0.05):
    for pol in ("plus", "cross"):
        s, inc, coh = coherence(a, pol)
        print(f"a = {a:5.3f} rad, s/w^2 = {s:.5f}, lab pol {pol:5s}: ring-averaged (1/2)int dPhi2 sum|M|^2 = {inc:.6e}"
              f"  [(4/5) pi G^2 s^2 = {0.8*PI*s*s:.6e}];  C_coh = {coh/inc:.5f}")
s, inc, coh = coherence(0.2, "R")
print(f"a = 0.200, both helicity +2: (1/2)int dPhi2 sum|M|^2 = {inc:.3e} (same helicity: 0 expected)")
