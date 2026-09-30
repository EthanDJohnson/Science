"""M-IDEALIZER-06 (F6): thermal (modular) time vs relational PW time. hbar = 1, energies rad/s.
PW physical state Psi = sum_n c_n |-E_n>_C |E_n>_S (non-degenerate clock) => rho_S = diag(|c_n|^2).
Modular Hamiltonian K = -ln rho_S; modular flow e^{-iK s} is proportional to e^{-iH_S t} (up to a global phase)
iff K_n - K_0 = beta (E_n - E_0) for one beta, i.e. rho_S is Gibbs. Claim: E = (0,1,3), Gibbs ratios 0.7, 0.7;
weights (0.5,0.2,0.3) give 0.916, 0.170. Any qubit diagonal state with p0 != p1 is Gibbs for some beta.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import quantity, identity, limit, finish

E = np.array([0.0, 1.0, 3.0])
# build the PW state with a clock containing levels -E_n plus spectator levels, check rho_S diagonal
cl = np.array([0.0, -1.0, -3.0, 2.0, 5.0])
HS = np.diag(E)
J = np.kron(np.diag(cl), np.eye(3)) + np.kron(np.eye(5), HS)
w, V = np.linalg.eigh(J)
null = V[:, np.abs(w) < 1e-12]
print("null dim", null.shape[1])
c = np.sqrt(np.array([0.5, 0.2, 0.3]))
# order null basis by system energy: pick component vectors directly
Psi = np.zeros(15, complex)
for n in range(3):
    Psi += c[n] * np.exp(1j * 0.3 * n) * np.kron(np.eye(5)[n], np.eye(3)[n])
print("|J Psi| =", np.linalg.norm(J @ Psi))
quantity(f"{1 + np.linalg.norm(J @ Psi)}", "1", rel_tol=1e-12)
R = Psi.reshape(5, 3)
rhoS = R.T @ R.conj()
off = np.abs(rhoS - np.diag(np.diag(rhoS))).max()
print("rho_S off-diagonal max", off)
quantity(f"{1 + off}", "1", rel_tol=1e-12)

def ratios(p):
    K = -np.log(p)
    return (K[1] - K[0]) / (E[1] - E[0]), (K[2] - K[0]) / (E[2] - E[0])
r = ratios(np.real(np.diag(rhoS)))
print("non-Gibbs ratios", r)
quantity(f"{r[0]}", "0.916", rel_tol=2e-3)
quantity(f"{r[1]}", "0.170", rel_tol=5e-3)
pg = np.exp(-0.7 * E); pg /= pg.sum()
rg = ratios(pg)
print("Gibbs beta=0.7 ratios", rg)
quantity(f"{rg[0]}", "0.7", rel_tol=1e-12)
quantity(f"{rg[1]}", "0.7", rel_tol=1e-12)
# qubit: every diagonal state is Gibbs with beta = ln(p0/p1)/(E1-E0)
p0, E1 = sp.symbols("p0 E1", positive=True)
beta = sp.log(p0 / (1 - p0)) / E1
identity(sp.exp(-beta * E1) / (1 + sp.exp(-beta * E1)), 1 - p0, domain={"p0": (0.05, 0.95), "E1": (0.1, 10)})
# limit: beta -> 0 gives the maximally mixed state (modular flow trivial)
b = sp.symbols("b", positive=True)
limit(sp.exp(-b * 3) / (1 + sp.exp(-b) + sp.exp(-3 * b)), "b", 0, "1/3")
raise SystemExit(finish())
