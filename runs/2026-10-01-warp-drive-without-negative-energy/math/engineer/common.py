"""Shared constants and a tolerance helper for the engineer math checks (checker's own code).
SI units throughout. Constants: CODATA 2018 (c, G, hbar), IAU nominal masses (as unit_tools)."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality

c = 299792458.0          # m/s
G = 6.67430e-11          # m^3 kg^-1 s^-2
hbar = 1.054571817e-34   # J s
Msun = 1.98840987e30     # kg (IAU nominal GM / G)
Mjup = 1.89812e27        # kg
WORLD_YR = 5.9e20        # J per year, world primary energy (quoted by the lens, D-46)
YEAR = 365.25 * 86400.0
LY = c * YEAR
m_n = 1.67492750e-27     # kg, neutron mass
RHO_NUC = 0.16e45 * m_n  # kg/m^3 at 0.16 fm^-3 (standard value, as the lens)
RHO_OS = 2.26e4          # kg/m^3 osmium (standard value, as the lens)


def near(label, value, claimed, tol):
    """PASS if |value - claimed| <= tol (absolute). Prints both numbers."""
    print(f"  {label}: ours = {value:.6g}, lens = {claimed:.6g}, |diff| = {abs(value - claimed):.3g}, tol = {tol}")
    return inequality(f"{float(abs(value - claimed))!r}", "<=", f"{float(tol)!r}")


def rel(label, value, claimed, rtol):
    """PASS if |value/claimed - 1| <= rtol."""
    r = abs(value / claimed - 1.0)
    print(f"  {label}: ours = {value:.6g}, lens = {claimed:.6g}, rel diff = {r:.3g}, rtol = {rtol}")
    return inequality(f"{float(r)!r}", "<=", f"{float(rtol)!r}")


def lg(x):
    return math.log10(x)
