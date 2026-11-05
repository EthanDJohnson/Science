"""(a) Heavy-tailed (Student-t, Bailey 2017 nu ~ 2-3) robustness of the local-vs-early split;
(b) calibrator-subsample variance for SH0ES vs CCHP; (c) residual tension after the best surviving
early-time model; local void cosmic variance; EDE delta-chi2 with parameter count;
(d) exposure / precision needed for deciding measurements. Units km/s/Mpc, mag."""
import sys, math
import numpy as np
from scipy import stats, optimize
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import (tension, total_error, sigma_to_p, p_to_sigma, exposure_to_reach, z_after_exposure,
                         precision_needed, _chi2_sf)

EARLY = (67.58, 0.32)   # CMB-SPA + BAO+BBN, this lens's grouped calc
SPA = (67.19, 0.38)
local = {"SH0ES": (73.49, 0.93), "CCHP": (70.39, 1.94), "SBF": (73.8, 2.40), "TF": (73.3, 4.08),
         "TD": (71.1, 2.35), "MAS": (71.6, 3.7), "GW": (71.7, 8.45)}

print("== (a) Student-t tails: P(|z| > z0) for a single pair ==")
for z0 in (4.55, 5.49, 6.27):
    print(f"  z0 = {z0}: Gaussian {sigma_to_p(z0, True):.2e}; t(nu=2) {2*stats.t.sf(z0, 2):.3f}; t(nu=3) {2*stats.t.sf(z0, 3):.4f}; t(nu=5) {2*stats.t.sf(z0, 5):.5f}")

def loglike_t(mu, names, nu, s_scale=1.0):
    return sum(stats.t.logpdf((local[n][0] - mu) / (local[n][1] * s_scale), nu) - math.log(local[n][1] * s_scale) for n in names)

print("\n== (a) Likelihood ratio: local values centred on early H0 (67.58, fixed) vs free local mean, t errors ==")
for names, lab in [(list(local), "all 7 local classes"), ([n for n in local if n != "SH0ES"], "6 local classes without SH0ES"),
                   (["SBF", "TF", "TD", "MAS", "GW"], "no-SN local (SBF, TF, TD, MAS, GW)"), (["TD", "MAS", "GW"], "one-step only")]:
    for nu in (2, 3, 1000):
        f = lambda m: -loglike_t(m, names, nu)
        r = optimize.minimize_scalar(f, bounds=(60, 80), method="bounded")
        lr = 2 * (f(EARLY[0]) - r.fun)   # 1 extra parameter; early error 0.32 neglected (small)
        z = math.sqrt(max(lr, 0))
        print(f"  {lab}, nu = {nu}: best local mu = {r.x:.2f}, -2 ln LR = {lr:.2f}, z ~ {z:.2f}")

print("\n== (b) Calibrator-subsample variance (sigma_SN per calibrator assumed 0.10-0.15 mag) ==")
for sig in (0.10, 0.13, 0.15):
    for nsub, nfull in ((24, 42), (11, 42), (11, 35)):
        s_mag = sig * math.sqrt(1 / nsub - 1 / nfull)       # subset mean vs full mean (nested samples)
        s_h0 = 73.0 * math.log(10) / 5 * s_mag
        print(f"  sigma_SN = {sig}: subset {nsub} of {nfull}: sigma(diff) = {s_mag:.3f} mag = {s_h0:.2f} km/s/Mpc; "
              f"2.5 km/s/Mpc offset = {2.5/s_h0:.1f} sigma")

print("\n== (c) Residual tension with SH0ES after best early-time fits (no SH0ES prior) ==")
for lab, v, e in [("Poulin 2026 EDE profile 71.0+-1.1 (D-53)", 71.0, 1.1), ("ACT P-ACT-LB EDE 69.9 +0.8/-1.5 (D-52)", 69.9, (0.8, 1.5)),
                  ("eROSITA+CMB EDE 71.4+-1.4 (D-94)", 71.4, 1.4), ("ACT PMF 69.1+-0.5 (D-52)", 69.1, 0.5),
                  ("ACT mod. recomb 69.6+-1.0 (D-52)", 69.6, 1.0), ("ACT+SPT e-density 69.3+-0.5 (D-95)", 69.3, 0.5)]:
    t = tension(73.49, 0.93, v, e)
    print(f"  {lab}: SH0ES - model = {t['difference']:.2f}, z = {t['z']:.2f}; gap closed vs CMB-SPA 67.19: {(v-67.19)/(73.49-67.19)*100:.0f}%")
print("  ACT EDE vs ACT LCDM baseline 68.2: closes", f"{(69.9-68.2)/(73.49-68.2)*100:.0f}% of SH0ES gap")
for dchi2, k, lab in [(4.3, 3, "EDE P-ACT"), (6.6, 3, "EDE P-ACT-LB"), (35.4, 3, "EDE with SH0ES (Poulin)")]:
    p = _chi2_sf(dchi2, k)
    print(f"  {lab}: dchi2 = {dchi2} for {k} extra params: p = {p:.3g}, z(2-sided) = {p_to_sigma(p, True):.2f}")
print("  DESI w0wa: largest of 3 SN samples (4.2 sigma) with Sidak N=3:",
      f"{p_to_sigma(1-(1-sigma_to_p(4.2, True))**3, True):.2f} sigma")

print("\n== (c) Local void within LCDM cosmic variance sigma = 0.31 (D-10, D-37) ==")
for gap in (73.49 - 67.19, 72.77 - 67.58, 70.39 - 67.19):
    print(f"  gap {gap:.2f}: {gap/0.31:.1f} sigma of cosmic variance")

print("\n== (d) Precision a deciding measurement needs (total 1-sigma on H0 or on a difference) ==")
for lab, d in [("ladder-systematic world (67.6) vs SH0ES-real (73.3)", 73.3 - 67.58),
               ("67.6 vs CCHP 70.4", 70.4 - 67.58), ("SH0ES 73.5 vs CCHP 70.4", 73.49 - 70.39),
               ("67.6 vs best EDE-like 71.0", 71.0 - 67.58), ("71.0 vs 73.3", 73.3 - 71.0)]:
    print(f"  {lab}: delta = {d:.2f}: 3 sigma needs {precision_needed(d,3):.2f} ({100*precision_needed(d,3)/70:.1f}%), "
          f"5 sigma needs {precision_needed(d,5):.2f} ({100*precision_needed(d,5)/70:.1f}%)")

print("\n== (d) Exposure to reach significance ==")
# TDCOSMO: 2.35 total on 11 lenses; MSD-dominated, split not published. Show pure-stat vs a 1.5% floor.
for lab, d in [("TD: 73.3 vs 67.58", 73.3 - 67.58), ("TD: 71.0 vs 67.58", 71.0 - 67.58)]:
    for floor in (0.0, 0.01 * 71.1, 0.015 * 71.1):
        for zt in (3, 5):
            k = exposure_to_reach(delta=d, sigma_stat=math.sqrt(max(2.35**2 - floor**2, 1e-9)), sigma_sys=floor, sigma_other=0.32, z_target=zt)
            print(f"  {lab}, sys floor {floor:.2f}: x{k:.1f} lenses ({k*11:.0f} lenses) for {zt} sigma" if math.isfinite(k) else
                  f"  {lab}, sys floor {floor:.2f}: never reaches {zt} sigma")
# SH0ES vs CCHP: delta 3.1; stat = CCHP stat+sigSN and SH0ES (all treated as stat); sys = CCHP sys 1.33
for zt in (3, 5):
    k = exposure_to_reach(delta=3.10, sigma_stat=total_error(1.22, 0.70, 0.93), sigma_sys=1.33, z_target=zt)
    print(f"  SH0ES vs CCHP, CCHP sys 1.33 floor: {'never' if not math.isfinite(k) else f'x{k:.1f}'} for {zt} sigma; ceiling z = {3.10/1.33:.2f}")
    k2 = exposure_to_reach(delta=3.10, sigma_stat=total_error(1.22, 0.70, 0.93), sigma_sys=0.67, z_target=zt)
    print(f"     with CCHP sys halved (0.67): {'never' if not math.isfinite(k2) else f'x{k2:.1f}'} for {zt} sigma")
# Sirens: 71.7 +9.4/-7.5 from 236 events (dominated by GW170817 + dark sirens); bright-siren-only scaling ~ 15%/sqrt(N)
for zt in (3, 5):
    s_need = precision_needed(73.3 - 67.58, zt)
    n = (0.15 * 70 / s_need) ** 2
    print(f"  bright sirens at ~15% each: N = {n:.0f} for {zt} sigma between 67.6 and 73.3 (sigma needed {s_need:.2f})")
