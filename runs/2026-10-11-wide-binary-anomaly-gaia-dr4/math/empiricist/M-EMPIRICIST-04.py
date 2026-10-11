"""M-EMPIRICIST-04: same-data gap decomposition and Cookson swing (empiricist F4a, F4c).

gap = gamma_Chae24b - gamma_BoufE2 = 1.37 - 1.045; estimator share = (gamma_E1 - gamma_E2)/gap for the
implied full-median gamma_E1 in [1.12, 1.20]; claims 0.325, 23-48 %, remainder 52-77 %.
Cookson: Bayes factor 1501 for Newton (d<130 pc, ipd=0) and 12 for MOND (d<150 pc, no ipd cut);
swing = log10(1501) + log10(12) = 4.26 dex (both ratios dimensionless). Also 41,760/81,088 = 51.5 %.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, inequality, finish

gap = 1.37 - 1.045
lo, hi = (1.12 - 1.045) / gap, (1.20 - 1.045) / gap
print(f"gap = {gap:.3f}; estimator share {lo:.3f}-{hi:.3f}; remainder {1-hi:.3f}-{1-lo:.3f}")
inequality(f"abs({gap} - 0.325)", "<", "1e-9")
inequality(f"abs({lo} - 0.23)", "<", "0.005")
inequality(f"abs({hi} - 0.48)", "<", "0.005")
# shares add to one; the share is linear and reaches 0 when gamma_E1 = gamma_E2 and 1 when gamma_E1 = gamma_Chae
identity("(g1 - g2)/(gc - g2) + (gc - g1)/(gc - g2)", "1", domain={"g1": (1.0, 1.3), "g2": (0.9, 0.99), "gc": (1.31, 1.6)})
identity(sp.sympify("(g1 - g2)/(gc - g2)").subs("g1", sp.Symbol("gc", positive=True)), "1", domain={"g2": (0.9, 0.99), "gc": (1.31, 1.6)})
swing = math.log10(1501) + math.log10(12)
print(f"Cookson swing = {swing:.4f} dex; frac kept = {41760/81088:.4f}")
inequality(f"abs({swing} - 4.26)", "<", "0.005")
inequality(f"abs({41760/81088} - 0.515)", "<", "0.0005")
raise SystemExit(finish())
