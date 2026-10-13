"""M-CONSTRAINTS-08: far-zone yield of a single outgoing wave beyond radius R falls as (w R)^-3.
Independent toy (my own construction, not the lens's grid): monochromatic outgoing monopole
field phi = e^{i w (r - t)}/r (units c = 1, w = 1). Pair source J = phi^2 = e^{-2it} e^{2ir}/r^2,
windowed to the region beyond R by a smooth W(r/R) = x^4/(1+x^4) (W -> 1 for r >> R).
Spatial FT (spherical): J~(q) = (4 pi/q) int_0^inf sin(q r) e^{2ir} W/r dr = (4 pi/q) A(q).
Pairs need time-like total momentum: q0 = 2, |q| < 2, s = 4 - q^2. Rate weight s^p with
p = 2 (sigma ~ s times flux factor (1 - cos) ~ s, as in the lens's two-beam toy).
Y(R) = int_0^2 q^2 dq |J~|^2 s^2  ~  int_0^2 dq |A(q)|^2 (4 - q^2)^2.
Analytic expectation: A is dominated by Phi((2 - q) R) with Phi(u) = int_0^inf e^{iux} W(x)/x dx,
so with kappa = 2 - q, Y ~ 16 int dkappa kappa^2 |Phi(kappa R)|^2 = 16 R^-3 int du u^2 |Phi(u)|^2.
Check: local slope d ln Y / d ln R -> -3; also s ~ 4 w/R scale (kappa ~ 1/R).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.integrate import quad
from math_checks import limit, identity, quantity, finish
import sympy as sp

def g(x): return x**3 / (1 + x**4)

def Phi(u):
    re = quad(g, 0, np.inf, weight="cos", wvar=u, limlst=200)[0]
    im = quad(g, 0, np.inf, weight="sin", wvar=u, limlst=200)[0]
    return complex(re, im)

def Y(R):
    def integrand(k):            # k = 2 - q
        q = 2 - k
        A = (Phi((2 + q) * R) - Phi(k * R)) / 2j
        return abs(A)**2 * (k * (4 - k))**2
    br = [0, 0.5 / R, 2 / R, 8 / R, 32 / R, 2.0]
    br = sorted(set(min(b, 2.0) for b in br))
    return sum(quad(integrand, a, b, limit=200)[0] for a, b in zip(br[:-1], br[1:]))

Rs = [10, 20, 40, 80, 160, 320]
Ys = [Y(R) for R in Rs]
slopes = []
for i in range(1, len(Rs)):
    sl = math.log(Ys[i] / Ys[i - 1]) / math.log(Rs[i] / Rs[i - 1])
    slopes.append(sl)
    print(f"wR {Rs[i-1]}->{Rs[i]}: Y={Ys[i]:.4e}, local slope {sl:.4f}, Y R^3 = {Ys[i]*Rs[i]**3:.5f}")
# asymptotic constant from the scaling form
I_u = quad(lambda u: u**2 * abs(Phi(u))**2, 1e-6, 60, limit=400)[0]
print("4 int u^2 |Phi|^2 du =", 4 * I_u, "(predicted limit of Y R^3: 16 x (1/2i)^2 = 4)")
quantity(f"{slopes[-1]}", "-3", rel_tol=0.02)
quantity(f"{Ys[-1]*Rs[-1]**3}", f"{4*I_u}", rel_tol=0.01)
# with p = 1 weight the exponent would be -2: shows the -3 is tied to sigma ~ s and flux ~ s
def Yp1(R):
    f = lambda k: abs((Phi((4 - k) * R) - Phi(k * R)) / 2j)**2 * (k * (4 - k))
    return sum(quad(f, a, b, limit=200)[0] for a, b in [(0, 0.5 / R), (0.5 / R, 8 / R), (8 / R, 2.0)])
sl1 = math.log(Yp1(320) / Yp1(160)) / math.log(2)
print("slope with s^1 weight:", sl1)
# exact scaling identity of the leading term: int_0^inf dk k^2 |Phi(kR)|^2 = R^-3 int du u^2 |Phi(u)|^2
Rs_, u, k = sp.symbols("R u k", positive=True)
fsym = sp.Function("f")
lhs = sp.integrate(k**2 * sp.exp(-k * Rs_), (k, 0, sp.oo))   # representative integrand f(kR) = e^{-kR}
identity(lhs, Rs_**-3 * sp.integrate(u**2 * sp.exp(-u), (u, 0, sp.oo)))
# numbers quoted by the lens: (lambda/(2 pi R))^3 at R = lambda, 1 AU, 410 Mpc; footnote 4 at c tau = 1.1e12 m
c = 299792458.0
lam = c / 150.0
red = lam / (2 * math.pi)
for R, want in [(lam, 4.0e-3), (1.495978707e11, 9.5e-18), (410 * 3.0856775814913673e22, 1.6e-59), (1.1e12, 2.5e-20)]:
    v = (red / R)**3
    print(f"R={R:.3e} m: (lambda/2piR)^3 = {v:.3e}")
    quantity(f"{v}", f"{want}", rel_tol=0.06)
raise SystemExit(finish())
