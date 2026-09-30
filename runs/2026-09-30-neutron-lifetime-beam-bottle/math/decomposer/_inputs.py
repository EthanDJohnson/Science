"""My own transcription of the dossier inputs (lifetimes in s, SI; lambda, Vud dimensionless).
Asymmetric errors are symmetrised as the mean of the two sides (the lens's stated convention)."""
import math

def q(*a):
    return math.sqrt(sum(x * x for x in a))

# value, total sigma (stat (+) sys)
BL1 = (887.7, q(1.2, 1.9))                 # D-20
SIL = (889.2, q(3.0, 3.8))                 # D-22 (lead)
JP = 877.2; JP_STAT = 1.7; JP_UP = 4.0; JP_DN = 3.6   # D-23
JPARC = (JP, q(JP_STAT, (JP_UP + JP_DN) / 2))
UCNT = (877.82, q(0.22, (0.20 + 0.17) / 2))  # D-27
EZHOV = (878.3, q(1.6, 1.0))               # D-30
GRAV = (881.5, q(0.7, 0.6))                # D-28
SER05 = (878.5, q(0.7, 0.3))               # D-29
MAMBO = (880.7, q(1.3, 1.2))
STEY = (882.5, q(1.4, 1.5))
ARZ = (880.2, 1.2)
MAGNETIC = [UCNT, EZHOV]
MATERIAL = [GRAV, SER05, MAMBO, STEY, ARZ]
STORAGE = MAGNETIC + MATERIAL
PROTON = [BL1, SIL]

def wmean(items):
    w = [1 / s ** 2 for _, s in items]
    W = sum(w)
    m = sum(wi * x for wi, (x, _) in zip(w, items)) / W
    chi2 = sum(wi * (x - m) ** 2 for wi, (x, _) in zip(w, items))
    n = len(items)
    S = max(1.0, math.sqrt(chi2 / (n - 1))) if n > 1 else 1.0
    return m, 1 / math.sqrt(W), chi2, S

def z(a, b):
    return abs(a[0] - b[0]) / q(a[1], b[1])

def p2(zv):
    return math.erfc(zv / math.sqrt(2))

def chi2_sf(x, k):
    import mpmath as mp
    return float(mp.gammainc(k / 2.0, x / 2.0, mp.inf, regularized=True))

def z_from_p(p):
    import mpmath as mp
    return float(mp.sqrt(2) * mp.erfinv(1 - mp.mpf(p)))

def near(label, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"{'PASS' if ok else 'FAIL'} {label}: got {got:.6g}, lens {want}, tol {tol}")
    return ok
