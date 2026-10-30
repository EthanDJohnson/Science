"""Crux C4: residual-tension sizes and deciding-test precisions.

Units: astronomical. H0 in km/s/Mpc, magnitudes in mag. sigma = Gaussian-equivalent.
Inputs (all from dossier / verdicts / candidates):
  CMB-SPA 67.19 +- 0.38 [D-44]; BAO+BBN 68.50 +- 0.58 [D-45]; H0DN 73.264 +- 0.806 [D-22]
  Huang 2025 two-rung 73.4 +- 1.0 (abstract, quoted in verdict C4-1)
  Kenworthy 2022 two-rung 73.1 +2.6/-2.3 (abstract, quoted in verdict C4-1)
  Newman 2026 early-type-host TRGB-SN 75.3 +- 2.9 (candidates.md, C1 evidence against)
  SBF 73.8 +- 0.7 +- 2.3 [D-29]; one-step mean 71.27 +- 1.93 (M-STATISTICIAN-03)
  TDCOSMO 3.3% with 11 lenses [D-31]
  C3 best no-ladder-prior value 71.0 (Poulin 2026, D-53); C8 non-SH0ES mean 71.2-71.7
  C7 anchor-calibrated group 73.02 +- 0.78 (M-EXAMINER-06)
  Gap 0.188 mag (H0DN vs CMB-SPA); C4(ii) step 0.146-0.188 mag.
"""
import math

def z(a, sa, b, sb):
    return (a - b) / math.hypot(sa, sb)

SPA, sSPA = 67.19, 0.38
BB, sBB = 68.50, 0.58
GAP_MAG = 0.188

print("== Near-volume two-rung H0 vs C4(ii) prediction (true H0 = early value) ==")
for name, v, s in [("Huang2025 two-rung", 73.4, 1.0), ("Kenworthy2022 two-rung (lower err)", 73.1, 2.3)]:
    print(f"{name}: vs CMB-SPA {z(v,s,SPA,sSPA):.2f} sigma; vs BAO+BBN {z(v,s,BB,sBB):.2f} sigma")

print("== Newman 2026 early-type-host TRGB-SN ladder 75.3+-2.9 ==")
print(f"vs C1(a)-host-type prediction 67.19: {z(75.3,2.9,SPA,sSPA):.2f} sigma; vs 68.50: {z(75.3,2.9,BB,sBB):.2f} sigma")
print(f"vs C4(ii) prediction 73.264 (ladder value): {z(75.3,2.9,73.264,0.806):.2f} sigma")

print("== SBF 73.8 +- 2.4 (stat+sys in quadrature) vs C4(ii-SN) true H0 ==")
sSBF = math.hypot(0.7, 2.3)
print(f"sigma_SBF = {sSBF:.2f}; vs 67.19: {z(73.8,sSBF,SPA,sSPA):.2f} sigma; vs 68.50: {z(73.8,sSBF,BB,sBB):.2f} sigma")

print("== One-step mean 71.27 +- 1.93 vs C4 upper prediction 68.50 (no pole error) ==")
print(f"{(71.27-68.50)/1.93:.2f} sigma; vs 67.19: {(71.27-67.19)/1.93:.2f} sigma")

print("== 4% G-step (GSM) SN-only magnitude with L_SN ∝ G^1.46 ==")
dm = 2.5 * 1.46 * math.log10(1.04)
print(f"|dm| = {dm:.4f} mag = {100*dm/GAP_MAG:.1f}% of the 0.188 mag gap (SN part only; Cepheid part not computed)")

print("== Deciding-test precisions ==")
def need(diff):
    return diff / 3.0, diff / 5.0

def lenses(sig, h0=70.0):
    frac = 100 * sig / h0
    return 11 * (3.3 / frac) ** 2, frac

for label, a, b in [("vs C3: anchor-free one-step, C3 71.0 vs C4 68.50", 71.0, 68.50),
                    ("vs C3: C3 71.0 vs C4 67.19", 71.0, 67.19),
                    ("vs C8: non-SH0ES 71.2 vs C4 68.50", 71.2, 68.50),
                    ("vs C7: SN-free anchor ladder 73.02 vs C4 68.50", 73.02, 68.50)]:
    s3, s5 = need(a - b)
    n3, f3 = lenses(s3); n5, f5 = lenses(s5)
    print(f"{label}: diff {a-b:.2f}; sigma<= {s3:.2f} (3sig, {f3:.2f}%) / {s5:.2f} (5sig, {f5:.2f}%); "
          f"no-floor TD lens count ~{n3:.0f} / ~{n5:.0f}")

print("== M_B step test (vs C1, C6) ==")
for label, a, b in [("step 0.146 vs none (C1 e/f, or C1 a at fixed host type)", 0.146, 0.0),
                    ("step 0.146 vs C6 ceiling 0.094 (half gap)", 0.146, 0.094)]:
    s3, s5 = need(a - b)
    # ASSUMED per-SN total scatter 0.15 mag (SN standardisation + distance), equal N near and far
    n3 = 2 * (0.15 / s3) ** 2; n5 = 2 * (0.15 / s5) ** 2
    print(f"{label}: sigma(dM)<= {s3:.3f} mag (3sig) / {s5:.3f} mag (5sig); "
          f"N per side at ASSUMED 0.15 mag/SN: {n3:.0f} / {n5:.0f}")
print(f"half-gap ceiling = {GAP_MAG/2:.3f} mag")
