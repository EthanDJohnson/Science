"""Crux C2: separations for the deciding tests (SI: lifetimes in s, rates in s^-1).

Inputs (all from candidates.md / dossier / verdicts):
  proton beam 887.97 +- 2.04 s; storage 878.32 +- 0.43 s (statistician)
  material class 880.03 +- 0.70 s (scaled); magnetic class 877.82 +- 0.27 s (M-STATISTICIAN-01)
  UCNProBe target 1-2 s (D-106, search-summary); LiNA ~1 s (D-102); BL2 < 1 s (D-100)
  C7 prediction for BL2: 880-886 s; C7 UCNProBe: ~storage 878-882 s (candidates.md)
"""
import math

tau_beam, s_beam = 887.97, 2.04
tau_stor, s_stor = 878.32, 0.43
tau_mat, s_mat = 880.03, 0.70
tau_mag, s_mag = 877.82, 0.27

print("== 1. UCNProBe same-trap test: C2 predicts tau_beta - tau_storage ~ +9.65 s; C1/C5/C6/C7(approx)/C8 predict ~0 ==")
gap = tau_beam - tau_stor
print(f"predicted gap under C2 = {gap:.2f} s")
for sig in (1.0, 1.5, 2.0):
    print(f"  UCNProBe sigma = {sig:.1f} s: prediction separation = {gap/sig:.1f} sigma")
for z in (3, 5):
    print(f"  sigma needed to separate predictions at {z} sigma: {gap/z:.2f} s")
# absolute beta-efficiency requirement: Gamma_beta = R_beta/(eps*N) -> dtau/tau = deps/eps
for sig in (1.0, 1.5, 2.0):
    print(f"  tau_beta to {sig:.1f} s needs absolute beta-efficiency x UCN-count normalisation to {100*sig/888:.3f} %")

print("== 2. C2 vs C3: apparatus dependence of the extra loss ==")
lam_mat = 1/tau_mat - 1/tau_beam
lam_mag = 1/tau_mag - 1/tau_beam
d = tau_mat - tau_mag
sd = math.hypot(s_mat, s_mag)
print(f"needed loss material = {lam_mat:.3e} s^-1, magnetic = {lam_mag:.3e} s^-1, ratio = {lam_mat/lam_mag:.2f}")
print(f"material - magnetic lifetime split = {d:.2f} +- {sd:.2f} s ({d/sd:.2f} sigma, scaled material error)")
print(f"C3 (bulk invisible decay) predicts identical tau_storage - tau_beta = {-gap:.2f} s in every trap;")
print(f"C2 (apparatus-dependent loss) predicts ~{tau_mat-tau_beam:.2f} s (material) vs ~{tau_mag-tau_beam:.2f} s (magnetic)")
for z in (2, 3):
    per = d / z / math.sqrt(2)
    print(f"  to see the {d:.2f} s trap dependence at {z} sigma, each in-trap beta-vs-storage gap needs sigma <= {per:.2f} s")

print("== 3. LiNA (electron beam): C2 predicts ~888 s; C5, C8, C1 predict ~878 s ==")
for sig in (1.0, 2.0):
    print(f"  LiNA sigma = {sig:.1f} s: separation of 888 vs 878 predictions = {gap/sig:.1f} sigma")

print("== 4. BL2 against C7: C2 888 s vs C7 880-886 s ==")
for c7 in (880.0, 883.0, 886.0):
    print(f"  BL2 sigma = 1.0 s: 888 vs {c7:.0f} s separation = {(tau_beam-c7)/1.0:.1f} sigma")

print("== 5. Symmetric lambda cost ==")
print("  A-route vs a-route split (M-STATISTICIAN-10): 3.49 sigma; C1 needs the a route wrong, C2 needs the A route wrong")
lamA, sA = 1.27641, math.hypot(0.00045, 0.00033)
lama, sa = 1.2668, 0.0027
print(f"  PERKEO III vs aSPECT 2024: {(lamA-lama)/math.hypot(sA, sa):.2f} sigma")
