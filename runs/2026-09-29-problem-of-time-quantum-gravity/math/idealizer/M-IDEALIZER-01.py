"""M-IDEALIZER-01 (F1): ideal Page-Wootters clock gives exact Schrodinger evolution.
Independent construction (hbar = 1, energies in rad/s, times in s).
Claim: for J = H_C x 1 + 1 x H_S with H_C = diag(-3.5..3.5) (d = 8) and H_S = sigma_x/2,
any null vector Psi of J gives conditional states psi(t) = (<t| x 1) Psi, <t| = d^-1/2 sum_n e^{i E_n t} <n|,
with psi(t) = exp(-i H_S t) psi(0) (fidelity 1, constant norm) over one period.
Analytic: i d/dt psi = (<t| H_C x 1) Psi = -(<t| x H_S) Psi ... sign: <t|H_C = -i d/dt <t| => i d/dt psi = -<t|H_C Psi = <t| H_S Psi = H_S psi.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, quantity, finish

d = 8
EC = np.arange(d) - 3.5
sx = np.array([[0, 1], [1, 0]], complex)
HS = 0.5 * sx
J = np.kron(np.diag(EC), np.eye(2)) + np.kron(np.eye(d), HS)
w, V = np.linalg.eigh(J)
null = V[:, np.abs(w) < 1e-12]
print("null-space dimension:", null.shape[1])
rng = np.random.default_rng(7)
Psi = null @ (rng.normal(size=null.shape[1]) + 1j * rng.normal(size=null.shape[1]))
Psi /= np.linalg.norm(Psi)
Psi2 = Psi.reshape(d, 2)

def cond(t):
    bra = np.exp(1j * EC * t) / np.sqrt(d)
    return bra @ Psi2

def U(t):
    ev, ew = np.linalg.eigh(HS)
    return ew @ np.diag(np.exp(-1j * ev * t)) @ ew.conj().T

p0 = cond(0.0)
n0 = np.vdot(p0, p0).real
ts = np.linspace(0, 2 * np.pi, 401)
maxdev = max(np.linalg.norm(cond(t) - U(t) @ p0) for t in ts)
normdev = max(abs(np.vdot(cond(t), cond(t)).real - n0) for t in ts)
fid = min(abs(np.vdot(cond(t) / np.linalg.norm(cond(t)), U(t) @ p0 / np.linalg.norm(p0))) ** 2 for t in ts)
print(f"max |psi(t) - U(t)psi(0)| = {maxdev:.2e}; max |norm - norm0| = {normdev:.2e}; min fidelity = {fid:.15f}")
quantity(f"{1 + maxdev}", "1", rel_tol=1e-12)
quantity(f"{fid}", "1", rel_tol=1e-12)
quantity(f"{1 + normdev}", "1", rel_tol=1e-12)

# symbolic proof of the generator for a general diagonal clock level: component n of Psi obeys (E_n + H_S) Psi_n = 0
t, En, lam_s = sp.symbols("t E_n lambda_s", real=True)
# along a system eigenvector with eigenvalue lam_s, a null vector needs E_n = -lam_s; the conditional amplitude is e^{i E_n t}:
amp = sp.exp(sp.I * (-lam_s) * t)
identity(sp.I * sp.diff(amp, t), lam_s * amp)   # i d/dt psi = lam_s psi, i.e. Schrodinger with H_S
# limit: at t -> 0 the conditional state reduces to psi(0)
limit(sp.Abs(amp), "t", 0, "1")
raise SystemExit(finish())
