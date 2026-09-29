"""M-IDEALIZER-04 (F4): generic clock-system coupling g V makes the relational evolution non-unitary, linearly in g.
Independent construction (hbar = 1, rad/s): clock d = 6, E_n = n - 2.5 (spacing omega_clock = 1 rad/s), qubit H_S = sigma_x/2.
J(g) = H_C + H_S + g V, V random Hermitian with operator norm 1 (three seeds).
(a) The exact null space of J(g) is generically empty for g > 0: the two eigenvalues that were 0 move by O(g).
(b) Retuning: subtract the two eigenvalues nearest 0 (J' = J(g) - sum_i w_i |v_i><v_i|) so a 2-dim kernel exists.
    Conditional map M(t): null basis -> (<t| x 1) basis, <t| = d^-1/2 sum_n e^{i E_n t}<n|.
    Effective generator G = i M'(0) M(0)^-1 (a 2x2 matrix on the system). Non-Hermiticity eta = ||G - G^dag|| / ||G + G^dag||.
    Claim: eta grows linearly in g (fitted log-log slope ~ 1); the lens's coefficient 0.45 depends on V, the retuning and the measure.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import quantity, inequality, finish

d = 6
EC = np.arange(d) - 2.5
HS = 0.5 * np.array([[0, 1], [1, 0]], complex)
J0 = np.kron(np.diag(EC), np.eye(2)) + np.kron(np.eye(d), HS)
gs = np.array([1e-3, 1e-2, 1e-1])
for seed in (1, 2, 3):
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(2 * d, 2 * d)) + 1j * rng.normal(size=(2 * d, 2 * d))
    V = (A + A.conj().T) / 2
    V /= np.linalg.norm(V, 2)
    etas, shifts = [], []
    for g in gs:
        w, U = np.linalg.eigh(J0 + g * V)
        idx = np.argsort(np.abs(w))[:2]
        shifts.append(np.abs(w[idx]).min() / g)
        Jp = J0 + g * V - sum(w[i] * np.outer(U[:, i], U[:, i].conj()) for i in idx)
        wn, Un = np.linalg.eigh(Jp)
        B = Un[:, np.abs(wn) < 1e-10]
        assert B.shape[1] == 2
        B3 = B.reshape(d, 2, 2)  # clock, system, basis
        M = lambda t: np.einsum("n,nsb->sb", np.exp(1j * EC * t) / np.sqrt(d), B3)
        dM = np.einsum("n,nsb->sb", 1j * EC * np.exp(0j) / np.sqrt(d), B3)
        G = 1j * dM @ np.linalg.inv(M(0.0))
        etas.append(np.linalg.norm(G - G.conj().T, 2) / np.linalg.norm(G + G.conj().T, 2))
    slope = np.polyfit(np.log(gs), np.log(etas), 1)[0]
    print(f"seed {seed}: min |eig J|/g = {np.round(shifts, 3)}, eta = {np.array(etas)}, eta/g = {np.array(etas)/gs}, slope {slope:.3f}")
    quantity(f"{slope}", "1", rel_tol=0.05)
    inequality(f"{min(shifts)}", ">", "0")
# limit g -> 0: uncoupled clock gives Hermitian generator exactly
w, U = np.linalg.eigh(J0); B = U[:, np.abs(w) < 1e-10].reshape(d, 2, 2)
dM = np.einsum("n,nsb->sb", 1j * EC / np.sqrt(d), B); M0 = np.einsum("n,nsb->sb", np.ones(d) / np.sqrt(d), B)
G0 = 1j * dM @ np.linalg.inv(M0)
print("g=0 generator:", np.round(G0, 12))
quantity(f"{1 + np.linalg.norm(G0 - HS)}", "1", rel_tol=1e-10)
raise SystemExit(finish())
