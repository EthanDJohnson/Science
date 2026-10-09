"""M-CONSTRAINTS-10 (F10, F11). Heaviside-Lorentz, hbar = c = 1, G = l_P^2.
Dirac quantisation (HL): g * g_m = 2 pi q. Extremal magnetic RN: r_e^2 = G g_m^2/(4 pi).
Claims: r_e = sqrt(pi) q l_P / g; l_B = 1/sqrt(g B(r_e)) = r_e sqrt(2/q), B = g_m/(4 pi r^2);
q = 1.59e41 at r_e = 1.5e7 m, g = 0.3028; l_B = 5.3e-14 m there; q = 2.1e15, l_B = 6.2e-27 m at r_e = 2e-19 m;
tau0/l_B = 0.01 r_e/l_B 'exceeds by 1e18 to 1e6'. F11: r_e linear in q makes l = 16 r_e^3/(G q) scale as q^2;
r_e ~ sqrt(q) would make it scale as q^(1/2)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, units, finish

q, g, lP = sp.symbols("q g l_P", positive=True)
gm = 2 * sp.pi * q / g
re = sp.sqrt(lP**2 * gm**2 / (4 * sp.pi))
identity(re, sp.sqrt(sp.pi) * q * lP / g)
B = gm / (4 * sp.pi * re**2)
lB = 1 / sp.sqrt(g * B)
identity(lB, re * sp.sqrt(2 / q))
inequality(abs(sp.sqrt(4 * sp.pi / 137.035999) - 0.3028) / 0.3028, "<", 1e-3)   # g = e in HL units
lPv = 1.616255e-35; gv = 0.3028
for rv, qcl, lcl in [(1.5e7, 1.59e41, 5.3e-14), (2e-19, 2.1e15, 6.2e-27)]:
    qv = rv * gv / (3.141592653589793**0.5 * lPv)
    lBv = rv * (2 / qv)**0.5
    ratio = 0.01 * rv / lBv
    print(f"r_e = {rv:g} m: q = {qv:.4g}, l_B = {lBv:.4g} m, tau0/l_B = {ratio:.3g}")
    inequality(abs(qv - qcl) / qcl, "<", 0.01)
    inequality(abs(lBv - lcl) / lcl, "<", 0.01)
    inequality(ratio, ">", 1e5)
# F11 scaling of l = 16 r_e^3/(G q)
k = sp.symbols("k", positive=True)
ell_lin = 16 * (k * q)**3 / (lP**2 * q)
ell_sqrt = 16 * (k * sp.sqrt(q))**3 / (lP**2 * q)
identity(sp.simplify(q * sp.diff(ell_lin, q) / ell_lin), sp.Integer(2))
identity(sp.simplify(q * sp.diff(ell_sqrt, q) / ell_sqrt), sp.Rational(1, 2))
units("l_P", "m")
raise SystemExit(finish())
