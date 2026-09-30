"""M-IDEALIZER-03 (F3): Smith-Ahmadi coupling J = H_C + H_S - lam H_C H_S.
Null vectors: for system eigenvalue s and clock eigenvalue c, c + s - lam c s = 0 => c = -s/(1 - lam s).
Conditional amplitude e^{i c t} = e^{-i s/(1-lam s) t} => H_eff = H_S (1 - lam H_S)^-1 (exact, any lam with 1 - lam s != 0).
Gap: depends on the energy zero of H_S. Spectrum {0, 1}: gap 1/(1-lam) (claimed). Spectrum {-1/2, 1/2} (sigma_x/2 of F1): 1/(1 - lam^2/4).
Fidelity vs bare evolution, equal superposition: 1 - F = sin^2(delta_gap t / 2).
lam = hbar G/(c^4 x) with H in rad/s: lam has units of s.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, series, limit, quantity, units, finish

c, s, lam, t = sp.symbols("c s lam t", real=True)
sol = sp.solve(sp.Eq(c + s - lam * c * s, 0), c)[0]
identity("-s/(1 - lam*s)", str(sol), domain={"s": (-3, 3), "lam": (-0.2, 0.2)})
# gap for spectrum {0,1}
gap01 = (1 / (1 - lam)) - 0
identity("1/(1-lam) - 0", "1/(1-lam)", domain={"lam": (0.001, 0.1)})
series("1/(1-lam)", "lam", 0, 2, "1 + lam")          # fractional shift lam*E_S (E_S = 1)
# gap for spectrum {-1/2,1/2}
gapsym = sp.Rational(1, 2) / (1 - lam / 2) + sp.Rational(1, 2) / (1 + lam / 2)
identity("(1/2)/(1-lam/2) + (1/2)/(1+lam/2)", "1/(1 - lam**2/4)", domain={"lam": (0.001, 0.1)})
# general first order: E/(1-lam E) = E + lam E^2 + ...; transition a->b shifts by lam (Eb^2 - Ea^2) = lam (Ea+Eb)(Eb-Ea)
Ea, Eb = sp.symbols("E_a E_b", real=True)
series("E_b/(1-lam*E_b) - E_a/(1-lam*E_a)", "lam", 0, 2, "(E_b - E_a) + lam*(E_b**2 - E_a**2)")
limit(str(sol), "lam", 0, "-s", domain={"s": (-3, 3)})                                 # uncoupled limit: ideal PW (F1)

# numeric: PW construction with a finite clock, spectrum {0,1}, lam = 0.05
lamv = 0.05
HS = np.diag([0.0, 1.0])
# clock levels at the needed values c = -s/(1-lam s) plus spectator levels
cvals = np.array([0.0, -1 / (1 - lamv), 2.0, -2.0, 0.7])
Jm = np.kron(np.diag(cvals), np.eye(2)) + np.kron(np.eye(5), HS) - lamv * np.kron(np.diag(cvals), HS)
w, V = np.linalg.eigh(Jm)
null = V[:, np.abs(w) < 1e-12]
Psi = null @ np.ones(null.shape[1]); Psi2 = Psi.reshape(5, 2)
cond = lambda tt: (np.exp(1j * cvals * tt) / np.sqrt(5)) @ Psi2
p0 = cond(0)
Heff = HS @ np.linalg.inv(np.eye(2) - lamv * HS)
dev = max(np.linalg.norm(cond(tt) - np.diag(np.exp(-1j * np.diag(Heff) * tt)) @ p0) for tt in np.linspace(0, 30, 301))
print("null dim", null.shape[1], "max dev from H_eff evolution", dev)
quantity(f"{1 + dev}", "1", rel_tol=1e-12)
# 1-F vs bare H_S, lam = 1e-3, t = 20, equal superposition, spectrum {0,1}
l3 = 1e-3; tt = 20.0
dgap = 1 / (1 - l3) - 1
F = abs((1 + np.exp(-1j * dgap * tt)) / 2) ** 2
print("1-F =", 1 - F, "sin^2(lam t/2) =", np.sin(l3 * tt / 2) ** 2)
quantity(f"{1 - F}", "1.0e-4", rel_tol=0.03)
# units of lam = hbar G/(c^4 x)
units("hbar * G / (c^4 * 1 mm)", "s")
quantity("hbar * G / (c^4 * 1 mm)", "8.7e-76 s", rel_tol=0.01)
raise SystemExit(finish())
