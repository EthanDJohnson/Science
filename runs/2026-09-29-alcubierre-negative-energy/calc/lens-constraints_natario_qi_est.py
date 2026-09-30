"""Constraints lens: fast estimate of the curvature radius of the Natario zero-expansion wall from the extrinsic
curvature (unit lapse, flat slices: Gauss part of Riemann = K K, Codazzi part = dK), calibrated on the Alcubierre
wall where the toolkit gives r_c = 1.000 Delta_PF/v exactly. Then the Ford-Roman QI-limited wall thickness and energy
for Natario at R = 100 m, v = 10c. Geometric units (G = c = 1, metres); SI conversions labelled.
K_ij = (d_i X_j + d_j X_i)/2 for the velocity field X (sign irrelevant for magnitudes).
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import to_si, PLANCK_LENGTH  # noqa: E402

MSUN = 1.989e30


def fprof(r, R, s):
    return (np.tanh(s * (r + R)) - np.tanh(s * (r - R))) / (2 * np.tanh(s * R))


def shift(kind, x, y, z, R, s, v=1.0):
    r = np.sqrt(x**2 + y**2 + z**2)
    f = fprof(r, R, s)
    if kind == "alcubierre":
        return np.stack([v * f, 0 * f, 0 * f])
    h = 1e-6
    fr = (fprof(r + h, R, s) - fprof(r - h, R, s)) / (2 * h)
    fy, fz = fr * y / r, fr * z / r
    return np.stack([v * (f + (y * fy + z * fz) / 2), -v * x * fy / 2, -v * x * fz / 2])


def kstats(kind, R, s, npts):
    D = 2.0 / s
    # sample points around the wall in the x-y half plane (z small), theta in (0, pi)
    th = np.linspace(0.01, math.pi - 0.01, npts)
    dr = np.linspace(-2.0 * D, 2.0 * D, npts)
    TH, DR = np.meshgrid(th, dr, indexing="ij")
    rr = R + DR
    X0, Y0, Z0 = rr * np.cos(TH), rr * np.sin(TH), 1e-3 + 0 * rr
    h = D * 1e-3
    grads = []  # dX_j/dx_i
    for e in np.eye(3):
        Xp = shift(kind, X0 + h * e[0], Y0 + h * e[1], Z0 + h * e[2], R, s)
        Xm = shift(kind, X0 - h * e[0], Y0 - h * e[1], Z0 - h * e[2], R, s)
        grads.append((Xp - Xm) / (2 * h))
    J = np.stack(grads)  # J[i, j] = d_i X_j
    K = 0.5 * (J + np.swapaxes(J, 0, 1))
    kmax = float(np.max(np.abs(K)))
    divX = float(np.max(np.abs(np.trace(J))))
    # second derivatives magnitude via finite difference of K along r
    return kmax, divX


print("Calibration and scaling (R = 1, v = 1): max|K_ij| and the curvature-radius estimate 1/max|K|")
rows = {}
for kind in ("alcubierre", "natario"):
    for s in (8.0, 16.0, 32.0, 64.0):
        D = 2 / s
        k1, d1 = kstats(kind, 1.0, s, 241)
        k2, _ = kstats(kind, 1.0, s, 361)
        rows[(kind, s)] = k2
        extra = f" ; K_max*Delta^2 = {k2*D**2:.4f} (Natario thin-wall law vR/Delta^2 x const)" if kind == "natario" else f" ; K_max*Delta = {k2*D:.4f}"
        print(f"{kind:10s} sigma={s:5.1f} Delta={D:.4f}: max|K| n=241 {k1:.5e}, n=361 {k2:.5e} /m ; max|div X| {d1:.2e}{extra}")

# Calibrate: Alcubierre toolkit r_c = Delta/v ; estimate 1/K_max -> factor c_A
cA = np.mean([(2 / s) / (1 / rows[("alcubierre", s)]) for s in (16.0, 32.0, 64.0)])
print(f"Alcubierre: toolkit r_c / (1/K_max) = {cA:.4f}")
kN = rows[("natario", 64.0)] * (2 / 64.0) ** 2  # K_max = kN v R / Delta^2
print(f"Natario thin-wall: K_max = {kN:.4f} v R / Delta^2 ; assume r_c = cA / K_max = {cA/kN:.4f} Delta^2/(v R)")

# Natario peak density: rho_min ~ -a v^2 R^2 / Delta^4 from Natario's formula along theta = pi/2 (sin^2 = 1):
# rho = -(v^2/8 pi) (f' + r f''/2)^2 at theta = pi/2 ; evaluate for thin wall
s = 64.0
r = np.linspace(1 - 8 / s, 1 + 8 / s, 200001)
fp = np.gradient(fprof(r, 1.0, s), r)
fpp = np.gradient(fp, r)
rho_eq = -(1 / (8 * math.pi)) * (fp + r * fpp / 2) ** 2
a = float(-rho_eq.min() * (2 / s) ** 4)
print(f"Natario peak Eulerian |rho| (equator) = {-rho_eq.min():.4e} /m^2 at sigma=64 -> a = {a:.5f} (rho_pk = -a v^2 R^2/Delta^4)")

b = cA / kN
for alpha in (0.1, 0.01):
    for (Rr, V) in ((100.0, 1.0), (100.0, 10.0)):
        D4 = 3 * PLANCK_LENGTH**2 * V**2 * Rr**2 / (32 * math.pi**2 * alpha**4 * b**4 * a)
        Dq = D4 ** 0.25
        En = -(V**2) * Rr**4 / (22.5 * Dq**3)
        print(f"alpha={alpha}, R={Rr:g} m, v={V:g}c: Natario QI wall Delta <= {Dq:.3e} m (= {Dq/PLANCK_LENGTH:.2e} L_P); r_c = {b*Dq**2/(V*Rr):.3e} m ;"
              f" E_Nat = {En:.3e} m = {to_si.mass_kg(En):.3e} kg = {to_si.mass_kg(En)/MSUN:.3e} Msun")
