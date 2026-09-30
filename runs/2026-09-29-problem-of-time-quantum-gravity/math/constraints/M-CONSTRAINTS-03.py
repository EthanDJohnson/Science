"""M-CONSTRAINTS-03: closed-LCDM York-time turning point.

H^2(a) = H0^2 (Om a^-3 + Ok a^-2 + OL), Ok < 0 (closed), OL = 1 - Om - Ok, a(today) = 1.
Claim: dH/da = 0 at a* = 3 Om / (2|Ok|); H_min just below H0 sqrt(OL); with Om = 0.315 and
H0 = 67.4 km/s/Mpc: a* = 472.5, 47.3, 9.45 and t* = 120.5, 79.9, 51.2 Gyr for Ok = -0.001, -0.01, -0.05.
t* is cosmic time since the big bang: t = int_0^a da'/(a' H(a')). Radiation is neglected (as in the claim).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, sign, limit, quantity, finish

a, Om, K = sp.symbols("a Om K", positive=True)   # K = |Ok|
OL = 1 - Om + K
H2 = Om * a**-3 - K * a**-2 + OL
sol = sp.solve(sp.diff(H2, a), a)
print("stationary points:", sol)
identity(sol[0], 3 * Om / (2 * K))
astar = 3 * Om / (2 * K)
# minimum: second derivative positive
sign(sp.simplify(sp.diff(H2, a, 2).subs(a, astar)), "positive", domain={"Om": (0.1, 1), "K": (1e-4, 0.1)})
# H_min^2 - OL = -4 K^3/(27 Om^2) < 0 : "just below H0 sqrt(OL)"
identity(sp.simplify(H2.subs(a, astar) - OL), -4 * K**3 / (27 * Om**2))
# limit K -> 0: a* -> infinity (flat LCDM has no turning point)
limit(1 / astar, "K", 0, "0")

mp.mp.dps = 30
H0 = mp.mpf(67.4) * 1000 / mp.mpf("3.0856775814913673e22")   # 1/s
Gyr = mp.mpf("3.15576e16")
Omv = mp.mpf("0.315")
expect = {"-0.001": (472.5, 120.5), "-0.01": (47.25, 79.9), "-0.05": (9.45, 51.2)}
for oks, (a_exp, t_exp) in expect.items():
    Kv = -mp.mpf(oks)
    OLv = 1 - Omv + Kv
    ast = 3 * Omv / (2 * Kv)
    Hf = lambda x: H0 * mp.sqrt(Omv / x**3 - Kv / x**2 + OLv)
    # integrate in ln a to handle the a -> 0 end: dt = d ln a / H
    tstar = mp.quad(lambda u: 1 / Hf(mp.e**u), [-30, -5, 0, mp.log(ast)]) / Gyr
    print(f"Ok = {oks}: a* = {mp.nstr(ast, 8)}, t* = {mp.nstr(tstar, 8)} Gyr, "
          f"H_min/(H0 sqrt OL) = {mp.nstr(Hf(ast)/(H0*mp.sqrt(OLv)), 12)}")
    quantity(f"{float(ast)}", f"{a_exp}", rel_tol=2e-3)
    quantity(f"{float(tstar)} Gyr", f"{t_exp} Gyr", rel_tol=2e-3)
    # sanity: age today
t0 = mp.quad(lambda u: 1 / (H0 * mp.sqrt(Omv * mp.e**(-3*u) + 1 - Omv)), [-30, -5, 0]) / Gyr
print("flat LCDM age today (Gyr):", mp.nstr(t0, 6))
quantity(f"{float(t0)} Gyr", "13.8 Gyr", rel_tol=1e-2)
raise SystemExit(finish())
