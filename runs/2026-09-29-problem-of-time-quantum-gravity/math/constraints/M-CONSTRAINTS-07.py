"""M-CONSTRAINTS-07: Smith-Ahmadi gravitational clock coupling.

Newtonian interaction of clock and system energies: -G (E_C/c^2)(E_S/c^2)/x = -lambda E_C E_S, lambda = G/(c^4 x)
(the analysis writes hbar G/(c^4 x) with energies in frequency units; same thing).
Claims (F7): lambda*E_S for the Sr transition (E_S = hbar 2pi 429 THz) = 2.35e-60 at x = 1 mm, 2.35e-63 at 1 m;
reaching 1e-18 needs E_S/x >= 1.2e26 J/m, i.e. 1.3e9 kg per metre; finite model (lambda = 0.05, H_S eigenvalues 0,1):
H_eff = H_S/(1 - lambda H_S), eigenvalues [0, 1.052632], Hermitian; a generic random Hermitian coupling
(g = 0.05, 0.2; dims 6 x 3) leaves no exact null vector of J.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from scipy.linalg import expm
from math_checks import identity, series, quantity, units, finish

quantity("G * (hbar*2*pi*429 THz) / (c^4 * 1 mm)", "2.35e-60", rel_tol=3e-3)
quantity("G * (hbar*2*pi*429 THz) / (c^4 * 1 m)", "2.35e-63", rel_tol=3e-3)
units("G * (hbar*2*pi*429 THz) / (c^4 * 1 mm)", "dimensionless")
quantity("1e-18 * c^4 / G", "1.2e26 J/m", rel_tol=0.02)
quantity("1e-18 * c^2 / G", "1.3e9 kg/m", rel_tol=0.04)
# Constraint H_C + H_S - lam H_C H_S = 0 => H_C (1 - lam H_S) = -H_S => clock "sees" H_eff = H_S (1 - lam H_S)^-1
lam, e = sp.symbols("lam e", positive=True)
Hc = sp.solve(sp.Eq(sp.Symbol("h") + e - lam * sp.Symbol("h") * e, 0), sp.Symbol("h"))[0]
identity(-Hc, e / (1 - lam * e), domain={"lam": (0.001, 0.09), "e": (0, 5)})
series(e / (1 - lam * e), "lam", 0, 2, "e + lam*e**2")       # weak-coupling limit: H_S + lam H_S^2
# Finite model: clock d = 12 equally spaced, system eigenvalues 0, 1 rotated to a random basis
rng = np.random.default_rng(3)
Q, _ = np.linalg.qr(rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2)))
HS = Q @ np.diag([0.0, 1.0]) @ Q.conj().T
l = 0.05
Heff = HS @ np.linalg.inv(np.eye(2) - l * HS)
print("H_eff eigenvalues:", np.linalg.eigvalsh((Heff + Heff.conj().T) / 2), "non-Hermiticity:", np.max(np.abs(Heff - Heff.conj().T)))
quantity(f"{np.max(np.linalg.eigvalsh((Heff + Heff.conj().T) / 2))}", "1.052632", rel_tol=1e-6)
print("PASS H_eff Hermitian" if np.max(np.abs(Heff - Heff.conj().T)) < 1e-14 else "FAIL H_eff Hermitian")
# Direct PW check: clock with a continuum-like spectrum is not needed; test on energy eigenvectors:
# for each system eigenvalue e_k, the coupled constraint is solved by clock energy -e_k/(1 - l e_k).
for ek in [0.0, 1.0]:
    quantity(f"{-(-ek/(1-l*ek)) - ek + l*(-ek/(1-l*ek))*ek + 1}", "1", rel_tol=1e-12)   # constraint residual + 1
# Generic coupling: no null vector
cnt = 0
for g in (0.05, 0.2):
    for trial in range(20):
        HC = np.diag(np.sort(rng.normal(size=6)))
        A3 = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); HS3 = (A3 + A3.conj().T) / 2
        B = rng.normal(size=(18, 18)) + 1j * rng.normal(size=(18, 18)); V = (B + B.conj().T) / 2
        J = np.kron(HC, np.eye(3)) + np.kron(np.eye(6), HS3) + g * V
        smin = np.min(np.abs(np.linalg.eigvalsh(J)))
        cnt += smin < 1e-10
print("PASS generic coupling: no exact null vector in 40 random trials" if cnt == 0 else f"FAIL {cnt} null vectors")
raise SystemExit(finish())
