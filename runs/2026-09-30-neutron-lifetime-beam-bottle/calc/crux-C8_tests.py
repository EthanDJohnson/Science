"""Crux C8: separations for the deciding tests.
Units: lifetimes in s; lambda, a dimensionless.
Inputs (dossier / candidates): PERKEO III lambda -1.27641(56) [D-40]; aSPECT 2024 a = -0.10402(82),
lambda -1.2668(27) [D-42]; aCORN 2024 lambda -1.2712(61) [verdict C8-1]; tau_beta(PERKEO III) = 878.50 s [U-01];
proton-class pole 887.97 +- 2.04 s, storage pole 878.32 +- 0.43 s [candidates.md reference gap];
Nab goal d lambda/|lambda| = 0.04 % [D-107]; LiNA ~1 s [D-102]; BL2 < 1 s [D-100]; UCNProBe 1-2 s [D-106].
"""
import math

def a_of(lam):
    return (1 - lam**2) / (1 + 3 * lam**2)

def dadlam(lam):
    return -8 * lam / (1 + 3 * lam**2) ** 2

lamP, slamP = -1.27641, 0.00056
aP = a_of(lamP)
saP = abs(dadlam(lamP)) * slamP
aS, saS = -0.10402, 0.00082
print(f"a(PERKEO III lambda) = {aP:.5f} +- {saP:.5f}")
print(f"required Delta a (aSPECT - PERKEO-predicted) = {aS - aP:+.5f}")

# Nab precision
slam_nab = 0.0004 * abs(lamP)
sa_nab = abs(dadlam(lamP)) * slam_nab
print(f"Nab: sigma_lambda = {slam_nab:.5f}, sigma_a = {sa_nab:.5f}")
d = aS - aP
print(f"Nab alone, pole-to-pole separation (fixed poles) = {abs(d)/sa_nab:.1f} sigma")
# PERKEO-like Nab reading vs aSPECT pole (R-strong prediction carries aSPECT's error)
z1 = abs(d) / math.hypot(saS, sa_nab)
print(f"PERKEO-like Nab reading vs aSPECT-pole (R-strong) = {z1:.2f} sigma")
# aSPECT-like Nab reading vs PERKEO pole (C1/C7 prediction)
z2 = abs(d) / math.hypot(saP, sa_nab)
print(f"aSPECT-like Nab reading vs PERKEO-pole (C1) = {z2:.1f} sigma")

# tau_beta for aCORN 2024
def tau_beta(lam, ref=878.50, lamref=-1.27641):
    return ref * (1 + 3 * lamref**2) / (1 + 3 * lam**2)
lamC, slamC = -1.2712, 0.0061
tC = tau_beta(lamC)
dtdl = tC * 6 * abs(lamC) / (1 + 3 * lamC**2)
print(f"tau_beta(aCORN 2024) = {tC:.2f} +- {dtdl*slamC:.2f} s")
print(f"check tau_beta(aSPECT 2024) = {tau_beta(-1.2668):.2f} s")

# lifetime poles
pP, spP = 887.97, 2.04
pS, spS = 878.32, 0.43
for name, sig in [("LiNA 1 s", 1.0), ("BL2 1 s", 1.0), ("UCNProBe 1.5 s", 1.5), ("BL3 0.3 s", 0.3)]:
    zs = abs(pP - pS) / math.hypot(spS, sig)  # reading at proton pole vs storage pole
    zp = abs(pP - pS) / math.hypot(spP, sig)  # reading at storage pole vs proton pole
    print(f"{name}: reading 888 vs storage pole = {zs:.1f} sigma; reading 878 vs proton pole = {zp:.1f} sigma")

# intermediate BL2 reading (C7) e.g. 883 +- 1
for r in (881.0, 883.0, 885.0):
    zS = (r - pS) / math.hypot(spS, 1.0)
    zP = (pP - r) / math.hypot(spP, 1.0)
    print(f"BL2 reading {r:.0f} +- 1 s: {zS:.1f} sigma above storage pole, {zP:.1f} sigma below proton pole")

# BL2 proton-side scan: if the 1.11 % deficit scales with a varied proton-side parameter by factor f
gap = 9.88
for f in (0.5, 2.0):
    shift = gap * abs(f - 1)
    print(f"scan changing a proportional proton-side loss by x{f}: shift {shift:.1f} s = {shift/math.hypot(1,1):.1f} sigma for two 1 s points")
