"""M-CONSTRAINTS-04: J = 0 for curl-free shifts, and the speed scaling T(v) = v^2 A + v B (F5).

Geometric units. N = 1, flat slices; momentum constraint d_j(K_ij - delta_ij theta) = 8 pi J_i
(sign convention immaterial). (a) K_ij = d_i d_j Phi => J_i = 0 identically.
(b) For a rigidly translating drive X_i = v W_i(x, y, z - v t), the Eulerian-frame components at a
fixed comoving point obey rho/v^2, S_ij/v^2, J_i/v independent of v. Checked with the toolkit's 4D
Einstein tensor (gr_tensors) for a Gaussian-profile Natario-type shift and a curl-free shift.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, quantity, finish
from gr_tensors import Spacetime

x, y, z, t = sp.symbols("x y z t", real=True)
Xs = [x, y, z]
Phi = sp.Function("Phi")(x, y, z)
K = sp.hessian(Phi, Xs)
th = K.trace()
for i in range(3):
    identity(sp.expand(sum(sp.diff(K[i, j], Xs[j]) for j in range(3)) - sp.diff(th, Xs[i])), 0)

v = sp.symbols("v", positive=True)
zc = z - v * t
r = sp.sqrt(x**2 + y**2 + zc**2)
g = sp.exp(-(r - 1)**2 * 4)

def frame_components(shift_up, pts, vs):
    st = Spacetime.from_adm(1, shift_up, sp.eye(3), [t, x, y, z])
    T = st.stress_energy()
    n = st.eulerian_observer()
    out = {}
    for vv in vs:
        Tn = T.subs(v, vv)
        nn = n.subs(v, vv)
        rows = []
        for p in pts:
            sub = {t: 0, x: p[0], y: p[1], z: p[2]}
            Tm = np.array(Tn.subs(sub).evalf(), dtype=float)
            nv = np.array(nn.subs(sub).evalf(), dtype=float).ravel()
            rho = nv @ Tm @ nv
            J = -(nv @ Tm)[1:]
            S = Tm[1:, 1:]
            rows.append((rho, J, S))
        out[vv] = rows
    return out

pts = [(0.3, 0.5, 1.0), (0.9, -0.2, 0.4)]
vs = [sp.Rational(1, 2), 1, 2]
# Natario-type: X = v curl(g (-y, x, 0)/2)
A = [-y * g / 2, x * g / 2, 0]
curl = [sp.diff(A[2], y) - sp.diff(A[1], z), sp.diff(A[0], z) - sp.diff(A[2], x), sp.diff(A[1], x) - sp.diff(A[0], y)]
nat = frame_components([-v * c for c in curl], pts, vs)
# curl-free: X = v grad(z g)
P = zc * g
grad = [sp.diff(P, q) for q in Xs]
irr = frame_components([-v * c for c in grad], pts, vs)
for name, res in (("natario", nat), ("irrotational", irr)):
    for k in range(len(pts)):
        r1 = res[1][k]
        for vv in (sp.Rational(1, 2), 2):
            rv = res[vv][k]
            fv = float(vv)
            print(name, k, "v =", fv, "rho/v^2:", rv[0] / fv**2, r1[0], " |J|/v:", np.linalg.norm(rv[1]) / fv, np.linalg.norm(r1[1]))
            quantity(f"{rv[0] / fv**2}", f"{r1[0]}", rel_tol=1e-9)
            quantity(f"{np.max(np.abs(rv[2] / fv**2 - r1[2])) + 1}", "1", rel_tol=1e-9)
            if name == "natario":
                quantity(f"{np.linalg.norm(rv[1] / fv - r1[1]) + 1}", "1", rel_tol=1e-9)
        if name == "irrotational":
            print("irrotational |J| at v=1:", np.linalg.norm(r1[1]), " |rho|:", abs(r1[0]))
            quantity(f"{np.linalg.norm(r1[1]) + 1}", "1", rel_tol=1e-12)
        else:
            print("natario |J| at v=1 (nonzero expected):", np.linalg.norm(r1[1]))
raise SystemExit(finish())
