"""M-MECHANIST-03: counter-streaming momentum parts P+ = -P- for the published shell profile.

Linear, flat-slice, unit-lapse estimate (the lens's stated model). From M-MECHANIST-01 (own
derivation): for g_tx = beta_x(r) = -b S(r) (warp_shell convention, b = beta_warp),
   j_x = (1/16 pi) [ beta_x'' sin^2 th + beta_x' (1 + cos^2 th)/r ]   (geometric, 1/m^2).
P+ = int max(j_x, 0) d^3x, converted to SI by c^3/G (geometric metres -> kg m/s).
Profile S(r) and the density are the toolkit's rebuild of Fuchs et al. 2024 (input, not the lens's code).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import quantity, identity, units, finish
from warp_shell import build_shell, shift_profile, G, C

M_in, R1, R2 = 4.49e27, 10.0, 20.0
sh = build_shell(M_in, R1, R2, beta_warp=0.02)
M_ADM = sh.M_ADM
print(f"M_ADM = {M_ADM:.4e} kg; GM/c^2 = {G*M_ADM/C**2:.4f} m")

r = np.linspace(R1 + 1e-6, R2 - 1e-6, 400001)
S = shift_profile(r, R1, R2)
dS = np.gradient(S, r)
d2S = np.gradient(dS, r)
mu = np.linspace(-1, 1, 2001)  # cos th


def parts(b):
    bx1, bx2 = -b * dS, -b * d2S
    Pp = Pm = 0.0
    sin2 = 1 - mu**2
    for k in range(0, len(r), 50):  # coarse radial sampling for the 2D sum
        jx = (bx2[k] * sin2 + bx1[k] * (1 + mu**2) / r[k]) / (16 * np.pi)
        w = 2 * np.pi * r[k]**2 * (r[1] - r[0]) * 50
        Pp += np.trapezoid(np.clip(jx, 0, None), mu) * w
        Pm += np.trapezoid(np.clip(jx, None, 0), mu) * w
    return Pp, Pm


for b, claimed, frac in [(0.02, "6.8e34 kg*m/s", 0.050), (0.04, "1.35e35 kg*m/s", 0.10)]:
    Pp, Pm = parts(b)
    Pp_SI, Pm_SI = Pp * C**3 / G, Pm * C**3 / G
    print(f"beta={b}: P+ = {Pp_SI:.4e}, P- = {Pm_SI:.4e} kg m/s; net/P+ = {(Pp+Pm)/Pp:.2e}; "
          f"P+/(M_ADM c) = {Pp_SI/(M_ADM*C):.4f}")
    quantity(f"{Pp_SI} kg*m/s", claimed, rel_tol=0.03)
    quantity(f"{Pp_SI/(M_ADM*C)} m/m", f"{frac} m/m", rel_tol=0.03)
    identity(f"{round(abs((Pp+Pm)/Pp), 4)}", "0")
# linearity limit: P+ scales as beta
Pa, _ = parts(0.02)
Pb, _ = parts(0.04)
identity(f"{Pb/Pa:.10f}", "2.0000000000")
units("(1 m) * (2.998e8 m/s)^3 / (6.674e-11 m^3/(kg*s^2))", "kg*m/s")
raise SystemExit(finish())
