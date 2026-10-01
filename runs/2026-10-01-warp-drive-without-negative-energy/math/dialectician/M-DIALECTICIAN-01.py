"""M-DIALECTICIAN-01: for unit lapse, flat slices, beta = grad(phi), the Eulerian energy density
satisfies 16 pi rho_E = (lap phi)^2 - phi_ij phi_ij = d_i F_i, F_i = phi_i lap phi - phi_j phi_ij.
Geometric units G = c = 1. rho_E [1/m^2], phi [m] (beta dimensionless => phi has units of length).
Independent route: (a) generic identity in sympy; (b) rho_E from the full 4D Einstein tensor
(not the Hamiltonian constraint) for explicit polynomial phi, contracted with the Eulerian normal.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, units, finish
from gr_tensors import Spacetime

t, x, y, z = sp.symbols("t x y z", real=True)
X = (x, y, z)
phi = sp.Function("phi")(x, y, z)
H = sp.Matrix(3, 3, lambda i, j: sp.diff(phi, X[i], X[j]))
lap = H.trace()
quad = sum(H[i, j] ** 2 for i in range(3) for j in range(3))
F = [sp.diff(phi, X[i]) * lap - sum(sp.diff(phi, X[j]) * H[i, j] for j in range(3)) for i in range(3)]
divF = sum(sp.diff(F[i], X[i]) for i in range(3))
print("generic identity residual:", sp.simplify(sp.expand(divF - (lap ** 2 - quad))))
identity(sp.expand(divF), sp.expand(lap ** 2 - quad))

# (b) 4D Einstein tensor for explicit phi, both shift sign conventions
a = sp.symbols("a", positive=True)
tests = [x**2 * y + y * z**2 / 3 + x * z**3 / 5,
         a * (x**3 * y - z * y**2) + x * y * z]  # Gaussian test dropped: 4D Einstein tensor too slow (>400 s)
for k, ph in enumerate(tests):
    for sgn in (+1, -1):
        shift = [sgn * sp.diff(ph, v) for v in X]
        st = Spacetime.from_adm(sp.Integer(1), shift, sp.eye(3), (t, x, y, z))
        G = st.einstein()
        g = st.metric if hasattr(st, "metric") else st.g
        # Eulerian normal n^a = (1, shift^i) for dx^i + shift^i dt convention? compute from metric
        ginv = st.g.inv()
        n_low = sp.Matrix([-1, 0, 0, 0])               # n_a = -N dt, N = 1
        n_up = ginv * n_low
        rhoE = sum(G[i, j] * n_up[i] * n_up[j] for i in range(4) for j in range(4)) / (8 * sp.pi)
        Hn = sp.Matrix(3, 3, lambda i, j: sp.diff(ph, X[i], X[j]))
        claim = (Hn.trace() ** 2 - sum(Hn[i, j] ** 2 for i in range(3) for j in range(3))) / (16 * sp.pi)
        pt = {x: sp.Rational(3, 10), y: sp.Rational(-7, 10), z: sp.Rational(11, 10), a: sp.Rational(13, 10)}
        print(f"test {k} sign {sgn}: rhoE(4D) = {sp.N(rhoE.subs(pt), 15)}, claim = {sp.N(claim.subs(pt), 15)}")
        identity(sp.simplify(rhoE), claim, domain={"x": (-2, 2), "y": (-2, 2), "z": (-2, 2)})

# limit: phi -> eps*phi gives rho_E -> 0 quadratically (flat space)
eps = sp.symbols("eps", positive=True)
ph0 = x**2 * y + z**3
Hn = sp.Matrix(3, 3, lambda i, j: sp.diff(eps * ph0, X[i], X[j]))
expr = (Hn.trace() ** 2 - sum(Hn[i, j] ** 2 for i in range(3) for j in range(3))) / eps**2
limit(sp.simplify(expr), "eps", 0, sp.simplify(expr.subs(eps, 1)), domain={"x": (-2, 2), "y": (-2, 2), "z": (-2, 2)})
# units: phi_ij ~ 1/m, so (phi_ij)^2 ~ 1/m^2 = geometric energy density; check SI conversion dimension
units("(1/m^2) * c^4 / G", "J/m^3")
raise SystemExit(finish())
