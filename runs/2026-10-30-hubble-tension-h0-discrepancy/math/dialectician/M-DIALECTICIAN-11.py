"""M-DIALECTICIAN-11: r_d-free H0 values against H0DN and CMB-SPA (F12).

Side-facing error: vs H0DN (above) use the value's upper error; vs SPA use the error facing SPA.
H0DN 73.264 +- 0.806; SPA 67.19 +- 0.38 (km/s/Mpc). Values [D-49].
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, finish

T, sT, P, sP = 73.264, 0.806, 67.19, 0.38
def zz(v, up, dn):
    zt = (T - v) / math.hypot(up, sT)
    sp_ = dn if v > P else up
    zp = (v - P) / math.hypot(sp_, sP)
    return zt, zp
new = [(69.2, 1.3, 1.4), (70.3, 1.4, 1.2), (69.6, 1.3, 1.8)]
old = [(66.7, 1.7, 1.9), (67.9, 1.9, 2.1)]
zn = [zz(*v) for v in new]; zo = [zz(*v) for v in old]
for v, z in zip(new + old, zn + zo):
    print(f"{v[0]}: {z[0]:.2f} sigma below H0DN, {z[1]:+.2f} sigma relative to SPA")
inequality(f"abs({min(z[0] for z in zn)} - 1.8)", "<=", "0.05")
inequality(f"abs({max(z[0] for z in zn)} - 2.7)", "<=", "0.05")
inequality(f"abs({min(z[1] for z in zn)} - 1.3)", "<=", "0.05")
inequality(f"abs({max(z[1] for z in zn)} - 2.5)", "<=", "0.05")
inequality(f"abs({min(z[0] for z in zo)} - 2.6)", "<=", "0.05")
inequality(f"abs({max(z[0] for z in zo)} - 3.5)", "<=", "0.05")
inequality(f"{max(abs(z[1]) for z in zo)}", "<=", "0.35")
raise SystemExit(finish())
