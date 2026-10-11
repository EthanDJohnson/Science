"""M-STATISTICIAN-06: Bayes-factor bounds (finding 7, 13, Table 1).
Sellke-Bayarri-Berger bound: B_01 >= -e p ln p for p < 1/e, so max odds against the null = 1/(-e p ln p).
Prior pi needed for posterior 0.5: pi = 1/(1+B). Posterior = B pi / (B pi + 1 - pi). All dimensionless."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, sign, finish
from _h import p2, z2, report

B = lambda p: 1 / (-math.e * p * math.log(p))
post = lambda b, pi: b * pi / (b * pi + 1 - pi)
ok = []
p_loc = p2(3.21)
ok += [report("max odds z=3.21", B(p_loc), 42, 1.5), report("prior needed z=3.21", 1 / (1 + B(p_loc)), 0.023, 0.001)]
p_lee = 1 - (1 - p_loc) ** 10
ok += [report("max odds LEE N=10", B(p_lee), 6.4, 0.15), report("prior LEE", 1 / (1 + B(p_lee)), 0.13, 0.01)]
p_r8 = p2(2.5)
ok += [report("max odds F1 rho=0.8 (z 2.5)", B(p_r8), 6.4, 0.5), report("prior rho=0.8", 1 / (1 + B(p_r8)), 0.14, 0.01)]
ok += [report("Chae+26 local z=4.29", B(p2(4.286)), 1883, 60), report("prior Chae+26", 1 / (1 + B(p2(4.286))), 0.0005, 0.0001)]
for z in (1.75, 1.8, 1.9):
    print(f"  Chae+26 w/o 2 systems z={z}: odds {B(p2(z)):.2f}, prior {1/(1+B(p2(z))):.2f}")
ok.append(report("Chae+26 w/o 2 systems (z 1.8-1.9) ~2.1", B(p2(1.85)), 2.1, 0.15))
ok += [report("Hernandez p=0.012", B(0.012), 6.8, 0.2), report("Hernandez prior", 1 / (1 + B(0.012)), 0.13, 0.01)]
ok += [report("Chae 2025 p2=0.037 odds", B(0.037), 2.4, 0.2), report("Chae 2025 prior", 1 / (1 + B(0.037)), 0.3, 0.03)]
print(f"  Chae 2025 exact p2 at z=2.087: {p2(2.087):.4f}, odds {B(p2(2.087)):.2f}; p giving 2.4:1 is about 0.05")
# Posterior bounds finding 13
ok += [report("post 42, 0.05", post(42, 0.05), 0.69, 0.01), report("post 42, 0.15", post(42, 0.15), 0.88, 0.01),
       report("post 6.4, 0.05", post(6.4, 0.05), 0.25, 0.01), report("post 6.4, 0.15", post(6.4, 0.15), 0.53, 0.01)]
# symbolic: prior needed for posterior 1/2
b, pi = sp.symbols("b pi_", positive=True)
identity(sp.solve(sp.Eq(b * pi / (b * pi + 1 - pi), sp.Rational(1, 2)), pi)[0], 1 / (1 + b))
# limit: the bound -> 1 (no evidence) at p = 1/e
p = sp.symbols("p", positive=True)
limit(-sp.E * p * sp.log(p), "p", 1 / sp.E, 1)
# bound decreasing in p on (0, 1/e): derivative of -e p ln p positive
sign(sp.diff(-sp.E * p * sp.log(p), p), "positive", domain={"p": (1e-8, 0.36)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
