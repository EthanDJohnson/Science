"""M-ENGINEER-13 (F17): gravitational-wave memory of a mass M accelerated to speed v.
Braginsky-Thorne (linear, ejecta ignored): Delta h_jk^TT = (4G/(c^4 d)) [M v_j v_k]^TT (Newtonian order).
For a line of sight n = z and v at angle theta, h_+ = (4G/(c^4 d)) (1/2) M v^2 sin^2 theta, so the maximum is
2 G M v^2/(c^4 d) = 4 G KE/(c^4 d). Lens: KE = 3.2e41 J (2.4 M_J at 0.04c), h = 3.5e-22 at 1 kpc, 3.5e-25 at 1 Mpc."""
import sys
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, units, quantity, limit, finish

v, th, Mm = sp.symbols("v theta M", positive=True)
vec = sp.Matrix([v * sp.sin(th), 0, v * sp.cos(th)])
n = sp.Matrix([0, 0, 1])
Pp = sp.eye(3) - n * n.T
A = Mm * vec * vec.T
TT = Pp * A * Pp - sp.Rational(1, 2) * Pp * (Pp * A).trace()
hplus = sp.simplify((TT[0, 0] - TT[1, 1]) / 2)
identity(hplus, Mm * v**2 * sp.sin(th)**2 / 2, domain={"theta": (0, 3.14), "v": (0.01, 0.9), "M": (0.1, 10)})
identity(TT.trace(), 0, domain={"theta": (0, 3.14), "v": (0.01, 0.9), "M": (0.1, 10)})
limit(hplus, "v", 0, "0")
M = 4.511e27
KE = (1 / math.sqrt(1 - 0.04**2) - 1) * M * c**2
rel("KE at 0.04c (J)", KE, 3.2e41, 0.03)
kpc = 3.0857e19
h1 = 4 * G * KE / (c**4 * kpc)
rel("h at 1 kpc", h1, 3.5e-22, 0.03)
rel("h at 1 Mpc", h1 / 1e3, 3.5e-25, 0.03)
units("G*1 J/(c^4*1 m)", "dimensionless")
quantity("4*G*3.24e41 J/(c^4*1 kpc)", "3.5e-22", rel_tol=0.02)
raise SystemExit(finish())
