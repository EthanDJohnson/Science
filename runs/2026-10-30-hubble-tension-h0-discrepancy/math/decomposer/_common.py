"""Shared inputs and helpers for the decomposer math checks (independent of the lens scripts).

All H0 values in km/s/Mpc. Asymmetric errors symmetrised as the mean of the two sides,
quadrature-summed stat and sys where quoted separately. Inputs taken from dossier.md.
"""
import sys
import math
import itertools
import mpmath as mp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, limit, units, inequality, sign, finish  # noqa: E402,F401

mp.mp.dps = 30


def quad(*s):
    return math.sqrt(sum(x * x for x in s))


def sym(up, dn):
    return 0.5 * (up + dn)


# Ten-result minimal-overlap set (F2)
TEN = {
    "SH0ES": (73.49, 0.93),                  # D-20
    "CCHP": (70.39, quad(1.22, 1.33, 0.70)),  # D-24
    "SBF": (73.8, quad(0.7, 2.3)),           # D-29
    "TD": (71.1, sym(2.4, 2.3)),             # D-31
    "MASER": (71.6, 3.7),                    # D-32 (Stiskalek 2026, supersedes Pesce)
    "SIREN": (71.7, sym(9.4, 7.5)),          # D-33
    "CMB": (67.19, 0.38),                    # D-44
    "BAOBBN": (68.50, 0.58),                 # D-45
    "RSFREE": (69.6, sym(1.3, 1.8)),         # D-49
    "EQ": (65.1, sym(3.0, 5.4)),             # D-50
}
LOCAL = ["SH0ES", "CCHP", "SBF", "TD", "MASER", "SIREN"]
EARLY = ["CMB", "BAOBBN", "RSFREE", "EQ"]


def wmean(items):
    w = [1 / s ** 2 for _, s in items]
    m = sum(wi * x for wi, (x, _) in zip(w, items)) / sum(w)
    return m, 1 / math.sqrt(sum(w))


def chi2_about_mean(items):
    m, _ = wmean(items)
    return sum(((x - m) / s) ** 2 for x, s in items)


def tension(a, sa, b, sb):
    return abs(a - b) / math.sqrt(sa ** 2 + sb ** 2)


def chi2_sf(x, k):
    """Survival function of chi^2 with k dof, via regularised upper incomplete gamma."""
    return float(mp.gammainc(mp.mpf(k) / 2, mp.mpf(x) / 2, mp.inf, regularized=True))


def z_from_p2(p):
    """Two-sided Gaussian-equivalent z for a p-value."""
    p = mp.mpf(p)
    return float(mp.findroot(lambda z: mp.erfc(z / mp.sqrt(2)) - p, 5))


def num(label, got, want, tol):
    """Dimensionless numeric comparison through math_checks.quantity (absolute tol -> relative)."""
    got, want = float(got), float(want)
    rel = abs(tol / want) if want != 0 else tol
    print(f"  {label}: computed {got:.6g}, lens {want:g}")
    return quantity(f"{got!r}", f"{want!r}", rel_tol=rel)
