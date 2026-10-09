"""M-DECOMPOSER-06: MM shortcut ratio T_thru/T_ext = (pi*l/c)/(d/c) = pi*l/d (exterior coordinate times).
Inputs: l = 3e3 ly (quoted, Q-02). Claims: 9.4 at d = 1000 ly; pi at d = l."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, inequality, units, finish

ell, d, c = sp.symbols("ell d c", positive=True)
ratio = (sp.pi * ell / c) / (d / c)
identity(ratio, sp.pi * ell / d)
identity(ratio.subs(d, ell), sp.pi)
quantity(f"(pi * 3e3 ly / c) / (1e3 ly / c)", "9.4", rel_tol=5e-3)
units("(pi * 3e3 ly / c) / (1e3 ly / c)", "dimensionless")
# not a shortcut (ratio > 1) for every d < pi*l, with l held fixed
inequality(sp.pi * ell / d, ">", 1, domain={"ell": (0.1, 10), "d": (0.01, 0.3)})
raise SystemExit(finish())
