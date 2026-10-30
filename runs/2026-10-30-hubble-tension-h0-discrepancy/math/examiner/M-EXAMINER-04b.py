"""M-EXAMINER-04b: scan of GLS constructions, to locate which (if any) gives the lens's 71.47 +- 1.26.
Diagnostic only."""
import sys, math, itertools
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from common import *
from math_checks import inequality, finish

names = ["CCHP", "SBF", "TF", "TD", "MASER", "SIREN"]
ms = [sym(m) for m in (CCHP, SBF, TF, TD, MASER, SIREN)]
x = np.array([m[0] for m in ms]); s = np.array([m[1] for m in ms])
def gls(C):
    Ci = np.linalg.inv(C); o = np.ones(len(x)); W = o @ Ci @ o
    return (o @ Ci @ x) / W, 1 / math.sqrt(W)
best = []
for share in ([0, 1], [0, 1, 2], [0, 1, 4], [0, 1, 2, 4]):
    for f in (0.0145, 0.0145 * 5 / math.log(10), 0.029, 0.0145 * 2):
        for diag in (False, True):
            for mode in ("H_i H_j", "H_mean^2"):
                C = np.diag(s**2)
                for i in share:
                    for j in share:
                        if i == j and not diag: continue
                        C[i, j] += (f * x[i] * f * x[j]) if mode == "H_i H_j" else (f * 71.5)**2
                try:
                    mu, sig = gls(C)
                except Exception:
                    continue
                d = abs(mu - 71.47) + abs(sig - 1.26)
                best.append((d, mu, sig, [names[k] for k in share], round(f, 5), diag, mode))
best.sort(key=lambda t: t[0])
for b in best[:8]:
    print(f"mismatch {b[0]:.3f}: {b[1]:.3f} +- {b[2]:.3f}, share {b[3]}, f {b[4]}, diag {b[5]}, {b[6]}")
# A positively correlated pair can push the GLS mean below the lower member only with large rho; report rho for the stated case
rho = (0.0145 * x[0]) * (0.0145 * x[1]) / (s[0] * s[1])
print("implied correlation coefficient CCHP-SBF (stated case, off-diag only):", rho)
inequality(f"{rho}", "<", "1")
raise SystemExit(finish())
