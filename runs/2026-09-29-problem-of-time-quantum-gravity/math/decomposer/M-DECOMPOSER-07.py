# M-DECOMPOSER-07: gravitational coupling between two clocks of energy E = hbar*omega at separation x:
# V = -G (H_A/c^2)(H_B/c^2)/x  => lambda = G/(c^4 x) [1/J], and lambda * hbar*omega is dimensionless.
# (Interpretation reconstructed from the Newtonian mass-energy coupling; the lens gives no formula.)
import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish
units("G/(c^4 * 1 mm) * hbar * 2*pi*429 THz", "dimensionless")
quantity("G/(c^4 * 1 mm) * hbar * 2*pi*429 THz", "2.35e-60", rel_tol=5e-3)
quantity("G/(c^4 * 1 m) * hbar * 2*pi*429 THz", "2.35e-63", rel_tol=5e-3)
# cross-check against Planck units: lambda*hbar*omega = (omega t_P) * (l_P / x)
quantity("2*pi*429 THz * t_P * l_P / (1 mm)", "2.35e-60", rel_tol=5e-3)
raise SystemExit(finish())
