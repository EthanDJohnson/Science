"""M-CONSTRAINTS-08 (F8) and M-CONSTRAINTS-09 (F9) arithmetic.
F8: band density -1/(8 pi r0 Delta), tau0 = f Delta, FR constant 3/(32 pi^2):
  Delta^3 <= 3 r0 l_P^2/(4 pi f^4); claims 1.84e-21 m (r0 = 1 m), 4.5e-19 m (1.5e7 m), 3.9e-16 m (1 ly), f = 0.01.
F9: N >= (b0/b0max)^2 = 4.19e-8 (b0/l_P)^2; N < 1e32 gives b0 <= 7.9e-16 m."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, inequality, finish

r0, D, f, lP = sp.symbols("r0 Delta f l_P", positive=True)
sol = [s for s in sp.solve(sp.Eq(1 / (8 * sp.pi * r0 * D), sp.Rational(3, 32) / sp.pi**2 * lP**2 / (f * D)**4), D) if s.is_positive][0]
identity(sol**3, 3 * r0 * lP**2 / (4 * sp.pi * f**4))
limit(sol, "r0", 0, "0")
lPv = 1.616255e-35
for rv, cl in [(1.0, 1.84e-21), (1.5e7, 4.5e-19), (9.4607e15, 3.9e-16)]:
    v = float(sol.subs({r0: rv, f: sp.Rational(1, 100), lP: lPv}))
    print(f"r0 = {rv:g} m: Delta_max = {v:.4g} m (claimed {cl:g})")
    inequality(abs(v - cl) / cl, "<", 0.02)
quantity("(3 * 1 m * l_P^2 / (4 * 3.14159265 * 1e-8))^(1/3)", "1.84e-21 m", rel_tol=3e-3)
# F9
bmax = (3 / (4 * 3.141592653589793))**0.5 / 1e-4      # in l_P, f = 0.01
coef = 1 / bmax**2
print("coef =", coef, " b0 at N = 1e32:", bmax * 1e16 * lPv, "m")
inequality(abs(coef - 4.19e-8) / 4.19e-8, "<", 0.002)
inequality(abs(bmax * 1e16 * lPv - 7.9e-16) / 7.9e-16, "<", 0.005)
inequality(abs(coef * (1 / lPv)**2 - 1.6e62) / 1.6e62, "<", 0.01)
inequality(abs(coef * (1.5e7 / lPv)**2 - 3.6e76) / 3.6e76, "<", 0.01)
raise SystemExit(finish())
