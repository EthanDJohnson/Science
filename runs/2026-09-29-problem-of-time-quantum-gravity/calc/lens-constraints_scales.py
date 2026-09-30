#!/usr/bin/env python3
"""Constraint audit: sizes (SI) of what each position requires or predicts, against bounds.

 1 Semiclassical WKB time: (E/m_P)^2 corrections vs precision and cosmic variance.
 2 Unimodular time: Lambda-4-volume uncertainty Delta Lambda Delta V4 >= 4 pi l_P^2 (derived below).
 3 Thermal time: Tolman-Ehrenfest ratio vs gravitational redshift over 1 mm (gr_tensors
   Schwarzschild, 50-digit precision), Unruh temperature, Hawking temperature via horizons_1p1.
 4 Gambini-Porto-Pullin clock limits vs the best clock; decoherence needed to be seen.
 5 Pikovski time-dilation decoherence and Zych clock-interferometer visibility.
 6 Diosi-Penrose: collapse time of the QGEM superposition; heating at the R0 bound.
 7 Postquantum classical gravity: the D2 squeeze (delta kernel).
Formula provenance: Q-04, Q-07, Q-09, Q-14, Q-15, Q-17, Q-20, Q-21 of the dossier; others derived here.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from gr_tensors import metrics, horizons_1p1, to_si, PLANCK_LENGTH, PLANCK_TIME
from unit_tools import HBAR, C, G

KB = 1.380649e-23
GeV = 1.602176634e-10
eV = 1.602176634e-19
yr = 3.15576e7

# ---------------------------------------------------------------- 1
print("1. Semiclassical (Kiefer-Singh) corrections ~ (E/m_P)^2, m_P = sqrt(3 pi hbar c/(2G)) (Q-17)")
mP_GeV = math.sqrt(3 * math.pi * HBAR * C / (2 * G)) * C**2 / GeV
print(f"   m_P (Kiefer convention) = {mP_GeV:.3e} GeV")
for label, E in [("Sr clock transition 1.77 eV", 1.77e-9), ("hydrogen 13.6 eV", 13.6e-9),
                 ("LHC 14 TeV", 1.4e4), ("inflation H = 1e13 GeV", 1e13), ("inflation H = 1e14 GeV (Q-19 tensor bound)", 1e14)]:
    print(f"   {label:42s}: (E/m_P)^2 = {(E/mP_GeV)**2:.2e}")
for ell in (2, 10, 30):
    print(f"   cosmic variance of C_ell at ell = {ell:2d}: sqrt(2/(2 ell+1)) = {math.sqrt(2/(2*ell+1)):.3f}")
print(f"   clock fractional precision (Q-05) 7.6e-21 vs Sr-scale correction {(1.77e-9/mP_GeV)**2:.1e}")

# ---------------------------------------------------------------- 2
print("\n2. Unimodular time: S_Lambda = -(c^3/(8 pi G)) Lambda V4 (V4 in m^4) => [V4, -(c^3/8piG) Lambda] = i hbar")
print("   => Delta Lambda * Delta V4 >= 4 pi hbar G / c^3 = 4 pi l_P^2 =", f"{4*math.pi*PLANCK_LENGTH**2:.3e} m^2")
H0 = 67.4e3 / 3.0857e22
Lam_obs = 3 * 0.685 * H0**2 / C**2
VH = 4 * math.pi / 3 * (C / H0)**3
for dt in (1e-15, 1.0, 1e9 * yr):
    dV4 = VH * C * dt
    dL = 4 * math.pi * PLANCK_LENGTH**2 / dV4
    print(f"   time resolution {dt:.1e} s over a Hubble volume: Delta V4 = {dV4:.2e} m^4 -> Delta Lambda >= {dL:.2e} m^-2"
          f" = {dL/Lam_obs:.1e} Lambda_obs (Lambda_obs = {Lam_obs:.3e} m^-2)")

# ---------------------------------------------------------------- 3
print("\n3. Thermal time vs gravitational redshift (Tolman-Ehrenfest T sqrt(-g_tt) = const)")
st, s = metrics.schwarzschild()
M_E = 3.986004418e14 / C**2          # GM_earth/c^2 in m
R_E = 6.371e6
gtt = st.g[0, 0]
v1 = st.evaluate(sp.sqrt(-gtt), (0, R_E, 1.0, 0), params={s["M"]: M_E}, precision=50)
v2 = st.evaluate(sp.sqrt(-gtt), (0, R_E + 1e-3, 1.0, 0), params={s["M"]: M_E}, precision=50)
import mpmath
with mpmath.workdps(50):
    f = lambda r: mpmath.sqrt(1 - 2 * mpmath.mpf(M_E) / mpmath.mpf(r))  # noqa: E731
    frac_hp = float(f(mpmath.mpf(R_E)) / f(mpmath.mpf(R_E) + mpmath.mpf("1e-3")) - 1)
v1f = float(st.compile(sp.sqrt(-gtt), params={s["M"]: M_E})(0, R_E, 1.0, 0))
v2f = float(st.compile(sp.sqrt(-gtt), params={s["M"]: M_E})(0, R_E + 1e-3, 1.0, 0))
print(f"   local Tolman T ratio T(R+1mm)/T(R) - 1 = sqrt(-g_tt(R))/sqrt(-g_tt(R+1mm)) - 1 = {frac_hp:.4e} (50-digit)")
print(f"   same in float64: {v1f/v2f - 1:.4e}   (float64 loses the 1e-19 difference: precision matters)")
print(f"   Newtonian -g dh/c^2 = {-9.80665e-3/C**2:.4e}; measured Sr gradient (Q-06): -9.8(2.3)e-20 per mm")
a_g = 9.80665
TU = HBAR * a_g / (2 * math.pi * C * KB)
print(f"   Unruh temperature at a = g: {TU:.3e} K; modular parameter -> proper time: dtau/ds = 2 pi c/a = {2*math.pi*C/a_g:.3e} s")
Msun_m = 1.3271244e20 / C**2
xs = np.linspace(0.5 * 2 * Msun_m, 4 * 2 * Msun_m, 20001)
hz = horizons_1p1(lambda x: -np.sqrt(2 * Msun_m / x), xs)
kap = hz[0]["kappa"]
print(f"   Painleve-Gullstrand river u = -sqrt(2M/r), M_sun: horizon at r = {hz[0]['x']:.2f} m (2M = {2*Msun_m:.2f} m), "
      f"kappa = {kap:.4e} 1/m (1/(4M) = {1/(4*Msun_m):.4e}) -> T_H = {to_si.hawking_temperature_k(kap):.3e} K")
Msun = 1.98847e30
t_ev = 5120 * math.pi * G**2 * Msun**3 / (HBAR * C**4)
print(f"   evaporation time of 1 M_sun (photon-only estimate) = {t_ev:.2e} s = {t_ev/yr:.2e} yr")

# ---------------------------------------------------------------- 4
print("\n4. Gambini-Porto-Pullin: dT ~ t_P^(2/3) T^(1/3) (Q-14); decoherence exponent (3/2) t_P^(4/3) T^(2/3) w^2 (Q-15)")
tP = PLANCK_TIME
T92 = 92 * 3600.0
print(f"   t_P = {tP:.3e} s; dT(1 s) = {tP**(2/3):.2e} s; dT(92 h) = {tP**(2/3)*T92**(1/3):.2e} s")
print(f"   Sr clock timing uncertainty over 92 h ~ 7.6e-21 x 92 h = {7.6e-21*T92:.2e} s -> gap {7.6e-21*T92/(tP**(2/3)*T92**(1/3)):.1e}")
wSr = 2 * math.pi * 429.228e12
for T in (1.0, yr, 13.8e9 * yr):
    print(f"   exponent for Sr (w = 2pi 429 THz), T = {T:.2e} s: {1.5*tP**(4/3)*T**(2/3)*wSr**2:.2e}")
for T in (1.0, 1e3):
    w_need = math.sqrt(0.01 / (1.5 * tP**(4/3) * T**(2/3)))
    print(f"   level splitting for 1% loss of coherence in T = {T:g} s: w = {w_need:.2e} rad/s = {HBAR*w_need/eV:.2e} eV")

# ---------------------------------------------------------------- 5
print("\n5. Pikovski tau_dec = sqrt(2/N) hbar c^2/(kB T g dx) (Q-07); Zych visibility |cos(w dtau/2)|, dtau = g dh T/c^2")
for label, N, Tk, dx in [("gram-scale, 300 K, dx = 1 um (Q-08)", 1e23, 300.0, 1e-6),
                         ("25 kDa molecule, ~6000 modes, 500 K, dx = 0.1 um vertical (assumed)", 6e3, 500.0, 1e-7),
                         ("QGEM diamond 1e-14 kg (1.5e12 modes), 1 K, dx = 250 um if vertical", 1.5e12, 1.0, 250e-6)]:
    tau = math.sqrt(2 / N) * HBAR * C**2 / (KB * Tk * 9.80665 * dx)
    print(f"   {label:70s}: tau_dec = {tau:.2e} s")
for dh in (0.01, 0.1, 0.5):
    dtau = 9.80665 * dh * 1.0 / C**2
    V = abs(math.cos(wSr * dtau / 2))
    print(f"   Sr clock, arms dh = {dh:4.2f} m apart for 1 s: dtau = {dtau:.2e} s, phase w dtau = {wSr*dtau:.3f} rad, visibility {V:.5f}")

# ---------------------------------------------------------------- 6
print("\n6. Diosi-Penrose for the QGEM superposition (Q-09: m = 1e-14 kg, dx = 250 um); tau = hbar/E_G")
m, rho_d, dx = 1e-14, 3510.0, 250e-6
R = (3 * m / (4 * math.pi * rho_d))**(1 / 3)
EG1 = G * m**2 * (6 / (5 * R) - 1 / dx)
for fac in (1, 2):
    print(f"   bulk sphere R = {R:.2e} m: E_G = {fac} x G m^2 (6/(5R) - 1/dx) = {fac*EG1:.2e} J -> tau_DP = {HBAR/(fac*EG1):.2e} s")
m_a = 12 * 1.66054e-27
N_at = m / m_a
for R0 in (0.54e-10,):
    EG_gran = N_at * G * m_a**2 * 6 / (5 * R0)
    print(f"   granular (per-nucleus, R0 = {R0:.2e} m) term ~ N G m_a^2 6/(5 R0) = {EG_gran:.2e} J (negligible vs bulk)")
m0 = 1.67262e-27
for R0 in (1e-15, 0.54e-10):
    dTdt = 4 * math.sqrt(math.pi) * m0 * G * HBAR / (3 * KB * R0**3)
    print(f"   DP heating (Q-04 formula) at R0 = {R0:.2e} m: dT/dt = {dTdt:.2e} K/s")

# ---------------------------------------------------------------- 7
print("\n7. Postquantum classical gravity, delta kernel (Q-20, Q-21)")
print(f"   required D2 >= 1e-24 kg^2 s m^-3 (coherence) vs allowed D2 <= 1e-41 kg^2 s m^-3 (diffusion): excluded by a factor {1e-24/1e-41:.0e}")
