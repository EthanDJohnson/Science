"""M-IDEALIZER-14 (F15): clock C coupled to system S by the Smith-Ahmadi product term, with an ideal reference clock R:
J = H_R + H_C + H_S - lam H_C H_S (hbar = 1, rad/s). Conditioned on R (M-IDEALIZER-01 logic), C x S evolves unitarily with
K = H_C + H_S - lam H_C H_S. (a) Conditioning also on a sharp clock energy c gives unitary S evolution with generator H_S(1 - lam c).
(b) Tracing out C with energy distribution p_c of width dE_C, the S coherence between levels s1, s2 decays as
|sum_c p_c exp(i lam c (s2-s1) t)|; for Gaussian p_c: exp(-(lam dE_C dS t)^2/2), i.e. inverse time scale lam * omega_S * dE_C.
Claim: dephasing "at a rate of order lam omega_S dE_C".
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.linalg import expm
from math_checks import quantity, finish

lam = 0.02; dC = 61
cvals = np.linspace(-15, 15, dC)          # clock energies, rad/s
sigma = 4.0                                # clock energy spread dE_C, rad/s
pc = np.exp(-cvals**2 / (2 * sigma**2)); pc /= pc.sum()
HS = np.diag([0.0, 1.5]); dS = 1.5          # omega_S = 1.5 rad/s
HC = np.diag(cvals)
K = np.kron(HC, np.eye(2)) + np.kron(np.eye(dC), HS) - lam * np.kron(HC, HS)
psiC = np.sqrt(pc).astype(complex); psiS = np.array([1, 1], complex) / np.sqrt(2)
psi0 = np.kron(psiC, psiS)
sd = np.sqrt(np.sum(pc * cvals**2))
tau = 1 / (lam * dS * sd)
for tt in (0.5 * tau, tau, 2 * tau):
    psi = expm(-1j * K * tt) @ psi0
    R = psi.reshape(dC, 2); rho = R.T @ R.conj()
    coh = abs(rho[0, 1]) / 0.5
    pred = np.exp(-(tt / tau) ** 2 / 2)
    print(f"t = {tt/tau:.1f} tau: |coherence| = {coh:.6f}, Gaussian prediction {pred:.6f}")
    quantity(f"{coh}", f"{pred}", rel_tol=1e-2)  # 61-level truncated discrete Gaussian: ~0.4% deviation at 2 tau expected
# (a) sharp clock energy c: conditional S evolution is unitary with generator H_S (1 - lam c)
c0 = 3.0; tt = 7.0
psi = expm(-1j * K * tt) @ np.kron(np.eye(dC)[np.argmin(abs(cvals - c0))], psiS)
R = psi.reshape(dC, 2); s = R[np.argmin(abs(cvals - c0))]
target = expm(-1j * HS * (1 - lam * cvals[np.argmin(abs(cvals - c0))]) * tt) @ psiS
ov = abs(np.vdot(target, s))
print("sharp-clock fidelity", ov**2, "norm", np.linalg.norm(s))
quantity(f"{ov**2}", "1", rel_tol=1e-12)
# limit lam -> 0: no dephasing
Ku = np.kron(HC, np.eye(2)) + np.kron(np.eye(dC), HS)
psi = expm(-1j * Ku * 3 * tau) @ psi0; R = psi.reshape(dC, 2); rho = R.T @ R.conj()
quantity(f"{abs(rho[0,1])/0.5}", "1", rel_tol=1e-10)
raise SystemExit(finish())
