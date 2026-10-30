"""Dialectician lens: numbers behind three syntheses of the Hubble-tension contradictions.

Units: H0 in km/s/Mpc; magnitudes in mag; r_d in Mpc. All inputs are dossier values (IDs in comments).
Tensions are naive (uncorrelated) unless stated; correlations noted in the analysis file.
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import tension, weighted_mean, total_error, precision_needed  # noqa: E402


def mag_from_ratio(r):
    """Distance-modulus / M_B shift (mag) equivalent to an H0 ratio r: 5 log10 r."""
    return 5 * math.log10(r)


def frac_from_mag(dm):
    return 10 ** (dm / 5) - 1


print("=== Contradiction 1: SH0ES vs CCHP (calibrator sample variance) ===")
# Per-SN calibrator scatter (mag), two independent estimates from dossier numbers:
# (a) R22 'SN calibrator statistics 0.020 mag' with 42 SNe (dossier sec. 6 gaps, RE)
s_a = 0.020 * math.sqrt(42)
# (b) CCHP sigma_SN = 0.70 km/s/Mpc at H0 = 70.39 with 24 SNe (D-24)
dm_b = mag_from_ratio(1 + 0.70 / 70.39)
s_b = dm_b * math.sqrt(24)
print(f"per-SN scatter (a) R22: {s_a:.3f} mag; (b) CCHP: {s_b:.3f} mag")
for s in (s_b, s_a):
    # disjoint subsets: CCHP 24 vs the 11 SH0ES-side hosts not in CCHP's 24 (D-27)
    sd = s * math.sqrt(1 / 24 + 1 / 11)
    dH = 70.4 * frac_from_mag(sd)
    print(f" s={s:.3f}: sigma(diff, 24 vs 11 disjoint) = {sd:.3f} mag = {dH:.2f} km/s/Mpc")
    obs = 74.1 - 70.39
    print(f"   observed 74.1 - 70.39 = {obs:.2f} km/s/Mpc -> {obs/dH:.2f} sigma")
    # subset of 11 drawn from a parent of 42 (JWST-only CCHP vs full SH0ES)
    sd2 = s * math.sqrt(1 / 11 - 1 / 42)
    dH2 = 70.4 * frac_from_mag(sd2)
    print(f"   sigma(11-of-42 subset vs parent) = {sd2:.3f} mag = {dH2:.2f} km/s/Mpc")
    # SH0ES HST Cepheid prediction for CCHP-selected subset 71.2 vs SH0ES-selected 73.6-73.9 (D-28)
    sel = 73.75 - 71.2
    print(f"   SH0ES-reported selection effect {sel:.2f} km/s/Mpc -> {sel/dH2:.2f} sigma of 11-of-42 subset noise")
# Decompose CCHP JWST-only 68.81 vs SH0ES 73.49:
tot = 73.49 - 68.81
sel = 73.75 - 71.2      # same-method (HST Cepheid) subset effect, D-28
meth = 71.2 - 68.81     # residual on the same subset: method/analysis/SN photometry
print(f"total SH0ES - CCHP-JWST = {tot:.2f}; selection part ~{sel:.2f}; residual method/analysis part ~{meth:.2f} km/s/Mpc")
print(f"  residual as mag: {mag_from_ratio(71.2/68.81):.3f} mag")
# Hoyt SN-photometry dependence (D-25): Pantheon+ +2.0 vs CSP-II +0.8 when extending to 24 SNe
print(f"  SN-compilation spread on extension (Hoyt): {2.0-0.8:.1f} km/s/Mpc = {mag_from_ratio((70+2.0)/(70+0.8)):.3f} mag")
# naive tensions
cchp_tot = total_error(1.22, 1.33, 0.70)
print(f"CCHP TRGB total error {cchp_tot:.2f}")
for name, x, e in [("CCHP TRGB 70.39", 70.39, cchp_tot), ("CCHP JWST-only 68.81", 68.81, 1.80)]:
    t1 = tension(73.49, 0.93, x, e)
    t2 = tension(x, e, 67.19, 0.38)
    print(f" {name}: vs SH0ES z={t1['z']:.2f}; vs CMB-SPA z={t2['z']:.2f}")

print()
print("=== Contradiction 2: inverse-ladder no-go (gap is in r_d / M_B) vs non-SN ladders at ~73 ===")
# Required r_d from DESI DR2 h*r_d = 101.54 +- 0.73 Mpc (D-45)
hrd, ehrd = 101.54, 0.73
for H in (67.19, 68.50, 70.39, 71.24, 73.26, 73.49):
    rd = hrd / (H / 100)
    print(f" H0={H:.2f}: r_d = {rd:.1f} +- {ehrd/(H/100):.1f} Mpc; vs CMB-SPA r_d 147.00 -> {100*(rd/147.0-1):+.1f}%")
# M_B gap ladder vs inverse ladder (D-21), and H0 equivalent
dMB = -19.253 - (-19.394)
print(f" M_B(ladder) - M_B(inverse, flat LCDM) = {dMB:+.3f} mag -> H0 ratio {10**(dMB/5):.4f}")
dMB2 = -19.253 - (-19.375)
print(f" M_B(ladder) - M_B(inverse, cosmography) = {dMB2:+.3f} mag -> H0 ratio {10**(dMB2/5):.4f}")
# Non-SN ladders (share primary-rung zero points; D-29, D-30)
sbf = total_error(0.7, 2.3); tf = total_error(2.1, 3.5)
print(f" SBF 73.8 +- {sbf:.2f}; TF 73.3 +- {tf:.2f}")
# Anchor-free one-step methods: TDCOSMO-2026 (D-31), masers Stiskalek 2026 (D-32, stat only), GWTC-5 (D-33)
# symmetrise: TDCOSMO (2.4+2.3)/2; sirens (9.4+7.5)/2
one = weighted_mean([71.1, 71.6, 71.7], [2.35, 3.7, 8.45])
print(f" one-step (lenses+masers+sirens) mean = {one['mean']:.2f} +- {one['error']:.2f}; chi2={one['chi2']:.2f}/{one['dof']}")
for name, x, e in [("CMB-SPA", 67.19, 0.38), ("DESI BAO+BBN", 68.50, 0.58), ("H0DN corrected", 73.264, 0.806),
                   ("SH0ES 2025", 73.49, 0.93)]:
    t = tension(one['mean'], one['error'], x, e)
    print(f"   one-step vs {name} {x}: diff={t['difference']:+.2f}, z={t['z']:.2f}")
# position of one-step mean between the two poles
pos = (one['mean'] - 67.19) / (73.264 - 67.19)
print(f" one-step mean sits {pos:.2f} of the way from CMB-SPA to H0DN")
# Precision needed for an anchor-free probe to separate 67.2 vs 73.3
gap = 73.264 - 67.19
for zt in (3, 5):
    p = precision_needed(gap, zt)
    print(f" precision to separate {gap:.2f} at {zt} sigma: {p:.2f} km/s/Mpc = {100*p/70:.2f}%")
# If truth is midpoint 70.2, precision to separate it from both poles at 3 sigma
mid = 0.5 * (73.264 + 67.19)
p3 = precision_needed(mid - 67.19, 3)
print(f" midpoint {mid:.2f}: precision to exclude both poles at 3 sigma: {p3:.2f} km/s/Mpc = {100*p3/70:.2f}%")

# Sound-horizon-free H0 (D-49; correlated DESI DR1 sets, so tested one at a time)
for name, x, e in [("Zaborowski lensxunWISE", 69.2, (1.3, 1.4)), ("Zaborowski DES 6x2pt", 70.3, (1.4, 1.2)),
                   ("Zaborowski lens+DESY5", 69.6, (1.3, 1.8)), ("2411.16677 DESY5", 66.7, (1.7, 1.9)),
                   ("2411.16677 Pantheon+", 67.9, (1.9, 2.1))]:
    t1 = tension(x, e, 73.264, 0.806)
    t2 = tension(x, e, 67.19, 0.38)
    print(f" r_d-free {name} {x}: vs H0DN z={t1['z']:.2f}; vs CMB-SPA z={t2['z']:.2f}")
# Shared-primary-rung systematic size needed (mag) for ladder -> CMB-SPA and -> DESI BAO+BBN
for target in (67.19, 68.50):
    print(f" ladder 73.264 -> {target}: needs {mag_from_ratio(73.264/target):.3f} mag common offset")

print()
print("=== Contradiction 3: EDE closed (Bayesian, full CMB) vs open (profile / DESI / eROSITA) ===")
lcdm_ref = 68.22  # P-ACT-LB LCDM (D-42), the same-data LCDM baseline used by ACT EDE fit (D-52 quotes 68.2)
ladder = 73.264
cases = [("ACT P-ACT-LB EDE", 69.9, (0.8, 1.5)), ("ACT P-ACT EDE", 69.3, (0.9, 1.5)),
         ("Poulin 2026 profile", 71.0, 1.1), ("eROSITA+ext", 71.4, 1.4), ("Reeves multiprobe (unchecked)", 70.5, 1.2),
         ("ACT mod. recomb.", 69.6, 1.0), ("ACT PMF", 69.1, 0.5), ("electron-density fluct. ACT+SPT", 69.3, 0.5)]
for name, x, e in cases:
    frac = (x - lcdm_ref) / (ladder - lcdm_ref)
    t = tension(x, e, ladder, 0.806)
    print(f" {name}: H0={x}; fraction of gap closed vs LCDM {lcdm_ref}: {frac:.2f}; residual vs H0DN z={t['z']:.2f}")
# Planck NPIPE 95% upper H0 69.5 -> 1-sigma-equivalent upper
print(f" NPIPE: 95% upper 69.5 is {(ladder-69.5)/0.806:.1f} H0DN-sigma below the ladder")
# f_EDE: profile 0.09 +- 0.03 vs Bayesian 95% upper limits 0.061 (NPIPE), 0.070 (SPA)
for ul in (0.061, 0.070, 0.088, 0.12):
    # profile best fit sits how many profile-sigma above each Bayesian upper limit
    print(f"  profile f=0.09+-0.03 vs Bayesian 95% UL {ul}: (0.09-UL)/0.03 = {(0.09-ul)/0.03:+.2f}")
