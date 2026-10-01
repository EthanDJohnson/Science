"""Crux calc for C3 (invisible dark branch).

Units: lifetimes in s (SI); lambda, Br_X dimensionless.
Inputs (all from dossier / candidates / verdict logs):
  storage 878.32 +- 0.43 s, proton beam 887.97 +- 2.04 s  (candidates.md header, lens-statistician_combination)
  J-PARC 877.2, stat 1.7, sys +4.0/-3.6 -> upper error sqrt(1.7^2+4.0^2) = 4.35 s (D-23)
  tau_beta per lambda: PERKEO III 878.50 +- 0.88, UCNA 877.60 +- 2.36, PERKEO II 880.34 +- 1.63,
      aSPECT 2024 889.58 +- 3.20, aCORN 874.86 +- 7.07 s (U-01)
  lambda: PERKEO III 1.27641(56) [D-40], aSPECT 1.2668(27) [D-42]; C3 needs 1.26812(179) (verdict C3-1 log)
  K = dtau/d|lambda| = 1142.7 s (verdict C3-1 log)
  Nab goal dlambda/|lambda| = 0.04% (D-107); LiNA ~1 s (D-102); UCNProBe 1-2 s (D-106, search-summary);
  tauSPECT < 0.3 s (D-103); UCNtau 877.82 +0.30 s total (D-27: 0.22 stat, 0.20 sys)
"""
import math

def z(a, sa, b, sb):
    return (a - b) / math.sqrt(sa**2 + sb**2)

def wavg(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(v * wi for (v, _), wi in zip(vals, w)) / sum(w)
    s = 1 / math.sqrt(sum(w))
    chi2 = sum(((v - m) / sv)**2 for v, sv in vals)
    return m, s, chi2

ST, sST = 878.32, 0.43
PB, sPB = 887.97, 2.04
JP, sJP = 877.2, math.sqrt(1.7**2 + 4.0**2)
taub = {"PERKEO III": (878.50, 0.88), "UCNA": (877.60, 2.36), "PERKEO II": (880.34, 1.63),
        "aSPECT 2024": (889.58, 3.20), "aCORN": (874.86, 7.07)}

print("== 1. Symmetry of the lambda conflict ==")
lP, slP = 1.27641, 0.00056
lA, slA = 1.2668, 0.0027
print(f"PERKEO III vs aSPECT 2024: {abs(z(lP, slP, lA, slA)):.2f} sigma -> at least one side carries an unidentified error")
print(f"C1 world needs aSPECT off by {(lP-lA)/slA:.2f} of its own errors")
print(f"C3 world (aSPECT right) needs PERKEO III off by {(lP-lA)/slP:.1f} of its own errors")

print("\n== 2. Total chi2 on the same data set, each model with 2 free parameters ==")
# C1: tau_n free (fitted to storage, J-PARC, all tau_beta), proton beam offset free (beam contributes 0)
nonbeam = [(ST, sST), (JP, sJP)] + list(taub.values())
m1, s1, c1 = wavg(nonbeam)
print(f"C1: tau = {m1:.2f} +- {s1:.2f} s, chi2 = {c1:.2f} (8 data, 2 params, 6 dof); p = {math.exp(-c1/2)*sum((c1/2)**k/math.factorial(k) for k in range(3)):.2e}")
# C3: tau_n = storage (free, storage fits exactly), tau_beta free, fitted to beam, J-PARC, all tau_beta
tb = [(PB, sPB), (JP, sJP)] + list(taub.values())
m3, s3, c3 = wavg(tb)
p3 = math.exp(-c3/2)*sum((c3/2)**k/math.factorial(k) for k in range(3))
print(f"C3: tau_beta = {m3:.2f} +- {s3:.2f} s, chi2 = {c3:.2f} (6 dof); p = {p3:.2e}; Br_X = {100*(1-ST/m3):.3f} %")
print(f"Delta chi2 (C3 - C1) = {c3-c1:.2f}")
# Same, but treat lambda as a discrete route choice: drop the route each model declares wrong
m1b, _, c1b = wavg([(ST, sST), (JP, sJP)] + [taub[k] for k in ("PERKEO III", "UCNA", "PERKEO II")])
m3b, _, c3b = wavg([(PB, sPB), (JP, sJP), taub["aSPECT 2024"]])
print(f"route-choice form: C1 (A route, aSPECT dropped) chi2 = {c1b:.2f}/4 ; C3 (a route, A group dropped) chi2 = {c3b:.2f}/1")
print(f"   cost of dropping: C1 drops 1 experiment (aSPECT, {z(taub['aSPECT 2024'][0], 3.20, m1b, 0.0):.2f} sigma from its fit); C3 drops 3 (A group)")
mA, sA, cA = wavg([taub[k] for k in ("PERKEO III", "UCNA", "PERKEO II")])
print(f"   A group tau_beta = {mA:.2f} +- {sA:.2f} s (internal chi2 {cA:.2f}/2); vs C3 tau_beta {m3b:.2f}: {z(m3b, 0, mA, sA):.2f} sigma (point)")

print("\n== 3. Deciding tests ==")
# C3 prediction for tau_beta: proton beam alone, or beam + aSPECT
mC3, sC3, _ = wavg([(PB, sPB), taub["aSPECT 2024"]])
print(f"C3 tau_beta prediction: beam alone {PB} +- {sPB}; beam + aSPECT {mC3:.2f} +- {sC3:.2f} s")
for sL in (1.0, 0.5):
    print(f"LiNA sigma = {sL} s:")
    print(f"  reads C3 value 887.97 -> {z(PB, sL, ST, sST):.1f} sigma from storage pole (C1, C5, C8)")
    print(f"  reads 878.32 -> {z(PB, sPB, ST, sL):.1f} sigma from C3 (beam error), {z(mC3, sC3, ST, sL):.1f} sigma (beam+aSPECT)")
    print(f"  reads 878.32 with BL2 at 888 +- 1 s -> {z(888.0, 1.0, ST, sL):.1f} sigma from C3")
# UCNProBe: in-trap difference D = tau_beta_rate - tau_storage
for sU in (1.0, 1.5, 2.0):
    print(f"UCNProBe difference sigma = {sU} s:")
    print(f"  reads D = 9.65 -> {9.65/sU:.1f} sigma from D = 0 (C1, C5, C6, C8)")
    print(f"  reads D = 0 -> {9.65/math.sqrt(sU**2+2.08**2):.1f} sigma from C3 (gap error 2.08 s), {9.65/math.sqrt(sU**2+1.1**2):.1f} sigma with BL2 at 1 s")
    print(f"  vs C7 (D up to ~4 s): D = 9.65 reading is {(9.65-4.0)/sU:.1f} sigma above C7's upper edge")
# Nab
sN = 0.0004 * 1.2764
lC3, slC3 = 1.26812, 0.00179
print(f"Nab sigma_lambda = {sN:.5f}")
print(f"  Nab reads PERKEO-like 1.27641 -> {z(lP, sN, lC3, slC3):.2f} sigma from C3's need")
print(f"  Nab reads C3-like 1.26812 -> {z(lP, slP, lC3, sN):.1f} sigma from the A route (C1, C6)")
print(f"  Nab reads C3-like 1.26812 -> {z(lA, slA, lC3, sN):.2f} sigma from aSPECT (C2, C5, C8 need the same)")
# C2 vs C3: universality of the extra storage loss
g_grav, g_ucnt = 7.92e-6, 1.268e-5   # s^-1, C2's required losses (candidates.md, M-CONSTRAINTS-12)
d_tau = 878.0**2 * (g_ucnt - g_grav)
print(f"C2 required losses differ by {g_ucnt-g_grav:.2e} s^-1 between Gravitrap and UCNtau -> {d_tau:.2f} s in tau")
sdiff = math.sqrt(0.3**2 + 0.30**2)
print(f"tauSPECT (0.3 s) vs UCNtau (0.30 s): difference sigma = {sdiff:.2f} s; a {d_tau:.1f} s trap-specific split = {d_tau/sdiff:.1f} sigma; C3 predicts 0")
print(f"observed material - magnetic split 2.21 s (M-STATISTICIAN-09) is unexplained by C3 (predicts 0)")
