"""M-STATISTICIAN-02: Sidak look-elsewhere correction (finding 2).
p_glob = 1 - (1 - p_loc)^N, two-sided normal p; N = number of effective trials (dimensionless)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import limit, series, inequality, finish
from _h import p2, z2, report
import sympy as sp
pp, NN = sp.symbols("p N", positive=True)

ok = []
for zloc, lens in [(3.21, [2.72, 2.48, 2.06]), (4.29, [3.9, 3.75, 3.5])]:
    p = p2(zloc)
    for N, want in zip([5, 10, 30], lens):
        g = 1 - (1 - p) ** N
        ok.append(report(f"z_loc {zloc} N={N}", z2(g), want, 0.06))
# small-p limit: Sidak -> Bonferroni N p
series(1-(1-pp)**NN, "p", 0, 2, NN*pp)
limit(1-(1-pp)**NN, "N", 1, pp, domain={"p": (0.001, 0.5)})
# global p >= local p for N >= 1
inequality(1-(1-pp)**NN, ">=", pp, domain={"p": (0.0001, 0.5), "N": (1, 50)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
