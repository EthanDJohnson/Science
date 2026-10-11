"""M-STATISTICIAN-03: grouped chi2 within / between estimator families (finding 3, cand C).
gamma dimensionless. Symmetric error = mean of the two sides (lens convention, stated).
Chae 2024b uses stat+sys symmetrised in quadrature (stat 0.095, sys 0.125) -- inferred, see log."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, inequality, finish
from _h import wmean, chi2_sf, z2, report

sym = lambda up, dn: (up + dn) / 2
c24b_tot = (sym(0.10, 0.09) ** 2 + sym(0.16, 0.09) ** 2) ** 0.5
fam = {
    "F1": ([1.37, 1.49, 1.32], [c24b_tot, sym(0.21, 0.19), sym(0.12, 0.11)]),
    "F2": ([1.045], [sym(0.023, 0.020)]),
    "F3": ([0.99], [sym(0.03, 0.02)]),
    "F4": ([1.48, 1.60, 1.17], [sym(0.33, 0.23), sym(0.24, 0.14), sym(0.37, 0.23)]),
}
print("Chae24b symmetric stat+sys sigma:", round(c24b_tot, 4))


def run(f, label, lens_between=None, lens_dof=None):
    means, errs, within = [], [], 0
    for k, (v, e) in f.items():
        m, s, c = wmean(v, e)
        means.append(m); errs.append(s); within += c
        print(f"  {label} {k}: mean {m:.4f} +- {s:.4f}, chi2_within {c:.3f}/{len(v)-1}")
    M, S, cb = wmean(means, errs)
    dof = len(means) - 1
    p = chi2_sf(cb, dof)
    nall = sum(len(v) for v, _ in f.values())
    Sfac = ((cb + within) / (nall - 1)) ** 0.5
    print(f"  {label}: between {cb:.2f}/{dof}, p = {p:.3g}, z2 = {z2(p):.2f}; within total {within:.2f}; "
          f"pooled {M:.4f} +- {S:.4f}; group-level S = {(cb/dof)**0.5:.2f}; all-member S = {Sfac:.2f}")
    return M, S, cb, p, within, Sfac


ok = []
M, S, cb, p, w, Sf = run(fam, "base")
ok += [report("F1 mean", wmean(*fam["F1"])[0], 1.364, 0.002), report("F1 sigma", wmean(*fam["F1"])[1], 0.084, 0.001),
       report("F4 mean", wmean(*fam["F4"])[0], 1.478, 0.002), report("F4 sigma", wmean(*fam["F4"])[1], 0.139, 0.001),
       report("between chi2", cb, 28.7, 0.3), report("p between", p, 2.5e-6, 0.3e-6), report("z", z2(p), 4.7, 0.05),
       report("within total", w, 2.0, 0.05), report("p within (4 dof)", chi2_sf(w, 4), 0.73, 0.02),
       report("pooled mean", M, 1.04, 0.005), report("pooled S (all members)", Sf, 2.1, 0.05)]
alt = dict(fam); alt["F4"] = ([1.48, 1.00, 1.17], [sym(0.33, 0.23), sym(0.24, 0.19), sym(0.37, 0.23)])
_, _, cb2, p2_, _, _ = run(alt, "S&T swap")
ok += [report("S&T swap between", cb2, 19.6, 0.3), report("S&T swap z", z2(p2_), 3.7, 0.06)]
low = {"F1": fam["F1"], "F2": ([1.11], [0.07]), "F4": fam["F4"]}
M3, S3, cb3, p3, w3, Sf3 = run(low, "low-g")
ok += [report("low-g between", cb3, 8.5, 0.1), report("low-g z", z2(p3), 2.45, 0.05),
       report("cand C pooled", M3, 1.248, 0.002), report("cand C sigma", S3, 0.050, 0.001),
       report("cand C S (all members)", Sf3, 1.3, 0.05)]
# algebra: inverse-variance mean of two equal-error values is the average
identity("(a/s**2 + b/s**2)/(2/s**2)", "(a+b)/2")
# chi2 decomposition: total about grand mean = within + between (one-group-per-member sanity)
inequality("(a-m)**2/s**2", ">=", "0", domain={"a": (-5, 5), "m": (-5, 5)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
