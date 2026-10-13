"""M-IDEALIZER-11: SGWB numbers (F9). SI. Gamma = (8 pi/15) G^2 rho^2/c^7 (M-05). rho = 2.8e-15 J/m^3 (DeltaN_eff = 0.3,
quoted input); LVK Omega_GW = 2.8e-9 with rho_c c^2 = 3 H0^2 c^2/(8 pi G), H0 = 67.4 km/s/Mpc (lens's choice).
Fraction of GW energy converted per Hubble time at 25 Hz: Gamma * (2 hbar w) * (1/H0) / rho, w = 2 pi 25.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

G, c, hbar, Mpc = 6.67430e-11, 299792458.0, 1.054571817e-34, 3.0856775814913673e22
H0 = 67.4e3 / Mpc
def Gam(rho): return 8 * math.pi / 15 * G**2 * rho**2 / c**7
rho1 = 2.8e-15
rho2 = 2.8e-9 * 3 * H0**2 * c**2 / (8 * math.pi * G)
w = 2 * math.pi * 25
for rho, lg, lf in ((rho1, 2.7e-109, 1.5e-108), (rho2, 1.6e-115, 1.1e-111)):
    g = Gam(rho); frac = g * 2 * hbar * w / H0 / rho
    print(f"rho = {rho:.3e} J/m^3: Gamma = {g:.3e} m^-3 s^-1, fraction per Hubble time = {frac:.3e}")
    quantity(f"{g}", f"{lg}", rel_tol=2e-2); quantity(f"{frac}", f"{lf}", rel_tol=4e-2)
units("(6.674e-11 m^3/(kg s^2))^2 * (2.8e-15 J/m^3)^2 / c^7", "1/(m^3 s)")
units("(1 /(m^3 s)) * hbar * (157 /s) * (1 s) / (1 J/m^3)", "dimensionless")
raise SystemExit(finish())
