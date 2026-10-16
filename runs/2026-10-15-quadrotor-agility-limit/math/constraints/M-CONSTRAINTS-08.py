"""M-CONSTRAINTS-08: the model-error power law and where it fills the gate clearance
(lens finding F10, candidate CONSTRAINTS-B).

Claim as I state it (SI units):
  (a) An ordinary least-squares fit in log-log of the replayed-flight positional RMSE of [A-18]
      against mean speed gives e_model(v) = c v^k with c = 0.0493 m (m/s)^-k, k = 0.858,
      R^2 = 0.83 for the BEM column and c = 0.0439, k = 1.173, R^2 = 0.89 for the polynomial
      ("Fit") column.  Data (dossier A-18, mean speed in m/s -> RMSE in m):
        BEM:  1.67 -> 0.059, 2.38 -> 0.138, 3.21 -> 0.146, 6.92 -> 0.232
        Fit:  1.67 -> 0.061, 2.38 -> 0.167, 3.21 -> 0.183, 6.92 -> 0.381
  (b) With clearance C = 0.60 m and estimator error e_est = 0.151 m, the budget for model error
      is B = C - e_est = 0.449 m, and the crossing speed is v* = (B/c)^(1/k):
      13.1 m/s (BEM) and 7.3 m/s (Fit).
  (c) Elasticities: d ln v*/d ln c = -1/k  = -1.17 (BEM), -0.85 (Fit);
      d ln v*/d ln C = (1/k) C/(C - e_est) = +1.56 (BEM), +1.14 (Fit).
  (d) Halving c multiplies v* by 2^(1/k): 13.1 -> 29.5 m/s (BEM), 7.3 -> 13.1 m/s (Fit).
Domain: v > 0, c > 0, k > 0, 0 < e_est < C.  The fit is on 1.67-6.92 m/s; (b)-(d) extrapolate.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, quantity, finish


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


def ols_loglog(vs, es):
    """Independent OLS of ln e = ln c + k ln v; returns c, k, R^2."""
    n = len(vs)
    x = [math.log(t) for t in vs]
    y = [math.log(t) for t in es]
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    sxx = sum((xi - mx) ** 2 for xi in x)
    syy = sum((yi - my) ** 2 for yi in y)
    k = sxy / sxx
    c = math.exp(my - k * mx)
    r2 = sxy * sxy / (sxx * syy)
    return c, k, r2


V = [1.67, 2.38, 3.21, 6.92]
E_BEM = [0.059, 0.138, 0.146, 0.232]
E_FIT = [0.061, 0.167, 0.183, 0.381]

print("1. independent log-log OLS of the A-18 replay RMSE")
c_bem, k_bem, r2_bem = ols_loglog(V, E_BEM)
c_fit, k_fit, r2_fit = ols_loglog(V, E_FIT)
print(f"   BEM: c = {c_bem:.5g} m, k = {k_bem:.5g}, R^2 = {r2_bem:.4f}")
print(f"   Fit: c = {c_fit:.5g} m, k = {k_fit:.5g}, R^2 = {r2_fit:.4f}")
approx("c_BEM [m]", c_bem, 0.0493, rel=0.01)
approx("k_BEM", k_bem, 0.858, rel=0.01)
approx("R^2_BEM", r2_bem, 0.83, rel=0.02)
approx("c_FIT [m]", c_fit, 0.0439, rel=0.01)
approx("k_FIT", k_fit, 1.173, rel=0.01)
approx("R^2_FIT", r2_fit, 0.89, rel=0.02)
units("0.0493 m * (10 m/s)^0.858 / (1 m/s)^0.858", "m")

print("2. budget and crossing speed")
C_CLEAR, E_EST = 0.60, 0.151
B = C_CLEAR - E_EST
approx("budget B [m]", B, 0.449, rel=1e-3)
v_bem = (B / c_bem) ** (1.0 / k_bem)
v_fit = (B / c_fit) ** (1.0 / k_fit)
approx("v*(BEM) [m/s]", v_bem, 13.1, rel=0.01)
approx("v*(Fit) [m/s]", v_fit, 7.3, rel=0.015)
quantity(f"{c_bem:.6g} m * {v_bem:.6g}^{k_bem:.6g}", f"{B} m", rel_tol=1e-4)

print("3. elasticities, symbolic")
c, k, Cc, ee = sp.symbols("c k Cc ee", positive=True)
vst = ((Cc - ee) / c) ** (1 / k)
el_c = sp.simplify(sp.diff(vst, c) * c / vst)
el_C = sp.simplify(sp.diff(vst, Cc) * Cc / vst)
print("   d ln v*/d ln c =", el_c, "   d ln v*/d ln C =", el_C)
identity(el_c, -1 / k)
identity(el_C, Cc / (k * (Cc - ee)))
approx("d ln v*/d ln c (BEM)", float(el_c.subs({k: k_bem})), -1.17, rel=0.01)
approx("d ln v*/d ln c (Fit)", float(el_c.subs({k: k_fit})), -0.85, rel=0.01)
approx("d ln v*/d ln C (BEM)", float(el_C.subs({k: k_bem, Cc: C_CLEAR, ee: E_EST})), 1.56, rel=0.01)
approx("d ln v*/d ln C (Fit)", float(el_C.subs({k: k_fit, Cc: C_CLEAR, ee: E_EST})), 1.14, rel=0.01)
# limit: k -> 1 (linear error growth) must give elasticities -1 and C/(C-ee)
limit(el_c, "k", 1, -1)

print("4. halving the model error")
approx("v*(BEM), c/2 [m/s]", v_bem * 2 ** (1 / k_bem), 29.5, rel=0.01)
approx("v*(Fit), c/2 [m/s]", v_fit * 2 ** (1 / k_fit), 13.1, rel=0.015)
identity(((Cc - ee) / (c / 2)) ** (1 / k) / vst, 2 ** (1 / k))
inequality("2**(1/k)", ">", "1", domain={"k": (0.1, 10.0)})

print("5. does the error at 5 m/s leave budget? (the 'below 5 m/s nothing binds' claim)")
approx("e_model(5 m/s) BEM [m]", c_bem * 5.0 ** k_bem, 0.19, rel=0.05)

raise SystemExit(finish())
