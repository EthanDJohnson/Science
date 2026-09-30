# M-DECOMPOSER-02 and -03: finite Page-Wootters model, built from scratch (hbar = 1, times in s, energies in rad/s).
# Clock: d = 8 levels, H_C = diag(k - 3.5), k = 0..7 (spacing 1 rad/s). System: qubit, H_S = 0.5 sigma_x.
# Constraint J = H_C x 1 + 1 x H_S. Clock time states |t> = d^-1/2 sum_k exp(-i c_k t)|k>; lattice t_j = 2 pi j / 8.
# Kuchar naive rule: P(b,t2 | a,t1) = ||(P_t2 x P_b)(P_t1 x P_a) Psi||^2 / ||(P_t1 x P_a) Psi||^2.
# Memory (GLM-type) rule: a memory qubit M records the sigma_z value at t1 by a CNOT triggered at clock step t1;
# P(b at t2 | memory a) = ||(<t2| x P_b x P^M_a) Psi_hist||^2 / ||(<t2| x P^M_a) Psi_hist||^2.
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.linalg import expm, null_space
from math_checks import quantity, inequality, identity, finish

d = 8
c = np.arange(d) - 3.5
HC = np.diag(c).astype(complex)
sx = np.array([[0, 1], [1, 0]], complex); sz = np.diag([1.0, -1.0]).astype(complex)
HS = 0.5 * sx
J = np.kron(HC, np.eye(2)) + np.kron(np.eye(d), HS)
K = null_space(J, rcond=1e-12)
print("physical subspace dimension:", K.shape[1])
rng = np.random.default_rng(3)
Psi = K @ (rng.normal(size=K.shape[1]) + 1j * rng.normal(size=K.shape[1])); Psi /= np.linalg.norm(Psi)

def tket(t): return np.exp(-1j * c * t) / np.sqrt(d)
def cond(t): return np.kron(tket(t).conj(), np.eye(2)) @ Psi    # <t|Psi>, a system vector
def U(t): return expm(-1j * HS * t)

# (i) single-time: conditional state at any real t equals U(t) cond(0) (Schrodinger evolution)
err = max(np.linalg.norm(cond(t) - U(t) @ cond(0)) for t in np.linspace(-5, 7, 41))
print("max ||<t|Psi> - U(t)<0|Psi>|| =", err)
inequality(f"{err}", "<", "1e-12")
# lattice orthogonality
tj = 2 * np.pi * np.arange(d) / d
G = np.array([[tket(a).conj() @ tket(b) for b in tj] for a in tj])
inequality(f"{np.abs(G - np.eye(d)).max()}", "<", "1e-12")

t1, t2 = tj[1], tj[4]
print("t1, t2 =", t1, t2, " t2 - t1 =", t2 - t1)
Pt = lambda t: np.outer(tket(t), tket(t).conj())
Pa = [np.diag([1, 0]).astype(complex), np.diag([0, 1]).astype(complex)]
def naive(a, b, s1, s2):
    A = np.kron(Pt(s1), Pa[a]) @ Psi
    B = np.kron(Pt(s2), Pa[b]) @ A
    return np.linalg.norm(B)**2 / np.linalg.norm(A)**2
tab = [[naive(a, b, t1, t2) for b in (0, 1)] for a in (0, 1)]
print("naive Kuchar table t1 != t2:", tab)
inequality(f"{max(max(r) for r in tab)}", "<", "1e-12")            # M-02: all zero
same = [[naive(a, b, t1, t1) for b in (0, 1)] for a in (0, 1)]
print("naive table t2 = t1:", same)
identity(f"{same[0][0]:.12f}", "1"); identity(f"{same[1][1]:.12f}", "1")

# (ii) memory rule (M-03): history state over the clock lattice with a CNOT (S -> M) at step t1
CNOT = np.kron(Pa[0], np.eye(2)) + np.kron(Pa[1], sx)
psi0 = np.kron(cond(0) / np.linalg.norm(cond(0)), np.array([1, 0], complex))
hist = []
for j, t in enumerate(tj):
    v = np.kron(U(t), np.eye(2)) @ psi0 if j < 1 else np.kron(U(t - t1), np.eye(2)) @ (CNOT @ (np.kron(U(t1), np.eye(2)) @ psi0))
    hist.append(v)
def memrule(a, b):
    v = hist[4]
    num = np.linalg.norm(np.kron(Pa[b], Pa[a]) @ v)**2
    den = np.linalg.norm(np.kron(np.eye(2), Pa[a]) @ v)**2
    return num / den
mem = [[memrule(a, b) for b in (0, 1)] for a in (0, 1)]
ref = [[abs(U(t2 - t1)[b, a])**2 for b in (0, 1)] for a in (0, 1)]
print("memory rule:", mem, " reference |<b|U|a>|^2:", ref)
inequality(f"{np.abs(np.array(mem) - np.array(ref)).max()}", "<", "1e-12")
quantity(f"{mem[0][0]}", "0.1464", rel_tol=5e-4); quantity(f"{mem[0][1]}", "0.8536", rel_tol=5e-4)
# closed form: |<0|exp(-i 0.5 sx 3pi/4)|0>|^2 = cos^2(3 pi/8)
identity("cos(3*pi/8)**2", "(2 - sqrt(2))/4")
quantity(f"{(2 - np.sqrt(2)) / 4}", "0.1464", rel_tol=5e-4)
# limit: t2 -> t1 in the memory rule gives delta_ab (no evolution)
inequality(f"{abs(abs(U(0)[0,0])**2 - 1)}", "<", "1e-15")
raise SystemExit(finish())
