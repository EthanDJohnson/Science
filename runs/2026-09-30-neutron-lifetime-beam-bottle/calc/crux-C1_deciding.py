"""Crux C1: separations for the deciding tests against C2, C3, C5, C6, C7, C8.

Units: lifetimes in s (SI); lambda, a, branching fractions dimensionless.
Inputs (all from candidates.md / verdicts, verified math checks):
  storage pole 878.32 +- 0.43 s; proton-beam pole 887.97 +- 2.04 s; BL1 887.7 +- 2.25 s
  PERKEO III lambda = -1.27641(56) -> tau_beta 878.50 +- 0.88 s  (M-CONSTRAINTS-02)
  aSPECT 2024 lambda = -1.2668(27) -> tau_beta 889.58 +- 3.20 s  (D-42, M-CONSTRAINTS-02)
  Nab goal: d(lambda)/|lambda| = 0.04 %  (D-107)
"""
import math

S, sS = 878.32, 0.43
B, sB = 887.97, 2.04
BL1, sBL1 = 887.7, 2.25
gap = B - S
print(f"gap proton pole - storage pole = {gap:.2f} s")

# --- C2 / C3: UCNProBe differential (beta-rate lifetime minus storage lifetime, same trap)
print("\nUCNProBe: C1 predicts difference 0 s; C2 and C3 predict ~ +gap")
for sd in (1.0, 1.5, 2.0):
    print(f"  sigma_diff = {sd:.1f} s: separation = {gap/sd:.1f} sigma")

# --- C3 (and C2): LiNA absolute electron-counting lifetime at ~1 s
sL = 1.0
z_888_vs_S = gap / math.hypot(sL, sS)
z_878_vs_B = gap / math.hypot(sL, sB)
z_878_vs_BL1 = (BL1 - S) / math.hypot(sL, sBL1)
print(f"\nLiNA at {sL} s: reading 888 vs storage pole = {z_888_vs_S:.2f} sigma;"
      f" reading 878 vs proton pole = {z_878_vs_B:.2f} sigma (vs BL1 {z_878_vs_BL1:.2f} sigma)")

# --- Nab: a coefficient and tau_beta
def a_of(l):
    return (1 - l * l) / (1 + 3 * l * l)

def dadl(l):
    # d/dl of (1-l^2)/(1+3l^2) = -8 l / (1+3l^2)^2
    return -8 * l / (1 + 3 * l * l) ** 2

lP, slP = -1.27641, 0.00056
lA, slA = -1.2668, 0.0027
slN = 0.0004 * abs(lP)
print(f"\nNab sigma_lambda (0.04 %) = {slN:.5f}")
print(f"a(PERKEO III lambda) = {a_of(lP):.5f}; a(aSPECT lambda) = {a_of(lA):.5f}")
print(f"Nab sigma_a = {abs(dadl(lP))*slN:.5f}")
dl = abs(lP - lA)
print(f"aSPECT-like Nab vs A route: {dl/math.hypot(slN, slP):.1f} sigma")
print(f"PERKEO-like Nab vs aSPECT: {dl/math.hypot(slN, slA):.2f} sigma")

tauP, stauP = 878.50, 0.88
def tau_beta(l):
    return tauP * (1 + 3 * lP * lP) / (1 + 3 * l * l)
dtau_dl = tauP * 6 * abs(lP) / (1 + 3 * lP * lP)
s_lam_part = dtau_dl * slP
s_vud_part = math.sqrt(stauP ** 2 - s_lam_part ** 2)
print(f"dtau/dlambda = {dtau_dl:.0f} s; lambda part of 0.88 s = {s_lam_part:.2f} s;"
      f" non-lambda (Vud, RC) part = {s_vud_part:.2f} s")
tA = tau_beta(lA)
s_nab = math.hypot(s_vud_part, dtau_dl * slN)
print(f"tau_beta at aSPECT lambda = {tA:.2f} s; with Nab precision +- {s_nab:.2f} s")
print(f"  aSPECT-like Nab tau_beta vs storage pole: {(tA - S)/math.hypot(s_nab, sS):.1f} sigma")
tP = tau_beta(lP)
print(f"  PERKEO-like Nab tau_beta = {tP:.2f} +- {s_nab:.2f} s vs proton pole: "
      f"{(B - tP)/math.hypot(s_nab, sB):.1f} sigma; vs storage: {(tP - S)/math.hypot(s_nab, sS):.2f} sigma")

# --- C7: BL2 (1 s) / BL3 (0.3 s) intermediate readings
print("\nBL2/BL3 readings vs storage pole (C1) - C7 predicts 880-886 s:")
for sb in (1.0, 0.3):
    for r in (880.0, 883.0, 886.0):
        print(f"  sigma {sb} s, reading {r}: {(r - S)/math.hypot(sb, sS):.1f} sigma from storage pole")
    print(f"  sigma {sb} s, reading 878.32: {(880.0 - S)/math.hypot(sb, sS):.1f} sigma below C7's lower edge 880 s")
