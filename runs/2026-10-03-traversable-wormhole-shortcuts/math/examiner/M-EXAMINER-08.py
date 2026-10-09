"""M-EXAMINER-08: GJW insertion lead Delta t = R ln(R/(h l_P)), h ~ 1, in units of R.
Lens: 4.6, 23, 138 for R/l_P = 1e2, 1e10, 1e60. Dimensionless (times in units of R/c).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, finish
import sympy as sp

x = sp.symbols("x", positive=True)
identity(sp.log(x**6) , 6 * sp.log(x))     # ln(1e60) = 6 ln(1e10) scaling
limit(sp.log(x) / x, "x", sp.oo, 0)       # lead grows slower than R/l_P
for v, lens in [(1e2, 4.6), (1e10, 23.0), (1e60, 138.0)]:
    val = math.log(v)
    print(f"ln({v:g}) = {val:.4f} (lens {lens})")
    quantity(f"{val}", f"{lens}", rel_tol=4e-3)
raise SystemExit(finish())
