"""Empiricist lens: which partition of the lifetime data carries the disagreement, how much of it rests on
one experiment, how J-PARC's internal scatter changes its weight, and how often a gap this size arises by
chance under the heavy-tailed error distributions of Bailey 2017 (Student-t, nu ~ 2-4).

Units: lifetimes in s (SI). Errors: stat and sys combined in quadrature per experiment (my choice).
Inputs are dossier items D-20, D-22 (Sussex-ILL, lead only, unverified), D-23, D-24, D-27, D-28, D-29, D-30.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import stats_tools as st
from mpmath import mp, quad, gamma, sqrt, pi, inf

q = lambda *a: st.total_error(*a)

# ---- experiments (value, symmetric total error in s) ----
BL1 = (887.7, q(1.2, 1.9))              # D-20
SUSSEX = (889.2, q(3.0, 3.8))           # D-22 (lead, unverified)
JP_up, JP_dn = q(1.7, 4.0), q(1.7, 3.6)  # D-23 asymmetric
JPARC = (877.2, 0.5 * (JP_up + JP_dn))  # symmetrised (mean of up/down) for chi2 tools
UCNTAU = (877.82, q(0.22, 0.20))        # D-27 (up-side sys used: +0.20)
EZHOV = (878.3, q(1.6, 1.0))            # D-30 (search-summary)
GRAV = (881.5, q(0.7, 0.6))             # D-28
SER05 = (878.5, q(0.7, 0.3))            # D-29 (same group, earlier apparatus)
MAMBO = (880.7, q(1.3, 1.2))            # D-29
STEY = (882.5, q(1.4, 1.5))             # D-29
ARZ = (880.2, 1.2)                      # D-29 (split unknown; 1.2 s total)

def grp(*xs):
    return ([x[0] for x in xs], [x[1] for x in xs])

print("Inputs (s): BL1 %.1f+-%.2f, Sussex %.1f+-%.2f, J-PARC %.1f +%.2f/-%.2f (sym %.2f), UCNtau %.2f+-%.3f,"
      " Ezhov %.1f+-%.2f, Gravitrap %.1f+-%.2f, Serebrov05 %.1f+-%.2f, MAMBO %.1f+-%.2f, Steyerl %.1f+-%.2f, Arz %.1f+-%.1f"
      % (BL1 + SUSSEX + (877.2, JP_up, JP_dn, JPARC[1]) + UCNTAU + EZHOV + GRAV + SER05 + MAMBO + STEY + ARZ))

classes = {
    "proton_beam": grp(BL1, SUSSEX),
    "electron_beam": grp(JPARC),
    "material_bottle": grp(GRAV, SER05, MAMBO, STEY, ARZ),
    "magnetic_trap": grp(UCNTAU, EZHOV),
}
print("\n== per-class weighted means ==")
for k, (v, e) in classes.items():
    w = st.weighted_mean(v, e)
    print(f"{k:16s} mean {w['mean']:.2f} s  err {w['error']:.2f} s  chi2 {w['chi2']:.2f}/{w['dof']}  S {w['scale_factor']:.2f}  err_scaled {w['error_scaled']:.2f} s")

def partition(name, groups):
    r = st.grouped_chi2(groups)
    print(f"\n== partition: {name} ==")
    for g, d in r["groups"].items():
        print(f"  {g:22s} mean {d['mean']:.2f} +- {d['error']:.2f} s  within chi2 {d['chi2']:.2f}/{d['dof']}")
    print(f"  within chi2 {r['within_chi2']:.2f}/{r['within_dof']} (p {r['p_within']:.3g}); between chi2 {r['between_chi2']:.2f}/{r['between_dof']} "
          f"(p {r['p_between']:.3g}, z {r['between_z']:.2f}); pooled chi2 {r['pooled']['chi2']:.2f}/{r['pooled']['dof']}")
    return r

allb = grp(GRAV, SER05, MAMBO, STEY, ARZ, UCNTAU, EZHOV)
partition("beam(p+e) vs bottle", {"beam_p_e": grp(BL1, SUSSEX, JPARC), "bottle": allb})
partition("proton-counting vs all else", {"proton": grp(BL1, SUSSEX), "rest": grp(JPARC, GRAV, SER05, MAMBO, STEY, ARZ, UCNTAU, EZHOV)})
partition("BL1 vs all else (reframe)", {"BL1": grp(BL1), "rest": grp(SUSSEX, JPARC, GRAV, SER05, MAMBO, STEY, ARZ, UCNTAU, EZHOV)})
partition("proton / electron / material / magnetic", classes)
partition("material vs magnetic", {"material": classes["material_bottle"], "magnetic": classes["magnetic_trap"]})

print("\n== pairwise tensions (two-sided, asymmetric where given) ==")
bott = st.weighted_mean(*allb)
pb = st.weighted_mean(*grp(BL1, SUSSEX))
def T(n1, x1, e1, n2, x2, e2):
    t = st.tension(x1, e1, x2, e2)
    print(f"  {n1} vs {n2}: diff {t['difference']:+.2f} s  sigma {t['sigma']:.2f} s  z {t['z']:.2f}  p {t['p_two_sided']:.2g}")
    return t
T("proton beam mean", pb["mean"], pb["error"], "bottle mean (unscaled)", bott["mean"], bott["error"])
T("proton beam mean", pb["mean"], pb["error"], "bottle mean (S-scaled)", bott["mean"], bott["error_scaled"])
T("BL1 alone", BL1[0], BL1[1], "UCNtau", UCNTAU[0], UCNTAU[1])
T("Sussex alone", SUSSEX[0], SUSSEX[1], "UCNtau", UCNTAU[0], UCNTAU[1])
T("J-PARC", 877.2, (JP_up, JP_dn), "UCNtau", UCNTAU[0], UCNTAU[1])
T("J-PARC", 877.2, (JP_up, JP_dn), "proton beam mean", pb["mean"], pb["error"])
T("J-PARC", 877.2, (JP_up, JP_dn), "BL1", BL1[0], BL1[1])
T("Gravitrap", GRAV[0], GRAV[1], "UCNtau", UCNTAU[0], UCNTAU[1])

# J-PARC internal scatter: chi2/dof = 15.8/3 (D-23). Inflate the stat error by S = sqrt(15.8/3).
S_jp = math.sqrt(15.8 / 3)
jp_up_s, jp_dn_s = q(1.7 * S_jp, 4.0), q(1.7 * S_jp, 3.6)
print(f"\nJ-PARC internal S = {S_jp:.2f}; stat 1.7 -> {1.7*S_jp:.2f} s; total +{jp_up_s:.2f}/-{jp_dn_s:.2f} s")
T("J-PARC (S-inflated)", 877.2, (jp_up_s, jp_dn_s), "proton beam mean", pb["mean"], pb["error"])
T("J-PARC (S-inflated)", 877.2, (jp_up_s, jp_dn_s), "UCNtau", UCNTAU[0], UCNTAU[1])
# J-PARC per-condition (D-24): stat only, to show spread
jpc = [(870.9, 3.5), (868.3, 4.0), (868.2, 7.7), (884.8, 2.4)]
w = st.weighted_mean([a for a, b in jpc], [b for a, b in jpc])
print(f"J-PARC 4 conditions (stat only): mean {w['mean']:.2f} s, chi2 {w['chi2']:.2f}/{w['dof']} (paper quotes 15.8/3 with its errors), p {w['p_consistent']:.3g}")
w3 = st.weighted_mean([a for a, b in jpc[:3]], [b for a, b in jpc[:3]])
print(f"J-PARC without 50 kPa/new-SFC: mean {w3['mean']:.2f} +- {w3['error']:.2f} s (stat only), chi2 {w3['chi2']:.2f}/{w3['dof']}")
print(f"J-PARC 50 kPa/new-SFC alone: 884.8 +- 2.4 s (stat) -> vs BL1 diff {884.8-887.7:+.1f} s; vs UCNtau diff {884.8-877.82:+.1f} s")

# UCNtau per-year scatter (D-27)
yrs = [(877.73, 0.32), (877.80, 0.50), (879.39, 0.89), (878.41, 0.58), (876.93, 0.57)]
w = st.weighted_mean([a for a, b in yrs], [b for a, b in yrs])
print(f"\nUCNtau per-year: mean {w['mean']:.2f} s, chi2 {w['chi2']:.2f}/{w['dof']}, p {w['p_consistent']:.3g}, S {w['scale_factor']:.2f}")

# Leave-one-out: how much of the proton-vs-rest between-chi2 rests on BL1?
rest = grp(JPARC, GRAV, SER05, MAMBO, STEY, ARZ, UCNTAU, EZHOV)
r_full = st.grouped_chi2({"p": grp(BL1, SUSSEX), "rest": rest})
r_noBL1 = st.grouped_chi2({"p": grp(SUSSEX), "rest": rest})
r_noSus = st.grouped_chi2({"p": grp(BL1), "rest": rest})
print(f"\nLeave-one-out, proton vs rest between chi2: full {r_full['between_chi2']:.2f}; without BL1 {r_noBL1['between_chi2']:.2f} "
      f"(z {r_noBL1['between_z']:.2f}); without Sussex {r_noSus['between_chi2']:.2f} (z {r_noSus['between_z']:.2f})")
r_noUCN = st.grouped_chi2({"p": grp(BL1, SUSSEX), "rest": grp(JPARC, GRAV, SER05, MAMBO, STEY, ARZ, EZHOV)})
print(f"Without UCNtau: between chi2 {r_noUCN['between_chi2']:.2f} (z {r_noUCN['between_z']:.2f}); rest mean {r_noUCN['groups']['rest']['mean']:.2f} s")

# Size of gap as a rate
tb, tt = pb["mean"], bott["mean"]
print(f"\nGap: proton beam {tb:.2f} s - bottle {tt:.2f} s = {tb-tt:.2f} s; fraction 1-tt/tb = {1-tt/tb:.5f}; "
      f"missing rate 1/tt - 1/tb = {1/tt-1/tb:.3e} s^-1")

# ---- base rate under heavy tails (Bailey 2017: Student-t nu ~ 2-4) ----
mp.dps = 30
def t_two_sided(z, nu):
    c = gamma((nu + 1) / 2) / (sqrt(nu * pi) * gamma(nu / 2))
    f = lambda x: c * (1 + x * x / nu) ** (-(nu + 1) / 2)
    return 2 * quad(f, [z, inf])
print("\nP(|z| > Z) for one comparison: Gaussian vs Student-t (unit scale), Bailey 2017 nu ~ 2-4")
for Z in (3.0, 4.0, 4.5, 5.0):
    row = [f"Gauss {st.sigma_to_p(Z, two_sided=True):.2e}"] + [f"t{nu} {float(t_two_sided(Z, nu)):.2e}" for nu in (2, 3, 4, 10)]
    print(f"  Z={Z}: " + ", ".join(row))
z_obs = r_full["between_z"]
print(f"Observed proton-vs-rest z = {z_obs:.2f}")
for nu in (2, 3, 4, 10):
    p1 = float(t_two_sided(z_obs, nu))
    print(f"  nu={nu}: p(one comparison) {p1:.3e}; equivalent Gaussian z {st.p_to_sigma(p1, two_sided=True):.2f}")
