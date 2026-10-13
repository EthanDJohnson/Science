"""M-CONSTRAINTS-02: SI form of eq. 14 and the quoted rates.
Natural-units Gamma = (8 pi/15) G_nat^2 rho^2 -> SI: Gamma = (8 pi/15) G^2 rho^2 / c^7 [m^-3 s^-1],
rho in J/m^3. Derived: sigma = (4/5) pi l_P^4 (s/(hbar c)^2), n = rho/(hbar w): hbar cancels.
rho_GW = (7/8)(4/11)^(4/3) DeltaN_eff rho_gamma, rho_gamma = 4.17e-14 J/m^3 (T = 2.7255 K).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import units, quantity, identity, finish
import sympy as sp

# units of the SI form
units("G^2 * (1 J/m^3)^2 / c^7", "1/(m^3 s)")
# hbar cancellation: n^2 sigma c with n = rho/(hbar w), sigma = (8pi/15)(hbar G/c^3)^2 (w/c)^2 [from s-proportional sigma]
Gs, rho, hb, w, cs = sp.symbols("G rho hbar w c", positive=True)
expr = (rho / (hb * w))**2 * (hb * Gs / cs**3)**2 * (w / cs)**2 * cs
identity(sp.simplify(expr), Gs**2 * rho**2 / cs**7)

# rho_gamma from blackbody at T0 = 2.7255 K: a T^4, a = 7.5657e-16 J m^-3 K^-4
rho_g = 7.5657e-16 * 2.7255**4
print("rho_gamma =", rho_g, "J/m^3")
quantity(f"{rho_g} J/m^3", "4.17e-14 J/m^3", rel_tol=0.01)
fac = 7 / 8 * (4 / 11)**(4 / 3)
for dn, want_rho, want_rate in [(0.3, 2.8e-15, 2.8e-109), (0.1, 9.5e-16, 3.1e-110), (0.05, 4.7e-16, 7.7e-111)]:
    r = fac * dn * rho_g
    rate = 8 * math.pi / 15 * 6.67430e-11**2 * r**2 / 299792458.0**7
    print(f"DeltaN_eff={dn}: rho_GW={r:.3e} J/m^3, pair rate={rate:.3e} m^-3 s^-1")
    quantity(f"{r} J/m^3", f"{want_rho} J/m^3", rel_tol=0.03)
    quantity(f"{rate} 1/(m^3 s)", f"{want_rate} 1/(m^3 s)", rel_tol=0.05)
print("rho_GW/rho_gamma at DeltaN_eff = 0.3:", fac * 0.3)
quantity(f"{fac*0.3}", "0.068", rel_tol=0.01)
# LVK-limited: Omega_GW = 2.8e-9 of critical density rho_c c^2 (H0 = 67.4 km/s/Mpc)
H0 = 67.4e3 / 3.0856775814913673e22
rho_c = 3 * H0**2 * 299792458.0**2 / (8 * math.pi * 6.67430e-11)
r = 2.8e-9 * rho_c
rate = 8 * math.pi / 15 * 6.67430e-11**2 * r**2 / 299792458.0**7
print("rho_crit c^2 =", rho_c, "J/m^3; LVK rho_GW =", r, "; rate =", rate)
quantity(f"{rho_c} J/m^3", "7.7e-10 J/m^3", rel_tol=0.02)
quantity(f"{rate} 1/(m^3 s)", "1.6e-115 1/(m^3 s)", rel_tol=0.1)
raise SystemExit(finish())
