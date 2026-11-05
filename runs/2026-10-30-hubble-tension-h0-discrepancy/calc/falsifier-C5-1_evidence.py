"""Falsifier C5-1 (evidence angle): confront the local-structure candidate with
published numbers. Units: km/s/Mpc throughout (SI-derived astronomical units).

Inputs (all quoted in verdicts/C5-1.md):
- local ladder 73.264, CMB-SPA 67.19 (gap 6.074), BAO+BBN gap 4.764 (run log falsifier-C5-0)
- Riess et al. 2022 (arXiv:2112.04510, p.46): extending Hubble flow to z<0.8 (>1300 SNe)
  raises H0 by 0.5; excluding z<0.06 in expanded samples raises H0 by ~0.3.
- Stiskalek, Desmond & Banik 2025 (MNRAS 543 1556): void-model local H0 72.1, 70.4, 70.2.
- Boehringer et al. 2020 (A&A 633 A19): +5.5 (+2.1/-2.8) % inside a ~100-140 Mpc underdensity.
- TDCOSMO-2026 (D-31): 71.1 +2.4/-2.3.
"""
import numpy as np

H_loc = 73.264
H_cmb = 67.19
gap = H_loc - H_cmb
gap_bbn = 4.764
print(f"gap vs CMB-SPA = {gap:.3f}; vs BAO+BBN = {gap_bbn:.3f}")

# --- A: share of the gap carried by published void estimates ---
print("\n=== A: share of gap in published void estimates ===")
for lab, H in [("Stiskalek exp (disfavoured by evidence)", 72.1),
               ("Stiskalek Gaussian", 70.4), ("Stiskalek Maxwell-Boltzmann", 70.2)]:
    # their background is Planck (67.4); share relative to SH0ES-Planck-like gap
    planck = 67.4
    print(f"{lab}: local {H} -> void boost {H-planck:.2f}; share of (73.2-67.4)={73.2-planck:.1f}: "
          f"{(H-planck)/(73.2-planck)*100:.0f}%; share of run gap {gap:.3f}: {(H-planck)/gap*100:.0f}%")
for p, lab in [(5.5, "central"), (5.5 + 2.1, "upper"), (5.5 - 2.8, "lower")]:
    dH = p / 100 * H_cmb
    print(f"Boehringer {lab} {p:.1f}%: dH = {dH:.2f} -> share {dH/gap*100:.0f}% (undiluted, inside ~100-140 Mpc only)")

# --- B: R22 high-z Hubble-flow variant vs void prediction ---
print("\n=== B: R22 z<0.8 variant vs void prediction ===")
N_low = 482      # R22 Fit 33: all host types, 0.0233<z<0.15, 482 SNe (Fit 34 extends this to z<0.8)
N_all = 1300     # ">more than 1300 SNe" for z<0.8 variant (R22 p.46)
# weight beyond a void edge at z~0.15: by count with equal per-SN weight (lower bound,
# since peculiar-velocity errors de-weight the lowest-z SNe further)
w_out = (N_all - N_low) / N_all
obs_shift = +0.5
for f in [1.0, 0.8, 0.6, 0.5]:
    pred = -w_out * f * gap
    for sig in [0.5, 1.0]:
        z = (obs_shift - pred) / sig
        print(f"share f={f:.1f}: weight beyond edge {w_out:.2f}; predicted shift {pred:+.2f}, "
              f"observed {obs_shift:+.1f}; discrepancy {z:.1f} sigma for nested-shift sigma {sig}")
# break-even: share of the gap still allowed at 2 sigma with sigma_shift = 1.0
for sig in [0.5, 1.0]:
    fmax = (2 * sig - obs_shift) / (w_out * gap)
    print(f"max share allowed at 2 sigma (sigma_shift={sig}): {fmax*100:.0f}% of gap")

# --- C: time delays as a test of the candidate ---
print("\n=== C: TDCOSMO-2026 vs global H0 implied by the candidate ===")
td, td_up, td_lo = 71.1, 2.4, 2.3
for f in [1.0, 0.8, 0.6, 0.5]:
    Hg = H_loc - f * gap
    sig = td_lo if td > Hg else td_up
    print(f"share f={f:.1f}: global H0 = {Hg:.2f}; TD 71.1 sits {(td-Hg)/sig:+.2f} sigma from it")
print(f"TD vs local ladder 73.264: {(td-H_loc)/td_up:+.2f} sigma")
