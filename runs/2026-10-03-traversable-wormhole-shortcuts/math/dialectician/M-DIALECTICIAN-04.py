"""M-DIALECTICIAN-04: 2D CFT vacuum on a twisted loop (t, x) ~ (t + Delta, x + L), 0 <= Delta < L.

Independent derivation: the identification vector (Delta, L) is spacelike; boost to the frame where it
is purely spatial, (0, L'), L' = sqrt(L^2 - Delta^2). There the state is the ordinary Casimir vacuum of
a circle of length L' with energy density rho' = -pi c/(6 L'^2) (known 2D CFT result, central charge c,
hbar = c_light = 1), T'_xx = rho' (traceless), T'_tx = 0. Transform T back to the lab frame and evaluate
on null vectors k_- = d_u, k_+ = d_v with u = t - x, v = t + x (d_u = (d_t - d_x)/2).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, finish

L, D, cc = sp.symbols("L Delta c_cft", positive=True)
v = D / L
g = 1 / sp.sqrt(1 - v**2)
# Lab coords (t, x) = Lambda (t', x'):  t = g(t' + v x'), x = g(x' + v t')
Lam = sp.Matrix([[g, g * v], [g * v, g]])
# check identification vector maps to (Delta, L)
Lp = sp.sqrt(L**2 - D**2)
identity(sp.simplify((Lam * sp.Matrix([0, Lp]))[0]), D, domain={"L": (1, 10), "Delta": (0, 0.99)})
identity(sp.simplify((Lam * sp.Matrix([0, Lp]))[1]), L, domain={"L": (1, 10), "Delta": (0, 0.99)})
rho_p = -sp.pi * cc / (6 * Lp**2)
Tp = sp.Matrix([[rho_p, 0], [0, rho_p]])          # covariant components in rest frame
Linv = Lam.inv()
# T_lab(a, b) = T_rest(Linv a, Linv b) for lab vectors a, b
def Tlab(a, b):
    return sp.simplify((Linv * a).T * Tp * (Linv * b))[0]
k_u = sp.Matrix([sp.Rational(1, 2), -sp.Rational(1, 2)])   # d_u, u = t - x
k_v = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])    # d_v, v = t + x
Tuu, Tvv = Tlab(k_u, k_u), Tlab(k_v, k_v)
print("T_uu =", sp.simplify(Tuu), "   T_vv =", sp.simplify(Tvv), "   T_uv =", sp.simplify(Tlab(k_u, k_v)))
dom = {"L": (1, 10), "Delta": (0, 0.99), "c_cft": (0.1, 10)}
identity(Tuu, -sp.pi * cc / (12 * (L - D)**2), domain=dom)
identity(Tvv, -sp.pi * cc / (12 * (L + D)**2), domain=dom)
identity(Tlab(k_u, k_v), 0, domain=dom)
# Limit Delta -> 0: ordinary Casimir, T_uu = T_vv = -pi c/(12 L^2), rho = T_uu + T_vv = -pi c/(6 L^2)
limit(Tuu, "Delta", 0, -sp.pi * cc / (12 * L**2), direction="+", domain=dom)
# The (L - Delta) chirality is the right-mover (function of u = t - x, moving toward +x), which is the
# direction in which the identification advances time: a +x ray returns after L - Delta.
# Spot value L = 1, Delta = 0.9, c = 1
val = sp.N((-sp.pi / 12) / (1 - 0.9)**2)
print("spot T_-- at L=1, Delta=0.9:", val)
identity(str(round(float(val), 2)), "-26.18")
# Enhancement ratio vs untwisted
identity(Tuu / (-sp.pi * cc / (12 * L**2)), (L / (L - D))**2, domain=dom)
sign(Tuu, "negative", domain=dom)
# Units: in natural units T_uu ~ 1/length^2 (energy per length in 1+1D), as both sides are.
raise SystemExit(finish())
