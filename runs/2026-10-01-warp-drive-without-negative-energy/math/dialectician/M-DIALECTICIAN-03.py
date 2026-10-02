"""M-DIALECTICIAN-03: characteristic cones of L = d_x^2 + d_y^2 - (2/v^2) d_z^2 (Lentz's operator as quoted, D-06).
Claim: a compact source radiates along r_perp = (v/sqrt 2)|z|. v = v_h > 0 dimensionless (units of c), lengths in m.
Checks: (a) principal symbol k_perp^2 - (2/v^2) k_z^2 = 0 gives |k_z|/|k_perp| = v/sqrt2, and the ray (group)
direction normal to that cone has r_perp/|z| = v/sqrt2; (b) plane waves f(x - (v/sqrt2) z) solve L u = 0;
(c) the 2+1 fundamental-solution form u = (c^2 z^2 - r^2)^(-1/2), c = v/sqrt2, solves L u = 0 inside the cone,
singular exactly on r_perp = c|z|; (d) limit: v -> infinity gives elliptic-in-plane (cone opens fully).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, finish

x, y, z = sp.symbols("x y z", real=True)
v, kp, kz = sp.symbols("v k_p k_z", positive=True)
L = lambda u: sp.diff(u, x, 2) + sp.diff(u, y, 2) - 2 / v**2 * sp.diff(u, z, 2)
f = sp.Function("f")
# (a) symbol zero set; ray direction = gradient of symbol wrt k: (2k_p, -4k_z/v^2) -> r/z ratio
kz_root = sp.solve(sp.Eq(kp**2 - 2 / v**2 * kz**2, 0), kz)[0]
identity(kz_root / kp, v / sp.sqrt(2))
ray_ratio = (2 * kp) / (4 * kz_root / v**2)          # |dr_perp/dz| along bicharacteristic
identity(sp.simplify(ray_ratio), v / sp.sqrt(2))
# (b) plane wave
identity(sp.simplify(L(f(x - v / sp.sqrt(2) * z))), 0)
# (c) 2+1 homogeneous solution singular on the cone
c = v / sp.sqrt(2)
u = (c**2 * z**2 - x**2 - y**2) ** sp.Rational(-1, 2)
identity(sp.simplify(L(u)), 0, domain={"x": (0.1, 0.5), "y": (0.1, 0.5), "z": (3, 10), "v": (1, 10)})
# (d) cone half-opening tan(theta) = v/sqrt2 -> pi/2 as v -> infinity
limit(sp.atan(v / sp.sqrt(2)), "v", sp.oo, sp.pi / 2)
raise SystemExit(finish())
