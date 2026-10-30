"""M-EXAMINER-04: GLS combination with CCHP and SBF sharing the NGC 4258 anchor error (F3).
Model: covariance C = diag(s_i^2) + rho-term; shared anchor error 1.45% in distance -> 1.45% in H0.
Variant A: off-diagonal only, C_ij = (0.0145 H_i)(0.0145 H_j) for i,j in {CCHP, SBF}, i != j.
Variant B: add the anchor term to diagonals as well (if not already in the quoted errors).
GLS mean = (1^T C^-1 x)/(1^T C^-1 1), var = 1/(1^T C^-1 1)."""
import sys, math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from common import *
from math_checks import identity, quantity, finish

# GLS reduces to inverse-variance weights for diagonal C (2x2 symbolic check)
x1, x2, s1, s2 = sp.symbols("x1 x2 s1 s2", positive=True)
Cd = sp.diag(s1**2, s2**2); one = sp.Matrix([1, 1]); xv = sp.Matrix([x1, x2])
g = (one.T * Cd.inv() * xv)[0] / (one.T * Cd.inv() * one)[0]
identity(g, (x1 / s1**2 + x2 / s2**2) / (1 / s1**2 + 1 / s2**2))

ms = [sym(m) for m in (CCHP, SBF, TF, TD, MASER, SIREN)]
x = np.array([m[0] for m in ms]); s = np.array([m[1] for m in ms])
def gls(C):
    Ci = np.linalg.inv(C); o = np.ones(len(x))
    W = o @ Ci @ o
    return (o @ Ci @ x) / W, 1 / math.sqrt(W)
f = 0.0145
out = {}
for name, diag_add in (("A offdiag only", False), ("B offdiag + diag", True)):
    C = np.diag(s**2)
    a = f * x[0] * f * x[1]
    C[0, 1] = C[1, 0] = a
    if diag_add:
        C[0, 0] += (f * x[0])**2; C[1, 1] += (f * x[1])**2
    mu, sig = gls(C)
    z = (mu - CMB[0]) / math.hypot(sig, CMB[1])
    out[name] = (mu, sig, z)
    print(f"{name}: {mu:.3f} +- {sig:.3f}, z vs CMB-SPA {z:.3f}")
# Variant C: masers also share NGC 4258 (D-32 says so), off-diagonal among CCHP, SBF, MASER
C = np.diag(s**2)
for i in (0, 1, 4):
    for j in (0, 1, 4):
        if i != j: C[i, j] = f * x[i] * f * x[j]
mu, sig = gls(C); print(f"C (+masers share): {mu:.3f} +- {sig:.3f}, z {(mu - CMB[0]) / math.hypot(sig, CMB[1]):.3f}")
mu, sig, z = out["A offdiag only"]
quantity(f"{mu}", "71.47", rel_tol=3e-4); quantity(f"{sig}", "1.26", rel_tol=5e-3); quantity(f"{z}", "3.25", rel_tol=5e-3)
raise SystemExit(finish())
