"""M-DIALECTICIAN-06: MMP energy E(l) = r_e^3/(G l^2) - q/(8 l) (hbar = c = 1; quoted Q-10).

Derive the minimum; check |E_min|/M_e = (r_e/l0)^2 with the extremal relation M_e = r_e/G (c = 1),
and the value 1/gamma^2 at gamma = l0/r_e = 2e12 against Q-05's 2.5e-25 (which is E_bin/M_e from
MM's quoted E_bin ~ -5e9 kg and M_e ~ 2.0e34 kg).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, quantity, finish

re_, G, q, l = sp.symbols("r_e G q l", positive=True)
E = re_**3 / (G * l**2) - q / (8 * l)
sols = sp.solve(sp.diff(E, l), l)
print("stationary points:", sols)
l0 = sols[0]
identity(l0, 16 * re_**3 / (G * q))
sign(sp.diff(E, l, 2).subs(l, l0), "positive")      # it is a minimum
Emin = sp.simplify(E.subs(l, l0))
identity(Emin, -G * q**2 / (256 * re_**3))
Me = re_ / G
identity(-Emin / Me, (re_ / l0)**2)
# limits: l -> oo gives E -> 0 (separate extremal BHs); l -> 0 gives +oo (gravitational term wins)
limit(E, "l", "oo", "0")
gamma_ = 2e12
print("1/gamma^2 =", 1 / gamma_**2)
identity(f"{1/gamma_**2}", "2.5e-25")
# Q-05 arithmetic: 5e9 kg / 2.0e34 kg
quantity("5e9 kg / (1.5e7 m * c^2 / G)", "2.5e-25", rel_tol=0.02)
raise SystemExit(finish())
