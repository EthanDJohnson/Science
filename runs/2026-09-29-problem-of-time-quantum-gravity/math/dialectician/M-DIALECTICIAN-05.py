"""M-DIALECTICIAN-05: log-log time slopes of decoherence exponents: GPP 2/3, Pikovski 2, Markovian 1; GPP ~ w^2.

Exponents Gamma(T) with -ln(visibility) = Gamma:
  GPP: a T^(2/3) w^2 (a > 0); Pikovski (quoted Gaussian form): (T/tau)^2; Markov (constant-rate Lindblad): r T.
Slope = d ln Gamma / d ln T. Regime check for Pikovski: the exact thermal-oscillator form
  -ln V = n ln(1 + (T/(sqrt(n) tau))^2) has slope 2 only for T << sqrt(n) tau (slope -> 0 at large T).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

T, a, w, tau, r, n = sp.symbols("T a omega tau r n", positive=True)
def slope(G):
    return sp.simplify(T * sp.diff(G, T) / G)
identity(slope(a * T ** sp.Rational(2, 3) * w**2), sp.Rational(2, 3))
identity(slope((T / tau) ** 2), 2)
identity(slope(r * T), 1)
Ggpp = a * T ** sp.Rational(2, 3) * w**2
identity(Ggpp.subs(w, 2 * w) / Ggpp, 4)                     # doubling the splitting quadruples the exponent
# Pikovski-type regime: slope of n ln(1 + T^2/(n tau^2))
Gp = n * sp.log(1 + T**2 / (n * tau**2))
limit(slope(Gp), "T", 0, "2")
limit(slope(Gp), "T", sp.oo, "0")
limit(Gp, "n", sp.oo, "T**2/tau**2")                         # large-n limit is the Gaussian form
raise SystemExit(finish())
