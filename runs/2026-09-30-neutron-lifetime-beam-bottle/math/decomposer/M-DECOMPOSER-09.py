"""M-DECOMPOSER-09 (F9, candidate C): Br_X = 1 - tau_UCNtau / tau_beta(lambda); error by propagation;
95% upper limit one-sided (1.645 sigma); exclusion of Br_X = 1.11% in sigma. SI (s), Br dimensionless."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import identity, limit, finish
from _inputs import near, q, UCNT, BL1
from _sm import *

need = 1 - UCNT[0] / BL1[0]
def br(lam, sl, C=C_TAN):
    t = tau_beta(lam, C=C)
    et = q(abs(dtau_dlam(lam, t)) * sl, 2 * t * VUD_E / VUD, t * DRV_E / (1 + DRV))
    b = 1 - UCNT[0] / t
    eb = q(UCNT[1] / t, UCNT[0] * et / t ** 2)
    return b, eb
rows = {"PERKEO III": (0.08, 0.11, 0.25), "PDG 2024": (0.21, 0.19, 0.51), "aSPECT 2024": (1.32, 0.36, None)}
for k, (bl, el, ul) in rows.items():
    b, eb = br(*LAM[k])
    up1 = b + 1.645 * eb; up2 = b + 1.96 * eb
    print(f"{k}: Br {b*100:.3f} +- {eb*100:.3f}%; UL95 one-sided {up1*100:.3f}%, two-sided {up2*100:.3f}%; "
          f"needed {need*100:.3f}% at {(need-b)/eb:+.2f} sigma; Br>0 at {b/eb:.2f} sigma")
    near(f"{k} Br (%)", b * 100, bl, 0.006); near(f"{k} err (%)", eb * 100, el, 0.006)
    if ul is not None:
        near(f"{k} UL95 one-sided (%)", up1 * 100, ul, 0.006)
bA, eA = br(1.27623, 0.00050)
print(f"A route: Br {bA*100:.3f} +- {eA*100:.3f}%, needed excluded at {(need-bA)/eA:.2f} sigma")
bP, eP = br(*LAM["PERKEO III"])
print(">7 sigma claim:", (need - bP) / eP > 7 and (need - bA) / eA > 7)
near("aSPECT Br>0 significance", br(*LAM["aSPECT 2024"])[0] / br(*LAM["aSPECT 2024"])[1], 3.7, 0.05)
identity("1 - ts/tb", "(tb - ts)/tb")
limit("1 - ts/tb", "tb", "ts", "0")
raise SystemExit(finish())
