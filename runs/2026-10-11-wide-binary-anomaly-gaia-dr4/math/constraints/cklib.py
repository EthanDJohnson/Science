"""Shared helpers for the constraints-lens math checks (written independently of the lens's calc scripts).

MOND: QUMOND g = nu(|g_N|/a0) g_N.  Families: nu_n(y) = (1/2 + sqrt(1/4 + y^-n))^(1/n)
(n = 1 'simple', n = 2 'standard'); MLS nu(y) = 1/(1 - exp(-sqrt(y))).
Kepler MC: units G M = 1, a = 1; isotropic orientation; uniform mean anomaly.
"""
import sys
import numpy as np
import mpmath as mp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity  # noqa: E402

A0 = 1.2e-10  # m s^-2


def nu_n(y, n):
    return (0.5 + mp.sqrt(0.25 + mp.power(y, -n))) ** (mp.mpf(1) / n)


def nu_mls(y):
    return 1 / (1 - mp.exp(-mp.sqrt(y)))


def NU(name):
    if name == "simple":
        return lambda y: nu_n(y, 1)
    if name == "standard":
        return lambda y: nu_n(y, 2)
    if name == "n1.5":
        return lambda y: nu_n(y, mp.mpf("1.5"))
    if name == "MLS":
        return nu_mls
    raise ValueError(name)


def ef_state(name, gext_over_a0):
    """Return y_e = g_Ne/a0, nu_e, K = dln nu/dln y at y_e."""
    nu = NU(name)
    ye = mp.findroot(lambda y: y * nu(y) - gext_over_a0, (mp.mpf(gext_over_a0) ** 2 / 100, mp.mpf(gext_over_a0)), solver="illinois")
    K = mp.diff(lambda t: mp.log(nu(mp.e ** t)), mp.log(ye))
    return ye, nu(ye), K


def qumond_ef(name, gx):
    ye, nue, K = ef_state(name, gx)
    return nue * (1 + K / 3)


def aqual_ef(name, gx):
    ye, nue, K = ef_state(name, gx)
    mue = 1 / nue
    L = -K / (1 + K)  # dln mu / dln x, with x = y nu(y)
    f = lambda c: 1 / (mue * mp.sqrt(1 + L) * mp.sqrt((1 - c * c) + c * c / (1 + L)))
    return mp.quad(f, [-1, 1]) / 2


def sphere_boost(name, h, gNe):
    """Exact QUMOND sphere-averaged radial boost; h = GM/r^2 / a0, gNe = Newtonian EF / a0 along z."""
    nu = NU(name)

    def integrand(c):
        gx2 = h * h * (1 - c * c)
        gz = gNe - h * c
        mag = mp.sqrt(gx2 + gz * gz)
        return nu(mag) * (gNe * c - h)

    pts = [-1, 1]
    c0 = gNe / h
    if -1 < c0 < 1:
        pts = [-1, c0, 1]
    avg = mp.quad(integrand, pts) / 2
    return -avg / h


def q(got, want, tol, label=""):
    if label:
        print(f"  {label}: computed {float(got):.6g} vs lens {want}")
    return quantity(f"{float(got):.12g}", f"{want}", rel_tol=tol)


# ---------------- Kepler Monte Carlo ----------------

def rand_rot(n, rng):
    qv = rng.normal(size=(n, 4))
    qv /= np.linalg.norm(qv, axis=1)[:, None]
    w, x, y, z = qv.T
    R = np.empty((n, 3, 3))
    R[:, 0, 0] = 1 - 2 * (y * y + z * z); R[:, 0, 1] = 2 * (x * y - z * w); R[:, 0, 2] = 2 * (x * z + y * w)
    R[:, 1, 0] = 2 * (x * y + z * w); R[:, 1, 1] = 1 - 2 * (x * x + z * z); R[:, 1, 2] = 2 * (y * z - x * w)
    R[:, 2, 0] = 2 * (x * z - y * w); R[:, 2, 1] = 2 * (y * z + x * w); R[:, 2, 2] = 1 - 2 * (x * x + y * y)
    return R


def draw_e(n, law, rng):
    if law == "circular":
        return np.zeros(n)
    if law == "uniform":
        alpha = 0.0
    elif law == "thermal":
        alpha = 1.0
    else:
        alpha = float(law)
    return rng.random(n) ** (1.0 / (alpha + 1.0))


def kepler(n, law, rng):
    """Return 3D position and velocity arrays (GM = 1, a = 1), sky = (x, y), LOS = z."""
    e = draw_e(n, law, rng)
    M = rng.uniform(0, 2 * np.pi, n)
    E = M.copy()
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    r = 1 - e * np.cos(E)
    b = np.sqrt(1 - e * e)
    pos = np.stack([np.cos(E) - e, b * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-np.sin(E) / r, b * np.cos(E) / r, np.zeros(n)], 1)
    R = rand_rot(n, rng)
    pos = np.einsum("nij,nj->ni", R, pos)
    vel = np.einsum("nij,nj->ni", R, vel)
    return pos, vel


def vt_sample(n, law, rng, beta=0.6):
    """Projected s, normalised sky velocity vector (2D, units of sqrt(GM/s)), weight (s/a)^beta, 3D r, pos."""
    pos, vel = kepler(n, law, rng)
    s = np.hypot(pos[:, 0], pos[:, 1])
    vt_vec = vel[:, :2] * np.sqrt(s)[:, None]
    w = s ** beta
    r = np.linalg.norm(pos, axis=1)
    return s, vt_vec, w, r, pos


def wquant(x, w, qs):
    i = np.argsort(x)
    xs, ws = x[i], w[i]
    c = np.cumsum(ws) - 0.5 * ws
    c /= ws.sum()
    return np.interp(qs, c, xs)


def wmed(x, w):
    return float(wquant(x, w, 0.5))
