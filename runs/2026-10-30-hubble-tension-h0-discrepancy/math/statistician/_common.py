"""Shared helpers for the statistician math checks (independent of the lens's scripts).

All H0 values in km/s/Mpc (SI-derived astronomical units), taken as quoted in dossier.md.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
from math_checks import inequality

mp.mp.dps = 40


def p2_of_z(z):
    """Two-sided Gaussian tail probability."""
    return mp.erfc(mp.mpf(z) / mp.sqrt(2))


def z_of_p2(p):
    """Inverse of p2_of_z by bisection in log space."""
    p = mp.mpf(p)
    lo, hi = mp.mpf(0), mp.mpf(40)
    for _ in range(200):
        mid = (lo + hi) / 2
        if mp.log(p2_of_z(mid)) > mp.log(p):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def chi2_sf(x, k):
    return mp.gammainc(mp.mpf(k) / 2, mp.mpf(x) / 2, mp.inf, regularized=True)


def quad(*errs):
    return mp.sqrt(sum(mp.mpf(e) ** 2 for e in errs))


def tension(a, a_up, a_dn, b, b_up, b_dn, rho=0.0):
    """Two-sided tension a vs b; each side uses the error facing the other value."""
    a, b = mp.mpf(a), mp.mpf(b)
    sa = mp.mpf(a_dn if a > b else a_up)
    sb = mp.mpf(b_up if a > b else b_dn)
    var = sa ** 2 + sb ** 2 - 2 * rho * sa * sb
    return abs(a - b) / mp.sqrt(var)


def wmean(vals, sigs):
    w = [1 / mp.mpf(s) ** 2 for s in sigs]
    m = sum(wi * mp.mpf(v) for wi, v in zip(w, vals)) / sum(w)
    chi2 = sum(wi * (mp.mpf(v) - m) ** 2 for wi, v in zip(w, vals))
    return m, 1 / mp.sqrt(sum(w)), chi2


def close(label, mine, claimed, tol):
    """PASS if |mine - claimed| <= tol."""
    mine = float(mine)
    print(f"  {label}: mine = {mine:.6g}, lens = {claimed}, tol = {tol}")
    return inequality(f"Abs({mine!r} - ({claimed}))", "<=", repr(float(tol)))
