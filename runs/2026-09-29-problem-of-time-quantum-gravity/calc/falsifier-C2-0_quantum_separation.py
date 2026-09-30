"""Falsifier C2-0: Page-Wootters ideal clock with a Smith-Ahmadi-type gravitational
coupling whose clock-system separation is a QUANTUM, DYNAMICAL degree of freedom.

Units: model units, hbar = 1; energies in rad/s, times in s, lambda in s (lambda*E dimensionless).
Lab value for reference: lambda = hbar G/(c^4 x) = 8.71e-76 s at x = 1 mm (SI) [candidate C2].

Constraint (ideal clock, H_C = p_t, spectrum R):
    C_tot = H_C (x) B + 1 (x) C = 0,
    B = 1 - lambda(x_hat) H_S      (gravitational coupling -lambda(x) H_C H_S),
    C = H_S + K,  K = -J sigma_x on the position qubit (hopping = kinetic term of the separation).
Conditional state psi(t) = <t|Psi> obeys  -i B psi' + C psi = 0  =>  i psi' = H_eff psi,
    H_eff = B^{-1} C.
H_eff is Hermitian iff [B, C] = 0, i.e. iff [lambda(x_hat), K] = 0: c-number geometry (J = 0)
or equal lambda at both positions. Otherwise H_eff is Hermitian only in the B-weighted inner
product <psi|B|psi>.

Checks:
 1. control: J = 0 (fixed, classical separations)  -> H_eff Hermitian, kinematic norm conserved
    (this is the candidate's 'unitary relational redshift').
 2. J != 0 (superposed, dynamical separation) -> anti-Hermitian part nonzero, kinematic norm drifts,
    B-norm conserved.
 3. scaling of anti-Hermitian part with J, d_lambda = lambda2 - lambda1, omega.
 4. exact null-state residual of Psi = int dt |t> psi(t) via finite differences (constraint is solved).
"""
import numpy as np
from scipy.linalg import expm

np.set_printoptions(precision=4, suppress=True)
I2 = np.eye(2)
sx = np.array([[0, 1], [1, 0]], dtype=complex)


def build(omega, lam1, lam2, J):
    HS = np.diag([0.0, omega]).astype(complex)          # system energies 0, omega (rad/s)
    lam = np.diag([lam1, lam2]).astype(complex)          # lambda at the two separations (s)
    B = np.kron(I2, I2) - np.kron(HS, lam)               # ordering: system (x) position
    C = np.kron(HS, I2) + np.kron(I2, -J * sx)
    Heff = np.linalg.solve(B, C)
    return B, C, Heff


def run(omega, lam1, lam2, J, T=40.0, n=2001, label=""):
    B, C, Heff = build(omega, lam1, lam2, J)
    antiH = np.linalg.norm((Heff - Heff.conj().T) / 2, 2)
    comm = np.linalg.norm(B @ C - C @ B, 2)
    psi0 = np.kron(np.array([1, 1]) / np.sqrt(2), np.array([1, 0])).astype(complex)  # system superposed, at x1
    ts = np.linspace(0, T, n)
    kin, bn = [], []
    for t in ts:
        p = expm(-1j * Heff * t) @ psi0
        kin.append(np.vdot(p, p).real)
        bn.append(np.vdot(p, B @ p).real)
    kin, bn = np.array(kin), np.array(bn)
    # null-state residual: -i B psi'(t) + C psi(t) with central differences
    dt = ts[1] - ts[0]
    res = 0.0
    for k in (100, 700, 1500):
        pm = expm(-1j * Heff * ts[k - 1]) @ psi0
        pp = expm(-1j * Heff * ts[k + 1]) @ psi0
        p = expm(-1j * Heff * ts[k]) @ psi0
        r = -1j * B @ ((pp - pm) / (2 * dt)) + C @ p
        res = max(res, np.linalg.norm(r))
    print(f"{label:34s} omega={omega:5.2f} rad/s lam1={lam1:.3f} s lam2={lam2:.3f} s J={J:.3f} rad/s | "
          f"||[B,C]||={comm:.3e}  ||antiHerm(H_eff)||={antiH:.3e} rad/s  "
          f"kin-norm range=[{kin.min():.6f},{kin.max():.6f}]  B-norm drift={bn.max()-bn.min():.2e}  "
          f"null residual={res:.1e}")
    return antiH, kin.max() - kin.min()


print("=== 1. control: classical (fixed) separations, J = 0 ===")
run(1.0, 0.05, 0.20, 0.0, label="c-number geometry")
run(1.0, 0.10, 0.10, 0.5, label="equal lambda (no geometry superp.)")
print("\n=== 2. quantum, dynamical separation (J != 0, lam1 != lam2) ===")
run(1.0, 0.05, 0.20, 0.5, label="superposed geometry")
run(1.0, 0.05, 0.20, 0.1, label="superposed geometry, slow hop")
print("\n=== 3. scaling of anti-Hermitian part (expected ~ J * omega * d_lambda at small lambda) ===")
for (om, l1, l2, J) in [(1.0, 0.0, 0.01, 0.5), (1.0, 0.0, 0.02, 0.5), (1.0, 0.0, 0.01, 1.0), (2.0, 0.0, 0.01, 0.5)]:
    B, C, H = build(om, l1, l2, J)
    a = np.linalg.norm((H - H.conj().T) / 2, 2)
    print(f"omega={om} rad/s dlam={l2-l1} s J={J} rad/s: antiHerm={a:.4e} rad/s, "
          f"ratio a/(J*omega*dlam)={a/(J*om*(l2-l1)):.4f}")
lab = 8.71e-76 * 2 * np.pi * 429e12
print(f"\nLab scale for reference (SI): lambda*omega(optical, 1 mm) = {lab:.3e} (dimensionless) -> "
      f"effect is in-principle, not observable.")
