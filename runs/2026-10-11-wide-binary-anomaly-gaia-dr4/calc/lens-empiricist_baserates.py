"""Empiricist lens: (1) base-rate tally of how comparable disagreements ended; (2) scoring-bin
bookkeeping for published results; (3) alpha_grav -> gamma conversion sensitivity.
Units: accelerations in m s^-2 (SI); gamma dimensionless."""
import math

print("== 1. Reference class: claimed new physics / anomalies from disagreeing precision methods ==")
# (case, years open, outcome class)  outcome: 'one-method systematic', 'shared input', 'estimator/model',
# 'hidden binaries', 'unresolved', 'new physics'
cases = [
    ("Proton radius muH vs eH/ep (2010-2019)", 9, "one-method systematic"),
    ("Muon g-2 vs SM, HVP data-driven vs lattice (2021-2025)", 4, "shared input"),
    ("Local DM density, Moni Bidin vs Bovy&Tremaine (2012)", 0.3, "estimator/model"),
    ("omega Cen outskirts MOND flattening, Scarpa vs McLaughlin&Meylan (2003)", 0.1, "estimator/model"),
    ("Triangulum II dispersion inflated by binary (2015-2017)", 2, "hidden binaries"),
    ("Pioneer anomaly (1998-2012) thermal recoil", 14, "one-method systematic"),
    ("OPERA superluminal neutrinos (2011-2012)", 0.5, "one-method systematic"),
    ("Fifth force from Eotvos re-analysis (1986-~1990)", 4, "estimator/model"),
    ("Neutron lifetime beam vs bottle (2005-)", None, "unresolved"),
    ("Hubble tension, distance ladder vs CMB (2016-)", None, "unresolved"),
]
from collections import Counter
c = Counter(o for _, _, o in cases)
for k, v in c.items():
    print(f"  {k}: {v}")
resolved = [x for x in cases if x[2] != "unresolved"]
n_res = len(resolved)
n_np = sum(1 for x in resolved if x[2] == "new physics")
print(f"resolved = {n_res}, resolved as new physics = {n_np}")
print(f"Laplace rule-of-succession P(new physics | resolved) = {(n_np+1)/(n_res+2):.3f}")
print(f"Jeffreys-prior posterior mean = {(n_np+0.5)/(n_res+1):.3f}")
astro = [x for x in resolved if x[0].startswith(("Local DM", "omega Cen", "Triangulum"))]
print(f"astrophysical kinematic subset (estimator/model or hidden binaries): {len(astro)} of {len(astro)} non-new-physics")
yrs = sorted(x[1] for x in resolved)
print(f"time to resolution, years: median = {yrs[len(yrs)//2]:.1f}, range {yrs[0]}-{yrs[-1]}")

print()
print("== 2. Scoring-bin bookkeeping (brief: bin wholly below 10^-9.5 and containing 10^-10 m s^-2) ==")
a0 = 1.2e-10
lo, hi = 0.03 * a0, 0.3 * a0
print(f"Boufourou deep bin g_N/a0 in [0.03,0.3] -> g_N = {lo:.2e} to {hi:.2e} m s^-2;"
      f" log10 = {math.log10(lo):.2f} to {math.log10(hi):.2f}; centre {0.5*(math.log10(lo)+math.log10(hi)):.2f}"
      f"; contains -10? {math.log10(lo) <= -10 <= math.log10(hi)}")
for name, l, h in [("Chae 2025 MOND regime", -11.0, -9.5), ("Chae 2025 MOND+transition", -11.0, -8.5),
                   ("Chae+26 g_N<10^-9.5", -12.0, -9.5), ("Chae+26 g_N<10^-10.1", -12.0, -10.1),
                   ("YTC25 at 10^-10.3 bin (centre)", -10.3, -10.3), ("Chae 2023 x0=-10.15 (centre)", -10.15, -10.15)]:
    ok = (h <= -9.5) and (l <= -10 <= h)
    print(f"  {name}: [{l}, {h}] wholly<-9.5 & contains -10: {ok}")

print()
print("== 3. Banik+24 alpha_grav -> gamma under different gamma_MOND,paper ==")
alpha, up, dn = -0.021, 0.065, 0.045
for gm in (1.333, 1.37, 1.4228, 1.44):
    g = 1 + alpha * (gm - 1)
    print(f"  gamma_MOND={gm}: gamma = {g:.3f} +{up*(gm-1):.3f} -{dn*(gm-1):.3f}")
