"""M-EMPIRICIST-01: eq. 16 (N_phi) into eq. 17, times 2m, equals B&O's printed W_phi.
Natural units hbar = c = 1. Independent route: derive N_phi from the definition of the
occupation number (number density / number of momentum modes inside |p| < m v), then substitute.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, units, quantity, finish

G, m, v, N0, H0, Om, x = sp.symbols("G m v N0 H0 Omega_DM x", positive=True)

# DM density: x times the cosmic mean, rho = x * Omega_DM * 3 H0^2 / (8 pi G)
rho = x * Om * 3 * H0**2 / (8 * sp.pi * G)
n = rho / m
# modes per unit volume with |p| < m v: (4 pi/3)(m v)^3 / (2 pi)^3
modes = sp.Rational(4, 3) * sp.pi * (m * v)**3 / (2 * sp.pi)**3
Nphi = sp.simplify(n / modes)
print("Derived N_phi =", Nphi)
Nphi_BO = 9 * sp.pi * H0**2 * Om * x / (4 * G * m**4 * v**3)
identity(Nphi, Nphi_BO)

# eq. 17: dP/dt = G^2 m^5 N0^2 v^6 N_phi / 128 ; power = 2 m * dP/dt (two scalars of energy ~ m)
rate = G**2 * m**5 * N0**2 * v**6 * Nphi / 128
W = 2 * m * rate
W_BO = 9 * sp.pi * G * m**2 * v**3 * N0**2 * H0**2 * Om * x / 256
identity(W, W_BO)
print("ratio W/W_BO =", sp.simplify(W / W_BO))

# limit: as v -> 0 at fixed density, the occupation grows as v^-3 while the rate goes as v^6 N_phi ~ v^3 -> 0
limit(W / (m**2 * N0**2 * H0**2 * Om * x * G), "v", 0, "0")
# and at fixed v the density relation is recovered: m * N_phi * modes = rho (x = 1 -> critical density times Omega)
identity(m * Nphi * modes, 3 * H0**2 * Om * x / (8 * sp.pi * G))

# units (SI): N_phi = 6 pi^2 n (hbar/(m v))^3 -- dimensionless number
units("1 GeV/(1 m^3 * 1 eV) * (1 hbar / (1e-22 eV/c^2 * 1e-3 * c))^3", "dimensionless")
# rate in eq. 17: G_nat^2 E^5 / hbar, G_nat = G/(hbar c^5) -> 1/s
units("(G/(hbar*c^5))^2 * (1 eV)^5 / hbar", "Hz")
# power: G_nat E^2 (hbar H0)^2 / hbar -> W
units("(G/(hbar*c^5)) * (1 eV)^2 * (hbar * 1 Hz)^2 / hbar", "W")

# numeric N_phi(1e-22 eV, v = 1e-3, x = 1), Planck 2018: Omega_c h^2 = 0.120, H0 = 100 h km/s/Mpc
# rho_DM = 0.120 * 3 (100 km/s/Mpc)^2 / (8 pi G) ; N_phi = 6 pi^2 (rho/m) (hbar/(m v c))^3 / ... in SI
import math
Gs, c, hbar, eV = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.602176634e-19
Mpc = 3.0856775814913673e22
H100 = 1e5 / Mpc
rho = 0.120 * 3 * H100**2 / (8 * math.pi * Gs)          # kg/m^3
mkg = 1e-22 * eV / c**2
n_num = rho / mkg                                      # 1/m^3
p = mkg * 1e-3 * c
modes_num = (4 / 3) * math.pi * p**3 / (2 * math.pi * hbar)**3
Nphi_num = n_num / modes_num
print(f"rho_DM = {rho:.4e} kg/m^3 = {rho*c**2/eV/1e9*1e-6:.4e} GeV/cm^3; N_phi(1e-22 eV) = {Nphi_num:.4e}")
quantity(f"{Nphi_num}", "5.75e87", rel_tol=0.02)
raise SystemExit(finish())
