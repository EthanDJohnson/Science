"""M-EXAMINER-08 (F6, F7, F5): arithmetic on medians the lens's simulation printed (dimensionless).
gamma_app from a median-v~ comparison = (median_test / median_template)^2.
F6: Newton, no triples, 0.5585 (5-30 kau) vs 0.5304 (300-700 au) -> 1.109.
F7: Newton 0.5583 -> MOND chae2024 0.6307 at 5-30 kau -> 1.276.
Expected value range for F7 from the chae2024 boost itself over 5-30 kau (M ~ 0.93-1.5 Msun) for comparison.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, sign, finish

identity(sp.Float(round((0.5585 / 0.5304) ** 2, 3)), sp.Float(1.109))
identity(sp.Float(round((0.6307 / 0.5583) ** 2, 3)), sp.Float(1.276))
m, k = sp.symbols("m k", positive=True)
identity((k * m / m) ** 2, k**2)                 # scale-free: a pure velocity boost b gives gamma_app = b^2
limit(((m + k) / m) ** 2, "k", 0, "1")
# chae2024 boost over the 5-30 kau zone at M = 0.93 and 1.5 Msun (g_N = G M / s^2, r = s here)
def nu1(y): return 0.5 + math.sqrt(0.25 + 1 / y)
def K1(y):
    w = math.sqrt(1 + 4 / y); return -2 / y / (w * (1 + w))
def gam(gN, a0=1.2e-10, beta=1.1, p=1.2, xe=1.90):
    y = gN / a0; ye = xe**2 / (1 + xe); yb = math.sqrt(y**2 + (beta * ye)**2)
    return nu1(yb) * (1 + math.tanh(beta * ye / y)**p * K1(yb) / 3)
G, Ms, au = 6.6743e-11, 1.98892e30, 1.495978707e11
for Mx in (0.93, 1.5):
    vals = [gam(G * Mx * Ms / (s * au) ** 2) for s in (5000, 10000, 30000)]
    print(f"M = {Mx} Msun: chae2024 gamma at s = 5, 10, 30 kau: " + ", ".join(f"{v:.3f}" for v in vals))
sign(sp.Float(1.33 - 1.276), "positive")          # diluted core shift lies below the injected plateau
raise SystemExit(finish())
