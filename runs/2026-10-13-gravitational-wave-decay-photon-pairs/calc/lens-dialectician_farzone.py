#!/usr/bin/env python3
"""Dialectician lens, K1 synthesis: where is the pair yield of an outgoing wave generated?

SCALING ESTIMATE (assumption-laden, labelled): outgoing spherical wave of power L at angular frequency w.
Graviton number density n(r) = L/(4 pi r^2 c hbar w). In the far zone the local momenta are radial within an angular
spread theta(r) ~ 1/(k r) (transverse momentum ~ hbar/r from the angular pattern; dossier D-55 inference, unsourced).
Tree-level g g -> gamma gamma: sigma_xs ~ G_nat^2 s, s = 2 w^2 (1 - cos theta) ~ w^2 theta^2; relative flux factor
(1 - cos theta) ~ theta^2/2. Local pair rate density ~ n^2 sigma_xs c theta^2 ~ n^2 G^2 w^2 theta^4.
=> dR/dr ~ 4 pi r^2 n^2 theta^4 ~ r^2 * r^-4 * r^-4 = r^-6, so the yield beyond radius r is a fraction ~ (r0/r)^5
of the total, r0 ~ 1/k = lambda/(2 pi) (the near zone, where the wave is not yet locally plane).
Contrast: B&O eq. 9 (N_gamma grows linearly with t, i.e. with r = c t) and footnote 4 (flux at sphere of radius c*tau).
Units: SI.
"""
import math

C = 299_792_458.0
MPC = 3.0857e22
PI = math.pi

for name, f, extra in (("GW150914, 150 Hz", 150.0, [("c*tau_BO (tau = 3578 s)", 3578 * C), ("1 AU", 1.496e11),
                                                     ("1 kpc", 3.0857e19), ("410 Mpc", 410 * MPC)]),
                        ("LISA WD binary, 6.2 mHz", 6.2e-3, [("1 kpc", 3.0857e19)])):
    lam = C / f
    r0 = lam / (2 * PI)
    print(f"{name}: lambda = {lam:.4g} m, r0 = lambda/2pi = {r0:.4g} m")
    for lab, r in extra:
        frac = (r0 / r)**5 if r > r0 else 1.0
        print(f"   fraction of yield made beyond {lab} (r = {r:.3g} m): ~ (r0/r)^5 = {frac:.3g};"
              f"  B&O linear-growth reading: yield(r)/yield(r0) = r/r0 = {r / r0:.3g}")

# check of the exponent by direct numerical integration of r^-6 from r0
import numpy as np  # noqa: E402
r = np.logspace(0, 6, 200001)   # in units of r0
dens = r**-6
cum = np.concatenate([[0], np.cumsum(0.5 * (dens[1:] + dens[:-1]) * np.diff(r))])
tot = cum[-1]
for x in (2.0, 10.0, 100.0):
    i = np.searchsorted(r, x)
    print(f"numeric fraction beyond {x:g} r0 = {(tot - cum[i]) / tot:.4g}; analytic x^-5 = {x**-5:.4g}")
