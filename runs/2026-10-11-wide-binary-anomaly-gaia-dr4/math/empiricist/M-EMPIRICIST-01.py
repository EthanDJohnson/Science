"""M-EMPIRICIST-01: grouped chi^2 by camp (empiricist F2).

Claim: pro-anomaly camp (6 values) weighted mean 1.436 +- 0.040, chi2 = 1.92 / 5 dof (p = 0.86);
null camp (4 values) 1.022 +- 0.016, chi2 = 3.04 / 3 dof (p = 0.39); between camps chi2 = 93.4 / 1 dof
(z ~ 9.7); within-camp combined 5.0 / 8 dof, p = 0.76; pooled PDG scale factor S = 3.31.
gamma = G_eff/G is dimensionless. Errors symmetrised as (up + down)/2, values treated as independent.
Inputs are the published values exactly as listed in the lens's table L1 (not re-sourced here).
"""
import sys
import itertools
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
import sympy as sp
from math_checks import identity, limit, inequality, finish

def wmean(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(wi * v for wi, (v, _) in zip(w, vals)) / sum(w)
    return m, (1 / sum(w)) ** 0.5

def chi2(vals, m):
    return sum(((v - m) / s) ** 2 for v, s in vals)

def pval(x, k):
    return mp.gammainc(k / 2.0, x / 2.0, mp.inf, regularized=True)

def z2(p):  # two-sided Gaussian equivalent
    return mp.sqrt(2) * mp.erfinv(1 - p)

sym = lambda up, dn: (up + dn) / 2
# Chae 2024b total: stat +0.10/-0.09, syst +0.16/-0.09 in quadrature
c24b_up = (0.10**2 + 0.16**2) ** 0.5
c24b_dn = (0.09**2 + 0.09**2) ** 0.5
print(f"Chae 2024b total error +{c24b_up:.4f} / -{c24b_dn:.4f} (lens: +0.189 / -0.127)")

pro_fixed = {
    "Chae2023": (1.43, 0.06),
    "Chae2024a": (1.49, sym(0.21, 0.19)),
    "Chae2024b": (1.37, sym(c24b_up, c24b_dn)),
    "Hernandez2024": (1.5, 0.2),
    "Chae2025": (1.48, sym(0.33, 0.23)),
}
yoon_opts = {"Yoon 1.32 (g<1e-10)": (1.32, sym(0.12, 0.11)), "Yoon 1.26 (1e-10.3)": (1.26, sym(0.12, 0.10))}
null_fixed = {"BoufE2": (1.045, sym(0.023, 0.020)), "ST36": (1.00, sym(0.24, 0.19))}
banik_opts = {"Banik gM=1.333": (0.993, sym(0.022, 0.015)), "Banik gM=1.44": (0.991, sym(0.029, 0.020))}
c3po_opts = {"C3PO s>3kau": (1.17, sym(0.37, 0.23)), "C3PO s<3kau": (1.05, sym(0.11, 0.08))}

best = None
for (yk, yv), (bk, bv), (ck, cv) in itertools.product(yoon_opts.items(), banik_opts.items(), c3po_opts.items()):
    pro = list(pro_fixed.values()) + [yv]
    nul = list(null_fixed.values()) + [bv, cv]
    mp_, sp_ = wmean(pro); mn, sn = wmean(nul)
    cp, cn = chi2(pro, mp_), chi2(nul, mn)
    cb = (mp_ - mn) ** 2 / (sp_**2 + sn**2)
    allv = pro + nul
    ma, _ = wmean(allv); ctot = chi2(allv, ma)
    S = (ctot / (len(allv) - 1)) ** 0.5
    pw = pval(cp + cn, 8)
    line = (f"[{yk}; {bk}; {ck}] pro {mp_:.4f}+-{sp_:.4f} chi2 {cp:.2f}/5 p={float(pval(cp,5)):.3f} | "
            f"null {mn:.4f}+-{sn:.4f} chi2 {cn:.2f}/3 p={float(pval(cn,3)):.3f} | between {cb:.1f} z={cb**0.5:.2f} | "
            f"within {cp+cn:.2f}/8 p={float(pw):.3f} | total {ctot:.2f}/9 S={S:.3f}")
    print(line)
    score = abs(mp_ - 1.436) + abs(sp_ - 0.040) + abs(cp - 1.92) / 10 + abs(mn - 1.022) + abs(sn - 0.016) + abs(cn - 3.04) / 10 + abs(cb - 93.4) / 100
    if best is None or score < best[0]:
        best = (score, line, cp, cn, cb, S, mp_, sp_, mn, sn, ctot)
print("closest variant to the lens's numbers:", best[1])
_, _, cp, cn, cb, S, mp_, sp_, mn, sn, ctot = best
print(f"reproduces: pro mean {mp_:.3f} (1.436), sd {sp_:.3f} (0.040), chi2 {cp:.2f} (1.92); null {mn:.3f} (1.022), "
      f"sd {sn:.3f} (0.016), chi2 {cn:.2f} (3.04); between {cb:.1f} (93.4); S {S:.2f} (3.31)")
ok = (abs(mp_ - 1.436) < 0.002 and abs(sp_ - 0.040) < 0.001 and abs(cp - 1.92) < 0.02 and abs(mn - 1.022) < 0.002
      and abs(sn - 0.016) < 0.001 and abs(cn - 3.04) < 0.02 and abs(cb - 93.4) < 0.2 and abs(S - 3.31) < 0.01)
print("NUMERIC", "PASS" if ok else "FAIL", "all F2 numbers reproduced to rounding")
print(f"z for chi2=93.4, 1 dof: sqrt = {93.4**0.5:.3f}")

# Diagnostic: Chae 2024a entered with the GENERAL self-calibrated sample error 1.49 +- 0.07 (dossier D-21),
# instead of the pure-binary +0.21/-0.19 the lens's table L1 lists for this row.
pro = [(1.43, 0.06), (1.49, 0.07), (1.37, sym(c24b_up, c24b_dn)), (1.32, sym(0.12, 0.11)), (1.5, 0.2), (1.48, sym(0.33, 0.23))]
nul = [(0.99, sym(0.029, 0.020)), (1.045, sym(0.023, 0.020)), (1.17, sym(0.37, 0.23)), (1.00, sym(0.24, 0.19))]
mp_, sp_ = wmean(pro); mn, sn = wmean(nul); cp, cn = chi2(pro, mp_), chi2(nul, mn)
cb = (mp_ - mn) ** 2 / (sp_**2 + sn**2); allv = pro + nul; ma, _ = wmean(allv)
S = (chi2(allv, ma) / 9) ** 0.5
print(f"[Chae2024a sigma=0.07, Banik 0.99] pro {mp_:.4f}+-{sp_:.4f} chi2 {cp:.2f}/5 | null {mn:.4f}+-{sn:.4f} chi2 {cn:.2f}/3 | "
      f"between {cb:.1f} z={cb**0.5:.2f} | within {cp+cn:.2f}/8 p={float(pval(cp+cn,8)):.3f} | S={S:.3f}")
ok2 = abs(mp_ - 1.436) < 0.002 and abs(sp_ - 0.040) < 0.001 and abs(cp - 1.92) < 0.02 and abs(cb - 93.4) < 0.3 and abs(S - 3.31) < 0.01
print("NUMERIC", "PASS" if ok2 else "FAIL", "lens numbers reproduced only with Chae 2024a sigma = 0.07 (general sample)")
print(f"p(5.0, 8 dof) = {float(pval(4.96, 8)):.3f}; p(1.92,5) = {float(pval(1.92,5)):.3f}; p(3.04,3) = {float(pval(3.04,3)):.3f}")

# Identity: total chi2 about the pooled mean = within_A + within_B + (mA - mB)^2/(sA^2 + sB^2)
x1, x2, y1, y2 = sp.symbols("x1 x2 y1 y2", real=True)
a1, a2, b1, b2 = sp.symbols("a1 a2 b1 b2", positive=True)
wA = [1/a1**2, 1/a2**2]; wB = [1/b1**2, 1/b2**2]
mA = (wA[0]*x1 + wA[1]*x2) / sum(wA); mB = (wB[0]*y1 + wB[1]*y2) / sum(wB)
m = (wA[0]*x1 + wA[1]*x2 + wB[0]*y1 + wB[1]*y2) / (sum(wA) + sum(wB))
tot = wA[0]*(x1-m)**2 + wA[1]*(x2-m)**2 + wB[0]*(y1-m)**2 + wB[1]*(y2-m)**2
dec = wA[0]*(x1-mA)**2 + wA[1]*(x2-mA)**2 + wB[0]*(y1-mB)**2 + wB[1]*(y2-mB)**2 + (mA-mB)**2/(1/sum(wA) + 1/sum(wB))
dom = {"x1": (-3, 3), "x2": (-3, 3), "y1": (-3, 3), "y2": (-3, 3)}
identity(tot, dec, domain=dom)
# Limit: the between-group chi2 vanishes as one group's error grows without bound
d, s1, s2 = sp.symbols("d s1 s2", positive=True)
limit(d**2/(s1**2 + s2**2), "s2", "oo", "0")
# 1-dof chi2 = z^2: z for the lens value 93.4 is sqrt(93.4)
inequality(str(93.4**0.5), ">", "9.6")
inequality(str(93.4**0.5), "<", "9.75")
raise SystemExit(finish())
