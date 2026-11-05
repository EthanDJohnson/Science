"""M-EXAMINER-05 and -06: pooled null and grouped chi2 partitions (F4, F5).
12 class representatives, symmetrised errors, independent. The lens does not list which r_s-free (D-49)
and equality (D-50) values it used, nor which inverse-ladder value; enumerate dossier options and keep
those consistent with the lens's P5 group values, then recompute every partition from the definitions:
  chi2_total = sum (x_i - mu)^2/s_i^2 about the pooled mean (N-1 dof)
  chi2_within = sum over groups of chi2 about each group mean (N - G dof)
  chi2_between = chi2_total - chi2_within (G - 1 dof); for G = 2 equal to z^2 with z = |m1-m2|/sqrt(s1^2+s2^2)."""
import sys, math, itertools
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from common import *
from math_checks import identity, quantity, finish

# algebraic identity: for two groups, chi2_between = (m1-m2)^2/(s1^2+s2^2) with s_k^2 = 1/W_k
W1, W2, m1, m2 = sp.symbols("W1 W2 m1 m2", positive=True)
mu = (W1 * m1 + W2 * m2) / (W1 + W2)
identity(W1 * (m1 - mu)**2 + W2 * (m2 - mu)**2, (m1 - m2)**2 / (1 / W1 + 1 / W2))

local = {"SH0ES": SH0ES, "CCHP": CCHP, "SBF": SBF, "TF": TF, "TD": TD, "MASER": MASER, "SIREN": SIREN}
rs = {"CMB": CMB, "BAOBBN": BAOBBN}
matches = []
for (ik, iv), (rk, rv), (ek, ev) in itertools.product({"cosmo": INVL_COSMO, "lcdm": INVL_LCDM}.items(), RSFREE.items(), EQ.items()):
    g_rs = [sym(CMB), sym(BAOBBN), sym(iv)]
    g_sw = [sym(TD), sym(MASER), sym(SIREN), sym(rv), sym(ev)]
    a = wmean(g_rs); b = wmean(g_sw)
    if abs(a[0] - 67.51) < 0.006 and abs(a[1] - 0.29) < 0.006 and abs(b[0] - 69.93) < 0.006 and abs(b[1] - 1.17) < 0.006:
        matches.append((ik, rk, ek))
print("representative choices reproducing P5 groups:", matches)
ik, rk, ek = matches[0]
D = {k: sym(v) for k, v in local.items()}
D.update({"CMB": sym(CMB), "BAOBBN": sym(BAOBBN), "INVL": sym({"cosmo": INVL_COSMO, "lcdm": INVL_LCDM}[ik]),
          "RSFREE": sym(RSFREE[rk]), "EQ": sym(EQ[ek])})
allk = list(D)
mu0, s0, chi0 = wmean([D[k] for k in allk])
p0 = chi2_sf(chi0, len(allk) - 1); S = math.sqrt(chi0 / (len(allk) - 1))
print(f"POOLED: {mu0:.3f} +- {s0:.3f}, chi2 {chi0:.3f}/{len(allk)-1}, p {p0:.4g}, S {S:.4f}")
quantity(f"{mu0}", "68.25", rel_tol=1e-4); quantity(f"{s0}", "0.26", rel_tol=2e-2)
quantity(f"{chi0}", "54.03", rel_tol=2e-4); quantity(f"{p0}", "1.17e-7", rel_tol=1e-2); quantity(f"{S}", "2.22", rel_tol=3e-3)

early = ["CMB", "BAOBBN", "INVL", "RSFREE", "EQ"]
parts = {"P1": [early, [k for k in allk if k not in early]],
         "P2": [["CMB", "BAOBBN", "INVL"], [k for k in allk if k not in ("CMB", "BAOBBN", "INVL")]],
         "P3": [["SH0ES"], [k for k in allk if k != "SH0ES"]],
         "P4": [["SH0ES", "CCHP", "SBF", "TF"], [k for k in allk if k not in ("SH0ES", "CCHP", "SBF", "TF")]],
         "P5": [["CMB", "BAOBBN", "INVL"], ["SH0ES", "CCHP", "SBF", "TF"], ["TD", "MASER", "SIREN", "RSFREE", "EQ"]]}
lens = {"P1": (6.73, 8.76, 0.555), "P2": (6.45, 12.40, 0.259), "P3": (5.87, 19.58, 0.034), "P4": (6.51, 11.64, 0.31), "P5": (6.50, 7.56, 0.579)}
for name, groups in parts.items():
    gs = [wmean([D[k] for k in g]) for g in groups]
    within = sum(g[2] for g in gs); dofw = len(allk) - len(groups)
    pw = chi2_sf(within, dofw); between = chi0 - within
    if len(groups) == 2:
        zb = abs(gs[0][0] - gs[1][0]) / math.hypot(gs[0][1], gs[1][1])
        print(f"{name}: z_between {zb:.3f} (z^2 {zb**2:.2f} vs chi2_tot - chi2_within {between:.2f}); within {within:.2f}/{dofw}, p {pw:.3f}")
    else:
        pb = chi2_sf(between, len(groups) - 1); zb = p_to_z(pb)
        print(f"{name}: groups " + "; ".join(f"{g[0]:.2f}+-{g[1]:.2f}" for g in gs) + f"; chi2_between {between:.2f}/2, p {pb:.3g}, z-equiv {zb:.3f}; within {within:.2f}/{dofw}, p {pw:.3f}")
        sw, rsg, lad = gs[2], gs[0], gs[1]
        print("  swing vs r_s:", (sw[0] - rsg[0]) / math.hypot(sw[1], rsg[1]), " ladder vs swing:", (lad[0] - sw[0]) / math.hypot(lad[1], sw[1]))
        quantity(f"{(sw[0] - rsg[0]) / math.hypot(sw[1], rsg[1])}", "2.0", rel_tol=2e-2)
        quantity(f"{(lad[0] - sw[0]) / math.hypot(lad[1], sw[1])}", "2.2", rel_tol=2e-2)
        quantity(f"{lad[0]}", "73.02", rel_tol=1e-4); quantity(f"{lad[1]}", "0.78", rel_tol=1e-2)
    zl, wl, pl = lens[name]
    quantity(f"{zb}", f"{zl}", rel_tol=3e-3); quantity(f"{within}", f"{wl}", rel_tol=2e-3); quantity(f"{pw}", f"{pl}", rel_tol=3e-2)
raise SystemExit(finish())
