"""M-DIALECTICIAN-08: generic clock-system coupling g X_C x sigma_z gives a non-Hermitian (non-unitary) conditional generator.

Model (hbar = 1): d = 6 clock H_C = diag(k - 5/2) (1 rad/s), X_C = nearest-neighbour hopping, H_S = sigma_x/2, g = 0.2 rad/s.
J = H_C x 1 + 1 x H_S + g X_C x sigma_z. If ker J is empty, retune H_S -> H_S - s 1 with s the eigenvalue of J
closest to 0 (as the lens's toolkit run reports). Conditional psi(t) = <t|Psi>, |t> = sum e^{-i eps t}|k>.
Effective generator: i dpsi/dt = G psi with G = i M'(t) M(t)^+ on the range of M(t) = <t|K (K basis of ker J).
Non-unitarity diagnostic: d/dt ||psi||^2 != 0 and ||P (G - G^dag) P||. Claim: ~1e-3 rad/s (up to 1.1e-3).
Independent: dM/dt by central finite differences, not by the analytic H_C trick.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import finish, Result, _done

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric (numpy)", note=note), True)

d, g = 6, 0.2
eps = np.arange(d) - (d - 1) / 2
X = np.diag(np.ones(d - 1), 1) + np.diag(np.ones(d - 1), -1)
sx = np.array([[0, 1], [1, 0]], complex); sz = np.diag([1.0, -1.0])
def build(shift):
    return np.kron(np.diag(eps), np.eye(2)) + np.kron(np.eye(d), sx / 2 - shift * np.eye(2)) + g * np.kron(X, sz)
J = build(0.0)
w = np.linalg.eigvalsh(J)
print("min |eig J| (no retune):", np.min(np.abs(w)))
shift = 0.0
if np.min(np.abs(w)) > 1e-9:
    shift = w[np.argmin(np.abs(w))]
    J = build(shift)
w, V = np.linalg.eigh(J)
K = V[:, np.abs(w) < 1e-9]
print("retune shift =", shift, "rad/s; dim ker J =", K.shape[1])
Kr = K.reshape(d, 2, -1)
def M(t):
    return np.einsum("c,csr->sr", np.exp(-1j * eps * t).conj(), Kr)
h = 1e-5
nh = []
for t in (0.0, 0.5, 1.0, 2.0, 3.0):
    Mt = M(t)
    dM = (M(t + h) - M(t - h)) / (2 * h)
    Mp = np.linalg.pinv(Mt)
    Gm = 1j * dM @ Mp
    PR = Mt @ Mp
    nh.append(np.linalg.norm(PR @ (Gm - Gm.conj().T) @ PR, 2))
    psi = Mt[:, 0]
    n0 = np.vdot(psi, psi).real
    dn = (np.vdot(M(t + h)[:, 0], M(t + h)[:, 0]).real - np.vdot(M(t - h)[:, 0], M(t - h)[:, 0]).real) / (2 * h)
    print(f"t = {t}: nonHermiticity {nh[-1]:.4g} rad/s, d ln||psi||^2/dt = {dn/n0:.4g} /s")
report("effective generator is non-Hermitian (non-unitary) for g = 0.2", max(nh) > 1e-6, f"max {max(nh):.3g} rad/s")
report("size ~1e-3 rad/s (max between 0.3e-3 and 3e-3)", 3e-4 < max(nh) < 3e-3, f"values {[f'{x:.3g}' for x in nh]}")
# control: g = 0 must give Hermitian generator
g0 = g; g = 0.0
J0 = build(0.0); w0, V0 = np.linalg.eigh(J0); K0 = V0[:, np.abs(w0) < 1e-9]; Kr0 = K0.reshape(d, 2, -1)
M0 = lambda t: np.einsum("c,csr->sr", np.exp(-1j * eps * t).conj(), Kr0)
Mt = M0(0.7); dM = (M0(0.7 + h) - M0(0.7 - h)) / (2 * h); Mp = np.linalg.pinv(Mt); Gm = 1j * dM @ Mp; PR = Mt @ Mp
c0 = np.linalg.norm(PR @ (Gm - Gm.conj().T) @ PR, 2)
report("control g = 0: generator Hermitian", c0 < 1e-8, f"{c0:.2e}")
raise SystemExit(finish())
