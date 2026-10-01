"""M-ENGINEER-01 (F5): compactness 2GM/(c^2 R2) = 0.335 for M_ADM = 4.51e27 kg, R2 = 20 m;
4.51e27 kg = 2.38 M_J; peak energy density 1.38e40 J/m^3 <-> 1.53e23 kg/m^3; this equals the mean
density of 4.49e27 kg spread uniformly over R1 = 10 m .. R2 = 20 m (D-22). SI units."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import quantity, units, limit, finish

M_adm, M_pub, R1, R2 = 4.511e27, 4.49e27, 10.0, 20.0
C = 2 * G * M_adm / (c**2 * R2)
rel("compactness 2GM/(c^2 R2)", C, 0.335, 3e-3)
quantity("2*G*4.511e27 kg/(c^2*20 m)", "0.335", rel_tol=3e-3)
units("2*G*1 kg/(c^2*1 m)", "dimensionless")
rel("M_ADM in Jupiter masses", M_adm / Mjup, 2.38, 3e-3)
rel("published M in Jupiter masses", M_pub / Mjup, 2.365, 3e-3)
rho_mean = M_pub / (4 / 3 * math.pi * (R2**3 - R1**3))
rel("mean density of the published shell (kg/m^3)", rho_mean, 1.53e23, 5e-3)
rel("eps = 1.38e40 J/m^3 divided by c^2 (kg/m^3)", 1.38e40 / c**2, 1.53e23, 5e-3)
rel("rho_mean c^2 vs lens peak eps (J/m^3)", rho_mean * c**2, 1.38e40, 5e-3)
quantity("1.38e40 J/m^3 / c^2", "1.535e23 kg/m^3", rel_tol=3e-3)
# limit: compactness of a thin shell goes to 0 as R2 -> infinity at fixed M
limit("2*g*m/(k**2*r)", "r", "oo", "0")
raise SystemExit(finish())
