"""M-DIALECTICIAN-07: toy MMP energetics with a twisted Casimir term.

Toy (lens's stated assumptions): MMP's E(l) = r_e^3/(G l^2) - q/(8 l), where the Casimir term is read
as a 2D CFT on a loop of length l. With a clock offset Delta the loop is identified as
(t, x) ~ (t + Delta, x + l). Energy in the mouths' rest frame = integral over the loop of T_tt
= T_uu + T_vv (T_uv = 0), which from M-04 is  -(K/2) l [ (l - Delta)^-2 + (l + Delta)^-2 ]  with K
fixed so that Delta = 0 gives -q/(8 l): K/2 * 2/l = q/(8l) -> K = q/8.
In units x = l/l0, delta = Delta/l0, energy in units q/(16 l0) (l0 = 16 r_e^3/(G q)):
  f(x) = 1/x^2 - x [ (x - delta)^-2 + (x + delta)^-2 ],  x > delta.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, limit, finish

x, dl = sp.symbols("x delta", positive=True)
re_, G, q, l, D = sp.symbols("r_e G q l Delta", positive=True)
l0 = 16 * re_**3 / (G * q)
E = re_**3 / (G * l**2) - (q / 16) * l * ((l - D)**-2 + (l + D)**-2)
f = 1 / x**2 - x * ((x - dl)**-2 + (x + dl)**-2)
# nondimensionalisation check
identity(sp.simplify(E.subs({l: x * l0, D: dl * l0}) / (q / (16 * l0))), f,
         domain={"x": (0.5, 3), "delta": (0, 0.2), "r_e": (0.1, 10), "G": (0.1, 10), "q": (0.1, 10)})
# Delta = 0 limit reproduces MMP: f = 1/x^2 - 2/x, min at x = 1, f = -1  (E_min = -q/(16 l0) = -G q^2/(256 r_e^3))
limit(f, "delta", 0, "1/x**2 - 2/x", direction="+", domain={"x": (0.5, 3)})
identity((-(q / (16 * l0))), -G * q**2 / (256 * re_**3))

fp = sp.diff(f, x)
fpp = sp.diff(f, x, 2)
for dv, claim in [(0.05, 0.977), (0.10, 0.896)]:
    xs = sp.nsolve(fp.subs(dl, dv), x, 1.0)
    curv = fpp.subs({dl: dv, x: xs})
    print(f"delta = {dv}: local min at x = {float(xs):.4f} (claim {claim}), f'' = {float(curv):.3g}")
    identity(f"{float(xs):.3f}", f"{claim}")
# critical delta: f' = 0 and f'' = 0 simultaneously
# Found by bisection on delta: does f' change sign (- to +) somewhere in (delta, 5]?
fp_l = sp.lambdify((x, dl), fp, "mpmath")
mp.mp.dps = 30
def has_min(dv, n=6000):
    prev = None
    for i in range(n + 1):
        xv = dv + 1e-6 + i * (5 - dv) / n
        val = fp_l(mp.mpf(xv), mp.mpf(dv))
        if prev is not None and prev < 0 <= val:
            return True
        prev = val
    return False
lo, hi = 0.10, 0.20
assert has_min(lo) and not has_min(hi)
for _ in range(30):
    mid = 0.5 * (lo + hi)
    if has_min(mid):
        lo = mid
    else:
        hi = mid
dc = 0.5 * (lo + hi)
# refine x_c: the double root of f' at delta_c (minimum of f' over x)
grid = [dc + 1e-3 + i * (3 - dc) / 20000 for i in range(20001)]
xc = min(grid, key=lambda xx: fp_l(mp.mpf(xx), mp.mpf(dc)))
print(f"critical: delta_c = {dc:.5f}, x_c = {xc:.4f}, f'(x_c) = {float(fp_l(xc, dc)):.2e} (claim delta_c = 0.1495)")
identity(f"{dc:.4f}", "0.1495")
# above delta_c: f' > 0 for all x in (delta, 3] -> f increases with x, i.e. the energy falls
# monotonically as x decreases to delta+ (f -> -oo there)
dv = 0.16
fpn = sp.lambdify(x, fp.subs(dl, dv), "mpmath")
mn = min(fpn(dv + 1e-4 + i * (3 - dv) / 4000) for i in range(4001))
print(f"delta = {dv}: min f'(x) on (delta, 3] = {float(mn):.3g} (> 0 means no stationary point, monotone)")
identity(str(int(mn > 0)), "1")
limit(f.subs(dl, sp.Rational(4, 25)), "x", sp.Rational(4, 25), "-oo", direction="+")
raise SystemExit(finish())
