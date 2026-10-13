"""M-EMPIRICIST-04: face-value ULDM luminosity ratios (SI).
W_phi(x) = W1 * x with W1 = W_phi(m = 1e-21 eV, E_rel = 2/65 M c^2, x = 1) recomputed here from the eq. 18 form.
Duration T = (1/sigma_omega of GW150914, 200 rad/s) scaled by mass, M/65 Msun.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish

G, c, hbar, eV = 6.67430e-11, 299792458.0, 1.054571817e-34, 1.602176634e-19
Msun = 1.3271244e20 / G
Lsun = 3.828e26
Mpc = 3.0856775814913673e22
OmH2 = 0.120 * (1e5 / Mpc)**2
Em = 1e-21 * eV
w = Em / hbar
M = 8800 * math.pi / w * Msun
Erel = 2 / 65 * M * c**2
N0 = Erel / Em
W1 = 9 * math.pi * (G / (hbar * c**5)) * Em**2 * 1e-9 * N0**2 * hbar**2 * OmH2 / (256 * hbar)
W5 = W1 * 1e5
T = (1 / 200) * (M / Msun) / 65
print(f"W1 = {W1:.4e} W, W(x=1e5) = {W5:.4e} W, T = {T:.4e} s, E_rel = {Erel:.4e} J")
quantity(f"{W5} W", "3.8e18 W", rel_tol=0.02)
quantity(f"{W5 / Lsun}", "1.0e-8", rel_tol=0.02)
quantity(f"{W5 / 3.6e49}", "1.1e-31", rel_tol=0.04)
quantity(f"{T} s", "1.4e6 s", rel_tol=0.02)
frac = W5 * T / Erel
print(f"converted fraction = {frac:.4e}")
quantity(f"{frac}", "5.4e-32", rel_tol=0.02)
quantity(f"{Lsun / W1}", "1.0e13", rel_tol=0.02)
W_inband1 = W1 * 5.0982e-14   # suppression from M-EMPIRICIST-03
print(f"x for 1 Lsun in-band = {Lsun / W_inband1:.3e}")
quantity(f"{Lsun / W_inband1}", "2e26", rel_tol=0.05)
units("1 W * 1 s / (1 Msun * c^2)", "dimensionless")
raise SystemExit(finish())
