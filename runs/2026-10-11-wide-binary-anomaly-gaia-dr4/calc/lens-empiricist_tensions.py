"""Empiricist lens: how large is the observed DR3 disagreement, and how much of it is
estimator, model or sample choice on the SAME data?  All inputs from the dossier (D-xx).
gamma = G_eff/G is dimensionless. Errors (up, down) are asymmetric as quoted.
Caveat printed below: most results share Gaia DR3 astrometry (D-11), so chi2 between them
overstates independent evidence."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import tension, total_error, grouped_chi2, weighted_mean

def show(label, d):
    print(f"{label}: diff = {d['difference']:+.3f}, sigma = {d['sigma']:.3f}, z = {d['z']:.2f}")

print("== 1. Pairwise tensions (published gamma, low-acceleration) ==")
chae24b_tot = total_error((0.10, 0.09), (0.16, 0.09))          # D-22 stat + syst
print("Chae 2024b total error (up, down) =", tuple(round(x, 3) for x in chae24b_tot))
bouf_E2 = (1.068 - 1.045, 1.045 - 1.025)                      # D-31 68% bootstrap
bouf_E3 = (0.02, 0.01)                                         # D-31 1.05 [1.04, 1.07]
banik = (0.03, 0.02)                                           # D-28 researcher conversion 0.99 +0.03 -0.02
show("Chae24b(stat+sys) 1.37 vs Boufourou E2 1.045 [same parent data]",
     tension(1.37, chae24b_tot, 1.045, bouf_E2))
show("Chae24b(stat only) 1.37 vs Boufourou E2 1.045",
     tension(1.37, (0.10, 0.09), 1.045, bouf_E2))
show("Chae24b(stat+sys) 1.37 vs Boufourou E3 1.05",
     tension(1.37, chae24b_tot, 1.05, bouf_E3))
show("Chae24b(stat+sys) 1.37 vs Banik+24 0.99 (converted)",
     tension(1.37, chae24b_tot, 0.99, banik))
show("Chae 2023 1.43+-0.06 (stat) vs Banik+24 0.99",
     tension(1.43, 0.06, 0.99, banik))
show("Chae 2024a pure 1.49 vs Banik+24 0.99",
     tension(1.49, (0.21, 0.19), 0.99, banik))
show("Hernandez+24 1.5+-0.2 vs 1.0", tension(1.5, 0.2, 1.0, 0.0001))
show("Chae+26 1.60 vs Saad&Ting 1.00 [SAME 36 pairs; modelling only]",
     tension(1.60, (0.24, 0.14), 1.00, (0.24, 0.19)))
show("Chae 2025 3D 1.48 vs 1.0", tension(1.48, (0.33, 0.23), 1.0, 0.0001))
show("Saad&Ting C3PO s>3kau 1.17 vs MOND 1.37", tension(1.17, (0.37, 0.23), 1.37, 0.0001))
show("Boufourou deep bin 1.11+-0.07 vs MOND 1.37", tension(1.11, 0.07, 1.37, 0.0001))
show("Boufourou deep bin 1.11+-0.07 vs Newton 1.00", tension(1.11, 0.07, 1.00, 0.0001))

print()
print("== 2. Same-data decomposition of the Chae-vs-robust gap (Chae 2024 catalogue) ==")
gap = 1.37 - 1.045
for fm in (1.12, 1.20):
    est = fm - 1.045
    print(f"implied full-median {fm:.2f}: estimator share = {est:.3f} of gap {gap:.3f} = {est/gap:.0%};"
          f" remaining (pipeline: cuts, f_multi, templates) = {gap-est:.3f} = {(gap-est)/gap:.0%}")
print(f"Boufourou fiducial cuts keep 41760/81088 = {41760/81088:.1%} of pairs (D-31)")
print("Saad&Ting same 36 pairs: deprojection choice moves gamma 1.00 -> 1.56, delta = 0.56 (D-17)")
import math
print(f"Cookson+26 cut choice: Newton 1501x (d<130pc, ipd=0) -> MOND 12x (d<150pc, no ipd):"
      f" swing = {math.log10(1501*12):.2f} dex in Bayes-factor-like ratio (D-29)")

print()
print("== 3. Grouped chi2 by camp (symmetrised: mean of up/down) -- correlated data, upper bound ==")
sym = lambda e: (e[0] + e[1]) / 2
groups = {
    "pro (Chae23, Chae24a, Chae24b tot, YTC25, Hern24, Chae25)":
        ([1.43, 1.49, 1.37, 1.32, 1.5, 1.48],
         [0.06, 0.07, sym(chae24b_tot), sym((0.12, 0.11)), 0.2, sym((0.33, 0.23))]),
    "null (Banik24, BoufE2, Saad&Ting C3PO, S&T 36-pair)":
        ([0.99, 1.045, 1.17, 1.00],
         [sym(banik), sym(bouf_E2), sym((0.37, 0.23)), sym((0.24, 0.19))]),
}
r = grouped_chi2(groups)
for k, g in r["groups"].items():
    print(f"{k}: mean = {g['mean']:.3f} +- {g['error']:.3f}, chi2 = {g['chi2']:.2f}/{g['dof']}, p = {g['p_consistent']:.3f}")
print(f"between-camp chi2 = {r['between_chi2']:.1f} (dof {r['between_dof']}), z = {r['between_z']:.1f}")
print(f"within chi2 = {r['within_chi2']:.1f}/{r['within_dof']}, p = {r['p_within']:.3f}")
p = r["pooled"]
print(f"pooled mean = {p['mean']:.3f} +- {p['error']:.3f}, PDG scale factor S = {p['scale_factor']:.2f}"
      f" -> {p['mean']:.3f} +- {p['error_scaled']:.3f}")

print()
print("== 4. Grouped chi2 by estimator family (provisional mapping, D-69) ==")
fam = {
    "F1 full-median": ([1.43, 1.37, 1.32], [0.06, sym(chae24b_tot), sym((0.12, 0.11))]),
    "F2 tail-truncated": ([1.045], [sym(bouf_E2)]),
    "F3 mixture": ([0.99, 1.05], [sym(banik), sym(bouf_E3)]),
    "F4 Bayes 3D (Chae25, Chae+26, S&T-36, C3PO)": ([1.48, 1.60, 1.00, 1.17],
        [sym((0.33, 0.23)), sym((0.24, 0.14)), sym((0.24, 0.19)), sym((0.37, 0.23))]),
}
r = grouped_chi2(fam)
for k, g in r["groups"].items():
    print(f"{k}: mean = {g['mean']:.3f} +- {g['error']:.3f}, chi2 = {g['chi2']:.2f}/{g['dof']}, p = {g['p_consistent']:.3f}")
print(f"between-family chi2 = {r['between_chi2']:.1f} (dof {r['between_dof']}), z = {r['between_z']:.1f}")
print("NOTE: F4 includes Chae+26 and S&T on the same 36 pairs (counted twice here deliberately to show"
      " within-family model spread); F1 entries share Chae 2023 parent data.")
