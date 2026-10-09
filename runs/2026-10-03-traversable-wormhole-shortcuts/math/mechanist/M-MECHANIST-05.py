"""M-MECHANIST-05: 2D CFT (central charge cc) on a loop with twisted identification
(t, x) ~ (t + Delta, x + L), 0 <= Delta < L, hbar = c_light = 1, signature (-,+).

Independent derivation: boost to the frame where the identification vector is purely spatial,
proper length Lp = sqrt(L^2 - Delta^2). There the Casimir vacuum has rho = p = -pi*cc/(6 Lp^2)
(traceless; E_0 = -pi cc/(6 L) on a circle). Transform T back to the lab frame and contract with the
right-moving k_R = (1, 1) and left-moving k_L = (1, -1) null vectors.

Which direction closes: a right-moving ray from (0,0) reaches (L, L) ~ (L - Delta, 0): time advance
per lap L - Delta, closed null curve at Delta = L. A left-moving ray reaches (L, -L) ~ (L + Delta, 0):
advance L + Delta, never closes for Delta > 0. So k_R is the closing direction.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, sign, quantity, finish

L, Dl, cc = sp.symbols("L Delta c_c", positive=True)
beta = Dl / L
gam = 1 / sp.sqrt(1 - beta**2)
Lp = sp.sqrt(L**2 - Dl**2)
# rest -> lab: t = gam (t' + beta x'), x = gam (x' + beta t'); check it maps (0, Lp) to (Delta, L)
ident = sp.Matrix([gam * beta * Lp, gam * Lp])
identity(sp.simplify(ident[0]), Dl, domain={"L": (1, 10), "Delta": (0, 0.99)})
identity(sp.simplify(ident[1]), L, domain={"L": (1, 10), "Delta": (0, 0.99)})
# lab -> rest for vectors: k' = Lambda^{-1} k
Linv = sp.Matrix([[gam, -gam * beta], [-gam * beta, gam]])
rho = -sp.pi * cc / (6 * Lp**2)
Trest = sp.Matrix([[rho, 0], [0, rho]])    # T'_{tt} = rho, T'_{xx} = p = rho (lower indices)

def Tkk(k):
    kp = Linv * sp.Matrix(k)
    return sp.simplify((kp.T * Trest * kp)[0])

TR = Tkk([1, 1])     # closing direction
TL = Tkk([1, -1])    # other direction
dom = {"L": (1, 10), "Delta": (0, 0.99), "c_c": (0.1, 10)}
# Corrected statement: the CLOSING direction has (L + Delta)^-2, the other (L - Delta)^-2
identity(TR, -sp.pi * cc / (3 * (L + Dl)**2), domain=dom)
identity(TL, -sp.pi * cc / (3 * (L - Dl)**2), domain=dom)
# The lens's assignment (closing direction gets (L - Delta)^-2) -- expected to FAIL
r = identity(TR, -sp.pi * cc / (3 * (L - Dl)**2), domain=dom, verbose=False)
print(("CONFIRMED-WRONG" if r.status == "fail" else "LENS-OK") +
      f" lens labelling T_kR = -pi c/(3(L-Delta)^2): status {r.status}"
      + (f", counterexample {r.counterexample}" if r.counterexample else ""))
# limit Delta -> 0: both -> -pi c/(3 L^2)
limit(TR, "Delta", 0, -sp.pi * cc / (3 * L**2))
limit(TL, "Delta", 0, -sp.pi * cc / (3 * L**2))
# energy density in lab frame T_tt; its enhancement over Delta = 0 is the lens's kappa
Ttt = Tkk([1, 0])
kappa = L**2 * (L**2 + Dl**2) / ((L - Dl)**2 * (L + Dl)**2)
identity(Ttt / (-sp.pi * cc / (6 * L**2)), kappa, domain=dom)
# ANEC per lap along the closing ray (affine lambda = t, lap length L in the covering space) stays finite at Delta -> L
anec_lap = TR * L
limit(anec_lap, "Delta", L, -sp.pi * cc / (12 * L), direction="-")
sign(TR, "negative", domain=dom)
# Spot values at MM D/c = 1e3 yr: L = T_w + D/c, Delta = Delta_sc = T_w - D/c
Tw = float(sp.pi * 3000)
Lv, Dv = Tw + 1e3, Tw - 1e3
print(f"INFO MM D/c=1e3 yr: (L/(L-Delta))^2 = {(Lv/(Lv-Dv))**2:.4g} (other direction); "
      f"(L/(L+Delta))^2 = {(Lv/(Lv+Dv))**2:.4g} (closing direction)")
quantity(f"{(Lv/(Lv-Dv))**2}", "27", rel_tol=0.01)
for d, want in [(3e3, "4.3"), (1.0, "2.2e7")]:
    Lv, Dv = Tw + d, Tw - d
    quantity(f"{(Lv/(Lv-Dv))**2}", want, rel_tol=0.02)
    print(f"INFO D/c={d} yr: closing-direction factor (L/(L+Delta))^2 = {(Lv/(Lv+Dv))**2:.4g}")
raise SystemExit(finish())
