"""Statistician lens: honest significance of the published DR3 wide-binary gamma values.

All gamma = G_eff/G (dimensionless). Accelerations in m s^-2. Values from the dossier [D-xx].
Errors: (up, down) asymmetric where quoted; symmetrised as stated in each line.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import (sigma_to_p, p_to_sigma, sidak_global_p, tension, weighted_mean, grouped_chi2,
                         total_error, min_bayes_factor, prior_needed, posterior_probability,
                         exposure_to_reach, z_after_exposure, precision_needed)


def g_from_Gamma(G, sG):
    g = 10 ** (2 * G)
    return g, 2 * math.log(10) * g * sG


def hdr(t):
    print("\n=== " + t + " ===")


# ---------------------------------------------------------------- 1. local significance vs gamma = 1
hdr("1. Local significance of each gamma > 1 claim (down-side error faces gamma = 1)")
rows = [
    # name, gamma, down error used (stat only), down error total (stat+sys), dossier id
    ("Chae 2023 (top of variants 1.33-1.43), stat", 1.43, 0.06, None, "D-20"),
    ("Chae 2023 strict sample (1.37, err assumed same 0.06)", 1.37, 0.06, None, "D-20"),
    ("Chae 2024a pure binary", 1.49, 0.19, None, "D-21"),
    ("Chae 2024b new sample, stat only", 1.37, 0.09, None, "D-22"),
    ("Chae 2024b new sample, stat+sys", 1.37, 0.09, total_error(0.09, 0.09), "D-22"),
    ("Yoon,Tian&Chae 2025 g_N<=1e-10", 1.32, 0.11, None, "D-23"),
    ("Hernandez+2024 r2D>0.01pc", 1.5, 0.2, None, "D-24"),
    ("Chae 2025 Bayes3D MOND regime N=35", 1.48, 0.23, None, "D-25"),
    ("Chae 2025 Bayes3D MOND+transition N=111", 1.34, 0.08, None, "D-25"),
    ("Chae+2026 36 pairs, geometric deprojection", 1.60, 0.14, None, "D-26"),
    ("Saad&Ting same 36 pairs, independent a", 1.00, 0.19, None, "D-26"),
    ("Saad&Ting C3PO s>3000 au", 1.17, 0.23, None, "D-27"),
    ("Boufourou E2 deep bin (perspective-corrected)", 1.11, 0.07, None, "D-31"),
]
for name, g, ds, dt, did in rows:
    e = dt if dt else ds
    z = (g - 1) / e
    p2 = sigma_to_p(abs(z), two_sided=True)
    print(f"{name:55s} [{did}] gamma={g:.3f} -err={e:.3f} z={z:5.2f} p2={p2:.2e}")

# Chae 2024b in its native Gamma units: Gamma = 0.068 +- 0.015 stat +0.024 -0.015 sys
G, sst = 0.068, 0.015
sdn = total_error(0.015, 0.015)
print(f"Chae 2024b Gamma=0.068: z(stat)={G/sst:.2f}; z(stat+sys, down side)={G/sdn:.2f} (sigma_tot_down={sdn:.4f})")
# Chae 2024b Chae-2023a sample Gamma = 0.059 +- 0.009 (stat), no sys quoted here
g23a, e23a = g_from_Gamma(0.059, 0.009)
print(f"Chae 2024b on Chae-2023a sample: gamma={g23a:.3f} +- {e23a:.3f}, z(stat)={0.059/0.009:.2f}")
# Chae+2026 without two dominant systems
for lab, Gm, gup, gdn in [("<10^-9.1", 0.042, 0.027, 0.024), ("<10^-9.5", 0.057, 0.035, 0.031),
                          ("<10^-10.1", 0.085, 0.059, 0.045)]:
    print(f"Chae+2026 w/o 2 systems g_N{lab}: gamma={10**(2*Gm):.3f}, z={Gm/gdn:.2f}")

# ---------------------------------------------------------------- 2. look-elsewhere
hdr("2. Look-elsewhere: Chae-camp choice of sample x bin x estimator variant")
for zloc, label in [(5.8, "Chae 2024b quoted (stat)"), (3.21, "Chae 2024b stat+sys"),
                    (2.9, "Yoon+2025"), (4.29, "Chae+2026 geometric")]:
    pl = sigma_to_p(zloc, two_sided=True)
    for N in (5, 10, 30):
        pg = sidak_global_p(pl, N)
        print(f"{label:28s} z_loc={zloc:.2f} N_trials={N:3d} p_glob={pg:.2e} z_glob={p_to_sigma(pg, two_sided=True):.2f}")

# ---------------------------------------------------------------- 3. tensions
hdr("3. Pairwise tensions (two-sided; independent errors unless noted)")
pairs = [
    ("Chae2024b(stat+sys) vs Banik+24 (bins differ)", 1.37, (total_error(0.10, 0.16), total_error(0.09, 0.09)), 0.99, (0.03, 0.02)),
    ("Chae2024b(stat+sys) vs Boufourou E2 global", 1.37, (total_error(0.10, 0.16), total_error(0.09, 0.09)), 1.045, (0.023, 0.020)),
    ("Chae2024b(stat+sys) vs Boufourou E2 deep", 1.37, (total_error(0.10, 0.16), total_error(0.09, 0.09)), 1.11, (0.07, 0.07)),
    ("Chae2024b(stat only) vs Boufourou E2 deep", 1.37, (0.10, 0.09), 1.11, (0.07, 0.07)),
    ("Chae+2026 vs Saad&Ting (SAME 36 pairs)", 1.60, (0.24, 0.14), 1.00, (0.24, 0.19)),
    ("Boufourou E2 deep vs MOND 1.37", 1.11, (0.07, 0.07), 1.37, (0.0, 0.0)),
    ("Boufourou E2 deep vs Newton 1.00", 1.11, (0.07, 0.07), 1.00, (0.0, 0.0)),
    ("Banik+24 vs Boufourou E3 (global)", 0.99, (0.03, 0.02), 1.05, (0.02, 0.01)),
    ("C3PO s>3000au vs MOND 1.37", 1.17, (0.37, 0.23), 1.37, (0.0, 0.0)),
]
for name, a, ea, b, eb in pairs:
    t = tension(a, ea, b, eb)
    print(f"{name:50s} {t}")

# same-data tension with correlation (Chae 2024b median vs Boufourou E2 on overlapping catalogue)
hdr("3b. Same-data estimator difference, Chae2024b-type full median vs Boufourou E2, with correlation rho")
# Use stat errors only: 0.095 (Chae 2024b sym stat) and 0.0215 (E2). Different subsamples -> rho unknown.
for rho in (0.0, 0.5, 0.8):
    s1, s2 = 0.095, 0.0215
    var = s1 ** 2 + s2 ** 2 - 2 * rho * s1 * s2
    d = 1.37 - 1.045
    print(f"rho={rho}: diff={d:.3f}, sigma_diff={math.sqrt(var):.4f}, z={d/math.sqrt(var):.2f}")
# Boufourou's own implied full-median on the same catalogue: 1.12-1.20, vs Chae 1.37
print("Boufourou's implied full-median on Chae's catalogue 1.12-1.20 vs Chae 2024b 1.37: gap 0.17-0.25 unexplained by his triples bias")

# ---------------------------------------------------------------- 4. grouped chi2 by family
hdr("4. grouped_chi2 by estimator family (symmetric errors = mean of the two sides)")


def sym(up, dn):
    return 0.5 * (up + dn)


fam1 = ([1.37, 1.49, 1.32], [sym(total_error(0.10, 0.16), total_error(0.09, 0.09)), sym(0.21, 0.19), sym(0.12, 0.11)])
fam1_H = ([1.37, 1.49, 1.32, 1.5], fam1[1] + [0.2])
fam2 = ([1.045], [sym(0.023, 0.020)])
fam2_deep = ([1.11], [0.07])
fam3 = ([0.99], [sym(0.03, 0.02)])
fam4_chae = ([1.48, 1.60, 1.17], [sym(0.33, 0.23), sym(0.24, 0.14), sym(0.37, 0.23)])
fam4_st = ([1.48, 1.00, 1.17], [sym(0.33, 0.23), sym(0.24, 0.19), sym(0.37, 0.23)])
cases = {
    "A: F1(Chae x3) | F2 global | F3 Banik | F4 (Chae2025, Chae+26 geom, C3PO)": dict(F1=fam1, F2=fam2, F3=fam3, F4=fam4_chae),
    "B: as A but F4 uses Saad&Ting 1.00 for the 36 pairs": dict(F1=fam1, F2=fam2, F3=fam3, F4=fam4_st),
    "C: as A with Hernandez in F1 and F2 = deep bin 1.11": dict(F1=fam1_H, F2=fam2_deep, F3=fam3, F4=fam4_chae),
    "D: low-g bins only: F1 Chae x3 | F2 deep 1.11 | F4 geom": dict(F1=fam1, F2=fam2_deep, F4=fam4_chae),
}
for lab, g in cases.items():
    r = grouped_chi2(g)
    print(lab)
    for k, v in r["groups"].items():
        print(f"   {k}: mean={v['mean']:.3f}+-{v['error']:.3f} chi2={v['chi2']:.2f}/{v['dof']} p={v['p_consistent']:.3f}")
    print(f"   within chi2={r['within_chi2']:.2f}/{r['within_dof']} p={r['p_within']:.3f}; between chi2={r['between_chi2']:.1f}/{r['between_dof']} p={r['p_between']:.2e} z={r['between_z']:.2f}")
    pm = r["pooled"]
    print(f"   pooled mean={pm['mean']:.3f}+-{pm['error']:.3f} S={pm.get('scale_factor', float('nan'))}")

# ---------------------------------------------------------------- 4b. correlation among F1 (shared parent catalogue)
hdr("4b. F1 (Chae x3) combined with correlation rho among them (GLS, shared El-Badry parent)")


def gls(vals, errs, rho):
    n = len(vals)
    C = [[(errs[i] ** 2 if i == j else rho * errs[i] * errs[j]) for j in range(n)] for i in range(n)]
    # invert small matrix by Gauss-Jordan
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(C)]
    for i in range(n):
        p = A[i][i]
        A[i] = [x / p for x in A[i]]
        for k in range(n):
            if k != i:
                f = A[k][i]
                A[k] = [a - f * b for a, b in zip(A[k], A[i])]
    Ci = [row[n:] for row in A]
    w = [sum(Ci[i][j] for j in range(n)) for i in range(n)]
    W = sum(w)
    mu = sum(w[i] * vals[i] for i in range(n)) / W
    chi2 = sum((vals[i] - mu) * Ci[i][j] * (vals[j] - mu) for i in range(n) for j in range(n))
    return mu, math.sqrt(1 / W), chi2


for rho in (0.0, 0.5, 0.8):
    mu, e, c2 = gls(fam1[0], fam1[1], rho)
    t_b = tension(mu, e, 1.045, (0.023, 0.020))
    t_n = (mu - 1) / e
    print(f"rho={rho}: F1 mean={mu:.3f}+-{e:.3f} chi2_within={c2:.2f}/2  z vs Newton={t_n:.2f}  tension vs F2 global={t_b['z']:.2f}")

# ---------------------------------------------------------------- 5. Bayes-factor bounds and priors
hdr("5. Bayes-factor bounds (two-sided p) and prior needed for P(real) > 0.5")
for label, z in [("Chae 2024b stat+sys", 3.21), ("Chae 2024b stat", 4.53), ("F1 combined rho=0.8 (see 4b)", None),
                 ("Chae+2026 geom", 4.29), ("Chae+2026 w/o 2 systems <10^-9.5", 1.84),
                 ("Chae 2024b stat+sys after LEE N=10", None)]:
    if label.startswith("F1 combined"):
        mu, e, _ = gls(fam1[0], fam1[1], 0.8)
        z = (mu - 1) / e
    if label.endswith("N=10"):
        z = p_to_sigma(sidak_global_p(sigma_to_p(3.21, two_sided=True), 10), two_sided=True)
    p2 = sigma_to_p(z, two_sided=True)
    mb = min_bayes_factor(p2)
    bf_alt = mb["max_odds_against_null"]
    print(f"{label:40s} z={z:.2f} p2={p2:.2e} sellke B01>={mb['sellke']:.3e} max odds={bf_alt:.1f} "
          f"prior_needed={prior_needed(bf_alt):.4f}; post@prior0.1={posterior_probability(0.1, bf_alt):.3f} post@0.02={posterior_probability(0.02, bf_alt):.3f}")

# ---------------------------------------------------------------- 6. what data would settle it
hdr("6. Exposure / precision to settle")
# Delta between Newton (1.00) and MOND (1.37 Chae eq22 at 1e-10; BZ18 1.42) in scoring bin
for dlt in (0.33, 0.37, 0.42):
    print(f"delta={dlt}: precision_needed (5 sigma) = {precision_needed(dlt):.4f}")
# Full-median family: real effect delta=0.37, sigma_stat 0.095 (Chae 2024b), sigma_sys ~0.125 (sym) -> floor
for ssys in (0.125, 0.10, 0.06):
    k = exposure_to_reach(delta=0.37, sigma_stat=0.095, sigma_sys=ssys)
    print(f"F1: delta=0.37 sigma_stat=0.095 sigma_sys={ssys}: k to 5 sigma = {k}")
    print(f"    z ceiling = {0.37/ssys:.2f}; z at k=3 = {z_after_exposure(0.37, 0.095, ssys, 3):.2f}")
# Estimator-family discrepancy (F1 - F2 ~ 0.3): whether DR4 can resolve it is not a stat question
for ssys in (0.05, 0.10):
    k = exposure_to_reach(delta=0.30, sigma_stat=0.09, sigma_sys=ssys)
    print(f"F1-F2 gap 0.30 with sys {ssys}: k={k}")
# Family 4: 36 pairs, sigma ~0.2 -> pairs needed to resolve 0.37 at 5 sigma (stat only), ignoring model sys
k4 = exposure_to_reach(delta=0.37, sigma_stat=0.20, sigma_sys=0.0)
print(f"F4: N_needed ~ 36 * {k4:.1f} = {36*k4:.0f} pairs (stat only)")
k4s = exposure_to_reach(delta=0.37, sigma_stat=0.20, sigma_sys=0.30)
print(f"F4 with deprojection-model sys 0.30 (spread 1.00 vs 1.56): k={k4s}")
