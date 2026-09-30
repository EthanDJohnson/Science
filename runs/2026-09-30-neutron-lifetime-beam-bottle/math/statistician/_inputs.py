"""Shared inputs and helpers for the statistician math checks (my own, independent of the lens's scripts).
All lifetimes in s (SI). Values from dossier D-20, D-22 (PDG listing per lens F1), D-23, D-24, D-27..D-30, D-40..D-42.
Asymmetric errors: symmetrized as the mean of the two sides for combinations (lens assumption, restated)."""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp

def q(*xs):
    return math.sqrt(sum(x * x for x in xs))

def sym(up, dn):
    return 0.5 * (up + dn)

# (name, value, total sigma, stat, sys)
BL1 = ("BL1 Yue13", 887.7, q(1.2, 1.9), 1.2, 1.9)
SUS = ("Sussex-ILL Byrne96", 889.2, q(3.0, 3.8), 3.0, 3.8)
PROTON = [BL1, SUS]

MATERIAL = [
    ("Serebrov05", 878.5, q(0.7, 0.3), 0.7, 0.3),
    ("Pichlmaier10", 880.7, q(1.3, 1.2), 1.3, 1.2),
    ("Steyerl12", 882.5, q(1.4, 1.5), 1.4, 1.5),
    ("Arzumanov15", 880.2, 1.2, None, None),
    ("Serebrov18", 881.5, q(0.7, 0.6), 0.7, 0.6),
]
MAGNETIC = [
    ("Musedinovic25", 877.82, q(0.22, sym(0.20, 0.17)), 0.22, sym(0.20, 0.17)),
    ("Pattie18", 877.7, q(0.7, sym(0.4, 0.2)), 0.7, sym(0.4, 0.2)),
    ("Ezhov18", 878.3, q(1.6, 1.0), 1.6, 1.0),
]
STORAGE = MATERIAL + MAGNETIC

JP_VAL = 877.2
JP_STAT = 1.7
JP_UP = q(1.7, 4.0)
JP_DN = q(1.7, 3.6)
JPARC = ("J-PARC24", JP_VAL, sym(JP_UP, JP_DN), 1.7, sym(4.0, 3.6))


def wmean(rows):
    w = [1 / r[2] ** 2 for r in rows]
    m = sum(wi * r[1] for wi, r in zip(w, rows)) / sum(w)
    s = 1 / math.sqrt(sum(w))
    chi2 = sum(wi * (r[1] - m) ** 2 for wi, r in zip(w, rows))
    dof = len(rows) - 1
    S = max(1.0, math.sqrt(chi2 / dof)) if dof > 0 else 1.0
    return m, s, chi2, dof, S


def p2(z):
    """two-sided Gaussian p-value"""
    return float(mp.erfc(mp.mpf(z) / mp.sqrt(2)))


def z_of_p2(p):
    """inverse of p2"""
    return float(mp.sqrt(2) * mp.erfinv(1 - mp.mpf(p)))


def chi2_sf(x, k):
    return float(mp.gammainc(mp.mpf(k) / 2, mp.mpf(x) / 2, mp.inf, regularized=True))


def say(label, val, lens=None):
    extra = f"   (lens: {lens})" if lens is not None else ""
    print(f"{label}: {val}{extra}")
