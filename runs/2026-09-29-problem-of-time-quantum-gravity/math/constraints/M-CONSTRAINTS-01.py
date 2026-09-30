"""M-CONSTRAINTS-01: FRW dH/dt identities and York-time monotonicity conditions (G = c = 1).

Claim (F1): from the Friedmann equations,
  dH/dt = -4 pi (rho + p) + k/a^2 = -(4 pi/3)(rho + 3p) - H^2,
so York time K = -3H is strictly monotonic whenever the SEC holds (any k) or the NEC holds and k <= 0.
Independent route: build the FRW metric for k = +1, 0, -1 with gr_tensors, read rho = G_tt/(8 pi)
and p = G^chi_chi/(8 pi), and test the two forms of dH/dt as identities in a, a', a''.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime
from math_checks import identity, sign, limit, finish

t, chi, th, ph = sp.symbols("t chi theta phi", real=True)
a = sp.Function("a")(t)
ok_all = True
for k, S in [(1, sp.sin(chi)), (0, chi), (-1, sp.sinh(chi))]:
    g = sp.diag(-1, a**2, a**2 * S**2, a**2 * S**2 * sp.sin(th) ** 2)
    st = Spacetime(g, [t, chi, th, ph], simplify=True)
    G = st.einstein()
    ginv = st.ginv
    rho = sp.simplify(G[0, 0] / (8 * sp.pi))            # u = d/dt, rho = G_tt/8pi
    p = sp.simplify((ginv * G)[1, 1] / (8 * sp.pi))       # G^chi_chi / 8pi
    # replace derivatives by plain symbols for the identity checks
    A, Ad, Add = sp.symbols("A Ad Add", positive=True)
    rep = {sp.Derivative(a, (t, 2)): Add, sp.Derivative(a, t): Ad, a: A}
    rho_s = rho.subs(rep)
    p_s = p.subs(rep)
    H = Ad / A
    Hdot = Add / A - Ad**2 / A**2
    dom = {"A": (0.1, 10), "Ad": (-5, 5), "Add": (-5, 5)}
    print(f"k = {k}: rho = {sp.simplify(rho_s)}, p = {sp.simplify(p_s)}")
    identity(rho_s, 3 * (Ad**2 + k) / (8 * sp.pi * A**2), domain=dom)       # Hamiltonian constraint
    identity(Hdot, -4 * sp.pi * (rho_s + p_s) + sp.Rational(k) / A**2, domain=dom)
    identity(Hdot, -sp.Rational(4, 3) * sp.pi * (rho_s + 3 * p_s) - H**2, domain=dom)

# Monotonicity: with SEC (rho+3p >= 0), dH/dt <= -H^2 <= 0 (strict unless H = 0 and rho+3p = 0).
x, h = sp.symbols("x h", real=True)   # x = rho + 3p >= 0
sign(-sp.Rational(4, 3) * sp.pi * x - h**2, "nonpositive", domain={"x": (0, 5), "h": (-5, 5)})
# With NEC (y = rho+p >= 0) and k <= 0: dH/dt <= 0
y, kk, A2 = sp.symbols("y kk A2", real=True)
sign(-4 * sp.pi * y + kk / A2**2, "nonpositive", domain={"y": (0, 5), "kk": (-1, 0), "A2": (0.1, 10)})
# Saturated counterexamples to *strict* monotonicity:
#  (a) flat de Sitter: rho = -p = Lambda/(8 pi), k = 0 -> dH/dt = 0, K constant.
L = sp.symbols("L", positive=True)
rho_dS, p_dS = L / (8 * sp.pi), -L / (8 * sp.pi)
identity(-4 * sp.pi * (rho_dS + p_dS) + 0, "0")
#  (b) Einstein static universe (k = +1, dust + Lambda, H = 0): a'' = 0 requires rho + 3p = 0 (SEC saturated),
#      so dH/dt = -(4pi/3)(rho+3p) - 0 = 0: York time constant, although SEC holds.
rm = sp.symbols("rm", positive=True)
aE = sp.symbols("aE", positive=True)
# ESU: rho_m = 1/(4 pi aE^2), Lambda = 1/aE^2  (standard); total rho = rho_m + Lambda/8pi, p = -Lambda/8pi
rho_tot = 1 / (4 * sp.pi * aE**2) + 1 / (8 * sp.pi * aE**2)
p_tot = -1 / (8 * sp.pi * aE**2)
identity(rho_tot, 3 * (0 + 1) / (8 * sp.pi * aE**2))          # Friedmann with H = 0, k = 1
identity(rho_tot + 3 * p_tot, "0")                              # SEC saturated
# Limit: k -> 0, rho+p -> 0 recovers dH/dt -> 0 (de Sitter)
limit(-4 * sp.pi * x, "x", 0, "0")
raise SystemExit(finish())
