"""M-DECOMPOSER-04: ladder levers as fractions of the gap (F4).

Shift in mag for an H0 change H_a -> H_b: dm = 5 log10(H_a/H_b) (from 5 log10 H0 = M_B + 5 a_B + 25);
a fractional distance change f gives dm = 5 log10(1 + f). Gap reference: 5 log10(73.264/67.19).
Cosmic variance: sigma_mag = (5/ln10) sigma_H/H.
"""
import sys
import math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import num, finish, units, inequality
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import series  # noqa: F811
import sympy as sp

gap = 5 * math.log10(73.264 / 67.19)
num("gap mag", gap, 0.188, 0.0006)
num("Cepheid photometry 0.07 mag fraction %", 100 * 0.07 / gap, 37, 0.6)
num("reddening 0.03 mag fraction %", 100 * 0.03 / gap, 16, 0.6)
dm_met = 5 * math.log10(73.50 / 73.080)   # H0DN original baseline vs no-metallicity variant (D-22, D-23)
num("metallicity term mag", dm_met, 0.012, 0.0006)
num("metallicity fraction %", 100 * dm_met / gap, 7, 0.6)
cv = 5 / math.log(10) * 0.31 / 67.19
cv2 = 5 / math.log(10) * 0.31 / 73.264
print(f"  cosmic variance in mag: {cv:.5f} (at 67.19), {cv2:.5f} (at 73.264)")
num("cosmic variance mag per sigma (at 67.19)", cv, 0.010, 0.0006)
num("gap in cosmic-variance sigmas", (73.264 - 67.19) / 0.31, 19.6, 0.06)
dm_wh = 5 * math.log10(73.49 / 70.59)
num("Wojtak-Hjorth mag", dm_wh, 0.087, 0.0006)
num("Wojtak-Hjorth fraction %", 100 * dm_wh / gap, 47, 0.6)
dm_p = 5 * math.log10(73.49 / (73.49 - 1.4 - 0.2 - 1.0))
num("Percival summed mag", dm_p, 0.078, 0.0006)
num("Percival fraction %", 100 * dm_p / gap, 42, 0.6)
dm_d = 5 * math.log10(74.30 / 71.37)
num("Dong PV mag", dm_d, 0.087, 0.0006)
num("Dong fraction %", 100 * dm_d / gap, 47, 0.6)
dm_mw = 5 * math.log10(1.009)
num("MW parallax 0.9% distance in mag", dm_mw, 0.019, 0.0006)
print(f"  MW fraction of gap: {100 * dm_mw / gap:.2f}% (lens: <= 10%)")
# "no single named effect reaches the gap; about two contested ones must add"
inequality(f"{max(dm_wh, dm_p, dm_d)!r}", "<", f"{gap!r}")
inequality(f"{dm_wh + dm_p!r}", ">=", f"{0.85 * gap!r}")

# mag <-> fractional shift: 5 log10(1+f) ~ (5/ln10) f
f = sp.symbols("f", positive=True)
series(5 * sp.log(1 + f) / sp.log(10), "f", 0, 2, 5 * f / sp.log(10))
units("(0.31 km/s/Mpc)/(67.19 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
