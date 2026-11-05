"""Shared inputs (from dossier.md, quoted values) and independent statistics helpers.
All H0 in km/s/Mpc. Asymmetric errors stored as (value, +err, -err)."""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")

def quad(*e):
    return math.sqrt(sum(x * x for x in e))

# local classes (dossier D-20, D-24, D-29, D-30, D-31, D-32, D-33)
SH0ES = (73.49, 0.93, 0.93)
CCHP = (70.39, quad(1.22, 1.33, 0.70), quad(1.22, 1.33, 0.70))
SBF = (73.8, quad(0.7, 2.3), quad(0.7, 2.3))
TF = (73.3, quad(2.1, 3.5), quad(2.1, 3.5))
TD = (71.1, 2.4, 2.3)
MASER = (71.6, 3.7, 3.7)
SIREN = (71.7, 9.4, 7.5)
# early classes (D-02, D-08, D-48)
CMB = (67.19, 0.38, 0.38)
BAOBBN = (68.50, 0.58, 0.58)
INVL_COSMO = (67.19, 0.66, 0.64)
INVL_LCDM = (67.67, 0.69, 0.68)
# r_s-free (D-49) and equality (D-50)
RSFREE = {"Z-lensxunWISE": (69.2, 1.3, 1.4), "Z-DES6x2": (70.3, 1.4, 1.2), "Z-lens+DESY5": (69.6, 1.3, 1.8),
          "2411-DESY5": (66.7, 1.7, 1.9), "2411-PP": (67.9, 1.9, 2.1), "2411-U3": (67.8, 2.0, 2.2)}
EQ = {"EQ-Pantheon": (65.1, 3.0, 5.4), "EQ-uncalBAO": (65.6, 3.4, 5.5), "EQ-BAOlens": (70.6, 3.7, 5.0)}

def sym(m):
    return (m[0], 0.5 * (m[1] + m[2]))

def wmean(items):
    """items: list of (value, sigma). Inverse-variance mean, its error and chi2 about it."""
    w = [1 / s ** 2 for _, s in items]
    W = sum(w)
    mu = sum(wi * v for wi, (v, _) in zip(w, items)) / W
    chi2 = sum(((v - mu) / s) ** 2 for v, s in items)
    return mu, 1 / math.sqrt(W), chi2

def z_facing(a, b):
    """a, b as (v, +e, -e). Uses the error of each on the side facing the other."""
    if a[0] >= b[0]:
        sa, sb = a[2], b[1]
    else:
        sa, sb = a[1], b[2]
    return abs(a[0] - b[0]) / math.hypot(sa, sb)

def z_sym(a, b):
    a, b = sym(a), sym(b)
    return abs(a[0] - b[0]) / math.hypot(a[1], b[1])

def chi2_sf(x, k):
    """Survival function of chi2 with k dof (mpmath, exact incomplete gamma)."""
    import mpmath as mp
    return float(mp.gammainc(k / 2, x / 2, mp.inf, regularized=True))

def p_to_z(p):
    """two-sided Gaussian equivalent."""
    import mpmath as mp
    return float(mp.sqrt(2) * mp.erfinv(1 - p))
