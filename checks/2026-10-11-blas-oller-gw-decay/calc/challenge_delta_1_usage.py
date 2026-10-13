#!/usr/bin/env python3
"""Challenge delta-1 (TASK C, findings 2-6): independent re-checks with my own constants and discretisations.

(a) T_eff = P_tot/R(0) for the top-hat and Gaussian band profiles: brute-force 2D grid in the band offsets (d1, d2), binned by
    x = d1 + d2. This is a different discretisation from taskC1's closed forms.
(b) Chirp: P_tot(chirp)/P_tot(transform-limited), with the same brute-force 2D grid and phase exp(i (d1^2+d2^2) D/(2 sig)),
    compared with 3 pi/(sig D). No Fresnel functions.
(c) SB example (E_rel = M_sun, eps = 0.15), with my own constants.
(d) Inspiral bins RESTRICTED to B&O's own allowed region tau < min(1/(eps w), t_eps) and tau < t_universe. The finding only
    quoted points over the whole plane. Both without and with B&O's CMB stimulated factor (1 + 2 f_gamma(w)), which shortens
    tau and leaves the overestimate ratio unchanged.
(e) h^4 identity, and eq.8/(eq.14 V).
"""
import math
import numpy as np
import sympy as sp

PI = math.pi
hbar = 6.582119569e-16          # eV s
MPl = 1.220890e28               # eV (non-reduced Planck mass)
Gn = 1 / MPl ** 2               # eV^-2
c = 2.99792458e8
Msun = 1.98847e30 * c ** 2 / 1.602176634e-19   # eV
GMsun_s = 4.925490947e-6        # s
t_univ = 13.8e9 * 3.15576e7     # s
kT0 = 8.617333e-5 * 2.7255      # eV


def conv_H(a, dd):
    """H on the lattice x_m = d_i + d_j: exact discrete convolution H_m = sum_i a_i a_(m-i) dd (bin width dd)."""
    return np.convolve(a, a) * dd


def teff(a, dd):
    H = conv_H(a, dd)
    return 2 * PI * np.sum(np.abs(H) ** 2) * dd / abs(np.sum(H) * dd) ** 2, np.sum(np.abs(H) ** 2) * dd


print("=" * 100)
print("(a) T_eff = 2 pi int H^2 dx / (int H dx)^2, by exact discrete convolution in the band offsets (sig = 1)")
for n in (2000, 20000):
    d = (np.arange(n) + 0.5) / n - 0.5
    print(f"   top hat (n={n}): T_eff = {teff(np.ones(n), 1/n)[0]:.6f}/sig   (claim 4 pi/3 = {4*PI/3:.6f})")
    L = 16.0
    dg = (np.arange(n) + 0.5) / n * L - L / 2
    print(f"   Gaussian exp(-(k-w)^2/(2 sig^2)) (n={n}): T_eff = {teff(np.exp(-dg**2/2), L/n)[0]:.6f}/sig   "
          f"(claim sqrt(pi/2) = {math.sqrt(PI/2):.6f})")

print("=" * 100)
print("(b) chirp f = exp(i d^2 D/(2 sig)): P_tot(chirp)/P_tot(transform-limited) by discrete convolution vs 3 pi/(sig D)")
n = 40000
d = (np.arange(n) + 0.5) / n - 0.5
P0 = teff(np.ones(n), 1 / n)[1]
for sD in (2 * PI, 20.0, 100.0, 300.0, 1000.0, 3000.0):
    r = teff(np.exp(1j * d ** 2 * sD / 2), 1 / n)[1] / P0
    print(f"   sig D = {sD:7.2f}: ratio = {r:.5f}   3pi/(sig D) = {3*PI/sD:.5f}   "
          f"eq.8 / (in-out pairs per D) = (3 sig D/(4 pi))/ratio = {3*sD/(4*PI)/r:11.3f}   (sig D)^2/(4pi^2) = {sD**2/(4*PI**2):11.3f}")

print("=" * 100)
print("(c) SB example, own constants: E_rel = M_sun c^2, eps = 0.15")
def tau_s(E, w, sig):
    return 25 * PI / (6 * Gn ** 2 * E ** 2 * w * sig ** 2) * hbar
for w in (1e4,):
    sig = 0.15 * w
    N0 = Msun / w
    ta = tau_s(Msun, w, sig)
    th = ta * N0
    frac = (4 * PI / 3) * (hbar / sig) / th
    print(f"   w = {w:.0e} eV: N0 = {N0:.4e}, tau = {ta:.4e} s, tau_h = {th:.4e} s (t_univ = {t_univ:.3e} s), "
          f"converted fraction (4pi/3)/(sig tau_h) = {frac:.4e}, photons = {frac*N0:.4e}")
wstar = 1e4 * (tau_s(Msun, 1e4, 1.5e3) * Msun / 1e4 / t_univ) ** 0.25
print(f"   w with tau_h = t_univ: {wstar:.4e} eV;  w for converted fraction = 1: "
      f"{1e4 * (1/((4*PI/3)*(hbar/1.5e3)/(tau_s(Msun,1e4,1.5e3)*Msun/1e4)))**(1/3):.4e} eV")

print("=" * 100)
print("(d) inspiral bins inside B&O's allowed region (eps = 0.1, equal mass): overestimate eq.8/(in-out per t_eps) ~ (sig t_eps)^2/(4pi^2)")
eps = 0.1
for stim in (False, True):
    worst = (0, None)
    count = 0
    tot = 0
    rows = []
    for lM in np.arange(0, 9.01, 0.25):
        M = 10 ** lM
        Mc = M / 2 ** 1.2
        nuI = 1 / (6 ** 1.5 * PI * GMsun_s * M)
        for lnu in np.arange(-5, 4.01, 0.125):
            nu = 10 ** lnu
            if nu >= nuI:
                continue
            tot += 1
            om = 2 * PI * nu
            teps = 5 * eps / (12 * (2 * (GMsun_s * Mc) ** 5 * om ** 8) ** (1 / 3))
            L = 32 / 5 * (GMsun_s * Mc * PI * nu) ** (10 / 3) * c ** 5 / 6.674e-11   # W
            Erel = L * teps / 1.602176634e-19   # eV
            w = hbar * om
            sig = eps * w if teps > 1 / (eps * om) else hbar / teps
            ta = tau_s(Erel, w, sig)
            if stim:
                ta /= (1 + 2 / math.expm1(w / kT0))
            if ta < min(1 / (eps * om), teps) and ta < t_univ:
                count += 1
                sD = sig / hbar * teps
                over = sD ** 2 / (4 * PI ** 2) if sD > 50 else float("nan")
                if sD > 50 and over > worst[0]:
                    worst = (over, (M, nu, teps, ta))
                rows.append((M, nu, sD, over))
    print(f"   stimulated factor {'ON ' if stim else 'OFF'}: {count}/{tot} grid points allowed;  max (sig t_eps)^2/(4pi^2) "
          f"inside allowed region = {worst[0]:.3e} at M = {worst[1][0] if worst[1] else None} Msun, nu = {worst[1][1] if worst[1] else None} Hz")
    if rows:
        sDs = np.array([r[2] for r in rows])
        print(f"      sig t_eps over allowed points: min {sDs.min():.3e}, median {np.median(sDs):.3e}, max {sDs.max():.3e}")
# the specific points quoted by the finding
for (M, nu) in ((1.0, 1e-3), (1.0, 10.0), (10.0, 10.0), (65.0, 10.0)):
    Mc = M / 2 ** 1.2
    om = 2 * PI * nu
    teps = 5 * eps / (12 * (2 * (GMsun_s * Mc) ** 5 * om ** 8) ** (1 / 3))
    L = 32 / 5 * (GMsun_s * Mc * PI * nu) ** (10 / 3) * c ** 5 / 6.674e-11
    Erel = L * teps / 1.602176634e-19
    w = hbar * om
    ta = tau_s(Erel, w, eps * w)
    stimf = 1 + 2 / math.expm1(w / kT0)
    print(f"   quoted point M={M} Msun nu={nu} Hz: (eps n)^2 = {(eps*om*teps/(2*PI))**2:.3e}; tau = {ta:.3e} s "
          f"(with CMB stim {ta/stimf:.3e} s) vs min(1/(eps w), t_eps) = {min(1/(eps*om), teps):.3e} s -> "
          f"{'inside' if ta/stimf < min(1/(eps*om), teps) else 'OUTSIDE'} B&O allowed region (stim on)")

print("=" * 100)
print("(e) symbolic identities")
G, E, w, d, r, V, N = sp.symbols("G E omega delta r V N", positive=True)
Ptot = sp.Rational(4, 25) * G ** 2 * (E / w) ** 2 * w ** 3 * d
h2 = 8 * G * E * d / (r ** 2 * w ** 2)          # from E d/(4 pi r^2) = w^2 h^2/(32 pi G)
print(f"   P_tot / h^4 = {sp.simplify(Ptot / h2**2)}   (claim w^5 r^4/(400 delta))")
eq8 = 3 * G ** 2 * N ** 2 * w ** 3 * d ** 2 / (25 * sp.pi)
eq14V = 8 * sp.pi * G ** 2 * (N * w / V) ** 2 / 15 * V
print(f"   eq.8/(eq.14 V) = {sp.simplify(eq8/eq14V)}   (claim 9 V sig^2 w/(40 pi^2))")
