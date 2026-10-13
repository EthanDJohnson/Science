#!/usr/bin/env python3
"""Examiner lens: put the toy's space-time results (lens-examiner_spacetime_toy.py) on the reference sources.

(1) Far-zone yield fraction. Toy result (retarded field, graviton-like vertex p = 2): fraction of the packet's
    yield made beyond R is F(R) ≈ 2.7e-3 at wR = 10 and falls as (wR)^-3 (fitted slopes -2.9..-3.0 for
    10 < wR < 100). Extrapolate F(R) = 2.7e-3 (10/(wR))^3 (LABELLED toy extrapolation) to astrophysical radii.
(2) B&O's eq. 19 / S12 assumption that each event radiates W_gamma for its whole propagation time:
    ratio of that path-integrated yield to the packet total (B&O 'rate' x T ~ 1/sigma).
(3) Competing near-source process (LABELLED order-of-magnitude, O(1) coefficients not computed): photon pairs
    from the source's own off-shell (time-like) field at LINEAR order in h, amplitude ~ G T (Redi-Tesi-type
    yield ∝ Int θ(q^2)|W(q)|^2). Per packet P_lin ~ k (hbar w / E_Pl)^2 N, while B&O's per-packet total is
    P_BO ~ c G^2 N^2 w^3 sigma (natural units). Ratio P_BO/P_lin ~ (c/k) G E sigma / c^5 (SI), E = N hbar w.
SI units throughout unless stated.
"""
import math

G = 6.674e-11
c = 2.998e8
hbar = 1.0546e-34
Msun = 1.989e30
pc = 3.086e16
Mpc = 1e6 * pc
AU = 1.496e11
E_Pl = math.sqrt(hbar * c ** 5 / G)       # J

F10 = 2.7e-3  # toy fraction beyond wR = 10 (retarded, p = 2) from lens-examiner_spacetime_toy.py.log


def far_fraction(w, R):
    x = w * R / c
    return F10 * (10.0 / x) ** 3 if x > 10 else float("nan")


sources = [
    # name, f_GW (Hz), E_rel (J), sigma (rad/s), distance (m)
    ("GW150914 merger (B&O inputs)", 150.0, 2 * Msun * c ** 2, 200.0, 410 * Mpc),
    ("GW170817 at 100 Hz (eps=0.1 bin)", 100.0, None, None, 40 * Mpc),
    ("Galactic WD binary (LISA, ASSUMED M_c=0.3 Msun)", 6.2e-3, None, None, 1e3 * pc),
]

print("=== (1) Far-zone yield fraction F(R) = 2.7e-3 (10/(wR/c))^3 [toy extrapolation] ===")
for name, f, E, sig, D in sources:
    w = 2 * math.pi * f
    lam_bar = c / w
    print(f"{name}: lambda/2pi = {lam_bar:.3e} m")
    for lab, R in (("100 lambda/2pi", 100 * lam_bar), ("1 AU", AU), ("1 pc", pc), ("distance", D)):
        print(f"   beyond R = {lab:15s} ({R:.2e} m): F = {far_fraction(w, R):.2e}")

print()
print("=== (2) B&O eq.19/S12: W_gamma sustained over the light-travel time vs the packet total ===")
# B&O's per-packet total ~ rate x T with T ~ 1/sigma; sustained emission over t_prop multiplies by sigma*t_prop
for name, f, E, sig, D in sources[:1]:
    t_prop = D / c
    print(f"{name}: T_packet ~ 1/sigma = {1/sig:.2e} s; light-travel time {t_prop:.2e} s;"
          f" B&O-style sustained yield / packet total = sigma*t_prop = {sig*t_prop:.2e}")
    print(f"   physically (F3 / toy): yield after the first 100 lambda/2pi is F = {far_fraction(2*math.pi*f, 100*c/(2*math.pi*f)):.1e} of the total,")
    print(f"   so the sustained-emission assumption overstates the per-event yield by ~{sig*t_prop:.0e}")
    print(f"   (relative to its own packet total) and the total converges within r ~ few lambda/2pi = {3*c/(2*math.pi*f):.2e} m")

print()
print("=== (3) Linear near-source pair production vs B&O fusion, per packet (order of magnitude) ===")
c_BO = 0.16  # c_tot for B&O's real-sign top-hat model (gw_coherent_fusion docstring: c_tot 0.16, c_rate 3/(25 pi))
for name, f, E, sig in (("GW150914 merger", 150.0, 2 * Msun * c ** 2, 200.0),
                        ("GW150914 with E=3 Msun c^2", 150.0, 3 * Msun * c ** 2, 200.0),
                        ("GW170817 100 Hz bin (eps=0.1, t_eps=0.60 s)", 100.0, 1.8e44 * 0.60, 0.1 * 2 * math.pi * 100.0)):
    w = 2 * math.pi * f
    N = E / (hbar * w)
    x_pl = hbar * w / E_Pl
    P_lin_over_k = x_pl ** 2 * N
    # B&O per-packet total in SI: c G^2 N^2 w^3 sigma (natural) -> c (G hbar / c^5)^2 N^2 w^3 sigma
    P_BO = c_BO * (G * hbar / c ** 5) ** 2 * N ** 2 * w ** 3 * sig
    ratio_param = G * E * sig / c ** 5
    print(f"{name}: N = {N:.2e}, hbar w/E_Pl = {x_pl:.2e}")
    print(f"   P_lin/k = {P_lin_over_k:.2e} pairs per packet; P_BO (c_tot=0.16) = {P_BO:.2e} pairs per packet")
    print(f"   P_BO/(P_lin/k) = {P_BO/P_lin_over_k:.2e};  check G E sigma/c^5 = {ratio_param:.2e} (x c_tot = {c_BO*ratio_param:.2e})")

print()
print("=== (4) Is the generation region inside the strong-field zone? (lambda/2pi vs GM/c^2, c/sigma) ===")
for name, f, M, sig in (("GW150914 (65 Msun, 150 Hz, sigma=200/s)", 150.0, 65 * Msun, 200.0),
                        ("GW170817 (2.74 Msun, 100 Hz)", 100.0, 2.74 * Msun, None)):
    lam_bar = c / (2 * math.pi * f)
    rg = G * M / c ** 2
    print(f"{name}: lambda/2pi = {lam_bar:.3e} m, GM/c^2 = {rg:.3e} m, ratio = {lam_bar/rg:.2f}"
          + (f"; c/sigma = {c/sig:.3e} m = {c/sig/rg:.1f} GM/c^2" if sig else ""))
    # inspiral: orbital radius a from Kepler at orbital freq f/2
    Om = math.pi * f
    a = (G * M / Om ** 2) ** (1 / 3)
    print(f"   orbital separation a = {a:.3e} m (Kepler at f_orb = f/2); lambda/2pi / a = {lam_bar/a:.2f}; v/c = {a*Om/c:.3f}")
