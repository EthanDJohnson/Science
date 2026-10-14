"""Falsifier C8-1 (evidence angle): B&O eq. 17-18 ULDM channel.
(1) Internal bandwidth mismatch: eq. 17 needs sigma_w ~ m v^2/2, but B&O's own
    merger/inspiral bins use eps = sigma_w/w_s = 0.1 (Fig. 2) and GW150914 ringdown eps ~ 0.15.
(2) Face-value eq. 18 rescaled to the observationally allowed masses
    (Rogers & Peiris 2021: m > 2e-20 eV, 95%; Dalal & Kravtsov 2022: m > 3e-19 eV, 99%).
(3) Overdensity x needed for 1 Lsun at those masses, converted to a physical density.
Units: SI for astrophysical numbers; eV for particle masses. W_phi scaling taken from
B&O eq. 18 (W ~ 1e14 W x (1e-21 eV/m)^2 (v/1e-3)^3) and from the verified
M-EMPIRICIST-02 value 3.84e13 W (E_rel = 2/65 M c^2, x = 1) at 1e-21 eV.
"""
import math

hbar_eVs = 6.582119569e-16      # eV s
h_eVs = 4.135667696e-15         # eV s
Msun_kg = 1.98847e30
c = 2.99792458e8
Lsun = 3.828e26                 # W
pc_cm = 3.0857e18
GeV_kg = 1.78266192e-27
rho_cosmic_GeVcm3 = 1.26e-6     # cosmic mean DM density [D-41]
v = 1e-3

W1_ref = 3.841e13   # W at m = 1e-21 eV, x = 1 [M-EMPIRICIST-02]
M_ref = 1.820e10    # Msun, resonant ISCO mass at 1e-21 eV [M-EMPIRICIST-02]

print("== (1) Bandwidth mismatch inside B&O ==")
frac_res = v**2 / 2
for eps in (0.1, 0.15):
    print(f"eps = {eps}: required fractional band v^2/2 = {frac_res:.2e}; "
          f"ratio eps/(v^2/2) = {eps/frac_res:.2e}")
    # flat spectrum across a band eps*w: fraction of gravitons inside the resonant band
    f_in = frac_res / eps
    print(f"   in-band graviton fraction (flat spectrum) = {f_in:.2e}; N0^2 suppression = {f_in**2:.2e}")
    print(f"   eq.18 at 1e-21 eV, x=1, in-band only: {W1_ref*f_in**2:.2e} W")
m = 1e-21
w = m / hbar_eVs
sig_res = w * frac_res
sig_merg = 0.1 * w
print(f"w_s(1e-21 eV) = {w:.3e} rad/s; 1/sigma_res = {1/sig_res:.3e} s; 1/sigma_merger(eps=0.1) = {1/sig_merg:.3e} s; "
      f"duration ratio = {sig_res/sig_merg:.2e}")

print("\n== (2) Face-value eq. 18 at allowed masses (W propto m^-2, x = 1) ==")
for label, mm in (("B&O fiducial", 1e-21), ("B&O eq.16 norm", 1e-22),
                  ("Rogers&Peiris 95% floor", 2e-20), ("Dalal&Kravtsov 99% floor", 3e-19)):
    W = W1_ref * (1e-21 / mm)**2
    M = M_ref * (1e-21 / mm)
    f_gw = mm / h_eVs
    x_lsun = Lsun / W
    rho_GeV = x_lsun * rho_cosmic_GeVcm3
    rho_Msunpc3 = rho_GeV * GeV_kg * 1e3 * pc_cm**3 / 1e3 / Msun_kg  # GeV/cm^3 -> kg/cm^3 -> kg/pc^3
    # careful: GeV_kg is kg per GeV; rho [kg/cm^3] = rho_GeV*GeV_kg ; per pc^3 multiply pc_cm^3
    rho_Msunpc3 = rho_GeV * GeV_kg * pc_cm**3 / Msun_kg
    print(f"{label:26s} m = {mm:.0e} eV: resonant M = {M:.2e} Msun, f_GW = {f_gw:.2e} Hz, "
          f"W(x=1) = {W:.2e} W, W(x=1e5) = {W*1e5:.2e} W = {W*1e5/Lsun:.2e} Lsun; "
          f"x for 1 Lsun = {x_lsun:.2e} -> rho = {rho_GeV:.2e} GeV/cm^3 = {rho_Msunpc3:.2e} Msun/pc^3")

print("\n== check: 1 GeV/cm^3 in Msun/pc^3 ==")
print(f"{GeV_kg*pc_cm**3/Msun_kg:.4f} Msun/pc^3 per GeV/cm^3")
print("\n== (3) Face-value converted fraction at x=1e5 vs L_GW peak 3.6e49 W ==")
for mm in (1e-21, 2e-20, 3e-19):
    W = W1_ref * (1e-21 / mm)**2 * 1e5
    print(f"m = {mm:.0e} eV: W/L_GW = {W/3.6e49:.2e}")
