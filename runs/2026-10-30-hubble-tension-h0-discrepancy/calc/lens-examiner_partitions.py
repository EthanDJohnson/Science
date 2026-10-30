"""Examiner lens: test which partition of the H0 data the brief's premises imply.

Units: H0 in km/s/Mpc; magnitudes in mag; r_d in Mpc.
Inputs are dossier anchors (IDs in comments). Asymmetric errors are symmetrised as
the mean of the two sides (stated). Stat and sys are added in quadrature.
Measurements are treated as independent unless stated: this is an approximation
(shared NGC 4258 anchor, shared CMB r_d in BAO+BBN vs inverse ladder vs CMB). A
rough correlated variant for the NGC 4258 anchor is printed separately.
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import tension, weighted_mean, grouped_chi2, total_error, precision_needed  # noqa: E402


def sym(up, down):
    return 0.5 * (up + down)


# --- one representative per class (current values) ---
M = {
    # local, Cepheid-calibrated SN ladder
    "SH0ES_Ceph_SN": (73.49, 0.93),                                   # D-20
    # local, TRGB-calibrated SN ladder (CCHP headline)
    "CCHP_TRGB_SN": (70.39, total_error(1.22, 1.33, 0.70)),           # D-24
    # non-SN ladders
    "SBF": (73.8, total_error(0.7, 2.3)),                             # D-29
    "TullyFisher": (73.3, total_error(2.1, 3.5)),                     # D-30
    # one-step
    "TDCOSMO2026": (71.1, sym(2.4, 2.3)),                             # D-31
    "Masers": (71.6, 3.7),                                            # D-32 (stat only)
    "Sirens_GWTC5": (71.7, sym(9.4, 7.5)),                            # D-33
    # r_s-free early-ish / shape measurements
    "BAO_no_rd_Zab": (69.6, sym(1.3, 1.8)),                           # D-49 (CMB lensing + DES Y5 SNe variant)
    "Equality_Philcox": (65.6, sym(3.4, 5.5)),                        # D-50 (uncalibrated-BAO Omega_m)
    # r_s-calibrated
    "CMB_SPA": (67.19, 0.38),                                         # D-44
    "BAO_BBN_DESI": (68.50, 0.58),                                    # D-45 / D-08
    "InvLadder": (67.19, sym(0.66, 0.64)),                            # D-48 (r_d from CMB; correlated with CMB)
}

print("Inputs (km/s/Mpc, symmetrised 68% errors):")
for k, (v, e) in M.items():
    print(f"  {k:18s} {v:6.2f} +- {e:5.2f}")


def grp(names):
    return ([M[n][0] for n in names], [M[n][1] for n in names])


def report(title, groups):
    g = grouped_chi2({k: grp(v) for k, v in groups.items()})
    print(f"\n== {title} ==")
    for name, d in g["groups"].items():
        print(f"  group {name:22s} n={d['n']:2d} mean={d['mean']:6.2f} +- {d['error']:4.2f} "
              f"chi2_within={d['chi2']:6.2f}/{d['dof']} p={d['p_consistent']:.3g}")
    print(f"  between chi2={g['between_chi2']:.2f} dof={g['between_dof']} z={g['between_z']:.2f}; "
          f"within chi2={g['within_chi2']:.2f}/{g['within_dof']} p_within={g['p_within']:.3g}; "
          f"pooled chi2={g['pooled']['chi2']:.2f}/{g['pooled']['dof']}")
    return g


all_names = list(M)
early = ["CMB_SPA", "BAO_BBN_DESI", "InvLadder", "BAO_no_rd_Zab", "Equality_Philcox"]
late = [n for n in all_names if n not in early]
rs = ["CMB_SPA", "BAO_BBN_DESI", "InvLadder"]
no_rs = [n for n in all_names if n not in rs]
shoes = ["SH0ES_Ceph_SN"]
not_shoes = [n for n in all_names if n not in shoes]
ladders = ["SH0ES_Ceph_SN", "CCHP_TRGB_SN", "SBF", "TullyFisher"]
not_ladders = [n for n in all_names if n not in ladders]

print("\nPartition test: a good partition has a large between-group chi2 AND acceptable within-group chi2.")
report("P1 early (incl. r_s-free shape) vs late", {"early": early, "late": late})
report("P2 uses r_s vs does not use r_s", {"uses_rs": rs, "no_rs": no_rs})
report("P3 SH0ES Cepheid-SN vs everything else", {"SH0ES": shoes, "rest": not_shoes})
report("P4 NGC4258/LMC-anchored ladders vs everything else", {"ladders": ladders, "rest": not_ladders})
report("P5 three groups: r_s | ladders | one-step+r_s-free",
       {"uses_rs": rs, "ladders": ladders,
        "onestep_rsfree": ["TDCOSMO2026", "Masers", "Sirens_GWTC5", "BAO_no_rd_Zab", "Equality_Philcox"]})

pool = weighted_mean(*grp(all_names))
print(f"\n== Null test: one common H0, all 12 classes, quoted errors ==\n  pooled mean {pool['mean']:.2f} +- {pool['error']:.2f}; "
      f"chi2={pool['chi2']:.2f}/{pool['dof']}; p={pool['p_consistent']:.3g}; PDG scale factor S={pool['scale_factor']:.2f} "
      f"(uniform error inflation the null needs)")
print("\n== Pairwise tensions vs CMB-SPA 67.19 +- 0.38 (independent approx.) ==")
for k in ["SH0ES_Ceph_SN", "CCHP_TRGB_SN", "SBF", "TullyFisher", "TDCOSMO2026", "Masers", "Sirens_GWTC5",
          "BAO_no_rd_Zab", "Equality_Philcox", "BAO_BBN_DESI"]:
    t = tension(M[k][0], M[k][1], 67.19, 0.38)
    print(f"  {k:18s} diff={t['difference']:+6.2f} sigma={t['sigma']:4.2f} z={t['z']:.2f}")

print("\n== Local combinations without SH0ES Cepheids (independent approx.) ==")
for title, names in [
    ("non-Cepheid local (CCHP,SBF,TF,TD,masers,sirens)",
     ["CCHP_TRGB_SN", "SBF", "TullyFisher", "TDCOSMO2026", "Masers", "Sirens_GWTC5"]),
    ("one-step only (TD, masers, sirens)", ["TDCOSMO2026", "Masers", "Sirens_GWTC5"]),
    ("no SN at all (SBF,TF,TD,masers,sirens)", ["SBF", "TullyFisher", "TDCOSMO2026", "Masers", "Sirens_GWTC5"]),
    ("all local incl. SH0ES", ["SH0ES_Ceph_SN", "CCHP_TRGB_SN", "SBF", "TullyFisher", "TDCOSMO2026",
                               "Masers", "Sirens_GWTC5"]),
]:
    wm = weighted_mean(*grp(names))
    for ref, (rv, re_) in [("CMB_SPA", M["CMB_SPA"]), ("BAO_BBN", M["BAO_BBN_DESI"]), ("SH0ES", M["SH0ES_Ceph_SN"])]:
        if ref == "SH0ES" and "SH0ES_Ceph_SN" in names:
            continue
        t = tension(wm["mean"], wm["error_scaled"], rv, re_)
        print(f"  {title:50s} {wm['mean']:6.2f} +- {wm['error_scaled']:4.2f} (S={wm['scale_factor']:.2f}) "
              f"vs {ref}: z={t['z']:.2f}")

# rough correlated variant: CCHP and SBF both rest on NGC 4258 alone (D-24, D-29);
# NGC 4258 distance error ~1.45% (7.58 +- 0.11 Mpc, RE-27, not seen by checker) -> shared H0 error.
print("\n== Rough NGC 4258 correlation: CCHP + SBF + TD + masers + sirens (GLS) ==")
f_anchor = 0.11 / 7.58
names = ["CCHP_TRGB_SN", "SBF", "TDCOSMO2026", "Masers", "Sirens_GWTC5"]
vals = [M[n][0] for n in names]
errs = [M[n][1] for n in names]
shared = {"CCHP_TRGB_SN": f_anchor * 70.39, "SBF": f_anchor * 73.8, "Masers": 0.0}
n = len(names)
C = [[0.0] * n for _ in range(n)]
for i in range(n):
    C[i][i] = errs[i] ** 2
for i in range(n):
    for j in range(n):
        if i != j:
            C[i][j] = shared.get(names[i], 0.0) * shared.get(names[j], 0.0)


def inv(A):
    m = len(A)
    Aug = [row[:] + [1.0 if i == j else 0.0 for j in range(m)] for i, row in enumerate(A)]
    for c in range(m):
        p = max(range(c, m), key=lambda r: abs(Aug[r][c]))
        Aug[c], Aug[p] = Aug[p], Aug[c]
        pv = Aug[c][c]
        Aug[c] = [x / pv for x in Aug[c]]
        for r in range(m):
            if r != c:
                fac = Aug[r][c]
                Aug[r] = [a - fac * b for a, b in zip(Aug[r], Aug[c])]
    return [row[m:] for row in Aug]


Ci = inv(C)
W = sum(sum(row) for row in Ci)
mean = sum(Ci[i][j] * vals[j] for i in range(n) for j in range(n)) / W
err = 1 / math.sqrt(W)
print(f"  shared anchor fraction {f_anchor*100:.2f}% -> shared err CCHP {shared['CCHP_TRGB_SN']:.2f}, SBF {shared['SBF']:.2f}")
t = tension(mean, err, 67.19, 0.38)
print(f"  GLS mean {mean:.2f} +- {err:.2f}; vs CMB-SPA z={t['z']:.2f}")

print("\n== Magnitude and sound-horizon restatements (premise 8) ==")
for loc in [73.49, 73.264, 70.39]:
    for early_v in [67.19, 68.50]:
        dm = 5 * math.log10(loc / early_v)
        print(f"  H0_loc={loc:6.2f} vs {early_v:5.2f}: gap {100*(loc/early_v-1):5.2f}% , "
              f"delta M_B = 5log10 ratio = {dm:.3f} mag; r_d needed at fixed r_d*H0 = "
              f"{147.00*early_v/loc:.1f} Mpc (from 147.00), reduction {100*(1-early_v/loc):.2f}%")
print("  Published M_B: ladder R22 -19.253 +- 0.027 (Pantheon+ system); inverse ladder DES5Y+DESI "
      "-19.375 (cosmography) / -19.394 (LCDM) mag (D-21, different SN systems)")
for mb_inv in [-19.375, -19.394]:
    print(f"    naive difference {(-19.253) - mb_inv:+.3f} mag (NOT comparable: SN zero points differ)")

print("\n== Premise 3: spread of 'CMB H0' across late-time models (D-51, D-52, D-53) ==")
models = {"LCDM CMB-SPA": 67.19, "w0wa DESI+CMB": 63.6, "wCDM DESI+CMB": 69.51, "w0wa +DESY5": 66.74,
          "w0wa +Pantheon+": 67.51, "EDE P-ACT-LB": 69.9, "EDE Poulin 2026 profile": 71.0}
for k, v in models.items():
    print(f"  {k:28s} {v:6.2f}")
print(f"  spread max-min = {max(models.values())-min(models.values()):.2f} km/s/Mpc")

print("\n== Fraction of gap closed by best early-time fits WITHOUT SH0ES prior ==")
for k, v, e in [("EDE P-ACT-LB", 69.9, sym(0.8, 1.5)), ("EDE Poulin 2026", 71.0, 1.1),
                ("eROSITA EDE", 71.4, 1.4), ("mod. recomb P-ACT-LB", 69.6, 1.0), ("PMF ACT", 69.1, 0.5)]:
    frac = (v - 67.19) / (73.49 - 67.19)
    t = tension(73.49, 0.93, v, e)
    print(f"  {k:22s} H0={v:5.2f}: closes {100*frac:4.0f}% of SH0ES-CMB_SPA gap; residual vs SH0ES z={t['z']:.2f}")

print("\n== Precision a deciding measurement needs ==")
for a, b, lab in [(73.3, 67.2, "73.3 vs 67.2 (real gap)"), (73.3, 70.0, "73.3 vs 70 (SH0ES vs CCHP-like)"),
                  (73.3, 68.5, "73.3 vs 68.5 (vs BAO+BBN)")]:
    print(f"  {lab:34s} delta={a-b:.1f}: total sigma for 3 sig {precision_needed(a-b,3):.2f} "
          f"({100*precision_needed(a-b,3)/a:.2f}%), for 5 sig {precision_needed(a-b,5):.2f} "
          f"({100*precision_needed(a-b,5)/a:.2f}%) km/s/Mpc")
