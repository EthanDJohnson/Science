#!/usr/bin/env python3
"""warp_shell.py - the constant-velocity "warp shell" of Fuchs et al. 2024, rebuilt.

Source of the construction: J. Fuchs, C. Helmerich, A. Bobrick, L. Sellers, B. Melcher,
G. Martire, "Constant velocity physical warp drive solution", Class. Quantum Grav. 41,
095013 (2024), arXiv:2405.02709, Sections 3-4, eqs. (16)-(28). Numerical method: Helmerich
et al., CQG 41, 095009 (2024), arXiv:2404.03095 (Warp Factory, MATLAB function
metricGet_WarpShellComoving.m).

WHAT IT COMPUTES
----------------
For a spherical shell of inner radius R1, outer radius R2 and total mass M:

1. Paper's initial guess (eqs. 19-21), SI units, rho = MASS density [kg/m^3]:
     rho'(r) = 3M / (4 pi (R2^3 - R1^3))      for R1 <= r <= R2, else 0
     m'(r)   = M (r^3 - R1^3)/(R2^3 - R1^3)    inside the shell
     dP'/dr  = -G (rho' + P'/c^2)(m' + 4 pi r^3 P'/c^2) / (r^2 (1 - 2 G m'/(c^2 r))),
     P'(R2) = 0, P' = 0 for r < R1 (vacuum interior).
   NOTE: eq. (21) as printed in the arXiv PDF carries the factors (rho'/c^2 + P'/c^4) and
   (m'/r^2 + 4 pi r P'/c^2), which is not dimensionally consistent with rho' in kg/m^3;
   we integrate the standard SI TOV equation above (it reproduces the Newtonian limit and the
   Schwarzschild interior solution, see selftest).
2. Paper's smoothing (eq. 22): moving average (MATLAB `smooth`: odd window, window shrinks
   symmetrically at the array ends), applied n_pass = 4 times, with span_rho = ratio * span_P.
   The paper's text gives ratio ~ 1.72; the public Warp Factory code uses 1.79. The paper does
   NOT print the absolute span (the code gives it in grid samples), so span_P [m] is a user
   parameter; our default (see DEFAULT_SPAN_FRAC) is OUR choice, not the paper's.
3. Mass profile from the smoothed density (eq. 23): m(r) = int_0^r 4 pi r^2 rho~ dr.
   ADM mass M_ADM = m(infinity); smoothing on a radial grid does not conserve int r^2 rho dr
   exactly, so M_ADM differs slightly from the input M (reported).
4. Metric (eqs. 16, 24, 25), static, spherical, comoving with the shell:
     ds^2 = -e^{2a} c^2 dt^2 + e^{2b} dr^2 + r^2 dOmega^2,
     e^{2b} = (1 - 2 G m/(c^2 r))^-1,
     da/dr  = G (m/(c^2 r^2) + 4 pi r P~/c^4) / (1 - 2 G m/(c^2 r)),
     a(r_max) = (1/2) ln(1 - 2 G M_ADM/(c^2 r_max))   (Schwarzschild outside the matter).
   Outside the matter support the metric is exactly Schwarzschild with mass M_ADM (Birkhoff);
   inside R1 (if no smoothed matter reaches there) it is flat with constant lapse e^{a(0)}.
5. Stress-energy the metric actually requires (exact for zero shift, from G_mu_nu):
     energy density   eps = rho~ c^2                              [J/m^3]
     radial pressure  p_r = P~                                     [Pa]
     tangential       p_t = p_r + (r/2) (dp_r/dr + (eps + p_r) da/dr)  [Pa]
   (the last is the anisotropic TOV identity, i.e. div T = 0). Static, diagonal in the
   orthonormal frame, so Hawking-Ellis type I and the energy conditions are tested EXACTLY:
     NEC eps+p_r >= 0, eps+p_t >= 0;  WEC adds eps >= 0;
     SEC adds eps + p_r + 2 p_t >= 0;  DEC eps >= |p_r|, eps >= |p_t|.
   Unsmoothed (smooth=False): P' jumps from 0 to P'(R1) at R1, so p_t has a delta-function
   sheet at R1 with surface (hoop) pressure R1 P'(R1)/2 [N/m] and zero surface energy: that
   sheet violates the DEC. This is why the paper smooths.
6. Warp shift (eqs. 26-28), coordinates x^0 = c t, x, y, z (all in metres):
     g_0x(warp) = g_0x - S(r) (g_0x + beta_warp) = -S(r) beta_warp   (g_0x = 0 for the shell)
     S(r) = 1 for r < R1+Rb;  1 - f(r) between;  0 for r > R2-Rb,
     f(r) = [exp((R2'-R1') (1/(r-R2') + 1/(r-R1'))) + 1]^-1,  R1' = R1+Rb, R2' = R2-Rb.
   Eq. (28) as printed uses R1, R2 inside f while switching at R1+Rb, R2-Rb, which makes S
   discontinuous for Rb > 0; we use the buffered radii (identical to eq. 28 when Rb = 0).
   Only g_0x is modified (as in the paper and the code); g_00 = -e^{2a} is kept, so the
   ADM lapse inside becomes N^2 = e^{2a} + beta_i beta^i and the contravariant shift is
   beta^x = gamma^{xx} g_0x (= -beta_warp in the flat interior). Covariant shift beta_x = g_0x.
   In the flat interior, Eulerian (normal) observers move at dx/d(ct) = +beta_warp relative
   to observers at rest with the shell, a relative speed beta_warp/N_in (units of c).

PAPER'S PARAMETERS (verified from the arXiv text, p. 13 and p. 17, and Table 1 p. 26):
  "R1 = 10 m, R2 = 20 m, M = 4.49 x 10^27 kg (2.365 Jupiter masses)"; Section 4 says "the
  addition of shift inside the shell is possible for beta_warp = 0.02 without any energy
  condition violation", while Table 1 (photon time delay, 7.6 ns) is "for v_warp = 0.04 c".
  So the energy-condition-checked warp shell has beta_warp = 0.02, not 0.04.
  With our default spans (span_P = 1.0 m, span_rho = 1.72 m, 4 passes), M_ADM = 4.511e27 kg
  (+0.48 % over the input M, from smoothing), 2GM/(c^2 R2) = 0.333, rho' c^2 = 1.376e40 J/m^3,
  P'(R1) = 1.01e39 Pa, and the zero-shift shell meets NEC/WEC/SEC/DEC exactly (type I).
  The unsmoothed construction carries a hoop-stress sheet of 5.0e39 N/m at R1 (DEC fails).

FRAME. The metric returned by `metric_cartesian` is in the frame COMOVING WITH THE SHELL
(the paper's frame, Fig. 11). Its exterior is static Schwarzschild, so this frame is also the
asymptotic rest frame of the exterior: in these coordinates the shell does not move relative
to infinity; only the interior shift differs. `metric_boosted(v)` returns the same spacetime
in the frame where the whole shell moves at +v along x (exact Lorentz transformation of the
coordinates; time dependent), i.e. the "exterior rest frame" of a moving drive.

UNITS. SI throughout the Python API: M [kg], R1, R2, r, x, y, z, Rb, spans [m], rho [kg/m^3],
eps and pressures [J/m^3 = Pa], surface quantities [J/m^2, N/m]. beta_warp dimensionless
(units of c). Metric components are dimensionless with x^0 = c t.

VALIDITY / REFUSALS (ValueError): M <= 0; R1 < 0; R1 >= R2; 2GM/(c^2 R2) >= 8/9 (Buchdahl);
a TOV solution whose pressure diverges, goes negative or is non-finite; 2Gm/(c^2 r) >= 1
anywhere; |beta_warp| >= 1; Rb outside [0, (R2-R1)/2). Shifted metrics: the tool returns the
metric only; its stress-energy must be computed numerically (e.g. numeric_stress_energy).
The 8/9 bound is Buchdahl's for spheres; for a thick shell the TOV pressure can diverge at a
different compactness, which is caught by the divergence test.

PYTHON
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from warp_shell import build_shell
    s = build_shell(M=4.49e27, R1=10.0, R2=20.0, beta_warp=0.02)
    s.summary()["compactness_input"]      # 2GM/(c^2 R2), ~0.333
    g = s.metric_cartesian(0.0, 0.0, 0.0, 0.0)   # 4x4 at the centre, comoving frame
    s.profiles()["p_t"]                    # tangential pressure on the radial grid [Pa]

COMMAND LINE
    python3 .claude/skills/conundrum/scripts/warp_shell.py shell \
        --M "2.365 Mjup" --R1 "10 m" --R2 "20 m" --beta 0.02
    python3 .claude/skills/conundrum/scripts/warp_shell.py selftest
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from unit_tools import Q  # noqa: E402

G = Q("G").si
C = Q("c").si
MJUP = Q("Mjup").si
MSUN = Q("Msun").si
BUCHDAHL = 8.0 / 9.0
DEFAULT_SPAN_FRAC = 0.10      # OUR default: span_P = 0.10 (R2 - R1); not given in the paper
DEFAULT_RATIO = 1.72          # paper text, Sec. 3.1 ("s_rho/s_P ~ 1.72"); code uses 1.79


# ----------------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------------
def _tov_rhs(r, P, rho0, R1):
    """Isotropic TOV dP/dr inside a constant-density shell, SI (rho0 mass density)."""
    # m/r^2 written to stay finite at r -> 0 when R1 = 0
    m = (4.0 * math.pi / 3.0) * rho0 * (r ** 3 - R1 ** 3)
    m_over_r2 = (4.0 * math.pi / 3.0) * rho0 * (r - (R1 ** 3 / r ** 2 if R1 > 0 else 0.0))
    one_minus = 1.0 - (2.0 * G * m / (C ** 2 * r) if r > 0 else 0.0)
    if one_minus <= 0:
        raise ValueError("2Gm/(c^2 r) >= 1 inside the shell: horizon, no static shell")
    return -G * (rho0 + P / C ** 2) * (m_over_r2 + 4.0 * math.pi * r * P / C ** 2) / one_minus


def tov_constant_density_shell(M, R1, R2, n=4000):
    """Paper eq. (21): RK4 inward from P'(R2)=0. Returns (r [m], P' [Pa]) on [R1, R2]."""
    rho0 = 3.0 * M / (4.0 * math.pi * (R2 ** 3 - R1 ** 3))
    r = np.linspace(R2, R1, n + 1)
    P = np.zeros_like(r)
    h = r[1] - r[0]                     # negative
    cap = 1e6 * rho0 * C ** 2
    for i in range(n):
        ri, Pi = r[i], P[i]
        k1 = _tov_rhs(ri, Pi, rho0, R1)
        k2 = _tov_rhs(ri + h / 2, Pi + h * k1 / 2, rho0, R1)
        k3 = _tov_rhs(ri + h / 2, Pi + h * k2 / 2, rho0, R1)
        k4 = _tov_rhs(ri + h, Pi + h * k3, rho0, R1)
        P[i + 1] = Pi + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        if not np.isfinite(P[i + 1]) or P[i + 1] > cap:
            raise ValueError("TOV pressure diverges inside the shell (too compact for a static shell)")
        if P[i + 1] < 0:
            raise ValueError("TOV pressure went negative inside the shell")
    return r[::-1].copy(), P[::-1].copy()


def matlab_smooth(y, span_pts):
    """MATLAB smooth(y, span) moving average: odd span, symmetric window shrinking at ends."""
    span_pts = int(span_pts)
    if span_pts % 2 == 0:
        span_pts -= 1
    if span_pts < 3:
        return y.copy()
    half = (span_pts - 1) // 2
    n = len(y)
    cs = np.concatenate(([0.0], np.cumsum(y)))
    i = np.arange(n)
    h = np.minimum(half, np.minimum(i, n - 1 - i))
    return (cs[i + h + 1] - cs[i - h]) / (2 * h + 1)


def _cumtrapz(y, x):
    out = np.zeros_like(y)
    out[1:] = np.cumsum(0.5 * (y[1:] + y[:-1]) * np.diff(x))
    return out


def _hermite(xg, yg, dyg, x):
    """C1 cubic Hermite interpolation with known derivatives (vectorized)."""
    x = np.asarray(x, dtype=float)
    xc = np.clip(x, xg[0], xg[-1])
    k = np.clip(np.searchsorted(xg, xc) - 1, 0, len(xg) - 2)
    h = xg[k + 1] - xg[k]
    t = (xc - xg[k]) / h
    h00 = 2 * t ** 3 - 3 * t ** 2 + 1
    h10 = t ** 3 - 2 * t ** 2 + t
    h01 = -2 * t ** 3 + 3 * t ** 2
    h11 = t ** 3 - t ** 2
    return h00 * yg[k] + h10 * h * dyg[k] + h01 * yg[k + 1] + h11 * h * dyg[k + 1]


def shift_profile(r, R1, R2, Rb=0.0):
    """Paper eqs. (27)-(28), with buffered radii (see module docstring). Dimensionless."""
    r = np.asarray(r, dtype=float)
    a1, a2 = R1 + Rb, R2 - Rb
    S = np.where(r <= a1, 1.0, 0.0)
    mid = (r > a1) & (r < a2)
    rm = r[mid]
    with np.errstate(over="ignore"):
        arg = (a2 - a1) * (1.0 / (rm - a2) + 1.0 / (rm - a1))
        f = 1.0 / (np.exp(arg) + 1.0)
    S[mid] = 1.0 - f
    return S


# ----------------------------------------------------------------------------------------
# main object
# ----------------------------------------------------------------------------------------
class WarpShell:
    """Result of build_shell; all arrays on the radial grid self.r [m], SI units."""

    def __init__(self, **kw):
        self.__dict__.update(kw)

    # radial metric functions (callables, SI)
    def a(self, r):
        return _hermite(self.r, self.a_grid, self.da_grid, np.abs(r))

    def m(self, r):
        r = np.asarray(r, dtype=float)
        out = _hermite(self.r, self.m_grid, 4 * math.pi * self.r ** 2 * self.rho_grid, np.abs(r))
        return np.where(np.abs(r) >= self.r[-1], self.M_ADM, out)

    def lapse_static(self, r):
        """e^{a(r)}: sqrt(-g_00), the static lapse before the shift is added."""
        r = np.abs(np.asarray(r, dtype=float))
        out = np.exp(self.a(r))
        ext = r >= self.r[-1]
        return np.where(ext, np.sqrt(np.clip(1 - 2 * G * self.M_ADM / (C ** 2 * np.maximum(r, 1e-300)), 0, None)), out)

    def grr(self, r):
        """e^{2b(r)} = 1/(1 - 2Gm/(c^2 r))."""
        r = np.abs(np.asarray(r, dtype=float))
        with np.errstate(divide="ignore", invalid="ignore"):
            out = 1.0 / (1.0 - 2 * G * self.m(r) / (C ** 2 * r))
        return np.where(r > 0, out, 1.0)

    def S(self, r):
        return shift_profile(r, self.R1, self.R2, self.Rb)

    def metric_cartesian(self, ct, x, y, z):
        """g_{mu nu} (shape (..., 4, 4)), coordinates (ct, x, y, z) in metres, frame comoving
        with the shell (= exterior asymptotic rest frame). Time independent."""
        x, y, z = np.broadcast_arrays(np.asarray(x, float), np.asarray(y, float), np.asarray(z, float))
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        e2a = self.lapse_static(r) ** 2
        e2b = self.grr(r)
        rs = np.where(r > 0, r, 1.0)
        n = np.stack([x / rs, y / rs, z / rs], axis=-1)
        g = np.zeros(r.shape + (4, 4))
        g[..., 0, 0] = -e2a
        for i in range(3):
            for j in range(3):
                g[..., i + 1, j + 1] = (1.0 if i == j else 0.0) + (e2b - 1.0) * n[..., i] * n[..., j]
        g0x = -self.S(r) * self.beta_warp
        g[..., 0, 1] = g0x
        g[..., 1, 0] = g0x
        return g

    def metric_boosted(self, v):
        """Callable g'(ct', x', y, z) in the frame where the shell moves at +v (m/s) along x."""
        beta = v / C
        if not abs(beta) < 1:
            raise ValueError("|v| must be < c")
        gam = 1.0 / math.sqrt(1 - beta ** 2)
        L = np.array([[gam, -gam * beta, 0, 0], [-gam * beta, gam, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1.0]])

        def g_prime(ctp, xp, y, z):
            ct = gam * (np.asarray(ctp, float) - beta * np.asarray(xp, float))
            x = gam * (np.asarray(xp, float) - beta * np.asarray(ctp, float))
            g = self.metric_cartesian(ct, x, y, z)
            return np.einsum("am,bn,...ab->...mn", L, L, g)
        return g_prime

    def adm_fields(self, x, y, z):
        """Lapse N, contravariant shift beta^i (units of c) and gamma_ij at a point."""
        g = self.metric_cartesian(0.0, x, y, z)
        gam = g[..., 1:, 1:]
        beta_low = g[..., 0, 1:]
        beta_up = np.linalg.solve(gam, beta_low[..., None])[..., 0]
        N2 = np.einsum("...i,...i->...", beta_low, beta_up) - g[..., 0, 0]
        return np.sqrt(N2), beta_up, gam

    def profiles(self):
        return dict(r=self.r, rho_initial=self.rho0_grid, P_initial=self.P0_grid, rho=self.rho_grid,
                    eps=self.eps, p_r=self.p_r, p_t=self.p_t, m=self.m_grid, a=self.a_grid,
                    e2a=np.exp(2 * self.a_grid), e2b=1.0 / (1.0 - 2 * G * self.m_grid / (C ** 2 * np.where(self.r > 0, self.r, 1.0))),
                    S=self.S(self.r))

    def energy_conditions_static(self):
        """Exact type-I tests for the ZERO-SHIFT shell (pointwise margins, Pa)."""
        e, pr, pt = self.eps, self.p_r, self.p_t
        # vacuum points have all margins = 0; report minima over points carrying stress-energy
        mat = np.maximum(np.abs(e), np.maximum(np.abs(pr), np.abs(pt))) > 1e-12 * self.eps_peak
        e, pr, pt, rr = e[mat], pr[mat], pt[mat], self.r[mat]
        out = dict(NEC=np.minimum(e + pr, e + pt), WEC=np.minimum(e, np.minimum(e + pr, e + pt)),
                   SEC=np.minimum(np.minimum(e + pr, e + pt), e + pr + 2 * pt),
                   DEC=np.minimum(e - np.abs(pr), e - np.abs(pt)))
        res = {}
        for k, v in out.items():
            i = int(np.argmin(v))
            res[k] = dict(min_margin_Pa=float(v[i]), at_r_m=float(rr[i]),
                          holds=bool(v[i] >= -1e-9 * self.eps_peak))
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(e > 0, np.maximum(np.abs(pr), np.abs(pt)) / e, np.inf)
        j = int(np.argmax(ratio))
        res["max_|p|/eps"] = dict(value=float(ratio[j]), at_r_m=float(rr[j]))
        if self.sheet_hoop_N_per_m:
            res["sheet_at_R1"] = dict(surface_energy_J_m2=0.0, hoop_pressure_N_m=self.sheet_hoop_N_per_m,
                                      DEC_holds=False, NEC_holds=True)
            res["DEC"]["holds"] = False
        return res

    def summary(self):
        N_in, bup, _ = self.adm_fields(0.0, 0.0, 0.0)
        return dict(
            frame="comoving with the shell = asymptotic rest frame of the Schwarzschild exterior",
            M_input_kg=self.M, M_ADM_kg=self.M_ADM, M_ADM_Mjup=self.M_ADM / MJUP, M_ADM_Msun=self.M_ADM / MSUN,
            compactness_input=2 * G * self.M / (C ** 2 * self.R2),
            compactness_ADM_at_R2=2 * G * self.M_ADM / (C ** 2 * self.R2),
            max_2Gm_over_c2r=float(np.max(2 * G * self.m_grid[1:] / (C ** 2 * self.r[1:]))),
            rho_initial_kg_m3=self.rho_const, rho_peak_kg_m3=float(self.rho_grid.max()),
            eps_peak_J_m3=self.eps_peak, P_initial_peak_Pa=float(self.P0_grid.max()),
            p_r_peak_Pa=float(self.p_r.max()), p_t_max_Pa=float(self.p_t.max()), p_t_min_Pa=float(self.p_t.min()),
            sheet_hoop_at_R1_N_per_m=self.sheet_hoop_N_per_m,
            lapse_static_centre=float(self.lapse_static(0.0)),
            beta_warp=self.beta_warp, adm_lapse_centre=float(N_in), shift_up_x_centre=float(bup[0]),
            eulerian_speed_rel_shell_centre_c=float(abs(self.beta_warp) / N_in),
            smoothing=self.smoothing)


def build_shell(M, R1, R2, beta_warp=0.0, Rb=0.0, smooth=True, span_P=None, ratio=DEFAULT_RATIO,
                n_pass=4, N=8001, r_max=None, n_tov=4000):
    """Build the Fuchs et al. 2024 shell (SI in, SI out). See module docstring."""
    M, R1, R2 = float(M), float(R1), float(R2)
    if not M > 0:
        raise ValueError("M must be > 0")
    if R1 < 0 or not R1 < R2:
        raise ValueError("need 0 <= R1 < R2")
    comp = 2 * G * M / (C ** 2 * R2)
    if comp >= BUCHDAHL:
        raise ValueError(f"2GM/(c^2 R2) = {comp:.4f} >= 8/9 (Buchdahl): no static shell")
    if not abs(beta_warp) < 1:
        raise ValueError("|beta_warp| must be < 1")
    if not (0 <= Rb < (R2 - R1) / 2):
        raise ValueError("Rb must be in [0, (R2-R1)/2)")
    rho_const = 3 * M / (4 * math.pi * (R2 ** 3 - R1 ** 3))
    rs_tov, Ps_tov = tov_constant_density_shell(M, R1, R2, n=n_tov)
    sheet = 0.0
    if smooth:
        if span_P is None:
            span_P = DEFAULT_SPAN_FRAC * (R2 - R1)
        span_rho = ratio * span_P
        if r_max is None:
            r_max = R2 + max(R2, 4 * n_pass * span_rho)
        r = np.linspace(0.0, r_max, N)
        dr = r[1] - r[0]
        rho0 = np.where((r >= R1) & (r <= R2), rho_const, 0.0)
        P0 = np.where((r >= R1) & (r <= R2), np.interp(r, rs_tov, Ps_tov), 0.0)
        rho, P = rho0.copy(), P0.copy()
        sp_r = int(round(span_rho / dr)) | 1
        sp_p = int(round(span_P / dr)) | 1
        for _ in range(n_pass):
            rho = matlab_smooth(rho, sp_r)
            P = matlab_smooth(P, sp_p)
        m = _cumtrapz(4 * math.pi * r ** 2 * rho, r)
        smoothing = dict(span_P_m=sp_p * dr, span_rho_m=sp_r * dr, ratio=ratio, n_pass=n_pass, dr_m=dr)
    else:
        # exact piecewise grid with R1 and R2 as nodes; analytic m
        if r_max is None:
            r_max = 2.0 * R2
        parts = [np.linspace(0, R1, 200, endpoint=False)] if R1 > 0 else []
        parts += [rs_tov, np.linspace(R2, r_max, 400)[1:]]
        r = np.concatenate(parts)
        inshell = (r >= R1) & (r <= R2)
        rho0 = np.where(inshell, rho_const, 0.0)
        P0 = np.where(inshell, np.interp(r, rs_tov, Ps_tov), 0.0)
        rho, P = rho0.copy(), P0.copy()
        m = np.where(r < R1, 0.0, np.where(r > R2, M, M * (np.clip(r, R1, R2) ** 3 - R1 ** 3) / (R2 ** 3 - R1 ** 3)))
        sheet = R1 * Ps_tov[0] / 2.0 if R1 > 0 else 0.0
        smoothing = None
    if np.any(P < 0) or not np.all(np.isfinite(P)):
        raise ValueError("pressure negative or non-finite after construction")
    M_ADM = float(m[-1])
    rr = np.where(r > 0, r, 1.0)
    one_minus = 1 - 2 * G * m / (C ** 2 * rr)
    if np.any(one_minus <= 0):
        raise ValueError("2Gm/(c^2 r) >= 1 somewhere: horizon")
    da = np.where(r > 0, G * (m / (C ** 2 * rr ** 2) + 4 * math.pi * rr * P / C ** 4) / one_minus, 0.0)
    a_end = 0.5 * math.log(1 - 2 * G * M_ADM / (C ** 2 * r[-1]))
    a = a_end - (_cumtrapz(da, r)[-1] - _cumtrapz(da, r))
    eps = rho * C ** 2
    if smooth:
        dP = np.gradient(P, r)
    else:
        dP = np.array([_tov_rhs(ri, Pi, rho_const, R1) if (R1 <= ri <= R2 and ri > 0) else 0.0
                       for ri, Pi in zip(r, P)])
    p_t = P + 0.5 * r * (dP + (eps + P) * da)
    return WarpShell(M=M, R1=R1, R2=R2, Rb=Rb, beta_warp=float(beta_warp), r=r, rho0_grid=rho0,
                     P0_grid=P0, rho_grid=rho, m_grid=m, a_grid=a, da_grid=da, eps=eps, p_r=P, p_t=p_t,
                     M_ADM=M_ADM, rho_const=rho_const, eps_peak=float(eps.max()),
                     sheet_hoop_N_per_m=sheet, smoothing=smoothing, tov=(rs_tov, Ps_tov))


def thin_shell_surface_integrals(shell):
    """Proper-thickness integrals sigma = int eps e^b dr [J/m^2] and
    P_surf = int p_t e^b dr (+ the R1 sheet) [N/m]; for comparison with Israel's thin shell."""
    r, e, pr, pt = shell.r, shell.eps, shell.p_r, shell.p_t
    rr = np.where(r > 0, r, 1.0)
    eb = 1 / np.sqrt(1 - 2 * G * shell.m_grid / (C ** 2 * rr))
    sel = (r >= shell.R1) & (r <= shell.R2)
    sig = np.trapezoid(e[sel] * eb[sel], r[sel]) if hasattr(np, "trapezoid") else np.trapz(e[sel] * eb[sel], r[sel])
    tr = np.trapezoid if hasattr(np, "trapezoid") else np.trapz
    Ps = tr(pt[sel] * eb[sel], r[sel]) + shell.sheet_hoop_N_per_m
    Pr = tr(pr[sel] * eb[sel], r[sel])
    return sig, Ps, Pr


# ----------------------------------------------------------------------------------------
# selftest
# ----------------------------------------------------------------------------------------
def selftest(verbose: bool = True) -> bool:
    ok_all = True

    def check(name, got, want, rel):
        nonlocal ok_all
        ok = abs(got - want) <= rel * abs(want)
        ok_all &= ok
        if verbose:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got:.10g}, want {want:.10g} (rel tol {rel:g})")

    def truth(name, cond):
        nonlocal ok_all
        ok_all &= bool(cond)
        if verbose:
            print(f"[{'PASS' if cond else 'FAIL'}] {name}")

    def raises(name, fn):
        try:
            fn()
        except ValueError:
            truth(name, True)
            return
        truth(name, False)

    # --- 1. Schwarzschild interior solution (R1 = 0, constant density, isotropic) --------
    # Schwarzschild 1916. Source text (fetch_text.py, en.wikipedia.org/wiki/Interior_Schwarzschild_metric,
    # "Pressure and stability"): "Its value is p = rho c^2 (cos eta - cos eta_g)/(3 cos eta_g - cos eta).
    # As expected, the pressure is zero at the surface of the sphere". There cos eta = sqrt(1 - r^2/Rhat^2),
    # cos eta_g = sqrt(1 - R^2/Rhat^2), Rhat^2 = c^2 R^3/(2GM); the same page's metric gives the
    # lapse e^a = (3/2) cos eta_g - (1/2) cos eta. The central pressure diverges when 3 cos eta_g = 1,
    # i.e. 2GM/(c^2 R) = 8/9 (Buchdahl).
    R, comp = 10.0, 0.5
    M = comp * C ** 2 * R / (2 * G)
    s = build_shell(M, 0.0, R, smooth=False)
    rho = 3 * M / (4 * math.pi * R ** 3)
    A = math.sqrt(1 - comp)
    for rt in (0.0, 5.0):
        Br = math.sqrt(1 - comp * rt ** 2 / R ** 2)
        Pc = rho * C ** 2 * (Br - A) / (3 * A - Br)
        check(f"Schwarzschild interior p({rt} m), 2GM/c^2R=0.5", float(np.interp(rt, s.r, s.p_r)), Pc, 1e-7)
        check(f"Schwarzschild interior lapse e^a({rt} m)", float(s.lapse_static(rt)), 1.5 * A - 0.5 * Br, 1e-6)

    # --- 2. Buchdahl limit: central pressure diverges as 2GM/c^2R -> 8/9 -----------------
    raises("refuses 2GM/(c^2 R2) = 8/9 exactly", lambda: build_shell(BUCHDAHL * C ** 2 * R / (2 * G), 0.0, R))
    raises("refuses R1 >= R2", lambda: build_shell(1e27, 20.0, 20.0))
    comp = 0.88
    M = comp * C ** 2 * R / (2 * G)
    s = build_shell(M, 0.0, R, smooth=False, n_tov=20000)
    A = math.sqrt(1 - comp)
    Pc = (3 * M / (4 * math.pi * R ** 3)) * C ** 2 * (1 - A) / (3 * A - 1)
    check("Schwarzschild interior central pressure at 2GM/c^2R = 0.88 (near Buchdahl)",
          float(s.p_r[0]), Pc, 1e-4)

    # --- 3. Newtonian limit of the constant-density shell --------------------------------
    # c -> infinity limit of the TOV eq. (21) of Fuchs et al.: Newtonian hydrostatics
    # dP/dr = -G rho m(r)/r^2, m = (4pi/3) rho (r^3 - R1^3), P(R2) = 0  =>
    # P(r) = (4pi/3) G rho^2 [ (R2^2 - r^2)/2 + R1^3 (1/R2 - 1/r) ]   (elementary integral)
    R1, R2 = 10.0, 20.0
    M = 1e-7 * C ** 2 * R2 / (2 * G)
    s = build_shell(M, R1, R2, smooth=False)
    rho = 3 * M / (4 * math.pi * (R2 ** 3 - R1 ** 3))
    for rt in (R1, 15.0):
        Pn = (4 * math.pi / 3) * G * rho ** 2 * ((R2 ** 2 - rt ** 2) / 2 + R1 ** 3 * (1 / R2 - 1 / rt))
        # GR corrections are O(2GM/c^2R) = 1e-7
        check(f"Newtonian shell pressure P({rt} m), 2GM/c^2R2 = 1e-7", float(np.interp(rt, s.r, s.p_r)), Pn, 1e-5)

    # --- 4. Thin-shell limit: Israel junction conditions -----------------------------------
    # Static shell, Minkowski inside, Schwarzschild (mass M) outside, areal radius R:
    # sigma = (c^4/(4 pi G R)) [1 - sqrt(1 - 2GM/(c^2 R))]       [J/m^2]
    # P     = (c^4/(8 pi G R)) [(1 - GM/(c^2 R))/sqrt(1 - 2GM/(c^2 R)) - 1]   [N/m]
    # (Israel 1966.) Source text, Visser & Wiltshire 2004, arXiv:gr-qc/0310107 p. 6 (G = c = 1,
    # [[X]] = X_+ - X_-, theta = surface TENSION = -P, A = 4-acceleration of the shell):
    # "Imposing the junction conditions, similarly to the case of the static shell, we then have
    #  sigma = - 1/(4 pi a) [[ sqrt(1 - 2m(a)/a + adot^2) ]], (25) and
    #  theta = - 1/(8 pi) [[ sqrt(1 - 2m(a)/a + adot^2)/a + A ]], (26)".
    # Static (adot = 0), m_- = 0, m_+ = M, A_+ = (M/a^2)/sqrt(1-2M/a), A_- = 0 gives the two lines
    # above after restoring c^4/G.
    R, comp, d = 10.0, 0.5, 1e-3
    M = comp * C ** 2 * R / (2 * G)
    s = build_shell(M, R, R * (1 + d), smooth=False, n_tov=4000)
    sig, Ps, Pr = thin_shell_surface_integrals(s)
    Rm = R * (1 + d / 2)
    cm = 2 * G * M / (C ** 2 * Rm)
    sig_I = C ** 4 / (4 * math.pi * G * Rm) * (1 - math.sqrt(1 - cm))
    P_I = C ** 4 / (8 * math.pi * G * Rm) * ((1 - cm / 2) / math.sqrt(1 - cm) - 1)
    # thickness/R = 1e-3, so O(1e-3) differences from which radius is "the" shell radius
    check("thin-shell surface energy density vs Israel (2GM/c^2R = 0.5, dR/R = 1e-3)", sig, sig_I, 3e-3)
    check("thin-shell surface pressure vs Israel", Ps, P_I, 3e-3)
    truth("thin-shell radial surface stress -> 0 (|int p_r e^b dr| < 1e-2 P_Israel)", abs(Pr) < 1e-2 * P_I)

    # --- 5. zero shift: exterior exactly Schwarzschild, interior flat, constant lapse ------
    s = build_shell(4.49e27, 10.0, 20.0, beta_warp=0.0)
    rt = np.array([s.r[-1] * 0.95, s.r[-1] * 0.9])
    g = s.metric_cartesian(0.0, 0.0, rt, 0.0)
    want_tt = -(1 - 2 * G * s.M_ADM / (C ** 2 * rt))
    check("smoothed shell: exterior g_tt = -(1 - 2GM_ADM/c^2 r)", float(g[0, 0, 0]), float(want_tt[0]), 1e-6)
    check("smoothed shell: exterior g_yy = 1/(1 - 2GM_ADM/c^2 r)", float(g[1, 2, 2]), float(-1 / want_tt[1]), 1e-6)
    gi = s.metric_cartesian(0.0, np.array([0.0, 3.0, -2.0]), np.array([0.0, 1.0, 4.0]), np.array([0.0, -5.0, 1.0]))
    truth("zero shift: interior metric = diag(-e^{2a0},1,1,1) at 3 points (flat, constant lapse)",
          np.allclose(gi, gi[0], rtol=1e-9, atol=1e-12) and np.allclose(gi[0, 1:, 1:], np.eye(3), atol=1e-12)
          and abs(gi[0, 0, 1]) == 0.0)
    su = build_shell(4.49e27, 10.0, 20.0, smooth=False)
    check("unsmoothed shell: ADM mass = M exactly", su.M_ADM, 4.49e27, 1e-12)

    # --- 6. Paper's worked example (Fuchs et al. 2024 Sec. 3.1) ---------------------------
    # "R1 = 10 m, R2 = 20 m, M = 4.49 x 10^27 kg (2.365 Jupiter masses)" (p. 13, fetched text)
    check("paper: 4.49e27 kg in Jupiter masses", 4.49e27 / MJUP, 2.365, 5e-4)
    # Fig. 4 energy-density axis is labelled x10^39 J/m^3 with ticks 0..15: constant density
    # rho' c^2 = 3Mc^2/(4pi(R2^3-R1^3)) = 1.38e40 J/m^3 lies on that scale (order check only).
    truth("paper Fig. 4 scale: 1e40 < rho' c^2 < 1.5e40 J/m^3", 1e40 < su.rho_const * C ** 2 < 1.5e40)
    # Fig. 4 pressure axis x10^38 Pa, ticks 0..15: our TOV P'(R1) should lie in 1e38..1.5e39 Pa
    truth(f"paper Fig. 4 scale: 1e38 < P'(R1) = {su.P0_grid.max():.3g} Pa < 1.5e39", 1e38 < su.P0_grid.max() < 1.5e39)

    # --- 7. Shift profile and frames --------------------------------------------------------
    # Exact definitions, Fuchs et al. p. 17: "gwarp 01 = g01 - Swarp(r)(g01 + beta_warp) (26)";
    # "Swarp(r) = 1 r < R1+Rb; 1 - f(r) R1+Rb < r < R2-Rb; 0 r > R2-Rb (27)";
    # "f(r) = (exp((R2-R1)(1/(r-R2) + 1/(r-R1))) + 1)^-1 (28)" (Rb = 0 here).
    S = shift_profile(np.array([5.0, 10.0, 15.0, 20.0, 25.0]), 10.0, 20.0)
    truth("eq. (27)-(28): S = 1, 1, 1/2, 0, 0 at r = 5, 10, 15, 20, 25 m",
          np.allclose(S, [1, 1, 0.5, 0, 0], atol=1e-12))
    sw = build_shell(4.49e27, 10.0, 20.0, beta_warp=0.02)
    g0 = sw.metric_cartesian(0.0, 0.0, 0.0, 0.0)
    truth("eq. (26): interior g_0x = -beta_warp", abs(g0[0, 1] + 0.02) < 1e-15)
    gb = sw.metric_boosted(0.0)(0.0, 1.0, 2.0, 3.0)
    truth("boost with v = 0 is the identity", np.allclose(gb, sw.metric_cartesian(0.0, 1.0, 2.0, 3.0)))
    # far field in a boosted frame must approach Minkowski (Lorentz invariance of eta)
    gfar = build_shell(1e20, 10.0, 20.0, smooth=False).metric_boosted(0.3 * C)(0.0, 0.0, 0.0, 15.0)
    truth("boosted weak-field metric -> eta", np.allclose(gfar, np.diag([-1, 1, 1, 1.0]), atol=1e-6))
    raises("refuses |beta_warp| >= 1", lambda: build_shell(4.49e27, 10.0, 20.0, beta_warp=1.0))

    if verbose:
        print("SELFTEST", "PASSED" if ok_all else "FAILED")
    return ok_all


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("selftest")
    sp = sub.add_parser("shell")
    sp.add_argument("--M", required=True, help='e.g. "2.365 Mjup" or "4.49e27 kg"')
    sp.add_argument("--R1", required=True)
    sp.add_argument("--R2", required=True)
    sp.add_argument("--beta", type=float, default=0.0, help="beta_warp (units of c)")
    sp.add_argument("--Rb", default="0 m")
    sp.add_argument("--span-P", default=None, help='pressure smoothing span, e.g. "1 m"')
    sp.add_argument("--ratio", type=float, default=DEFAULT_RATIO)
    sp.add_argument("--no-smooth", action="store_true")
    a = p.parse_args(argv)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    if a.cmd == "shell":
        s = build_shell(Q(a.M).expect("mass").si, Q(a.R1).expect("length").si, Q(a.R2).expect("length").si,
                        beta_warp=a.beta, Rb=Q(a.Rb).si, smooth=not a.no_smooth,
                        span_P=None if a.span_P is None else Q(a.span_P).si, ratio=a.ratio)
        for k, v in s.summary().items():
            print(f"{k}: {v}")
        print("energy conditions, zero-shift shell, exact type I:")
        for k, v in s.energy_conditions_static().items():
            print(f"  {k}: {v}")
        return 0
    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
