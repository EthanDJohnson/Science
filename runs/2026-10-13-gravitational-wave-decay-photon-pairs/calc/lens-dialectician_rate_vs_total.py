#!/usr/bin/env python3
"""Dialectician lens: the 2 pi delta(0) -> T hinge, hbar counting, path over-count, and the chirp/binning claim.

Units: SI unless stated; natural units (hbar = c = 1) only inside the profile integrals (dimensionless after scaling).
Model: B&O eq. 8 (pair rate) R = (3/(25 pi)) G^2 N^2 w^3 sigma^2 (natural) for a transform-limited top hat of width
sigma. In SI with N = E/(hbar w): R = (3/(25 pi)) G^2 E^2 w sigma^2 / c^10 (hbar cancels -- shown symbolically below).
The in-out total of B&O's own model is P = R * T_eff, T_eff = 2 pi J_f / I_f^4 = (4 pi/3)/sigma (top hat)
(toolkit gw_coherent_fusion docstring). P = J_f * I_ang, so a spectral PHASE psi(k) (a chirp) changes P only through
J_f = int dK0 |C(K0)|^2, C(K0) = int da f(a) f(K0 - a).
"""
import math
import sys

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from unit_tools import C, G, HBAR  # noqa: E402

PI = math.pi
MSUN = 1.98847e30
MPC = 3.0857e22

print("=== Part A: hbar counting of B&O eq. 8 (symbolic) ===")
Gs, hb, c, E, w, s = sp.symbols("G hbar c E omega sigma", positive=True)
G_nat = Gs / (hb * c**5)             # G in J^-2 (G = 1/M_Pl^2, M_Pl^2 c^4 = hbar c^5/G)
N = E / (hb * w)
R_energy = sp.Rational(3, 25) / sp.pi * G_nat**2 * N**2 * (hb * w)**3 * (hb * s)**2   # rate in J
R_SI = sp.simplify(R_energy / hb)    # pairs per second
print("pair rate R [1/s] =", R_SI)
print("d ln R / d ln hbar =", sp.simplify(sp.diff(sp.log(R_SI), hb) * hb))
W = sp.simplify(2 * R_SI * hb * w)
print("photon power W = 2 R hbar w =", W, "; d ln W/d ln hbar =", sp.simplify(sp.diff(sp.log(W), hb) * hb))
kT = sp.symbols("kT", positive=True)
W_stim = sp.simplify(W * 2 * kT / (hb * w))   # (1 + 2 f) ~ 2 kT/(hbar w) in the Rayleigh-Jeans limit
print("stimulated power ~ W * 2kT/(hbar w) =", W_stim, "; d ln/d ln hbar =",
      sp.simplify(sp.diff(sp.log(W_stim), hb) * hb))

print()
print("=== Part B: GW150914 at B&O's inputs (E_rel = 2 Msun c^2, f = 150 Hz, sigma = 200 rad/s, dt = 5 ms) ===")
E_rel = 2 * MSUN * C**2
om = 2 * PI * 150.0
sig = 200.0
R = 3 / (25 * PI) * G**2 * E_rel**2 * om * sig**2 / C**10
T_eff = 4 * PI / (3 * sig)
P = R * T_eff
tau_photon = 1 / (2 * R)
print(f"E_rel = {E_rel:.4g} J, N = {E_rel / (HBAR * om):.4g}")
print(f"B&O pair rate R = {R:.4g} pairs/s; photon time tau = 1/(2R) = {tau_photon:.4g} s (B&O-style eq. 10)")
print(f"T_eff (top hat, 4 pi/(3 sigma)) = {T_eff:.4g} s; in-out total per packet P = R*T_eff = {P:.4g} pairs")
print(f"Probability that ANY pair is made by the GW150914 merger packet (Poisson) = {1 - math.exp(-P):.4g}")
D = 410 * MPC
t_prop = D / C
print(f"propagation time to Earth (410 Mpc, no cosmology) = {t_prop:.4g} s")
print(f"if R were sustained along the path: R * t_prop = {R * t_prop:.4g} pairs; over-count vs P = t_prop/T_eff = "
      f"{t_prop / T_eff:.4g}")
# B&O validity condition tau << 1/sigma
print(f"B&O condition tau << 1/sigma: tau*sigma = {tau_photon * sig:.4g} (fails if >> 1)")

print()
print("=== Part C: chirp (spectral phase) at fixed |f|: J_f(chirped)/J_f(transform-limited) ===")


def J_ratio_numeric(profile, beta, n=3001):
    """|f| profile of width 1 (sigma = 1), spectral phase psi = beta * x^2 (linear chirp). Returns J_chirp/J_0."""
    if profile == "tophat":
        x = np.linspace(-0.5, 0.5, n)
        amp = np.ones_like(x)
    else:
        x = np.linspace(-7, 7, n)
        amp = np.exp(-x**2 / 2)
    dx = x[1] - x[0]

    def J(b):
        f = amp * np.exp(1j * b * x**2)
        Cc = np.convolve(f, f) * dx            # C(K0) on the K0 grid
        return np.sum(np.abs(Cc)**2) * dx

    return J(beta) / J(0.0)


def t_rms(profile, beta, n=4001):
    """rms duration of |h(t)|^2 for the spectral amplitude f(x) = amp(x) exp(i beta x^2) (sigma = 1, time in 1/sigma)."""
    if profile == "tophat":
        x = np.linspace(-0.5, 0.5, n)
        amp = np.ones_like(x)
    else:
        x = np.linspace(-7, 7, n)
        amp = np.exp(-x**2 / 2)
    # group delay t_g = d psi/dx = 2 beta x; rms of t over |f|^2 plus transform-limited width (Gaussian exact)
    wgt = amp**2 / np.sum(amp**2)
    tg = 2 * beta * x
    return math.sqrt(np.sum(wgt * tg**2))


print("Gaussian closed form: J_chirp/J_0 = 1/sqrt(1 + 4 beta^2 sigma^4) = t_TL/t_rms exactly")
for beta in (0.0, 1.0, 5.0, 25.0, 100.0):
    num = J_ratio_numeric("gaussian", beta)
    cf = 1 / math.sqrt(1 + 4 * beta**2)
    t0 = 1 / math.sqrt(2)
    trms = math.sqrt(t0**2 + 2 * beta**2)
    print(f"  beta*sigma^2 = {beta:6.1f}: numeric {num:.6f}  closed {cf:.6f}  t_TL/t_rms {t0 / trms:.6f}")
print("Top hat (width sigma, duration of sweep t_c = 2 beta sigma): asymptote J ratio -> 3 pi/(sigma t_c)")
for beta in (5.0, 25.0, 100.0, 400.0):
    num = J_ratio_numeric("tophat", beta, n=8001)
    tc = 2 * beta
    print(f"  sigma*t_c = {tc:6.1f}: numeric {num:.5f}  3pi/(sigma t_c) = {3 * PI / tc:.5f}  ratio {num / (3 * PI / tc):.4f}")

print()
print("=== Part D: B&O chirp bins vs the model's own coherent total ===")
print("B&O bin yield Y_BO = R(sigma_b) * t_b = c_rate G^2 N^2 w^3 sigma_b^2 t_b (natural).")
print("Model total for a chirped top-hat bin (sigma_b t_b >> 1): P = c_rate * (4pi/3) * (3pi/(sigma_b t_b)) *")
print("  G^2 N^2 w^3 sigma_b = 4 pi^2 c_rate G^2 N^2 w^3 / t_b.  Y_BO/P = (sigma_b t_b / 2pi)^2.")
cases = [
    ("GW170817 bin at 100 Hz, eps = 0.1, t_eps = 0.60 s [D-48]", 0.1 * 2 * PI * 100, 0.60),
    ("GW150914 merger, sigma = 200 rad/s, dt = 5 ms [D-27]", 200.0, 5e-3),
    ("WD binary 6.2 mHz, eps = 0.1, t_eps ~ 1e13 s (assumed, inspiral time scale)", 0.1 * 2 * PI * 6.2e-3, 1e13),
]
for name, sb, tb in cases:
    x = sb * tb
    print(f"  {name}: sigma_b t_b = {x:.4g}; Y_BO/P = {(x / (2 * PI))**2:.4g}"
          + ("  (sigma t ~ 1: transform-limited, factor not applicable; ratio ~ O(1))" if x < 2 * PI else ""))

print()
print("Splitting a fixed coherent band into n bins with B&O's recipe (rate x bin time):")
print("  sum_bins = n * c (N/n)^2 (sigma/n)^2 (t/n) = c N^2 sigma^2 t / n^4  -> 'lower bound' vs eq. 8 on the full band,")
print("  while the model's own total 4pi^2 c_rate G^2 N^2 w^3 / t is independent of n and of the bandwidth.")
for n in (1, 3, 10, 30):
    sigma_t = 37.7 * 3  # an illustrative whole-inspiral-segment time-bandwidth product
    Y = (sigma_t)**2 / n**4 / (4 * PI**2)
    print(f"  n = {n:3d}: Y_BO(binned)/P_model = {Y:.4g}")

print()
print("=== Part E: sustained-source reading: rate set by luminosity, not bandwidth ===")
print("P_model/t = 4 pi^2 c_rate G^2 (N/t)^2 w^3 = 4 pi^2 c_rate G^2 L^2 w / c^10 (SI, L = GW power).")
c_rate = 3 / (25 * PI)
for name, L, f in (("GW150914 peak, L = 3.6e49 W, 150 Hz [D-29]", 3.6e49, 150.0),
                   ("GW170817 at 100 Hz, L = 1.8e44 W [D-48]", 1.8e44, 100.0)):
    wv = 2 * PI * f
    r = 4 * PI**2 * c_rate * G**2 * L**2 * wv / C**10
    print(f"  {name}: luminosity-set pair rate = {r:.4g} pairs/s; photon power = {2 * r * HBAR * wv:.4g} W")
