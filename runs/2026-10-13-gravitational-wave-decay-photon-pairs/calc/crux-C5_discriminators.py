"""Crux C5: numbers that separate C5 (linear off-shell channel dominates) from rivals.

Units: SI unless marked. k is dimensionless (natural-units coefficient in
P_lin = k G w E / c^5, w = angular GW frequency, E = radiated GW energy).
Inputs are taken from the C5 verdicts and candidates.md:
  k = 0.0251 .. 0.0357 (falsifier-C5-2 log), 67/(630 pi) = 0.033852 (C5-0, C5-1),
  1/(6 pi) upper estimate (C5-2); threshold 3.15e-4 (M-EXAMINER-09 via C5-0 log);
  P_BO = 2.92e-6 pairs, (hbar w/E_Pl)^2 N = 9.286e-3 for GW150914 (B&O inputs);
  C3 retarded fraction 0.02-0.1; C4 window 0.3-3 x P_BO times pattern 0.3-0.6;
  eq. 14 kinetic rate (8 pi/15) G^2 rho^2 / c^7 pairs m^-3 s^-1 (C6).
"""
import math

G = 6.67430e-11
c = 2.99792458e8
Msun = 1.98892e30  # kg (value only used for orders of magnitude)
Mpc = 3.0857e22

k_vals = {"C5-2 v=0.8": 0.0251, "C5-2 v=0.5": 0.0310, "exact quadrupole 67/(630pi)": 67 / (630 * math.pi),
          "C5-2 point": 0.0357, "upper 1/(6pi)": 1 / (6 * math.pi)}
k_req = 3.15e-4
P_BO = 2.92e-6
X150914 = 9.286e-3  # (hbar w/E_Pl)^2 N = G w E/c^5 for E = 2 Msun c^2, 150 Hz

print("1. Margin over C5's own survival threshold and P_lin for GW150914 (B&O inputs)")
for name, k in k_vals.items():
    print(f"   {name:30s} k = {k:.4f}  k/k_req = {k/k_req:6.1f}  P_lin = {k*X150914:.2e} pairs  P_lin/P_BO = {k*X150914/P_BO:6.1f}")

# Conformal scalar cross-check: c_J = 4/3 instead of 16
k_scalar = 67 / (630 * math.pi) * (4 / 3) / 16
print(f"   conformal-scalar k (c_J = 4/3) = {k_scalar:.2e}  (C5-1 quotes 2.8e-3; Rahvar-implied ~14 -> ratio {14/k_scalar:.1e})")

print("\n2. Total in-in yield / (eq. 8 x T_eff) predicted by each candidate (GW150914, B&O inputs)")
kmin, kmax = 0.0251, 0.0357
lin_lo, lin_hi = kmin * X150914 / P_BO, kmax * X150914 / P_BO
print(f"   C5: (P_lin + P_fus)/P_BO ~ {lin_lo:.0f} .. {lin_hi:.0f} (linear term alone)")
print("   C4: 0.3 .. 3 (x pattern 0.3-0.6 -> 0.09 .. 1.8)")
print("   C3: 0.02 .. 0.1")
print(f"   gap C5_low / C4_high = {lin_lo/3:.0f}; C5_low / C3_high = {lin_lo/0.1:.0f}")

print("\n3. Energy scaling at fixed w, sigma: d ln P / d ln E")
for name, frac in [("fusion = B&O total", 1.0), ("fusion = C3 0.1 x B&O", 0.1), ("fusion = C4 3 x B&O", 3.0)]:
    Pf = frac * P_BO
    Pl = 0.0310 * X150914
    slope = (Pl * 1 + Pf * 2) / (Pl + Pf)  # incoherent sum; interference ignored
    print(f"   {name:24s}: P_fus/P_lin = {Pf/Pl:.2e}, slope = {slope:.4f}  (C5 -> 1, C3/C4 fusion-dominated -> 2)")
LP = c**5 / G
k0 = 67 / (630 * math.pi)
Lcross = (k0 / (12 * math.pi / 25)) * LP
print(f"   crossover luminosity-weighted <L> where fusion = linear: {Lcross/LP:.4f} c^5/G = {Lcross:.2e} W")
print(f"   GW150914 L_peak = 3.6e49 W is {3.6e49/Lcross:.1e} of crossover")

print("\n4. Cosmic budget vs C6: source linear channel vs background eq.14 fusion (astrophysical SGWB)")
H0 = 67.4e3 / Mpc
rho_c_E = 3 * H0**2 * c**2 / (8 * math.pi * G)  # J/m^3
t_H = 1 / H0
w25 = 2 * math.pi * 25.0
for Om in (0.9e-9, 2.0e-9):
    rho = Om * rho_c_E
    lin_per_vol = k0 * G * w25 * rho / c**5  # pairs/m^3, energy rho emitted at 25 Hz
    fus_per_vol = (8 * math.pi / 15) * G**2 * rho**2 / c**7 * t_H  # pairs/m^3 over a Hubble time
    print(f"   Omega_GW = {Om:.1e}: rho = {rho:.2e} J/m^3; kinetic pair rate {(8*math.pi/15)*G**2*rho**2/c**7:.2e} m^-3 s^-1;"
          f" linear-at-source {lin_per_vol:.2e} vs background fusion {fus_per_vol:.2e} pairs/m^3; ratio {lin_per_vol/fus_per_vol:.1e}")
print(f"   (rho_c c^2 = {rho_c_E:.2e} J/m^3, t_H = 1/H0 = {t_H:.2e} s; bandwidth and redshift ignored, order of magnitude only)")
