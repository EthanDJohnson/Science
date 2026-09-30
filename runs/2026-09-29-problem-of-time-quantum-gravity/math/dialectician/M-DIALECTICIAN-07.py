"""M-DIALECTICIAN-07: Newtonian clock-system coupling gives H_eff = H_S (1 - lam H_S)^(-1), Hermitian; lam and lam E at 1 mm.

Constraint (hbar = 1, energies in rad/s): J = H_C + H_S - lam H_C H_S, lam = hbar G/(c^4 x) (s), x > 0 separation.
(Attractive Newtonian interaction -G m_C m_S/x with m = H/c^2.) Energy eigenvalues: eps (clock), E (system), real,
lam E != 1. Physical pairs: eps + E - lam eps E = 0. Conditional state psi_S(t) = sum_E c_E e^{+i eps(E) t}|E>,
i.e. generator -eps(E) = E/(1 - lam E), a real function of H_S -> Hermitian.
Numbers: lam(1 mm) = 8.714e-76 s; lam E for E = h x 429 THz is 2.35e-60 (dimensionless).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, series, limit, quantity, units, finish, Result, _done

def report(name, ok, note=""):
    _done(Result("pass" if ok else "fail", name, "numeric (numpy)", note=note), True)

eps, E, lam = sp.symbols("epsilon E lam", real=True)
sol = sp.solve(sp.Eq(eps + E - lam * eps * E, 0), eps)
print("eps(E) =", sol)
identity(-sol[0], E / (1 - lam * E), domain={"E": (-3, 3), "lam": (-0.1, 0.1)})
series(E / (1 - lam * E), "lam", 0, 3, E + lam*E**2 + lam**2*E**3)
limit(E / (1 - lam * E), "lam", 0, E)

# numeric check in a PW model: clock tuned to contain eps(E) for each system level, generic 3-level H_S
rng = np.random.default_rng(11)
A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); HS = (A + A.conj().T) / 2
l = 0.07
ES, VS = np.linalg.eigh(HS)
epsC = -ES / (1 - l * ES)
extra = np.array([2.3, -1.7, 0.4])                 # non-resonant clock levels
HCd = np.concatenate([epsC, extra])
HC = np.diag(HCd).astype(complex)
Jm = np.kron(HC, np.eye(3)) + np.kron(np.eye(6), HS) - l * np.kron(HC, HS)
w, V = np.linalg.eigh(Jm)
K = V[:, np.abs(w) < 1e-10]
print("dim ker J =", K.shape[1])
psi0 = rng.normal(size=3) + 1j * rng.normal(size=3)
Psi = K @ (K.conj().T @ np.kron(np.ones(6), psi0))
Heff = VS @ np.diag(ES / (1 - l * ES)) @ VS.conj().T
report("H_eff Hermitian", np.allclose(Heff, Heff.conj().T))
def cond(t):
    return np.exp(-1j * HCd * t).conj() @ Psi.reshape(6, 3)
p0 = cond(0.0)
fmin = 1
for t in (0.5, 1.9, 6.0):
    ref = VS @ (np.exp(-1j * ES / (1 - l * ES) * t) * (VS.conj().T @ p0))
    p = cond(t)
    fmin = min(fmin, abs(np.vdot(ref, p)) ** 2 / (np.vdot(ref, ref).real * np.vdot(p, p).real))
    nrm = np.vdot(p, p).real / np.vdot(p0, p0).real
report("conditional evolution = exp(-i H_eff t), norm conserved", 1 - fmin < 1e-10 and abs(nrm - 1) < 1e-10,
       f"min fidelity {fmin:.12f}, norm ratio {nrm:.12f}")

quantity("hbar * G / (c^4 * 1 mm)", "8.714e-76 s", rel_tol=1e-3)
quantity("G * (2 * 3.14159265358979 * hbar * 429 THz) / (c^4 * 1 mm)", "2.35e-60", rel_tol=3e-3)
units("G * (1 J) / (c^4 * 1 m)", "dimensionless")
raise SystemExit(finish())
