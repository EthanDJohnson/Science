"""M-DECOMPOSER-01: WEC (T(u,u) >= 0 for all timelike u) implies NEC (T(k,k) >= 0 for all null k).
Orthonormal frame, signature (-,+,+,+), T a real symmetric 2-tensor with 10 generic components.
Argument: u_eps = (1, (1-eps) n) is timelike for 0 < eps < 1 (n a unit 3-vector); T(u_eps,u_eps)
is a polynomial in eps, continuous at eps = 0, where u_0 = k = (1, n) is null. So T(k,k) is a limit
of non-negative numbers, hence non-negative. Converse fails (rho = -1, p = 1 counterexample)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import limit, sign, identity, inequality, finish

eps = sp.symbols("eps", positive=True)
th, ph = sp.symbols("th ph", real=True)
T = sp.Matrix(4, 4, lambda i, j: sp.Symbol(f"T{min(i,j)}{max(i,j)}", real=True))
n = sp.Matrix([sp.sin(th)*sp.cos(ph), sp.sin(th)*sp.sin(ph), sp.cos(th)])
eta = sp.diag(-1, 1, 1, 1)
u = sp.Matrix([1, *((1-eps)*n)])
k = sp.Matrix([1, *n])
norm_u = sp.simplify((u.T*eta*u)[0])
print("g(u_eps,u_eps) =", sp.factor(norm_u))
# timelike for 0<eps<1:
sign(-norm_u.subs({th: 0.7, ph: 0.3}) , "positive", domain={"eps": (1e-6, 0.999)})
Tuu = (u.T*T*u)[0]
Tkk = (k.T*T*k)[0]
identity(sp.expand(Tuu.subs(eps, 0)), sp.expand(Tkk))
# continuity: limit eps->0 at a numeric generic T
vals = {s: sp.Rational(i+1, 7)*(-1)**i for i, s in enumerate(sorted(T.free_symbols, key=str))}
limit(Tuu.subs(vals).subs({th: sp.Rational(7, 10), ph: sp.Rational(3, 10)}), "eps", 0,
      Tkk.subs(vals).subs({th: sp.Rational(7, 10), ph: sp.Rational(3, 10)}), direction="+")
# type-I form: rho + p_i >= 0 is the NEC; WEC adds rho >= 0. Converse counterexample rho=-1, p=1:
rho, p = -1, 1
print("counterexample NEC holds (rho+p =", rho + p, ") WEC fails (rho =", rho, ")")
inequality("rho + p", ">=", "0", domain={"rho": (-1, -1), "p": (1, 1)})
raise SystemExit(finish())
