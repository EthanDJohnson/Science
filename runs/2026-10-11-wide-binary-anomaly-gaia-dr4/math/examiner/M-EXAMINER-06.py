"""M-EXAMINER-06 (F4): Galactic tidal accelerations across a 10 kau pair vs internal g_N (SI).
Derivation: axisymmetric potential, Phi'(R) = Omega^2 R, Oort A = -(R/2) dOmega/dR, B = A - Omega.
  Inertial-frame radial tidal stretching: -Phi'' x with Phi'' = Omega^2 + 2 Omega R Omega' = Omega(Omega - 4A).
  Rotating (Hill) frame adds the centrifugal Omega^2 x: total 4 A Omega x = 4 A (A - B) x  (lens's form).
  Vertical: Phi_zz = 4 pi G rho0 + 2(B^2 - A^2) (Poisson in a disc); lens drops the small (B^2 - A^2) term.
Inputs as the lens supplied: A = 15.3, B = -11.9 km/s/kpc, rho0 = 0.1 Msun/pc^3, r = 10 kau, M = 1.5 Msun.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, units, identity, limit, finish

R = sp.symbols("R", positive=True)
Om = sp.Function("Omega")(R)
A = -R / 2 * sp.diff(Om, R)
Phi2 = sp.diff(Om**2 * R, R)          # Phi'' for Phi' = Omega^2 R
identity(sp.expand(Phi2 - Om * (Om - 4 * A)), 0)
identity(sp.expand(-Phi2 + Om**2), sp.expand(4 * A * Om))   # rotating-frame stretching = 4 A Omega
a_, b_ = sp.symbols("A B", real=True)
print("4A(A-B) =", 4 * 15.3 * 27.2, "(km/s/kpc)^2 [rotating frame];  inertial (A-B)(3A+B) =", 27.2 * (3 * 15.3 - 11.9))

quantity("4 * 15.3 km/s/kpc * 27.2 km/s/kpc * 10000 au", "2.6e-15 m/s^2", rel_tol=0.02)
quantity("27.2 km/s/kpc * 34.0 km/s/kpc * 10000 au", "1.45e-15 m/s^2", rel_tol=0.02)   # inertial-frame variant (my value, factor 0.56 of the lens form)
quantity("4 * pi * 6.67430e-11 m^3/(kg s^2) * 0.1 Msun/pc^3 * 10000 au", "8.5e-15 m/s^2", rel_tol=0.02)
quantity("2 * ((11.9 km/s/kpc)^2 - (15.3 km/s/kpc)^2) * 10000 au", "-2.9e-16 m/s^2", rel_tol=0.02)  # dropped term, ~3% of 8.5e-15
quantity("6.67430e-11 m^3/(kg s^2) * 1.5 Msun / (10000 au)^2", "8.9e-11 m/s^2", rel_tol=0.01)
units("4 * pi * 6.67430e-11 m^3/(kg s^2) * 0.1 Msun/pc^3 * 10000 au", "acceleration")
units("15.3 km/s/kpc * 27.2 km/s/kpc * 10000 au", "acceleration")
quantity("(4 * pi * 6.67430e-11 m^3/(kg s^2) * 0.1 Msun/pc^3 * 10000 au) / (6.67430e-11 m^3/(kg s^2) * 1.5 Msun / (10000 au)^2)",
         "9.5e-5", rel_tol=0.05)
r, k, M = sp.symbols("r k M", positive=True)
limit((k * r) / (M / r**2), "r", 0, "0")    # tide/g_N ~ k r^3 / M -> 0 for close pairs
raise SystemExit(finish())
