"""Pairwise H0 tensions (two-sided, asymmetric errors on the facing side), local-choice dependence,
look-elsewhere over analysis choices, Bayes-factor bounds. Units: km/s/Mpc throughout; M_B in mag.
Values from dossier.md (D-IDs in comments)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import tension, total_error, sigma_to_p, p_to_sigma, sidak_global_p, min_bayes_factor, prior_needed

# ---- local (one value per dataset; superseded values excluded)
local = {
    "SH0ES Ceph-SN 2025 (D-20)": (73.49, 0.93),
    "SH0ES Ceph+TRGB 2025 (D-20, same data)": (73.18, 0.88),
    "H0DN corrected (D-22)": (73.264, 0.806),
    "H0DN no-Cepheid (D-23, orig. Pantheon+)": (72.509, 1.296),
    "CCHP TRGB 2025 (D-24), stat+sys+sigSN": (70.39, total_error(1.22, 1.33, 0.70)),
    "CCHP JWST-only TRGB (D-25)": (68.81, total_error(1.79, 1.32)),
    "CCHP JWST JAGB (D-26)": (67.80, total_error(2.17, 1.64)),
    "SH0ES-side JAGB 2.0 (D-26)": (73.3, total_error(1.4, 2.0)),
    "SBF Jensen 2025 (D-29)": (73.8, total_error(0.7, 2.3)),
    "Tully-Fisher CF4 (D-30)": (73.3, total_error(2.1, 3.5)),
    "TDCOSMO-2026 (D-31)": (71.1, (2.4, 2.3)),
    "Masers Stiskalek 2026 stat-only (D-32)": (71.6, 3.7),
    "Sirens GWTC-5 (D-33)": (71.7, (9.4, 7.5)),
    "Wojtak&Hjorth 2025 alt SN std (D-35, same data as SH0ES)": (70.59, 1.15),
    "R22 superseded, for check only (D-20)": (73.04, 1.04),
}
early = {
    "Planck PR4 (D-41)": (67.64, 0.52),
    "Planck PR3 (D-41, superseded)": (67.36, 0.54),
    "ACT DR6 alone (D-42)": (66.51, 0.64),
    "SPT-3G D1 alone (D-43)": (66.66, 0.60),
    "CMB-SPA (D-44)": (67.19, 0.38),
    "CMB SPT+ACT+Planck as quoted by H0DN (D-22/D-44)": (67.24, 0.35),
    "DESI DR2 BAO+BBN (D-45)": (68.50, 0.58),
    "DESI+CMB LCDM (D-45, joint)": (68.17, 0.28),
    "Inverse ladder cosmography (D-48)": (67.19, (0.66, 0.64)),
    "Inverse ladder flat LCDM (D-48)": (67.67, (0.69, 0.68)),
}

print("== Total errors used ==")
for k, (v, e) in local.items():
    print(f"  {k}: {v} +- {e}")

print("\n== Pairwise tensions local vs early (two-sided, uncorrelated) ==")
hdr = list(early.keys())
for lk, (lv, le) in local.items():
    row = []
    for ek in hdr:
        ev, ee = early[ek]
        t = tension(lv, le, ev, ee)
        row.append(f"{t['z']:.2f}")
    print(f"{lk}:")
    for ek, z in zip(hdr, row):
        print(f"     vs {ek}: z = {z}")

print("\n== Selected pairs with difference, sigma, p ==")
pairs = [("SH0ES Ceph-SN 2025 (D-20)", "Planck PR4 (D-41)"),
         ("SH0ES Ceph-SN 2025 (D-20)", "CMB-SPA (D-44)"),
         ("SH0ES Ceph-SN 2025 (D-20)", "DESI DR2 BAO+BBN (D-45)"),
         ("SH0ES Ceph-SN 2025 (D-20)", "DESI+CMB LCDM (D-45, joint)"),
         ("R22 superseded, for check only (D-20)", "Planck PR3 (D-41, superseded)"),
         ("H0DN corrected (D-22)", "CMB-SPA (D-44)"),
         ("H0DN corrected (D-22)", "CMB SPT+ACT+Planck as quoted by H0DN (D-22/D-44)"),
         ("H0DN corrected (D-22)", "DESI DR2 BAO+BBN (D-45)"),
         ("CCHP TRGB 2025 (D-24), stat+sys+sigSN", "Planck PR4 (D-41)"),
         ("CCHP TRGB 2025 (D-24), stat+sys+sigSN", "CMB-SPA (D-44)"),
         ("CCHP TRGB 2025 (D-24), stat+sys+sigSN", "DESI DR2 BAO+BBN (D-45)"),
         ("TDCOSMO-2026 (D-31)", "CMB-SPA (D-44)"),
         ("TDCOSMO-2026 (D-31)", "Planck PR4 (D-41)"),
         ("TDCOSMO-2026 (D-31)", "H0DN corrected (D-22)"),
         ("TDCOSMO-2026 (D-31)", "SH0ES Ceph-SN 2025 (D-20)"),
         ("CCHP TRGB 2025 (D-24), stat+sys+sigSN", "SH0ES Ceph-SN 2025 (D-20)"),
         ("CCHP JWST JAGB (D-26)", "SH0ES-side JAGB 2.0 (D-26)"),
         ("Wojtak&Hjorth 2025 alt SN std (D-35, same data as SH0ES)", "CMB-SPA (D-44)"),
         ]
allv = {**local, **early}
for a, b in pairs:
    t = tension(allv[a][0], allv[a][1], allv[b][0], allv[b][1])
    print(f"  {a}  vs  {b}: diff = {t['difference']:+.2f}, sigma = {t['sigma']:.2f}, z = {t['z']:.2f}, p2 = {t['p_two_sided']:.2e}")

# SH0ES vs CCHP with shared NGC 4258 anchor and overlapping SN calibrators: correlation scan
print("\n== SH0ES (73.49+-0.93) vs CCHP (70.39+-1.94) with correlation rho ==")
s1, s2 = 0.93, total_error(1.22, 1.33, 0.70)
for rho in (0.0, 0.3, 0.5, 0.8):
    sd = math.sqrt(s1**2 + s2**2 - 2 * rho * s1 * s2)
    z = (73.49 - 70.39) / sd
    print(f"  rho = {rho}: sigma_diff = {sd:.2f}, z = {z:.2f}")

# M_B framing (D-21): ladder R22 vs inverse ladder (different SN systems; caveat)
print("\n== M_B framing (D-21) ==")
for lab, v, e in [("cosmography", -19.375, (0.018, 0.017)), ("flat LCDM", -19.394, (0.017, 0.016))]:
    t = tension(-19.253, 0.027, v, e)
    print(f"  R22 M_B -19.253+-0.027 vs inverse ladder {lab} {v}: diff = {t['difference']:+.3f} mag, z = {t['z']:.2f}")
for (a, b) in [(73.49, 67.19), (73.264, 67.19), (70.39, 67.19), (73.49, 68.50)]:
    print(f"  5 log10({a}/{b}) = {5*math.log10(a/b):.3f} mag; fractional gap {100*(a/b-1):.2f}%")

# Look-elsewhere over the choice of (local headline, early headline)
print("\n== Look-elsewhere over choice of pair (Sidak; conservative because choices are highly correlated) ==")
for zloc, lab in [(tension(73.49, 0.93, 67.19, 0.38)["z"], "SH0ES vs CMB-SPA"),
                  (tension(73.264, 0.806, 68.50, 0.58)["z"], "H0DN vs BAO+BBN"),
                  (tension(72.509, 1.296, 67.19, 0.38)["z"], "H0DN-noCepheid vs CMB-SPA")]:
    p = sigma_to_p(zloc, two_sided=True)
    for n in (10, 30, 100):
        pg = sidak_global_p(p, n)
        print(f"  {lab}: z_local = {zloc:.2f} (p2 = {p:.2e}); N = {n}: p_global = {pg:.2e}, z_global = {p_to_sigma(pg, two_sided=True):.2f}")

# Bayes-factor bounds (common H0 = null) and prior needed
print("\n== Min Bayes factors (null = one common H0) ==")
for zloc, lab in [(6.30, "SH0ES vs CMB-SPA ~"), (3.9, "no-Cepheid local vs CMB ~"), (2.0, "one-step only vs CMB ~"), (1.5, "CCHP vs SH0ES ~")]:
    p = sigma_to_p(zloc, two_sided=True)
    mb = min_bayes_factor(p)
    bf_alt = 1 / mb["sellke"]
    print(f"  {lab} z = {zloc}: p2 = {p:.2e}, Sellke BF_null >= {mb['sellke']:.2e} (max odds vs null {mb['max_odds_against_null']:.3g}), "
          f"Gaussian bound {mb['gaussian']:.2e}; prior needed for P(real)=0.5: {prior_needed(bf_alt):.2e}")
