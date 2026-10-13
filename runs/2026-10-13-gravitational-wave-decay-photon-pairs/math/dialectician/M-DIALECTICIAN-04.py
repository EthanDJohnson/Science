"""M-DIALECTICIAN-04: Gaussian linear chirp suppresses J_f (F4).

f(a) = (pi s^2)^(-1/4) exp(-x^2/(2 s^2)) exp(i beta x^2), x = a - w, s the amplitude width
(same convention under which T_eff = sqrt(pi/2)/s, M-02). C(y) = int f(x) f(y - x) dx,
J = int |C|^2 dy. Claim: J(beta)/J(0) = 1/sqrt(1 + 4 beta^2 s^4) = t_TL/t_rms, where t_rms is
the rms width of |a(t)|^2 and the group delay is d psi/da = 2 beta x.
Route: complete the square (own algebra), then a direct numerical double integral.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from math_checks import identity, limit, series, quantity, finish

s, b = sp.symbols("s b", positive=True)
xr, yr = sp.symbols("x_r y_r", real=True)
alpha = 1 / (2 * s**2) - sp.I * b
# x^2 + (y-x)^2 = 2 (x - y/2)^2 + y^2/2  => C = sqrt(pi/(2 alpha)) exp(-alpha y^2/2) (pi s^2)^(-1/2)
identity(sp.expand(xr**2 + (yr - xr) ** 2), sp.expand(2 * (xr - yr / 2) ** 2 + yr**2 / 2))
absC2 = sp.pi / (2 * sp.Abs(alpha)) * sp.exp(-sp.re(alpha) * yr**2) / (sp.pi * s**2)
J = sp.integrate(absC2, (yr, -sp.oo, sp.oo))
J = sp.simplify(J)
J0 = sp.simplify(J.subs(b, 0))
ratio = sp.simplify(J / J0)
print("J(beta) =", J, " J(0) =", J0, " ratio =", ratio)
identity(ratio, 1 / sp.sqrt(1 + 4 * b**2 * s**4))
# time widths: var_w under |f|^2 = s^2/2; t_TL^2 = 1/(4 var_w); chirp adds (2 beta)^2 var_w
var_w = s**2 / 2
tTL2 = 1 / (4 * var_w)
trms2 = tTL2 + 4 * b**2 * var_w
identity(sp.sqrt(tTL2 / trms2), 1 / sp.sqrt(1 + 4 * b**2 * s**4))
limit(ratio, "b", 0, 1)
limit(ratio * b, "b", sp.oo, 1 / (2 * s**2))  # 1/duration at large chirp

# numeric: direct C(y) by quadrature for s = 1
xs = np.linspace(-12, 12, 4001)
dx = xs[1] - xs[0]
def Jnum(beta):
    f = np.pi ** -0.25 * np.exp(-xs**2 / 2) * np.exp(1j * beta * xs**2)
    C = np.convolve(f, f) * dx  # C on grid y in [-24, 24]
    return np.sum(np.abs(C) ** 2) * dx
J0n = Jnum(0.0)
print(f"J(0) numeric {J0n:.8f} vs closed {float(J0.subs(s,1)):.8f}")
for bs2 in (1, 5, 25):
    r = Jnum(bs2) / J0n
    print(f"beta s^2 = {bs2}: numeric {r:.8f}, closed {1/np.sqrt(1+4*bs2**2):.8f}")
    quantity(f"{r}", f"{1/np.sqrt(1+4*bs2**2)}", rel_tol=1e-5)
raise SystemExit(finish())
