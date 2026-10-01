"""M-ENGINEER-11 (F15): lab rotor m = 1e4 kg, R = 1 m, rim 1 km/s (omega = 1e3 rad/s).
Lens estimate Omega ~ 2 G m omega/(c^2 R) = 1.5e-20 rad/s; gap to 2e-15 rad/s = 5.1 orders. Cross-check:
Lense-Thirring dragging inside a thin spherical shell, Omega = 4 G M omega/(3 c^2 R) (standard result; we
re-derive it from the M-ENGINEER-05 Green's function: interior h_0i = -(4G/c^3)(M omega/(3R)) (omega x x)_i
-> frame rotation Omega = -(1/2) curl h_0 * c = 4GM omega/(3c^2 R)). Counterflow: same mass as two
streams (+-P, P = m u/2, R1 = 0.5 m, R2 = 1 m) gives beta = 4GP(1/R1 - 1/R2)/c^3 ~ 1e-28; 26 orders short of 0.02."""
import sys
import sympy as sp
import mpmath as mp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import identity, units, finish

# interior dipole integral: Int x'_z/|x-x'| dA for interior point on z axis = (4 pi R/3) z
Rv, zv = 7.0, 3.0
dip = mp.quad(lambda t: 2 * mp.pi * Rv**2 * Rv * mp.cos(t) * mp.sin(t) / mp.sqrt(zv**2 + Rv**2 - 2 * zv * Rv * mp.cos(t)), [0, mp.pi])
print(f"  interior dipole integral {dip} vs 4 pi R z/3 = {4*mp.pi*Rv*zv/3}")
identity(sp.Float(dip, 30), sp.Rational(4, 3) * sp.pi * 7 * 3)
# h_0 = -(4G/c^3) sigma (omega x (4 pi R/3) x) = -(4G M omega/(3 c^3 R)) (zhat x x); curl(zhat x x) = 2 zhat
# frame-dragging angular velocity Omega = (c/2)|curl h_0| = 4 G M omega/(3 c^2 R)
m, R, om = 1e4, 1.0, 1e3
Om_lens = 2 * G * m * om / (c**2 * R)
Om_LT = 4 * G * m * om / (3 * c**2 * R)
rel("lens estimate 2Gm omega/(c^2 R) (rad/s)", Om_lens, 1.5e-20, 0.02)
print(f"  thin-shell Lense-Thirring 4Gm omega/(3c^2R) = {Om_LT:.3g} rad/s, gap {lg(2e-15/Om_LT):.2f}")
near("gap to GINGERINO 2e-15 rad/s", lg(2e-15 / Om_lens), 5.1, 0.05)
inequality(repr(abs(lg(Om_LT / Om_lens))), "<=", "0.3")
P = m * 1e3 / 2
beta = 4 * G * P * (1 / 0.5 - 1 / 1.0) / c**3
print(f"  counterflow beta = {beta:.3g}; single stream m u/R: {4*G*m*1e3/(c**3*1.0):.3g}")
inequality(repr(abs(lg(beta / 1e-28))), "<=", "0.5")
near("orders short of 0.02", lg(0.02 / beta), 26, 0.7)
units("G*1 kg*(1/s)/(c^2*1 m)", "1/s")
raise SystemExit(finish())
