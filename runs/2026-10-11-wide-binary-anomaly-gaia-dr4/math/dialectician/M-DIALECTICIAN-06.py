"""M-DIALECTICIAN-06 (F4, F10): veto-ladder extrapolation. Data (DR4, low bin) from the lens's shape log:
(surviving triple fraction t, median gamma). Lens: line through first and last rungs; slopes 0.65-0.75 per unit t;
intercepts 1.004 (Newton f=.2), 1.022 (Newton f=.3), 1.261 (MOND chae2024 f=.2), 1.406 (const 1.4 f=.2).
Here: two-point fit, least-squares fit over all six rungs, and the Newton f=0.1 ladder the lens did not report."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, quantity, finish

L = {
    "Newton f=.1": ([0.101, 0.083, 0.058, 0.035, 0.019, 0.012], [1.028, 1.014, 1.007, 0.994, 0.982, 0.976], None, 0.988),
    "Newton f=.2": ([0.201, 0.169, 0.122, 0.075, 0.042, 0.026], [1.135, 1.106, 1.084, 1.063, 1.039, 1.021], 1.004, 0.988),
    "Newton f=.3": ([0.300, 0.257, 0.191, 0.120, 0.069, 0.044], [1.217, 1.182, 1.151, 1.115, 1.074, 1.051], 1.022, 0.988),
    "MOND f=.2":   ([0.199, 0.167, 0.120, 0.074, 0.041, 0.025], [1.396, 1.373, 1.341, 1.318, 1.300, 1.278], 1.261, 1.255),
    "const1.4 f=.2": ([0.201, 0.169, 0.121, 0.074, 0.042, 0.027], [1.556, 1.526, 1.501, 1.478, 1.451, 1.426], 1.406, 1.364),
}
for name, (t, g, lens_int, notrip) in L.items():
    t = np.array(t); g = np.array(g)
    s2 = (g[0] - g[-1]) / (t[0] - t[-1]); i2 = g[-1] - s2 * t[-1]
    A = np.vstack([t, np.ones_like(t)]).T
    (s_ls, i_ls), res, *_ = np.linalg.lstsq(A, g, rcond=None)
    resid = g - (s_ls * t + i_ls)
    se_i = np.sqrt(np.sum(resid ** 2) / (len(t) - 2) * np.linalg.inv(A.T @ A)[1, 1])
    print(f"{name:14s} two-point slope {s2:.3f} intercept {i2:.4f} | LSQ slope {s_ls:.3f} intercept {i_ls:.4f} "
          f"(se {se_i:.4f}) | lens {lens_int} | same-release no-triple median {notrip}")
    if lens_int is not None:
        quantity(f"{i2}", f"{lens_int}", rel_tol=0.002)
# symbolic: the two-point intercept formula
t1, t2, g1, g2 = sp.symbols("t1 t2 g1 g2", positive=True)
icpt = g2 - (g1 - g2) / (t1 - t2) * t2
identity(icpt, (g2 * t1 - g1 * t2) / (t1 - t2))
# F10: ipd cut 1421 -> 1216 removes 14%
quantity(f"{1 - 1216 / 1421}", "0.144", rel_tol=0.01)
print("fraction removed by ipd cut:", round(1 - 1216 / 1421, 4))
raise SystemExit(finish())
