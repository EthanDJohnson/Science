"""Falsifier C1-1 (evidence angle): B&O's own S-matrix total versus a path-sustained eq. 8 rate.

SI units throughout (rates in 1/s, distances in m), natural-unit formula converted
with N = E/(hbar w), G_nat = G/(hbar c^5):  R = 3 G^2 E^2 w sigma^2 / (25 pi c^10)  [pairs/s].

B&O v2 SM S6 (p. 10, verbatim): "the remaining energy-conserving delta function is treated as
2 pi delta(0) -> T, the interaction time ... since T ~ 1/sigma_w, provided 1/sigma_w >> tau".
With a finite packet the delta is smeared by the packet profile, so the in->out probability
(already integrated over t from -inf to +inf, i.e. the whole propagation) is P = R * T_eff,
T_eff = 4 pi/(3 sigma) for a top-hat band (verified in M-DIALECTICIAN-02).
"""
import math

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
Msun = 1.98847e30
Mpc = 3.0856775814913673e22

# B&O GW150914 inputs (D-27)
E = 2.0 * Msun * c**2          # J
f = 150.0                      # Hz
w = 2 * math.pi * f            # rad/s
sigma = 200.0                  # rad/s
D = 410 * Mpc                  # m

R = 3 * G**2 * E**2 * w * sigma**2 / (25 * math.pi * c**10)   # pairs/s
tau = 1 / (2 * R)              # B&O eq. 10 reaction time (one photon), s
T_eff = 4 * math.pi / (3 * sigma)
P_total = R * T_eff            # in-model total over all time, pairs
t_prop = D / c
P_sustained = R * t_prop
N0 = E / (hbar * w)

print(f"eq.8 pair rate R = {R:.4e} 1/s (SI)")
print(f"B&O reaction time tau = 1/(2R) = {tau:.4e} s")
print(f"packet duration 1/sigma = {1/sigma:.4e} s ; B&O validity needs 1/sigma >> tau: ratio tau*sigma = {tau*sigma:.4e}")
print(f"T_eff = 4 pi/(3 sigma) = {T_eff:.5e} s")
print(f"in-model S-matrix total (all time, incl. all propagation) P = R*T_eff = {P_total:.4e} pairs")
print(f"sustained-rate reading over 410 Mpc: R*t_prop = {P_sustained:.4e} pairs (t_prop = {t_prop:.4e} s)")
print(f"over-count of the sustained reading relative to the model's own total: {P_sustained/P_total:.4e}")
print(f"N0 = {N0:.4e} gravitons; tau_h = tau*N0? B&O tau_h = tau*E/w (nat) -> N0/(2R)*... = {N0/(2*R):.4e} s")

# Limit check: as sigma -> 0, R -> 0 and P_total = (4/25) G^2 N^2 w^3 sigma (nat) -> 0, never infinite.
for s in (200.0, 20.0, 2.0):
    Rs = 3 * G**2 * E**2 * w * s**2 / (25 * math.pi * c**10)
    print(f"sigma = {s:6.1f} rad/s: R = {Rs:.3e} 1/s, total P = {Rs*4*math.pi/(3*s):.3e} pairs")

# Variant (b) (Jones-Singleton decay length ~1e11 m) vs GW150914 detection at 410 Mpc
L_JS = 1e11
print(f"Jones-Singleton amplitude e-fold exponent D/(2 L) = {D/(2*L_JS):.3e}")
# LIGO O3b amplitude calibration <= 11.29% -> energy e-folding length lower bound
Lmin = D / (2 * -math.log(1 - 0.1129))
print(f"energy e-folding length bound from 11.29% amplitude calibration: L >= {Lmin:.3e} m")
