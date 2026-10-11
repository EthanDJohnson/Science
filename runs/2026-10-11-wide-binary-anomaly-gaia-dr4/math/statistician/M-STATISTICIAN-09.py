"""M-STATISTICIAN-09: conditional DR4 predictive distributions (Table 3, finding 12, cand A).
Independent Monte Carlo of the model as the lens states it in prose (not its code):
gamma_DR4 = truth + offset + N(0, sigma_stat,DR4) + N(0, sigma_analyst); gamma dimensionless.
sigma_stat,DR4 = sigma_DR3/sqrt(k), k log-uniform [2,5] (F4: [1,3]).
Unstated distribution shapes are assumed uniform for '40-100%' and 'U(0.15,0.8)' as written."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, finish
from _h import report

rng = np.random.default_rng(11)
n = 2_000_000
N = lambda m, s: rng.normal(m, s, n)
U = lambda a, b: rng.uniform(a, b, n)
k25 = np.exp(U(np.log(2), np.log(5))); k13 = np.exp(U(0, np.log(3)))
stat = {"F1": 0.095 / np.sqrt(k25), "F2": 0.040 / np.sqrt(k25), "F3": 0.025 / np.sqrt(k25), "F4": 0.20 / np.sqrt(k13)}
an = {"F1": 0.05, "F2": 0.035, "F3": 0.035, "F4": 0.12}
noise = {f: rng.normal(0, 1, n) * stat[f] + N(0, an[f]) for f in stat}
T = N(1.32, 0.05)
chae = rng.random(n) < 0.65
sims = {
    ("F1", "Newton"): 1 + U(0.4, 1.0) * 0.33,
    ("F1", "MOND"): T * N(1.02, 0.04),
    ("F2", "Newton"): 1 + N(0.06, 0.03),
    ("F2", "MOND"): 1 + U(0.15, 0.8) * (T - 1),
    ("F3", "Newton"): 1 + N(0.02, 0.025),
    ("F3", "MOND"): 1 + U(0.15, 0.8) * (T - 1),
    ("F4", "Newton"): 1 + np.where(chae, N(0.35, 0.15), N(0.0, 0.05)),
    ("F4", "MOND"): T * np.where(chae, N(1.10, 0.10), N(0.85, 0.10)),
}
lens = {("F1", "Newton"): (1.231, 1.137, 1.325, 0.024, 0.421, 0.093), ("F1", "MOND"): (1.346, 1.243, 1.450, 0.002, 0.823, 0.104),
        ("F2", "Newton"): (1.060, 1.009, 1.111, 0.408, 0.000, 0.052), ("F2", "MOND"): (1.149, 1.072, 1.233, 0.091, 0.113, 0.077),
        ("F3", "Newton"): (1.020, 0.975, 1.065, 0.685, 0.000, 0.045), ("F3", "MOND"): (1.149, 1.073, 1.231, 0.084, 0.109, 0.076),
        ("F4", "Newton"): (1.223, 0.934, 1.522, 0.108, 0.465, 0.287), ("F4", "MOND"): (1.344, 1.044, 1.627, 0.070, 0.623, 0.289)}
ok = []
X = {}
for (f, h), base in sims.items():
    x = base + noise[f]
    X[(f, h)] = x
    q16, q50, q84 = np.percentile(x, [16, 50, 84])
    pin = np.mean((x >= 0.95) & (x <= 1.05)); phi = np.mean(x > 1.25); sd = x.std()
    L = lens[(f, h)]
    print(f"{f} {h:6s}: median {q50:.3f} [{q16:.3f}, {q84:.3f}] P[.95,1.05] {pin:.3f} P>1.25 {phi:.3f} sd {sd:.3f}")
    ok += [report(f"{f} {h} median", q50, L[0], 0.006), report(f"{f} {h} q16", q16, L[1], 0.008),
           report(f"{f} {h} q84", q84, L[2], 0.008), report(f"{f} {h} P in", pin, L[3], 0.01),
           report(f"{f} {h} P>1.25", phi, L[4], 0.01), report(f"{f} {h} sd", sd, L[5], 0.004)]


def dens(x, at, h=0.01):
    return np.mean(np.abs(x - at) < h) / (2 * h)


print("Likelihood ratio p(x|MOND)/p(x|Newton) at each conditional median:")
for f in ("F1", "F2", "F3", "F4"):
    xn, xm = X[(f, "Newton")], X[(f, "MOND")]
    lrs = [dens(xm, np.median(xn)) / dens(xn, np.median(xn)), dens(xm, np.median(xm)) / dens(xn, np.median(xm))]
    print(f"  {f}: at Newton median {lrs[0]:.3f}, at MOND median {lrs[1]:.3f}")
xn, xm = X[("F3", "Newton")], X[("F3", "MOND")]
pa = np.mean((xn >= 0.97) & (xn <= 1.07)); pb = np.mean((xm >= 0.97) & (xm <= 1.07))
ok += [report("cand A: P(F3 in [0.97,1.07] | Newton)", pa, 0.69, 0.02), report("cand A: same | MOND", pb, 0.08, 0.02)]
print("Illustrative mix P(Newton)=0.75:")
mixlens = {"F1": (1.256, 1.152, 1.367), "F2": (1.074, 1.017, 1.148), "F3": (1.037, 0.984, 1.125), "F4": (1.254, 0.956, 1.552)}
for f in ("F1", "F2", "F3", "F4"):
    pick = rng.random(n) < 0.75
    x = np.where(pick, X[(f, "Newton")], X[(f, "MOND")])
    q = np.percentile(x, [50, 16, 84])
    print(f"  {f}: {q[0]:.3f} [{q[1]:.3f}, {q[2]:.3f}]")
    ok += [report(f"mix {f} median", q[0], mixlens[f][0], 0.008), report(f"mix {f} q16", q[1], mixlens[f][1], 0.01),
           report(f"mix {f} q84", q[2], mixlens[f][2], 0.01)]
# analytic sd check F2 Newton: sqrt(0.03^2 + E[sigma_stat^2] + 0.035^2), E[1/k] for log-uniform [2,5] = (1/2-1/5)/ln(5/2)
a_, b_ = sp.symbols("a b", positive=True)
kk = sp.symbols("k", positive=True)
Einv = sp.integrate(1 / kk / (kk * sp.log(b_ / a_)), (kk, a_, b_))
identity(Einv, (1 / a_ - 1 / b_) / sp.log(b_ / a_), domain={"a": (1, 2), "b": (3, 6)})
sd_an = (0.03**2 + 0.04**2 * (0.5 - 0.2) / np.log(2.5) + 0.035**2) ** 0.5
ok.append(report("F2 Newton sd analytic", sd_an, 0.052, 0.002))
print("ALL NUMERIC CHECKS OK" if all(ok) else "SOME NUMERIC CHECK DIFFERS")
raise SystemExit(finish())
