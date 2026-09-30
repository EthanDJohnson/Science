# M-DECOMPOSER-13: GPP exponent |ln(rho12(T)/rho12(0))| = (3/2) t_P^(4/3) T^(2/3) omega^2 (SI: dimensionless)
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, identity, finish
units("t_P^(4/3) * (1 s)^(2/3) * (2*pi*429 THz)^2", "dimensionless")
quantity("1.5 * t_P^(4/3) * (1 s)^(2/3) * (2*pi*429 THz)^2", "2.2e-27", rel_tol=0.03)
# scaling T^(2/3) omega^2: doubling omega x4, T x8 -> x4
identity("(3/2)*t**(4/3)*(8*T)**(2/3)*w**2", "4*(3/2)*t**(4/3)*T**(2/3)*w**2")
raise SystemExit(finish())
