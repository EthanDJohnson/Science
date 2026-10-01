"""Falsifier C7, refuter 2 (angle: bounds).
Tests the null C7 ("a fluctuation plus several modestly underestimated uncertainties in BL1,
J-PARC and material bottles, none dominating, produce the gap") against the gap arithmetic and
the independent anchors it must satisfy (magnetic traps, J-PARC, SM tau_beta from lambda+Vud,
first-row unitarity). Units: lifetimes in s (SI); lambda, Vud dimensionless.
Inputs as in calc/lens-statistician_combination.py (dossier D-20..D-30) and the SM route values
verified in math/constraints.md (M-CONSTRAINTS-02/-04)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import weighted_mean, tension, sigma_to_p

def q(*a):
    return math.sqrt(sum(x * x for x in a))

BL1 = (887.7, q(1.2, 1.9)); SUS = (889.2, q(3.0, 3.8))
JP = (877.2, 0.5 * (q(1.7, 4.0) + q(1.7, 3.6)))
mat = {"SER05": (878.5, q(0.7, 0.3)), "PIC10": (880.7, q(1.3, 1.2)), "STE12": (882.5, q(1.4, 1.5)),
       "ARZ15": (880.2, 1.2), "SER18": (881.5, q(0.7, 0.6))}
mag = {"MUS25": (877.82, 0.5 * (q(0.22, 0.20) + q(0.22, 0.17))),
       "PAT18": (877.7, 0.5 * (q(0.7, 0.4) + q(0.7, 0.2))), "EZH18": (878.3, q(1.6, 1.0))}
TAU_A = (878.70, 0.83)   # SM tau_beta, A route (M-CONSTRAINTS-02 verified)
TAU_a = (887.21, 2.93)   # SM tau_beta, a route (aSPECT), same check

def wm(lst):
    return weighted_mean([v for v, _ in lst], [e for _, e in lst])

w = lambda e: 1.0 / e**2
pb = wm([BL1, SUS]); st = wm(list(mat.values()) + list(mag.values()))
S_st = st["scale_factor"]
Wp = w(BL1[1]) + w(SUS[1]); Ws = sum(w(e) for _, e in list(mat.values()) + list(mag.values()))
Wmat = sum(w(e) for _, e in mat.values()); Wmag = sum(w(e) for _, e in mag.values())
gap = pb["mean"] - st["mean"]; sgap = q(pb["error"], S_st * st["error"])
print("== 1. Reference gap (proton beam - all storage) ==")
print("proton beam %.3f +- %.3f s; storage %.3f +- %.3f s (S=%.3f); gap %.3f +- %.3f s, z=%.2f"
      % (pb["mean"], pb["error"], st["mean"], st["error"], S_st, gap, sgap, gap / sgap))

print("\n== 2. Linear response of the gap to a bias b (s) in each class ==")
d_BL1 = w(BL1[1]) / Wp; d_SUS = w(SUS[1]) / Wp
d_mat = -Wmat / Ws; d_mag = -Wmag / Ws; d_JP = 0.0
print("dGap/db: BL1 %+.3f, Sussex-ILL %+.3f, material (all 5, common bias) %+.3f, magnetic %+.3f, J-PARC %+.3f"
      % (d_BL1, d_SUS, d_mat, d_mag, d_JP))
print("=> a bias that makes material bottles read LONG reduces the gap; J-PARC is not an input to the gap at all.")

print("\n== 3. C7's own shift table applied (BL1 +3..+6 s, material +2 s, magnetic 0, J-PARC +-5 s) ==")
for bB in (3.0, 6.0):
    explained = d_BL1 * bB + d_mat * 2.0 + d_mag * 0.0 + d_JP * 5.0
    resid = gap - explained
    # residual must be a fluctuation; express in units of the gap's own quoted error
    print("BL1 bias %+.1f s, material +2 s: explained %+.2f s (BL1 %+.2f, material %+.2f, J-PARC %+.2f); "
          "residual %.2f s = %.2f sigma_gap (p1 %.2e)"
          % (bB, explained, d_BL1 * bB, d_mat * 2.0, d_JP * 5.0, resid, resid / sgap, sigma_to_p(resid / sgap)))
    print("   share of gap carried by the proton-counting side incl. its fluctuation: %.0f%%; by material/J-PARC: %.0f%%"
          % (100 * (gap - d_mat * 2.0) / gap, 100 * (d_mat * 2.0) / gap))

print("\n== 4. Independent anchors (exclude BL1, Sussex-ILL and material bottles) ==")
anc = wm(list(mag.values()) + [JP, TAU_A])
print("magnetic + J-PARC + SM A-route: %.3f +- %.3f s, chi2 %.2f/%d" % (anc["mean"], anc["error"], anc["chi2"], anc["dof"]))
anc2 = wm([JP, TAU_A])
print("J-PARC + SM A-route only (no storage at all): %.3f +- %.3f s" % (anc2["mean"], anc2["error"]))
for nm, (v, e) in [("BL1", BL1), ("Sussex-ILL", SUS), ("material mean", (wm(list(mat.values()))['mean'], wm(list(mat.values()))['error_scaled'])),
                   ("magnetic mean", (wm(list(mag.values()))['mean'], wm(list(mag.values()))['error'])), ("J-PARC", JP),
                   ("SM a-route", TAU_a)]:
    t = tension(v, e, anc["mean"], anc["error"])
    print("  %-14s offset from anchor %+6.2f s, %.2f sigma" % (nm, v - anc["mean"], t["z"]))
t = tension(BL1[0], BL1[1], anc2["mean"], anc2["error"])
print("  BL1 vs (J-PARC + SM A-route) only: %+.2f s, %.2f sigma" % (BL1[0] - anc2["mean"], t["z"]))

print("\n== 5. Does inflating J-PARC's error help? all-beam (BL1+Sussex+J-PARC) vs storage ==")
for S in (1.0, 2.295, 4.0):
    b = wm([BL1, SUS, (JP[0], JP[1] * S)])
    g = b["mean"] - st["mean"]; sg = q(b["error"], S_st * st["error"])
    print("J-PARC error x%.3f: beam mean %.2f +- %.2f s, gap %.2f s, z %.2f" % (S, b["mean"], b["error"], g, g / sg))

print("\n== 6. Same-sign structure under a uniform inflation S (C7's 'diffuse underestimation') ==")
# truth = anchor (C7 says magnetic ~ 0 shift). Proton-detecting results: BL1, Sussex-ILL, aSPECT a-route.
# Non-proton results: J-PARC. One-sided probabilities of each landing as high as observed.
for S in (1.0, 1.5, 2.0, 2.35):
    zs = [(BL1[0] - anc["mean"]) / (S * BL1[1]), (SUS[0] - anc["mean"]) / (S * SUS[1]),
          (TAU_a[0] - anc["mean"]) / (S * TAU_a[1])]
    ps = [sigma_to_p(z) for z in zs]
    print("S=%.2f: z(BL1,Sussex,a-route) = %.2f, %.2f, %.2f; one-sided p = %.2e, %.2e, %.2e; joint %.2e"
          % (S, *zs, *ps, ps[0] * ps[1] * ps[2]))

print("\n== 7. 'Either SM route' under C7's truth (magnetic ~ 0 => tau ~ anchor) ==")
tA = tension(TAU_A[0], TAU_A[1], anc["mean"], anc["error"]); ta = tension(TAU_a[0], TAU_a[1], anc["mean"], anc["error"])
print("A route vs anchor %.2f sigma; a route vs anchor %.2f sigma" % (tA["z"], ta["z"]))
print("=> if magnetic traps read true (C7), the a route cannot be right; C7 must add an aSPECT underestimate of")
print("   %.1f s-equivalent in tau_beta, same sign as BL1's excess." % (TAU_a[0] - anc["mean"]))
