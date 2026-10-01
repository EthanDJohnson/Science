"""M-IDEALIZER-04: linearized momentum constraint (F4). Geometric units.
Metric: unit lapse, flat slices, static shift b^i = eps*w_i(x,y,z) (h = delta, so covariant = contravariant),
ds^2 = -dt^2 + (dx^i + eps w_i dt)^2. Claims:
 (a) G_0i = (eps/2)[curl curl w]_i + O(eps^2), hence T_0i = (1/16pi) curl curl w;
 (b) a gradient w = grad chi gives G_0i = 0 at O(eps);
 (c) the Eulerian density is O(eps^2); for w = S(r) z-hat it is <= 0.
Exact Einstein tensor from gr_tensors (own metric input), expanded in eps.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime
from math_checks import identity, sign, limit, quantity, finish

t, x, y, z, eps = sp.symbols("t x y z epsilon", real=True)
wx, wy, wz = [sp.Function(n)(x, y, z) for n in ("w_x", "w_y", "w_z")]
w = sp.Matrix([wx, wy, wz])
st = Spacetime.from_adm(1, eps*w, sp.eye(3), [t, x, y, z])
G = st.einstein()
X = [x, y, z]
def curl(v):
    return sp.Matrix([sp.diff(v[2], y) - sp.diff(v[1], z), sp.diff(v[0], z) - sp.diff(v[2], x), sp.diff(v[1], x) - sp.diff(v[0], y)])
cc = curl(curl(w))
for i in range(3):
    lin = sp.diff(G[0, i + 1], eps).subs(eps, 0)
    identity(sp.simplify(lin - cc[i]/2), 0)
    identity(sp.simplify(G[0, i + 1].subs(eps, 0)), 0)   # no O(1) part

# Eulerian density rho = G_ab n^a n^b / 8pi, n^a = (1, -eps w)
n = sp.Matrix([1, -eps*wx, -eps*wy, -eps*wz])
rhoE = (n.T*G*n)[0, 0]/(8*sp.pi)
identity(sp.simplify(rhoE.subs(eps, 0)), 0)
identity(sp.simplify(sp.diff(rhoE, eps).subs(eps, 0)), 0)
# O(eps^2) part: concrete, asymmetric test shift (generic functions are too slow to simplify)
wc = sp.Matrix([x*y + z**2, x*z - y**2/2, x**3 + y*z])
stc = Spacetime.from_adm(1, eps*wc, sp.eye(3), [t, x, y, z])
Gc = stc.einstein()
nc = sp.Matrix([1, -eps*wc[0], -eps*wc[1], -eps*wc[2]])
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(wc[j], X[i]) + sp.diff(wc[i], X[j]))/2)
trK = Kij.trace()
KK = sum(Kij[i, j]**2 for i in range(3) for j in range(3))
for pt in [{x: 0.3, y: -1.1, z: 0.7}, {x: 1.3, y: 0.4, z: -0.9}, {x: -0.6, y: 0.8, z: 1.5}]:
    Gp = Gc.subs(pt); npnt = nc.subs(pt)          # functions of eps only
    rho_eps = sp.simplify((npnt.T*Gp*npnt)[0, 0]/(8*sp.pi))
    c0, c1, c2 = [sp.diff(rho_eps, eps, k).subs(eps, 0)/sp.factorial(k) for k in range(3)]
    ref = ((trK**2 - KK)/(16*sp.pi)).subs(pt)
    print(f"point {pt}: rho_E series coeffs {float(c0):.3e}, {float(c1):.3e}, {float(c2):.6f}; (K^2-KK)/16pi = {float(ref):.6f}")
    identity(sp.nsimplify(float(c0)), 0); identity(sp.nsimplify(float(c1)), 0)
    quantity(f"{float(c2)}", f"{float(ref)}", rel_tol=1e-9)

# (b) gradient shift
chi = sp.Function("chi")(x, y, z)
gw = sp.Matrix([sp.diff(chi, v) for v in X])
for i in range(3):
    identity(sp.simplify(curl(curl(gw))[i]), 0)

# (c) w = S(r) z-hat: (K^2 - K_ij K^ij) = -(1/2) S'^2 sin^2(theta) <= 0
r = sp.sqrt(x**2 + y**2 + z**2)
Sf = sp.Function("S")
wS = sp.Matrix([0, 0, Sf(r)])
K2 = sp.Matrix(3, 3, lambda i, j: (sp.diff(wS[j], X[i]) + sp.diff(wS[i], X[j]))/2)
val = sp.simplify(K2.trace()**2 - sum(K2[i, j]**2 for i in range(3) for j in range(3)))
target = -sp.Rational(1, 2)*sp.diff(Sf(r), x)**2 - sp.Rational(1, 2)*sp.diff(Sf(r), y)**2
identity(sp.simplify(val - target), 0)
print("for w = S(r) z: K^2 - K_ij K^ij =", val, " = -(1/2)(d_x S^2 + d_y S^2) <= 0")
# but the sign is not universal: w = (x, y, z) gives +6
wr = sp.Matrix([x, y, z])
K3 = sp.Matrix(3, 3, lambda i, j: (sp.diff(wr[j], X[i]) + sp.diff(wr[i], X[j]))/2)
print("for w = (x,y,z): K^2 - K_ij K^ij =", K3.trace()**2 - sum(K3[i, j]**2 for i in range(3) for j in range(3)))
# limit: uniform w (cavity) -> curl curl w = 0
for i in range(3):
    identity(curl(curl(sp.Matrix([sp.Integer(2), sp.Integer(-1), sp.Integer(3)])))[i], 0)
raise SystemExit(finish())
