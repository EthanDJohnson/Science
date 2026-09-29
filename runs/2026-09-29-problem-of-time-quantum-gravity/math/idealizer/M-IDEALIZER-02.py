"""M-IDEALIZER-02 (F2): Kuchar's naive two-time probability vanishes; a memory register restores textbook values.
Qubit H_S = sigma_x/2 (rad/s, hbar = 1), psi0 = |0>. Textbook P(1 at t2 | 0 at t1) = |<1|U(t2-t1)|0>|^2 = sin^2((t2-t1)/2).
Naive rule: P = <Psi|A1 A2 A1|Psi>/<Psi|A1|Psi>, A1 = |t1><t1| x |0><0|, A2 = |t2><t2| x |1><1|.
Since |0><0| |1><1| = 0 on the same factor, A1 A2 A1 = |<t1|t2>|^2 |t1><t1| x (P0 P1 P0) = 0 for ANY t1, t2 (lattice or not).
Memory: independent construction, a history state over lattice times with a record qubit that copies the
system's 0/1 value at step k1 (CNOT), built as sum_k |k> x V_k (psi0 x |ready>), V_k the k-step evolution with
the record written at step k1.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import quantity, finish

d = 8
EC = np.arange(d) - 3.5
HS = 0.5 * np.array([[0, 1], [1, 0]], complex)
ev, ew = np.linalg.eigh(HS)
U = lambda t: ew @ np.diag(np.exp(-1j * ev * t)) @ ew.conj().T
def tstate(t):
    return np.exp(-1j * EC * t) / np.sqrt(d)
J = np.kron(np.diag(EC), np.eye(2)) + np.kron(np.eye(d), HS)
w, V = np.linalg.eigh(J)
null = V[:, np.abs(w) < 1e-12]
# PW state with psi(0) = |0>: Psi = sum_k |t_k> x U(t_k)|0> (lattice) is a null vector
tk = 2 * np.pi * np.arange(d) / d
Psi = sum(np.kron(tstate(t), U(t) @ np.array([1, 0], complex)) for t in tk)
print("J Psi norm:", np.linalg.norm(J @ Psi))
quantity(f"{1 + np.linalg.norm(J @ Psi)}", "1", rel_tol=1e-12)
P0 = np.diag([1, 0]).astype(complex); P1 = np.diag([0, 1]).astype(complex)
def naive(t1, t2):
    c1 = np.outer(tstate(t1), tstate(t1).conj()); c2 = np.outer(tstate(t2), tstate(t2).conj())
    A1 = np.kron(c1, P0); A2 = np.kron(c2, P1)
    return np.vdot(Psi, A1 @ A2 @ A1 @ Psi).real / np.vdot(Psi, A1 @ Psi).real
for (t1, t2) in [(0, np.pi / 4), (0, np.pi / 2), (0, 3 * np.pi / 4), (0.3, 0.4), (0.3, 0.6)]:
    pn = naive(t1, t2); pt = np.sin((t2 - t1) / 2) ** 2
    print(f"t2-t1={t2-t1:.3f}: naive {pn:.2e}, textbook {pt:.6e}")
    quantity(f"{1 + abs(pn)}", "1", rel_tol=1e-12)
quantity(f"{np.sin(0.05)**2}", "2.50e-3", rel_tol=2e-3)
quantity(f"{np.sin(0.15)**2}", "2.23e-2", rel_tol=2e-3)

# memory register: system (2) x record (2); history clock of d lattice steps, step dt = 2pi/d
dt = 2 * np.pi / d
Ustep = np.kron(U(dt), np.eye(2))
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex)  # system controls record
def glm(k1, k2):
    s = np.kron(np.array([1, 0], complex), np.array([1, 0], complex))
    hist = []
    for k in range(d):
        if k == k1:
            s = CNOT @ s
        hist.append(s.copy())
        s = Ustep @ s
    H = np.array(hist)  # rows: clock k, columns: system x record
    # condition on clock = k2, system = 1, record = 0 (system was 0 at t1)
    rec0_at_k2 = H[k2].reshape(2, 2)[:, 0]
    num = abs(rec0_at_k2[1]) ** 2
    den = np.linalg.norm(rec0_at_k2) ** 2
    return num / den
for k2, want in [(2, 0.146447), (3, 0.5), (4, 0.853553)]:
    g = glm(1, k2)
    print(f"GLM k1=1,k2={k2}: {g:.6f}; textbook {np.sin((k2-1)*dt/2)**2:.6f}")
    quantity(f"{g}", f"{want}", rel_tol=1e-5)
raise SystemExit(finish())
