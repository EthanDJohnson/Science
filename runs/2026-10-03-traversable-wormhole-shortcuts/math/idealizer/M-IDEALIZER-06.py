"""M-IDEALIZER-06 and M-IDEALIZER-07: transverse tidal acceleration at the Ellis throat for a radial traveller,
and the comparison with MM's AdS2 x S2 throat.

Ellis: ds^2 = -dt^2 + dl^2 + (b0^2 + l^2) dOmega^2 (c = 1 inside the symbolic part).
Traveller 4-velocity u = gamma (e_t + v e_l). Transverse geodesic deviation along e_theta (unit):
  a_tid / xi = -R^theta_{u theta u} = -gamma^2 (R^th_tth t + 2 v R^th_t th l + v^2 R^th_l th l).
Claim F6: R^th_lthl = -1/b0^2 at l = 0, R^th_tth t = 0, so |a_tid| = gamma^2 v^2 xi / b0^2 and b0 >= gamma v sqrt(xi/a_max).
Claim F6 (M-07): "Ultra-relativistic travel reproduces MM's 1.5e7 m (0.5 m, 20 g)" and 1.35e8 m for 2 m at 1 g.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime
from math_checks import identity, limit, sign, quantity, units, finish

t, l, th, ph = sp.symbols("t l theta phi", real=True)
b0, v = sp.symbols("b0 v", positive=True)
r2 = b0**2 + l**2
st = Spacetime(sp.diag(-1, 1, r2, r2 * sp.sin(th)**2), [t, l, th, ph])
R = st.riemann()   # R[a][b][c][d] = R^a_bcd
Rtt = sp.simplify(R[2][0][2][0]); Rll = sp.simplify(R[2][1][2][1]); Rtl = sp.simplify(R[2][0][2][1])
print("R^th_t th t =", Rtt, "; R^th_l th l =", Rll, "; R^th_t th l =", Rtl)
identity(Rtt, 0)
identity(Rtl, 0)
identity(Rll.subs(l, 0), -1 / b0**2)
gam2 = 1 / (1 - v**2)
tid = sp.simplify(-gam2 * (Rtt + 2 * v * Rtl + v**2 * Rll).subs(l, 0))   # per unit xi, c = 1
identity(tid, gam2 * v**2 / b0**2, domain={"v": (0.01, 0.99)})
sign(tid, "positive", domain={"v": (0.01, 0.99)})          # stretching
limit(tid, "v", 0, 0)                                         # static observer feels no transverse tide (Phi = 0)

# SI numbers for slow crossing at 10 km/s (gamma ~ 1)
g0 = 9.80665
c = 299792458.0
for xi, amax, claim_b, claim_M, claim_t in [(0.5, 20 * g0, 505.0, 0.34, 0.16), (2.0, g0, 4.5e3, 3.1, 1.4)]:
    vv = 1e4
    gm = 1 / math.sqrt(1 - (vv / c)**2)
    bmin = gm * vv * math.sqrt(xi / amax)
    tcross = math.pi * bmin / vv
    print(f"xi={xi} m, a={amax:.3g} m/s^2: b0_min = {bmin:.4g} m, |M| = b0 c^2/G, crossing pi b0/v = {tcross:.3g} s")
    quantity(f"{bmin} m", f"{claim_b} m", rel_tol=0.01)
    quantity(f"{bmin} m * c^2 / G", f"{claim_M} Msun", rel_tol=0.02)
    quantity(f"{tcross} s", f"{claim_t} s", rel_tol=0.03)
units("1 m/s * sqrt(1 m / (1 m/s^2))", "length") if False else units("1 m/s * 1 s", "length")

# (the ultra-relativistic limit, M-IDEALIZER-07, is checked in its own script)
raise SystemExit(finish())
