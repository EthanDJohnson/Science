# M-DECOMPOSER-01: fractional gravitational redshift between clocks separated by dh near Earth's surface
# Weak-field, static: d(tau)/tau = g dh / c^2 (first order in Phi/c^2). SI units.
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, limit, identity, finish
units("g0 * 1 mm / c^2", "dimensionless")
quantity("g0 * 1 mm / c^2", "1.09e-19", rel_tol=5e-3)
# Independent route: Schwarzschild exact ratio sqrt(1-2GM/(c^2 r)) between r=R and R+dh, first order in dh
limit("(sqrt(1-2*G*M/(c**2*(R+h)))/sqrt(1-2*G*M/(c**2*R)) - 1)/h", "h", 0,
      "G*M/(c**2*R**2)/(1-2*G*M/(c**2*R))", domain={"G": (0.1, 1), "M": (0.1, 1), "c": (2, 10), "R": (1, 10)})
# Newtonian-limit weak field: g = GM/R^2 recovered when 2GM/(c^2 R) -> 0; numeric Earth value
quantity("G * 5.9722e24 kg / (6.371e6 m)^2 * 1 mm / c^2", "1.09e-19", rel_tol=1e-2)
raise SystemExit(finish())
