"""Falsifier C1-2 (bounds angle).
Tests C1 ("ladder systematic, most likely at the SN Ia calibration step, biases
local H0 high by most of the gap; true global H0 ~67-68.5 km/s/Mpc") against the
independent constraints it must satisfy.
Units: H0 in km/s/Mpc; magnitudes in mag (5 log10 H0 convention).
Inputs are dossier values (D-22, D-23, D-29..D-33, D-49, D-50, D-44, D-45).
Asymmetric errors: the side facing the tested value is used.
"""
import math

def mag(h1, h2):
    return 5 * math.log10(h1 / h2)

def wmean(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(wi * v for wi, (v, _) in zip(w, vals)) / sum(w)
    return m, math.sqrt(1 / sum(w))

def side(v, up, lo, truth):
    return lo if truth < v else up

def chi2_at(data, truth):
    return sum(((v - truth) / side(v, up, lo, truth))**2 for v, up, lo in data)

def chi2_sf(x, k):
    # survival of chi2 with k dof (series for integer k)
    if k % 2 == 0:
        s, t = 0.0, 1.0
        for i in range(k // 2):
            if i > 0:
                t *= (x / 2) / i
            s += t
        return math.exp(-x / 2) * s
    # odd k: use erfc + series
    s = math.erfc(math.sqrt(x / 2))
    t = math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    for i in range(1, (k + 1) // 2):
        s += t
        t *= x / (2 * i + 1)
    return s

def p_to_z(p):
    # two-sided Gaussian equivalent by bisection
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

print("=== 1. Required SN-step bias for C1's stated true-H0 range ===")
H_ladder = 73.264  # H0DN corrected [D-22]
for Ht in (67.0, 67.19, 68.0, 68.5, 70.2):
    print(f"  true H0 {Ht:6.2f}: required ladder bias {mag(H_ladder, Ht):.3f} mag "
          f"({100*(H_ladder/Ht-1):.1f}% in H0)")

print("\n=== 2. Direct bound on the SN-step contribution: H0DN with vs without SNe Ia ===")
H_all, s_all = 73.264, 0.806   # D-22 (corrected Pantheon+)
H_all0, s_all0 = 73.50, 0.81   # D-22 baseline (same-version as D-23 variants)
H_noSN, s_noSN = 73.434, 1.795  # D-23 (original Pantheon+, matched to baseline 73.50)
for lab, Ha, sa in (("baseline 73.50 (same Pantheon+ version)", H_all0, s_all0),
                    ("corrected 73.264", H_all, s_all)):
    # nested-subset approximation: var(diff) = var(sub) - var(full)
    sd_nested = math.sqrt(s_noSN**2 - sa**2)
    sd_indep = math.sqrt(s_noSN**2 + sa**2)
    d = mag(Ha, H_noSN)  # SN-step contribution to the ladder magnitude offset
    sdm_n = 5 / math.log(10) * sd_nested / H_noSN
    sdm_i = 5 / math.log(10) * sd_indep / H_noSN
    print(f"  vs {lab}: SN-step contribution = {d:+.4f} mag; sigma {sdm_n:.4f} (nested) / {sdm_i:.4f} (indep.) mag")
    for need in (0.146, 0.188, 0.194):
        print(f"     needed {need:.3f} mag -> deficit {(need-d)/sdm_n:.2f} sigma (nested), {(need-d)/sdm_i:.2f} sigma (indep.)")
# In H0 terms: under SN-step-only C1, the no-SN ladder should read the true H0
for Ht in (67.0, 67.19, 68.0, 68.5, 70.2):
    print(f"  H0DN no-SNe 73.434 +- 1.795 vs true {Ht:5.2f}: {(H_noSN-Ht)/s_noSN:.2f} sigma")

print("\n=== 3. SN-free probe set under an SN-step-only bias (they should read true H0) ===")
# (value, up, lo)
setB = {"SBF (D-29)": (73.8, math.hypot(0.7, 2.3), math.hypot(0.7, 2.3)),
        "TF (D-30)": (73.3, math.hypot(2.1, 3.5), math.hypot(2.1, 3.5)),
        "TD TDCOSMO-2026 (D-31)": (71.1, 2.4, 2.3),
        "masers (D-32, stat only)": (71.6, 3.7, 3.7),
        "sirens GWTC-5 (D-33)": (71.7, 9.4, 7.5)}
setA = {"H0DN no-SNe (D-23; contains SBF+masers)": (73.434, 1.795, 1.795),
        "TF (D-30)": setB["TF (D-30)"],
        "TD TDCOSMO-2026 (D-31)": setB["TD TDCOSMO-2026 (D-31)"],
        "sirens GWTC-5 (D-33)": setB["sirens GWTC-5 (D-33)"]}
for name, S in (("Set B (SBF,TF,TD,masers,sirens)", setB), ("Set A (H0DN-noSN,TF,TD,sirens)", setA)):
    data = list(S.values())
    m, s = wmean([(v, (u + l) / 2) for v, u, l in data])
    print(f"  {name}: symmetrised mean {m:.2f} +- {s:.2f}")
    for Ht in (67.0, 67.19, 68.0, 68.5, 70.2):
        c2 = chi2_at(data, Ht)
        k = len(data)
        p = chi2_sf(c2, k)
        print(f"     true {Ht:5.2f}: (mean-true)/sigma = {(m-Ht)/s:.2f}; chi2 = {c2:.2f}/{k} dof, p = {p:.2e} ({p_to_z(p):.2f} sigma)")

print("\n=== 3b. Same, Cepheid-free and SN-free only (SBF, TD, masers, sirens; drop TF, which uses Cepheid zero points) ===")
data = [setB[k] for k in ("SBF (D-29)", "TD TDCOSMO-2026 (D-31)", "masers (D-32, stat only)", "sirens GWTC-5 (D-33)")]
m, s = wmean([(v, (u + l) / 2) for v, u, l in data])
print(f"  mean {m:.2f} +- {s:.2f}")
for Ht in (67.0, 67.19, 68.0, 68.5, 70.2):
    print(f"     true {Ht:5.2f}: {(m-Ht)/s:.2f} sigma")

print("\n=== 4. Anchor-free one-step probes (bound on ANY ladder systematic) ===")
data = [setB[k] for k in ("TD TDCOSMO-2026 (D-31)", "masers (D-32, stat only)", "sirens GWTC-5 (D-33)")]
m, s = wmean([(v, (u + l) / 2) for v, u, l in data])
print(f"  one-step mean {m:.2f} +- {s:.2f}")
for Ht in (67.0, 67.19, 68.0, 68.5, 70.2, 73.264):
    print(f"     vs {Ht:6.3f}: {(m-Ht)/s:+.2f} sigma")

print("\n=== 5. Anchor-free AND r_d-free arbiters for the 'true global H0' clause ===")
# one-step + one DESI-DR1 r_d-free value (correlated variants: use one at a time) + BOSS equality
rdfree_variants = {"Zaborowski CMBlens x unWISE 69.2": (69.2, 1.3, 1.4),
                   "Zaborowski DES 6x2pt 70.3": (70.3, 1.4, 1.2),
                   "Zaborowski CMBlens+DESY5 69.6": (69.6, 1.3, 1.8),
                   "2411.16677 DESY5 66.7": (66.7, 1.7, 1.9),
                   "2411.16677 Pantheon+ 67.9": (67.9, 1.9, 2.1)}
eq = (65.1, 3.0, 5.4)  # D-50, pre-DESI BOSS, independent of DESI DR1
for lab, rv in rdfree_variants.items():
    data = [setB["TD TDCOSMO-2026 (D-31)"], setB["masers (D-32, stat only)"],
            setB["sirens GWTC-5 (D-33)"], rv, eq]
    m, s = wmean([(v, (u + l) / 2) for v, u, l in data])
    out = ", ".join(f"{Ht}: {(m-Ht)/s:+.2f}" for Ht in (67.0, 68.5, 70.2, 73.264))
    print(f"  with {lab}: arbiter mean {m:.2f} +- {s:.2f}; sigma from [{out}]")
