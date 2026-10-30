"""M-CONSTRAINTS-14 (F15): inverse-variance combinations of non-Cepheid local probes (independent, symmetrised errors).
Inputs quoted from the dossier (km/s/Mpc): time delays 71.1 +2.4/-2.3 [D-31]; masers 71.6+-3.7 [D-32];
sirens 71.7 +9.4/-7.5 [D-33]; SBF 73.8 +-0.7(stat)+-2.3(sys) [D-29]; CCHP TRGB 70.39 +-1.22+-1.33+-0.70 [D-24].
Comparisons: CMB-SPA 67.19+-0.38, BAO+BBN 68.50+-0.58, H0DN 73.264+-0.806."""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import identity, finish
from _bg import near

TD = (71.1, (2.4 + 2.3) / 2); MA = (71.6, 3.7); GW = (71.7, (9.4 + 7.5) / 2)
SBF = (73.8, math.hypot(0.7, 2.3)); TRGB = (70.39, math.sqrt(1.22**2 + 1.33**2 + 0.70**2))

def comb(items):
    v = np.array([x[0] for x in items]); s = np.array([x[1] for x in items]); w = 1 / s**2
    m = (w * v).sum() / w.sum(); e = 1 / math.sqrt(w.sum()); chi2 = (w * (v - m) ** 2).sum()
    return m, e, chi2

def ns(a, b):
    return (a[0] - b[0]) / math.hypot(a[1], b[1])

SPA, BB, H0DN = (67.19, .38), (68.50, .58), (73.264, .806)
m, e, c2 = comb([TD, MA, GW]); print("one-step", m, e, c2)
near("mean", m, 71.27, 0.03); near("err", e, 1.93, 0.03); near("chi2", c2, 0.02, 0.02)
near("vs SPA", ns((m, e), SPA), 2.1, 0.06); near("vs H0DN", -ns((m, e), H0DN), 1.0, 0.06)
m, e, c2 = comb([TD, MA, GW, SBF]); print("+SBF", m, e, c2)
near("mean", m, 72.26, 0.03); near("err", e, 1.51, 0.03)
near("vs SPA", ns((m, e), SPA), 3.3, 0.06); near("vs BAO+BBN", ns((m, e), BB), 2.3, 0.06)
near("vs H0DN", -ns((m, e), H0DN), 0.6, 0.06)
m, e, c2 = comb([TD, MA, GW, SBF, TRGB]); print("+TRGB", m, e, c2)
near("mean", m, 71.56, 0.03); near("err", e, 1.19, 0.03); near("chi2", c2, 1.27, 0.03)
near("vs SPA", ns((m, e), SPA), 3.5, 0.06); near("vs H0DN", -ns((m, e), H0DN), 1.2, 0.06)
# identity: weighted mean of two equal-error values is their average
identity("(a/s**2 + b/s**2)/(2/s**2)", "(a+b)/2")
raise SystemExit(finish())
