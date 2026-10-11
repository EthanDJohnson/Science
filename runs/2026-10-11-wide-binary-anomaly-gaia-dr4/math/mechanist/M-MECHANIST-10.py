"""M-MECHANIST-10 (SPECULATIVE physics, MOND): γ_MOND(g_N) in the form the lens used (Chae 2024 eq. 22 form, per the run tool's docstring):
γ = ν(y_b) [1 + tanh(β y_e / y)^p K(y_b)/3], y = g_N/a0, y_b = sqrt(y^2 + (β y_e)^2), K = dln ν/dln y,
y_e the Newtonian-equivalent external field: y_e ν(y_e) = x_e = g_ext/a0. ν_n(y) = [(1 + sqrt(1 + 4 y^-n))/2]^(1/n)
(n = 1 'simple', n = 2 'standard'). a0 = 1.2e-10 m s^-2, g_ext = (232.8 km/s)^2/(8.2 kpc) (SI), β = 1, p = 1.2.
Lens: γ(1e-10) = 1.3748 (simple), 1.0608 (standard); EF limit η = ν_e(1 + K_e/3) = 1.4228, range ν_e(1+K_e/2)..ν_e = 1.354..1.560.
Independent: K by symbolic differentiation; y_e by numerical root-finding (not the closed form)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp, mpmath as mp
from math_checks import quantity, limit, identity, finish
mp.mp.dps = 30
y = sp.symbols("y", positive=True)
def nu(n): return ((1 + sp.sqrt(1 + 4 * y**(-n))) / 2) ** sp.Rational(1, n)
KPC = 1e3 * 1.495978707e11 * 648000 / mp.pi
a0 = mp.mpf("1.2e-10"); gext = mp.mpf(232.8e3)**2 / (mp.mpf("8.2") * KPC); xe = gext / a0
print(f"g_ext = {mp.nstr(gext, 6)} m/s^2, x_e = {mp.nstr(xe, 6)}")
res = {}
for n, lens in ((1, 1.3748), (2, 1.0608)):
    nun = nu(n); K = sp.simplify(sp.diff(sp.log(nun), y) * y)
    fnu = sp.lambdify(y, nun, "mpmath"); fK = sp.lambdify(y, K, "mpmath")
    ye = mp.findroot(lambda t: t * fnu(t) - xe, xe)
    yy = mp.mpf("1e-10") / a0
    yb = mp.sqrt(yy**2 + ye**2)
    g = fnu(yb) * (1 + mp.tanh(ye / yy) ** mp.mpf("1.2") * fK(yb) / 3)
    eta = fnu(ye) * (1 + fK(ye) / 3)
    print(f"n = {n}: y_e = {mp.nstr(ye, 6)} (closed form x^2/(1+x^n)^(1/n) = {mp.nstr(xe**2/(1+xe**n)**(mp.mpf(1)/n), 6)}), "
          f"γ(1e-10) = {mp.nstr(g, 6)} (lens {lens}); η = {mp.nstr(eta, 6)}, perp {mp.nstr(fnu(ye)*(1+fK(ye)/2), 6)}, par {mp.nstr(fnu(ye), 6)}")
    quantity(mp.nstr(g, 12), f"{lens}", rel_tol=2e-4)
    res[n] = (fnu(ye), fK(ye), eta)
    # limits: K -> -1/2 deep MOND (y -> 0), K -> 0 Newtonian; ν -> 1 Newtonian
    limit(K, "y", 0, "-1/2"); limit(nun, "y", sp.oo, "1")
nue, Ke, eta = res[1]
quantity(mp.nstr(eta, 12), "1.4228", rel_tol=2e-4)
quantity(mp.nstr(nue * (1 + Ke / 2), 12), "1.354", rel_tol=1e-3)
quantity(mp.nstr(nue, 12), "1.560", rel_tol=1e-3)
# isolated deep-MOND limit (g_ext = 0, tanh factor -> 0 when y_e = 0): γ -> ν(y) ~ y^-1/2
limit(nu(1) * sp.sqrt(y), "y", 0, "1")
# simple-ν inverse: y ν(y) = x  <=>  y = x^2/(1+x)
x = sp.symbols("x", positive=True)
identity(sp.simplify((x**2 / (1 + x)) * nu(1).subs(y, x**2 / (1 + x))), x)
raise SystemExit(finish())
