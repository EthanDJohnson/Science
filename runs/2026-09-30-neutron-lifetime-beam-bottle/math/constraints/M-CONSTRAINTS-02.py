"""M-CONSTRAINTS-02 (F4, F7): tau_beta per lambda input (GS2023, Vud = 0.97361(32)), group means, sensitivities.
tau_beta = K/(Vud^2 (1+3 lam^2)(1+dRV)); sigma = lam (+) Vud (+) 0.19 s (f and outer RC, the lens's input)."""
import sympy as sp
from _common import near, tau_beta, sig_tau_beta, LAM, wmean, VUD_GS
from math_checks import identity, limit, units, finish

# symbolic sensitivities
K, V, lam = sp.symbols("K V lam", positive=True)
t = K / (V**2 * (1 + 3 * lam**2))
identity(sp.diff(t, lam), -t * 6 * lam / (1 + 3 * lam**2))
identity(sp.diff(t, V), -2 * t / V)
limit(t, "lam", 0, K / V**2)
units("1 s / 1", "time")

lens = {"PERKEO III": (878.50, 0.88), "UCNA": (877.60, 2.36), "PERKEO II": (880.34, 1.63),
        "PDG 2024": (879.65, 1.61), "aSPECT 2020": (888.53, 3.31), "aSPECT 2024": (889.58, 3.20),
        "aCORN": (874.86, 7.07)}
for k, (tv, sv) in lens.items():
    l, s = LAM[k]
    near(f"tau_beta {k}", tau_beta(l), tv, 0.06)   # 5024.7 s constant rounding gives ~0.04 s offset
    near(f"sigma {k}", sig_tau_beta(l, s), sv, 0.006)

A = wmean([LAM["PERKEO III"], LAM["UCNA"], LAM["PERKEO II"]])
a = wmean([LAM["aSPECT 2024"], LAM["aCORN"]])
near("A-group lambda", A[0], 1.27623, 6e-6); near("A-group sigma", A[1], 0.00050, 6e-6)
near("A-group chi2", A[2], 1.51, 0.006)
near("a-group lambda", a[0], 1.26884, 6e-6); near("a-group sigma", a[1], 0.00248, 6e-6)
near("a-group chi2", a[2], 3.58, 0.006)
near("tau_beta A group", tau_beta(A[0]), 878.70, 0.06); near("sigma A", sig_tau_beta(A[0], A[1]), 0.83, 0.006)
near("tau_beta a group", tau_beta(a[0]), 887.21, 0.06); near("sigma a", sig_tau_beta(a[0], a[1]), 2.93, 0.006)
between = (A[0] - a[0]) ** 2 / (A[1] ** 2 + a[1] ** 2)
near("between-group chi2", between, 8.56, 0.006)
p3, asp = LAM["PERKEO III"], LAM["aSPECT 2024"]
near("PERKEO III vs aSPECT 2024 sigma", (p3[0] - asp[0]) / (p3[1] ** 2 + asp[1] ** 2) ** 0.5, 3.5, 0.05)

# sensitivities at PERKEO III lambda
tb = tau_beta(p3[0])
dl = -tb * 6 * p3[0] / (1 + 3 * p3[0] ** 2)
dv = -2 * tb / VUD_GS
near("dtau/dlam (scaled to lens tau 878.50)", dl * 878.50 / tb, -1142.7, 0.06); near("dtau/dVud (scaled)", dv * 878.50 / tb, -1804.6, 0.06)
near("1 s <-> dlam", 1 / abs(dl), 8.75e-4, 5e-7); near("1 s <-> dVud", 1 / abs(dv), 5.5e-4, 5e-6)
near("0.0096 split in tau", (p3[0] - asp[0]) * abs(dl), 10.98, 0.006)
print(f"   exact nonlinear split tau(aSPECT24) - tau(PERKEO III) = {tau_beta(asp[0]) - tb:.2f} s")
raise SystemExit(finish())
