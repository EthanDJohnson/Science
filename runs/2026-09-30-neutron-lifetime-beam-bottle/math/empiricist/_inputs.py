"""My own transcription of the dossier inputs (lifetimes in s, SI) and small helpers.

Sources: D-20 (BL1), D-22 (Sussex-ILL, unverified lead), D-23 (J-PARC 2024), D-27 (UCNtau 2025),
D-28 (Gravitrap 2018), D-29 (Serebrov 2005, MAMBO II, Steyerl 2012, Arzumanov 2015), D-30 (Ezhov 2018).
Per experiment: stat and sys in quadrature; an asymmetric sys is symmetrized as the mean of its sides.
"""
import sys
from math import sqrt, erfc
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
from math_checks import inequality


def q(*a):
    return sqrt(sum(x * x for x in a))


D = {
    "BL1": (887.7, q(1.2, 1.9)),
    "SUS": (889.2, q(3.0, 3.8)),
    "JP": (877.2, q(1.7, (4.0 + 3.6) / 2)),
    "SER05": (878.5, q(0.7, 0.3)),
    "MAMBO": (880.7, q(1.3, 1.2)),
    "STEY": (882.5, q(1.4, 1.5)),
    "ARZ": (880.2, 1.2),
    "GRAV": (881.5, q(0.7, 0.6)),
    "UCNT": (877.82, q(0.22, 0.20)),   # larger sys side; the lens's numbers reproduce with this (see M-01 log)
    "EZH": (878.3, q(1.6, 1.0)),
}
D_MEANSIDE = dict(D, UCNT=(877.82, q(0.22, (0.20 + 0.17) / 2)))   # sensitivity: mean-of-sides symmetrization
PROTON = ["BL1", "SUS"]
EBEAM = ["JP"]
MATERIAL = ["SER05", "MAMBO", "STEY", "ARZ", "GRAV"]
MAGNETIC = ["UCNT", "EZH"]
STORAGE = MATERIAL + MAGNETIC
ALL = PROTON + EBEAM + STORAGE


def wmean(keys, data=D):
    w = [1 / data[k][1] ** 2 for k in keys]
    m = sum(wi * data[k][0] for wi, k in zip(w, keys)) / sum(w)
    return m, 1 / sqrt(sum(w))


def chi2(keys, data=D):
    m, _ = wmean(keys, data)
    return sum(((data[k][0] - m) / data[k][1]) ** 2 for k in keys)


def grouped(groups, data=D):
    """Return (within, between, total) chi2 for a partition of experiments into groups."""
    allk = [k for g in groups for k in g]
    tot = chi2(allk, data)
    within = sum(chi2(g, data) for g in groups if len(g) > 1)
    return within, tot - within, tot


def between_direct(groups, data=D):
    """Between-group chi2 computed directly from the group means (independent of the total)."""
    ms = [wmean(g, data) for g in groups]
    W = [1 / s ** 2 for _, s in ms]
    M = sum(w * m for w, (m, _) in zip(W, ms)) / sum(W)
    return sum(w * (m - M) ** 2 for w, (m, _) in zip(W, ms))


def pchi2(x, k):
    return float(mp.gammainc(k / 2, x / 2, mp.inf, regularized=True))


def zeq(p):
    """Two-sided Gaussian-equivalent significance of a p value."""
    return float(mp.sqrt(2) * mp.erfinv(1 - mp.mpf(p)))


def agree(label, got, lens, tol):
    """PASS when |got - lens| < tol (a rounding tolerance on the lens's printed value)."""
    print(f"  {label}: mine {got:.6g}, lens {lens}")
    return inequality(f"Abs({got!r} - ({lens!r}))", "<", repr(tol))
