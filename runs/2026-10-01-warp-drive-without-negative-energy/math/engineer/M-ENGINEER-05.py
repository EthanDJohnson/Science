"""M-ENGINEER-05 (F9, ENGINEER-C): linearised GR, harmonic gauge, x^0 = ct.
Box hbar_0i = -16 pi G T_0i / c^4, static => |h_0i(x)| = (4G/c^3) Int g(x')/|x - x'| d^3x', g = momentum density.
Thin shell of radius R, total momentum P spread uniformly over its surface: inside, Int dA/|x-x'| = 4 pi R
(uniform), so |h_0i| = 4GP/(c^3 R). Two counterflowing shells (+P at R1, -P at R2): interior shift
beta = (4GP/c^3)(1/R1 - 1/R2), exterior field zero (monopole cancels exactly).
Normalisation check: the same Green's function reproduces the Lense-Thirring far field
g_0i = -2G (J x x)_i/(c^3 r^3) of a spinning shell (J = 2 M R^2 omega / 3).
Lens numbers: beta = 0.02, R1 = 10 m, R2 = 20 m => E_flow >= 1.2e43 J = 1.35e26 kg = 0.03 Mc^2;
u = 10 km/s => 4e30 kg; beta = 1e-6 => 2e26 kg. DEC: |g| c <= energy density, so each stream
needs E >= cP; the two streams together need E >= 2cP."""
import sys
import sympy as sp
import mpmath as mp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, limit, units, quantity, finish

r, R, th = sp.symbols("r R theta", positive=True)
dist = sp.sqrt(r**2 + R**2 - 2 * r * R * sp.cos(th))
# antiderivative of sin(th)/dist is dist/(r R); evaluate for r < R and r > R
F = dist / (r * R)
identity(sp.diff(F, th), sp.sin(th) / dist, domain={"r": (0.1, 0.9), "R": (1, 10), "theta": (0.01, 3.1)})
inside = (r + R) / (r * R) - (R - r) / (r * R)        # |r - R| = R - r for r < R
outside = (r + R) / (r * R) - (r - R) / (r * R)       # r > R
identity(2 * sp.pi * R**2 * inside, 4 * sp.pi * R)    # Int dA/|x-x'| inside: uniform
identity(2 * sp.pi * R**2 * outside, 4 * sp.pi * R**2 / r)
# numerical spot value of the monopole integral inside (r = 3, R = 7)
num = mp.quad(lambda t: 2 * mp.pi * 49 * mp.sin(t) / mp.sqrt(9 + 49 - 42 * mp.cos(t)), [0, mp.pi])
print(f"  numeric Int dA/|x-x'| at r=3, R=7: {num} vs 4 pi R = {4*mp.pi*7}")
identity(sp.Float(num, 30), 4 * sp.pi * 7)
# Lense-Thirring normalisation: dipole moment Int x'_z/|x-x'| dA for exterior point on z axis
dip = mp.quad(lambda t: 2 * mp.pi * 49 * 7 * mp.cos(t) * mp.sin(t) / mp.sqrt(30**2 + 49 - 2 * 30 * 7 * mp.cos(t)), [0, mp.pi])
print(f"  numeric dipole integral at r=30, R=7: {dip} vs 4 pi R^4/(3 r^2) = {4*mp.pi*7**4/(3*900)}")
identity(sp.Float(dip, 30), sp.Rational(4, 3) * sp.pi * 7**4 / 900)
# with sigma = M/(4 pi R^2): (4G/c^3) sigma omega (4 pi R^4/3)/r^2 = (4G/c^3)(M R^2 omega/3)/r^2 = 2 G J/(c^3 r^2)
Mm, om, Gg, cc = sp.symbols("M omega G_g c_c", positive=True)
J = sp.Rational(2, 3) * Mm * R**2 * om
identity(4 * Gg / cc**3 * Mm / (4 * sp.pi * R**2) * om * sp.Rational(4, 3) * sp.pi * R**4 / r**2, 2 * Gg * J / (cc**3 * r**2))
# limit: R2 -> R1 gives zero interior shift (counterflows on the same sphere cancel)
P, R1, R2 = sp.symbols("P R1 R2", positive=True)
beta_expr = 4 * Gg * P / cc**3 * (1 / R1 - 1 / R2)
limit(beta_expr, "R2", R1, "0")
units("4*G*(1 kg m/s)/(c^3*1 m)", "dimensionless")
# numbers
b, r1, r2 = 0.02, 10.0, 20.0
Pn = b * c**3 / (4 * G * (1 / r1 - 1 / r2))
print(f"  P per stream = {Pn:.4g} kg m/s; cP = {c*Pn:.4g} J; 2cP = {2*c*Pn:.4g} J")
rel("cP (one stream) vs lens E_flow (J)", c * Pn, 1.2e43, 0.02)
rel("cP/c^2 (kg)", Pn / c, 1.35e26, 0.01)
rel("cP/(M c^2)", Pn / c / 4.49e27, 0.03, 0.02)
rel("two-stream minimum 2cP (J) vs lens 1.2e43", 2 * c * Pn, 1.2e43, 0.02)   # expected FAIL: factor 2
rel("mass per stream at u = 10 km/s (kg)", Pn / 1e4, 4e30, 0.02)
Pm = 1e-6 * c**3 / (4 * G * (1 / r1 - 1 / r2))
rel("mass per stream at beta = 1e-6, u = 10 km/s (kg)", Pm / 1e4, 2e26, 0.02)
u_all = 2 * Pn / 4.49e27
print(f"  if all of M = 4.49e27 kg counterflows (half each way), u = 2P/M = {u_all:.4g} m/s = {u_all/c:.4f} c (lens: about 0.03c)")
raise SystemExit(finish())
