"""Crux C3: arithmetic for the response to verdicts C3-0/1/2 and the deciding-test precisions.

Units: H0 in km/s/Mpc (astronomical), r_d in Mpc, f_EDE dimensionless.
Inputs (dossier / verdicts):
  CMB-SPA LCDM 67.19 +- 0.38 [D-44], r_d 147.00 Mpc [D-44]; H0DN 73.264 +- 0.806 [D-22]
  DESI DR2 h*r_d = 101.54 +- 0.73 Mpc [D-45]
  EDE fits without ladder prior: ACT P-ACT-LB 69.9 [D-52], Khalife CMB-SPA 68.03, CMB-SPA+DESI 69.81 (verdict C3-1),
  Poulin 71.0 +- 1.1 [D-53], eROSITA 71.4 +- 1.4 [D-94]
  TDCOSMO-2026 71.1 +2.4/-2.3 with 11 lenses [D-31]
  f_EDE dominance threshold 0.065-0.072 (verdict C3-0 calc)
"""
import math

def Phi(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))

early, late = 67.19, 73.264
gap = late - early
mid = 0.5 * (early + late)
print(f"gap = {gap:.3f} km/s/Mpc, midpoint = {mid:.3f}, half-gap = {gap/2:.3f}")

# 1. The two dominance conditions in C3 are one condition:
#    early shift s = H_true - early, ladder residual r = late - H_true; s > r <=> H_true > mid.
print("\n[1] early shift vs ladder residual at each fit (s > r iff H > midpoint):")
fits = [("Khalife CMB-SPA EDE", 68.03), ("CMB-SPA+DESI EDE", 69.81), ("ACT P-ACT-LB EDE", 69.9),
        ("Poulin profile", 71.0), ("eROSITA+ext", 71.4)]
for name, h in fits:
    s, r = h - early, late - h
    print(f"  {name:22s} H0={h:6.2f}: shift={s:5.2f} residual={r:5.2f} share={s/gap*100:5.1f}%  s>r: {s > r}  (H>mid: {h > mid})")
    assert (s > r) == (h > mid)

# 2. Required r_d at H_true for the two h*r_d calibrations
hrd_cmb = 0.6719 * 147.00
hrd_desi = 101.54
print(f"\n[2] h*r_d CMB-SPA = {hrd_cmb:.2f} Mpc, DESI DR2 = {hrd_desi:.2f} Mpc; ratio DESI/CMB = {hrd_desi/hrd_cmb:.4f} ({(hrd_desi/hrd_cmb-1)*100:.2f}%)")
for h in (mid, 71.0, late):
    rc, rd = hrd_cmb / (h / 100), hrd_desi / (h / 100)
    print(f"  H0={h:6.2f}: r_d(CMB h r_d)={rc:6.1f} Mpc ({(rc/147.0-1)*100:+.2f}%), r_d(DESI h r_d)={rd:6.1f} Mpc ({(rd/147.0-1)*100:+.2f}%)")

# 3. Deciding-test precisions (one-sided separation of two predicted central values)
def sig_needed(a, b, nsig):
    return abs(a - b) / nsig

print("\n[3] precision needed for a true-H0 (anchor-free, r_d-free) measurement:")
c3 = 71.0  # C3 narrowed central (Poulin profile); C3 window 70.2-71.4
pairs = [("C1 upper edge 68.5", 68.5), ("C1 central 67.75", 67.75), ("C4(ii) 67.5", 67.5),
         ("boundary 70.23 (C6)", mid), ("C6 central 70.0", 70.0)]
for name, v in pairs:
    print(f"  C3 71.0 vs {name:20s}: diff={abs(c3-v):.2f}; sigma for 2/3/5 sigma = "
          f"{sig_needed(c3, v, 2):.2f} / {sig_needed(c3, v, 3):.2f} / {sig_needed(c3, v, 5):.2f} km/s/Mpc")
# lower edge of C3 window vs C1 upper edge
print(f"  C3 lower edge 70.23 vs C1 upper edge 68.5: 3 sigma needs {sig_needed(mid, 68.5, 3):.2f} km/s/Mpc")

# time-delay lens count, pure 1/sqrt(N) scaling, no systematic floor (optimistic)
sig_td = 0.5 * (2.4 + 2.3)
for target in (1.0, 0.83, 0.58, 0.39):
    n = 11 * (sig_td / target) ** 2
    print(f"  time delays: sigma {target:.2f} km/s/Mpc needs ~{n:.0f} lenses (from 11 at {sig_td:.2f}, no floor)")

print("\n[4] f_EDE precision needed (CMB without ladder prior):")
for f_c, f_t, n in ((0.09, 0.068, 2), (0.09, 0.068, 3), (0.07, 0.0, 3), (0.09, 0.0, 3), (0.09, 0.03, 3)):
    print(f"  separate f={f_c} from {f_t} at {n} sigma: sigma(f) <= {abs(f_c-f_t)/n:.4f}")

# 5. Where the C6/C3 boundary sits for an r_d-free combination like Zaborowski 69.73 +- 0.80..1.32 (verdict C3-0)
print("\n[5] P(H > midpoint) for r_d-free combination 69.73 at several sigma:")
for s in (1.32, 0.80, 0.5, 0.39):
    print(f"  sigma={s:.2f}: P(H>{mid:.2f}) = {1-Phi((mid-69.73)/s):.3f}; z(71.0) = {(71.0-69.73)/s:.2f}")
