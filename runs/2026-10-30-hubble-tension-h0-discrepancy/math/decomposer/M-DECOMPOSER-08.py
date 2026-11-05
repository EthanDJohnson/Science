"""M-DECOMPOSER-08: common ladder offset, GLS partition fit (F8).

Model: x = A mu + e, e ~ N(0, C), C = diag(s_i^2) + sigma_c^2 u u^T, u_i = 1 for SH0ES, CCHP, SBF.
Convention A ('added'): the term includes its diagonal (an extra error component).
Convention B ('off-diagonal'): only the off-diagonal part (the shared error already in quoted totals).
Two-group fit mu = (mu_local, mu_early) by GLS; z = |mu_L - mu_E| / sqrt(Var(mu_L - mu_E));
chi2 = r^T C^-1 r, 8 dof. Exhaustive search over all bipartitions at each sigma_c.
"""
import sys
import itertools
import numpy as np
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import TEN, LOCAL, num, finish, identity, units, inequality

names = list(TEN)
x = np.array([TEN[n][0] for n in names])
s = np.array([TEN[n][1] for n in names])
u = np.array([1.0 if n in ("SH0ES", "CCHP", "SBF") else 0.0 for n in names])


def cov(sc, conv):
    C = np.diag(s ** 2) + sc ** 2 * np.outer(u, u)
    if conv == "B":
        C -= np.diag(sc ** 2 * u * u)
    return C


def fit(g1, C):
    A = np.array([[1.0, 0.0] if n in g1 else [0.0, 1.0] for n in names])
    Ci = np.linalg.inv(C)
    F = A.T @ Ci @ A
    Fi = np.linalg.inv(F)
    mu = Fi @ A.T @ Ci @ x
    r = x - A @ mu
    chi2 = float(r @ Ci @ r)
    var = Fi[0, 0] + Fi[1, 1] - 2 * Fi[0, 1]
    return mu, chi2, abs(mu[0] - mu[1]) / np.sqrt(var)


lens_z = {0.0: 6.4, 0.5: 5.6, 1.0: 4.4, 1.5: 3.5, 2.0: 3.0}
for conv in ["A", "B"]:
    print(f"Convention {conv}:")
    for sc, zl in lens_z.items():
        C = cov(sc, conv)
        if conv == "B" and np.min(np.linalg.eigvalsh(C)) <= 0:
            print(f"  sigma_c={sc}: covariance not positive definite")
            continue
        mu, c2, z = fit(LOCAL, C)
        allfits = []
        for r_ in range(1, len(names)):
            for g in itertools.combinations(names, r_):
                if names[0] in g:
                    allfits.append((fit(list(g), C)[1], g))
        allfits.sort()
        best = allfits[0][1]
        csh = fit(["SH0ES"], C)[1]
        worst_named = max(fit(["SH0ES"], C)[1], fit(["SH0ES", "CCHP", "SBF"], C)[1], fit(["CMB", "BAOBBN"], C)[1])
        print(f"  sigma_c={sc}: mu_L={mu[0]:.3f} mu_E={mu[1]:.3f} z={z:.3f} (lens {zl}); chi2 local/early={c2:.3f}; "
              f"best={'local/early' if set(best) == set(LOCAL) else best}; SH0ES-vs-rest chi2={csh:.3f}; "
              f"SH0ES-vs-rest is worst named: {abs(csh - worst_named) < 1e-9}")
        if conv == "A":
            num(f"z local vs early at sigma_c={sc}", z, zl, 0.06)
            named = {"local/early": c2, "ladders/rest": fit(["SH0ES", "CCHP", "SBF"], C)[1],
                     "rs-using/not": fit(["CMB", "BAOBBN"], C)[1], "SH0ES/rest": csh}
            print(f"    exhaustive best chi2 = {allfits[0][0]:.3f} ({allfits[0][1]}); local/early - best = "
                  f"{c2 - allfits[0][0]:.3f}; named: " + ", ".join(f"{k} {v:.3f}" for k, v in named.items()))
            # M-DECOMPOSER-10 reading 1 (among the named partitions): local/early is the minimum
            inequality(f"{c2!r}", "<=", f"{min(named.values())!r}")
            # reading 2 (exhaustive): local/early is within 0.4 of the best split
            inequality(f"{c2 - allfits[0][0]!r}", "<=", "0.4")
            inequality(f"{c2!r}", ">=", "8.1")
            inequality(f"{c2!r}", "<=", "8.55")

# limit: sigma_c = 0 reduces to inverse-variance means (F3 all-local 72.755 +- 0.732)
mu0, _, _ = fit(LOCAL, cov(0.0, "A"))
num("sigma_c = 0 local mean equals inverse-variance mean", mu0[0], 72.7554, 0.001)
# '~1.5% common-mode ladder error' = 1.5 km/s/Mpc at H ~ 73? 1.5/73.26
num("1.5 km/s/Mpc as percent of 73.26", 100 * 1.5 / 73.26, 2.0, 0.06)
num("1.5 km/s/Mpc in mag (lens 0.045)", 5 / np.log(10) * 1.5 / 73.26, 0.045, 0.0006)
units("(72.76 km/s/Mpc - 67.6 km/s/Mpc)/(1.5 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
