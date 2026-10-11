"""M-EMPIRICIST-07: base rate (F8, L3).

k = 0 new-physics resolutions in n = 8 resolved cases.
Laplace rule of succession (uniform Beta(1,1) prior): P = (k+1)/(n+2) = 0.100.
Jeffreys Beta(1/2,1/2) prior: posterior mean (k+1/2)/(n+1) = 0.0556.
Median time to resolution from the 'Years open' column of L3 (resolved rows only):
 proton radius 2010-2019, muon g-2 2021-2025, local DM 2012 (same year), omega Cen 2003 (same year),
 Triangulum II 2015-2017, Pioneer ~1998-2012, OPERA 2011-2012, Eotvos fifth force 1986-~1990.
 Same-year cases are given 0.1 yr (the lens's stated range starts at 0.1 yr). Claim: median ~4 yr, range 0.1-14 yr.
Cause tally: systematic 3, shared input 1, estimator/model 3, hidden binaries 1 (sum 8).
"""
import sys, statistics
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, finish

k, n = 0, 8
lap = (k + 1) / (n + 2); jef = (k + 0.5) / (n + 1)
print(f"Laplace {lap:.4f}; Jeffreys {jef:.4f}")
inequality(f"abs({lap} - 0.100)", "<", "1e-9")
inequality(f"abs({jef} - 0.056)", "<", "0.0005")
# Laplace rule = posterior mean of Beta(1,1) after k successes in n: integral check
p = sp.symbols("p", positive=True)
kk, nn = sp.symbols("kk nn", positive=True)
post_mean = sp.integrate(p * p**k * (1 - p)**(n - k), (p, 0, 1)) / sp.integrate(p**k * (1 - p)**(n - k), (p, 0, 1))
identity(post_mean, sp.Rational(1, 10))
post_mean_j = sp.integrate(p * p**(k - sp.Rational(1, 2)) * (1 - p)**(n - k - sp.Rational(1, 2)), (p, 0, 1)) / \
    sp.integrate(p**(k - sp.Rational(1, 2)) * (1 - p)**(n - k - sp.Rational(1, 2)), (p, 0, 1))
identity(post_mean_j, sp.Rational(1, 18))
limit("(kk + 1)/(nn + 2)", "nn", "oo", "0")   # with no successes the rate falls to 0 as n grows

dur = {"proton": 9, "muon g-2": 4, "local DM": 0.1, "omega Cen": 0.1, "Tri II": 2, "Pioneer": 14, "OPERA": 1, "Eotvos": 4}
med = statistics.median(dur.values())
print("durations (yr):", dur, "median", med, "range", min(dur.values()), "-", max(dur.values()))
# sensitivity: the median is the mean of the 4th and 5th of 8 sorted values; try plausible alternatives
alts = {"OPERA 0.5": dict(dur, OPERA=0.5), "Pioneer 2002-2012 (10)": dict(dur, Pioneer=10),
        "local DM 2012-2015 (3, to Moni Bidin 2015)": dict(dur, **{"local DM": 3}),
        "Eotvos 1986-1991 (5)": dict(dur, Eotvos=5)}
for kname, d in alts.items():
    print(f"  alt {kname}: median {statistics.median(d.values())}")
inequality(str(med), "<", "4")
print(f"tally: {3+1+3+1} causes for {n} resolved cases")
identity("3 + 1 + 3 + 1", "8")
raise SystemExit(finish())
