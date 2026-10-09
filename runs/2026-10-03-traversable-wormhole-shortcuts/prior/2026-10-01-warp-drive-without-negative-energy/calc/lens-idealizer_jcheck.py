"""Idealizer lens: check of the linearized momentum-constraint formula with gr_tensors.

Geometric units (G = c = 1, metres). Metric: unit lapse, flat slice, small covariant shift
g_0z = w(x) = eps * exp(-(x^2+y^2+z^2)) (from_adm convention: g_0i = h_ij b^j = b_i).
Claim to test (linear in eps): G_0i = (1/2) [curl curl w]_i, so T_0i = (1/16 pi) [curl curl w]_i,
and the Eulerian energy density is O(eps^2).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from gr_tensors import Spacetime

t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
w = eps*sp.exp(-(x**2 + y**2 + z**2))
st = Spacetime.from_adm(1, [0, 0, w], sp.eye(3), [t, x, y, z])
Gt = st.einstein()

W = sp.Matrix([0, 0, w])
def curl(V):
    return sp.Matrix([sp.diff(V[2], y) - sp.diff(V[1], z),
                      sp.diff(V[0], z) - sp.diff(V[2], x),
                      sp.diff(V[1], x) - sp.diff(V[0], y)])
cc = curl(curl(W))

pts = [(0.3, -0.2, 0.5), (0.7, 0.1, -0.4), (0.0, 0.9, 0.2)]
for p in pts:
    sub = {x: p[0], y: p[1], z: p[2], t: 0}
    for i, name in enumerate("xyz"):
        G0i = Gt[0, i+1]
        lin = sp.diff(G0i, eps).subs(eps, 0).subs(sub)
        pred = (sp.Rational(1, 2)*cc[i]/eps).subs(sub)
        print(f"point {p} component {name}: dG_0{name}/deps|0 = {float(lin): .6e}   (1/2)curlcurl/eps = {float(pred): .6e}")
rho = st.energy_density()
print("Eulerian rho at eps-linear order (should be 0):",
      float(sp.diff(rho, eps).subs(eps, 0).subs({x: 0.3, y: -0.2, z: 0.5, t: 0})))
print("Eulerian rho second order coefficient at (0.3,-0.2,0.5):",
      float((sp.diff(rho, eps, 2)/2).subs(eps, 0).subs({x: 0.3, y: -0.2, z: 0.5, t: 0})))
