"""M-ENGINEER-12: charge-to-mass of known fermions in Planck units.
Gaussian: q = Z sqrt(alpha), mu = m/m_P. Heaviside-Lorentz: q = Z sqrt(4 pi alpha).
Mass needed for q/mu < 1: m > q m_P.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, limit, finish

alpha = 7.2973525693e-3
mP_GeV = math.sqrt(1.054571817e-34 * 299792458.0 / 6.67430e-11) * 299792458.0**2 / 1.602176634e-10
me_GeV = 0.51099895e-3
print(f"m_P = {mP_GeV:.5e} GeV")
vals = {}
for name, Z, m in (("electron", 1, me_GeV), ("top", 2/3, 172.6)):
    for conv, qq in (("Gaussian", Z * math.sqrt(alpha)), ("HL", Z * math.sqrt(4 * math.pi * alpha))):
        r = qq / (m / mP_GeV)
        vals[(name, conv)] = r
        print(f"{name} {conv}: q/mu = {r:.3e} (log {math.log10(r):.2f}); m needed > {qq*mP_GeV:.3e} GeV")
quantity(f"{vals[('electron','Gaussian')]} m/m", "2.0e21 m/m", rel_tol=3e-2)
quantity(f"{vals[('electron','HL')]} m/m", "7.2e21 m/m", rel_tol=2e-2)
quantity(f"{vals[('top','Gaussian')]} m/m", "4.0e15 m/m", rel_tol=2e-2)
quantity(f"{vals[('top','HL')]} m/m", "1.4e16 m/m", rel_tol=3e-2)
quantity(f"{(2/3)*math.sqrt(alpha)*mP_GeV} GeV", "7e17 GeV", rel_tol=2e-2)
quantity(f"{math.sqrt(4*math.pi*alpha)*mP_GeV} GeV", "3.7e18 GeV", rel_tol=2e-2)
quantity("me/(hbar*c/G)^0.5", "4.185e-23 m/m", rel_tol=2e-3)
raise SystemExit(finish())
