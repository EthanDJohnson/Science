"""Falsifier C3-2 (bounds angle): does the TRUE global H0 that C3 needs (>= 70.2 km/s/Mpc,
the run's dominance midpoint) survive the independent constraints that do not use r_d?

Units: H0 in km/s/Mpc; ages in Gyr; distances in Mpc.  Astronomical units, not SI.
Inputs (dossier IDs):
  D-49 r_d-free BAO H0 (DESI DR1; correlated sets, so one value is used at a time)
  D-50 equality-scale H0 (BOSS DR12, pre-DESI)
  D-55 GC age t_U = 13.81 +- 0.25 (stat) +- 0.23 (sys) Gyr
  D-31 time delays 71.1 +2.4/-2.3; D-32 masers 71.6 +- 3.7; D-33 sirens 71.7 +9.4/-7.5
  D-52/D-53/D-94 EDE fits without SH0ES prior
  D-44 CMB-SPA 67.19 +- 0.38, Omega_m 0.3175; D-45 DESI Omega_m 0.2975; D-22 H0DN 73.264 +- 0.806
EDE changes only pre-recombination H(z), so t0 is the LCDM integral at the same (H0, Omega_m)
to < 0.1% (the z > 1000 era contributes < 1 Myr).
"""
import math
import numpy as np
from scipy import integrate, stats

MID = 70.2          # dominance midpoint (candidates.md boundary rule)
H_SPA = 67.19
H_LOC, S_LOC = 73.264, 0.806

def split_sigma(x, c, up, lo):
    """sigma to use for a point x relative to central value c of an asymmetric result"""
    return up if x > c else lo

def p_above(thr, c, up, lo):
    """P(H > thr) for a split-normal with central c, upper sigma up, lower sigma lo
    (two half-Gaussians; normalisation weights 2*s/(up+lo))."""
    wl = lo / (lo + up); wu = up / (lo + up)
    if thr >= c:
        return wu * 2 * stats.norm.sf((thr - c) / up)
    return wu + wl * 2 * (stats.norm.cdf((c - thr) / lo) - 0.5)

print("=== 1. Each r_d-free / non-ladder probe: sigma-distance of C3's true-H0 values ===")
probes = {
    "rdfree Zaborowski CMBlens x unWISE (D-49)": (69.2, 1.3, 1.4),
    "rdfree Zaborowski DES Y3 6x2pt (D-49)":     (70.3, 1.4, 1.2),
    "rdfree Zaborowski CMBlens+DESY5 (D-49)":    (69.6, 1.3, 1.8),
    "rdfree 2411.16677 DESY5 (D-49)":            (66.7, 1.7, 1.9),
    "rdfree 2411.16677 Pantheon+ (D-49)":        (67.9, 1.9, 2.1),
    "rdfree 2411.16677 Union3 (D-49)":           (67.8, 2.0, 2.2),
    "equality BOSS Pantheon prior (D-50)":       (65.1, 3.0, 5.4),
    "equality BOSS uncal-BAO Om (D-50)":         (65.6, 3.4, 5.5),
    "equality BOSS + BAO-lensing (D-50)":        (70.6, 3.7, 5.0),
    "time delays TDCOSMO-2026 (D-31)":           (71.1, 2.4, 2.3),
    "masers stat only (D-32)":                   (71.6, 3.7, 3.7),
    "sirens GWTC-5 (D-33)":                      (71.7, 9.4, 7.5),
}
for name, (c, up, lo) in probes.items():
    row = []
    for H in (MID, 71.0, 73.264):
        s = split_sigma(H, c, up, lo)
        row.append((H - c) / s)
    print(f"{name:45s} {c:6.2f}: (H-c)/sigma at 70.2 {row[0]:+5.2f}, 71.0 {row[1]:+5.2f}, 73.26 {row[2]:+5.2f};"
          f" P(H>70.2) = {p_above(MID, c, up, lo):.3f}")

print("\n=== 2. Inverse-variance combinations of r_d-free, non-ladder probes (symmetrised errors) ===")
def combo(names):
    vals = np.array([probes[n][0] for n in names])
    sig = np.array([(probes[n][1] + probes[n][2]) / 2 for n in names])
    w = 1 / sig**2
    m = np.sum(w * vals) / np.sum(w); s = 1 / math.sqrt(np.sum(w))
    chi2 = np.sum(w * (vals - m)**2)
    return m, s, chi2, len(names)

sets = {
    # one DESI-DR1 r_d-free value at a time (they are correlated), + independent equality (BOSS)
    "A: rdfree high (Zab 6x2pt) + equality BAO-lensing [most favourable to C3]":
        ["rdfree Zaborowski DES Y3 6x2pt (D-49)", "equality BOSS + BAO-lensing (D-50)"],
    "B: rdfree mid (Zab unWISE) + equality uncal-BAO":
        ["rdfree Zaborowski CMBlens x unWISE (D-49)", "equality BOSS uncal-BAO Om (D-50)"],
    "C: rdfree low (2411 Pantheon+) + equality Pantheon":
        ["rdfree 2411.16677 Pantheon+ (D-49)", "equality BOSS Pantheon prior (D-50)"],
    "D: A + one-step (TD, masers, sirens)":
        ["rdfree Zaborowski DES Y3 6x2pt (D-49)", "equality BOSS + BAO-lensing (D-50)",
         "time delays TDCOSMO-2026 (D-31)", "masers stat only (D-32)", "sirens GWTC-5 (D-33)"],
    "E: B + one-step":
        ["rdfree Zaborowski CMBlens x unWISE (D-49)", "equality BOSS uncal-BAO Om (D-50)",
         "time delays TDCOSMO-2026 (D-31)", "masers stat only (D-32)", "sirens GWTC-5 (D-33)"],
    "F: C + one-step":
        ["rdfree 2411.16677 Pantheon+ (D-49)", "equality BOSS Pantheon prior (D-50)",
         "time delays TDCOSMO-2026 (D-31)", "masers stat only (D-32)", "sirens GWTC-5 (D-33)"],
}
for k, names in sets.items():
    m, s, chi2, n = combo(names)
    print(f"{k}\n   mean {m:.2f} +- {s:.2f}; chi2 {chi2:.2f}/{n-1}; "
          f"midpoint 70.2 at {(MID-m)/s:+.2f} sigma, P(H>70.2) = {stats.norm.sf((MID-m)/s):.3f}; "
          f"71.0 at {(71.0-m)/s:+.2f}; 73.26 at {(73.264-m)/s:+.2f}; 67.19 at {(67.19-m)/s:+.2f}")

print("\n=== 3. GC age bound on the true H0 (EDE leaves t0(H0, Om) unchanged) ===")
OMR_H2 = 4.18e-5  # omega_r incl. 3.044 massless nu (approx, radiation negligible for t0)
GYR = 977.792     # 1/(km/s/Mpc) in Gyr
def t0(H0, Om):
    h = H0 / 100; Or = OMR_H2 / h**2; OL = 1 - Om - Or
    f = lambda a: 1 / (a * math.sqrt(Om / a**3 + Or / a**4 + OL))
    val, _ = integrate.quad(f, 0, 1, limit=200)  # t0 = int da/(a H0 E(a))
    return GYR / H0 * val
# check: EdS limit
_t = t0(67.19, 0.3175); print(f"check t0(67.19, 0.3175) = {_t:.3f} Gyr (D-44 quotes 13.805): {'PASS' if abs(_t-13.805)<0.05 else 'FAIL'}")
_e = t0(67.19, 0.99995); print(f"check EdS limit t0 = {_e:.3f} vs 2/(3H0) = {2*GYR/3/67.19:.3f}: {'PASS' if abs(_e-2*GYR/3/67.19)<0.02 else 'FAIL'}")
tU, sU = 13.81, math.hypot(0.25, 0.23)
for Om in (0.2975, 0.3175):
    for H in (MID, 71.0, 71.4, 73.264):
        t = t0(H, Om)
        print(f"  Om {Om}: H0 {H:6.2f} -> t0 {t:6.3f} Gyr, {(tU - t)/sU:+.2f} sigma below GC t_U")
    # H0 implied by the GC age (central) at this Om
    from scipy.optimize import brentq
    Hc = brentq(lambda H: t0(H, Om) - tU, 50, 90)
    Hlo = brentq(lambda H: t0(H, Om) - (tU + sU), 50, 90)
    Hhi = brentq(lambda H: t0(H, Om) - (tU - sU), 50, 90)
    print(f"  Om {Om}: age-implied H0 = {Hc:.2f} (+{Hhi-Hc:.2f}/-{Hc-Hlo:.2f})")

print("\n=== 4. EDE posteriors without a ladder prior: mass above the 70.2 midpoint ===")
fits = {
    "ACT P-ACT-LB EDE (D-52)": (69.9, 0.8, 1.5),
    "ACT P-ACT EDE (D-52)": (69.3, 0.9, 1.5),
    "ACT alone EDE (D-52)": (67.5, 0.9, 1.7),
    "Poulin 2026 profile (D-53)": (71.0, 1.1, 1.1),
    "eROSITA+ext (D-94)": (71.4, 1.4, 1.4),
    "Reeves 2026 multiprobe EDE (D-53, not source-checked)": (70.5, 1.2, 1.2),
    "ACT modified recombination (D-52)": (69.6, 1.0, 1.0),
    "ACT PMF (D-52)": (69.1, 0.5, 0.5),
    "e-density fluct. ACT+SPT WITH ladder prior (D-95)": (69.3, 0.5, 0.5),
}
for k, (c, up, lo) in fits.items():
    print(f"  {k:55s} {c:5.1f}: P(H>70.2) = {p_above(MID, c, up, lo):.3f}; "
          f"fraction of 67.19->73.264 gap = {(c-H_SPA)/(H_LOC-H_SPA):.2f}")
print("  Planck NPIPE EDE 95% upper H0 = 69.5 (D-53/D-75) < 70.2: P(H>70.2) < 0.025 by construction")

print("\n=== 5. Joint: Poulin profile (71.0+-1.1) vs r_d-free set B and C (independent data?) ===")
for k in ("B: rdfree mid (Zab unWISE) + equality uncal-BAO", "C: rdfree low (2411 Pantheon+) + equality Pantheon"):
    m, s, _, _ = combo(sets[k])
    d = (71.0 - m) / math.hypot(1.1, s)
    print(f"  {k}: 71.0 - {m:.2f} = {71.0-m:.2f} +- {math.hypot(1.1,s):.2f} -> {d:.2f} sigma")

print("\n=== 6. r_d-free + one-step sets combined with the GC-age-implied H0 (Om = 0.2975, DESI) ===")
age_H, age_s = 68.39, (1.73 + 1.64) / 2
for k in ("A: rdfree high (Zab 6x2pt) + equality BAO-lensing [most favourable to C3]",
          "D: A + one-step (TD, masers, sirens)", "E: B + one-step", "F: C + one-step"):
    m, s, _, _ = combo(sets[k])
    w1, w2 = 1 / s**2, 1 / age_s**2
    M = (w1 * m + w2 * age_H) / (w1 + w2); S = 1 / math.sqrt(w1 + w2)
    print(f"  {k[:2]} + age: {M:.2f} +- {S:.2f}; P(H>70.2) = {stats.norm.sf((MID-M)/S):.3f}; "
          f"73.26 at {(73.264-M)/S:+.2f} sigma; 71.0 at {(71.0-M)/S:+.2f}")
