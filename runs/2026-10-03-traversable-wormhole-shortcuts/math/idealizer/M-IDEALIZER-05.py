"""M-IDEALIZER-05: ANEC along the radial null geodesic of the Ellis throat.

ds^2 = -dt^2 + dl^2 + (b0^2 + l^2) dOmega^2 (G = c = 1). Radial null geodesic k = E (d_t + d_l), E > 0 constant
(t and l are both affine-compatible: Gamma^t_tt = Gamma^l_tt = Gamma^l_ll = 0 here), so dl/dlambda = E, dlambda = dl/E.
ANEC = int T_kk dlambda = E int (T_tt + T_ll) dl.  Claim: -E/(8 b0) (= -0.125 /m at b0 = 1 m, E = 1).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime
from math_checks import identity, limit, sign, quantity, finish

t, l, th, ph = sp.symbols("t l theta phi", real=True)
b0, E = sp.symbols("b0 E", positive=True)
r2 = b0**2 + l**2
st = Spacetime(sp.diag(-1, 1, r2, r2 * sp.sin(th)**2), [t, l, th, ph])
T = st.stress_energy()
Tkk = sp.simplify(E**2 * (T[0, 0] + T[1, 1] + 2 * T[0, 1]))
print("T_kk =", Tkk)
sign(Tkk, "negative", domain={"l": (-10, 10)})
anec = sp.simplify(sp.integrate(Tkk / E, (l, -sp.oo, sp.oo)))
print("ANEC =", anec)
identity(anec, -E / (8 * b0))
# check affinity: k^a nabla_a k^b = 0 for k = (1,1,0,0)
G = st.christoffel()
acc = [sp.simplify(sum(G[bb][aa][cc] for aa in (0, 1) for cc in (0, 1))) for bb in range(4)]
print("geodesic acceleration of k:", acc)
identity(sum(x**2 for x in acc), 0)
# limits: wide throat -> 0 (flat-space ANEC), units 1/length with E dimensionless
limit(anec, "b0", "oo", 0)
print("b0 = 1 m, E = 1:", anec.subs({b0: 1, E: 1}), "per metre")
identity(anec.subs({b0: 1, E: 1}), sp.Rational(-1, 8))
raise SystemExit(finish())
