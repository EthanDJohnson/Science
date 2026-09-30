"""M-EMPIRICIST-10: Laplace's rule of succession (Lens output 2). Uniform prior on the rate p, s successes
in n trials: P(next is a success) = (s + 1)/(n + 2). s = 0 new-physics endings; n = 7 sourced, n = 12 with
unsourced cases (dimensionless)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, finish
import sympy as sp

p, n = sp.symbols("p n", positive=True)
# posterior predictive from the Beta(1, n+1) posterior after 0 successes in n trials
pred = sp.integrate(p * (1 - p) ** n, (p, 0, 1)) / sp.integrate((1 - p) ** n, (p, 0, 1))
identity(sp.simplify(pred), 1 / (n + 2))
limit("1/(n + 2)", "n", "oo", "0")
for nn, lens in [(7, 0.11), (12, 0.07)]:
    v = float(pred.subs(n, nn)); print(f"n = {nn}: {v:.4f} (1/{nn+2})")
    agree(f"n={nn}", v, lens, 0.006)
raise SystemExit(finish())
