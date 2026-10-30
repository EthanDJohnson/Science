"""Decomposer lens: gap sizes, partition test (premise 2), required effect sizes,
fraction of gap closed by each candidate, and null-model error inflation.
Units: H0 in km/s/Mpc; magnitudes in mag; r_d in Mpc.
All inputs are dossier values (IDs given). Correlations through shared anchors
(NGC 4258) and shared SNe are NOT modelled here except by choosing a
minimal-overlap set; this is an approximation flagged in the analysis.
"""
import math
from itertools import combinations

def sym(up, lo):
    return 0.5 * (abs(up) + abs(lo))

def tot(*e):
    return math.sqrt(sum(x * x for x in e))

def wmean(items):
    w = [1 / s ** 2 for _, s in items]
    m = sum(v * wi for (v, _), wi in zip(items, w)) / sum(w)
    return m, 1 / math.sqrt(sum(w))

def chi2_about(items, m):
    return sum(((v - m) / s) ** 2 for v, s in items)

def pval_chi2(x, k):
    # survival function of chi2 with k dof via regularized gamma (series/cont. fraction)
    a = k / 2.0; xx = x / 2.0
    if xx <= 0:
        return 1.0
    if xx < a + 1:
        s = 1 / a; t = s; n = a
        for _ in range(500):
            n += 1; t *= xx / n; s += t
        P = s * math.exp(-xx + a * math.log(xx) - math.lgamma(a))
        return 1 - P
    b = xx + 1 - a; c = 1e300; d = 1 / b; h = d
    for i in range(1, 500):
        an = -i * (i - a); b += 2
        d = an * d + b; d = 1e-300 if abs(d) < 1e-300 else d
        c = b + an / c; c = 1e-300 if abs(c) < 1e-300 else c
        d = 1 / d; h *= d * c
    return h * math.exp(-xx + a * math.log(xx) - math.lgamma(a))

def sigma_from_p(p):
    # two-sided Gaussian equivalent
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

print("=== 1. Gap sizes (km/s/Mpc, %, mag in 5 log10 H0) ===")
loc = {
    "SH0ES Riess2025 Ceph HST+JWST [D-20]": (73.49, 0.93),
    "H0DN corrected [D-22]": (73.264, 0.806),
    "CCHP TRGB [D-24]": (70.39, tot(1.22, 1.33, 0.70)),
    "CCHP JWST-only TRGB [D-25]": (68.81, tot(1.79, 1.32)),
}
early = {
    "CMB-SPA [D-44]": (67.19, 0.38),
    "Planck PR4 [D-41]": (67.64, 0.52),
    "DESI DR2 BAO+BBN [D-45]": (68.50, 0.58),
}
for ln, (lv, ls) in loc.items():
    for en, (ev, es) in early.items():
        d = lv - ev; s = tot(ls, es)
        print(f"{ln:38s} - {en:24s}: dH0={d:+.2f} +- {s:.2f} ({d/s:.2f} sigma uncorrelated), "
              f"{100*d/ev:.2f}%, dmag={5*math.log10(lv/ev):.3f} mag")

print("\n=== 2. Partition test (premise 2) on a minimal-overlap set ===")
# Minimal-overlap set: one entry per method class. Excludes H0DN (combination of
# SH0ES/TRGB/SBF/masers), inverse ladder (r_d from CMB, SNe shared), Tully-Fisher
# (calibrated through same hosts), Li/Hoyt/JAGB variants (same data).
data = {
    "SH0ES": (73.49, 0.93, "cephSN"),                     # D-20
    "CCHP_TRGB": (70.39, tot(1.22, 1.33, 0.70), "trgbSN"),  # D-24
    "SBF": (73.8, tot(0.7, 2.3), "nonSN"),               # D-29
    "TDCOSMO": (71.1, sym(2.4, 2.3), "onestep"),          # D-31
    "Masers": (71.6, 3.7, "onestep"),                     # D-32 (stat only)
    "Sirens": (71.7, sym(9.4, 7.5), "onestep"),           # D-33
    "CMB_SPA": (67.19, 0.38, "rs"),                       # D-44
    "BAO_BBN": (68.50, 0.58, "rs"),                       # D-45 (shares nothing with CMB-SPA except physics)
    "BAO_rsfree": (69.6, sym(1.3, 1.8), "nors_early"),     # D-49 (Zaborowski, lensing+DESY5 SNe)
    "Equality": (65.1, sym(3.0, 5.4), "nors_early"),       # D-50
}
names = list(data)
items_all = [(data[n][0], data[n][1]) for n in names]
m0, s0 = wmean(items_all)
c0 = chi2_about(items_all, m0)
k0 = len(items_all) - 1
print(f"One common H0: mean={m0:.2f} +- {s0:.2f}; chi2={c0:.2f} for {k0} dof; p={pval_chi2(c0,k0):.2e} "
      f"(~{sigma_from_p(pval_chi2(c0,k0)):.2f} sigma)")

partitions = {
    "P1 early(all CMB/BAO/equality/rs-free) vs local(all ladders+one-step)":
        lambda n: data[n][2] in ("rs", "nors_early"),
    "P2 r_s-using (CMB, BAO+BBN) vs everything not using r_s":
        lambda n: data[n][2] == "rs",
    "P3 SH0ES Cepheid-SN vs everything else":
        lambda n: n == "SH0ES",
    "P4 all distance ladders (SH0ES, CCHP, SBF) vs everything else":
        lambda n: data[n][2] in ("cephSN", "trgbSN", "nonSN"),
    "P5 SH0ES+SBF (high ladders) vs everything else":
        lambda n: n in ("SH0ES", "SBF"),
}
results = []
for pname, f in partitions.items():
    A = [(data[n][0], data[n][1]) for n in names if f(n)]
    B = [(data[n][0], data[n][1]) for n in names if not f(n)]
    mA, sA = wmean(A); mB, sB = wmean(B)
    cA = chi2_about(A, mA); cB = chi2_about(B, mB)
    ctot = cA + cB; k = len(names) - 2
    dchi = c0 - ctot
    sig_split = abs(mA - mB) / tot(sA, sB)
    results.append((ctot, pname))
    print(f"{pname}\n   group A mean {mA:.2f}+-{sA:.2f} (chi2 {cA:.2f}/{len(A)-1}), "
          f"group B mean {mB:.2f}+-{sB:.2f} (chi2 {cB:.2f}/{len(B)-1}); total chi2={ctot:.2f}/{k} "
          f"p={pval_chi2(ctot,k):.3f}; delta-chi2 vs one-mean={dchi:.2f}; A-B split {sig_split:.2f} sigma")
print("Ranking by residual chi2 (lower = better 2-group description, same parameter count):")
for c, p in sorted(results):
    print(f"   {c:6.2f}  {p}")

# exhaustive best 2-group split (all 2^(n-1)-1 splits) to see what the data alone pick
best = []
for r in range(1, len(names)):
    for A_names in combinations(names, r):
        if names[0] not in A_names:
            continue  # avoid double counting
        B_names = [n for n in names if n not in A_names]
        if not B_names:
            continue
        A = [(data[n][0], data[n][1]) for n in A_names]
        B = [(data[n][0], data[n][1]) for n in B_names]
        c = chi2_about(A, wmean(A)[0]) + chi2_about(B, wmean(B)[0])
        best.append((c, A_names))
best.sort()
print("Best five unrestricted 2-group splits (group containing SH0ES listed):")
for c, A_names in best[:5]:
    print(f"   chi2={c:.2f}  {{{', '.join(A_names)}}} vs rest")

print("\n=== 3. Tension without each block (load-bearing test) ===")
def block(nlist):
    return wmean([(data[n][0], data[n][1]) for n in nlist])
sets = {
    "one-step only (TDCOSMO, masers, sirens)": ["TDCOSMO", "Masers", "Sirens"],
    "all local except SH0ES": ["CCHP_TRGB", "SBF", "TDCOSMO", "Masers", "Sirens"],
    "all local except any SN ladder (SBF + one-step)": ["SBF", "TDCOSMO", "Masers", "Sirens"],
    "all local": ["SH0ES", "CCHP_TRGB", "SBF", "TDCOSMO", "Masers", "Sirens"],
}
ref = [("CMB-SPA", 67.19, 0.38), ("BAO+BBN", 68.50, 0.58)]
for sname, nl in sets.items():
    m, s = block(nl)
    out = ", ".join(f"vs {r}: {(m-rv)/tot(s,rs):.2f} sigma" for r, rv, rs in ref)
    print(f"{sname:48s}: {m:.2f} +- {s:.2f}; {out}")

print("\n=== 4. Required effect size vs published levers (mag, % H0) ===")
gap_mag = 5 * math.log10(73.264 / 67.19)
gap_pct = 100 * (73.264 / 67.19 - 1)
print(f"Gap to explain (H0DN corrected vs CMB-SPA): {gap_mag:.3f} mag = {gap_pct:.2f}% in H0")
levers = [
    ("JWST-HST Cepheid photometry bound [D-09,D-78] |-0.01 +- 0.03| 2-sigma upper", 0.01 + 2 * 0.03),
    ("Cepheid reddening total correction [D-15]", 0.03),
    ("Drop Cepheid metallicity term: H0DN 73.50->73.080 [D-23]", 5 * math.log10(73.50 / 73.080)),
    ("Efstathiou 2020 needed P-L intercept bias (upper) [D-79b]", 0.15),
    ("Wojtak-Hjorth 2025 SN two-population (73.49->70.59) [D-35]", 5 * math.log10(73.49 / 70.59)),
    ("Percival 2026 selection sum -2.6 km/s/Mpc on 73.49 [D-88]", 5 * math.log10(73.49 / (73.49 - 2.6))),
    ("Dong 2026 PV, forward 74.30->71.37 [D-82]", 5 * math.log10(74.30 / 71.37)),
    ("MW parallax residual offset ~0.9% distance [D-86] (if whole ladder; MW is 1 of 3-4 anchors)", 5 * math.log10(1.009)),
    ("LCDM cosmic variance 1 sigma 0.31 km/s/Mpc [D-10]", 5 * math.log10((67.19 + 0.31) / 67.19)),
]
for n, v in levers:
    print(f"   {n:95s}: {v:.3f} mag = {100*v/gap_mag:5.1f}% of gap")
print(f"   cosmic variance: gap/sigma_CV = {(73.264-67.19)/0.31:.1f} sigma")

print("\n=== 5. Fraction of the gap closed by new-physics fits WITHOUT a SH0ES prior ===")
lo, hi = 67.19, 73.264  # reference CMB-SPA LCDM -> H0DN
models = [
    ("ACT DR6 EDE P-ACT-LB 69.9 [D-52] (vs its own LCDM 68.2)", 69.9, 68.2),
    ("ACT DR6 PMF 69.1 [D-52]", 69.1, 68.2),
    ("ACT DR6 modified recombination 69.6 [D-52]", 69.6, 68.2),
    ("Planck NPIPE EDE 95% upper 69.5 [D-53]", 69.5, 67.64),
    ("Poulin 2026 EDE profile 71.0 [D-53]", 71.0, 68.2),
    ("eROSITA+ EDE 71.4 [D-94]", 71.4, 68.2),
    ("electron-density fluct. ACT+SPT 69.3 (with ladder prior!) [D-95]", 69.3, 68.2),
    ("DESI DR2 w0wa DESI+CMB 63.6 [D-51]", 63.6, 68.17),
    ("DESI DR2 w0wa DESI+CMB+Pantheon+ 67.51 [D-51]", 67.51, 68.17),
]
for n, h, own in models:
    f_ref = (h - lo) / (hi - lo)
    f_own = (h - own) / (hi - own)
    resid = (hi - h)
    print(f"   {n:66s}: closes {100*f_ref:6.1f}% of 67.19->73.26 gap; {100*f_own:6.1f}% relative to its own LCDM ({own}); residual {resid:.2f} km/s/Mpc")

print("\n=== 6. Null model: error inflation needed ===")
d = 73.264 - 67.19
for target in (3.0, 2.0):
    need = d / target
    s_loc = math.sqrt(max(need ** 2 - 0.38 ** 2, 0))
    print(f"   H0DN vs CMB-SPA to {target} sigma: total sigma {need:.2f}; ladder sigma {s_loc:.2f} = x{s_loc/0.806:.2f} of quoted 0.806")
# one-mean chi2 in minimal set with ladder errors inflated by factor s
for s in (1.0, 1.5, 2.0, 2.5, 3.0):
    it = []
    for n in names:
        v, e, cls = data[n]
        if cls in ("cephSN", "trgbSN", "nonSN"):
            e *= s
        it.append((v, e))
    m, _ = wmean(it); c = chi2_about(it, m)
    print(f"   ladder errors x{s}: one-mean {m:.2f}, chi2={c:.2f}/{k0}, p={pval_chi2(c,k0):.3f}")
for s in (1.0, 1.5, 2.0, 3.0):
    it = []
    for n in names:
        v, e, cls = data[n]
        if cls in ("rs",):
            e *= s
        it.append((v, e))
    m, _ = wmean(it); c = chi2_about(it, m)
    print(f"   early (CMB, BAO+BBN) errors x{s}: one-mean {m:.2f}, chi2={c:.2f}/{k0}, p={pval_chi2(c,k0):.3f}")

print("\n=== 7. Reframe arithmetic: r_d and M_B ===")
for hrd_label, hrd in (("CMB-SPA H0*r_d = 67.19*147.00/100", 67.19 * 147.00 / 100), ("DESI DR2 h*r_d [D-45]", 101.54)):
    for H in (73.264, 70.39):
        rd = hrd / (H / 100)
        print(f"   {hrd_label} = {hrd:.2f} Mpc: r_d needed for H0={H}: {rd:.1f} Mpc ({100*(1-rd/147.00):.2f}% below 147.00)")
print(f"   M_B ladder(R22) - inverse-ladder(flat LCDM, DES-SN5YR) = {-19.253 - (-19.394):.3f} mag; cosmography {-19.253 - (-19.375):.3f} mag (different SN systems; indicative only) [D-21]")
print(f"   gap in 5log10H0, SH0ES 73.49 vs CMB-SPA: {5*math.log10(73.49/67.19):.3f} mag")
