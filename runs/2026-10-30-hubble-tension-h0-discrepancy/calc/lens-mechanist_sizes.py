#!/usr/bin/env python3
"""Mechanist lens: size each candidate mechanism would need against published budgets.
Units: H0 in km/s/Mpc; magnitudes in mag; distances Mpc; densities physical (omega = Omega h^2).
All input numbers are from the run dossier (D-IDs in comments)."""
import math, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import cosmo_background as cb

def dmag(h1, h2):
    """5 log10(h1/h2): magnitude-equivalent of an H0 ratio (distance-modulus / M_B shift)."""
    return 5 * math.log10(h1 / h2)

print("=== A. The gap in magnitudes (5 log10 H_loc/H_early) ===")
pairs = [("SH0ES 2025 73.49 (D-20)", 73.49, 0.93), ("H0DN corrected 73.264 (D-22)", 73.264, 0.806),
         ("SH0ES R22 73.04 (D-20)", 73.04, 1.04), ("CCHP TRGB 70.39 (D-24, quad sum 1.94)", 70.39, math.hypot(math.hypot(1.22, 1.33), 0.70))]
early = [("CMB-SPA 67.19 (D-44)", 67.19, 0.38), ("BAO+BBN 68.50 (D-45)", 68.50, 0.58), ("inverse ladder 67.19 (D-48)", 67.19, 0.65)]
for nl, hl, sl in pairs:
    for ne, he, se in early:
        g = hl - he
        print(f"{nl} vs {ne}: dH0 = {g:.2f} km/s/Mpc = {100*(hl/he-1):.2f} % = {dmag(hl, he):.3f} mag; naive {g/math.hypot(sl, se):.1f} sigma")
GAP = dmag(73.264, 67.19)
print(f"Reference gap used below: H0DN-corrected vs CMB-SPA = {GAP:.3f} mag")
print(f"SH0ES-CCHP difference 73.49 vs 70.39 = {dmag(73.49, 70.39):.3f} mag ({100*dmag(73.49,70.39)/GAP:.0f}% of reference gap)")
print(f"Distance-scale error equivalent to the gap: {100*(10**(GAP/5)-1):.1f} % (anchor distances too short)")

print("\n=== B. Ladder sub-hypotheses: required size vs published bound ===")
# B1 Cepheid photometry/crowding: JWST-HST = -0.01 +- 0.03 mag (D-09, D-78)
req = GAP; obs, sig = -0.01, 0.03
print(f"B1 crowding: need +{req:.3f} mag HST bias; JWST check {obs} +- {sig} -> needed value is {(req-obs)/sig:.1f} sigma from the measured offset")
# B2 metallicity: lever calibrated from H0DN variant with/without metallicity term (D-23: 73.080 vs 73.50 baseline D-22)
lever_mag = dmag(73.50, 73.080); gamma, sgamma = -0.234, 0.052  # Breuval 2024 (D-21)
dOH_eff = lever_mag / abs(gamma)
need_gamma_err = GAP / dOH_eff
print(f"B2 metallicity: removing the term moves H0 by {lever_mag:.3f} mag -> effective anchor-host [O/H] lever {dOH_eff:.3f} dex;"
      f" to make {GAP:.3f} mag the slope must be wrong by {need_gamma_err:.2f} mag/dex = {need_gamma_err/sgamma:.0f} sigma of gamma")
# B3 Cepheid dust: total reddening correction ~0.03 mag (D-15)
print(f"B3 Cepheid dust/R: total correction ~0.03 mag -> need {GAP/0.03:.1f}x the entire correction; host-specific R moves H0 UP by 0.8 (wrong sign)")
# B4 SN standardisation (Wojtak & Hjorth, D-35) on same data as SH0ES R22-type value 73.04-73.49
for v in (70.59, 71.45, 70.5):
    print(f"B4 SN colour/2-population: SH0ES 73.04 -> {v}: {dmag(73.04, v):.3f} mag = {100*dmag(73.04, v)/GAP:.0f}% of gap")
# B5 SN environment/young-progenitor step: offset = step * (f_young,cal - f_young,HF); calibrators ~all young
for step in (0.05, 0.10):
    for dfrac in (0.3, 0.5):
        off = step * dfrac
        print(f"B5 env step {step} mag, young-fraction difference {dfrac}: offset {off:.3f} mag = {100*off/GAP:.0f}% of gap")
# B6 anchor error: need coherent distance-scale error of all anchors
for name, frac in (("NGC4258 maser 7.558+-0.073 Mpc (D-32)", 0.073/7.558), ("LMC DEB ~1% (assumed typical)", 0.012), ("MW Gaia parallax offset 14 us ~0.9% (D-86)", 0.009)):
    need = 10**(GAP/5) - 1
    print(f"B6 anchor {name}: quoted {100*frac:.2f} % vs needed {100*need:.1f} % -> {need/frac:.1f} sigma, and all anchors must shift together")
# B7 peculiar velocities: coherent flow needed in Hubble-flow sample at mean z ~0.05-0.07
c = 299792.458
for zbar in (0.05, 0.07):
    v = (10**(GAP/5) - 1) * c * zbar
    print(f"B7 coherent outflow needed at z~{zbar}: {v:.0f} km/s (vs typical bulk flows ~ few 100 km/s; ASSUMED reference)")
print(f"B7 Dong 2026 host-PV correction 74.30->71.37: {dmag(74.30, 71.37):.3f} mag = {100*dmag(74.30,71.37)/GAP:.0f}% of gap; Laniakea +0.6 goes the other way (D-36)")
# B8 calibrator selection (Percival, D-88)
for nm, d in (("Cepheid cut-off", 1.4), ("SN selection", 0.2), ("distance prior", 1.0), ("all three if additive", 2.6)):
    print(f"B8 selection {nm}: -{d} km/s/Mpc = {dmag(73.264, 73.264-d):.3f} mag = {100*dmag(73.264, 73.264-d)/GAP:.0f}% of gap")
# B9 Hoyt SN photometry compilation (D-25)
print(f"B9 Pantheon+ vs CSP compilation shift +2 vs +0.8 km/s/Mpc: difference 1.2 km/s/Mpc = {dmag(70.0, 68.8):.3f} mag")
# B10 sum of the partially independent SN-side and selection levers
combo = dmag(73.04, 71.45) + dmag(73.264, 73.264-1.4) + dmag(74.30, 71.37)
print(f"B10 W&H(conservative)+Percival cut-off+Dong PV naive sum: {combo:.3f} mag = {100*combo/GAP:.0f}% of gap (overlap unknown; upper envelope)")

print("\n=== C. Early-side systematics: size of shift needed in the CMB/BAO inference ===")
ob, oc, th = 0.02237, 0.1200, 1.04110   # Planck 2018 (D-40/D-41 style values)
h0 = cb.solve_h_from_theta(th, ob, oc)
print(f"C0 baseline: theta=1.04110, omega_b=0.02237, omega_c=0.1200 -> h = {h0:.4f}")
h_t = cb.solve_h_from_theta(th * 1.01, ob, oc)
dlnh_dlnth = math.log(h_t / h0) / math.log(1.01)
print(f"C1 dln h / dln theta_* (fixed omega_b, omega_c) = {dlnh_dlnth:.2f}")
target = math.log(73.264 / 67.19)
need_th = target / dlnh_dlnth
print(f"C1 theta_* shift needed for 67.19->73.26: {100*need_th:.2f} % vs 0.03 % precision (D-40) -> {need_th/0.0003*1.0411/1.0411:.0f}x... i.e. {100*need_th/0.0288:.0f} sigma")
h_c = cb.solve_h_from_theta(th, ob, oc * 0.99)
dlnh_dlnoc = math.log(h_c / h0) / math.log(0.99)
need_oc = target / dlnh_dlnoc
print(f"C2 dln h / dln omega_c at fixed theta_* = {dlnh_dlnoc:.2f}; need omega_c change {100*need_oc:.1f} % "
      f"(Planck sigma(omega_c) ~0.0012 = 1.0 %, ASSUMED) -> {abs(need_oc)/0.01:.0f} sigma")
# BAO+BBN: h r_d fixed by BAO (101.54 +- 0.73 Mpc, D-45); to move 68.50 -> 73.26 need r_d down by:
need_rd = 1 - 68.50 / 73.264
print(f"C3 BAO+BBN: r_d must fall {100*need_rd:.2f} % (BAO h r_d precision {100*0.73/101.54:.2f} %) -> BAO error of {need_rd/(0.73/101.54):.0f} sigma")
# via omega_b: r_d ∝ omega_b^-0.128 (Aubourg) at fixed omega_cb
fac = (1/(1-need_rd))**(1/0.12807)
print(f"C3 or via omega_b: needs omega_b x {fac:.2f} (D/H gives omega_b to ~1 %, D-46) -> excluded")
for nm, h, s in (("Planck PR4", 67.64, 0.52), ("ACT DR6", 66.51, 0.64), ("SPT-3G", 66.66, 0.60)):
    print(f"C4 {nm} {h}+-{s}: needs its own +{73.264-h:.2f} km/s/Mpc bias = {(73.264-h)/s:.1f} sigma, same sign in three instruments")

print("\n=== D. Local channels that share no Cepheid/SN mechanism ===")
chan = [("TDCOSMO-2026 (D-31)", 71.1, 2.35), ("masers Stiskalek (D-32, stat only)", 71.6, 3.7), ("GWTC-5 sirens (D-33)", 71.7, 8.45)]
w = sum(1/s**2 for _, _, s in chan); m = sum(h/s**2 for _, h, s in chan)/w; e = w**-0.5
print(f"D1 no-ladder one-step mean (TD+masers+sirens): {m:.2f} +- {e:.2f}; vs CMB-SPA 67.19+-0.38: {(m-67.19)/math.hypot(e,0.38):.1f} sigma; vs H0DN 73.264: {(73.264-m)/math.hypot(e,0.806):.1f} sigma")
chan2 = chan + [("SBF Jensen (D-29, quad)", 73.8, math.hypot(0.7, 2.3)), ("TF CF4 (D-30, quad)", 73.3, math.hypot(2.1, 3.5))]
w = sum(1/s**2 for _, _, s in chan2); m2 = sum(h/s**2 for _, h, s in chan2)/w; e2 = w**-0.5
print(f"D2 no-SN-Ia set (+SBF+TF, which share anchors): {m2:.2f} +- {e2:.2f}; vs CMB-SPA {(m2-67.19)/math.hypot(e2,0.38):.1f} sigma")
print(f"D3 fraction of the gap carried by the one-step mean: {(m-67.19)/(73.264-67.19)*100:.0f} % (+- {e/(73.264-67.19)*100:.0f} %)")

print("\n=== E. Late-time G_eff / M_B transition ===")
# M_Ch ∝ G^-3/2; L_peak ∝ M_Ni ∝ M_Ch (Arnett, ASSUMED proportional) -> dM = -2.5 log10(L ratio) = 3.75 log10(G_HF/G_cal)
# Ladder M_B (-19.253) is FAINTER than inverse-ladder M_B (-19.39) (D-21): Hubble-flow SNe must be intrinsically
# BRIGHTER by GAP than calibrators. L ∝ G^-1.5 -> (G_HF/G_loc)^-1.5 = 10^(0.4 GAP)
Lrat = 10**(0.4 * GAP)
ratio = Lrat**(-2/3)
print(f"E1 Hubble-flow SNe must be {GAP:.3f} mag brighter (L ratio {Lrat:.3f}); with L ∝ M_Ch ∝ G^-1.5 (ASSUMED Arnett scaling): G_HF/G_local = {ratio:.3f} (D-92 quotes mu_G ~ 0.9)")
print(f"E1b ladder vs inverse-ladder M_B (D-21): {-19.253 - (-19.375):.3f} mag (cosmography) / {-19.253 - (-19.394):.3f} mag (flat LCDM)")
print(f"E2 transition must sit between calibrators (D<~40 Mpc, z<0.01) and Hubble flow (z>0.023): {0.01*c/73:.0f}-{0.023*c/73:.0f} Mpc")

print("\n=== F. Local void ===")
print(f"F1 needed local expansion excess {100*(73.264/67.19-1):.1f} %; ΛCDM sigma 0.31 km/s/Mpc (D-37) -> {(73.264-67.19)/0.31:.0f} sigma")

print("\n=== G. Fraction of the gap closed by early-time models fitted WITHOUT a SH0ES prior ===")
base, top = 67.19, 73.264
for nm, h in (("ACT DR6 EDE P-ACT-LB 69.9 (D-52)", 69.9), ("ACT DR6 PMF 69.1 (D-52)", 69.1), ("ACT DR6 mod. recomb. 69.6 (D-52)", 69.6),
              ("Planck NPIPE EDE 95% upper 69.5 (D-53)", 69.5), ("Poulin 2026 EDE profile 71.0 (D-53)", 71.0),
              ("eROSITA+ EDE 71.4 (D-94)", 71.4), ("electron-density fluct. ACT+SPT 69.3 (D-95)", 69.3)):
    print(f"G {nm}: closes {100*(h-base)/(top-base):.0f} % of the 67.19->73.26 gap; residual {dmag(top, h):.3f} mag")

print("\n=== H. SH0ES-CCHP split: sampling noise vs calibration choices ===")
per_sn = dmag(70.39 + 0.70, 70.39) * math.sqrt(24)
print(f"H1 per-SN scatter implied by CCHP sigma_SN = 0.70 km/s/Mpc over 24 SNe: {per_sn:.3f} mag")
per_host = math.hypot(per_sn, 0.06)  # plus ASSUMED ~0.06 mag per-host primary-distance error
for n1, n2 in ((11, 35), (24, 35), (11, 55)):
    s = per_host * math.sqrt(1/n1 - 1/n2)
    print(f"H2 subset of {n1} drawn from {n2}: sigma(subset mean - full mean) = {s:.3f} mag; split 70.39 vs 73.18 = {dmag(73.18,70.39):.3f} mag; 68.81 vs 73.18 = {dmag(73.18,68.81):.3f} mag")
print(f"H3 JAGB NGC 4258 field-to-field difference 0.11 mag (D-26) = {100*0.11/GAP:.0f}% of gap = {100*(10**(0.11/5)-1):.1f}% in H0; CCHP uses NGC 4258 as sole anchor (D-24)")
print(f"H4 Anand 2025 ground JAGB vs HST TRGB offset 0.17 mag (D-81) = {100*0.17/GAP:.0f}% of gap")
