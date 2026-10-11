"""M-STATISTICIAN-04: correlated combination of F1 and the same-data estimator gap (finding 4).
GLS mean with covariance C_ij = rho s_i s_j (i != j), C_ii = s_i^2: m = (1'C^-1 x)/(1'C^-1 1), var = 1/(1'C^-1 1).
Difference of two correlated estimates: var(x1-x2) = s1^2 + s2^2 - 2 rho s1 s2.  gamma dimensionless."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, sign, finish
from _h import report

x = np.array([1.37, 1.49, 1.32])
s = np.array([(0.095**2 + 0.125**2) ** 0.5, 0.20, 0.115])  # same symmetrised errors as M-03
ok = []
lens = {0.0: (1.364, 0.084, 4.3, 3.7), 0.5: (1.330, 0.111, 3.0, 2.5), 0.8: (1.266, 0.108, 2.5, 2.0)}
for rho, (lm, ls, lz, lt) in lens.items():
    C = rho * np.outer(s, s) + (1 - rho) * np.diag(s**2)
    Ci = np.linalg.inv(C)
    one = np.ones(3)
    var = 1 / (one @ Ci @ one)
    m = var * (one @ Ci @ x)
    sd = var**0.5
    r = x - m
    chi = r @ Ci @ r
    t = (m - 1.045) / (sd**2 + 0.0215**2) ** 0.5
    print(f"rho={rho}: GLS {m:.4f} +- {sd:.4f}, z vs Newton {(m-1)/sd:.2f}, tension vs F2 {t:.2f}, chi2_within {chi:.2f}/2")
    ok += [report(f"GLS mean rho={rho}", m, lm, 0.003), report(f"GLS sd rho={rho}", sd, ls, 0.002),
           report(f"z Newton rho={rho}", (m - 1) / sd, lz, 0.06), report(f"tension F2 rho={rho}", t, lt, 0.06)]
    if rho == 0.8:
        ok.append(report("chi2_within rho=0.8", chi, 1.77, 0.03))
# same-data gap Chae 2024b (stat 0.095) vs Boufourou E2 (0.0215)
for rho, want in [(0, 3.3), (0.5, 3.8), (0.8, 4.1)]:
    sd = (0.095**2 + 0.0215**2 - 2 * rho * 0.095 * 0.0215) ** 0.5
    ok.append(report(f"same-data gap rho={rho}", 0.325 / sd, want, 0.06))
# sensitivity (not a lens number): same gap using Chae's stat+sys 0.157
for rho in (0, 0.8):
    sd = (0.157**2 + 0.0215**2 - 2 * rho * 0.157 * 0.0215) ** 0.5
    print(f"  [sensitivity] gap with Chae stat+sys, rho={rho}: {0.325/sd:.2f} sigma")
# symbolic: var(x1-x2) decreases with rho for s1,s2>0 -> significance rises with rho
r_, a, b = sp.symbols("rho a b", positive=True)
v = a**2 + b**2 - 2 * r_ * a * b
sign(sp.diff(v, r_), "negative", domain={"rho": (0.01, 0.99)})
limit(v, "rho", 1, (a - b) ** 2)   # fully correlated, equal errors cancel
# GLS for two equal-error equicorrelated measurements: var = s^2 (1+rho)/2
s0 = sp.symbols("s0", positive=True)
C2 = sp.Matrix([[s0**2, r_ * s0**2], [r_ * s0**2, s0**2]])
o = sp.Matrix([1, 1])
identity(1 / (o.T * C2.inv() * o)[0], s0**2 * (1 + r_) / 2, domain={"rho": (0.01, 0.99)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
