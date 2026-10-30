"""Falsifier C2-0 (magnitude): can ONE early-universe analysis systematic carry most of the H0 gap
in every early-type measurement class at once?

Units: H0 in km/s/Mpc; r_d in Mpc; omega_i = Omega_i h^2 dimensionless (astronomical units, not SI).
Inputs are the dossier values [D-41..D-48]; the background model is the run's own verified
flat-FRW toolkit (math/constraints/_bg.py, used and calibrated in M-CONSTRAINTS-04).
"""
import sys, math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from _bg import Model, bisect

def phi_up(z):  # one-sided upper tail
    return 0.5 * math.erfc(z / math.sqrt(2))

LOCAL = 73.264          # H0DN [D-22]
CMB_SPA = (67.19, 0.38) # [D-44]
MID = 0.5 * (CMB_SPA[0] + LOCAL)  # "dominant" boundary ~70.23
print(f"midpoint (dominance boundary) = {MID:.3f} km/s/Mpc; full gap = {LOCAL-CMB_SPA[0]:.3f}")

classes = {
    "Planck PR4": (67.64, 0.52),
    "ACT DR6": (66.51, 0.64),
    "SPT-3G D1": (66.66, 0.60),
    "CMB-SPA": CMB_SPA,
    "Planck TE only": (68.49, 0.76),
    "BAO+BBN (DESI DR2)": (68.50, 0.58),
    "inverse ladder (cosmography)": (67.19, 0.65),
    "inverse ladder (flat LCDM)": (67.67, 0.685),
}
print("\n1. Shift each early class needs (to midpoint / to full local value), in km/s/Mpc and own sigma")
for k, (h, s) in classes.items():
    print(f"  {k:30s} H0={h:6.2f}+-{s:4.2f}: to mid +{MID-h:5.2f} ({(MID-h)/s:5.2f} sig); to 73.264 +{LOCAL-h:5.2f} ({(LOCAL-h)/s:5.2f} sig)")

print("\n2. Published analysis-choice spreads (dossier D-41) vs the needed CMB shift")
spreads = {"Plik vs CamSpec-NPIPE in P-ACT": 67.86 - 67.62, "PR3 -> PR4 Planck": 67.64 - 67.36,
           "Planck PR4 vs Planck-in-SPT-TableI": 67.64 - 67.41}
need_min = MID - 67.64
for k, v in spreads.items():
    print(f"  {k:36s} {v:+.2f} km/s/Mpc; needed (PR4 to midpoint) {need_min:.2f} = x{need_min/abs(v):.1f}")

print("\n3. Cross-class reach: a CMB-anisotropy systematic leaves BAO+BBN untouched (no shared data), and vice versa")
bb = classes["BAO+BBN (DESI DR2)"]
z_bb_mid = (MID - bb[0]) / bb[1]
z_bb_full = (LOCAL - bb[0]) / bb[1]
print(f"  (a) CMB-only systematic: BAO+BBN must still be a low fluctuation of {z_bb_mid:.2f} sig (p1={phi_up(z_bb_mid):.2e}) at the midpoint,"
      f" {z_bb_full:.2f} sig (p1={phi_up(z_bb_full):.1e}) at 73.264")
z_cmb_mid = (MID - CMB_SPA[0]) / CMB_SPA[1]
print(f"  (b)/(c) BAO- or BBN-only systematic: CMB-SPA must be a low fluctuation of {z_cmb_mid:.2f} sig (p1={phi_up(z_cmb_mid):.1e}) at the midpoint")

print("\n4. Sign check of the (a) omega_c route on the BAO-side classes (calibrated as in M-CONSTRAINTS-04)")
wb = 0.02237
ref = Model(0.6736, wb, 0.1200).theta100()
wc_need = bisect(lambda w: Model(0.73264, wb, w).theta100() - ref, 0.06, 0.16, tol=1e-8)

def zdrag(wb, wm):  # Eisenstein & Hu 1998
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    return 1291 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)

def rd(h, wb, wc):
    m = Model(h, wb, wc)
    return m.rs(zdrag(wb, m.wm))

rd0 = rd(0.6736, wb, 0.1200)
rdA = rd(0.73264, wb, wc_need)
norm = 147.09 / rd0
print(f"  omega_c needed {wc_need:.5f}; r_d(Planck bf) = {rd0*norm:.2f} Mpc (normalised); r_d(true under (a)) = {rdA*norm:.2f} Mpc ({100*(rdA/rd0-1):+.2f}%)")
inv = 67.67 * rd0 / rdA
print(f"  inverse ladder H0 propto 1/r_d: 67.67 -> {inv:.2f} km/s/Mpc (moves AWAY from 73.26)")
mA = Model(0.73264, wb, wc_need)
print(f"  Omega_m implied = {mA.Om:.4f}; vs DESI 0.2975+-0.0086: {(0.2975-mA.Om)/0.0086:.1f} sig; vs SN 0.322+-0.012: {(0.322-mA.Om)/0.012:.1f} sig")
# DESI BAO+BBN under (a)'s true cosmology: h*r_d predicted vs measured 101.54+-0.73
hrd = 0.73264 * rdA * norm
print(f"  predicted h*r_d = {hrd:.2f} Mpc vs DESI 101.54+-0.73: {(hrd-101.54)/0.73:+.1f} sig")

print("\n5. theta_* route (omega_c fixed): Omega_m implied")
mT = Model(0.73264, wb, 0.1200)
print(f"  Omega_m = {mT.Om:.4f}; vs DESI {(0.2975-mT.Om)/0.0086:.1f} sig; vs SN {(0.322-mT.Om)/0.012:.1f} sig")

print("\n6. Route that keeps late-time shape Omega_m (DESI 0.2975) at h = 0.73264: CMB must be wrong in omega_m AND theta_*")
wm_need = 0.2975 * 0.73264 ** 2
wc_s = wm_need - wb - 0.06 / 93.14
mS = Model(0.73264, wb, wc_s)
t = mS.theta100() / ref * 1.0411
print(f"  omega_m needed {wm_need:.4f} -> omega_c {wc_s:.4f} (+{(wc_s-0.12)/0.0012:.1f} sig of 0.0012); 100theta_* predicted {t:.5f} vs 1.0411+-0.0003: {(t-1.0411)/0.0003:+.0f} sig")
for Om in (0.322,):
    wcx = Om * 0.73264 ** 2 - wb - 0.06 / 93.14
    tx = Model(0.73264, wb, wcx).theta100() / ref * 1.0411
    print(f"  with SN Omega_m {Om}: omega_c {wcx:.4f} (+{(wcx-0.12)/0.0012:.1f} sig); 100theta_* {tx:.5f} ({(tx-1.0411)/0.0003:+.0f} sig)")

print("\n7. (c) BBN route: omega_b x1.26 [M-MECHANIST-07] vs the CMB's own omega_b 0.02237+-0.00015 (independent, peak-height ratio)")
wb_need = 0.02218 * 1.26
print(f"  omega_b needed ~{wb_need:.4f}; vs CMB {(wb_need-0.02237)/0.00015:.0f} sig; D/H eta10 5.931+-0.051 -> omega_b needed ~ +26% = {0.26*5.931/0.051:.0f} sig of D/H")

print("\n8. Lensing-anomaly sign: experiments without Planck's A_L excess are LOWER")
w = [1/0.64**2, 1/0.60**2]
m = (66.51*w[0] + 66.66*w[1]) / sum(w); s = 1/math.sqrt(sum(w))
print(f"  ACT+SPT naive mean {m:.2f}+-{s:.2f} (published SPT+ACT 66.59+-0.46) vs Planck PR4 67.64+-0.52: diff {m-67.64:+.2f}")

print("\n9. Shared-input route (recombination/drag code common to CMB and BAO r_d): z_d shift needed for r_d -6.5% [M-MECHANIST-07]")
m0 = Model(0.6736, wb, 0.1200)
zd0 = zdrag(wb, m0.wm)
target = 0.935 * m0.rs(zd0)
f = bisect(lambda x: m0.rs(zd0 * x) - target, 1.0, 1.5, tol=1e-7)
print(f"  z_d {zd0:.1f} -> {zd0*f:.1f} (x{f:.4f}, Delta z = {zd0*(f-1):+.0f}); d ln r_d / d ln(1+z_d) ~ {math.log(0.935)/math.log((1+zd0*f)/(1+zd0)):.2f}")
