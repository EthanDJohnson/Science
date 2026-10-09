"""M-CONSTRAINTS-12 (F14). hbar = c = 1, G = l_P^2.
Claims: E(l) = r_e^3/(G l^2) - q/(8 l) has minimum at l = 16 r_e^3/(G q), E_min = -G q^2/(256 r_e^3),
E'' = G^3 q^4/(32768 r_e^9) > 0. 2D Casimir on a periodic circle of circumference L, central charge c (c_L = c_R):
E0 = -pi c/(6 L); with c = q, L = pi l: E0 = -q/(6 l), ratio to -q/(8l) is 4/3. Per loop null-energy integral
for k = d_t + d_x: int_0^L T_kk dx = -pi c/(3L); n wraps give -n pi c/(3L)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, finish

l, re, G, q, c, L, n = sp.symbols("l r_e G q c L n", positive=True)
E = re**3 / (G * l**2) - q / (8 * l)
crit = sp.solve(sp.diff(E, l), l)
print("critical l:", crit)
identity(crit[0], 16 * re**3 / (G * q))
identity(sp.simplify(E.subs(l, crit[0])), -G * q**2 / (256 * re**3))
E2 = sp.simplify(sp.diff(E, l, 2).subs(l, crit[0]))
identity(E2, G**3 * q**4 / (32768 * re**9))
sign(E2, "positive")
limit(E, "l", "oo", "0")
# dimension check: G (length^2) q^2 / r_e^3 -> 1/length = energy in hbar = c = 1
Lsym = sp.symbols("Len", positive=True)
identity(sp.simplify((Lsym**2 / Lsym**3) * Lsym), sp.Integer(1))
# 2D Casimir, independent: zeta-regularised sum over modes k_m = 2 pi m / L, both chiralities, c free bosons
m = sp.symbols("m", positive=True, integer=True)
E0 = c * 2 * sp.Rational(1, 2) * (2 * sp.pi / L) * sp.zeta(-1)      # c * sum_{m} 2 * (1/2) * k_m, zeta(-1) = -1/12
identity(sp.simplify(E0), -sp.pi * c / (6 * L))
identity(sp.simplify(E0.subs({c: q, L: sp.pi * l})), -q / (6 * l))
identity(sp.simplify((-q / (6 * l)) / (-q / (8 * l))), sp.Rational(4, 3))
rho = E0 / L
Tkk = 2 * rho                        # traceless: p = rho; T_kk = rho + 2 T_tx + p, T_tx = 0 in the static state
identity(sp.simplify(Tkk * L), -sp.pi * c / (3 * L))
identity(sp.simplify(n * Tkk * L), -n * sp.pi * c / (3 * L))
sign(-n * sp.pi * c / (3 * L), "negative")   # grows without bound in n (linear)
raise SystemExit(finish())
