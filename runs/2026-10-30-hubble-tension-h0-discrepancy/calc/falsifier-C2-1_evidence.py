"""Falsifier C2-1 (evidence angle): size the C2 sub-hypotheses against published,
quoted error budgets. Units: H0 in km/s/Mpc; omega_b dimensionless; percentages."""
import math

H_loc = 73.264        # H0DN-corrected local reference (candidates.md convention)
H_SH0ES = 73.49
H_CMB = 67.19         # CMB-SPA, Camphuis et al. 2025 abstract
mid = 0.5 * (H_CMB + H_loc)
print(f"midpoint (dominance threshold) = {mid:.3f} km/s/Mpc")

# (1) Polarisation-only Planck PR4 (D-41): foregrounds are subdominant in TE/EE.
for lab, h, s in [("PR4 TE", 68.49, 0.76), ("PR4 EE", 68.49, 1.91), ("PR4 TT", 67.89, 1.11)]:
    print(f"{lab}: {h}±{s}; gap to {H_loc} = {H_loc-h:.2f} = {(H_loc-h)/s:.2f} sigma; "
          f"to midpoint {mid-h:.2f} = {(mid-h)/s:.2f} sigma")

# (2) BBN: needed omega_b x1.26 (M-MECHANIST-07) vs Schoneberg 2024 conservative
#     rate-marginalised omega_b = 0.02218 +- 0.00055 (arXiv:2401.15054 abstract)
wb, swb = 0.02218, 0.00055
need = 1.26 * wb
print(f"BBN: conservative omega_b = {wb}±{swb} ({100*swb/wb:.2f}%); x1.26 -> {need:.5f}, "
      f"{(need-wb)/swb:.1f} sigma of the rate-marginalised error")
# even reaching only the midpoint: scale factor needed ~ linear-in-log fraction
fmid = math.log(mid / 68.51) / math.log(H_loc / 68.51)
need_mid = wb * 1.26 ** fmid
print(f"BBN to reach midpoint {mid:.2f} from DESI+BBN 68.51: omega_b x{1.26**fmid:.3f} "
      f"= {(need_mid-wb)/swb:.1f} sigma (log-linear interpolation of x1.26)")

# (3) BAO: needed r_d (equivalently common BAO distance scale) shift 6.5% (M-MECHANIST-07)
for lab, sys in [("alpha_AP fiducial-cosmology sys (DR2) 0.18%", 0.18),
                 ("Lya theoretical sys 0.3%", 0.3)]:
    print(f"BAO: needed 6.5% common shift = {6.5/sys:.0f} x {lab}")

# (4) DESI-CMB Omega_m discrepancy: largest early-type value
for lab, h in [("DESI+BBN", 68.51), ("P-ACT+DESI DR2", 68.43)]:
    frac = (h - H_CMB) / (H_loc - H_CMB)
    print(f"{lab} {h}: fraction of gap from CMB-SPA = {frac:.3f}")

# (5) Likelihood choice (Plik vs CamSpec-NPIPE, D-41): 0.24 km/s/Mpc
print(f"likelihood-choice shift 0.24 = {0.24/(H_loc-H_CMB):.3f} of the gap; "
      f"needs x{(mid-H_CMB)/0.24:.1f} to reach the midpoint")
# (6) PR3 -> PR4 shift (A_L reduced): 67.36 -> 67.64
print(f"PR3->PR4 shift 0.28 = {0.28/(H_loc-H_CMB):.3f} of the gap")
