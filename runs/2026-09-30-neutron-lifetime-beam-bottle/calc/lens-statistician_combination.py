"""Statistician lens: combination of neutron-lifetime results by method class, grouped chi2,
tensions, partitions, correlations, Bayes bounds, and precision needed. Units: seconds (s)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from stats_tools import (weighted_mean, grouped_chi2, tension, total_error, sigma_to_p, p_to_sigma,
                         sidak_global_p, min_bayes_factor, prior_needed, posterior_probability,
                         exposure_to_reach, precision_needed, z_after_exposure, _chi2_sf)

def q(*a):
    return math.sqrt(sum(x * x for x in a))

def symm(up, down):
    return 0.5 * (up + down)

# ---------------- inputs (one value per independent dataset) ----------------
# proton-counting beam
BL1 = (887.7, q(1.2, 1.9))           # Yue 2013 [D-20], supersedes Nico 2005
SUS = (889.2, q(3.0, 3.8))           # Byrne 1996 [D-22; PDG listing]
# electron-counting beam: J-PARC 2024 [D-23], 877.2 +- 1.7 (stat) +4.0/-3.6 (sys)
JP_up, JP_dn = q(1.7, 4.0), q(1.7, 3.6)
JP = (877.2, (JP_up, JP_dn))
# material bottles [D-28, D-29, PDG listing]
SER05 = (878.5, q(0.7, 0.3)); PIC10 = (880.7, q(1.3, 1.2)); STE12 = (882.5, q(1.4, 1.5))
ARZ15 = (880.2, 1.2); SER18 = (881.5, q(0.7, 0.6))
# magnetic traps
MUS25_up, MUS25_dn = q(0.22, 0.20), q(0.22, 0.17)
MUS25 = (877.82, symm(MUS25_up, MUS25_dn))   # [D-27]
PAT18_up, PAT18_dn = q(0.7, 0.4), q(0.7, 0.2)
PAT18 = (877.7, symm(PAT18_up, PAT18_dn))    # Pattie 18, separate 2016-17 data, same apparatus (PDG)
EZH18 = (878.3, q(1.6, 1.0))                 # [D-30]
print("Input totals (s): BL1 %.3f, Sussex %.3f, J-PARC +%.3f/-%.3f (sym %.3f), MUS25 +%.3f/-%.3f, PAT18 +%.3f/-%.3f"
      % (BL1[1], SUS[1], JP_up, JP_dn, symm(JP_up, JP_dn), MUS25_up, MUS25_dn, PAT18_up, PAT18_dn))

pbeam = [BL1, SUS]
mat = [SER05, PIC10, STE12, ARZ15, SER18]
mag = [MUS25, PAT18, EZH18]
store = mat + mag
JPs = (JP[0], symm(JP_up, JP_dn))

def wm(lst):
    return weighted_mean([v for v, _ in lst], [e for _, e in lst])

def show(name, r):
    print("%-34s mean %.3f +- %.3f s (scaled +- %.3f, S=%.2f), chi2 %.2f / %d dof, p=%.3g"
          % (name, r["mean"], r["error"], r["error_scaled"], r["scale_factor"], r["chi2"], r["dof"], r["p_consistent"]))

print("\n== 1. Class combinations ==")
R = {}
for nm, l in [("proton beam (BL1+Sussex)", pbeam), ("material bottles (5)", mat), ("magnetic traps (3)", mag),
              ("all storage (8)", store), ("PDG-set check: storage w/o Pattie", mat + [MUS25, EZH18])]:
    R[nm] = wm(l); show(nm, R[nm])
print("J-PARC 2024: 877.2 +%.2f/-%.2f s (single result)" % (JP_up, JP_dn))
pb, st = R["proton beam (BL1+Sussex)"], R["all storage (8)"]
print("BL1 weight share in proton-beam mean: %.3f" % ((1 / BL1[1]**2) / (1 / BL1[1]**2 + 1 / SUS[1]**2)))

print("\n== 2. Tensions (two-sided) ==")
def T(label, x1, e1, x2, e2):
    t = tension(x1, e1, x2, e2)
    print("%-58s diff %+7.2f s, sigma %.2f s, z %.2f, p2 %.2e" % (label, t["difference"], t["sigma"], t["z"], t["p_two_sided"]))
    return t
st_s = st["error_scaled"]
t_main = T("p-beam vs storage (storage S-scaled err)", pb["mean"], pb["error"], st["mean"], st_s)
T("p-beam vs storage (unscaled)", pb["mean"], pb["error"], st["mean"], st["error"])
T("BL1 alone vs storage (scaled)", BL1[0], BL1[1], st["mean"], st_s)
T("Sussex alone vs storage (scaled)", SUS[0], SUS[1], st["mean"], st_s)
T("p-beam vs magnetic traps", pb["mean"], pb["error"], R["magnetic traps (3)"]["mean"], R["magnetic traps (3)"]["error_scaled"])
T("p-beam vs material bottles (scaled)", pb["mean"], pb["error"], R["material bottles (5)"]["mean"], R["material bottles (5)"]["error_scaled"])
T("material vs magnetic (both scaled)", R["material bottles (5)"]["mean"], R["material bottles (5)"]["error_scaled"],
  R["magnetic traps (3)"]["mean"], R["magnetic traps (3)"]["error_scaled"])
T("Serebrov18 vs Musedinovic25", SER18[0], SER18[1], MUS25[0], (MUS25_up, MUS25_dn))
T("J-PARC vs p-beam (asym, facing side)", JP[0], JP[1], pb["mean"], pb["error"])
T("J-PARC vs BL1 alone", JP[0], JP[1], BL1[0], BL1[1])
T("J-PARC vs storage (asym, facing side)", JP[0], JP[1], st["mean"], st_s)
# J-PARC internal inconsistency: inflate its stat error by sqrt(15.8/3)
S_jp = math.sqrt(15.8 / 3)
JPi = (877.2, (q(1.7 * S_jp, 4.0), q(1.7 * S_jp, 3.6)))
print("J-PARC internal S = sqrt(15.8/3) = %.2f -> inflated errors +%.2f/-%.2f" % (S_jp, JPi[1][0], JPi[1][1]))
t_jp_beam_infl = T("J-PARC(inflated) vs p-beam", JPi[0], JPi[1], pb["mean"], pb["error"])
T("J-PARC(inflated) vs storage", JPi[0], JPi[1], st["mean"], st_s)
# J-PARC four conditions (stat only, Table II)
jp4 = [(870.9, 3.5), (868.3, 4.0), (868.2, 7.7), (884.8, 2.4)]
r4 = wm(jp4); show("J-PARC 4 conditions, stat only", r4)
jp4b = [(870.9, q(3.5, 2.3, 5.2)), (868.3, q(4.0, 2.2, 3.5)), (868.2, q(7.7, 1.8, 4.35)), (884.8, q(2.4, 1.05, 3.1))]
r4b = wm(jp4b); show("J-PARC 4 conditions, +sym other cols", r4b)
print("  (the listed columns beyond stat are unlabelled in the dossier; second line is a stress test only)")

print("\n== 3. Beam averages with J-PARC ==")
b3 = wm(pbeam + [JPs]); show("beam (BL1+Sussex+J-PARC sym)", b3)
T("beam incl. J-PARC vs storage", b3["mean"], b3["error_scaled"], st["mean"], st_s)

print("\n== 4. Grouped chi2 (J-PARC symmetrized to mean of sides, %.2f s) ==" % JPs[1])
def G(label, groups):
    g = grouped_chi2({k: ([v for v, _ in l], [e for _, e in l]) for k, l in groups.items()})
    print("-- " + label)
    for k, d in g["groups"].items() if "groups" in g else []:
        pass
    return g
import json
def G2(label, groups):
    g = grouped_chi2({k: ([v for v, _ in l], [e for _, e in l]) for k, l in groups.items()})
    print("-- " + label)
    for k, v in g.items():
        if isinstance(v, dict):
            print("   ", k, {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in v.items()} if all(not isinstance(vv, dict) for vv in v.values()) else "")
            for kk, vv in v.items():
                if isinstance(vv, dict):
                    print("      %-20s mean %.3f +- %.3f chi2 %.2f/%d p %.3g" % (kk, vv["mean"], vv["error"], vv["chi2"], vv["dof"], vv["p_consistent"]))
        else:
            print("   ", k, round(v, 5) if isinstance(v, float) else v)
    return g
g2 = G2("beam(p) vs storage (J-PARC excluded)", {"pbeam": pbeam, "storage": store})
g2j = G2("beam(p+e) vs storage", {"beam": pbeam + [JPs], "storage": store})
g2p = G2("proton-counting vs everything else", {"pbeam": pbeam, "rest": store + [JPs]})
g3 = G2("three classes: pbeam, ebeam, storage", {"pbeam": pbeam, "ebeam": [JPs], "storage": store})
g4 = G2("four classes: pbeam, ebeam, material, magnetic", {"pbeam": pbeam, "ebeam": [JPs], "material": mat, "magnetic": mag})

print("\n== 5. Partition comparison: total chi2 of a 2-mean model ==")
allm = pbeam + [JPs] + store
tot = wm(allm); show("one common value (all 11)", tot)
print("pooled z-equivalent of one-value chi2: p=%.3g -> %.2f sigma (two-sided)" % (tot["p_consistent"], p_to_sigma(tot["p_consistent"], True)))
def two_mean_chi2(A, B):
    a, b = wm(A), wm(B); return a["chi2"] + b["chi2"]
c_bb = two_mean_chi2(pbeam + [JPs], store)
c_pr = two_mean_chi2(pbeam, store + [JPs])
c_bl1 = two_mean_chi2([BL1], [SUS, JPs] + store)
print("beam/bottle partition chi2 = %.2f; proton/rest partition chi2 = %.2f; delta = %.2f (J-PARC favours proton/rest)" % (c_bb, c_pr, c_bb - c_pr))
print("Likelihood ratio proton/rest vs beam/bottle = exp(delta/2) = %.2f" % math.exp((c_bb - c_pr) / 2))
print("BL1-vs-rest partition chi2 = %.2f" % c_bl1)
# look-elsewhere over partitions tried (beam/bottle, proton/rest, BL1/rest, material/magnetic, strong-field/weak ~ proton/rest)
z_loc = math.sqrt(g2p["between_chi2"] if "between_chi2" in g2p else 0)

print("\n== 6. Correlations: shared apparatus/group systematics ==")
def gls(vals, cov):
    vals = np.array(vals); C = np.array(cov); Ci = np.linalg.inv(C); one = np.ones(len(vals))
    w = Ci @ one / (one @ Ci @ one); m = w @ vals; e = math.sqrt(1 / (one @ Ci @ one))
    r = vals - m; chi2 = float(r @ Ci @ r)
    return m, e, chi2
names = ["SER05", "PIC10", "STE12", "ARZ15", "SER18", "MUS25", "PAT18", "EZH18"]
vals = [SER05[0], PIC10[0], STE12[0], ARZ15[0], SER18[0], MUS25[0], PAT18[0], EZH18[0]]
sys_ = [0.3, 1.2, 1.5, None, 0.6, symm(0.20, 0.17), symm(0.4, 0.2), 1.0]
tot_ = [e for _, e in store]
for rho in (0.0, 0.8):
    C = np.diag([t * t for t in tot_])
    # Serebrov 05/18 (same group) and Pattie18/Musedinovic25 (same apparatus): correlate systematic parts
    for i, j in [(0, 4), (5, 6)]:
        C[i, j] = C[j, i] = rho * sys_[i] * sys_[j]
    m, e, c2 = gls(vals, C)
    print("storage GLS rho_sys=%.1f: mean %.3f +- %.3f, chi2 %.2f/7, S=%.2f" % (rho, m, e, c2, max(1, math.sqrt(c2 / 7))))
    # stress: correlate TOTAL errors of same-group pairs at rho
    C2 = np.diag([t * t for t in tot_])
    for i, j in [(0, 4), (5, 6)]:
        C2[i, j] = C2[j, i] = rho * tot_[i] * tot_[j]
    m2, e2, c22 = gls(vals, C2)
    print("storage GLS rho_total=%.1f (stress): mean %.3f +- %.3f, chi2 %.2f/7, S=%.2f; tension with p-beam %.2f sigma"
          % (rho, m2, e2, c22, max(1, math.sqrt(c22 / 7)), abs(pb["mean"] - m2) / q(pb["error"], e2 * max(1, math.sqrt(c22 / 7)))))
# p-beam: BL1 & Sussex share method, not apparatus; common method systematic stress
for rho in (0.0, 0.8):
    C = np.array([[BL1[1]**2, rho * 1.9 * 3.8], [rho * 1.9 * 3.8, SUS[1]**2]])
    m, e, c2 = gls([BL1[0], SUS[0]], C)
    print("p-beam GLS rho_sys=%.1f: mean %.3f +- %.3f, chi2 %.3f; tension with storage(scaled) %.2f sigma"
          % (rho, m, e, c2, abs(m - st["mean"]) / q(e, st_s)))

print("\n== 7. Common unknown systematic needed to erase the tension ==")
gap = pb["mean"] - st["mean"]
for z in (3, 2, 1):
    sc = math.sqrt(max(0, (gap / z)**2 - pb["error"]**2 - st_s**2))
    print("common extra uncertainty on either side for tension to fall to %d sigma: %.2f s" % (z, sc))
print("gap = %.2f s = %.4f of tau; missing rate = %.3e s^-1" % (gap, gap / pb["mean"], 1 / st["mean"] - 1 / pb["mean"]))
# uniform error inflation factor for all 11 results needed to bring p-beam vs storage to 2 and 3 sigma
z0 = abs(gap) / q(pb["error"], st["error"])
for z in (3, 2):
    print("global error-inflation factor for z=%d: %.2f (unscaled z0=%.2f)" % (z, z0 / z, z0))

print("\n== 8. Look-elsewhere over partitions ==")
zl = t_main["z"]; pl = t_main["p_two_sided"]
for n in (1, 3, 5, 10):
    pg = sidak_global_p(pl, n); print("local z %.2f (p2 %.2e): %2d partitions tried -> global p %.2e, z %.2f" % (zl, pl, n, pg, p_to_sigma(pg, True)))

print("\n== 9. Bayes-factor bounds (fluctuation vs real difference) ==")
for label, z in [("p-beam vs storage", t_main["z"]), ("J-PARC vs p-beam", 10.77/4.80), ("J-PARC(infl) vs p-beam", t_jp_beam_infl["z"]),
                 ("material vs magnetic", abs(R["material bottles (5)"]["mean"] - R["magnetic traps (3)"]["mean"]) /
                  q(R["material bottles (5)"]["error_scaled"], R["magnetic traps (3)"]["error_scaled"]))]:
    p2 = sigma_to_p(z, two_sided=True); b = min_bayes_factor(p2)
    odds = b["max_odds_against_null"]
    print("%-26s z %.2f p2 %.2e: Sellke BF_min %.2e (max odds %.0f:1), Gaussian bound %.2e; prior needed for 50%% %.4f, for 95%% %.4f"
          % (label, z, p2, b["sellke"], odds, b["gaussian"], prior_needed(odds, 0.5), prior_needed(odds, 0.95)))
# realistic BF for "two values" with a Gaussian prior on the gap, width tau_g
d, sd = t_main["difference"], t_main["sigma"]
for tau_g in (5.0, 10.0, 20.0):
    bf = (math.exp(-0.5 * d * d / (sd * sd + tau_g * tau_g)) / math.sqrt(sd * sd + tau_g * tau_g)) / (math.exp(-0.5 * d * d / (sd * sd)) / sd)
    print("Gaussian-prior BF(two values : one) with gap prior N(0, %.0f s): %.1f; posterior at prior 0.5: %.4f" % (tau_g, bf, posterior_probability(0.5, bf)))

print("\n== 10. Precision needed ==")
dcent = gap
for z in (3, 5):
    print("single new measurement vs a known pole (either side), z=%d: total sigma <= %.2f s" % (z, precision_needed(dcent, z)))
    # new measurement x ~ one pole; compare to the other pole with its uncertainty
    s_vs_store = math.sqrt(max(0, precision_needed(dcent, z)**2 - st_s**2))
    s_vs_beam = math.sqrt(max(0, precision_needed(dcent, z)**2 - pb["error"]**2))
    print("   new result must have sigma <= %.2f s to exclude the storage value, <= %.2f s to exclude the p-beam value (%s)"
          % (s_vs_store, s_vs_beam, "impossible: p-beam error alone exceeds budget" if s_vs_beam == 0 else ""))
for s_new, lab in [(1.0, "LiNA ~1 s / BL2 <1 s"), (0.3, "BL3 0.3 s"), (1.5, "UCNProBe 1-2 s (1.5)"), (2.0, "UCNProBe 2 s")]:
    print("%-24s: separation of the two poles %.1f sigma (vs storage), %.1f sigma (vs p-beam)"
          % (lab, dcent / q(s_new, st_s), dcent / q(s_new, pb["error"])))
# exposure: BL1-type p-beam systematic floor 1.9 s
print("BL1: gap/sys floor -> max z from more BL1-type data: %.2f; exposure_to_reach 5 sigma: %s"
      % (gap / q(1.9, st_s), exposure_to_reach(delta=gap, sigma_stat=1.2, sigma_sys=1.9, sigma_other=st_s)))
print("J-PARC 2024 (stat 1.7, sys ~3.8): exposure to separate from p-beam at 5 sigma: %s; at 3 sigma: %.2f"
      % (exposure_to_reach(delta=10.5, sigma_stat=1.7, sigma_sys=3.8, sigma_other=pb["error"], z_target=5),
         exposure_to_reach(delta=10.5, sigma_stat=1.7, sigma_sys=3.8, sigma_other=pb["error"], z_target=3)))
