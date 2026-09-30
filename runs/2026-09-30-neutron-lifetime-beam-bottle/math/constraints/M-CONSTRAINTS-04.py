"""M-CONSTRAINTS-04 (F6, K3): first-row sums. Neutron Vud from tau and lambda:
Vud_n^2 = Vud_ref^2 tau_beta(lam; Vud_ref)/tau (same master formula), sigma from tau, lambda and 0.19 s RC (not Vud_ref).
Row = Vud^2 + Vus^2 + Vub^2; Vus = 0.22431(85) (PDG avg), Vub^2 ~ 1.5e-5."""
import math
import sympy as sp
from _common import near, tau_beta, sig_tau_beta, LAM, VUD_GS, S_VUD_GS, VUS, S_VUS, VUB, TAU_UCN, S_UCN_UP, S_UCN_DN, TAU_BL1, S_BL1
from math_checks import identity, finish

V0, T0, T, lam, K = sp.symbols("V0 T0 T lam K", positive=True)
# tau(lam, V) = K/(V^2(1+3lam^2)); if tau(lam,V0) = T0 then V^2 at tau T is V0^2 T0 / T
T0e = K / (V0**2 * (1 + 3 * lam**2)); Vn = V0 * sp.sqrt(T0e / T)
identity(K / (Vn**2 * (1 + 3 * lam**2)), T)

v2ub = VUB**2
s_us = 2 * VUS * S_VUS


def row(tau, stau, lamkey):
    l, sl = LAM[lamkey]
    tb = tau_beta(l)
    sb = sig_tau_beta(l, sl, include_vud=False)
    vud2 = VUD_GS**2 * tb / tau
    s = math.hypot(vud2 * math.hypot(stau / tau, sb / tb), s_us)
    r = vud2 + VUS**2 + v2ub
    return r, s, (r - 1) / s


r0 = VUD_GS**2 + VUS**2 + v2ub
s0 = math.hypot(2 * VUD_GS * S_VUD_GS, s_us)
near("superallowed row", r0, 0.99825, 6e-6); near("superallowed sigma", s0, 0.00073, 6e-6)
near("superallowed z", (r0 - 1) / s0, -2.4, 0.06)
for lab, tau, st, lk, want, ws, wz in [("UCNtau+PERKEO III", TAU_UCN, S_UCN_UP, "PERKEO III", 0.99898, 0.00087, -1.2),
                                       ("BL1+PERKEO III", TAU_BL1, S_BL1, "PERKEO III", 0.98842, 0.00251, -4.6),
                                       ("BL1+aSPECT 2024", TAU_BL1, S_BL1, "aSPECT 2024", 1.00025, 0.00415, 0.1),
                                       ("UCNtau+aSPECT 2024", TAU_UCN, S_UCN_DN, "aSPECT 2024", 1.01094, 0.00343, 3.2)]:
    r, s, z = row(tau, st, lk)
    near(f"{lab} row", r, want, 6e-5)   # my tau_beta 0.04 s high -> row +5e-5
    near(f"{lab} sigma", s, ws, 1.5e-5)
    near(f"{lab} z", z, wz, 0.06)
# exact unitarity
for lab, vus, want in [("PDG avg", VUS, 876.88), ("K_l3", 0.2233, 876.5), ("K_mu2", 0.2250, 877.2)]:
    vud_u = math.sqrt(1 - vus**2 - v2ub)
    t = tau_beta(LAM["PERKEO III"][0], vud=vud_u)
    if lab == "PDG avg":
        near("unitary Vud", vud_u, 0.97451, 6e-6)
    near(f"tau_beta under exact unitarity ({lab})", t, want, 0.06)
raise SystemExit(finish())
