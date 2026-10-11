"""M-STATISTICIAN-11: conversions used for the inputs (Table 1, finding 3, cand C). Dimensionless.
Gamma = log10 sqrt(gamma) -> gamma = 10^(2 Gamma); alpha_grav -> gamma = 1 + alpha (gamma_M - 1)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish
from _h import report

g = lambda G: 10 ** (2 * G)
ok = []
ok.append(report("Chae24b Gamma 0.068", g(0.068), 1.37, 0.005))
ok.append(report("Chae23a sample Gamma 0.059 (lens 1.31)", g(0.059), 1.31, 0.005))
for G, want in [(0.042, 1.21), (0.085, 1.48)]:
    ok.append(report(f"Chae+26 w/o 2 systems Gamma {G}", g(G), want, 0.01))
# Banik alpha -> gamma with gamma_M = 1.44
a, gm = -0.021, 1.44
ok += [report("Banik central", 1 + a * (gm - 1), 0.99, 0.002), report("Banik +err", 0.065 * (gm - 1), 0.03, 0.002),
       report("Banik -err", 0.045 * (gm - 1), 0.02, 0.001)]
al, gM = sp.symbols("alpha gamma_M", positive=True)
lin = 1 + al * (gM - 1)
limit(lin, "alpha", 0, 1)
limit(lin, "alpha", 1, gM)
G0 = sp.symbols("G0", real=True)
identity(sp.log(sp.sqrt(10 ** (2 * G0)), 10), G0, domain={"G0": (-1, 1)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
