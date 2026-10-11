"""Small independent statistics helpers for the statistician math check (mpmath only)."""
import mpmath as mp

mp.mp.dps = 30


def p2(z):
    """two-sided normal tail probability"""
    return float(mp.erfc(mp.mpf(z) / mp.sqrt(2)))


def z2(p):
    """z for a two-sided p"""
    return float(mp.sqrt(2) * mp.erfinv(1 - mp.mpf(p)))


def chi2_sf(x, k):
    """upper tail of chi2 with k dof"""
    return float(mp.gammainc(mp.mpf(k) / 2, mp.mpf(x) / 2, mp.inf, regularized=True))


def wmean(vals, errs):
    w = [1 / e**2 for e in errs]
    m = sum(wi * v for wi, v in zip(w, vals)) / sum(w)
    s = sum(w) ** -0.5
    chi = sum(((v - m) / e) ** 2 for v, e in zip(vals, errs))
    return m, s, chi


def report(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"{'OK ' if ok else 'BAD'} {name}: got {got:.4g}, lens {want:.4g} (tol {tol:g})")
    return ok
