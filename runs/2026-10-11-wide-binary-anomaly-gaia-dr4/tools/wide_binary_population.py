#!/usr/bin/env python3
"""Synthetic Gaia-like wide-binary catalogues, Newtonian or with a parametrised MOND boost (numpy only).

WHAT IT COMPUTES
  A catalogue of ~1e5 wide pairs as Gaia would see them: projected separation s, sky-projected
  relative velocity v_p, a luminosity-based total-mass estimate M_est, a parallax distance, a
  g_N proxy, and flags for contaminants and hidden companions. The truth (a, e, r, gamma, true
  masses, true velocities) is returned alongside, so an estimator can be scored against it.
  Built for injection-recovery tests of wide-binary gravity estimators (run
  2026-10-11-wide-binary-anomaly-gaia-dr4).

MODEL (SI units throughout the Python API)
  1. Wide orbit: Kepler two-body orbit of total mass M = M_A + M_B (each component's true mass
     includes any hidden inner companion), with G replaced by G_eff = gamma * G:
        mean anomaly Mm ~ U(0, 2 pi)  (uniform in time),  Mm = E - e sin E,
        r = a (1 - e cos E),   |v|^2 = gamma G M (2/r - 1/a)   (vis-viva with G_eff).
     APPROXIMATION (labelled): real MOND with the Galactic external field effect (EFE) is
     non-linear and anisotropic; "Kepler with G_eff = gamma(g_N) G" is the pseudo-Newtonian
     approximation used by Chae 2023/2024 (no elliptical-orbit AQUAL/QUMOND solutions exist,
     Chae 2024 ApJ 972, 186). gamma is one number per orbit, evaluated at g_N = G M / a_eval^2,
     with a_eval = a (default) or the time-averaged separation a (1 + e^2/2).
  2. Orientation: isotropic (uniform random rotation, Shoemake quaternions); the sky plane is
     (x, y), the line of sight z. s = |(x, y)|, v_p = |(v_x, v_y)|.
  3. Eccentricity f(e): "thermal" f = 2e; "uniform"; "power" f ~ e^alpha (alpha given);
     "htz": f ~ e^alpha(a) with alpha interpolated (in log10 a) through Hwang, Ting & Zakamska
     2022 (MNRAS 512, 3383) Table 1 bin centres, clamped outside 10^1.75 - 10^4.25 au. HTZ bin
     by separation; we use a as the proxy because e must be drawn before s exists (approximation).
     "circular": e = 0.
  4. Population: d uniform in volume in [d_min, d_max]; primary mass dN/dm ~ m^-2.3 on
     [m_min, m_max]; q = m_B/m_A ~ U(q_min, 1) (floor 0.08 Msun); dN/da ~ a^-1.6 on
     [a_min, a_max] (assumed population shape, not fitted); pairs are kept if the OBSERVED s lies
     in [s_min, s_max].
  5. Hidden companions (hierarchical triples): with probability f_triple one wide component
     (A or B at random) is an unresolved inner binary, m_2 = q_in m_1, q_in ~ U(q_in_min, 1),
     a_in log-uniform in [a_in_min, min(a_in_max, f_stab a (1 - e))] (crude stability cut,
     f_stab = 0.3 by default), e_in thermal, isotropic orientation, random phase. Photocentre of
     the inner pair relative to its centre of mass (Belokurov et al. 2020 MNRAS 496, 1922 eq. 4):
        x_phot = (l/(1+l) - q/(1+q)) r_rel,   l = L_2/L_1 = q_in^alpha_L   (L ~ m^alpha_L).
     Gaia-baseline averaging: the photocentre is sampled at n_epoch epochs evenly spread over the
     baseline T (DR3 34 months, DR4 66 months) and its proper motion is the least-squares slope;
     the photocentre's mean offset is added to the separation. `wobble_mas` is the rms residual
     of the photocentre about that linear fit, in mas (a RUWE-like detectability proxy).
  6. Contaminants (fractions of the final catalogue):
     chance alignments: s drawn with p(s) ~ s on [s_min, s_max] (uniform surface density),
     relative v_p from a 2D Gaussian with per-axis sigma_chance (default 25 km/s);
     unbound comoving pairs: s as for binaries, v_p from a 2D Gaussian with per-axis
     sigma_unbound (default 0.5 km/s). Both are phenomenological.
  7. Mass estimates: each visible source gets m_est = (sum of its luminosities)^(1/alpha_L) in
     solar units (a single main-sequence star read off L ~ m^alpha_L, alpha_L = 3.5 as in
     Belokurov et al. 2020 Fig. 3), times a lognormal error exp(sigma_lnM N(0,1)) and a common
     multiplicative bias mass_bias. An unresolved companion therefore makes M_est < M_true.
  8. Gaia noise: each star gets Gaussian proper-motion noise sigma_mu per axis and parallax
     noise sigma_plx; the TRUE noise is err_inflate times the QUOTED error (El-Badry et al. 2021
     found formal errors ~30% too small). Pair parallax = mean of the two. d_obs = 1/plx_obs,
     s_obs = theta * d_obs, v_p,obs = |mu_rel,obs| * d_obs (4.740470 km/s per (mas/yr * kpc)).
     Release presets: DR3 sigma_mu = 0.05 mas/yr, sigma_plx = 0.05 mas (a mid value; Gaia DR3
     medians are 0.02-0.03 at G = 9-14 and ~0.5 at G = 20, so vary these); DR4 scales them by
     (34/66)^1.5 (proper motion) and (34/66)^0.5 (parallax), the usual baseline scaling.
  9. MOND boost gamma(g_N) (SPECULATIVE physics, labelled), Chae & Milgrom 2022 / Chae 2024
     eq. 22 form, with interpolating-function family nu_n:
        nu_n(y) = [(1 + sqrt(1 + 4 y^-n)) / 2]^(1/n)   (n = 1 "simple", n = 2 "standard")
        K(y)    = dln nu / dln y = -2 y^-n / (w (1 + w)),  w = sqrt(1 + 4 y^-n)
        y_e     = x_e^2 / (1 + x_e^n)^(1/n)      (Newtonian EF from true EF x_e = g_ext/a0,
                                                  i.e. y_e nu(y_e) = x_e, QUMOND)
        y_b     = sqrt(y^2 + (beta y_e)^2),  y = g_N / a0
        gamma   = nu(y_b) [1 + tanh(beta y_e / y)^p K(y_b) / 3].
     Limits: y >> 1 -> 1 (Newton); g_ext = 0 -> nu(y) -> y^-1/2 (deep MOND, g = sqrt(a0 g_N));
     y << y_e with beta = 1 -> nu_ext (1 + K0/3) = eta, Banik & Zhao 2018 (MNRAS 480, 2660)
     eq. 16, the angle-averaged EF-dominated QUMOND boost. Presets:
        "bz18_simple"   n=1, beta=1,   p=1.2, g_ext = (232.8 km/s)^2 / 8.2 kpc = 2.142e-10 m/s^2
        "bz18_standard" n=2, beta=1,   p=1.2, same g_ext
        "chae2024"      n=1, beta=1.1, p=1.2, g_ext = 1.90 a0 (Chae: deep value G_eff ~ 1.37 G)
        "isolated"      n=1, g_ext = 0
     a0 = 1.2e-10 m/s^2 by default. For the bz18 presets only the EF limit is BZ18's; the shape
     of the transition (beta, p) is borrowed from the Chae form. BZ18 Table 3 asymptotes:
     simple 1.4228 (QUMOND) / 1.4056 (AQUAL), standard 1.0726 / 1.0661. NOTE: the brief's
     "~1.44 deep" for the simple function isn't the Table 3 value; Table 3 gives 1.4228, and the
     anisotropic EF-limit boost ranges from nu_ext (1 + K0/2) = 1.354 to nu_ext = 1.560
     (efe_limit()).

ASSUMPTIONS AND VALIDITY
  Hierarchical (point-mass) wide orbit; inner binaries only perturb the photocentre and mass.
  No perspective-rotation or radial-velocity terms, no Galactic tide, no wide-orbit motion over
  the baseline (P_wide >~ 1e3 yr). Unbound contaminants are not integrated. Main-sequence
  power-law mass-luminosity relation. Valid for 50 au <~ s <~ 1e5 au, d <~ 1 kpc,
  0 <= e < 1, gamma > 0. Inputs outside these ranges raise ValueError.

UNITS
  Python API: SI (m, s, kg, m/s, m/s^2); proper-motion and parallax errors in mas/yr and mas as
  named. Command line accepts unit strings through unit_tools.Q.

PYTHON
  import sys; sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/tools")
  import wide_binary_population as wbp
  cat = wbp.generate(100000, gravity="bz18_simple", ecc="htz", f_triple=0.2, release="DR3", seed=1)
  cat["s"], cat["v_p"], cat["M_est"], cat["distance"], cat["gN"], cat["flags"]
  wbp.gamma_mond(1e-10, model="bz18_simple")          # -> ~1.38 (dimensionless)

COMMAND LINE
  python3 runs/2026-10-11-wide-binary-anomaly-gaia-dr4/tools/wide_binary_population.py selftest
  python3 runs/2026-10-11-wide-binary-anomaly-gaia-dr4/tools/wide_binary_population.py gamma --gN "1e-10 m/s^2" --model bz18_simple
  python3 runs/2026-10-11-wide-binary-anomaly-gaia-dr4/tools/wide_binary_population.py generate --n 100000 --gravity 1.0 --ecc htz --f-triple 0.2 --release DR3 --seed 1 [--out cat.npz]
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
try:
    from unit_tools import Q  # noqa: E402
except Exception:  # pragma: no cover - toolkit missing
    Q = None

# ---------------------------------------------------------------- constants (SI)
G = 6.67430e-11                      # m^3 kg^-1 s^-2, CODATA 2018
MSUN = 1.3271244e20 / G              # kg, IAU 2015 nominal GM_sun / G
AU = 1.495978707e11                  # m, IAU 2012 exact
PC = AU * 648000.0 / math.pi         # m, IAU exact definition
KPC = 1e3 * PC
YR = 365.25 * 86400.0                # s, Julian year
MAS = math.pi / 180.0 / 3600.0 / 1000.0   # rad
MASYR = MAS / YR                     # rad/s per (mas/yr)
A0_DEFAULT = 1.2e-10                 # m/s^2
GEXT_BZ18 = (232.8e3) ** 2 / (8.2 * KPC)  # m/s^2, BZ18 sec 3.6: v_LSR = 232.8 km/s, R0 = 8.2 kpc

FLAG_TRIPLE_A = 1
FLAG_TRIPLE_B = 2
FLAG_CHANCE = 4
FLAG_UNBOUND = 8

# Hwang, Ting & Zakamska 2022 Table 1: (log10 sep [au] bin centre, alpha), quoted in dossier RT-16
HTZ_TABLE = np.array([
    (1.75, 0.08), (2.125, 0.59), (2.375, 0.82), (2.625, 0.94),
    (2.875, 1.20), (3.25, 1.30), (3.75, 1.32), (4.25, 1.17)])

RELEASES = {
    # sigma_mu [mas/yr per axis per star], sigma_plx [mas], baseline [s]
    "DR3": dict(sigma_mu=0.05, sigma_plx=0.05, baseline=34.0 / 12.0 * YR),
    "DR4": dict(sigma_mu=0.05 * (34.0 / 66.0) ** 1.5, sigma_plx=0.05 * (34.0 / 66.0) ** 0.5,
                baseline=66.0 / 12.0 * YR),
}

MOND_PRESETS = {
    "bz18_simple": dict(n=1.0, beta=1.0, p=1.2, g_ext=GEXT_BZ18),
    "bz18_standard": dict(n=2.0, beta=1.0, p=1.2, g_ext=GEXT_BZ18),
    "chae2024": dict(n=1.0, beta=1.1, p=1.2, g_ext=1.90 * A0_DEFAULT),
    "isolated": dict(n=1.0, beta=1.0, p=1.2, g_ext=0.0),
}


# ---------------------------------------------------------------- MOND boost
def nu_n(y, n=1.0):
    """QUMOND interpolating function nu_n(y) = [(1 + sqrt(1 + 4 y^-n))/2]^(1/n); y = g_N/a0 > 0."""
    y = np.asarray(y, dtype=float)
    if np.any(y <= 0) or n <= 0:
        raise ValueError("nu_n needs y > 0 and n > 0")
    return ((1.0 + np.sqrt(1.0 + 4.0 * y ** (-n))) / 2.0) ** (1.0 / n)


def k_log_slope(y, n=1.0):
    """K(y) = dln nu_n / dln y = -2 y^-n / (w (1 + w)), w = sqrt(1 + 4 y^-n). -1/2 deep, 0 Newtonian."""
    y = np.asarray(y, dtype=float)
    if np.any(y <= 0):
        raise ValueError("K needs y > 0")
    yn = y ** (-n)
    w = np.sqrt(1.0 + 4.0 * yn)
    return -2.0 * yn / (w * (1.0 + w))


def newtonian_ext(x_e, n=1.0):
    """Newtonian-equivalent external field y_e from the true one x_e (units of a0): y_e nu_n(y_e) = x_e."""
    x_e = float(x_e)
    if x_e < 0:
        raise ValueError("external field must be >= 0")
    return x_e ** 2 / (1.0 + x_e ** n) ** (1.0 / n)


def _mond_params(model, a0, g_ext, n, beta, p):
    if model not in MOND_PRESETS:
        raise ValueError(f"unknown MOND model {model!r}; choose from {sorted(MOND_PRESETS)}")
    par = dict(MOND_PRESETS[model])
    for k, v in (("g_ext", g_ext), ("n", n), ("beta", beta), ("p", p)):
        if v is not None:
            par[k] = float(v)
    if a0 <= 0 or par["g_ext"] < 0 or par["n"] <= 0 or par["beta"] <= 0 or par["p"] <= 0:
        raise ValueError("need a0 > 0, g_ext >= 0, n > 0, beta > 0, p > 0")
    return par


def gamma_mond(gN, model="bz18_simple", a0=A0_DEFAULT, g_ext=None, n=None, beta=None, p=None):
    """SPECULATIVE. MOND boost gamma = g/g_N (dimensionless) at Newtonian internal acceleration gN [m/s^2].

    gamma = nu(y_b)[1 + tanh(beta y_e/y)^p K(y_b)/3], y_b = sqrt(y^2 + (beta y_e)^2) (Chae 2024 eq. 22 form).
    """
    gN = np.asarray(gN, dtype=float)
    if np.any(gN <= 0):
        raise ValueError("gN must be > 0 m/s^2")
    par = _mond_params(model, a0, g_ext, n, beta, p)
    y = gN / a0
    y_e = newtonian_ext(par["g_ext"] / a0, par["n"])
    yb = np.sqrt(y ** 2 + (par["beta"] * y_e) ** 2)
    t = np.tanh(par["beta"] * y_e / y) ** par["p"]
    out = nu_n(yb, par["n"]) * (1.0 + t * k_log_slope(yb, par["n"]) / 3.0)
    return float(out) if out.ndim == 0 else out


def efe_limit(model="bz18_simple", a0=A0_DEFAULT, g_ext=None, n=None):
    """EF-dominated QUMOND limit (Banik & Zhao 2018 eqs. 15-16): nu_ext, K0, eta = nu_ext(1+K0/3),
    and the anisotropic range nu_ext(1+K0/2) (separation perpendicular to g_ext) .. nu_ext (parallel)."""
    par = _mond_params(model, a0, g_ext, n, None, None)
    if par["g_ext"] <= 0:
        raise ValueError("EF limit needs g_ext > 0")
    y_e = newtonian_ext(par["g_ext"] / a0, par["n"])
    nu_e = float(nu_n(y_e, par["n"]))
    K0 = float(k_log_slope(y_e, par["n"]))
    return dict(x_ext=par["g_ext"] / a0, y_ext=y_e, nu_ext=nu_e, K0=K0, eta=nu_e * (1 + K0 / 3),
                gamma_perp=nu_e * (1 + K0 / 2), gamma_par=nu_e)


# ---------------------------------------------------------------- orbits
def solve_kepler(Mm, e, tol=1e-13, itmax=60):
    """Eccentric anomaly E from mean anomaly Mm (Newton iteration, vectorised; 0 <= e < 1)."""
    Mm = np.asarray(Mm, dtype=float)
    e = np.broadcast_to(np.asarray(e, dtype=float), Mm.shape)
    if np.any((e < 0) | (e >= 1)):
        raise ValueError("eccentricity must be in [0, 1)")
    Mw = np.mod(Mm, 2 * np.pi)
    E = Mw + 0.85 * e * np.sign(np.sin(Mw))
    for _ in range(itmax):
        f = E - e * np.sin(E) - Mw
        dE = f / (1 - e * np.cos(E))
        E = E - dE
        if np.max(np.abs(dE)) < tol:
            break
    return E


def kepler_state(a, e, Mm, mu):
    """Perifocal position (x, y) [m], velocity (vx, vy) [m/s] and r for G_eff M = mu [m^3/s^2]."""
    E = solve_kepler(Mm, e)
    cE, sE = np.cos(E), np.sin(E)
    sq = np.sqrt(1 - e * e)
    x = a * (cE - e)
    y = a * sq * sE
    r = a * (1 - e * cE)
    Edot = np.sqrt(mu / a ** 3) / (1 - e * cE)
    vx = -a * sE * Edot
    vy = a * sq * cE * Edot
    return x, y, vx, vy, r


def random_rotations(n, rng):
    """n uniformly random 3x3 rotation matrices (Shoemake 1992 quaternions), shape (n, 3, 3)."""
    u1, u2, u3 = rng.random((3, n))
    q0 = np.sqrt(1 - u1) * np.sin(2 * np.pi * u2)
    q1 = np.sqrt(1 - u1) * np.cos(2 * np.pi * u2)
    q2 = np.sqrt(u1) * np.sin(2 * np.pi * u3)
    q3 = np.sqrt(u1) * np.cos(2 * np.pi * u3)
    w, x, y, z = q3, q0, q1, q2
    R = np.empty((n, 3, 3))
    R[:, 0, 0] = 1 - 2 * (y * y + z * z); R[:, 0, 1] = 2 * (x * y - z * w); R[:, 0, 2] = 2 * (x * z + y * w)
    R[:, 1, 0] = 2 * (x * y + z * w); R[:, 1, 1] = 1 - 2 * (x * x + z * z); R[:, 1, 2] = 2 * (y * z - x * w)
    R[:, 2, 0] = 2 * (x * z - y * w); R[:, 2, 1] = 2 * (y * z + x * w); R[:, 2, 2] = 1 - 2 * (x * x + y * y)
    return R


def htz_alpha(a):
    """Eccentricity power-law index alpha(a) from Hwang, Ting & Zakamska 2022 Table 1 (a in m)."""
    la = np.log10(np.asarray(a, dtype=float) / AU)
    return np.interp(la, HTZ_TABLE[:, 0], HTZ_TABLE[:, 1])


def sample_ecc(kind, n, rng, a=None, alpha=None, e_max=0.999):
    """Draw eccentricities. kind: thermal | uniform | power (needs alpha) | htz (needs a) | circular."""
    u = rng.random(n)
    if kind == "thermal":
        e = np.sqrt(u)
    elif kind == "uniform":
        e = u
    elif kind == "power":
        if alpha is None or alpha <= -1:
            raise ValueError("power-law eccentricity needs alpha > -1")
        e = u ** (1.0 / (alpha + 1.0))
    elif kind == "htz":
        if a is None:
            raise ValueError("htz eccentricities need semi-major axes")
        e = u ** (1.0 / (htz_alpha(a) + 1.0))
    elif kind == "circular":
        e = np.zeros(n)
    else:
        raise ValueError(f"unknown eccentricity kind {kind!r}")
    return np.minimum(e, e_max)


def photocentre_factor(q, l):
    """Photocentre offset per unit relative separation, computed from luminosity-weighted positions:
    x1 = -q/(1+q) r_rel, x2 = 1/(1+q) r_rel, x_phot = (x1 + l x2)/(1 + l). Returns x_phot / r_rel."""
    q = np.asarray(q, float); l = np.asarray(l, float)
    x1 = -q / (1 + q)
    x2 = 1.0 / (1 + q)
    return (x1 + l * x2) / (1 + l)


def lsq_slope(t, X):
    """Least-squares slope of X (..., n_epoch) against epochs t (n_epoch,)."""
    tc = t - t.mean()
    return (X * tc).sum(-1) / (tc * tc).sum()


def _inner_photocentre(m1, q_in, a_in, e_in, l, T, n_epoch, d, rng):
    """Photocentre velocity (2D, m/s), mean offset (2D, m) and rms wobble (mas) of inner binaries."""
    k = m1.size
    mu = G * m1 * (1 + q_in)
    P = 2 * np.pi * np.sqrt(a_in ** 3 / mu)
    t = np.linspace(0.0, T, n_epoch)
    M0 = rng.random(k) * 2 * np.pi
    Mm = M0[:, None] + 2 * np.pi * t[None, :] / P[:, None]
    x, y, _, _, _ = kepler_state(a_in[:, None], e_in[:, None], Mm, mu[:, None])
    R = random_rotations(k, rng)
    B = photocentre_factor(q_in, l)[:, None]
    X = B * (R[:, 0, 0, None] * x + R[:, 0, 1, None] * y)
    Y = B * (R[:, 1, 0, None] * x + R[:, 1, 1, None] * y)
    vx, vy = lsq_slope(t, X), lsq_slope(t, Y)
    tc = t - t.mean()
    resx = X - X.mean(-1, keepdims=True) - vx[:, None] * tc
    resy = Y - Y.mean(-1, keepdims=True) - vy[:, None] * tc
    wob = np.sqrt((resx ** 2 + resy ** 2).mean(-1)) / d / MAS
    return np.stack([vx, vy], -1), np.stack([X.mean(-1), Y.mean(-1)], -1), wob


# ---------------------------------------------------------------- generator
def _gamma_fn(gravity, a0):
    if callable(gravity):
        return gravity
    if isinstance(gravity, (int, float)):
        g = float(gravity)
        if g <= 0:
            raise ValueError("gamma must be > 0")
        return lambda gN: np.full_like(np.asarray(gN, float), g)
    if isinstance(gravity, str):
        return lambda gN: gamma_mond(gN, model=gravity, a0=a0)
    if isinstance(gravity, dict):
        kw = dict(gravity)
        return lambda gN: gamma_mond(gN, a0=a0, **kw)
    raise ValueError("gravity must be a float, a MOND preset name, a dict of gamma_mond kwargs or a callable")


def _powerlaw(rng, n, lo, hi, slope):
    """Draw from dN/dx ~ x^slope on [lo, hi]."""
    u = rng.random(n)
    if abs(slope + 1) < 1e-12:
        return lo * (hi / lo) ** u
    k = slope + 1
    return (lo ** k + u * (hi ** k - lo ** k)) ** (1 / k)


def generate(n, gravity=1.0, ecc="htz", ecc_alpha=None, f_triple=0.0, f_chance=0.0, f_unbound=0.0,
             release="DR3", sigma_mu=None, sigma_plx=None, baseline=None, err_inflate=1.0,
             noise=True, sigma_lnM=0.05, mass_bias=1.0, alpha_L=3.5,
             s_range=(200 * AU, 30000 * AU), a_range=(50 * AU, 1e5 * AU), a_slope=-1.6,
             m_range=(0.4 * MSUN, 1.2 * MSUN), m_slope=-2.3, q_min=0.2,
             d_range=(10 * PC, 200 * PC), a_in_range=(0.1 * AU, 300 * AU), q_in_min=0.1, f_stab=0.3,
             n_epoch=24, sigma_chance=25e3, sigma_unbound=0.5e3, gamma_at="a", r_over_s=1.2,
             a0=A0_DEFAULT, seed=None):
    """Synthetic wide-binary catalogue of n pairs. Returns a dict of numpy arrays (SI units).

    Main outputs: s [m], v_p [m/s], M_est [kg], distance [m], gN [m/s^2] (= G M_est/(r_over_s s)^2,
    Chae 2024's r ~ 1.2 s proxy), flags (bitmask: 1 triple in A, 2 triple in B, 4 chance, 8 unbound),
    sigma_vp [m/s] (from QUOTED errors). Truth: s_true, v_p_true (photocentre, no noise), v_p_orb
    (wide-orbit CoM velocity), M_true, d_true, a, e, r, gamma, gN_true (= G M_true / r^2), wobble_mas.
    """
    n = int(n)
    if n < 1:
        raise ValueError("n must be >= 1")
    for nm, f in (("f_triple", f_triple), ("f_chance", f_chance), ("f_unbound", f_unbound)):
        if not 0 <= f <= 1:
            raise ValueError(f"{nm} must be in [0, 1]")
    if f_chance + f_unbound > 1:
        raise ValueError("f_chance + f_unbound must be <= 1")
    if release not in RELEASES:
        raise ValueError(f"release must be one of {sorted(RELEASES)}")
    for nm, (lo, hi) in (("s_range", s_range), ("a_range", a_range), ("m_range", m_range),
                         ("d_range", d_range), ("a_in_range", a_in_range)):
        if not 0 < lo < hi:
            raise ValueError(f"{nm} must satisfy 0 < lo < hi")
    if s_range[0] < 50 * AU or s_range[1] > 1e5 * AU * 1.0001 or d_range[1] > 1000 * PC:
        raise ValueError("validity: 50 au <= s <= 1e5 au and d <= 1 kpc")
    if gamma_at not in ("a", "rmean"):
        raise ValueError("gamma_at must be 'a' or 'rmean'")
    if err_inflate <= 0 or mass_bias <= 0 or sigma_lnM < 0 or alpha_L <= 0 or n_epoch < 3:
        raise ValueError("need err_inflate > 0, mass_bias > 0, sigma_lnM >= 0, alpha_L > 0, n_epoch >= 3")
    rel = RELEASES[release]
    s_mu = rel["sigma_mu"] if sigma_mu is None else float(sigma_mu)
    s_px = rel["sigma_plx"] if sigma_plx is None else float(sigma_plx)
    T = rel["baseline"] if baseline is None else float(baseline)
    gfun = _gamma_fn(gravity, a0)
    rng = np.random.default_rng(seed)

    n_ch = int(round(f_chance * n))
    n_un = int(round(f_unbound * n))
    n_bd = n - n_ch - n_un
    n_wide = n_bd + n_un          # unbound pairs borrow the binaries' s distribution

    cols = {}
    have = 0
    while have < n_wide:
        m = max(4 * (n_wide - have), 1000)
        d = _powerlaw(rng, m, d_range[0], d_range[1], 2.0)
        mA = _powerlaw(rng, m, m_range[0], m_range[1], m_slope)
        mB = np.maximum(mA * rng.uniform(q_min, 1.0, m), 0.08 * MSUN)
        a = _powerlaw(rng, m, a_range[0], a_range[1], a_slope)
        e = sample_ecc(ecc, m, rng, a=a, alpha=ecc_alpha)
        flags = np.zeros(m, dtype=np.int64)
        # hidden inner binaries
        trip = rng.random(m) < f_triple
        inB = rng.random(m) < 0.5
        q_in = np.where(trip, rng.uniform(q_in_min, 1.0, m), 0.0)
        mAt = np.where(trip & ~inB, mA * (1 + q_in), mA)
        mBt = np.where(trip & inB, mB * (1 + q_in), mB)
        flags[trip & ~inB] |= FLAG_TRIPLE_A
        flags[trip & inB] |= FLAG_TRIPLE_B
        Mt = mAt + mBt
        a_eval = a if gamma_at == "a" else a * (1 + e * e / 2)
        gam = np.asarray(gfun(G * Mt / a_eval ** 2), float)
        if np.any(gam <= 0):
            raise ValueError("gravity function returned gamma <= 0")
        x, y, vx, vy, r = kepler_state(a, e, rng.random(m) * 2 * np.pi, gam * G * Mt)
        R = random_rotations(m, rng)
        px = R[:, 0, 0] * x + R[:, 0, 1] * y
        py = R[:, 1, 0] * x + R[:, 1, 1] * y
        pvx = R[:, 0, 0] * vx + R[:, 0, 1] * vy
        pvy = R[:, 1, 0] * vx + R[:, 1, 1] * vy
        v_orb = np.hypot(pvx, pvy)
        wob = np.zeros(m)
        # photocentre of the inner pair (sign: B's photocentre moves +, A's moves -)
        idx = np.nonzero(trip)[0]
        if idx.size:
            m1 = np.where(inB[idx], mB[idx], mA[idx])
            amax = np.minimum(a_in_range[1], f_stab * a[idx] * (1 - e[idx]))
            amax = np.maximum(amax, a_in_range[0] * 1.0001)
            a_in = np.exp(rng.uniform(np.log(a_in_range[0]), np.log(amax)))
            e_in = sample_ecc("thermal", idx.size, rng)
            l = q_in[idx] ** alpha_L
            vph, xph, wb = _inner_photocentre(m1, q_in[idx], a_in, e_in, l, T, n_epoch, d[idx], rng)
            sgn = np.where(inB[idx], 1.0, -1.0)[:, None]
            pvx[idx] += sgn[:, 0] * vph[:, 0]; pvy[idx] += sgn[:, 0] * vph[:, 1]
            px[idx] += sgn[:, 0] * xph[:, 0]; py[idx] += sgn[:, 0] * xph[:, 1]
            wob[idx] = wb
        s_true = np.hypot(px, py)
        # mass estimates from light
        LA = (mA / MSUN) ** alpha_L * np.where(trip & ~inB, 1 + q_in ** alpha_L, 1.0)
        LB = (mB / MSUN) ** alpha_L * np.where(trip & inB, 1 + q_in ** alpha_L, 1.0)
        Mest = (LA ** (1 / alpha_L) * np.exp(sigma_lnM * rng.standard_normal(m))
                + LB ** (1 / alpha_L) * np.exp(sigma_lnM * rng.standard_normal(m))) * MSUN * mass_bias
        batch = dict(s_true=s_true, theta=s_true / d, v_true2=np.stack([pvx, pvy], -1), v_orb=v_orb,
                     M_true=Mt, M_est=Mest, d_true=d, a=a, e=e, r=r, gamma=gam, flags=flags, wobble=wob)
        # parallax noise -> observed distance and s; select on the OBSERVED s, as a survey does
        batch = _observe(batch, rng, s_mu, s_px, err_inflate, noise)
        sel = (batch["s"] >= s_range[0]) & (batch["s"] <= s_range[1])
        for k, v in batch.items():
            cols.setdefault(k, []).append(v[sel])
        have += int(sel.sum())
    cat = {k: np.concatenate(v)[:n_wide] for k, v in cols.items()}
    # unbound comoving pairs: replace velocities of the last n_un rows
    if n_un:
        iu = np.arange(n_bd, n_wide)
        cat["v_true2"][iu] = sigma_unbound * rng.standard_normal((n_un, 2))
        cat["flags"][iu] = FLAG_UNBOUND
        for key in ("v_orb", "a", "e", "r", "gamma"):
            cat[key][iu] = np.nan
        cat["wobble"][iu] = 0.0
        # unbound pairs keep the drawn masses (and M_est); any inner-binary flag is overwritten
    # chance alignments
    if n_ch:
        parts, got = [], 0
        while got < n_ch:
            k = max(2 * (n_ch - got), 100)
            ch = {}
            ch["s_true"] = np.sqrt(rng.uniform(s_range[0] ** 2, s_range[1] ** 2, k))   # p(s) ~ s
            ch["d_true"] = _powerlaw(rng, k, d_range[0], d_range[1], 2.0)
            ch["theta"] = ch["s_true"] / ch["d_true"]
            mA = _powerlaw(rng, k, m_range[0], m_range[1], m_slope)
            mB = np.maximum(mA * rng.uniform(q_min, 1.0, k), 0.08 * MSUN)
            ch["M_true"] = mA + mB
            ch["M_est"] = (mA * np.exp(sigma_lnM * rng.standard_normal(k))
                           + mB * np.exp(sigma_lnM * rng.standard_normal(k))) * mass_bias
            ch["v_true2"] = sigma_chance * rng.standard_normal((k, 2))
            for key in ("v_orb", "a", "e", "r", "gamma"):
                ch[key] = np.full(k, np.nan)
            ch["flags"] = np.full(k, FLAG_CHANCE, dtype=np.int64)
            ch["wobble"] = np.zeros(k)
            ch = _observe(ch, rng, s_mu, s_px, err_inflate, noise)
            sel = (ch["s"] >= s_range[0]) & (ch["s"] <= s_range[1])
            parts.append({key: v[sel] for key, v in ch.items()})
            got += int(sel.sum())
        ch = {key: np.concatenate([p[key] for p in parts])[:n_ch] for key in parts[0]}
        cat = {key: np.concatenate([cat[key], ch[key]]) for key in cat}
    cat = _observe_velocity(cat, rng, s_mu, s_px, err_inflate, noise)
    cat["gN"] = G * cat["M_est"] / (r_over_s * cat["s"]) ** 2
    cat["gN_true"] = G * cat["M_true"] / cat["r"] ** 2
    cat["vtilde"] = cat["v_p"] / np.sqrt(G * cat["M_est"] / cat["s"])
    cat["vtilde_true"] = cat["v_orb"] / np.sqrt(G * cat["M_true"] / cat["s_true"])
    cat["wobble_mas"] = cat.pop("wobble")
    cat["meta"] = dict(release=release, sigma_mu_masyr=s_mu, sigma_plx_mas=s_px, baseline_s=T,
                       err_inflate=err_inflate, ecc=ecc, f_triple=f_triple, f_chance=f_chance,
                       f_unbound=f_unbound, gravity=str(gravity), r_over_s=r_over_s, seed=seed)
    return cat


def _observe(cat, rng, s_mu, s_px, err_inflate, noise):
    """Parallax noise -> observed distance and s (theta itself is taken as exact)."""
    d = cat["d_true"]
    plx_true = PC / d * 1000.0                      # mas
    k = d.size
    if noise:
        e1 = rng.standard_normal(k); e2 = rng.standard_normal(k)
        plx = plx_true + err_inflate * s_px * 0.5 * (e1 + e2)
    else:
        plx = plx_true
    if np.any(plx <= 0):
        raise ValueError("non-positive observed parallax; reduce d_max or sigma_plx")
    cat["plx_obs_mas"] = plx
    cat["distance"] = PC * 1000.0 / plx
    cat["s"] = cat["theta"] * cat["distance"]
    return cat


def _observe_velocity(cat, rng, s_mu, s_px, err_inflate, noise):
    """Proper-motion noise on the relative motion; v_p = |mu_rel| d_obs."""
    v2 = cat["v_true2"]
    mu = v2 / cat["d_true"][:, None] / MASYR          # mas/yr, relative
    if noise:
        mu = mu + err_inflate * s_mu * np.sqrt(2.0) * rng.standard_normal(mu.shape)
    cat["v_p"] = np.hypot(mu[:, 0], mu[:, 1]) * MASYR * cat["distance"]
    cat["v_p_true"] = np.hypot(v2[:, 0], v2[:, 1])
    d = cat["distance"]
    frac_plx = s_px / np.sqrt(2.0) / cat["plx_obs_mas"]
    cat["sigma_vp"] = np.hypot(np.sqrt(2.0) * s_mu * MASYR * d, cat["v_p"] * frac_plx)
    cat.pop("v_true2")
    return cat


# ---------------------------------------------------------------- selftest
def selftest(verbose=True):
    ok = True
    rng = np.random.default_rng(12345)

    def check(name, got, ref, tol, note=""):
        nonlocal ok
        good = bool(np.all(np.abs(np.asarray(got) - np.asarray(ref)) <= tol))
        ok &= good
        if verbose:
            print(f"{'PASS' if good else 'FAIL'}  {name}: got {np.round(got, 6)} ref {ref} tol {tol} {note}")

    # 0. constants against unit_tools (exact SI/IAU definitions)
    if Q is not None:
        check("pc [m] vs unit_tools", PC, Q("1 pc").to("m"), 1e3)
        check("Msun [kg] vs unit_tools", MSUN, Q("1 Msun").to("kg"), 1e26)
    # Exact definition: 1 au/yr in km/s with the Julian year; v[km/s] = 4.740470 mu[mas/yr] d[kpc]
    check("4.740470 km/s per (mas/yr x kpc)", MASYR * KPC / 1e3, 4.740470, 1e-6)

    # 1. gamma = 1 reproduces Newtonian Kepler speeds.
    # NASA Earth fact sheet (https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html):
    # "Semimajor axis (10 6 km) 149.598 ... Mean orbital velocity (km/s) 29.78 Max. orbital
    #  velocity (km/s) 30.29 Min. orbital velocity (km/s) 29.29 ... Orbit eccentricity 0.0167"
    a_E, e_E, mu_S = 149.598e9, 0.0167, G * MSUN
    _, _, vx, vy, _ = kepler_state(np.array([a_E, a_E]), np.array([e_E, e_E]), np.array([0.0, np.pi]), mu_S)
    check("Earth perihelion speed [km/s] (NASA 30.29)", np.hypot(vx[0], vy[0]) / 1e3, 30.29, 0.011,
          "(fact-sheet rounding)")
    check("Earth aphelion speed [km/s] (NASA 29.29)", np.hypot(vx[1], vy[1]) / 1e3, 29.29, 0.011)
    check("sqrt(GM/a) [km/s] (NASA mean 29.78)", math.sqrt(mu_S / a_E) / 1e3, 29.78, 0.011)
    # vis-viva |v|^2 = gamma G M (2/r - 1/a), exact Kepler law, over random orbits, gamma = 1 and 1.4
    m = 20000
    a = 10 ** rng.uniform(2, 4.5, m) * AU; e = rng.random(m) * 0.99; Mtot = 1.5 * MSUN
    for gam in (1.0, 1.4):
        x, y, vx, vy, r = kepler_state(a, e, rng.random(m) * 2 * np.pi, gam * G * Mtot)
        rel = np.max(np.abs((vx ** 2 + vy ** 2) / (gam * G * Mtot * (2 / r - 1 / a)) - 1))
        check(f"vis-viva max rel. error, gamma={gam}", rel, 0.0, 1e-9)
        check(f"r = |(x, y)|, gamma={gam}", np.max(np.abs(np.hypot(x, y) / r - 1)), 0.0, 1e-9)

    # 2. Time-averaged <r> = a(1 + e^2/2) and <1/r> = 1/a. Wikipedia, Semi-major and semi-minor axes:
    # "averaging over the mean anomaly ... gives the time-average a ( 1 + e 2 2 ) ... The
    #  time-averaged value of the reciprocal of the radius, r - 1, is a - 1."
    Mg = (np.arange(200000) + 0.5) / 200000 * 2 * np.pi     # uniform grid in mean anomaly = time
    for ee in (0.0, 0.5, 0.9, 0.99):
        E = solve_kepler(Mg, ee); rr = 1 - ee * np.cos(E)
        check(f"<r>/a at e={ee} (a(1+e^2/2))", rr.mean(), 1 + ee * ee / 2, 1e-6)
        check(f"<a/r> at e={ee}", (1 / rr).mean(), 1.0, 1e-4, "(grid integration of a peaked 1/r)")
    # random mean anomaly as used by the generator, Monte Carlo tolerance 5 sigma
    ee = 0.7; E = solve_kepler(rng.random(200000) * 2 * np.pi, ee); rr = 1 - ee * np.cos(E)
    check("<r>/a random phase, e=0.7", rr.mean(), 1 + ee ** 2 / 2, 5 * rr.std() / math.sqrt(rr.size))

    # 3. Isotropic projection: <sin theta> = pi/4 (exact: int sin^2 / 2 over [0, pi]); <cos^2> = 1/3
    R = random_rotations(200000, rng)
    z = R[:, 2, 0]
    sth = np.sqrt(1 - z ** 2)
    check("<sin theta> isotropic (pi/4)", sth.mean(), math.pi / 4, 5 * sth.std() / math.sqrt(sth.size))
    check("<cos^2 theta> isotropic (1/3)", (z ** 2).mean(), 1 / 3, 5 * (z ** 2).std() / math.sqrt(z.size))
    check("rotation matrices orthonormal", np.max(np.abs(np.einsum("nij,nkj->nik", R[:1000], R[:1000]) - np.eye(3))), 0.0, 1e-12)

    # 4. Eccentricity sampler: f ~ e^alpha has <e> = (alpha+1)/(alpha+2) (thermal 2/3, uniform 1/2)
    for kind, alp, ref in (("thermal", None, 2 / 3), ("uniform", None, 0.5), ("power", 1.3, 2.3 / 3.3)):
        ev = sample_ecc(kind, 200000, rng, alpha=alp)
        check(f"<e> {kind} {alp or ''}", ev.mean(), ref, 5 * ev.std() / math.sqrt(ev.size))
    # HTZ 2022 Table 1 (dossier RT-16): alpha = 1.30 in [3.00, 3.50] log au, 1.20 in [2.75, 3.00]
    check("HTZ alpha at 10^3.25 au", htz_alpha(10 ** 3.25 * AU), 1.30, 1e-12)
    check("HTZ alpha at 10^2.875 au", htz_alpha(10 ** 2.875 * AU), 1.20, 1e-12)

    # 5. Energy bound: for bound pairs s <= r and v^2 <= 2 gamma G M / r, so v~ <= sqrt(2 gamma).
    # (Brief, definition of v~: "For any bound pair with s <= r, v~ <= sqrt(2 gamma)".)
    for gam, kind in ((1.0, "thermal"), (1.4, "power")):
        cat = generate(30000, gravity=gam, ecc=kind, ecc_alpha=4.0, noise=False, seed=7)
        vt = cat["vtilde_true"]
        check(f"max v~/sqrt(2 gamma), gamma={gam}, {kind}", float(np.max(vt) / math.sqrt(2 * gam) <= 1 + 1e-12),
              1.0, 0.0, f"(max v~ = {np.max(vt):.4f})")
        if gam == 1.0:
            # without noise or triples, v_p = v_orb and s = s_true: observed v~ equals the truth
            check("noise-free v~ equals true v~", np.max(np.abs(cat["vtilde"] - vt * np.sqrt(cat["M_true"] / cat["M_est"]))), 0.0, 1e-9)
    # per-pair gamma(g_N) (MOND preset, HTZ eccentricities): v~ <= sqrt(2 gamma_i) pair by pair
    cat = generate(30000, gravity="bz18_simple", ecc="htz", noise=False, seed=8)
    rat = cat["vtilde_true"] / np.sqrt(2 * cat["gamma"])
    check("max v~/sqrt(2 gamma_i), bz18_simple", float(np.max(rat) <= 1 + 1e-12), 1.0, 0.0, f"(max ratio {np.max(rat):.4f})")
    # gamma scaling: identical seeds, gamma 1 vs 1.4 -> v_orb ratio sqrt(1.4) exactly
    c1 = generate(5000, gravity=1.0, ecc="thermal", noise=False, seed=3)
    c2 = generate(5000, gravity=1.4, ecc="thermal", noise=False, seed=3)
    check("v_orb(gamma=1.4)/v_orb(1) = sqrt(1.4)", np.max(np.abs(c2["v_orb"] / c1["v_orb"] - math.sqrt(1.4))), 0.0, 1e-9)

    # 6. MOND gamma(g_N).
    # Banik & Zhao 2018 eq. 5: "nu (y) = 1/2 + sqrt(1/4 + 1/y)" (simple function)
    yy = np.array([0.01, 0.3, 1.0, 7.0])
    check("nu_1 = 1/2 + sqrt(1/4 + 1/y)", np.max(np.abs(nu_n(yy, 1) - (0.5 + np.sqrt(0.25 + 1 / yy)))), 0.0, 1e-14)
    # n=2 is the QUMOND partner of the standard mu(x) = x/sqrt(1+x^2): x mu(x) = y with x = y nu(y) (BZ18 eq. 31)
    xx = yy * nu_n(yy, 2)
    check("standard: x mu(x) = y for x = y nu_2(y)", np.max(np.abs(xx * xx / np.sqrt(1 + xx * xx) - yy)), 0.0, 1e-12)
    # BZ18 eq. 10: "K0 = dLn nu_ext / dLn g_N,ext = -1/2 if gN,ext << a0"; and K -> 0 Newtonian
    check("K(y=1e-8) -> -1/2 (BZ18 eq. 10)", float(k_log_slope(1e-8, 1)), -0.5, 1e-4)
    h = 1e-5; y0 = 0.7
    kfd = (math.log(nu_n(y0 * (1 + h), 1)) - math.log(nu_n(y0 * (1 - h), 1))) / (math.log(1 + h) - math.log(1 - h))
    check("K analytic vs finite difference (internal)", float(k_log_slope(y0, 1)), kfd, 1e-8)
    # Newtonian limit: gamma -> 1 for g_N >> a0 (any preset)
    for mdl in ("bz18_simple", "bz18_standard", "chae2024", "isolated"):
        check(f"Newtonian limit gamma(1e-6 m/s^2) {mdl}", gamma_mond(1e-6, mdl), 1.0, 2e-4)
    # Deep-MOND isolated limit (Milgrom): g = sqrt(a0 g_N) -> gamma sqrt(g_N/a0) -> 1
    check("isolated deep MOND gamma*sqrt(y), y=1e-8", gamma_mond(1e-8 * A0_DEFAULT, "isolated") * 1e-4, 1.0, 1e-3)
    # BZ18 Table 3 (EF-dominated, Solar neighbourhood; g_ext from sec. 3.6 "vc = 232.8 km/s ... R = 8.2 kpc"):
    # "Standard 1.1462 1.0726 1.0661 Simple 1.5602 1.4228 1.4056" (nu_ext, eta QUMOND, eta AQUAL)
    for mdl, nu_ref, eta_ref in (("bz18_simple", 1.5602, 1.4228), ("bz18_standard", 1.1462, 1.0726)):
        lim = efe_limit(mdl)
        check(f"BZ18 Table 3 nu_ext {mdl}", lim["nu_ext"], nu_ref, 3e-4, "(table rounding + a0, kpc conventions)")
        check(f"BZ18 Table 3 eta (QUMOND) {mdl}", lim["eta"], eta_ref, 3e-4)
        check(f"gamma_mond deep limit (g_N=1e-15) -> eta {mdl}", gamma_mond(1e-15, mdl), eta_ref, 3e-4)
    # Chae 2024 (ApJ 972, 186): "This model becomes Newtonian as s/rM -> 0 and pseudo-Newtonian with
    # Geff = 1.37 for s/rM >~ 1" (dossier RT-09). s/rM = 1 means g_N ~ a0 / 1.44.
    check("Chae 2024 G_eff ~ 1.37 at s/rM = 1", gamma_mond(A0_DEFAULT / 1.44, "chae2024"), 1.37, 0.03,
          "(quote gives 2 digits; s/rM = 1 is the start of the plateau)")
    check("Chae 2024 deep plateau g_N = 1e-12", gamma_mond(1e-12, "chae2024"), 1.37, 0.01)

    # 7. Hidden companion photocentre (Belokurov et al. 2020 eq. 4): Delta = |q - l| <|x1 - x2|> / ((q+1)(l+1));
    # "an unresolved binary of two identical stars (q = l) will not show any e[ffect]"
    qq = rng.random(1000); ll = rng.random(1000)
    check("photocentre factor = (l - q)/((1+q)(1+l))", np.max(np.abs(photocentre_factor(qq, ll) - (ll - qq) / ((1 + qq) * (1 + ll)))), 0.0, 1e-14)
    check("q = l gives no wobble", float(photocentre_factor(0.6, 0.6)), 0.0, 1e-15)
    # Gaia-baseline averaging. Short baseline -> instantaneous velocity of a circular orbit (2 pi a/P);
    # P << T -> fitted proper motion averages out (Belokurov: "If the binary period is smaller than the
    # Gaia's temporal baseline then the additional centroid perturbation is non-linear and cannot be
    # absorbed into the proper motion").
    a_in = AU; m1 = MSUN
    Pin = 2 * math.pi * math.sqrt(a_in ** 3 / (G * m1 * 2))
    t = np.linspace(0, 1e-4 * Pin, 24)
    x, y, vx, vy, _ = kepler_state(np.full((1, 24), a_in), np.zeros((1, 24)), 2 * np.pi * t[None] / Pin + 0.3, G * m1 * 2)
    check("short baseline: LSQ slope = instantaneous speed", float(np.hypot(lsq_slope(t, x), lsq_slope(t, y))[0] / (2 * math.pi * a_in / Pin)), 1.0, 1e-6)
    t = np.linspace(0, 40 * Pin, 4000)
    x, y, _, _, _ = kepler_state(np.full((1, 4000), a_in), np.zeros((1, 4000)), 2 * np.pi * t[None] / Pin + 0.3, G * m1 * 2)
    check("P = T/40: |LSQ slope| / v_orb < 0.02", float(float(np.hypot(lsq_slope(t, x), lsq_slope(t, y))[0] / (2 * math.pi * a_in / Pin)) < 0.02), 1.0, 0.0)
    # Closed form (derived here, not an external reference): for x = A cos(w t + phi) on a uniform window
    # of length T, the LSQ slope is K(u) * xdot(t_mid) with K(u) = 3 (sin u - u cos u) / u^3, u = w T / 2.
    for frac in (0.3, 0.7, 2.5):
        T = frac * Pin
        t = np.linspace(0, T, 20001)
        ph = 2 * np.pi * t / Pin + 0.3
        x, y, _, _, _ = kepler_state(np.full((1, t.size), a_in), np.zeros((1, t.size)), ph[None], G * m1 * 2)
        u = math.pi * T / Pin
        Ku = 3 * (math.sin(u) - u * math.cos(u)) / u ** 3
        w = 2 * math.pi / Pin; phm = 0.3 + w * T / 2
        check(f"LSQ slope / mid-window velocity, T = {frac} P (K(u) = {Ku:.4f})",
              float(lsq_slope(t, x)[0] / (-a_in * w * math.sin(phm))), Ku, 1e-4, "(discrete 20001-epoch sampling)")

    # 8. Noise model: zero intrinsic motion -> v_p Rayleigh with sigma = sqrt(2) sigma_mu d, mean sigma sqrt(pi/2)
    ch = dict(d_true=np.full(200000, 100 * PC), theta=np.full(200000, 1e-5), v_true2=np.zeros((200000, 2)))
    ch = _observe(ch, rng, 0.05, 0.0, 1.0, True)
    ch = _observe_velocity(ch, rng, 0.05, 0.0, 1.0, True)
    sig = math.sqrt(2) * 0.05 * MASYR * 100 * PC
    check("Rayleigh mean of pure-noise v_p / (sigma sqrt(pi/2))", ch["v_p"].mean() / (sig * math.sqrt(math.pi / 2)), 1.0, 5 * 0.52 / math.sqrt(2e5))

    # 9. Full catalogue smoke test: flags and fractions; input refusal
    cat = generate(20000, gravity="bz18_simple", ecc="htz", f_triple=0.2, f_chance=0.02, f_unbound=0.03, seed=11)
    nflag = lambda f: np.mean((cat["flags"] & f) > 0)
    check("triple fraction among catalogue ~ 0.2 x 0.95", nflag(3), 0.19, 0.02)
    check("chance fraction", nflag(FLAG_CHANCE), 0.02, 1e-3)
    check("s within window", float(np.all((cat["s"] >= 200 * AU) & (cat["s"] <= 30000 * AU))), 1.0, 0.0)
    try:
        generate(10, ecc="power", ecc_alpha=-2)
        refused = False
    except ValueError:
        refused = True
    check("refuses alpha <= -1", float(refused), 1.0, 0.0)
    if verbose:
        print("selftest", "PASSED" if ok else "FAILED")
    return ok


# ---------------------------------------------------------------- CLI
def _si(text, unit):
    if Q is None:
        return float(text)
    try:
        return float(text)
    except ValueError:
        return Q(text).to(unit)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    g = sub.add_parser("gamma", help="MOND boost at g_N")
    g.add_argument("--gN", required=True, help='e.g. "1e-10 m/s^2"')
    g.add_argument("--model", default="bz18_simple", choices=sorted(MOND_PRESETS))
    g.add_argument("--a0", default=str(A0_DEFAULT))
    g.add_argument("--gext", default=None)
    c = sub.add_parser("generate", help="synthetic catalogue summary")
    c.add_argument("--n", type=int, default=100000)
    c.add_argument("--gravity", default="1.0", help="float gamma or MOND preset name")
    c.add_argument("--ecc", default="htz")
    c.add_argument("--ecc-alpha", type=float, default=None)
    c.add_argument("--f-triple", type=float, default=0.0)
    c.add_argument("--f-chance", type=float, default=0.0)
    c.add_argument("--f-unbound", type=float, default=0.0)
    c.add_argument("--release", default="DR3")
    c.add_argument("--err-inflate", type=float, default=1.0)
    c.add_argument("--mass-bias", type=float, default=1.0)
    c.add_argument("--seed", type=int, default=None)
    c.add_argument("--out", default=None, help="save arrays to .npz")
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    if a.cmd == "gamma":
        gN = _si(a.gN, "m/s^2"); a0 = _si(a.a0, "m/s^2")
        gext = None if a.gext is None else _si(a.gext, "m/s^2")
        print(f"gamma({gN:.3e} m/s^2; {a.model}, a0={a0:.3e} m/s^2) = {gamma_mond(gN, a.model, a0=a0, g_ext=gext):.4f}")
        if a.model != "isolated":
            lim = efe_limit(a.model, a0=a0, g_ext=gext)
            print("EF-dominated limit (BZ18 eqs. 15-16): " + ", ".join(f"{k}={v:.4f}" for k, v in lim.items()))
        return 0
    try:
        grav = float(a.gravity)
    except ValueError:
        grav = a.gravity
    cat = generate(a.n, gravity=grav, ecc=a.ecc, ecc_alpha=a.ecc_alpha, f_triple=a.f_triple,
                   f_chance=a.f_chance, f_unbound=a.f_unbound, release=a.release,
                   err_inflate=a.err_inflate, mass_bias=a.mass_bias, seed=a.seed)
    print(f"N = {cat['s'].size}; meta = {cat['meta']}")
    for f, nm in ((3, "triple"), (FLAG_CHANCE, "chance"), (FLAG_UNBOUND, "unbound")):
        print(f"  fraction {nm}: {np.mean((cat['flags'] & f) > 0):.3f}")
    print(f"  s [au]: median {np.median(cat['s']) / AU:.0f}, range {cat['s'].min() / AU:.0f}-{cat['s'].max() / AU:.0f}")
    print(f"  v_p [km/s]: median {np.median(cat['v_p']) / 1e3:.3f}; sigma_vp median {np.median(cat['sigma_vp']) / 1e3:.4f}")
    print(f"  M_est/M_true median {np.median(cat['M_est'] / cat['M_true']):.3f}")
    edges = np.array([-12.0, -10.5, -10.0, -9.5, -9.0, -8.5, -7.0])
    lg = np.log10(cat["gN"])
    print("  log10 gN_proxy bin   N     median v~   median gamma_true")
    for lo, hi in zip(edges[:-1], edges[1:]):
        s = (lg >= lo) & (lg < hi)
        if s.sum():
            print(f"  [{lo:6.1f},{hi:6.1f})  {s.sum():6d}   {np.median(cat['vtilde'][s]):.4f}      {np.nanmedian(cat['gamma'][s]):.4f}")
    if a.out:
        np.savez_compressed(a.out, **{k: v for k, v in cat.items() if k != "meta"}, meta=str(cat["meta"]))
        print(f"saved {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
