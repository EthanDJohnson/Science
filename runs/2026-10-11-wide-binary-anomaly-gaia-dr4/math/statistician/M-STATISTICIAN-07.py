"""M-STATISTICIAN-07: what settles it (finding 8). gamma dimensionless.
z(k) = Delta / sqrt(sigma_stat^2/k + sigma_sys^2); k = data multiple. Ceiling as k -> oo is Delta/sigma_sys."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import limit, identity, finish
from _h import report

ok = []
ok += [report("5 sigma precision, Delta 0.33", 0.33 / 5, 0.066, 1e-4), report("Delta 0.42", 0.42 / 5, 0.084, 1e-4)]
ok.append(report("F1 z ceiling 0.37/0.125", 0.37 / 0.125, 2.96, 0.005))
st, sy, D = 0.095, 0.06, 0.37
k = st**2 / ((D / 5) ** 2 - sy**2)
ok.append(report("k for 5 sigma with sys 0.06", k, 4.8, 0.05))
print(f"  sys must be < Delta/5 = {D/5:.3f} for any finite k (lens: ~0.06 is 'below' with k = 4.8)")
# F4: sigma = 0.2 at 36 pairs; N for 5 sigma at Delta = 0.37
N = 36 * (5 * 0.2 / 0.37) ** 2
ok.append(report("F4 pairs for 5 sigma (Delta 0.37)", N, 260, 10))
for d in (0.33, 0.42, 0.60):
    print(f"  [sensitivity] F4 pairs at Delta={d}: {36*(5*0.2/d)**2:.0f}")
print(f"  F4 ceiling with model spread 0.3: Delta 0.33-0.42 -> {0.33/0.3:.2f}-{0.42/0.3:.2f} sigma")
kk, s1, s2, Dl = sp.symbols("k s1 s2 Delta", positive=True)
z = Dl / sp.sqrt(s1**2 / kk + s2**2)
limit(z, "k", sp.oo, Dl / s2)
limit(z.subs(s2, 0) / sp.sqrt(kk), "k", sp.oo, Dl / s1)   # stat-only scales as sqrt(k)
identity(sp.solve(sp.Eq(z, 5), kk)[0], s1**2 / (Dl**2 / 25 - s2**2), domain={"Delta": (1, 2), "s2": (0.01, 0.1)})
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
