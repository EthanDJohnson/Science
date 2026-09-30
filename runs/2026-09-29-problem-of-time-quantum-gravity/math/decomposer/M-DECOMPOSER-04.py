# M-DECOMPOSER-04 and -05: one constraint on A x B x S (hbar = 1; energies in rad/s, times in s).
# A: 3-level, H_A = diag(-1, 0, 1); S: qubit, H_S = 0.35 sigma_z (non-degenerate H_A + H_S); coupling g X_A x sigma_x, X_A = A's position-like
# tridiagonal operator. H_AS = H_A + H_S + g X_A sigma_x (6 x 6). B: 6-level clock, uncoupled, resonant:
# spectrum b_k = -eig_k(H_AS), so J = H_B + H_AS has a 6-dimensional kernel.
# Clock time states: |t>_B = 6^-1/2 sum_k e^{-i b_k t}|k>_B ; |t>_A = 3^-1/2 sum_n e^{-i a_n t}|n>_A (A's free spectrum).
# Claims: (04) relative to B, <t|_B Psi evolves exactly by H_AS, norm constant (any B spectrum);
#         (05) relative to A (coupled), conditional B x S states have non-constant norm and a non-Hermitian,
#              time-dependent effective generator; this vanishes as g -> 0.
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.linalg import expm, null_space
from math_checks import inequality, finish

a = np.array([-1.0, 0.0, 1.0]); HA = np.diag(a)
XA = (np.diag([1, 1], 1) + np.diag([1, 1], -1)) / np.sqrt(2)
sx = np.array([[0, 1], [1, 0]]); sz = np.diag([1.0, -1.0])

def build(g):
    HAS = np.kron(HA, np.eye(2)) + 0.35 * np.kron(np.eye(3), sz) + g * np.kron(XA, sx)
    h, V = np.linalg.eigh(HAS)
    b = -h
    # ordering A x B x S
    I2, I3, I6 = np.eye(2), np.eye(3), np.eye(6)
    HB = np.diag(b)
    HAS_full = np.kron(np.kron(HA, I6), I2) + 0.35 * np.kron(np.kron(I3, I6), sz) + g * np.kron(np.kron(XA, I6), sx)
    J = HAS_full + np.kron(np.kron(I3, HB), I2)
    K = null_space(J, rcond=1e-10)
    return HAS, b, J, K

def cond_B(Psi, b, t):   # <t|_B Psi on A x S
    tk = np.exp(-1j * b * t) / np.sqrt(6)
    T = Psi.reshape(3, 6, 2)
    return np.einsum("k,aks->as", tk.conj(), T).reshape(6)

def cond_A(Psi, t):      # <t|_A Psi on B x S
    tk = np.exp(-1j * a * t) / np.sqrt(3)
    T = Psi.reshape(3, 6, 2)
    return np.einsum("n,nks->ks", tk.conj(), T).reshape(12)

rng = np.random.default_rng(7)
ts = np.linspace(0, 2 * np.pi, 121)
res = {}
for g in (0.3, 0.1, 0.01, 0.0):
    HAS, b, J, K = build(g)
    print(f"g = {g}: physical subspace dimension {K.shape[1]}")
    Psi = K @ (rng.normal(size=K.shape[1]) + 1j * rng.normal(size=K.shape[1])); Psi /= np.linalg.norm(Psi)
    # (04) relative to B
    phi0 = cond_B(Psi, b, 0.0)
    errB = max(np.linalg.norm(cond_B(Psi, b, t) - expm(-1j * HAS * t) @ phi0) for t in ts)
    nB = [np.linalg.norm(cond_B(Psi, b, t))**2 for t in ts]
    # (05) relative to A: conditional map M(t): C^6 (kernel coords) -> B x S, generator Kt = i M' M^+
    M = lambda t: np.column_stack([cond_A(K[:, j], t) for j in range(K.shape[1])])
    nonherm, gens = [], []
    for t in ts:
        dt = 1e-5
        Md = (M(t + dt) - M(t - dt)) / (2 * dt)
        Kt = 1j * Md @ np.linalg.pinv(M(t))
        nonherm.append(np.linalg.norm(Kt - Kt.conj().T, 2) / 2); gens.append(Kt)
    nA = [np.linalg.norm(cond_A(Psi, t))**2 / np.linalg.norm(cond_A(Psi, 0))**2 for t in ts]
    var = max(np.linalg.norm(G - gens[0], 2) for G in gens)
    res[g] = (errB, max(nB) - min(nB), min(nA), max(nA), min(nonherm), max(nonherm), var)
    print(f"  rel. B: max ||phi(t) - e^(-iH_AS t) phi(0)|| = {errB:.2e}; norm spread {max(nB)-min(nB):.2e}")
    print(f"  rel. A: norm ratio {min(nA):.4f}-{max(nA):.4f}; non-Hermiticity {min(nonherm):.3f}-{max(nonherm):.3f} rad/s;"
          f" generator variation {var:.3f} rad/s")

# (04): exact unitary H_AS evolution relative to uncoupled clock B, for every g
for g in res:
    inequality(f"{res[g][0]}", "<", "1e-10"); inequality(f"{res[g][1]}", "<", "1e-12")
# (05): at g = 0.3, the A-relative dynamics is non-unitary: norm varies and generator non-Hermitian
inequality(f"{res[0.3][3] - res[0.3][2]}", ">", "1e-3")
inequality(f"{res[0.3][5]}", ">", "1e-2")
# limit g -> 0: A becomes an uncoupled clock and non-unitarity disappears
inequality(f"{res[0.0][3] - res[0.0][2]}", "<", "1e-10")
inequality(f"{res[0.0][5]}", "<", "1e-6")
inequality(f"{res[0.01][5]}", "<", f"{res[0.1][5]}")
raise SystemExit(finish())
