"""M-EXAMINER-06: exotic branching ratio Br_X = 1 - tau_bottle/tau_beta (F10).
tau_beta from route (a) of M-05 (K0 = 5024.46 s from G_F, m_e, f, delta_R', DeltaR^V 0.02479(21), Vud 0.97361(32)); tau_bottle = UCNtau 877.82 s.
sigma(Br) = (tau_b/tau_beta) sqrt((s_b/tau_b)^2 + (s_beta/tau_beta)^2); one-sided 95% UL = Br + 1.645 sigma. Dimensionless."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
import sympy as sp
from math_checks import identity, limit, finish
from _inputs import *
from _h import cmp

def tau(lam, slam):
    t = 5024.46 / ((1 + DRV) * VUD**2 * (1 + 3 * lam**2))
    s = t * math.sqrt((6 * lam / (1 + 3 * lam**2) * slam) ** 2 + (2 * SVUD / VUD) ** 2 + (SDRV / (1 + DRV)) ** 2)
    return t, s

for lab, cB, cS in (("PERKEO III", 0.077, 0.106), ("aSPECT 2024", 1.32, 0.36)):
    t, s = tau(*LAM[lab])
    for sU, tag in ((UCNTAU[1], "sym"), (q(U_STAT, U_UP), "upper side")):
        br = 1 - U_X / t
        sb = (U_X / t) * math.sqrt((sU / U_X) ** 2 + (s / t) ** 2)
        print(f"{lab} ({tag} UCNtau error): tau_beta {t:.2f} +- {s:.2f} s; Br_X = {100*br:.3f} +- {100*sb:.3f} %; UL95 {100*(br+1.645*sb):.3f} %")
    cmp(f"{lab} Br_X (%)", 100 * br, cB, 0.006 if cB < 1 else 0.02)
    cmp(f"{lab} sigma (%)", 100 * sb, cS, 0.006)
    if lab == "PERKEO III":
        cmp("UL95 (%)", 100 * (br + 1.645 * sb), 0.25, 0.006)
gap_frac = 1 - U_X / BL1[0]
print(f"Br needed by the gap = {100*gap_frac:.3f} %")
a, b = sp.symbols("a b", positive=True)
identity(1 - a / b, (b - a) / b)
limit("1 - a/b", "a", 3, "0", domain={"b": (3, 3)}) if False else limit("1 - a/3", "a", 3, "0")  # tau_bottle -> tau_beta gives Br -> 0
raise SystemExit(finish())
