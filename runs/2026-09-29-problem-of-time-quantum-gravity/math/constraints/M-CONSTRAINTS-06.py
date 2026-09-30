"""M-CONSTRAINTS-06: Kuchar two-time objection in a finite Page-Wootters model (hbar = 1).

System: qubit, H_S = 0.5 sigma_x (rad/s). Clock: d = 8, E_n = n - 3.5 (covers -H_S spectrum +-0.5),
lattice t_j = 2 pi j/8 s. Physical state: projection of |t_0> (x) |0> onto ker(H_C + H_S).
Naive rule: P(1 at t2 | 0 at t1) = <Psi|P1 Q2 P1|Psi>/<Psi|P1|Psi>, P1 = |t1><t1| (x) |0><0|, Q2 = |t2><t2| (x) |1><1|.
Memory rule (GLM-type, built independently): a record qubit R that copies the system's sigma_z value at
clock time t1 is added to the history state; P = prob(R = 0, S = 1 at t2)/prob(R = 0).
Claim (F6): naive P = 0 for t1 != t2; memory rule gives |<1|U(t2 - t1)|0>|^2 = 0.5, 0.853553, 1.0.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.linalg import expm, null_space
from math_checks import identity, quantity, finish

d = 8
E = np.arange(d) - 3.5
HC = np.diag(E)
sx = np.array([[0, 1], [1, 0]], complex)
HS = 0.5 * sx
J = np.kron(HC, np.eye(2)) + np.kron(np.eye(d), HS)
tj = 2 * np.pi * np.arange(d) / d
ket_t = lambda t: np.exp(-1j * E * t) / np.sqrt(d)
U = lambda t: expm(-1j * HS * t)
z0, z1 = np.array([1, 0], complex), np.array([0, 1], complex)

# Physical state: projector onto null space of J applied to |t0>|0>
Nsp = null_space(J)
print("null space dim:", Nsp.shape[1])
psi = Nsp @ (Nsp.conj().T @ np.kron(ket_t(0.0), z0))
psi /= np.linalg.norm(psi)
print("PASS J Psi = 0" if np.linalg.norm(J @ psi) < 1e-12 else "FAIL J Psi")
# conditional state reproduces Schroedinger evolution on lattice
for j in range(d):
    cond = np.kron(ket_t(tj[j]).conj(), np.eye(2)) @ psi
    cond /= np.linalg.norm(cond)
    ref = U(tj[j]) @ z0
    if abs(abs(np.vdot(ref, cond)) - 1) > 1e-10:
        print("FAIL conditional state at", j)

pairs = [(1, 3), (0, 3), (2, 6)]   # step differences 2, 3, 4 -> dt = pi/2, 3pi/4, pi
expect = [0.5, 0.853553, 1.0]
for (j1, j2), ex in zip(pairs, expect):
    P1 = np.kron(np.outer(ket_t(tj[j1]), ket_t(tj[j1]).conj()), np.outer(z0, z0))
    Q2 = np.kron(np.outer(ket_t(tj[j2]), ket_t(tj[j2]).conj()), np.outer(z1, z1))
    naive = np.real(np.vdot(psi, P1 @ Q2 @ P1 @ psi)) / np.real(np.vdot(psi, P1 @ psi))
    # Memory rule: history state sum_j |t_j> (x) |s_j, r_j>, with r_j = |ready> for j < j1 and the CNOT-copied
    # record for j >= j1. Evolution applied on S (x) R with U (x) 1 and the copy at step j1.
    CN = np.zeros((4, 4)); CN[0, 0] = CN[1, 1] = CN[3, 2] = CN[2, 3] = 1      # order |s r>: copy s into r
    sr = np.kron(z0, z0).astype(complex)   # s = 0, r = ready(=0)
    hist = []
    dt = 2 * np.pi / d
    Ustep = np.kron(U(dt), np.eye(2))
    state = sr.copy()
    for j in range(d):
        if j == j1:
            state = CN @ state
        hist.append(state.copy())
        state = Ustep @ state
    # history (PW-with-record) state and conditional probability at t2
    Hst = sum(np.kron(ket_t(tj[j]), hist[j]) for j in range(d)) / np.sqrt(d)
    Pt2 = np.kron(np.outer(ket_t(tj[j2]), ket_t(tj[j2]).conj()), np.eye(4))
    # the record in |ready> = |0> is ambiguous with record value 0; use record-of-1 flag instead:
    # prob(system 1 at t2 AND record 0 set at t1) / prob(record 0 set at t1); for j2 > j1 record basis is sigma_z
    PS1R0 = np.kron(np.eye(d), np.kron(np.outer(z1, z1), np.outer(z0, z0)))
    PR0 = np.kron(np.eye(d), np.kron(np.eye(2), np.outer(z0, z0)))
    mem = np.real(np.vdot(Hst, Pt2 @ PS1R0 @ Pt2 @ Hst)) / np.real(np.vdot(Hst, Pt2 @ PR0 @ Pt2 @ Hst))
    born = abs(z1 @ U(tj[j2] - tj[j1]) @ z0) ** 2
    print(f"t1={tj[j1]:.4f}, t2={tj[j2]:.4f}: naive {naive:.2e}, memory {mem:.6f}, Born {born:.6f}")
    quantity(f"{naive + 1}", "1", rel_tol=1e-12)      # naive = 0
    quantity(f"{mem}", f"{born}", rel_tol=1e-9)
    quantity(f"{born}", f"{ex}", rel_tol=1e-6)
# analytic Born value: |<1|exp(-i 0.5 sx t)|0>|^2 = sin^2(t/2)
identity("sin(t/2)**2", "(1 - cos(t))/2", domain={"t": (-6, 6)})
# limit: equal times give naive P(0|0) = 1
P1 = np.kron(np.outer(ket_t(tj[1]), ket_t(tj[1]).conj()), np.outer(z0, z0))
same = np.real(np.vdot(psi, P1 @ P1 @ P1 @ psi)) / np.real(np.vdot(psi, P1 @ psi))
quantity(f"{same}", "1", rel_tol=1e-12)
raise SystemExit(finish())
