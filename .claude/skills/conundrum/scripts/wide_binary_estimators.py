#!/usr/bin/env python3
"""wide_binary_estimators.py -- estimator families for wide-binary gravity tests (gamma = G_eff/G).

WHAT IT COMPUTES
    From per-pair arrays (projected separation s, sky-projected relative velocity v_p, total mass
    estimate M, a Newtonian-acceleration proxy g_N, and errors) it returns gamma = G_eff/G per
    log10(g_N) bin with bootstrap errors, for four estimator families (brief, "Estimator families"):

      1. full-median     : median (or several quantiles) of v~ matched to a Newtonian calibration,
                           either a forward-modelled Kepler template (optionally with a triple
                           fraction f_multi) or an empirical calibration sample (Chae-style).
      2. tail-truncated  : (a) "threshold": truncated likelihood of the pure-binary model using only
                           pairs with v~ < v_cut, renormalised on [0, v_cut);
                           (b) "trimmed": upper-trimmed mean of v~ (top fraction p removed) matched to
                           the template's trimmed mean.
      3. mixture         : binned likelihood on [0, v_max) of
                           (1 - f_t - f_ca) B(v~|gamma) + f_t T(v~|gamma) + f_ca C(v~),
                           gamma profiled over (f_t, f_ca) by EM at each gamma.
      4. bayes           : SIMPLIFIED Bayesian deprojection: population-level posterior on gamma with
                           the orbit (eccentricity exponent alpha_e, phase, orientation, i.e. the
                           deprojection) marginalised through Kepler templates, an outlier fraction
                           f_out marginalised on a grid, flat prior in ln(gamma). Optionally uses the
                           3D velocity when radial-velocity differences v_r are supplied. It is NOT a
                           per-system orbit fit (Chae 2025, Chae et al. 2026); label it as simplified.

MODEL AND FORMULAS
    v~ = v_p / sqrt(G M / s)           (Pittordis & Sutherland 2018; Banik & Zhao 2018 eq. 3; Chae 2024 eq. 1)
    g_N proxy (if not given) = G M / (k s)^2, k = r/s factor (default 1; Chae-type uses k ~ 1.2).
    Gravity law: Keplerian orbits with G -> gamma G (an APPROXIMATION to MOND with the external field;
    brief "Definitions"). Then every bound-orbit velocity scales as sqrt(gamma) at fixed geometry, so
        v~_true(gamma) = sqrt(gamma) * v~_N,
    with v~_N drawn from a Newtonian template.
    Newtonian template (this file's own Kepler Monte Carlo; does NOT import the run's generator):
        f(e) ∝ e^alpha_e on [0, e_max]; mean anomaly uniform; Kepler's equation by Newton iteration;
        isotropic orientation (cos i, Omega, omega uniform); line of sight = z.
        Population dN/da ∝ a^-lam selected in a narrow s bin -> weight w = (s/a)^(lam-1)
        (scale-free: for lam = 1, Opik, selection in s does not change the v~ distribution).
    Observation model (forward model, common random numbers):
        v_obs_vec = sqrt(gamma) v~_N m_f x_hat + sig~ (n1, n2)  [+ kappa * khat_xy for triples]
        v~_obs = |v_obs_vec|,  sig~ = sigma_vp / v_c(s) (1-sigma per sky component),
        m_f = exp(-delta/2), delta ~ N(0, sigma_lnM) (mass-estimate scatter; v~ ∝ M_est^-1/2).
    Triple component (mixture and optional in full-median): an isotropic 3D velocity kick of size
        kappa (in units of v_c(s)) log-uniform on [kappa_lo, kappa_hi] = [0.1, 5] by default. The
        inner orbit is Newtonian (high acceleration), so kappa does NOT scale with gamma. This is a
        crude NUISANCE SHAPE, not a physical triple model (no photocentre or Gaia-baseline averaging).
    Chance-alignment component: C(v~) = 2 v~ / v_max^2 on [0, v_max) (2D velocity difference with a
        broad dispersion has density ∝ v~ near the origin).
    Closed form used in the self-test (circular orbits, isotropic projection, random phase):
        v~^2 / gamma = sin^2(psi) sin(theta)  [v~ = v_p sqrt(s)/sqrt(GM), v = sqrt(GM/r), s = r sin(theta)], cos(theta) = u ~ U(0,1),
        sin^2(psi) = 1 - sin^2(theta) cos^2(phi), phi ~ U(0, 2 pi), so
        F(t) = P(v~ <= t) = int_0^1 du G(t^2/gamma, S(u)), S = sqrt(1 - u^2),
        G(x, S) = 0 if q > 1; 1 if q <= 0; (2/pi) arccos(sqrt(q)) else, q = (1 - x / S) / S^2.
        E[v~^2]/gamma = E[S] - E[S^3]/2 = pi/4 - 3 pi/32 = 0.49087, E[S^a] = (sqrt(pi)/2) Gamma(a/2+1)/Gamma(a/2+3/2).
    Statistical error scaling: sigma_stat(N_target) = sigma(N) sqrt(N / N_target) (CLT, all families
        are root-N consistent). Analytic full-median error (Laplace; asymptotic sample median):
        sigma_median = 1 / (2 f(m) sqrt(N))  ->  sigma_gamma = gamma / (m f(m) sqrt(N)).

ASSUMPTIONS AND VALIDITY
    * Scalar gamma per bin: the anisotropic MOND external-field boost is averaged (approximation).
    * Template eccentricity law and separation slope are user choices (alpha_e default 1 = thermal,
      lam default 1 = Opik); mis-specifying them biases gamma (brief premise 5). This is intended.
    * gamma grid limited to [0.3, 4]; inputs giving gamma outside raise ValueError.
    * Template Monte Carlo noise: n_model draws (default 2e5) add relative error ~ sqrt(N/n_model) to
      sigma; bootstrap errors do NOT include it. Use n_model >> N for DR4-sized bins.
    * Bins with fewer than 50 pairs are skipped.

UNITS
    Python API is SI: s [m], v_p, sigma_vp, v_r, sigma_vr [m/s], M [kg], g_N [m s^-2];
    sigma_lnM is dimensionless (natural-log scatter of M_est). gamma is dimensionless.
    CLI accepts units via unit_tools.Q (e.g. "5000 au", "1.5 Msun", "20 m/s").

PYTHON USAGE
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import wide_binary_estimators as wbe
    res = wbe.gamma_per_bin(s, v_p, M, gN=None, sigma_vp=sig, sigma_lnM=0.1,
                            bins=[-11, -10, -9.5, -9, -8], estimator="mixture",
                            template=wbe.KeplerTemplate(alpha_e=1.3), n_boot=100, target_N=300000)
    for row in res: print(row["bin"], row["gamma"], row["sigma_boot"], row["sigma_at_target"])

COMMAND LINE
    python3 .claude/skills/conundrum/scripts/wide_binary_estimators.py selftest
    python3 .claude/skills/conundrum/scripts/wide_binary_estimators.py demo \
        --gamma 1.4 --n 20000 --sep "5000 au" --mass "1.5 Msun" --sigma-v "20 m/s" --target-n 300000
    python3 .../wide_binary_estimators.py scale --sigma 0.03 --n 26000 --target-n 300000
    python3 .../wide_binary_estimators.py fit --npz pairs.npz --estimator all --bins -11 -10 -9.5 -9 -8
        (npz arrays: s [m], v_p [m/s], M [kg]; optional gN, sigma_vp, sigma_lnM, v_r, sigma_vr)
"""
import argparse
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
try:
    import unit_tools as _ut  # SI constants (CODATA G) and CLI unit parsing
    G = _ut.G
except Exception:  # pragma: no cover - fall back to CODATA 2018 value
    _ut = None
    G = 6.67430e-11

GAMMA_MIN, GAMMA_MAX = 0.3, 4.0
_DW = 0.04  # histogram bin width in v~ units


# ----------------------------------------------------------------------------------------------
# basic quantities
# ----------------------------------------------------------------------------------------------
def _arr(x, name, positive=True, allow_zero=False):
    a = np.atleast_1d(np.asarray(x, dtype=float))
    if not np.all(np.isfinite(a)):
        raise ValueError(f"{name}: non-finite values")
    if positive and (np.any(a < 0) or (not allow_zero and np.any(a == 0))):
        raise ValueError(f"{name}: must be {'>= 0' if allow_zero else '> 0'}")
    return a


def v_circ(s, M):
    """Newtonian circular speed at the projected separation, sqrt(G M / s) [m/s]."""
    return np.sqrt(G * _arr(M, "M") / _arr(s, "s"))


def vtilde(s, v_p, M):
    """Normalised projected velocity v~ = v_p / sqrt(G M / s) (dimensionless)."""
    return _arr(v_p, "v_p", allow_zero=True) / v_circ(s, M)


def gN_proxy(s, M, r_over_s=1.0):
    """Newtonian acceleration proxy G M / (k s)^2 [m s^-2]; k = r/s (default 1)."""
    if r_over_s < 1.0:
        raise ValueError("r_over_s must be >= 1 (r >= s)")
    return G * _arr(M, "M") / (r_over_s * _arr(s, "s")) ** 2


def sigma_at_target(sigma, N, N_target):
    """Root-N scaling of a statistical error to a target sample size."""
    if sigma < 0 or N <= 0 or N_target <= 0:
        raise ValueError("sigma >= 0, N > 0, N_target > 0 required")
    return sigma * math.sqrt(N / N_target)


def sigma_median_analytic(vt_obs, gamma):
    """Asymptotic full-median error: sigma_gamma = gamma / (m f(m) sqrt(N)) (Laplace).
    f(m) is estimated by a Gaussian KDE (Silverman bandwidth) at the sample median m."""
    v = _arr(vt_obs, "vt_obs", allow_zero=True)
    n = v.size
    m = np.median(v)
    iqr = np.subtract(*np.percentile(v, [75, 25]))
    h = 0.9 * min(v.std(), iqr / 1.34) * n ** -0.2
    fm = np.mean(np.exp(-0.5 * ((v - m) / h) ** 2)) / (h * math.sqrt(2 * math.pi))
    return gamma / (m * fm * math.sqrt(n))


# ----------------------------------------------------------------------------------------------
# Newtonian templates (own Monte Carlo; independent of the run's generator)
# ----------------------------------------------------------------------------------------------
def _solve_kepler(Mmean, e):
    E = Mmean + 0.85 * e * np.sign(np.sin(Mmean))
    for _ in range(60):
        f = E - e * np.sin(E) - Mmean
        E = E - f / (1.0 - e * np.cos(E))
    return E


class KeplerTemplate:
    """Newtonian (gamma = 1) v~ template from Kepler orbits.

    alpha_e : eccentricity exponent, f(e) ∝ e^alpha_e on [0, e_max] (alpha_e > -1); None = circular.
    lam     : population slope dN/da ∝ a^-lam (0 <= lam <= 3), applied as weight (s/a)^(lam-1).
    Attributes vt (projected v~), vz (line-of-sight component in the same units), and, for checks,
    s1 = s/a, r1 = r/a, vp1, v31 (velocities in units of sqrt(G M / a)), e, cospsi (sky v-r angle).
    """

    def __init__(self, alpha_e=1.0, lam=1.0, e_max=0.99, n=200000, seed=101):
        if alpha_e is not None and alpha_e <= -1:
            raise ValueError("alpha_e must be > -1")
        if not (0 < e_max < 1):
            raise ValueError("e_max must be in (0, 1)")
        if not (0 <= lam <= 3):
            raise ValueError("lam must be in [0, 3]")
        rng = np.random.default_rng(seed)
        self.label = "circular" if alpha_e is None else f"alpha_e={alpha_e:g}, lam={lam:g}"
        if alpha_e is None:
            e = np.zeros(n)
        else:  # truncated power law by inverse CDF
            e = (rng.random(n) * e_max ** (alpha_e + 1)) ** (1.0 / (alpha_e + 1))
        Mm = rng.uniform(0, 2 * np.pi, n)
        E = _solve_kepler(Mm, e)
        sq = np.sqrt(1 - e * e)
        x, y = np.cos(E) - e, sq * np.sin(E)
        Edot = 1.0 / (1.0 - e * np.cos(E))  # a = GM = 1
        vx, vy = -np.sin(E) * Edot, sq * np.cos(E) * Edot
        ci = rng.uniform(-1, 1, n)
        si = np.sqrt(1 - ci * ci)
        Om, om = rng.uniform(0, 2 * np.pi, (2, n))

        def rot(px, py):
            c, s_ = np.cos(om), np.sin(om)
            X1, Y1 = c * px - s_ * py, s_ * px + c * py
            return (np.cos(Om) * X1 - np.sin(Om) * ci * Y1,
                    np.sin(Om) * X1 + np.cos(Om) * ci * Y1,
                    si * Y1)

        X, Y, Z = rot(x, y)
        VX, VY, VZ = rot(vx, vy)
        s1 = np.hypot(X, Y)
        vp1 = np.hypot(VX, VY)
        if lam != 1.0:
            w = s1 ** (lam - 1.0)
            idx = rng.choice(n, size=n, replace=True, p=w / w.sum())
        else:
            idx = np.arange(n)
        self.e = e[idx]
        self.s1, self.r1 = s1[idx], np.sqrt(X * X + Y * Y + Z * Z)[idx]
        self.vp1, self.v31 = vp1[idx], np.sqrt(VX * VX + VY * VY + VZ * VZ)[idx]
        self.vt = (vp1 * np.sqrt(s1))[idx]
        self.vz = (VZ * np.sqrt(s1))[idx]
        self.cospsi = ((X * VX + Y * VY) / (s1 * vp1))[idx]
        self.n = n


class ArrayTemplate:
    """Template from user arrays of Newtonian v~ (and optional LOS component), e.g. from a generator."""

    def __init__(self, vt, vz=None, label="user array"):
        self.vt = _arr(vt, "template vt", allow_zero=True)
        self.vz = np.zeros_like(self.vt) if vz is None else np.asarray(vz, float)
        self.n, self.label = self.vt.size, label


# ----------------------------------------------------------------------------------------------
# forward model
# ----------------------------------------------------------------------------------------------
class _Forward:
    def __init__(self, tmpl, sp, sm, sr=None, n_model=200000, seed=7, kick=(0.1, 5.0)):
        if not (0 < kick[0] < kick[1]):
            raise ValueError("kick range must satisfy 0 < lo < hi")
        rng = np.random.default_rng(seed)
        it = rng.integers(0, tmpl.n, n_model)
        self.vt, self.vz = tmpl.vt[it], tmpl.vz[it]
        ie = rng.integers(0, len(sp), n_model)
        self.sp = sp[ie]
        self.sr = None if sr is None else sr[ie]
        self.mf = np.exp(-0.5 * sm[ie] * rng.standard_normal(n_model))
        self.n1, self.n2, self.n3 = rng.standard_normal((3, n_model))
        self.kap = np.exp(rng.uniform(np.log(kick[0]), np.log(kick[1]), n_model))
        kz = rng.uniform(-1, 1, n_model)
        kph = rng.uniform(0, 2 * np.pi, n_model)
        ks = np.sqrt(1 - kz * kz)
        self.kx, self.ky, self.kz = ks * np.cos(kph), ks * np.sin(kph), kz
        self.n = n_model

    def draw(self, gamma, triple=False, three_d=False):
        g = math.sqrt(gamma)
        x = g * self.vt * self.mf + self.sp * self.n1
        y = self.sp * self.n2
        if triple:
            x = x + self.kap * self.kx
            y = y + self.kap * self.ky
        if not three_d:
            return np.hypot(x, y)
        z = g * self.vz * self.mf + (0 if self.sr is None else self.sr * self.n3)
        if triple:
            z = z + self.kap * self.kz
        return np.sqrt(x * x + y * y + z * z)


def _hist(v, nb):
    k = np.floor(v / _DW).astype(np.int64)
    k = k[k < nb]
    return np.bincount(k, minlength=nb).astype(float)


def _pmf_grid(fw, gammas, nb, triple=False, three_d=False):
    out = np.empty((len(gammas), nb))
    for i, g in enumerate(gammas):
        out[i] = _hist(fw.draw(g, triple, three_d), nb) / fw.n
    return np.maximum(out, 1e-12)


def _parabolic_max(x, y):
    i = int(np.argmax(y))
    if i == 0 or i == len(y) - 1:
        raise ValueError("gamma maximum at the grid edge: outside [0.3, 4] or model misfit")
    x0, x1, x2 = x[i - 1:i + 2]
    y0, y1, y2 = y[i - 1:i + 2]
    den = (x0 - x1) * (x0 - x2) * (x1 - x2)
    A = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / den
    B = (x2 * x2 * (y0 - y1) + x1 * x1 * (y2 - y0) + x0 * x0 * (y1 - y2)) / den
    return -B / (2 * A) if A < 0 else x1


def _profile_interval(lng, lnL):
    """1-sigma interval in gamma from Delta lnL = 0.5 on a ln(gamma) grid."""
    i = int(np.argmax(lnL))
    thr = lnL[i] - 0.5
    lo = hi = None
    for j in range(i, 0, -1):
        if lnL[j - 1] < thr:
            lo = np.interp(thr, [lnL[j - 1], lnL[j]], [lng[j - 1], lng[j]])
            break
    for j in range(i, len(lnL) - 1):
        if lnL[j + 1] < thr:
            hi = np.interp(thr, [lnL[j + 1], lnL[j]], [lng[j + 1], lng[j]])
            break
    return (math.exp(lo) if lo is not None else float("nan"),
            math.exp(hi) if hi is not None else float("nan"))


def _two_pass(lnL_fun):
    """Coarse ln(gamma) grid on [0.3, 4], then a fine grid over the region within 12 of the max."""
    g1 = np.geomspace(GAMMA_MIN, GAMMA_MAX, 57)
    L1 = lnL_fun(g1)
    i = int(np.argmax(L1))
    if i == 0 or i == len(g1) - 1:
        raise ValueError("gamma outside [0.3, 4] (likelihood peaks at grid edge)")
    ok = np.where(L1 > L1[i] - 12)[0]
    lo, hi = g1[max(ok[0] - 1, 0)], g1[min(ok[-1] + 1, len(g1) - 1)]
    g2 = np.geomspace(lo, hi, 61)
    return g2, lnL_fun(g2)


# ----------------------------------------------------------------------------------------------
# estimator families (operate on one bin: arrays in v~ units)
# ----------------------------------------------------------------------------------------------
def _boot_summary(vals):
    vals = np.asarray(vals)
    vals = vals[np.isfinite(vals)]
    if vals.size < 5:
        return float("nan"), (float("nan"), float("nan"))
    return float(np.std(vals, ddof=1)), tuple(float(x) for x in np.percentile(vals, [16, 84]))


def _invert_curve(gg, stat_curve, value):
    ls = np.log(np.maximum.accumulate(stat_curve))
    if not (ls[0] <= math.log(value) <= ls[-1]):
        raise ValueError("statistic outside the model range for gamma in [0.3, 4]")
    return float(np.exp(np.interp(math.log(value), ls, np.log(gg))))


def est_full_median(vt, fw=None, quantiles=(0.5,), f_multi=0.0, calib_vt=None, n_boot=200, seed=1):
    """Full-median family. gamma from matching data quantiles of v~ to the Newtonian calibration.
    calib_vt: empirical Newtonian calibration sample (already noisy, incl. its own triples):
              gamma = mean_q (Q_data/Q_calib)^2, no forward model (Chae-style)."""
    vt = np.asarray(vt, float)
    qs = np.asarray(quantiles, float)
    if np.any((qs <= 0) | (qs >= 1)):
        raise ValueError("quantiles must lie in (0, 1)")
    if not (0 <= f_multi < 1):
        raise ValueError("f_multi must lie in [0, 1)")
    rng = np.random.default_rng(seed)
    if calib_vt is not None:
        qc = np.quantile(np.asarray(calib_vt, float), qs)
        fun = lambda d: float(np.mean((np.quantile(d, qs) / qc) ** 2))
    else:
        gg = np.geomspace(GAMMA_MIN, GAMMA_MAX, 81)
        nt = int(round(f_multi * fw.n))
        curves = []
        for g in gg:
            v = fw.draw(g)
            if nt:
                v[:nt] = fw.draw(g, triple=True)[:nt]
            curves.append(np.quantile(v, qs))
        curves = np.array(curves)  # (ng, nq)

        def fun(d):
            qd = np.quantile(d, qs)
            return float(np.exp(np.mean([math.log(_invert_curve(gg, curves[:, j], qd[j]))
                                         for j in range(len(qs))])))
    gam = fun(vt)
    boots = []
    for _ in range(n_boot):
        try:
            boots.append(fun(vt[rng.integers(0, vt.size, vt.size)]))
        except ValueError:
            boots.append(np.nan)
    sb, ci = _boot_summary(boots)
    return dict(gamma=gam, sigma_boot=sb, ci68_boot=ci, N_used=int(vt.size))


def est_trimmed(vt, fw, p_trim=0.1, n_boot=200, seed=2):
    """Tail-truncated family, trimmed variant: mean of the lowest (1 - p_trim) of v~."""
    if not (0 <= p_trim < 0.5):
        raise ValueError("p_trim must lie in [0, 0.5)")
    vt = np.asarray(vt, float)
    rng = np.random.default_rng(seed)

    def tmean(v):
        v = np.sort(v)
        return float(v[: max(1, int(round((1 - p_trim) * v.size)))].mean())

    gg = np.geomspace(GAMMA_MIN, GAMMA_MAX, 81)
    curve = np.array([tmean(fw.draw(g)) for g in gg])
    fun = lambda d: _invert_curve(gg, curve, tmean(d))
    gam = fun(vt)
    boots = [fun(vt[rng.integers(0, vt.size, vt.size)]) for _ in range(n_boot)]
    sb, ci = _boot_summary(boots)
    return dict(gamma=gam, sigma_boot=sb, ci68_boot=ci, N_used=int(vt.size), p_trim=p_trim)


def est_threshold(vt, fw, v_cut=1.0, n_boot=200, seed=3):
    """Tail-truncated family, threshold variant: truncated likelihood of the pure-binary model
    on v~ < v_cut (cut rounded to the 0.04 histogram grid), renormalised on [0, v_cut)."""
    kc = int(round(v_cut / _DW))
    if kc < 5:
        raise ValueError("v_cut too small (< 0.2)")
    vt = np.asarray(vt, float)
    n = _hist(vt, kc)
    if n.sum() < 50:
        raise ValueError("fewer than 50 pairs below v_cut")
    cache = {}

    def P(gs):
        key = (gs[0], gs[-1], len(gs))
        if key not in cache:
            B = _pmf_grid(fw, gs, kc)
            cache[key] = np.log(B / B.sum(1, keepdims=True))
        return cache[key]

    lnL_fun = lambda gs, cnt=None: P(gs) @ (n if cnt is None else cnt)
    g2, L2 = _two_pass(lambda gs: lnL_fun(gs))
    lng = np.log(g2)
    gam = math.exp(_parabolic_max(lng, L2))
    prof = _profile_interval(lng, L2)
    rng = np.random.default_rng(seed)
    LP = P(g2)
    boots = []
    for _ in range(n_boot):
        cnt = rng.multinomial(int(n.sum()), n / n.sum())
        try:
            boots.append(math.exp(_parabolic_max(lng, LP @ cnt)))
        except ValueError:
            boots.append(np.nan)
    sb, ci = _boot_summary(boots)
    return dict(gamma=gam, sigma_boot=sb, ci68_boot=ci, ci68_profile=prof,
                N_used=int(n.sum()), v_cut=kc * _DW)


def _em_weights(cnt, comps, n_iter=300, w0=None, fixed=None):
    """EM for mixture weights with fixed component pmfs. comps: (ng, nc, K). Returns w (ng, nc), lnL."""
    ng, nc, K = comps.shape
    w = np.full((ng, nc), 1.0 / nc) if w0 is None else w0.copy()
    N = cnt.sum()
    for _ in range(n_iter):
        P = np.einsum("gc,gck->gk", w, comps)
        R = w[:, :, None] * comps / P[:, None, :]
        w = (R @ cnt) / N
        if fixed is not None:
            for j, val in fixed.items():
                w[:, j] = val
            free = [j for j in range(nc) if j not in fixed]
            w[:, free] *= ((1 - sum(fixed.values())) / w[:, free].sum(1))[:, None]
    P = np.einsum("gc,gck->gk", w, comps)
    return w, np.log(P) @ cnt


def est_mixture(vt, fw, v_max=5.0, f_triple_fixed=None, n_boot=100, seed=4):
    """Mixture-likelihood family: (1-f_t-f_ca) B(gamma) + f_t T(gamma) + f_ca C on [0, v_max).
    f_triple_fixed: fix f_t (e.g. calibrated at high acceleration); else profiled."""
    K = int(round(v_max / _DW))
    vt = np.asarray(vt, float)
    n = _hist(vt, K)
    if n.sum() < 50:
        raise ValueError("fewer than 50 pairs below v_max")
    edges = np.arange(K + 1) * _DW
    C = np.diff(edges ** 2) / edges[-1] ** 2
    fixed = None if f_triple_fixed is None else {1: float(f_triple_fixed)}
    cache = {}

    def comps(gs):
        key = (gs[0], gs[-1], len(gs))
        if key not in cache:
            B = _pmf_grid(fw, gs, K)
            T = _pmf_grid(fw, gs, K, triple=True)
            B /= B.sum(1, keepdims=True)
            T /= T.sum(1, keepdims=True)
            cache[key] = np.stack([B, T, np.broadcast_to(C, B.shape)], axis=1)
        return cache[key]

    def lnL_fun(gs):
        return _em_weights(n, comps(gs), fixed=fixed)[1]

    g2, L2 = _two_pass(lnL_fun)
    lng = np.log(g2)
    gam = math.exp(_parabolic_max(lng, L2))
    W, _ = _em_weights(n, comps(g2), fixed=fixed)
    iw = int(np.argmax(L2))
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        cnt = rng.multinomial(int(n.sum()), n / n.sum()).astype(float)
        _, Lb = _em_weights(cnt, comps(g2), n_iter=120, w0=W, fixed=fixed)
        try:
            boots.append(math.exp(_parabolic_max(lng, Lb)))
        except ValueError:
            boots.append(np.nan)
    sb, ci = _boot_summary(boots)
    return dict(gamma=gam, sigma_boot=sb, ci68_boot=ci, ci68_profile=_profile_interval(lng, L2),
                f_triple=float(W[iw, 1]), f_ca=float(W[iw, 2]), N_used=int(n.sum()),
                N_beyond_vmax=int(vt.size - n.sum()))


def est_bayes(vt, fws, log_prior_alpha=None, v_max=5.0, three_d=False, n_f=26, f_max=0.5,
              n_boot=50, seed=5):
    """Simplified Bayesian deprojection: posterior on gamma, marginalising the template set
    (fws: list of forward models, one per eccentricity exponent) and an outlier fraction
    f_out ~ U(0, f_max) with a linear outlier density on [0, v_max). Flat prior in ln gamma."""
    K = int(round(v_max / _DW))
    vt = np.asarray(vt, float)
    n = _hist(vt, K)
    if n.sum() < 50:
        raise ValueError("fewer than 50 pairs below v_max")
    na = len(fws)
    lpa = np.zeros(na) if log_prior_alpha is None else np.asarray(log_prior_alpha, float)
    edges = np.arange(K + 1) * _DW
    C = np.diff(edges ** 2) / edges[-1] ** 2
    fs = np.linspace(0, f_max, n_f)
    cache = {}

    def logP(gs):  # (ng, na, nf, K)
        key = (gs[0], gs[-1], len(gs))
        if key not in cache:
            B = np.stack([_pmf_grid(fw, gs, K, three_d=three_d) for fw in fws], axis=1)
            B /= B.sum(2, keepdims=True)
            M = (1 - fs)[None, None, :, None] * B[:, :, None, :] + fs[None, None, :, None] * C
            cache[key] = np.log(M)
        return cache[key]

    def log_marg(gs, cnt):
        L = logP(gs) @ cnt + lpa[None, :, None]  # (ng, na, nf)
        mx = L.max(axis=(1, 2), keepdims=True)
        return np.log(np.exp(L - mx).sum(axis=(1, 2))) + mx[:, 0, 0]

    g2, L2 = _two_pass(lambda gs: log_marg(gs, n))

    def post_summary(Lg):
        p = np.exp(Lg - Lg.max())
        cdf = np.cumsum(p) / p.sum()
        lg = np.log(g2)
        return [math.exp(np.interp(q, cdf, lg)) for q in (0.16, 0.5, 0.84)]

    lo, med, hi = post_summary(L2)
    rng = np.random.default_rng(seed)
    boots = [post_summary(log_marg(g2, rng.multinomial(int(n.sum()), n / n.sum()).astype(float)))[1]
             for _ in range(n_boot)]
    sb, ci = _boot_summary(boots)
    return dict(gamma=med, sigma_boot=sb, ci68_boot=ci, ci68_posterior=(lo, hi),
                sigma_posterior=0.5 * (hi - lo), N_used=int(n.sum()))


ESTIMATORS = ("median", "trimmed", "threshold", "mixture", "bayes")


def run_estimator(name, vt, sp, sm, template=None, sr=None, n_model=200000, seed=11, **kw):
    """Run one estimator on a bin. vt: v~ values; sp: sigma_vp/v_c(s); sm: sigma_lnM arrays."""
    if name not in ESTIMATORS:
        raise ValueError(f"estimator must be one of {ESTIMATORS}")
    template = template if template is not None else KeplerTemplate()
    if name == "bayes":
        alphas = kw.pop("alphas", None)
        if alphas is None:
            tmpls = [template]
        else:
            tmpls = [KeplerTemplate(alpha_e=a, lam=kw.get("lam", 1.0), seed=200 + i)
                     for i, a in enumerate(alphas)]
        kw.pop("lam", None)
        fws = [_Forward(t, sp, sm, sr, n_model=n_model // 2, seed=seed + i) for i, t in enumerate(tmpls)]
        return est_bayes(vt, fws, three_d=sr is not None, **kw)
    fw = _Forward(template, sp, sm, sr, n_model=n_model, seed=seed, kick=kw.pop("kick", (0.1, 5.0)))
    fn = {"median": est_full_median, "trimmed": est_trimmed, "threshold": est_threshold,
          "mixture": est_mixture}[name]
    return fn(vt, fw, **kw)


def gamma_per_bin(s, v_p, M, gN=None, sigma_vp=None, sigma_lnM=None, v_r=None, sigma_vr=None,
                  bins=(-11.0, -10.0, -9.5, -9.0, -8.5, -8.0), estimator="median", template=None,
                  target_N=None, r_over_s=1.0, n_model=200000, min_pairs=50, **kw):
    """gamma per log10(g_N [m s^-2]) bin. Returns a list of dicts (one per populated bin).
    If v_r is given (bayes only) the 3D velocity v~_3D = sqrt(v_p^2 + v_r^2)/v_c(s) is used."""
    s = _arr(s, "s")
    v_p = _arr(v_p, "v_p", allow_zero=True)
    M = _arr(M, "M")
    if not (s.size == v_p.size == M.size):
        raise ValueError("s, v_p, M must have equal length")
    gN = gN_proxy(s, M, r_over_s) if gN is None else _arr(gN, "gN")
    vc = v_circ(s, M)
    sp = np.zeros_like(s) if sigma_vp is None else _arr(np.broadcast_to(sigma_vp, s.shape), "sigma_vp", allow_zero=True) / vc
    sm = np.zeros_like(s) if sigma_lnM is None else _arr(np.broadcast_to(sigma_lnM, s.shape), "sigma_lnM", allow_zero=True)
    use3d = v_r is not None
    if use3d and estimator != "bayes":
        raise ValueError("v_r (3D velocities) is supported only by the bayes estimator")
    vt = v_p / vc if not use3d else np.sqrt(v_p ** 2 + np.asarray(v_r, float) ** 2) / vc
    sr = None
    if use3d:
        sr = np.zeros_like(s) if sigma_vr is None else _arr(np.broadcast_to(sigma_vr, s.shape), "sigma_vr", allow_zero=True) / vc
    b = np.asarray(bins, float)
    if b.size < 2 or np.any(np.diff(b) <= 0):
        raise ValueError("bins must be increasing log10(g_N) edges")
    lg = np.log10(gN)
    out = []
    for lo, hi in zip(b[:-1], b[1:]):
        m = (lg >= lo) & (lg < hi)
        if m.sum() < min_pairs:
            continue
        r = run_estimator(estimator, vt[m], sp[m], sm[m], template=template,
                          sr=None if sr is None else sr[m], n_model=n_model, **dict(kw))
        r.update(bin=(float(lo), float(hi)), N_bin=int(m.sum()), estimator=estimator)
        if target_N:
            r["sigma_at_target"] = sigma_at_target(r["sigma_boot"], r["N_used"], target_N)
        out.append(r)
    return out


# ----------------------------------------------------------------------------------------------
# closed form for circular orbits (used by the self-test and the demo)
# ----------------------------------------------------------------------------------------------
def circular_cdf(t, gamma=1.0, n_quad=4000):
    """P(v~ <= t) for circular orbits, isotropic orientation, random phase, under G -> gamma G."""
    t = np.atleast_1d(np.asarray(t, float))
    x = (t * t / gamma)[:, None]
    # u = cos(beta), beta in [0, pi/2] -> S = sin(beta), du = sin(beta) d beta; midpoint rule
    beta = (np.arange(n_quad) + 0.5) * (np.pi / 2) / n_quad
    S = np.sin(beta)[None, :]
    wq = np.sin(beta) * (np.pi / 2) / n_quad
    q = (1 - x / S) / S ** 2
    Gv = np.where(q <= 0, 1.0, np.where(q > 1, 0.0, (2 / np.pi) * np.arccos(np.sqrt(np.clip(q, 0, 1)))))
    return Gv @ wq


def circular_sample(n, gamma, rng):
    """Inverse-CDF draws from the closed-form circular distribution."""
    tg = np.linspace(0, math.sqrt(gamma), 3001)
    F = circular_cdf(tg, gamma)
    F = np.maximum.accumulate(F)
    F[0], F[-1] = 0.0, 1.0
    return np.interp(rng.random(n), F, tg)


def circular_mean_v2(gamma=1.0):
    ES = lambda a: (math.sqrt(math.pi) / 2) * math.gamma(a / 2 + 1) / math.gamma(a / 2 + 1.5)
    return gamma * (ES(1.0) - 0.5 * ES(3.0))


# ----------------------------------------------------------------------------------------------
# independent Kepler sampler for tests/demo: true anomaly from p(f|e) (Hwang et al. 2022 eq. 12)
# by rejection, random orientation by Gram-Schmidt. Written separately from KeplerTemplate.
# ----------------------------------------------------------------------------------------------
def _test_kepler_sample(n, rng, e_max=0.99, thermal=True):
    e = np.empty(0)
    while e.size < n:  # thermal f(e) = 2e by sqrt(U), rejecting e > e_max (renormalised)
        c = np.sqrt(rng.random(2 * n)) if thermal else rng.random(2 * n)
        e = np.concatenate([e, c[c <= e_max]])
    e = e[:n]
    f = np.empty(n)
    todo = np.arange(n)
    while todo.size:
        ee = e[todo]
        ft = rng.uniform(0, 2 * np.pi, todo.size)
        acc = rng.random(todo.size) < ((1 - ee) / (1 + ee * np.cos(ft))) ** 2
        f[todo[acc]] = ft[acc]
        todo = todo[~acc]
    p = 1 - e * e  # a = GM = 1
    r = p / (1 + e * np.cos(f))
    vr_, vt_ = e * np.sin(f) / np.sqrt(p), (1 + e * np.cos(f)) / np.sqrt(p)
    # orbit-plane vectors: radial and tangential unit vectors in a random orthonormal frame
    nvec = rng.standard_normal((n, 3))
    nvec /= np.linalg.norm(nvec, axis=1, keepdims=True)
    t1 = rng.standard_normal((n, 3))
    t1 -= np.sum(t1 * nvec, 1, keepdims=True) * nvec
    t1 /= np.linalg.norm(t1, axis=1, keepdims=True)
    t2 = np.cross(nvec, t1)
    rhat = np.cos(f)[:, None] * t1 + np.sin(f)[:, None] * t2
    that = -np.sin(f)[:, None] * t1 + np.cos(f)[:, None] * t2
    R = r[:, None] * rhat
    V = vr_[:, None] * rhat + vt_[:, None] * that
    s = np.hypot(R[:, 0], R[:, 1])
    vp = np.hypot(V[:, 0], V[:, 1])
    cospsi = (R[:, 0] * V[:, 0] + R[:, 1] * V[:, 1]) / (s * vp)
    return dict(e=e, r=r, v2=np.sum(V * V, 1), s=s, vp=vp, vt=vp * np.sqrt(s), cospsi=cospsi, vz=V[:, 2] * np.sqrt(s))


def _test_observe(vt_true, rng, sp, sm, gamma, f_triple=0.0, f_ca=0.0, v_max=5.0, kick=(0.1, 5.0)):
    """Test-side observation: scale by sqrt(gamma), mass scatter, Gaussian 2D noise, optional
    triple kicks and chance alignments (linear density on [0, v_max)). Independent code path."""
    n = vt_true.size
    a = np.sqrt(gamma) * vt_true * np.exp(0.5 * sm * rng.standard_normal(n))
    ang = rng.uniform(0, 2 * np.pi, n)
    x, y = a * np.cos(ang), a * np.sin(ang)
    trip = rng.random(n) < f_triple
    kap = np.exp(rng.uniform(np.log(kick[0]), np.log(kick[1]), n))
    kv = rng.standard_normal((n, 3))
    kv /= np.linalg.norm(kv, axis=1, keepdims=True)
    x = x + trip * kap * kv[:, 0]
    y = y + trip * kap * kv[:, 1]
    v = np.hypot(x + sp * rng.standard_normal(n), y + sp * rng.standard_normal(n))
    ca = rng.random(n) < f_ca
    v[ca] = v_max * np.sqrt(rng.random(ca.sum()))
    return v


# ----------------------------------------------------------------------------------------------
# self-test
# ----------------------------------------------------------------------------------------------
def selftest(verbose: bool = True) -> bool:
    import time
    t0 = time.time()
    results = []

    def check(name, ok, detail=""):
        results.append(bool(ok))
        if verbose:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}")

    rng = np.random.default_rng(2026)

    # R1 exact definition: <sin theta> = int_0^1 sqrt(1-u^2) du = pi/4 for isotropic projection;
    #    circular template s/r = sin(theta).
    tc = KeplerTemplate(alpha_e=None, n=200000, seed=1)
    m = tc.s1.mean()
    check("R1 <s/r> = pi/4 (isotropic projection, circular)", abs(m - math.pi / 4) < 3e-3,
          f"got {m:.4f}, exact {math.pi/4:.4f}")

    # R2 Banik & Zhao 2018 (MNRAS 480, 2660; arXiv:1805.12273, p. 14), fetched with fetch_text.py:
    #    "the rms 3D relative velocity between WB stars. Due to isotropy, this is expected to be
    #     sqrt(3/2)x larger than just its sky-projected component."
    tt = KeplerTemplate(alpha_e=1.0, n=200000, seed=2)
    ratio = math.sqrt(np.mean(tt.v31 ** 2) / np.mean(tt.vp1 ** 2))
    check("R2 rms v3D / rms v_p = sqrt(3/2) (Banik & Zhao 2018 p.14)", abs(ratio - math.sqrt(1.5)) < 5e-3,
          f"got {ratio:.4f}, ref {math.sqrt(1.5):.4f}")

    # R3 Banik & Zhao 2018 p. 5: "calculating v~ in this way provides an upper limit on
    #    v / sqrt(GM/r), a quantity which can't exceed sqrt(2) in Newtonian gravity."
    #    Circular orbits: v = sqrt(GM/r) exactly, so v~ <= 1 (limit of the same bound).
    ts = _test_kepler_sample(200000, rng)
    vmax_t, vmax_s, vmax_c = tt.vt.max(), ts["vt"].max(), tc.vt.max()
    check("R3 Newtonian v~ <= sqrt(2) (template and test sampler); circular v~ <= 1",
          vmax_t <= math.sqrt(2) + 1e-9 and vmax_s <= math.sqrt(2) + 1e-9 and vmax_c <= 1 + 1e-9,
          f"max template {vmax_t:.4f}, test sampler {vmax_s:.4f}, circular {vmax_c:.4f}")

    # R4 Wikipedia "Semi-major and semi-minor axes" (fetched): "averaging over the mean anomaly ...
    #    gives the time-average a(1 + e^2/2). The time-averaged value of the reciprocal of the
    #    radius, r^-1, is a^-1."  Checked for the template Kepler solver and the independent
    #    true-anomaly sampler, and vis-viva + <1/r> = 1/a gives <v^2> = GM/a.
    worst = 0.0
    for e0 in (0.3, 0.7, 0.9):
        Mm = rng.uniform(0, 2 * np.pi, 400000)
        E = _solve_kepler(Mm, np.full(Mm.size, e0))
        r = 1 - e0 * np.cos(E)
        worst = max(worst, abs(r.mean() / (1 + e0 * e0 / 2) - 1), abs(np.mean(1 / r) - 1))
    e_s = ts["e"]
    worst_s = max(abs(np.mean(ts["r"]) / np.mean(1 + e_s ** 2 / 2) - 1), abs(np.mean(1 / ts["r"]) - 1),
                  abs(np.mean(ts["v2"]) - 1))
    check("R4 <r> = a(1+e^2/2), <1/r> = 1/a, <v^2> = GM/a (Kepler solver and test sampler)",
          worst < 4e-3 and worst_s < 1e-2, f"max rel dev solver {worst:.1e}, sampler {worst_s:.1e}")

    # R5 Hwang, Ting & Zakamska 2022 (arXiv:2111.01789, p. 4), fetched: "A thermal eccentricity
    #    distribution (alpha = 1) leads to a uniform observed v-r angle distribution."
    #    KS distance of the sky-projected v-r angle from uniform on [0, pi].
    def ks_uniform(cp):
        ang = np.sort(np.arccos(np.clip(cp, -1, 1)) / np.pi)
        return np.max(np.abs(ang - (np.arange(ang.size) + 0.5) / ang.size))
    # The exact statement holds for the untruncated f(e) = 2e; e_max = 0.99 removes 2% of the
    # most eccentric orbits and shifts the KS distance to ~0.007, so this check uses e_max = 0.9999.
    k1 = ks_uniform(KeplerTemplate(alpha_e=1.0, e_max=0.9999, n=200000, seed=4).cospsi)
    k2 = ks_uniform(_test_kepler_sample(200000, rng, e_max=0.9999)["cospsi"])
    tu = KeplerTemplate(alpha_e=0.0, n=200000, seed=3)
    k3 = ks_uniform(tu.cospsi)
    check("R5 thermal -> uniform projected v-r angle (Hwang+2022); uniform-e is not",
          k1 < 0.006 and k2 < 0.006 and k3 > 0.03,
          f"KS thermal template {k1:.4f}, test sampler {k2:.4f}, uniform-e {k3:.4f} (KS 99%: 0.0036)")

    # R6 closed form (circular): exact moment E[v~^2] = E[S] - E[S^3]/2 = pi/4 - 3pi/32 (Gamma functions),
    #    quadrature CDF vs direct (u, phi) draws and vs the Kepler template at e = 0.
    u, ph = rng.random(400000), rng.uniform(0, 2 * np.pi, 400000)
    S = np.sqrt(1 - u * u)
    vdir = np.sqrt((1 - S * S * np.cos(ph) ** 2) * S)
    # independent circular sample: random orthonormal (r_hat, v_hat) pair by Gram-Schmidt
    ga = rng.standard_normal((200000, 3))
    ga /= np.linalg.norm(ga, axis=1, keepdims=True)
    gb = rng.standard_normal((200000, 3))
    gb -= np.sum(ga * gb, 1, keepdims=True) * ga
    gb /= np.linalg.norm(gb, axis=1, keepdims=True)
    vgs = np.sqrt((1 - gb[:, 2] ** 2) * np.sqrt(1 - ga[:, 2] ** 2))
    ks_gs = np.max(np.abs(circular_cdf(np.linspace(0.02, 0.99, 50)) - np.searchsorted(np.sort(vgs), np.linspace(0.02, 0.99, 50)) / vgs.size))
    tg = np.linspace(0.02, 0.99, 50)
    Fq = circular_cdf(tg)
    ks_dir = np.max(np.abs(Fq - np.searchsorted(np.sort(vdir), tg) / vdir.size))
    ks_tpl = np.max(np.abs(Fq - np.searchsorted(np.sort(tc.vt), tg) / tc.vt.size))
    mv2 = circular_mean_v2()
    check("R6 circular closed form: E[v~^2] exact, CDF vs direct draws and template",
          abs(np.mean(vdir ** 2) - mv2) < 2e-3 and abs(np.mean(tc.vt ** 2) - mv2) < 3e-3
          and abs(np.mean(vgs ** 2) - mv2) < 3e-3 and ks_dir < 4e-3 and ks_tpl < 5e-3 and ks_gs < 5e-3,
          f"E[v~^2] exact {mv2:.4f}, direct {np.mean(vdir**2):.4f}, template {np.mean(tc.vt**2):.4f},"
          f" Gram-Schmidt {np.mean(vgs**2):.4f}; KS direct {ks_dir:.4f}, template {ks_tpl:.4f},"
          f" Gram-Schmidt {ks_gs:.4f}; median {np.interp(0.5, Fq, tg):.4f}")

    # R7 recovery of gamma = 1 and 1.4, all families, (a) circular closed-form draws with a circular
    #    template, (b) independent thermal Kepler draws with the thermal template. Noise
    #    sigma~ ~ U(0.02, 0.08), mass scatter sigma_lnM = 0.1.
    #    Tolerance: 3 sigma_boot inflated by sqrt(1 + N/n_model) for template MC noise (not in the
    #    bootstrap; see ASSUMPTIONS), plus 0.01 absolute for the 0.04-wide histogram binning.
    N = 12000
    nmod = 100000
    for case, tmpl, alphas in (("circular", tc, None), ("thermal", tt, None)):
        for gtrue in (1.0, 1.4):
            vt_true = circular_sample(N, gtrue, rng) / math.sqrt(gtrue) if case == "circular" \
                else _test_kepler_sample(N, rng)["vt"]
            sp = rng.uniform(0.02, 0.08, N)
            sm = np.full(N, 0.1)
            vobs = _test_observe(vt_true, rng, sp, sm, gtrue)
            row = []
            okall = True
            for est in ESTIMATORS:
                kw = dict(n_boot=40) if est in ("mixture", "bayes") else dict(n_boot=100)
                if est == "bayes" and case == "thermal":
                    kw["alphas"] = (0.5, 1.0, 1.5)
                r = run_estimator(est, vobs, sp, sm, template=tmpl, n_model=nmod, **kw)
                sig = r["sigma_boot"]
                tol = 3 * sig * math.sqrt(1 + N / nmod) + 0.01
                okall &= abs(r["gamma"] - gtrue) < tol
                row.append(f"{est}={r['gamma']:.3f}±{sig:.3f}" + (f" (post {r['sigma_posterior']:.3f})" if est == 'bayes' else ''))
            check(f"R7 recover gamma={gtrue} ({case}, N={N})", okall, "; ".join(row))

    # R8 contaminated MOND-like sample: gamma=1.4, 15% triples (same nuisance shape), 5% chance
    #    alignments. The mixture must recover 1.4; the uncontaminated full-median must be biased UP
    #    (direction stated by Clarke 2020 / Banik & Zhao: triples populate the high-v~ tail).
    vt_true = _test_kepler_sample(N, rng)["vt"]
    sp = rng.uniform(0.02, 0.08, N)
    sm = np.full(N, 0.1)
    vobs = _test_observe(vt_true, rng, sp, sm, 1.4, f_triple=0.15, f_ca=0.05)
    rm = run_estimator("mixture", vobs[vobs < 5], sp[vobs < 5], sm[vobs < 5], template=tt, n_model=nmod, n_boot=40)
    rmed = run_estimator("median", vobs, sp, sm, template=tt, n_model=nmod, n_boot=100)
    tolm = 3 * rm["sigma_boot"] * math.sqrt(1 + N / nmod) + 0.01
    check("R8 mixture recovers gamma=1.4 with 15% triples + 5% chance alignments; median biased up",
          abs(rm["gamma"] - 1.4) < tolm and abs(rm["f_triple"] - 0.15) < 0.05 and rmed["gamma"] > 1.4 + 3 * rmed["sigma_boot"],
          f"mixture {rm['gamma']:.3f}±{rm['sigma_boot']:.3f} (f_t {rm['f_triple']:.3f}, f_ca {rm['f_ca']:.3f});"
          f" full-median {rmed['gamma']:.3f}±{rmed['sigma_boot']:.3f}")

    # R9 Laplace / Wikipedia "Median" (fetched): "The distribution of the sample median from a
    #    population with a density function f(x) is asymptotically normal with mean m and variance
    #    1/(4 n f(m)^2)". Compare (i) the spread of full-median gamma over 40 independent replicate
    #    samples and (ii) the bootstrap sigma with gamma/(m f(m) sqrt(N)); 40 replicates give the SD
    #    to ~11% (1 sigma), so a 35% band is ~3 sigma.
    Nr = 4000
    fwc = _Forward(tc, np.full(10, 0.0), np.full(10, 0.0), n_model=nmod, seed=9)
    reps, boots, anal = [], [], []
    for i in range(40):
        v = circular_sample(Nr, 1.0, rng)
        r = est_full_median(v, fwc, n_boot=60, seed=i)
        reps.append(r["gamma"])
        boots.append(r["sigma_boot"])
        anal.append(sigma_median_analytic(v, 1.0))
    sd_rep, sb, sa = np.std(reps, ddof=1), np.median(boots), np.median(anal)
    check("R9 sigma(full-median) vs asymptotic 1/(4 n f(m)^2) (Laplace)",
          abs(sd_rep / sa - 1) < 0.35 and abs(sb / sa - 1) < 0.25,
          f"replicate SD {sd_rep:.4f}, bootstrap {sb:.4f}, analytic {sa:.4f}")

    # R10 CLT root-N scaling used for DR4 forecasts: sigma(N)/sigma(4N) = 2 (exact definition).
    v1 = circular_sample(4000, 1.0, rng)
    v4 = circular_sample(16000, 1.0, rng)
    s1 = est_full_median(v1, fwc, n_boot=200, seed=1)["sigma_boot"]
    s4 = est_full_median(v4, fwc, n_boot=200, seed=2)["sigma_boot"]
    check("R10 sigma(N)/sigma(4N) = 2 and sigma_at_target", abs(s1 / s4 / 2 - 1) < 0.25 and
          abs(sigma_at_target(0.02, 10000, 40000) - 0.01) < 1e-15, f"ratio {s1/s4:.3f}")

    # R12 end-to-end SI plumbing through gamma_per_bin: two populations in different log10 g_N bins
    #    (s = 1 kau -> g_N ~ 4e-9 m/s^2 with gamma = 1; s = 15 kau -> g_N ~ 2e-11 m/s^2 with gamma = 1.4),
    #    M = 1.5 Msun, sigma_vp = 10 m/s (SI). Circular closed-form draws, circular template, median.
    AU, MSUN = 1.495978707e11, 1.98841e30
    s_arr = np.concatenate([np.full(8000, 1000 * AU), np.full(8000, 15000 * AU)])
    M_arr = np.full(16000, 1.5 * MSUN)
    vc_arr = np.sqrt(G * M_arr / s_arr)
    vt_arr = np.concatenate([circular_sample(8000, 1.0, rng), circular_sample(8000, 1.4, rng)])
    ang = rng.uniform(0, 2 * np.pi, 16000)
    vx = vt_arr * vc_arr * np.cos(ang) + 10.0 * rng.standard_normal(16000)
    vy = vt_arr * vc_arr * np.sin(ang) + 10.0 * rng.standard_normal(16000)
    rows = gamma_per_bin(s_arr, np.hypot(vx, vy), M_arr, sigma_vp=10.0, bins=(-11.5, -10.0, -8.0),
                         estimator="median", template=tc, n_model=100000, target_N=4 * 8000, n_boot=100)
    okb = len(rows) == 2 and all(abs(r["gamma"] - g0) < 3 * r["sigma_boot"] * math.sqrt(1 + 8000 / 1e5) + 0.01
                                 for r, g0 in zip(rows, (1.4, 1.0)))
    okb &= all(abs(r["sigma_at_target"] / r["sigma_boot"] - 0.5) < 1e-12 for r in rows)
    check("R12 gamma_per_bin SI end-to-end (1.4 at low g_N, 1.0 at high g_N; sigma at 4N = sigma/2)", okb,
          "; ".join(f"bin {r['bin']}: {r['gamma']:.3f}±{r['sigma_boot']:.3f} (N={r['N_bin']})" for r in rows))

    # R13 published worked example, Banik & Zhao 2018 p. 14 (fetched): "For a WB system with
    #    M = 1.5M_sun and separation r = 20 kAU, Newtonian gravity predicts a circular velocity of
    #    260 m/s (Equation 3)." 260 is quoted to 2 significant figures, hence the 2% tolerance.
    vc20 = float(v_circ(20000 * AU, 1.5 * MSUN)[0])
    check("R13 v_c(20 kau, 1.5 Msun) = 260 m/s (Banik & Zhao 2018)", abs(vc20 / 260.0 - 1) < 0.02,
          f"got {vc20:.1f} m/s")

    # R11 refusals
    bad = 0
    for fn in (lambda: vtilde([-1.0], [1.0], [1.0]), lambda: KeplerTemplate(alpha_e=-1.5),
               lambda: est_full_median(np.full(100, 50.0), fwc, n_boot=0),
               lambda: gN_proxy([1.0], [1.0], r_over_s=0.5)):
        try:
            fn()
        except ValueError:
            bad += 1
    check("R11 out-of-range inputs raise ValueError", bad == 4, f"{bad}/4 raised")

    if verbose:
        print(f"{sum(results)}/{len(results)} checks passed in {time.time()-t0:.1f} s")
    return all(results)


# ----------------------------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------------------------
def _q(text, unit):
    if _ut is None:
        return float(text)
    try:
        return float(text)
    except ValueError:
        return _ut.Q(text).to(unit)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sc = sub.add_parser("scale", help="root-N scaling of sigma to a target sample size")
    sc.add_argument("--sigma", type=float, required=True)
    sc.add_argument("--n", type=float, required=True)
    sc.add_argument("--target-n", type=float, required=True)
    dm = sub.add_parser("demo", help="synthetic thermal-Kepler sample (test sampler), all estimators")
    dm.add_argument("--gamma", type=float, default=1.0)
    dm.add_argument("--n", type=int, default=20000)
    dm.add_argument("--sep", default="5000 au")
    dm.add_argument("--mass", default="1.5 Msun")
    dm.add_argument("--sigma-v", default="20 m/s")
    dm.add_argument("--sigma-lnM", type=float, default=0.1)
    dm.add_argument("--f-triple", type=float, default=0.0)
    dm.add_argument("--f-ca", type=float, default=0.0)
    dm.add_argument("--alpha-e", type=float, default=1.0, help="template eccentricity exponent")
    dm.add_argument("--target-n", type=float, default=None)
    dm.add_argument("--estimators", default="all")
    ft = sub.add_parser("fit", help="fit arrays from an .npz file (SI units)")
    ft.add_argument("--npz", required=True)
    ft.add_argument("--estimator", default="median")
    ft.add_argument("--bins", type=float, nargs="+", default=[-11, -10, -9.5, -9, -8.5, -8])
    ft.add_argument("--alpha-e", type=float, default=1.0)
    ft.add_argument("--target-n", type=float, default=None)
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    if a.cmd == "scale":
        print(f"sigma_stat at N={a.target_n:g}: {sigma_at_target(a.sigma, a.n, a.target_n):.5f} (from {a.sigma} at N={a.n:g})")
        return 0
    if a.cmd == "demo":
        rng = np.random.default_rng(42)
        s, M, sv = _q(a.sep, "m"), _q(a.mass, "kg"), _q(a.sigma_v, "m/s")
        vc = math.sqrt(G * M / s)
        sp = np.full(a.n, sv / vc)
        sm = np.full(a.n, a.sigma_lnM)
        vt = _test_observe(_test_kepler_sample(a.n, rng)["vt"], rng, sp, sm, a.gamma, a.f_triple, a.f_ca)
        print(f"s = {s:.4e} m, M = {M:.4e} kg, v_c(s) = {vc:.1f} m/s, g_N = G M/s^2 = {G*M/s**2:.3e} m/s^2,"
              f" sigma~ = {sv/vc:.4f}; true gamma = {a.gamma}, f_triple = {a.f_triple}, f_ca = {a.f_ca}")
        tmpl = KeplerTemplate(alpha_e=a.alpha_e)
        ests = ESTIMATORS if a.estimators == "all" else a.estimators.split(",")
        for est in ests:
            kw = dict(n_boot=40) if est in ("mixture", "bayes") else dict(n_boot=100)
            v = vt[vt < 5] if est in ("mixture", "bayes") else vt
            r = run_estimator(est, v, sp[: v.size], sm[: v.size], template=tmpl, **kw)
            extra = f"; sigma at N={a.target_n:g}: {sigma_at_target(r['sigma_boot'], r['N_used'], a.target_n):.4f}" if a.target_n else ""
            print(f"{est:9s} gamma = {r['gamma']:.4f} ± {r['sigma_boot']:.4f} (boot 68% {r['ci68_boot'][0]:.4f}-{r['ci68_boot'][1]:.4f}){extra}")
        return 0
    if a.cmd == "fit":
        d = np.load(a.npz)
        get = lambda k: d[k] if k in d.files else None
        ests = ESTIMATORS if a.estimator == "all" else (a.estimator,)
        for est in ests:
            res = gamma_per_bin(d["s"], d["v_p"], d["M"], gN=get("gN"), sigma_vp=get("sigma_vp"),
                                sigma_lnM=get("sigma_lnM"), bins=a.bins, estimator=est,
                                template=KeplerTemplate(alpha_e=a.alpha_e), target_N=a.target_n)
            for r in res:
                print(est, r["bin"], r["N_bin"], f"{r['gamma']:.4f} ± {r['sigma_boot']:.4f}",
                      f"(at target: {r.get('sigma_at_target', float('nan')):.4f})")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
