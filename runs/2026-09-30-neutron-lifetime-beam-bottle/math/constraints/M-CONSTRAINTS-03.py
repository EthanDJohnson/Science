"""M-CONSTRAINTS-03 (F5, K1, K2): exotic branch Br_X = 1 - tau_tot/tau_beta, with tau_tot = UCNtau 877.82 s.
sigma(Br) = (tau_tot/tau_beta) sqrt((s_tot/tau_tot)^2 + (s_beta/tau_beta)^2); one-sided 95% UL = Br + 1.645 sigma.
My tau_beta is ~0.04 s above the lens's (5024.7 s constant rounding) -> Br ~0.005% higher; tolerances allow that."""
import math
import sympy as sp
from _common import near, tau_beta, sig_tau_beta, LAM, wmean, TAU_UCN, S_UCN_UP, TAU_BL1, S_BL1
from math_checks import identity, limit, series, finish

tt, tb = sp.symbols("tau_t tau_b", positive=True)
br = 1 - tt / tb
limit(br, "tau_b", sp.oo, 1)                      # no beta decay -> all exotic
identity(br.subs(tt, tb), 0)                      # equal lifetimes -> no exotic branch
d = sp.symbols("d", positive=True)
series((1 - tt / (tt + d)), "d", 0, 2, d / tt)    # small-gap limit: Br ~ gap / tau

s_tot = S_UCN_UP   # facing side (+0.20 sys) toward longer tau_beta


def brx(t, s):
    b = 1 - TAU_UCN / t
    sb = (TAU_UCN / t) * math.hypot(s_tot / TAU_UCN, s / t)
    return b, sb


A = wmean([LAM["PERKEO III"], LAM["UCNA"], LAM["PERKEO II"]])
a = wmean([LAM["aSPECT 2024"], LAM["aCORN"]])
cases = {"PERKEO III": LAM["PERKEO III"], "PDG 2024": LAM["PDG 2024"], "aSPECT 2024": LAM["aSPECT 2024"],
         "A group": A[:2], "a group": a[:2]}
res = {k: brx(tau_beta(l), sig_tau_beta(l, s)) for k, (l, s) in cases.items()}
needed = 1 - TAU_UCN / TAU_BL1
near("needed Br (%)", 100 * needed, 1.113, 0.0006)
near("PERKEO III Br (%)", 100 * res["PERKEO III"][0], 0.077, 0.006)
near("PERKEO III sigma (%)", 100 * res["PERKEO III"][1], 0.106, 0.0006)
near("PERKEO III UL95 (%)", 100 * (res["PERKEO III"][0] + 1.645 * res["PERKEO III"][1]), 0.25, 0.01)
near("needed distance PERKEO III (sigma)", (needed - res["PERKEO III"][0]) / res["PERKEO III"][1], 9.8, 0.1)
near("A-group UL95 (%)", 100 * (res["A group"][0] + 1.645 * res["A group"][1]), 0.27, 0.01)
near("A-group needed distance", (needed - res["A group"][0]) / res["A group"][1], 10.0, 0.25)
near("PDG UL95 (%)", 100 * (res["PDG 2024"][0] + 1.645 * res["PDG 2024"][1]), 0.51, 0.01)
near("PDG needed distance", (needed - res["PDG 2024"][0]) / res["PDG 2024"][1], 4.9, 0.06)
near("aSPECT 2024 Br (%)", 100 * res["aSPECT 2024"][0], 1.32, 0.01)
near("aSPECT 2024 sigma (%)", 100 * res["aSPECT 2024"][1], 0.36, 0.006)
near("a-group Br (%)", 100 * res["a group"][0], 1.06, 0.01)
near("a-group sigma (%)", 100 * res["a group"][1], 0.33, 0.006)
# K1 tensions
tA, sA = tau_beta(A[0]), sig_tau_beta(*A[:2])
ta, sa = tau_beta(a[0]), sig_tau_beta(*a[:2])
tP, sP = tau_beta(LAM["PERKEO III"][0]), sig_tau_beta(*LAM["PERKEO III"])
near("UCNtau vs PERKEO III tau_beta (sigma)", (tP - TAU_UCN) / math.hypot(sP, s_tot), 0.7, 0.06)
near("UCNtau vs A route", (tA - TAU_UCN) / math.hypot(sA, s_tot), 1.0, 0.06)
near("UCNtau vs a route", (ta - TAU_UCN) / math.hypot(sa, s_tot), 3.2, 0.06)
near("BL1 vs A route", (TAU_BL1 - tA) / math.hypot(sA, S_BL1), 3.8, 0.06)
raise SystemExit(finish())
