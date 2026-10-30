"""Falsifier C4-0 (magnitude angle): how much of the local-vs-early H0 gap can each
post-recombination variant of C4 carry, class by class?

Units: H0 in km/s/Mpc; magnitudes in mag; temperatures in K; fluxes in W/m^2;
times in Myr.  All inputs are dossier values (IDs in comments) or math-check rows.
"""
import math

def mag(h1, h2):
    return 5 * math.log10(h1 / h2)

def wmean(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(v * wi for (v, _), wi in zip(vals, w)) / sum(w)
    return m, math.sqrt(1 / sum(w))

print("=== A. Reference gap (H0DN-corrected vs CMB-SPA) ===")
H_loc, s_loc = 73.264, 0.806      # D-22
H_cmb, s_cmb = 67.19, 0.38        # D-44
H_bbn, s_bbn = 68.50, 0.58        # D-45
gap = H_loc - H_cmb
mid = 0.5 * (H_loc + H_cmb)
print(f"gap = {gap:.3f} km/s/Mpc = {mag(H_loc,H_cmb):.4f} mag; midpoint (dominance line) = {mid:.3f}")

print("\n=== B. Variant (i): smooth H(z) changes, standard r_d ===")
# inverse distance ladder D-48 (H(z)-shape-free given r_d)
for lab, h, s in [("IDL cosmography", 67.19, 0.65), ("IDL flat LCDM", 67.67, 0.685)]:
    frac = (h - H_cmb) / gap
    up2 = (h + 2 * s - H_cmb) / gap
    nsig = (mid - h) / s
    print(f"{lab}: H0={h:.2f}+-{s:.3f}; fraction of gap carried = {100*frac:.1f}% "
          f"(2-sigma upper {100*up2:.1f}%); reaching the midpoint {mid:.2f} needs a {nsig:.2f} sigma upward fluctuation")
# DESI DR2 evolving-DE / wCDM fits D-51 (with CMB and/or SNe)
for lab, h in [("w0wa DESI+CMB", 63.6), ("w0wa +Pantheon+", 67.51), ("w0wa +Union3", 65.91),
               ("w0wa +DESY5", 66.74), ("wCDM +Pantheon+", 67.97), ("wCDM +Union3", 68.01),
               ("wCDM +DESY5", 67.34), ("wCDM DESI+CMB (no SN)", 69.51)]:
    print(f"  {lab:24s} H0={h:.2f}: shift vs CMB-SPA LCDM {h-H_cmb:+.2f} -> fraction of gap {100*(h-H_cmb)/gap:+.1f}%")
# constant-w solution M-CONSTRAINTS-10: Omega_m = 0.2664
om_w = 0.2664
for lab, om, s in [("DESI DR2 BAO", 0.2975, 0.0086), ("SN (DES-SN5YR, flat LCDM)", 0.322, 0.012)]:
    print(f"  w=-1.194 solution Omega_m={om_w} vs {lab} {om}+-{s}: {(om-om_w)/s:.2f} sigma")

print("\n=== C. Variant (ii), G_eff form: what a 9-12% G step 145-333 Myr ago does to Earth ===")
# G ratios (G_before_step / G_now) from M-CONSTRAINTS-11 / M-MECHANIST-12
# Homology: L_sun ∝ G^7 M^5; adiabatic orbit r ∝ 1/(G M) => insolation ∝ G^9, T ∝ G^(9/4)
# (M&P 2021 quote T ∝ G^2.25 themselves).
T_now = 288.15         # K, present GMST (15 C)
PhanDA = (284.15, 309.15)  # K, Judd et al. 2024 GMST range 11-36 C over 485 Myr
S0 = 1361.0            # W/m^2 solar constant
albedo = 0.30
for lab, g in [("Chandrasekhar sign, dm=0.146", 0.914254), ("Chandrasekhar sign, dm=0.188", 0.890977),
               ("M&P headline mu_G=0.9", 0.90), ("opposite (Wright-Li) sign, dm=0.146", 1.09379),
               ("opposite sign, dm=0.188", 1.12236)]:
    ins = g**9
    Tfac = g**2.25
    dF = S0 / 4 * (1 - albedo) * (ins - 1)
    T_then = T_now * Tfac
    T_cold = PhanDA[0] * Tfac
    T_warm = PhanDA[1] * Tfac
    print(f"{lab}: G ratio {g:.4f}; L_sun ratio G^7 = {g**7:.3f}; insolation ratio G^9 = {ins:.3f}; "
          f"absorbed-flux change {dF:+.0f} W/m^2; T factor G^2.25 = {Tfac:.3f}")
    print(f"     no-feedback GMST before step: from today's 288 K -> {T_then:.0f} K ({T_then-273.15:+.0f} C); "
          f"scaling the PhanDA extremes -> {T_cold:.0f}-{T_warm:.0f} K ({T_cold-273.15:+.0f} to {T_warm-273.15:+.0f} C) "
          f"vs PhanDA 11 to 36 C")
    if dF < 0:
        # CO2 needed to offset (simplified Myhre et al. 1998 forcing 5.35 ln C/C0; order of magnitude only)
        ln_ratio = -dF / 5.35
        print(f"     greenhouse offset needed: {-dF:.0f} W/m^2 = {-dF/3.7:.0f} CO2 doublings (5.35 ln C/C0 law; illustrative)")
lb = (144.5, 333.3)  # Myr, M-CONSTRAINTS-11
print(f"step lookback window {lb[0]}-{lb[1]} Myr (M-CONSTRAINTS-11); Mesozoic 252-66 Myr ago lies inside/around it; "
      f"pre-step epoch includes everything older than {lb[0]} Myr")

print("\n=== D. Variant (ii), SN-only (non-gravitational) step: predicted vs observed non-SN H0 ===")
TD = (71.1, 2.35)      # D-31 symmetrised
MAS = (71.6, 3.7)      # D-32 stat only
GW = (71.7, 8.45)      # D-33 symmetrised
SBF = (73.8, math.hypot(0.7, 2.3))  # D-29
TF = (73.3, 4.1)       # D-30
sets = {"one-step (TD, masers, sirens)": [TD, MAS, GW],
        "one-step + SBF": [TD, MAS, GW, SBF],
        "one-step + SBF + TF": [TD, MAS, GW, SBF, TF]}
for lab, vals in sets.items():
    m, s = wmean(vals)
    for plab, p, sp in [("CMB-SPA", H_cmb, s_cmb), ("BAO+BBN", H_bbn, s_bbn)]:
        z = (m - p) / math.hypot(s, sp)
        chi2 = sum(((v - p) / math.hypot(sv, sp))**2 for v, sv in vals)
        print(f"{lab}: mean {m:.2f}+-{s:.2f}; vs (ii)'s true H0 = {plab} {p}: {z:.2f} sigma; "
              f"chi2 of all points to prediction = {chi2:.2f} for {len(vals)} dof")
    print(f"   fraction of gap these classes put on the LOCAL side (not carried by an SN step): "
          f"{100*(m-H_cmb)/gap:.0f}% (vs CMB-SPA)")

print("\n=== E. Variant (iii): Cepheid-only screened fifth force ===")
need = mag(H_loc, H_cmb)
# Li 2025 JAGB - Cepheid on same hosts: -0.03 +- 0.02 (stat) +- 0.05 (sys)  (D-26)
d_obs, s_obs = 0.03, math.hypot(0.02, 0.05)
print(f"needed Cepheid-specific brightening = {need:.3f} mag; observed |JAGB-Cepheid| = {d_obs} +- {s_obs:.3f} mag "
      f"-> prediction off by {(need-d_obs)/s_obs:.2f} sigma")
for lab, hc, ho in [("SH0ES JWST D<=25 Mpc: Cepheid 73.4 vs TRGB 72.1", 73.4, 72.1),
                    ("SH0ES JWST D<=25 Mpc: Cepheid 73.4 vs JAGB 72.2", 73.4, 72.2),
                    ("SH0ES 73.49 vs CCHP TRGB 70.39 (different hosts/SNe)", 73.49, 70.39)]:
    dm = mag(hc, ho)
    print(f"{lab}: Cepheid-specific part {dm:.3f} mag = {100*dm/need:.0f}% of the gap")
