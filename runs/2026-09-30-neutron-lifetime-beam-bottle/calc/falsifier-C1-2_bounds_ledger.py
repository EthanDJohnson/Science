"""Falsifier C1-2 (bounds angle): test C1 (storage ~878 s true; proton beam reads long)
against every independent constraint that does not itself count protons in a Penning trap
or store UCN. Units: SI (s); Yp dimensionless.

For each constraint x +/- s we compute the pull at the two poles:
  storage pole  tau_S = 878.32 s (statistician, all storage, S-scaled)
  beam pole     tau_B = 887.97 s (statistician, proton-counting beam)
and delta_chi2 = chi2(tau_S) - chi2(tau_B) (negative favours C1's pole).
Inputs are the run's verified numbers (M-CONSTRAINTS-02/-03/-04/-11, M-STATISTICIAN-11) plus
the BBN sensitivity quoted from Yeh et al. 2023 (arXiv:2303.04140): dtau = 5 s -> dYp = 0.0010
~ 0.3 sigma_obs(Yp).
"""
import math

tS, sS = 878.32, 0.43
tB, sB = 887.97, 2.04

def pulls(name, x, sp, sm=None, pole_err=True):
    sm = sp if sm is None else sm
    out = []
    for lab, t, st in (("S", tS, sS), ("B", tB, sB)):
        # side-facing asymmetric error: if pole above x use +err
        s = sp if t > x else sm
        s_tot = math.hypot(s, st) if pole_err else s
        out.append((lab, (x - t) / s_tot))
    zS, zB = out[0][1], out[1][1]
    d = zS**2 - zB**2
    print(f"{name:45s} x={x:8.2f}  z_S={zS:+6.2f}  z_B={zB:+6.2f}  dchi2(S-B)={d:+7.2f}")
    return d

print("== Independent constraints vs the two poles ==")
led = {}
led["SM tau_beta, A route (PERKEO III+UCNA+PERKEO II)"] = pulls("SM tau_beta, A route", 878.70, 0.83)
led["SM tau_beta, a route (aSPECT 2024 + aCORN)"] = pulls("SM tau_beta, a route", 887.21, 2.93)
led["SM tau_beta, PDG-2024 lambda (S=2.7)"] = pulls("SM tau_beta, PDG lambda", 879.68, 1.61)
led["J-PARC 2024 e-counting (as quoted)"] = pulls("J-PARC 2024 (as quoted)", 877.2, 4.35, 3.98)
# inflated by S = 2.29 on stat only: stat 1.7 -> 3.89
jp = lambda sys: math.hypot(1.7 * 2.29, sys)
led["J-PARC 2024 (stat x 2.29)"] = pulls("J-PARC 2024 (stat x2.29)", 877.2, jp(4.0), jp(3.6))
led["Lunar Prospector"] = pulls("Lunar Prospector (space)", 887.0, 14.0)
s_ill = math.hypot(3.0, 3.8)
led["Sussex-ILL (same method)"] = pulls("Sussex-ILL (same method, not independent)", 889.2, s_ill)

print("\n== BBN helium-4 (Yeh et al. 2023) ==")
dYp_per_s = 0.0010 / 5.0
sig_obs = 0.0010 / 0.3
dY = dYp_per_s * (tB - tS)
print(f"dYp/dtau = {dYp_per_s:.2e} per s; sigma_obs(Yp) ~ {sig_obs:.4f}")
print(f"Yp shift between the poles = {dY:.4f} = {dY/sig_obs:.2f} sigma_obs -> uninformative")

print("\n== Sums ==")
indep = ["SM tau_beta, A route (PERKEO III+UCNA+PERKEO II)", "SM tau_beta, a route (aSPECT 2024 + aCORN)",
         "J-PARC 2024 e-counting (as quoted)", "Lunar Prospector"]
tot = sum(led[k] for k in indep)
print(f"Sum dchi2 over A route + a route + J-PARC + space: {tot:+.2f} (negative favours C1)")
tot2 = sum(led[k] for k in ["SM tau_beta, PDG-2024 lambda (S=2.7)", "J-PARC 2024 (stat x 2.29)", "Lunar Prospector"])
print(f"Sum dchi2 with PDG lambda + inflated J-PARC + space: {tot2:+.2f}")
tot3 = sum(led[k] for k in ["SM tau_beta, a route (aSPECT 2024 + aCORN)", "J-PARC 2024 (stat x 2.29)", "Lunar Prospector"])
print(f"Worst case for C1 (a route only + inflated J-PARC + space): {tot3:+.2f}")

print("\n== The a-route cost C1 must pay ==")
# C1 requires the A route; the A- vs a-route tau_beta split
d = 887.21 - 878.70
s = math.hypot(0.83, 2.93)
print(f"A route vs a route tau_beta split: {d:.2f} s, {d/s:.2f} sigma (C1 must blame the a route)")
print(f"C1 storage pole vs a route: {(887.21-tS)/math.hypot(2.93,sS):.2f} sigma")
print(f"C1 storage pole vs aSPECT 2024 alone (889.58 +/- 3.20): {(889.58-tS)/math.hypot(3.20,sS):.2f} sigma")

print("\n== Unitarity (M-CONSTRAINTS-04 inputs) ==")
print("Exact first-row unitarity + A-route lambda + Vus 0.22431 -> tau_beta = 876.88 s")
print(f"  pull vs storage pole: {(876.88-tS):+.2f} s ; vs beam pole: {(876.88-tB):+.2f} s")
