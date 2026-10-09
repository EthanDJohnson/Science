"""M-ENGINEER-13: simulator gate count n_g = 2 k N^2 n_T (lens's model, k = 4, n_T = 10) and the error per gate
for circuit fidelity 1/2 under independent errors: (1 - eps)^n_g = 1/2 -> eps = 1 - 2^(-1/n_g) ~ ln2/n_g.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

n = sp.symbols("n", positive=True)
epsn = 1 - 2**(-1 / n)
limit(epsn * n, "n", "oo", sp.log(2))
Nq = sp.symbols("Nq", positive=True)
identity(sp.log(2 * 4 * (2 * Nq)**2 * 10) - sp.log(2 * 4 * Nq**2 * 10), sp.log(4))  # doubling N: x4
for N in (20, 50, 100):
    g = 2 * 4 * N**2 * 10
    print(f"N={N}: gates={g}, log10(g/164)={math.log10(g/164):.2f}, eps={1-2**(-1/g):.3e}, log10(eps_demo/eps)={math.log10((1-2**(-1/164))/(1-2**(-1/g))):.2f}")
quantity(f"{1-2**(-1/164)} m/m", "4.2e-3 m/m", rel_tol=1e-2)
quantity(f"{1-2**(-1/32000)} m/m", "2.2e-5 m/m", rel_tol=2e-2)
quantity(f"{1-2**(-1/800000)} m/m", "8.7e-7 m/m", rel_tol=1e-2)
quantity(f"{math.log10(32000/164)} m/m", "2.3 m/m", rel_tol=1e-2)
quantity(f"{math.log10(800000/164)} m/m", "3.7 m/m", rel_tol=1e-2)
quantity(f"{math.log10(4)} m/m", "0.6 m/m", rel_tol=1e-2)
raise SystemExit(finish())
