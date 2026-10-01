"""Shared inputs and helpers for the constraints-lens math checks (my own transcription of the dossier).
Lifetimes in s (SI); masses in MeV (natural units, c = 1)."""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity  # noqa: E402

# Dossier inputs (D-20, D-23, D-27, D-28, D-40..D-45, D-48, D-49)
TAU_BL1, S_BL1 = 887.7, math.hypot(1.2, 1.9)
TAU_UCN, S_UCN_UP, S_UCN_DN = 877.82, math.hypot(0.22, 0.20), math.hypot(0.22, 0.17)
TAU_GRAV, S_GRAV = 881.5, math.hypot(0.7, 0.6)
TAU_JP, S_JP_UP, S_JP_DN = 877.2, math.hypot(1.7, 4.0), math.hypot(1.7, 3.6)

LAM = {  # |lambda|, total sigma
    "PERKEO III": (1.27641, math.hypot(0.00045, 0.00033)),
    "UCNA": (1.2772, 0.0020),
    "PERKEO II": (1.2748, math.hypot(0.0008, 0.00105)),
    "PDG 2024": (1.2754, 0.0013),
    "aSPECT 2020": (1.2677, 0.0028),
    "aSPECT 2024": (1.2668, 0.0027),
    "aCORN": (1.2796, 0.0062),
}
VUD_GS, S_VUD_GS = 0.97361, 0.00032
VUS, S_VUS = 0.22431, 0.00085
VUB = 3.82e-3  # |Vub|^2 ~ 1.5e-5, negligible

# Radiative corrections. Gorchtein-Seng master formula: |Vud|^2 = 5024.7 s / [tau (1+3 lam^2)(1+dRV)]
K_GS = 5024.46  # Tan/Dubbers value (D-49); Gorchtein-Seng 5024.7 s gives tau_beta +0.04 s (checked in M-01)
DRV_GS = 0.02479


def near(label, got, want, tol_abs):
    """PASS if |got - want| <= tol_abs (tolerance chosen as half the last printed digit of the lens)."""
    rel = abs(tol_abs / want) if want != 0 else tol_abs
    print(f"   {label}: got {got:.6g}, lens {want:.6g}")
    return quantity(f"{got!r}", f"{want!r}", rel_tol=max(rel, 1e-12))


def tau_beta(lam, vud=VUD_GS, drv=DRV_GS, K=K_GS):
    return K / (vud**2 * (1 + 3 * lam**2) * (1 + drv))


def sig_tau_beta(lam, slam, vud=VUD_GS, svud=S_VUD_GS, s_rc=0.19, include_vud=True):
    t = tau_beta(lam, vud)
    d_lam = t * 6 * lam / (1 + 3 * lam**2) * slam
    d_vud = 2 * t / vud * svud if include_vud else 0.0
    return math.sqrt(d_lam**2 + d_vud**2 + s_rc**2)


def wmean(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(wi * x for wi, (x, _) in zip(w, vals)) / sum(w)
    chi2 = sum(wi * (x - m) ** 2 for wi, (x, _) in zip(w, vals))
    return m, 1 / math.sqrt(sum(w)), chi2
