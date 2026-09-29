"""M-DIALECTICIAN-02: record (GLM memory) two-time probability equals the textbook propagator.

Model (hbar = 1): clock lattice t_j = 2 pi j/d (d = 8, spacing 1 rad/s), system qubit U(t) = exp(-i sigma_x t/2),
memory qubit M. History state Psi = d^{-1/2} sum_j |t_j> x V_j |psi0>|0>_M with V_j = U(t_j) (j < j1) and
V_j = U(t_j - t_j1) CNOT_{S->M} U(t_j1) (j >= j1). Claim: P(b at t_j2 | memory = a) = |<b|U(t_j2 - t_j1)|a>|^2,
= 0.146447, 0.5, 1.0 at tau = 1, 2, 4 lattice steps (a=0, b=1); textbook values 0.00997 (tau=0.2 s), 0.366 (1.3 s).
Also: Psi is invariant under the unitary clock-shift W (so it solves a constraint J = i log W).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, finish, Result, _done

d = 8
sx = np.array([[0, 1], [1, 0]], complex)
def U(t):
    return np.cos(t / 2) * np.eye(2) - 1j * np.sin(t / 2) * sx
I2 = np.eye(2)
CNOT = np.zeros((4, 4), complex)  # order S x M
for s in (0, 1):
    for m in (0, 1):
        CNOT[2 * s + (m ^ s), 2 * s + m] = 1
tj = [2 * np.pi * j / d for j in range(d)]

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric (numpy)", note=note), True)

def history(psi0, j1):
    V = []
    for j in range(d):
        if j < j1:
            V.append(np.kron(U(tj[j]), I2))
        else:
            V.append(np.kron(U(tj[j] - tj[j1]), I2) @ CNOT @ np.kron(U(tj[j1]), I2))
    phi0 = np.kron(psi0, [1, 0])
    blocks = [Vj @ phi0 for Vj in V]
    return V, np.concatenate(blocks) / np.sqrt(d)   # clock lattice basis |t_j> are orthonormal

def cond(Psi, j2, a, b):
    blk = Psi.reshape(d, 4)[j2].reshape(2, 2)   # [s, m]
    num = abs(blk[b, a]) ** 2
    den = np.sum(abs(blk[:, a]) ** 2)
    return num / den

rng = np.random.default_rng(3)
for psi0, j1, label in [(np.array([1, 0], complex), 1, "psi0=|0>, j1=1"),
                        ((lambda v: v / np.linalg.norm(v))(rng.normal(size=2) + 1j * rng.normal(size=2)), 2, "random psi0, j1=2")]:
    V, Psi = history(psi0, j1)
    for tau_steps in (1, 2, 4):
        j2 = j1 + tau_steps
        if j2 >= d:
            continue
        for a in (0, 1):
            for b in (0, 1):
                got = cond(Psi, j2, a, b)
                want = abs(U(tj[j2] - tj[j1])[b, a]) ** 2
                if not abs(got - want) < 1e-12:
                    report(f"GLM = textbook ({label}, tau={tau_steps}, a={a}, b={b})", False, f"{got} vs {want}")
    report(f"GLM conditional = |<b|U(tau)|a>|^2 for all a,b, tau in 1,2,4 steps ({label})", True)
    # constraint: cyclic clock shift W with Psi as a +1 eigenvector
    W = np.zeros((4 * d, 4 * d), complex)
    for j in range(d):
        jn = (j + 1) % d
        W[4 * jn:4 * jn + 4, 4 * j:4 * j + 4] = V[jn] @ V[j].conj().T
    report(f"W unitary and W Psi = Psi ({label})",
           np.allclose(W.conj().T @ W, np.eye(4 * d)) and np.allclose(W @ Psi, Psi))

_, Psi = history(np.array([1, 0], complex), 1)
vals = [cond(Psi, 1 + s, 0, 1) for s in (1, 2, 4)]
report("quoted values 0.146447, 0.500000, 1.000000", np.allclose(vals, [0.146447, 0.5, 1.0], atol=1e-6),
       ", ".join(f"{v:.6f}" for v in vals))
report("textbook sin^2(tau/2) at 0.2 s and 1.3 s = 0.00997, 0.366",
       abs(np.sin(0.1) ** 2 - 0.00997) < 5e-6 and abs(np.sin(0.65) ** 2 - 0.366) < 5e-4,
       f"{np.sin(0.1)**2:.5f}, {np.sin(0.65)**2:.4f}")
t = sp.symbols("t", positive=True)
Us = sp.exp(-sp.I * sp.Matrix([[0, 1], [1, 0]]) * t / 2)
identity(sp.simplify(sp.Abs(Us[1, 0]) ** 2), sp.sin(t / 2) ** 2)
limit(sp.sin(t / 2) ** 2 / t**2, "t", 0, "1/4")   # short-time Zeno limit P ~ (Omega t/2)^2
raise SystemExit(finish())
