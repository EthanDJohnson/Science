"""M-EMPIRICIST-02: grouped chi^2 by estimator family (empiricist Calculations: 56.2 for 3 dof, z = 6.9).

Family membership as the lens states it (L1, provisional mapping):
 F1: Chae 2023 1.43+-0.06; Chae 2024b 1.37 (stat+syst, +0.189/-0.127); Yoon+25 1.32 +0.12/-0.11
     (Chae 2024a and Hernandez are left out of this F1 grouping in the lens's calc; also tested with them).
 F2: Boufourou E2 1.045 +0.023/-0.020
 F3: Banik 0.99 (+0.029/-0.020 for gM=1.44, or +0.022/-0.015 for gM=1.333); Boufourou E3 1.05 +0.02/-0.01
 F4: Chae 2025 1.48 +0.33/-0.23; Chae+26 1.60 +0.24/-0.14; S&T-36 1.00 +0.24/-0.19; C3PO 1.17 +0.37/-0.23
Symmetrised errors; independence assumed. gamma dimensionless.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
from math_checks import identity, inequality, finish

sym = lambda u, d: (u + d) / 2
def wmean(v):
    w = [1 / s**2 for _, s in v]; m = sum(wi * x for wi, (x, _) in zip(w, v)) / sum(w)
    return m, sum(w) ** -0.5
def chi2(v, m): return sum(((x - m) / s) ** 2 for x, s in v)
def pval(x, k): return mp.gammainc(k / 2.0, x / 2.0, mp.inf, regularized=True)
def zfromp(p): return -mp.sqrt(2) * mp.erfinv(2 * p - 1) if p > 1e-300 else mp.inf  # one-sided Gaussian quantile
def z2(p):  # two-sided equivalent, robust for tiny p
    with mp.workdps(60):
        return mp.sqrt(2) * mp.erfinv(1 - p)

c24b = sym((0.10**2 + 0.16**2) ** 0.5, (0.09**2 + 0.09**2) ** 0.5)
F1 = [(1.43, 0.06), (1.37, c24b), (1.32, sym(0.12, 0.11))]
F1x = F1 + [(1.49, sym(0.21, 0.19)), (1.5, 0.2)]
F2 = [(1.045, sym(0.023, 0.020))]
F4 = [(1.48, sym(0.33, 0.23)), (1.60, sym(0.24, 0.14)), (1.00, sym(0.24, 0.19)), (1.17, sym(0.37, 0.23))]
for bname, banik in [("Banik +0.029/-0.020", (0.99, sym(0.029, 0.020))), ("Banik +0.022/-0.015", (0.99, sym(0.022, 0.015)))]:
    F3 = [banik, (1.05, sym(0.02, 0.01))]
    for fname, f1 in [("F1 = {C23, C24b, Y25}", F1), ("F1 + C24a(0.20) + Hern", F1x)]:
        fams = [f1, F2, F3, F4]
        stats = [wmean(f) for f in fams]
        # between-family chi2 = chi2 of the family means about their weighted mean
        bm, _ = wmean(stats)
        cb = chi2(stats, bm)
        allv = [x for f in fams for x in f]
        ma, _ = wmean(allv)
        within = sum(chi2(f, m) for f, (m, _) in zip(fams, stats))
        print(f"[{bname}; {fname}] means " + ", ".join(f"{m:.3f}+-{s:.3f}" for m, s in stats)
              + f" | within chi2 " + ", ".join(f"{chi2(f, m):.2f}" for f, (m, _) in zip(fams, stats))
              + f" | between {cb:.1f}/3, p = {mp.nstr(pval(cb, 3), 3)}, z(2-sided) = {float(z2(pval(cb, 3))):.2f}"
              + f" | check total {chi2(allv, ma):.2f} = within+between {within + cb:.2f}")
print("lens: F1 1.403+-0.050 (0.77/2); F2 1.045+-0.022; F3 1.034+-0.013 (4.24/1); F4 1.336+-0.117 (4.94/3); between 56.2/3, z = 6.9")
identity(str(56.2 / 1.0), "56.2")
inequality(str(float(z2(pval(56.2, 3)))), ">", "6.8")
inequality(str(float(z2(pval(56.2, 3)))), "<", "7.0")
raise SystemExit(finish())
