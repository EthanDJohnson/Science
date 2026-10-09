"""M-CONSTRAINTS-15 (F17). Cube wormhole (Visser 1989): a cube excised from each of two flat spaces, faces identified.
Total angle around an edge: each exterior dihedral angle is 2 pi - pi/2 = 3 pi/2; two copies give 3 pi; conical
deficit delta = 2 pi - 3 pi = -pi. Straight static string (literature relation): delta = 8 pi G mu / c^2.
Claims: mu = -c^2/(8 G) = -1.68e26 kg/m; 12 edges of 1 m: -2.0e27 kg; spherical shell a = 0.5 m: -2a c^2/G = -1.35e27 kg."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

ext = 2 * sp.pi - sp.pi / 2
total = 2 * ext
delta = 2 * sp.pi - total
identity(total, 3 * sp.pi)
identity(delta, -sp.pi)
c, G, mu, dl = sp.symbols("c G mu delta", real=True)
mu_sol = sp.solve(sp.Eq(dl, 8 * sp.pi * G * mu / c**2), mu)[0]
identity(sp.simplify(mu_sol.subs(dl, delta)), -c**2 / (8 * G), domain={"c": (0.1, 10), "G": (0.1, 10)})
limit(mu_sol, "delta", 0, "0")       # flat-space limit: no excess, no line mass
quantity("-1 * c^2/(8*G)", "-1.68e26 kg/m", rel_tol=3e-3)
quantity("-12 * 1 m * c^2/(8*G)", "-2.0e27 kg", rel_tol=0.02)
quantity("-2 * 0.5 m * c^2/G", "-1.35e27 kg", rel_tol=3e-3)
raise SystemExit(finish())
