#!/usr/bin/env python3
"""Task B, step 0: normalisation of the LOCAL (in-in, kinetic) pair-production rate used in Task B.

Quantity checked: pairs per unit volume per unit time,
    Gamma(x) = (1/2) int d3k1 d3k2 F(x,k1) F(x,k2) sigma(s) (1 - cos theta12),     (*)
F = graviton phase-space number density, sigma = g g -> gamma gamma cross section for the gravitons' polarisation
states (counting PAIRS, identical-photon 1/2 included), s = 2 k1 k2 (1 - cos theta12). The 1/2 avoids double counting
when both gravitons come from the same population; for two distinct beams (*) gives sigma n_a n_b (1 - cos theta).

Independent checks (none of them uses the module's amplitude code):
  (a) sigma for opposite physical helicities from the closed form |M|^2 = (8 pi G)^2 (t^4 + u^4)/s^2 (summed over the two
      non-zero photon helicity assignments; module docstring/literature form), integrated here with scipy:
      expect (4/5) pi G^2 s; linear polarisations: half of it.
  (b) two crossing plane waves: own Gamma = sigma n1 n2 (1 - cos th) with n = rho/w, rho = w^2 h^2/(32 pi G) (linear) or
      w^2 h^2/(16 pi G) (circular), versus qft_second_order.beams_pair_rate (module, background-field amplitude).
  (c) B&O's own eq. 14 (dP/dtdV = 8 pi G^2 rho_GW^2/15 for an isotropic unpolarised background) reproduced from (*) with
      sigma_unpol = (2/5) pi G^2 s by direct angular integration: this anchors (*) to B&O's own normalisation.
  (d) toy (scalar-proxy) normalisation used in later Task-B scripts: for J = psi^2 (psi = positive-frequency part of the
      field), P = int d4Q/(2pi)^4 rho(s) |J~(Q)|^2; two plane waves psi = a1 e^{-ik1x} + a2 e^{-ik2x} give
      Gamma = 4 rho(s) |a1 a2|^2 = sigma_toy n1 n2 (1-cos th) with n = 2 w |a|^2 and sigma_toy = 2 rho(s)/s, so the
      gravity-equivalent spectral weight is rho_grav(s) = sigma_lin(s) s/2 = (pi/5) G^2 s^2. Checked numerically below by
      a Monte Carlo of the momentum-space (Parseval) form of |J~|^2 for two crossing waves under a smooth space-time
      envelope (the envelope only smears s by O(1/(w L)); the identity itself is algebraic).
"""
import math
import sys

import numpy as np
from scipy import integrate

sys.path.insert(0, "/home/user/Science/.claude/skills/conundrum/scripts")
import qft_second_order as q2  # noqa: E402

PI = math.pi
G = 1.0

print("=== (a) cross section from the closed-form helicity amplitudes (own quadrature) ===")
s = 3.7


def integrand(c):
    t = -0.5 * s * (1 - c)
    u = -0.5 * s * (1 + c)
    return (8 * PI * G) ** 2 * (t ** 4 + u ** 4) / s ** 2


val, _ = integrate.quad(integrand, -1, 1, epsabs=0, epsrel=1e-13)
# sigma = (1/2: identical photons) * (1/(2s): flux) * int dPhi2, dPhi2 = dOmega/(32 pi^2), phi integral = 2 pi
sigma_opp = 0.5 / (2 * s) * (2 * PI * val) / (32 * PI ** 2)
print(f"sigma_opp(own quad)            = {sigma_opp:.12e}")
print(f"(4/5) pi G^2 s                 = {0.8 * PI * G * G * s:.12e}")
print(f"module sigma_total(R,L)        = {q2.sigma_total(s, 'R', 'L', 'photon', G=G):.12e}")
print(f"module sigma_total(plus,plus)  = {q2.sigma_total(s, 'plus', 'plus', 'photon', G=G):.12e}  (expect half: {0.4*PI*G*G*s:.12e})")
print(f"module sigma_total(plus,cross) = {q2.sigma_total(s, 'plus', 'cross', 'photon', G=G):.12e}")
print(f"module sigma_total(R,R)        = {q2.sigma_total(s, 'R', 'R', 'photon', G=G):.3e}  (same helicity: 0)")

print("\n=== (b) two crossing plane waves: own sigma n1 n2 (1-cos) vs module beams_pair_rate ===")
w1, w2, h1, h2 = 1.0, 1.3, 1e-3, 2e-3
for pol1, pol2 in [("plus", "plus"), ("plus", "cross"), ("R", "L"), ("R", "R")]:
    for th_deg in (30.0, 90.0, 150.0, 180.0):
        th = math.radians(th_deg)
        lin = lambda p: p in ("plus", "cross")
        n1 = w1 * h1 ** 2 / ((32 if lin(pol1) else 16) * PI * G)
        n2 = w2 * h2 ** 2 / ((32 if lin(pol2) else 16) * PI * G)
        ss = 2 * w1 * w2 * (1 - math.cos(th))
        if lin(pol1) or lin(pol2):
            sig = 0.4 * PI * G * G * ss
        else:
            sig = 0.8 * PI * G * G * ss if pol1 != pol2 else 0.0
        own = sig * n1 * n2 * (1 - math.cos(th))
        mod = q2.beams_pair_rate(w1, h1, w2, h2, th, pol1, pol2, "photon", G=G)["pair_rate"]
        rel = abs(mod - own) / own if own > 0 else abs(mod)
        print(f"{pol1:>5}/{pol2:<5} th={th_deg:5.1f}: own={own:.10e} module={mod:.10e}  rel.diff={rel:.1e}")

print("\n=== (c) B&O eq. 14 from the kinetic formula (*) with sigma_unpol = (2/5) pi G^2 s ===")
# isotropic monochromatic gas, number density n, energy w: Gamma = (1/2) n^2 <sigma (1 - c)>, s = 2 w^2 (1 - c)
# <f(c)> over independent isotropic directions = (1/2) int_{-1}^{1} f(c) dc
for w in (0.7, 2.0):
    n = 1.0
    avg, _ = integrate.quad(lambda c: 0.4 * PI * G * G * 2 * w * w * (1 - c) * (1 - c) * 0.5, -1, 1)
    Gam = 0.5 * n * n * avg
    rho = n * w
    print(f"w={w}: Gamma(kinetic)/rho^2 = {Gam/rho**2:.12f};  B&O eq.14: 8 pi G^2/15 = {8*PI*G*G/15:.12f}")
# broad isotropic spectrum: Gamma depends only on rho (sigma ~ s ~ k1 k2)
ks = np.linspace(0.2, 3.0, 400)
wk = np.exp(-(ks - 1.2) ** 2)          # arbitrary isotropic spectrum (number per dk, up to norm)
nk = wk / np.trapezoid(wk, ks)
rho = np.trapezoid(nk * ks, ks)
avg_c, _ = integrate.quad(lambda c: (1 - c) ** 2 * 0.5, -1, 1)
Gam = 0.5 * np.trapezoid(np.trapezoid(np.outer(nk, nk) * 0.4 * PI * G * G * 2 * np.outer(ks, ks), ks), ks) * avg_c
print(f"broad spectrum: Gamma/rho^2 = {Gam/rho**2:.12f} (expect 8 pi/15 = {8*PI/15:.12f})")

print("\n=== (d) toy normalisation: Monte Carlo of the Parseval form of |J~|^2 for two enveloped crossing waves ===")
# psi = a1 exp(-i k1.x) + a2 exp(-i k2.x); J = psi^2 contains 2 a1 a2 exp(-i K.x). With a smooth space-time envelope
# E(x) (Gaussian, widths >> 1/w), P = int d4Q/(2pi)^4 rho(Q^2) |J~(Q)|^2 should equal Gamma * int E^4 d4x with
# Gamma = 4 rho(s) |a1 a2|^2 (the 2 a1 a2 cross term; self terms have K^2 = 0 -> rho = 0).
# 1+1 dimensional reduction is not possible for a 3D phase space, so test the identity directly in momentum space:
# J~ = 2 a1 a2 E4~(Q - K) where E4~ is the FT of E^2; P = 4|a1 a2|^2 int d4q/(2pi)^4 rho((K+q)^2) |E4~(q)|^2
# -> 4|a1a2|^2 rho(K^2) int E^4 d4x  when rho varies slowly on the envelope's momentum scale. Monte Carlo check:
rng = np.random.default_rng(1)
K = np.array([2.0, 0.3, 0.0, 0.5])
s0 = K[0] ** 2 - np.sum(K[1:] ** 2)
rho_fn = lambda ss: np.where(ss > 0, ss ** 2, 0.0)
Lw = 40.0                                   # envelope width (x and t), E = exp(-x^2/(2 Lw^2)) in each of 4 coords
# FT of E^2 = exp(-x^2/Lw^2) per coordinate: sqrt(pi) Lw exp(-q^2 Lw^2/4); |.|^2 = pi Lw^2 exp(-q^2 Lw^2/2)
# sample q from the normalised density |E4~|^2/norm (Gaussian, std 1/Lw per coordinate)
qs = rng.normal(0.0, 1.0 / Lw, size=(400000, 4))
Kq = K + qs
ssq = Kq[:, 0] ** 2 - np.sum(Kq[:, 1:] ** 2, axis=1)
mean_rho = np.mean(rho_fn(ssq) * (Kq[:, 0] > 0))
# int d4q/(2pi)^4 |E4~|^2 = int E^4 d4x (Parseval) -> ratio = mean_rho / rho(s0)
print(f"<rho(s)> over envelope / rho(K^2) = {mean_rho/rho_fn(s0):.5f} (-> 1 + O(1/(w Lw)^2): Gamma = 4 rho |a1 a2|^2 confirmed)")
print("sigma_toy = Gamma/(n1 n2 (1-cos)) with n = 2 w |a|^2 and s = 2 w1 w2 (1-cos):  = 4 rho/(4 w1 w2 (1-cos)) = 2 rho/s")
print(f"gravity-equivalent weight: rho_grav(s) = sigma_lin s/2 = (pi/5) G^2 s^2 ; e.g. s=1: {PI/5:.6f}")
