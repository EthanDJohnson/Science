"""M-MECHANIST-06: payload kick when a uniform interior shift is ramped (shell frame).

Interior metric ds^2 = -N^2 c^2 dt^2 + (dx + beta(t) c dt)^2 + dy^2 + dz^2, N constant, flat.
x-translation symmetry -> u_x = dx/dtau + beta c dt/dtau conserved. Payload at rest with beta = 0
-> u_x = 0 -> dx/dt = -beta c. Speed relative to static (shell-fixed) observers: gamma_rel = -u_s.u_p.
Claim: 0.0263 c (beta = 0.02, N = 0.761), crossing R1 = 10 m in 1.27 us, recoil 1.7e-16 m/s.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

Nn, b = sp.symbols("N_l b", positive=True)
g = sp.Matrix([[-Nn**2 + b**2, b], [b, 1]])   # (ct, x) block
up = sp.Matrix([1 / Nn, -b / Nn])              # Eulerian payload (u_x = 0)
us = sp.Matrix([1 / sp.sqrt(Nn**2 - b**2), 0])  # static observer
identity(sp.simplify((up.T * g * up)[0]), "-1")
identity(sp.simplify((g * up)[1]), "0")          # covariant u_x = 0 (conserved value)
gam = sp.simplify(-(us.T * g * up)[0])
vrel = sp.simplify(sp.sqrt(1 - 1 / gam**2))
print("relative speed =", vrel)
identity(vrel, b / Nn, domain={"N_l": (0.5, 1), "b": (0.001, 0.4)})
limit(b / Nn, "b", 0, "0")
c = 2.99792458e8
v = 0.02 / 0.761
print(f"v_rel = {v:.5f} c; crossing 10 m: {10/(v*c):.4e} s; recoil (M=4.511e27): {1e5*v*c/4.5114e27:.3e} m/s")
quantity(f"{v} m/m", "0.0263 m/m", rel_tol=0.002)
quantity(f"10 m / ({v} * 2.99792458e8 m/s)", "1.27 us", rel_tol=0.005)
quantity(f"1e5 kg * {v} * 2.99792458e8 m/s / (4.5114e27 kg)", "1.7e-16 m/s", rel_tol=0.04)
units("1e5 kg * 3e8 m/s / (4.5e27 kg)", "m/s")
raise SystemExit(finish())
