"""M-EXAMINER-06: Kuchar's naive two-time probability vs the Giovannetti-Lloyd-Maccone (GLM) memory construction.

Claim (finding 9, hardest question 3), hbar = 1: qubit H_S = 0.5 sigma_x (rad/s), 8-level equally spaced clock
(spacing 1 rad/s), t1 = 0.785 s (= pi/4), t2 = 2.356 s (= 3 pi/4):
  naive P(0 at t2 | 0 at t1) = 0; GLM memory P = 0.5 = |<0|U(t2 - t1)|0>|^2.
Independent construction:
  clock energies E_n = n - 3.5 (n = 0..7) so that both system energies +-0.5 are covered (-e in spec H_C);
  time states |t> = sum_n e^{-i E_n t}|n> / sqrt(d), lattice t_k = 2 pi k / d (orthonormal);
  PW null state Psi = sum_e |n(e)> (x) P_e psi0 where E_n(e) = -e  => (<t| (x) 1) Psi = e^{-iH_S t} psi0 / sqrt(d).
  Naive: P = <Psi|P1 P2 P1|Psi> / <Psi|P1|Psi>, P_i = |t_i><t_i| (x) |0><0|.
  GLM: history state over the lattice, Psi = d^{-1/2} sum_k |t_k> (x) phi(t_k), phi on S (x) M (M: ready r, records 0, 1),
       phi(t) = U(t) psi0 |r> for t < t1, and U(t - t1) W U(t1) psi0 |r> for t >= t1, with W: |s>|r> -> |s>|s>.
       P(b | a) = ||(<t2| Pi_b <a|_M) Psi||^2 / ||(<t2| <a|_M) Psi||^2.
Also checks: the PW null state satisfies (H_C + H_S) Psi = 0, and the lattice history state without W equals it
(so the GLM state differs from the null state only by the record).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, inequality, finish

d = 8
E = np.arange(d) - 3.5
HC = np.diag(E)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
HS = 0.5 * sx
eS, VS = np.linalg.eigh(HS)


def U(t):
    return VS @ np.diag(np.exp(-1j * eS * t)) @ VS.conj().T


def tstate(t):
    return np.exp(-1j * E * t) / np.sqrt(d)


psi0 = np.array([1, 0], dtype=complex)
Psi = np.zeros(d * 2, dtype=complex)
for i, e in enumerate(eS):
    n = int(np.argmin(np.abs(E + e)))
    assert abs(E[n] + e) < 1e-12
    ket_n = np.zeros(d); ket_n[n] = 1
    Pe = np.outer(VS[:, i], VS[:, i].conj())
    Psi += np.kron(ket_n, Pe @ psi0)
J = np.kron(HC, np.eye(2)) + np.kron(np.eye(d), HS)
res = np.abs(J @ Psi).max()
print("|J Psi| =", res)
inequality(sp.Float(res), "<", sp.Float(1e-12))

tk = 2 * np.pi * np.arange(d) / d
G = np.array([[tstate(a).conj() @ tstate(b) for b in tk] for a in tk])
orth = np.abs(G - np.eye(d)).max()
print("lattice orthonormality defect:", orth)
inequality(sp.Float(orth), "<", sp.Float(1e-12))
t1, t2 = tk[1], tk[3]
print("t1, t2 =", t1, t2)

P0 = np.diag([1, 0]).astype(complex)
P1 = np.kron(np.outer(tstate(t1), tstate(t1).conj()), P0)
P2 = np.kron(np.outer(tstate(t2), tstate(t2).conj()), P0)
naive = np.real(Psi.conj() @ P1 @ P2 @ P1 @ Psi) / np.real(Psi.conj() @ P1 @ Psi)
textbook = abs(U(t2 - t1)[0, 0])**2
print("naive Kuchar P =", naive, "; textbook =", textbook)
inequality(sp.Float(abs(naive)), "<", sp.Float(1e-12))
identity(sp.Float(textbook, 20), sp.Rational(1, 2))

# GLM history state; memory basis |0>, |1>, |r> (index 2)
dM = 3
r = np.zeros(dM, dtype=complex); r[2] = 1
W = np.zeros((2 * dM, 2 * dM), dtype=complex)  # on S (x) M
for s in range(2):
    for m in range(dM):
        src = s * dM + m
        dst = s * dM + (s if m == 2 else (2 if m == s else m))  # swap |r> <-> |s>, identity otherwise (unitary)
        W[dst, src] = 1
assert np.allclose(W.conj().T @ W, np.eye(2 * dM))


def phi(t, record=True):
    if t < t1 - 1e-12:
        return np.kron(U(t) @ psi0, r)
    base = np.kron(U(t1) @ psi0, r)
    if record:
        base = W @ base
    return np.kron(U(t - t1), np.eye(dM)) @ base


def history(record):
    return sum(np.kron(tstate(t), phi(t, record)) for t in tk) / np.sqrt(d)


Hglm = history(True)
bra2 = np.kron(tstate(t2).conj(), np.eye(2 * dM))
v2 = bra2 @ Hglm                       # state of S (x) M at clock reading t2
a = 0
proj_a = np.kron(np.eye(2), np.outer(np.eye(dM)[a], np.eye(dM)[a]))
proj_b = np.kron(P0, np.eye(dM))
glm = np.linalg.norm(proj_b @ proj_a @ v2)**2 / np.linalg.norm(proj_a @ v2)**2
print("GLM P(0 at t2 | 0 at t1) =", glm)
# float64 result: compare to 1/2 within round-off
inequality(sp.Float(abs(glm - 0.5)), "<", sp.Float(1e-12))

# without the record, the history state equals the PW null state (up to the 1/sqrt(d) normalisations)
H0 = history(False)
# compare component-wise after reshaping: Psi (x) |r>, both normalised
A = H0 / np.linalg.norm(H0)
B = np.einsum("ns,m->nsm", Psi.reshape(d, 2), r).reshape(-1)
B = B / np.linalg.norm(B)
diff = np.abs(A - B).max()
print("history state (no record) vs PW null state (x) |r>: max diff =", diff)
inequality(sp.Float(diff), "<", sp.Float(1e-12))

# robustness: different initial state and a different lattice pair
psi0 = np.array([np.cos(0.3), np.exp(0.7j) * np.sin(0.3)])
t1, t2 = tk[2], tk[7]
v2 = np.kron(tstate(t2).conj(), np.eye(2 * dM)) @ history(True)
glm2 = np.linalg.norm(proj_b @ proj_a @ v2)**2 / np.linalg.norm(proj_a @ v2)**2
tb2 = abs(U(t2 - t1)[0, 0])**2
print("GLM (other state/times) =", glm2, "; textbook =", tb2)
identity(sp.Float(glm2, 20), sp.Float(tb2, 20))

raise SystemExit(finish())
