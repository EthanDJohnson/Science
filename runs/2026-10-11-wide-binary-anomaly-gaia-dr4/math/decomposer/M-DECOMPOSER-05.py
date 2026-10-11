"""M-DECOMPOSER-04 and -05: independent noise-free Kepler Monte Carlo for pure binaries.

Model (built here from Kepler's laws, not the run's generator): units G M = a = 1 (Kepler orbits
are self-similar, so the v~ distribution does not depend on a or M). e ~ f(e) propto e^alpha on
[0, 0.999]; mean anomaly uniform; isotropic orientation (uniform random rotation via a unit
quaternion). s = sky-projected separation, v_p = sky-projected relative speed,
v~ = v_p / sqrt(gam G M / s) * sqrt(gam) = v_p_true / sqrt(G M / s) where MOND is approximated as
Keplerian with G -> gam G (velocities scale by sqrt(gam) at fixed positions).

M-04 claims (lens calc C, TEST bin, DR3 noise, HTZ template): gamma_app = (med v~_truth /
med v~_template)^2 = 0.935 (truth alpha = 2), 1.063 (thermal), 1.305 (uniform); CAL: 0.865, 0.997,
1.246; differentials 1.080 / 1.067 / 1.048.  HTZ alpha in the TEST bin (s ~ 5-17 kau for 1-2 Msun
at 10^-10.5..10^-9.5 m/s^2; log10 a ~ 3.7-4.25) is ~1.17-1.32; in the CAL bin (0.2-1.7 kau)
~0.8-1.3.  Here: template alpha_T in {1.2, 1.25, 1.3} (TEST) and alpha_C in {0.95, 1.05, 1.15} (CAL).
M-05 claims (calc D): P(v~ > sqrt2) for pure MOND binaries with mean gam 1.291 / 1.266 = 0.0125 /
0.0108; truncating at sqrt2 lowers the median by 0.9%; v~ <= sqrt(2 gam) always.
Self-tests: v~ <= sqrt2 (Newton), <r> = a(1 + <e^2>/2), <sin theta> = pi/4, energy.
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, inequality, finish

rng = np.random.default_rng(20261011)
N = 1_000_000

def kepler_E(M, e):
    E = M + e * np.sin(M)
    E = np.where(e > 0.8, np.pi * np.ones_like(M), E)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def quat_rot(n):
    q = rng.standard_normal((n, 4)); q /= np.linalg.norm(q, axis=1)[:, None]
    w, x, y, z = q.T
    R = np.empty((n, 3, 3))
    R[:, 0] = np.stack([1-2*(y*y+z*z), 2*(x*y-w*z), 2*(x*z+w*y)], 1)
    R[:, 1] = np.stack([2*(x*y+w*z), 1-2*(x*x+z*z), 2*(y*z-w*x)], 1)
    R[:, 2] = np.stack([2*(x*z-w*y), 2*(y*z+w*x), 1-2*(x*x+y*y)], 1)
    return R

def sample(alpha, n=N):
    e = np.minimum(rng.random(n) ** (1.0 / (alpha + 1.0)), 0.999)
    M = rng.uniform(0, 2 * np.pi, n)
    E = kepler_E(M, e)
    sq = np.sqrt(1 - e * e)
    pos = np.stack([np.cos(E) - e, sq * np.sin(E), np.zeros(n)], 1)
    den = 1 - e * np.cos(E)
    vel = np.stack([-np.sin(E) / den, sq * np.cos(E) / den, np.zeros(n)], 1)
    R = quat_rot(n)
    P = np.einsum("nij,nj->ni", R, pos); V = np.einsum("nij,nj->ni", R, vel)
    r = np.linalg.norm(pos, axis=1); v = np.linalg.norm(vel, axis=1)
    s = np.hypot(P[:, 0], P[:, 1]); vp = np.hypot(V[:, 0], V[:, 1])
    return dict(e=e, r=r, v=v, s=s, vt=vp / np.sqrt(1.0 / s), sin_theta=s / r)


# ---- M-05 (and noise sensitivity of M-04): add a simple, independent DR3-like noise model ----
# Relative PM noise per axis: sqrt(2) * 0.05 mas/yr (DR3 per-star per-axis, quoted in the brief's
# calculator spec; SI conversion v = 4.74047 km/s * mu[arcsec/yr] * d[pc]). d ~ p(d) propto d^2 on
# 10-200 pc; M_tot log-uniform 1-2 Msun; s log-uniform within the TEST bin
# 10^-10.5 < G M / s^2 <= 10^-9.5 m/s^2. Noise is isotropic in the sky plane, so
# v~_obs = sqrt((v~ + n1)^2 + n2^2), n_i ~ N(0, sigma_v / v_c(s)).
GMsun, AU = 1.32712440018e20, 1.495978707e11
def noisy(vt, n):
    d = (10**3 + (200**3 - 10**3) * rng.random(n)) ** (1 / 3)
    M = 10 ** rng.uniform(0, np.log10(2), n)
    gN = 10 ** rng.uniform(-10.5, -9.5, n)
    s = np.sqrt(GMsun * M / gN)
    vc = np.sqrt(GMsun * M / s)                       # m/s
    sig = 4.74047e3 * (np.sqrt(2) * 0.05e-3) * d       # m/s per axis
    k = sig / vc
    n1, n2 = rng.standard_normal(n) * k, rng.standard_normal(n) * k
    return np.sqrt((vt + n1) ** 2 + n2 ** 2), np.median(k)

base = sample(1.25)
vtN, kmed = noisy(base["vt"], N)
print(f"median noise sigma in v~ units per axis: {kmed:.3f}")
print(f"Newton noisy: P(v~>sqrt2) = {np.mean(vtN > np.sqrt(2)):.4f} (lens 0.0021); median {np.median(vtN):.4f} (lens 0.5393)")
for gam, claim in ((1.291, 0.0125), (1.266, 0.0108)):
    vt, _ = noisy(base["vt"] * np.sqrt(gam), N)
    frac = np.mean(vt > np.sqrt(2)); m_all = np.median(vt); m_cut = np.median(vt[vt <= np.sqrt(2)])
    print(f"gam={gam} noisy: P(v~>sqrt2) = {frac:.4f} (lens {claim}); median {m_all:.4f} -> {m_cut:.4f} ({(m_cut/m_all-1)*100:.2f}%)")
    inequality(f"{frac}", "<", "0.03")             # substance: only a few % of pairs above sqrt2
    inequality(f"{abs(m_cut / m_all - 1)}", "<", "0.015")   # truncation moves the median by < 1.5%
    inequality(f"{(m_all / np.median(vtN)) ** 2}", ">", f"{gam - 0.08}")   # boost survives in the median
# noise-free reference
vt0 = base["vt"] * np.sqrt(1.291)
print(f"noise-free gam=1.291: P = {np.mean(vt0 > np.sqrt(2)):.4f}")

# eccentricity ratios with the same noise (template alpha = 1.27, the HTZ TEST-bin value)
tmpl, _ = noisy(sample(1.27)["vt"], N)
mt = np.median(tmpl)
for name, al, lens in (("alpha2", 2.0, 0.935), ("thermal", 1.0, 1.063), ("uniform", 0.0, 1.305)):
    v, _ = noisy(sample(al)["vt"], N)
    g = (np.median(v) / mt) ** 2
    v0 = sample(al)["vt"]; g0 = (np.median(v0) / np.median(sample(1.27)["vt"])) ** 2
    print(f"TEST {name}: noisy {g:.3f}, noise-free {g0:.3f}, lens {lens}")
raise SystemExit(finish())
