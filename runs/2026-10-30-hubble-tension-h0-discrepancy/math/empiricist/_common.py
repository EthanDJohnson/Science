"""Shared inputs and helpers for the empiricist math checks (written by the math checker, not the lens).

All H0 values in km/s/Mpc (SI-equivalent unit km s^-1 Mpc^-1). Inputs are the values the lens quotes
from the dossier; asymmetric errors are symmetrised as the mean of up and down, as the lens states.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import mpmath as mp
from math_checks import quantity

H = {  # name: (value, sigma)
    "SH0ES": (73.49, 0.93),
    "CCHP": (70.39, 1.94),
    "SBF": (73.8, 2.40),
    "TF": (73.3, 4.1),
    "TDCOSMO": (71.1, (2.4 + 2.3) / 2),
    "masers": (71.6, 3.7),
    "sirens": (71.7, (9.4 + 7.5) / 2),
    "Refsdal": (64.8, (4.4 + 4.3) / 2),
    "H0pe": (75.4, (8.1 + 5.5) / 2),
    "CMB": (67.19, 0.38),
    "BAOBBN": (68.50, 0.58),
}


def gls(names, cov=None):
    """Generalised least-squares mean of a constant; returns (mean, sigma)."""
    x = np.array([H[n][0] for n in names])
    if cov is None:
        cov = np.diag([H[n][1] ** 2 for n in names])
    w = np.linalg.solve(cov, np.ones(len(x)))
    var = 1.0 / w.sum()
    return float(var * (w @ x)), float(np.sqrt(var))


def tension(a, b):
    """|a - b| / sqrt(sa^2 + sb^2) for (value, sigma) pairs, uncorrelated."""
    return abs(a[0] - b[0]) / np.hypot(a[1], b[1])


def two_sided_gauss(n):
    return float(mp.erfc(mp.mpf(n) / mp.sqrt(2)))


def cmp(label, got, quoted, abs_tol, unit=""):
    """PASS if got rounds to quoted within abs_tol (rounding of the lens's printed digits)."""
    u = (" " + unit) if unit else ""
    rel = abs(abs_tol / quoted) if quoted else abs_tol
    print(f"  {label}: computed {got:.6g}{u}, lens {quoted}{u}")
    return quantity(f"{float(got)!r}{u}", f"{float(quoted)!r}{u}", rel_tol=rel)
