"""M-EXAMINER-06: a thick static shell has interior lapse below the thin-shell value at R2.

Geometric units, metres. Static spherical metric ds^2 = -e^{2 Phi(r)} dt^2 + dr^2/(1 - 2 m(r)/r) + r^2 dOmega^2.
Einstein G_rr = 8 pi T_rr with T^r_r = p_r gives Phi' = (m + 4 pi r^3 p_r) / (r (r - 2m)).
Outside R2 the metric is Schwarzschild, so e^{Phi(R2)} = sqrt(1 - 2M/R2). If m + 4 pi r^3 p_r > 0 and
r > 2m in the wall, Phi increases outward, so the cavity lapse e^{Phi(R1)} < sqrt(1 - 2M/R2).
Also g_rr = 1/(1 - 2m/r) >= 1 for m >= 0. The axial coordinate null speed inside R2 is then at most
N(R2) + beta_max (ADM form), so the thin-shell-at-R2 delay is a lower bound.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, finish
from gr_tensors import Spacetime

t, r, th, ph = sp.symbols("t r theta phi", real=True)
Phi, m = sp.Function("Phi"), sp.Function("m")
g = sp.diag(-sp.exp(2*Phi(r)), 1/(1 - 2*m(r)/r), r**2, r**2*sp.sin(th)**2)
st = Spacetime(g, [t, r, th, ph], simplify=True)
Gt = st.einstein()
pr = sp.Symbol("p_r", real=True)
# T_rr = p_r g_rr  (static, diagonal); solve G_rr = 8 pi p_r g_rr for Phi'
eq = sp.Eq(sp.simplify(Gt[1, 1]), 8*sp.pi*pr*g[1, 1])
dPhi = sp.solve(eq, sp.diff(Phi(r), r))[0]
print("Phi'(r) from G_rr:", sp.simplify(dPhi))
mm = sp.Symbol("mm", positive=True)
rr = sp.Symbol("rr", positive=True)
expr = sp.simplify(dPhi.subs(m(r), mm).subs(r, rr))
identity(expr, (mm + 4*sp.pi*rr**3*pr)/(rr*(rr - 2*mm)))
# sign: positive when p_r >= 0 and r > 2m
sign(((mm + 4*sp.pi*rr**3*pr)/(rr*(rr - 2*mm))).subs(pr, sp.Rational(1, 100)).subs(rr, 3*mm), "positive")
# Schwarzschild limit (p_r = 0, m = M const): Phi' = M/(r(r-2M)) is d/dr of ln sqrt(1 - 2M/r)
M = sp.Symbol("M", positive=True)
identity(sp.diff(sp.log(sp.sqrt(1 - 2*M/rr)), rr), M/(rr*(rr - 2*M)))
# Flat limit: m -> 0, p_r -> 0 gives Phi' -> 0
limit((mm + 4*sp.pi*rr**3*pr).subs(pr, 0)/(rr*(rr - 2*mm)), "mm", 0, "0")
# Counterexample direction: sufficiently negative p_r (tension) reverses the sign
sign(((mm + 4*sp.pi*rr**3*pr)/(rr*(rr - 2*mm))).subs({pr: -1, rr: 3, mm: 1}), "negative")
raise SystemExit(finish())
