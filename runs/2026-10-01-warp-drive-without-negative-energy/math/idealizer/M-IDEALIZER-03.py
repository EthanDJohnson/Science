"""M-IDEALIZER-03: static thin shell (F3). Geometric units G = c = 1.
Flat interior, Schwarzschild exterior f = 1 - 2M/r, static shell at r = R, 0 < 2M/R < 1.
Own derivation: K_ab = -Gamma^r_ab n_r with n_r = 1/sqrt(f); Lanczos S^a_b = -(1/8pi)([K^a_b] - delta [K]).
Claims: sigma = (1 - sqrt(1-2M/R))/(4 pi R); p = [(1 - M/R)/sqrt(1-2M/R) - 1]/(8 pi R);
p/sigma = 0.056 (x = 1/3), 0.183 (x = 2/3); DEC p <= sigma iff x <= 24/25; NEC, WEC, SEC for x < 1.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, inequality, series, quantity, finish

t, r, th, ph, M, R = sp.symbols("t r theta phi M R", positive=True)
xx = sp.symbols("x", positive=True)

def Kmixed(f):
    co = [t, r, th, ph]
    g = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
    gi = g.inv()
    def Gam(a, b_, c):
        return sum(gi[a, d]*(sp.diff(g[d, b_], co[c]) + sp.diff(g[d, c], co[b_]) - sp.diff(g[b_, c], co[d]))/2 for d in range(4))
    nr = 1/sp.sqrt(f)
    Ktt = -Gam(1, 0, 0)*nr
    Kthth = -Gam(1, 2, 2)*nr
    return sp.simplify((gi[0, 0]*Ktt).subs(r, R)), sp.simplify((gi[2, 2]*Kthth).subs(r, R))

Kt_out, Kth_out = Kmixed(1 - 2*M/r)
Kt_in, Kth_in = Kmixed(sp.Integer(1) + 0*r)
dKt, dKth = Kt_out - Kt_in, Kth_out - Kth_in
trK = dKt + 2*dKth
sigma = sp.simplify((1/(8*sp.pi))*(dKt - trK))      # -S^t_t = sigma
p = sp.simplify(-(1/(8*sp.pi))*(dKth - trK))         # S^th_th = p
dom = {"M": (0.01, 4.99), "R": (10, 10)}
sig_claim = (1 - sp.sqrt(1 - 2*M/R))/(4*sp.pi*R)
p_claim = ((1 - M/R)/sp.sqrt(1 - 2*M/R) - 1)/(8*sp.pi*R)
identity(sigma, sig_claim, domain=dom)
identity(p, p_claim, domain=dom)

# in terms of x = 2M/R, R = 1
sx = (1 - sp.sqrt(1 - xx))/(4*sp.pi); px = ((1 - xx/2)/sp.sqrt(1 - xx) - 1)/(8*sp.pi)
d01 = {"x": (1e-6, 1 - 1e-9)}
sign(sx, "positive", domain=d01)
sign(px, "positive", domain=d01)                     # p > 0 -> NEC, WEC, SEC follow
sign(sx + px, "positive", domain=d01)
sign(sx + 2*px, "positive", domain=d01)
inequality(px, "<=", sx, domain={"x": (1e-6, 0.96)})
inequality(px, ">", sx, domain={"x": (0.9601, 1 - 1e-9)})
sols = sp.solve(sp.Eq(px, sx), xx)
print("DEC boundary p = sigma at x =", sols)
identity(sp.nsimplify(sols[0]), sp.Rational(24, 25))
for xv, claim in [(sp.Rational(1, 3), 0.056), (sp.Rational(2, 3), 0.183)]:
    v = float((px/sx).subs(xx, xv))
    print(f"p/sigma at 2M/R = {xv}: {v:.4f} (claim {claim})")
    quantity(f"{v}", f"{claim}", rel_tol=0.01)
# Newtonian limit: sigma -> M/(4 pi R^2), p -> M^2/(16 pi R^3) at leading order
series(sigma.subs(R, 1), "M", 0, 2, "M/(4*pi)")
series(p.subs(R, 1), "M", 0, 3, "M**2/(16*pi)")
raise SystemExit(finish())
