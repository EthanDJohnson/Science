"""M-STATISTICIAN-08: sigma_stat DR3 -> DR4 (Table 2). gamma dimensionless.
sigma_DR4 = sigma_DR3/sqrt(k), k = N_DR4/N_DR3 log-uniform on [2,5] (F4: [1,3]); median of k = sqrt(lo*hi).
Also: Gaia proper-motion error scaling (T_DR3/T_DR4)^1.5 with T in months; Boufourou 0.005 at N ~ 1e5 to a 10% bin."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, finish
from _h import report

ok = []
for fam, s3, lo, hi, want in [("F1", 0.095, 2, 5, (0.053, 0.043, 0.067)), ("F2", 0.040, 2, 5, (0.023, 0.018, 0.028)),
                              ("F3", 0.025, 2, 5, (0.014, 0.011, 0.018)), ("F4", 0.20, 1, 3, (0.15, 0.12, 0.20))]:
    med = s3 / (lo * hi) ** 0.25
    ok += [report(f"{fam} median", med, want[0], 0.0015), report(f"{fam} low", s3 / hi**0.5, want[1], 0.0015),
           report(f"{fam} high", s3 / lo**0.5, want[2], 0.0015)]
f = (34 / 66) ** 1.5
print(f"  (34/66)^1.5 = {f:.4f}, improvement {1/f:.2f}x")
ok.append(report("PM improvement factor", 1 / f, 2.7, 0.02))
ok.append(report("scoring-bin sigma from 0.005 at 10% of pairs", 0.005 * 10**0.5, 0.0158, 0.0005))
# median of log-uniform k on [a,b] is sqrt(ab)
a, b = sp.symbols("a b", positive=True)
identity(sp.exp((sp.log(a) + sp.log(b)) / 2), sp.sqrt(a * b))
quantity("34*30.4375 day", "2.8333 yr", rel_tol=1e-3)
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
