"""M-CONSTRAINTS-11 (F13, K11): J-PARC 2024 (877.2 s, stat 1.7, sys +4.0/-3.6) tensions, using the side facing each
comparison; z = |x - J|/sqrt(s_J,side^2 + s_x^2). Likelihood ratio of two Gaussian hypotheses for J-PARC's value:
LR = N(J; tau_S, s_S) / N(J; tau_B, s_B), with s = sigma_J,side (+) sigma_pole (normalisation included)."""
import math
import sympy as sp
from _common import near, TAU_JP, S_JP_UP, S_JP_DN, TAU_BL1, S_BL1, TAU_UCN, S_UCN_DN, TAU_GRAV, S_GRAV
from math_checks import identity, limit, finish

x, mS, mB, sS, sB = sp.symbols("x mS mB sS sB", positive=True)
N = lambda mu, s: sp.exp(-(x - mu) ** 2 / (2 * s**2)) / (sp.sqrt(2 * sp.pi) * s)
LR = N(mS, sS) / N(mB, sB)
identity(sp.log(LR), -((x - mS) / sS) ** 2 / 2 + ((x - mB) / sB) ** 2 / 2 + sp.log(sB / sS))
limit(sp.log(LR.subs(sB, sS)), "sS", sp.oo, 0)   # uninformative measurement -> LR = 1

near("sigma_J up", S_JP_UP, 4.35, 0.006); near("sigma_J down", S_JP_DN, 3.98, 0.006)
zB = (TAU_BL1 - TAU_JP) / math.hypot(S_JP_UP, S_BL1)
zU = (TAU_UCN - TAU_JP) / math.hypot(S_JP_UP, S_UCN_DN)
zG = (TAU_GRAV - TAU_JP) / math.hypot(S_JP_UP, S_GRAV)
zA = (878.70 - TAU_JP) / math.hypot(S_JP_UP, 0.83)
za = (887.21 - TAU_JP) / math.hypot(S_JP_UP, 2.93)
near("vs BL1", zB, 2.15, 0.006); near("vs UCNtau", zU, 0.14, 0.006); near("vs Gravitrap", zG, 0.97, 0.006)
near("vs SM A route", zA, 0.34, 0.006); near("vs SM a route", za, 1.91, 0.006)
Sj = math.sqrt(15.8 / 3)
near("scale factor", Sj, 2.29, 0.006); near("scaled stat", 1.7 * Sj, 3.90, 0.006)
sup2 = math.hypot(1.7 * Sj, 4.0)
zB2 = (TAU_BL1 - TAU_JP) / math.hypot(sup2, S_BL1)
near("vs BL1 scaled", zB2, 1.74, 0.006)


def lr(su):
    sB, sS = math.hypot(su, S_BL1), math.hypot(su, S_UCN_DN)
    zb, zs = (TAU_BL1 - TAU_JP) / sB, (TAU_UCN - TAU_JP) / sS
    return math.exp(-(zs**2 - zb**2) / 2) * sB / sS, math.exp(-(zs**2 - zb**2) / 2)


l1, l1p = lr(S_JP_UP); l2, l2p = lr(sup2)
print(f"   LR with normalisation {l1:.2f} (scaled {l2:.2f}); profile exp(dchi2/2) {l1p:.2f} (scaled {l2p:.2f})")
near("LR as quoted", l1, 11.1, 0.06); near("LR scaled", l2, 4.9, 0.06)
raise SystemExit(finish())
