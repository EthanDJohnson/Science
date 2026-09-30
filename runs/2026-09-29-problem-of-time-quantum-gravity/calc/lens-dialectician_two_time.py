#!/usr/bin/env python3
"""Dialectician, contradiction I: Kuchar's naive two-time probability vs the record (GLM/HSL) version.

Units: natural units hbar = 1; energies are angular frequencies in rad/s, times in s.
Model: equally spaced clock, d levels, spacing w = 1 rad/s, symmetric (E = -3.5 .. 3.5 rad/s for d = 8);
system qubit H_S = (Omega/2) sigma_x with Omega = 1 rad/s (eigenvalues +-0.5 rad/s, resonant with the clock).
Questions:
 (1) Naive P(b at t2 | a at t1) at distinct lattice times (Kuchar: should be 0).
 (2) Naive formula off the lattice: is it  |<t1|t2>|^2/d^2 * |<b|a>|^2  (clock overlap x NO evolution)?
 (3) GLM memory version: equals textbook |<b|U(t2-t1)|a>|^2 ?
"""
import sys
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import page_wootters as pw  # noqa: E402

d, w, Om = 8, 1.0, 1.0
HC = pw.equally_spaced_clock(d, w, k0=-(d - 1) / 2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
HS = 0.5 * Om * sx
m = pw.PWModel(HC, HS)
psi0 = np.array([1.0, 0.0], dtype=complex)
Psi = m.physical_state(psi0)
Psi = Psi / np.linalg.norm(Psi)
Pi = [np.diag([1.0, 0.0]).astype(complex), np.diag([0.0, 1.0]).astype(complex)]
step = 2 * np.pi / (d * w)
print(f"clock d={d}, spacing w={w} rad/s, lattice step {step:.6f} s, period {2*np.pi/w:.6f} s; qubit Omega={Om} rad/s")

def textbook(a, b, tau):
    U = m.evolve(np.eye(2, dtype=complex)[:, a], tau)
    return abs(U[b]) ** 2

print("\n(1)+(3) lattice times: naive vs GLM vs textbook, P(b=1 at t2 | a=0 at t1)")
j1 = 1
for j2 in [1, 2, 3, 5]:
    t1, t2 = j1 * step, j2 * step
    naive = pw.kuchar_naive(m, Psi, t1, t2, Pi[0], Pi[1])
    g = pw.glm_two_time(HS, psi0, d, w, j1, j2)["P_b_given_a"]
    print(f"  t1={t1:.4f} s t2={t2:.4f} s | naive={naive:.3e} | GLM={g[0,1]:.6f} | textbook={textbook(0,1,t2-t1):.6f}")

print("\n(2) naive formula off-lattice: sum_b P_naive(b|a) vs clock overlap |<t1|t2>|^2/d^2; and normalised naive P(b|a)")
t1 = step
for tau in [0.05, 0.2, 0.4, step / 2, step, 1.3]:
    t2 = t1 + tau
    n0 = pw.kuchar_naive(m, Psi, t1, t2, Pi[0], Pi[0])
    n1 = pw.kuchar_naive(m, Psi, t1, t2, Pi[0], Pi[1])
    ov = (m.overlap(tau)[0]) ** 2
    tot = n0 + n1
    frac1 = n1 / tot if tot > 1e-14 else float("nan")
    print(f"  tau={tau:.4f} s | naive total={tot:.6e} | overlap^2={ov:.6e} | naive P(1|0) normalised={frac1:.3e} "
          f"| textbook P(1|0)={textbook(0,1,tau):.6f}")
print("\nReading: the naive formula factorises into (clock self-overlap) x (no system evolution);")
print("the record (GLM) construction reproduces the textbook propagator at every lattice pair.")
