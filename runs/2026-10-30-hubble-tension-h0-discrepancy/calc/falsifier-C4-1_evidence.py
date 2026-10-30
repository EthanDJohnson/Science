"""Falsifier C4-1 (evidence angle): confront C4's variants with measurements they must move.

Units: H0 in km/s/Mpc (astronomical units, not SI). Asymmetric errors are
handled by using the error on the side facing the comparison value.

(A) Variant (i), smooth H(z): leaves both the anchor ladder and the inverse
    ladder (BAO r_d + uncalibrated SNe; no late-time model assumed) unchanged,
    so their difference is a gap (i) cannot touch.
(B) Variant (ii), low-z M_B / G step between z = 0.01 and 0.023: predicts that
    SN-free, G-independent (or near-region) H0 probes read the true H0
    (CMB-SPA 67.19 +- 0.38, or BAO+BBN 68.50 +- 0.58).  Compare with:
      Kenworthy+2022 two-rung Cepheid ladder, hosts cz < 3300 km/s (near
        region, Cepheids unaffected under (ii)): 73.1 +2.6/-2.3
      Megamasers (Stiskalek 2026 reanalysis, stat only, prelim): 71.6 +- 3.7
        alternative: Pesce 2020 73.9 +- 3.0
      TDCOSMO-2026 time delays: 71.1 +2.4/-2.3
      GWTC-5 sirens: 71.7 +9.4/-7.5
      EDD TRGB two-rung (prelim; shares PV-field systematics with Kenworthy):
        72.3 +- 2.6 (evidence weighting)
(C) Variant (ii) needs Delta G/G0 ~ +0.11 at ~130-145 Myr lookback; quote the
    red-dwarf exclusion Delta chi^2 = 16.41 (Sakstein & Desmond 2026) as sigma.
"""
import math
from math import sqrt

def lo_hi(val, up, dn, ref):
    # error on the side facing ref
    return dn if ref < val else up

def comb(items, ref):
    w = 0.0; s = 0.0
    for name, v, up, dn in items:
        e = lo_hi(v, up, dn, ref)
        w += 1/e**2; s += v/e**2
    m = s/w; e = 1/sqrt(w)
    chi2 = sum(((v-ref)/lo_hi(v, up, dn, ref))**2 for name, v, up, dn in items)
    return m, e, chi2

def p_to_sigma(chi2, dof):
    # survival function of chi2 with integer dof via series; then two-sided Gaussian equivalent
    from math import exp, lgamma, log
    k = dof/2.0; x = chi2/2.0
    # regularized upper incomplete gamma Q(k,x) via series for P
    term = 1.0/k; ssum = term; n = 1
    while n < 500:
        term *= x/(k+n); ssum += term; n += 1
        if term < 1e-16*ssum: break
    P = exp(-x + k*log(x) - lgamma(k)) * ssum
    Q = 1 - P
    # Gaussian equivalent (two-sided) by bisection
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if math.erfc(mid/sqrt(2)) > Q: lo = mid
        else: hi = mid
    return Q, 0.5*(lo+hi)

print("=== (A) variant (i): ladder minus inverse ladder (both untouched by smooth H(z)) ===")
lad = [("H0DN corrected", 73.264, 0.806), ("SH0ES", 73.49, 0.93)]
inv = [("inverse ladder cosmography", 67.19, 0.66), ("inverse ladder flat LCDM", 67.67, 0.69)]
for ln, lv, le in lad:
    for iname, iv, ie in inv:
        d = lv-iv; e = sqrt(le**2+ie**2)
        print(f"  {ln} - {iname}: {d:.2f} +- {e:.2f} km/s/Mpc = {d/e:.2f} sigma")

print()
print("=== (B) variant (ii): SN-free / G-independent probes vs true H0 predicted by (ii) ===")
base = [("Kenworthy22 two-rung Cepheid", 73.1, 2.6, 2.3),
        ("masers Stiskalek26 (stat)", 71.6, 3.7, 3.7),
        ("TDCOSMO-2026", 71.1, 2.4, 2.3),
        ("GWTC-5 sirens", 71.7, 9.4, 7.5)]
alt_maser = [b if not b[0].startswith("masers") else ("masers Pesce20", 73.9, 3.0, 3.0) for b in base]
plus_trgb = base + [("EDD TRGB two-rung (prelim)", 72.3, 2.6, 2.6)]
no_td = [b for b in base if not b[0].startswith("TDCOSMO")]
sets = [("baseline 4 probes", base), ("Pesce20 masers", alt_maser),
        ("+ TRGB two-rung (correlated PV; upper bound)", plus_trgb),
        ("drop time delays (G-dependent kinematics caveat)", no_td)]
for ref_name, ref, ref_e in [("CMB-SPA", 67.19, 0.38), ("BAO+BBN", 68.50, 0.58)]:
    print(f" reference true H0 under (ii) = {ref_name} {ref} +- {ref_e}")
    for sname, items in sets:
        m, e, chi2 = comb(items, ref)
        d = m-ref; et = sqrt(e**2+ref_e**2)
        Q, zs = p_to_sigma(chi2, len(items))
        print(f"  {sname}: mean {m:.2f} +- {e:.2f}; offset {d:+.2f} +- {et:.2f} = {d/et:.2f} sigma; "
              f"chi2(vs ref, dof={len(items)}) = {chi2:.2f}, p = {Q:.3g} ({zs:.2f} sigma eq.)")
    for name, v, up, dn in base:
        e = lo_hi(v, up, dn, ref)
        print(f"   single {name}: {(v-ref)/sqrt(e**2+ref_e**2):.2f} sigma above {ref_name}")
    print()

print("=== same probes vs ladder value 73.264 (what a cause-on-the-early-side would predict) ===")
for sname, items in sets:
    m, e, chi2 = comb(items, 73.264)
    Q, zs = p_to_sigma(chi2, len(items))
    print(f"  {sname}: chi2 = {chi2:.2f} (dof {len(items)}), p = {Q:.3g}")

print()
print("=== (C) red-dwarf G-step exclusion (Sakstein & Desmond 2026, Delta chi2 at benchmark) ===")
for lab, dchi2 in [("OGSM dG/G0=+0.11 @130 Myr", 16.41), ("EGSM dG/G0=+0.04 @73 Myr", 9.52)]:
    Q, zs = p_to_sigma(dchi2, 1)
    print(f"  {lab}: Delta chi2 = {dchi2} -> p = {Q:.3g}, {sqrt(dchi2):.2f} sigma (1 dof)")
