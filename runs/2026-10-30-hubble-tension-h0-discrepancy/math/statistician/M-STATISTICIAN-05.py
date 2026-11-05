"""M-STATISTICIAN-05: grouped chi2 per class, PDG scale factor, partitions (F5, F6, F7, table C).
Groups combined by inverse variance; chi2_within = sum over groups of chi2 about the group mean;
chi2_between = chi2 of the group means about their own weighted mean (dof = groups - 1);
z = two-sided Gaussian equivalent of the chi2 tail. PDG S = sqrt(chi2_total/(N-1)). km/s/Mpc."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import wmean, quad, chi2_sf, z_of_p2, close
from math_checks import identity, limit, units, finish

V = {  # value, symmetrised total sigma
    "SPA": (67.19, 0.38), "BB": (68.50, 0.58), "SH": (73.49, 0.93), "CC": (70.39, float(quad(1.22, 1.33, .70))),
    "SBF": (73.8, float(quad(0.7, 2.3))), "TF": (73.3, float(quad(2.1, 3.5))), "TD": (71.1, 2.35),
    "MAS": (71.6, 3.7), "GW": (71.7, 8.45), "ZB": (69.2, 1.35)}


def grp(keys):
    return wmean([V[k][0] for k in keys], [V[k][1] for k in keys])


def partition(groups, label, claims):
    stats = [grp(g) for g in groups]
    within = sum(s[2] for s in stats); dof_w = sum(len(g) - 1 for g in groups)
    m, s, between = wmean([x[0] for x in stats], [x[1] for x in stats])
    zb = z_of_p2(chi2_sf(between, len(groups) - 1))
    print(f"{label}: within {float(within):.3f}/{dof_w} (p = {float(chi2_sf(within, dof_w)):.3f}); "
          f"between {float(between):.2f}/{len(groups)-1}, z = {float(zb):.3f}")
    for (name, mine), cl in zip([("within", within), ("between z", zb)], claims[:2]):
        if cl is not None:
            close(label + " " + name, mine, cl[0], cl[1])
    return stats, within, between


# classes: non-SN ladder = SBF+TF
nonsn = grp(["SBF", "TF"])
close("non-SN class within chi2", nonsn[2], 0.01, 0.006)
V["NSL"] = (nonsn[0], nonsn[1])
classes = ["SPA", "BB", "SH", "CC", "NSL", "TD", "MAS", "GW"]
m, s, chb = wmean([V[k][0] for k in classes], [V[k][1] for k in classes])
close("between-class chi2", chb, 49.87, 0.15)
close("  z (7 dof)", z_of_p2(chi2_sf(chb, 7)), 5.66, 0.02)
allv = ["SPA", "BB", "SH", "CC", "SBF", "TF", "TD", "MAS", "GW"]
m9, s9, c9 = wmean([V[k][0] for k in allv], [V[k][1] for k in allv])
close("pooled mean", m9, 68.43, 0.01); close("pooled sigma", s9, 0.29, 0.005)
close("PDG S = sqrt(chi2/(N-1)), N = 9", mp.sqrt(c9 / 8), 2.50, 0.01)

late = ["SH", "CC", "NSL", "TD", "MAS", "GW"]
st, w1, b1 = partition([["SPA", "BB"], late], "P1 early/late", [(6.50, 0.05), (6.59, 0.02)])
close("P1 late mean", st[1][0], 72.77, 0.01); close("P1 late sigma", st[1][1], 0.72, 0.01)
close("P1 between chi2", b1, 43.4, 0.1)
_, w2, _ = partition([["SH"], ["SPA", "BB", "CC", "NSL", "TD", "MAS", "GW"]], "P2 SH0ES/rest", [(17.0, 0.1), (5.73, 0.02)])
st3, _, _ = partition([["SPA", "BB"], ["SH"], ["CC", "NSL", "TD", "MAS", "GW"]], "P3 three-way", [(5.01, 0.05), (6.38, 0.02)])
close("P3 other-local mean", st3[2][0], 71.69, 0.01); close("P3 other-local sigma", st3[2][1], 1.14, 0.01)
close("P3 other vs early z", (st3[2][0] - st3[0][0]) / quad(st3[2][1], st3[0][1]), 3.5, 0.05)
close("P3 other vs SH0ES z", (73.49 - st3[2][0]) / quad(st3[2][1], 0.93), 1.2, 0.05)
partition([["SPA", "BB"], late + ["ZB"]], "P4 r_s / no r_s", [(11.95, 0.05), (6.18, 0.02)])
close("Delta chi2_within P2 - P1", w2 - w1, 10.5, 0.15)
ns = grp(["SBF", "TF", "TD", "MAS", "GW"])
close("no-SN local mean", ns[0], 72.39, 0.01); close("no-SN local sigma", ns[1], 1.41, 0.01)
close("no-SN vs early z", (ns[0] - 67.5834) / quad(ns[1], 0.317855), 3.32, 0.01)
print(f"no-SN within chi2 = {float(ns[2]):.3f}/4 (table A says 4.32/5)")

# structural checks: chi2 decomposition total = within + between (one-group-per-value identity)
identity("w1*(x1-(w1*x1+w2*x2)/(w1+w2))**2 + w2*(x2-(w1*x1+w2*x2)/(w1+w2))**2",
         "(x1-x2)**2/(1/w1+1/w2)", domain={"x1": (-10, 10), "x2": (-10, 10)})
limit("sqrt(c/(n-1))", "c", "n-1", "1", domain={"n": (2, 20)})
units("(5.2 km/s/Mpc)**2 / (0.72 km/s/Mpc)**2", "dimensionless")
raise SystemExit(finish())
