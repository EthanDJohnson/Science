"""M-STATISTICIAN-11: SM tau_beta and Br_X (F10, F11, S5, S6, candidate C).
Master formula structure: tau_beta = K_eff / (Vud^2 (1 + 3 lambda^2)), K_eff in s (radiative corrections and f absorbed).
Independent calibration of K_eff: Gorchtein-Seng 2023 inverted numbers (D-44): tau = 877.75 s, lambda = 1.27641 -> Vud = 0.97404.
Cross-check: CMS-style 5024.7 s/(1 + DeltaR^V), DeltaR^V = 0.02479 (D-48, D-49).
Vud = 0.97361(32) (GS2023 superallowed, D-43). K error 0.19 s taken from the lens as an input (not derived).
Lens: PERKEO III 878.50 +- 0.88 (Vud 0.58, lambda 0.64, K 0.19); A route 878.70 +- 0.83; aSPECT 889.58 +- 3.20;
a route 887.21 +- 2.93; swapped 888.74 +- 2.93; PDG 879.65 +- 1.61.
Br_X = 1 - tau_storage/tau_beta: PERKEO III 0.0002 +- 0.0011 (95% UL 0.0020), needed 0.0109 at 9.5 sigma;
aSPECT 0.0127 +- 0.0036; PDG 0.0015 +- 0.0019, needed at 4.9 sigma. Tensions: 4.26/0.18, 0.42/3.49, 3.20/0.80."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, quantity, units, inequality, finish
import sympy as sp

K_cal = 877.75 * 0.97404**2 * (1 + 3 * 1.27641**2)
K_alt = 5024.7 / 1.02479
print("K_eff calibrated from GS2023 (s):", K_cal, " alt 5024.7/1.02479:", K_alt)
VUD, SV, SK = 0.97361, 0.00032, 0.19
def tau(lam, slam, K=K_cal):
    t = K / (VUD**2 * (1 + 3 * lam**2))
    sv = 2 * SV / VUD * t
    sl = 6 * lam / (1 + 3 * lam**2) * t * slam
    return t, q(sv, sl, SK), sv, sl
# symbolic sensitivities
lam, V, K = sp.symbols("lam V K", positive=True)
T = K / (V**2 * (1 + 3 * lam**2))
identity(sp.diff(T, lam), -6 * lam * T / (1 + 3 * lam**2))
identity(sp.diff(T, V), -2 * T / V)
limit(T * (1 + 3 * lam**2), "lam", 0, "K/V**2")   # pure Fermi limit: tau = K/Vud^2
units("4903 s / (0.97361^2 * 5.8877)", "s")

mp_, sp_, *_ = wmean(PROTON)
ms, ss, c, d, S = wmean(STORAGE); ss *= S
rows = [("PERKEO III", 1.27641, q(0.00045, 0.00033), "878.50", "0.88"),
        ("A route", 1.27623, 0.00050, "878.70", "0.83"),
        ("aSPECT24", 1.2668, 0.0027, "889.58", "3.20"),
        ("a route", 1.26884, 0.00248, "887.21", "2.93"),
        ("a swapped", 1.26752, 0.00247, "888.74", "2.93"),
        ("PDG24", 1.2754, 0.0013, "879.65", "1.61")]
for lab, l, sl, lt, ls in rows:
    t, st, sv, slam = tau(l, sl); t2 = tau(l, sl, K_alt)[0]
    zB = abs(t - mp_) / q(st, sp_); zS = abs(t - ms) / q(st, ss)
    br = 1 - ms / t; sbr = (ms / t) * q(ss / ms, st / t)
    need = 1 - ms / mp_
    print(f"{lab}: tau {t:.2f} +- {st:.2f} s (Vud {sv:.2f}, lam {slam:.2f}; alt-K {t2:.2f})  lens {lt} +- {ls}; "
          f"z_beam {zB:.2f} z_stor {zS:.2f}; Br {br:.4f} +- {sbr:.4f}; UL95 {br+1.645*sbr:.4f}; need {need:.4f} at {(need-br)/sbr:.2f} sigma")
    inequality(f"{abs(t - float(lt))}", "<", "0.06")   # agreement within 0.06 s (K calibration rounding)
    identity(f"{st:.2f}", ls)
quantity("877.75 s * 0.97404^2 * 5.88767", "4903.1 s", rel_tol=2e-4)
raise SystemExit(finish())
