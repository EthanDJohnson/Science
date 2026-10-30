"""Decomposer lens, part 2.
(a) Sensitivity of the partition test (F2) to a shared ladder systematic:
    a common offset (NGC 4258 anchor / shared SN zero point) correlated across
    SH0ES, CCHP TRGB and SBF, modelled as a covariance term c_i c_j sigma_c^2.
(b) Precision a single one-step (ladder-free, r_s-free) H0 needs to separate
    the candidate predictions at 3 and 5 sigma.
Units: H0 in km/s/Mpc.
"""
import numpy as np
from itertools import combinations

def sym(a, b):
    return 0.5 * (abs(a) + abs(b))

names = ["SH0ES", "CCHP_TRGB", "SBF", "TDCOSMO", "Masers", "Sirens",
         "CMB_SPA", "BAO_BBN", "BAO_rsfree", "Equality"]
val = np.array([73.49, 70.39, 73.8, 71.1, 71.6, 71.7, 67.19, 68.50, 69.6, 65.1])
sig = np.array([0.93, np.sqrt(1.22**2 + 1.33**2 + 0.70**2), np.sqrt(0.7**2 + 2.3**2),
                sym(2.4, 2.3), 3.7, sym(9.4, 7.5), 0.38, 0.58, sym(1.3, 1.8), sym(3.0, 5.4)])
ladder = np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0], dtype=float)

def gls_chi2(groups, C):
    # groups: list of index lists; fit one mean per group with full covariance
    n = len(val)
    X = np.zeros((n, len(groups)))
    for g, idx in enumerate(groups):
        X[idx, g] = 1.0
    Ci = np.linalg.inv(C)
    A = X.T @ Ci @ X
    b = X.T @ Ci @ val
    m = np.linalg.solve(A, b)
    r = val - X @ m
    return float(r @ Ci @ r), m, np.sqrt(np.diag(np.linalg.inv(A)))

idx = {n: i for i, n in enumerate(names)}
parts = {
    "one mean": [list(range(10))],
    "P1 local vs early-type": [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9]],
    "P4 ladders vs rest": [[0, 1, 2], [3, 4, 5, 6, 7, 8, 9]],
    "P2 r_s-using vs rest": [[6, 7], [0, 1, 2, 3, 4, 5, 8, 9]],
    "P3 SH0ES vs rest": [[0], list(range(1, 10))],
}
print("=== (a) partition chi2 with a common ladder offset sigma_c (km/s/Mpc) ===")
for sc in (0.0, 0.5, 1.0, 1.5, 2.0):
    C = np.diag(sig**2) + sc**2 * np.outer(ladder, ladder)
    line = []
    for p, g in parts.items():
        c, m, e = gls_chi2(g, C)
        line.append(f"{p}: {c:.2f}")
    # tension local vs early with this covariance
    c1, m1, e1 = gls_chi2(parts["P1 local vs early-type"], C)
    c0, _, _ = gls_chi2(parts["one mean"], C)
    print(f"sigma_c={sc:.1f}: " + "; ".join(line))
    print(f"      P1 means local {m1[0]:.2f}+-{e1[0]:.2f}, early {m1[1]:.2f}+-{e1[1]:.2f}; "
          f"local-early = {(m1[0]-m1[1])/np.hypot(e1[0],e1[1]):.2f} sigma; delta-chi2(one mean - P1) = {c0-c1:.2f}")

print("\n=== (b) one-step H0 precision needed to separate candidate predictions ===")
# Predicted true (global) H0 that a ladder-free, r_s-free one-step method would see
preds = {
    "ladder systematic / M_B-G_eff transition / null-ladder (true = CMB-SPA LCDM)": 67.19,
    "true = BAO+BBN LCDM": 68.50,
    "early new physics, best surviving fit (Poulin 2026 EDE)": 71.0,
    "early new physics, eROSITA+ EDE": 71.4,
    "early new physics closing whole gap (true = ladder)": 73.264,
}
pairs = [
    ("ladder systematic / M_B-G_eff transition / null-ladder (true = CMB-SPA LCDM)", "early new physics closing whole gap (true = ladder)"),
    ("ladder systematic / M_B-G_eff transition / null-ladder (true = CMB-SPA LCDM)", "early new physics, best surviving fit (Poulin 2026 EDE)"),
    ("true = BAO+BBN LCDM", "early new physics, best surviving fit (Poulin 2026 EDE)"),
    ("early new physics, best surviving fit (Poulin 2026 EDE)", "early new physics closing whole gap (true = ladder)"),
]
for a, b in pairs:
    d = abs(preds[a] - preds[b])
    for ns in (3, 5):
        s = d / ns
        print(f"{a[:40]:40s} vs {b[:40]:40s}: dH0={d:.2f}; {ns} sigma needs sigma(H0) <= {s:.2f} km/s/Mpc = {100*s/70:.2f}% of 70")
# time-delay lens count scaling from TDCOSMO-2026: 3.3% with 11 lenses (D-31); naive 1/sqrt(N) (ignores MSD floor)
for target in (2.0, 1.5, 1.0):
    N = 11 * (3.3 / target) ** 2
    print(f"time delays: naive N lenses for {target}% = {N:.0f} (from 3.3% with 11; ignores systematic floor)")
# sirens: GWTC-5.0 ~ (9.4+7.5)/2/71.7 = 11.8% with 236 sources incl. GW170817
f5 = sym(9.4, 7.5) / 71.7 * 100
for target in (3.0, 2.0, 1.0):
    print(f"sirens: naive scale-up factor in information for {target}% = {(f5/target)**2:.0f}x GWTC-5.0 (from {f5:.1f}%)")
