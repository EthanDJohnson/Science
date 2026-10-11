"""Independent Kepler sampler for the dialectician math checks (written from the two-body equations,
not from the run's generator). Units: G = M = 1 (scale-free); returns normalised velocity
v~ = v_p / sqrt(G M / s), which does not depend on a or M for a pure Kepler orbit."""
import numpy as np


def sample_e(n, kind, rng, alpha=None):
    """f(e) ~ e^alpha on [0, 1): uniform alpha = 0, thermal alpha = 1."""
    if kind == "uniform":
        alpha = 0.0
    elif kind == "thermal":
        alpha = 1.0
    u = rng.random(n)
    return np.minimum(u ** (1.0 / (alpha + 1.0)), 0.999)


def solve_kepler(M, e):
    E = M + e * np.sin(M)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def random_rotations(n, rng):
    q = rng.standard_normal((n, 4))
    q /= np.linalg.norm(q, axis=1)[:, None]
    w, x, y, z = q.T
    R = np.empty((n, 3, 3))
    R[:, 0, 0] = 1 - 2 * (y * y + z * z); R[:, 0, 1] = 2 * (x * y - z * w); R[:, 0, 2] = 2 * (x * z + y * w)
    R[:, 1, 0] = 2 * (x * y + z * w); R[:, 1, 1] = 1 - 2 * (x * x + z * z); R[:, 1, 2] = 2 * (y * z - x * w)
    R[:, 2, 0] = 2 * (x * z - y * w); R[:, 2, 1] = 2 * (y * z + x * w); R[:, 2, 2] = 1 - 2 * (x * x + y * y)
    return R


def kepler_vtilde(n, e, rng, gamma=1.0, return_all=False):
    """Random mean anomaly, isotropic orientation, a = 1, G M = 1; velocities scaled by sqrt(gamma)."""
    M = rng.uniform(0, 2 * np.pi, n)
    E = solve_kepler(M, e)
    rr = 1 - e * np.cos(E)
    pos = np.stack([np.cos(E) - e, np.sqrt(1 - e * e) * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-np.sin(E) / rr, np.sqrt(1 - e * e) * np.cos(E) / rr, np.zeros(n)], 1) * np.sqrt(gamma)
    R = random_rotations(n, rng)
    P = np.einsum("nij,nj->ni", R, pos)
    V = np.einsum("nij,nj->ni", R, vel)
    s = np.hypot(P[:, 0], P[:, 1])
    vp = np.hypot(V[:, 0], V[:, 1])
    vt = vp / np.sqrt(1.0 / s)
    if return_all:
        return vt, s, rr, np.linalg.norm(V, axis=1)
    return vt


def gamma_profile(vt_obs, vt_tmpl, ps=(0.3, 0.5, 0.8)):
    qo = np.quantile(vt_obs, ps)
    qt = np.quantile(vt_tmpl, ps)
    return (qo / qt) ** 2
