"""Falsifier C7-0 (magnitude): can 'a fluctuation plus several modest underestimated uncertainties
(BL1, J-PARC, material bottles), none dominating' carry the 9.65 s proton-beam/storage gap?
Units: lifetimes and shifts in s (SI). Inputs transcribed from the dossier entries used by the
statistician lens (D-20, D-22, D-23, D-27-D-30); symmetric totals = stat (+) sys in quadrature."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy import optimize, stats
from stats_tools import weighted_mean, tension, sigma_to_p, p_to_sigma

q = lambda *a: math.sqrt(sum(x * x for x in a))
data = {  # name: (value s, sym error s, class)
    "BL1":    (887.7, q(1.2, 1.9), "pbeam"),
    "Sussex": (889.2, q(3.0, 3.8), "pbeam"),
    "SER05":  (878.5, q(0.7, 0.3), "material"),
    "PIC10":  (880.7, q(1.3, 1.2), "material"),
    "STE12":  (882.5, q(1.4, 1.5), "material"),
    "ARZ15":  (880.2, 1.2, "material"),
    "SER18":  (881.5, q(0.7, 0.6), "material"),
    "MUS25":  (877.82, 0.5 * (q(0.22, 0.20) + q(0.22, 0.17)), "magnetic"),
    "PAT18":  (877.7, 0.5 * (q(0.7, 0.4) + q(0.7, 0.2)), "magnetic"),
    "EZH18":  (878.3, q(1.6, 1.0), "magnetic"),
    "JPARC":  (877.2, 0.5 * (q(1.7, 4.0) + q(1.7, 3.6)), "ebeam"),
}
P = ["BL1", "Sussex"]
S = ["SER05", "PIC10", "STE12", "ARZ15", "SER18", "MUS25", "PAT18", "EZH18"]

def wm(names, shift=None):
    shift = shift or {}
    v = [data[n][0] - shift.get(n, 0.0) for n in names]
    e = [data[n][1] for n in names]
    return weighted_mean(v, e)

p0, s0 = wm(P), wm(S)
gap = p0["mean"] - s0["mean"]
sd_scaled = math.hypot(p0["error"], s0["error_scaled"])
sd_unscaled = math.hypot(p0["error"], s0["error"])
print("== 0. Reference ==")
print("p-beam %.3f +- %.3f s; storage %.3f +- %.3f (scaled %.3f, S=%.2f); gap %.3f s; sigma %.3f s (scaled) -> z %.2f"
      % (p0["mean"], p0["error"], s0["mean"], s0["error"], s0["error_scaled"], s0["scale_factor"], gap, sd_scaled, gap / sd_scaled))

print("\n== 1. Where does the gap live? Minimum-chi2 (most probable Gaussian) allocation ==")
# minimise sum (d_i/s_i)^2 s.t. mean shift(P) - mean shift(S) = gap -> each pole shifts in proportion to its variance
for lab, sS in [("storage unscaled", s0["error"]), ("storage S-scaled", s0["error_scaled"])]:
    fP = p0["error"] ** 2 / (p0["error"] ** 2 + sS ** 2)
    print("%-18s: proton-beam pole carries %.1f%% of the gap (%.2f s), storage %.1f%% (%.2f s)"
          % (lab, 100 * fP, fP * gap, 100 * (1 - fP), (1 - fP) * gap))
fP = p0["error"] ** 2 / (p0["error"] ** 2 + s0["error"] ** 2)
dP = fP * gap  # common shift of every proton-beam member (Lagrange solution: equal within pole)
print("  in that allocation BL1 and Sussex each shift %.2f s = %.2f sigma_BL1, %.2f sigma_Sussex; each storage result shifts %.3f s"
      % (dP, dP / data["BL1"][1], dP / data["Sussex"][1], (1 - fP) * gap))

print("\n== 2. 'None dominates' allocation: every result pulled k of its own sigma toward closing the gap ==")
cont = {}
for n in P:
    cont[n] = (data[n][1] ** -2 / sum(data[m][1] ** -2 for m in P)) * data[n][1]  # s of gap closed per unit k
for n in S:
    cont[n] = (data[n][1] ** -2 / sum(data[m][1] ** -2 for m in S)) * data[n][1]
tot = sum(cont.values())
for n in P + S:
    print("  %-7s closes %.3f s per unit k  (%.1f%% of the closure)" % (n, cont[n], 100 * cont[n] / tot))
cls = {}
for n in P + S:
    cls[data[n][2]] = cls.get(data[n][2], 0) + cont[n]
for c, v in cls.items():
    print("  class %-9s %.1f%%" % (c, 100 * v / tot))
for zt in (3, 2, 1):
    k = (gap - zt * sd_scaled) / tot
    print("  k needed for residual gap = %d sigma (sigma_gap held at %.2f s): k = %.2f; BL1 then shifts %.2f s" % (zt, sd_scaled, k, k * data["BL1"][1]))
print("  NOTE sign: in this allocation the material bottles must move UP (toward the beam), i.e. they read LOW;"
      " C7's shift table says material bottles read HIGH by +2 s")

print("\n== 3. C7's own shift-by-class (BL1 +3 to +6 s, material +2 s, magnetic 0; J-PARC not in either pole) ==")
for dB in (3.0, 4.5, 6.0):
    for dM in (0.0, 2.0):
        sh = {"BL1": dB}
        for n in ["SER05", "PIC10", "STE12", "ARZ15", "SER18"]:
            sh[n] = dM
        p1, s1 = wm(P, sh), wm(S, sh)
        # storage scale factor recomputed after the correction
        g1 = p1["mean"] - s1["mean"]
        sd1 = math.hypot(p1["error"], s1["error_scaled"])
        z1 = g1 / sd1
        explained = gap - g1
        print("  BL1 -%.1f s, material -%.1f s: p-beam %.2f, storage %.2f (S=%.2f), residual gap %.2f s = %.2f sigma (p2 %.1e); "
              "explained %.2f s of %.2f; BL1 correction = %.2f sigma_BL1 = %.1fx BL1 sys 1.9 s"
              % (dB, dM, p1["mean"], s1["mean"], s1["scale_factor"], g1, z1, sigma_to_p(z1, True), explained, gap,
                 dB / data["BL1"][1], dB / 1.9))
sh = {n: 2.0 for n in ["SER05", "PIC10", "STE12", "ARZ15", "SER18"]}
s2 = wm(S, sh)
print("  material -2 s alone moves the storage mean by %+.3f s -> gap changes by %+.3f s (wrong sign for closing it)"
      % (s2["mean"] - s0["mean"], -(s2["mean"] - s0["mean"])))
print("  J-PARC: not a member of either pole -> d(gap)/d(J-PARC) = 0 exactly")
# if the gap is taken as all-beam (BL1+Sussex+J-PARC) vs storage
Pall = P + ["JPARC"]
pa = wm(Pall)
wJ = data["JPARC"][1] ** -2 / sum(data[n][1] ** -2 for n in Pall)
print("  all-beam variant: beam mean %.2f s, J-PARC weight %.3f; J-PARC reading LOW by 5 s (true higher) would RAISE the beam mean by %.2f s (widen gap);"
      " J-PARC can close this variant's gap only by reading HIGH, i.e. in the direction opposite to its 877.2 s value relative to BL1"
      % (pa["mean"], wJ, 5 * wJ))

print("\n== 4. Heavy tails (Student-t, unit scale) robust location over the 10 pole results and all 11 ==")
def tfit(names, nu):
    x = np.array([data[n][0] for n in names]); s = np.array([data[n][1] for n in names])
    nll = lambda mu: -np.sum(stats.t.logpdf((x - mu) / s, nu) - np.log(s))
    r = optimize.minimize_scalar(nll, bounds=(870, 895), method="bounded")
    mu = r.x
    return mu, (x - mu) / s, nll(mu)
for nu in (2, 3, 4):
    mu, res, _ = tfit(P + S + ["JPARC"], nu)
    names = P + S + ["JPARC"]
    pulls = ", ".join("%s %+.2f" % (n, r) for n, r in zip(names, res))
    print("  nu=%d: mu = %.2f s; pulls: %s" % (nu, mu, pulls))
    # per-point tail probability
    big = [(n, r, 2 * stats.t.sf(abs(r), nu)) for n, r in zip(names, res) if abs(r) > 2]
    print("        |pull|>2: " + "; ".join("%s %.2f (p2=%.3f)" % b for b in big))

print("\n== 5. Concession: chi2 contributions against the one-value fit (all 11) ==")
allN = P + S + ["JPARC"]
w = wm(allN)
c2 = {n: ((data[n][0] - w["mean"]) / data[n][1]) ** 2 for n in allN}
T = sum(c2.values())
for n in sorted(c2, key=lambda k: -c2[k]):
    print("  %-7s %6.2f  (%.1f%%)" % (n, c2[n], 100 * c2[n] / T))
print("  total %.2f / %d dof (mean %.3f s)" % (T, len(allN) - 1, w["mean"]))
print("  proton-beam pair share of total chi2: %.1f%%" % (100 * (c2["BL1"] + c2["Sussex"]) / T))

print("\n== 6. Heavy-tail null: look-elsewhere over 11 results and the joint proton-pair excursion ==")
for nu in (2, 3, 4):
    mu, res, _ = tfit(P + S + ["JPARC"], nu)
    zB, zS = res[0], res[1]
    p1 = 2 * stats.t.sf(abs(zB), nu)
    pany = 1 - (1 - p1) ** 11
    joint = stats.t.sf(zB, nu) * stats.t.sf(zS, nu)
    # probability that, among 11, some pair of results are both high by >= these pulls (upper bound: C(11,2)*joint)
    print("  nu=%d: P(|t|>%.2f) one result %.3f; any of 11: %.3f; both proton results high (one-sided) %.2e; x C(11,2)=55 -> <= %.3f"
          % (nu, zB, p1, pany, joint, min(1, 55 * joint)))
