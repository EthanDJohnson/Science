"""Falsifier C2-2 (bounds): if an early-universe ANALYSIS systematic is the cause, the true universe is
flat LCDM with standard physics and H0 ~ 73.26. Test that world against the independent constraints it
must satisfy, none of which use the CMB likelihood, BAO reconstruction choices or BBN rates jointly:
  (1) late-time Omega_m from probes that do not use r_d or the CMB (SN Hubble-diagram shape, DES Y6 3x2pt,
      DESI BAO shape) -> the true omega_m = Omega_m h^2 and hence the CMB omega_m the CMB 'should' see;
  (2) the direction a CMB-side bias must take at fixed theta_* (omega_c low -> Omega_m low) versus (1);
  (3) the predicted 100 theta_* and h*r_d of the H0 = 73.26 LCDM world vs measured values;
  (4) the age of that world vs globular-cluster ages;
  (5) r_d-free and equality-scale H0 values (D-49, D-50) vs 73.26;
  (6) BBN omega_b (D/H) vs CMB omega_b (two independent methods) vs the x1.26 needed.
Units: H0 km/s/Mpc; distances Mpc; ages Gyr; omega_i = Omega_i h^2 dimensionless (astronomical units).
Background: the run's verified flat-FRW toolkit math/constraints/_bg.py (M-CONSTRAINTS-04).
"""
import sys, math
import numpy as np
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from _bg import Model, bisect, ONU

H_LOC = 73.264                     # H0DN [D-22]
TH_MEAS, TH_ERR = 1.0411, 0.0003   # Planck 100 theta_* [D-40]
HRD, HRD_ERR = 101.54, 0.73        # DESI DR2 h r_d (Mpc) [D-45]
OM_DESI, OM_DESI_ERR = 0.2975, 0.0086
WB_CMB = 0.02218                   # Planck-like omega_b (CMB)

def zdrag(wb, wm):  # Eisenstein & Hu 1998 drag-epoch fit
    b1 = 0.313 * wm ** -0.419 * (1 + 0.607 * wm ** 0.674)
    b2 = 0.238 * wm ** 0.223
    return 1291 * wm ** 0.251 / (1 + 0.659 * wm ** 0.828) * (1 + b1 * wb ** b2)

def model(h, Om, wb=WB_CMB):
    wc = Om * h * h - wb - ONU
    return Model(h, wb, wc)

def rd(m):
    return m.rs(zdrag(m.wb, m.wm))

# --- 0. validation against CMB-SPA [D-44]: h=0.6719, Om=0.3175 -> r_d 147.00 Mpc, age 13.805 Gyr
m0 = model(0.6719, 0.3175)
rd0_raw = rd(m0)
NORM = 147.00 / rd0_raw   # calibrate the EH98-z_d r_d to the Boltzmann-code value (same approach as M-MECHANIST-07)
print("0. Validation (CMB-SPA point h=0.6719, Om=0.3175):")
print(f"   100theta_* = {m0.theta100():.5f} (Planck 1.0411); r_d raw = {rd0_raw:.2f} Mpc (CMB-SPA 147.00) -> norm {NORM:.4f}")
print(f"   age = {m0.age():.3f} Gyr (CMB-SPA 13.805); omega_m = {m0.wm:.4f}")
TH_OFF = TH_MEAS - m0.theta100()   # calibrate theta_* fit offset at the CMB point
print(f"   theta_* fit offset applied = {TH_OFF:+.5f} (z_* fitting formula); convergence: theta(n=40000) = "
      f"{100*m0.rs(m0.zstar(), n=40000)/m0.DM(m0.zstar(), n=40000):.6f}")

def theta_cal(m):
    return m.theta100() + TH_OFF

h = H_LOC / 100
print("\n1. The C2 world: flat LCDM, h = 0.73264, omega_b = 0.02218, Omega_m from r_d-free late-time probes")
probes = {
    "DESI DR2 BAO shape [D-45]": (0.2975, 0.0086),
    "DES-SN5YR+DESI inverse ladder flat LCDM [D-48]": (0.322, 0.012),
    "DES Y6 3x2pt [D-54] (lower err)": (0.333, 0.028),
}
GC_AGE, GC_ERR = 13.81, math.hypot(0.25, 0.23)   # [D-55]
for k, (Om, s) in probes.items():
    m = model(h, Om)
    th = theta_cal(m)
    hr = h * rd(m) * NORM
    age = m.age()
    print(f"  {k}: Om={Om}")
    print(f"     omega_m = {m.wm:.4f} (CMB-SPA {m0.wm:.4f}: {100*(m.wm/m0.wm-1):+.1f}%)")
    print(f"     100theta_* = {th:.5f} vs 1.0411+-0.0003: {(th-TH_MEAS)/TH_ERR:+.1f} sigma ({100*(th/TH_MEAS-1):+.2f}%)")
    print(f"     h r_d = {hr:.2f} Mpc vs DESI 101.54+-0.73: {(hr-HRD)/HRD_ERR:+.1f} sigma (marginal)")
    print(f"     age = {age:.3f} Gyr vs GC 13.81+-{GC_ERR:.2f}: {(age-GC_AGE)/GC_ERR:+.2f} sigma")

print("\n2. Direction of a CMB-side bias at fixed theta_*: Omega_m along the CMB degeneracy at h = 0.73264")
def f(wc):
    return Model(h, WB_CMB, wc).theta100() + TH_OFF - TH_MEAS
wc_star = bisect(f, 0.05, 0.20)
mC = Model(h, WB_CMB, wc_star)
print(f"  omega_c needed = {wc_star:.5f} (CMB-SPA {m0.wc:.5f}: {100*(wc_star/m0.wc-1):+.1f}%); Omega_m = {mC.Om:.4f}")
for k, (Om, s) in probes.items():
    print(f"     vs {k}: {(mC.Om-Om)/s:+.1f} sigma")
print(f"  age of this world = {mC.age():.3f} Gyr ({(mC.age()-GC_AGE)/GC_ERR:+.2f} sigma vs GC)")
hr = h * rd(mC) * NORM
print(f"  its h r_d = {hr:.2f} Mpc vs DESI 101.54: {(hr-HRD)/HRD_ERR:+.1f} sigma")

print("\n3. Joint DESI-BAO (Om, h r_d; rho=-0.92) + SN Om + GC age chi2, standard r_d, omega_b = 0.02218, h free vs h=0.73264")
rho = -0.92
cov = np.array([[OM_DESI_ERR**2, rho*OM_DESI_ERR*HRD_ERR], [rho*OM_DESI_ERR*HRD_ERR, HRD_ERR**2]])
icov = np.linalg.inv(cov)
def chi2(hh, Om, with_age=True, with_sn=True):
    m = model(hh, Om)
    d = np.array([Om - OM_DESI, hh * rd(m) * NORM - HRD])
    c = float(d @ icov @ d)
    if with_sn:
        c += ((Om - 0.322) / 0.012) ** 2
    if with_age:
        c += ((m.age() - GC_AGE) / GC_ERR) ** 2
    return c
for label, kw in [("BAO only", dict(with_age=False, with_sn=False)), ("BAO+SN", dict(with_age=False)), ("BAO+SN+age", {})]:
    best = (1e9, None, None)
    for hh in np.arange(0.64, 0.76, 0.0025):
        for Om in np.arange(0.27, 0.37, 0.0025):
            c = chi2(hh, Om, **kw)
            if c < best[0]:
                best = (c, hh, Om)
    c73 = min(chi2(h, Om, **kw) for Om in np.arange(0.27, 0.37, 0.001))
    dchi = c73 - best[0]
    print(f"  {label:12s}: best h={best[1]:.4f}, Om={best[2]:.4f}, chi2_min={best[0]:.2f}; at h=0.73264 chi2={c73:.2f}; "
          f"dchi2={dchi:.2f} -> {math.sqrt(max(dchi,0)):.2f} sigma (1 dof)")

print("\n4. r_d-free / equality-scale H0 vs 73.264 (using the error on the side facing 73.26)")
rdfree = {"Zaborowski CMBlens x unWISE [D-49]": (69.2, 1.3), "Zaborowski DES Y3 6x2pt [D-49]": (70.3, 1.4),
          "Zaborowski lens+DESY5 [D-49]": (69.6, 1.3), "2411.16677 DESY5 [D-49]": (66.7, 1.7),
          "2411.16677 Pantheon+ [D-49]": (67.9, 1.9), "2411.16677 Union3 [D-49]": (67.8, 2.0),
          "Philcox Pantheon Om [D-50]": (65.1, 3.0), "Philcox uncal-BAO Om [D-50]": (65.6, 3.4),
          "Philcox BAO-lensing [D-50]": (70.6, 3.7)}
for k, (v, s) in rdfree.items():
    print(f"  {k:36s} {v:5.1f} +{s:.1f}: {(H_LOC-v)/s:.2f} sigma below 73.264")

print("\n5. omega_b: BBN D/H (Cooke 2018, eta10 = 5.931 +- 0.051 [D-46]) vs CMB, vs the x1.26 needed [M-MECHANIST-07]")
wb_bbn = 5.931 / 273.9; wb_bbn_err = 0.051 / 273.9
print(f"  omega_b(BBN) = {wb_bbn:.5f} +- {wb_bbn_err:.5f}; CMB 0.02218; needed 1.26x = {1.26*wb_bbn:.5f}"
      f" -> {(1.26*wb_bbn-wb_bbn)/wb_bbn_err:.0f} sigma (BBN), ratio vs CMB {1.26*wb_bbn/0.02218:.2f}")

print("\n6. Minimum 'dominant' version: true H0 at the midpoint 70.23 km/s/Mpc (C2 carries just over half the gap)")
hm = 0.70227
for k, (Om, s) in probes.items():
    m = model(hm, Om)
    th = theta_cal(m)
    print(f"  late Om={Om} ({k}): omega_m {100*(m.wm/m0.wm-1):+.1f}% vs CMB; 100theta_* {(th-TH_MEAS)/TH_ERR:+.0f} sigma "
          f"({100*(th/TH_MEAS-1):+.2f}%); age {m.age():.3f} Gyr ({(m.age()-GC_AGE)/GC_ERR:+.2f} sigma)")
wcm = bisect(lambda wc: Model(hm, WB_CMB, wc).theta100() + TH_OFF - TH_MEAS, 0.05, 0.20)
mM = Model(hm, WB_CMB, wcm)
print(f"  theta_*-preserving CMB route: omega_c {100*(wcm/m0.wc-1):+.1f}%, Omega_m = {mM.Om:.4f}; "
      + "; ".join(f"{(mM.Om-Om)/s:+.1f} sig vs {k.split(' [')[0]}" for k, (Om, s) in probes.items()))
cm = min(chi2(hm, Om, with_age=False, with_sn=False) for Om in np.arange(0.27, 0.37, 0.001))
print(f"  DESI BAO + standard r_d (omega_b fixed) at h=0.70227: chi2 = {cm:.2f} -> {math.sqrt(cm):.2f} sigma; "
      f"published DESI+BBN 68.50+-0.58 -> {(70.227-68.50)/0.58:.2f} sigma")
