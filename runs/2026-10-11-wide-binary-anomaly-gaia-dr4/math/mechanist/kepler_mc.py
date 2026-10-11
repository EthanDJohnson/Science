"""Independent Keplerian projection Monte Carlo (written for the math check; not the run's generator).
Units: G M = 1, lengths in units of a unless a is passed. Returns sky-projected s, v_p and ṽ = v_p / sqrt(GM/s)."""
import numpy as np

def sample_e(rng, alpha, n):
    # p(e) ∝ e^alpha on [0, 1): inverse CDF e = u^(1/(alpha+1)); alpha may be an array
    return rng.random(n) ** (1.0 / (np.asarray(alpha) + 1.0))

def kepler_E(Mean, e):
    E = Mean + e * np.sin(Mean)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - Mean) / (1 - e * np.cos(E))
    return E

def project(rng, a, e, GM=1.0):
    n = len(e)
    Mean = rng.random(n) * 2 * np.pi
    E = kepler_E(Mean, e)
    nn = np.sqrt(GM / a**3)
    den = 1 - e * np.cos(E)
    pos = np.stack([a * (np.cos(E) - e), a * np.sqrt(1 - e**2) * np.sin(E), np.zeros(n)], 1)
    vel = np.stack([-a * nn * np.sin(E) / den, a * nn * np.sqrt(1 - e**2) * np.cos(E) / den, np.zeros(n)], 1)
    # uniform random rotation via random unit quaternion
    q = rng.normal(size=(n, 4)); q /= np.linalg.norm(q, axis=1)[:, None]
    w, x, y, z = q.T
    R = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]]).transpose(2, 0, 1)
    P = np.einsum("nij,nj->ni", R, pos); V = np.einsum("nij,nj->ni", R, vel)
    r = np.linalg.norm(pos, axis=1); v = np.linalg.norm(vel, axis=1)
    s = np.linalg.norm(P[:, :2], axis=1); vp2 = V[:, :2]
    vt = vp2 / np.sqrt(GM / s)[:, None]
    return dict(s=s, r=r, v=v, a=a, vt_vec=vt, vt=np.linalg.norm(vt, axis=1), cos_inc=P[:, 2] / r)
