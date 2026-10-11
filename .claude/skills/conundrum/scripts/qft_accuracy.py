#!/usr/bin/env python3
"""qft_accuracy: particle production where qft_production.py cannot resolve the answer -- far below its
double-precision floor (|beta|^2 about 1e-28) and beyond first-order Born -- with every function saying
exactly WHICH quantity it returns (numpy + mpmath, no scipy). It imports qft_production.py (as qp) and
re-implements none of its solvers; qp's double-precision solvers serve as independent references here.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as qp.
    Pick ONE energy unit (e.g. eV, or units of the mass m) and give every energy, mass, momentum, frequency
    and inverse time in it; times are then in 1/energy and E-fields as eE in energy^2, omega^2 and V in
    energy^2. Number densities come out in energy^3. As in qp (precedent page_wootters.py) this deviates
    from schemas.md's "SI in the Python API" on purpose: qp's SI helpers convert, and the command line
    accepts units through unit_tools.Q ("0.511 MeV", "1e17 V/m", "1e-21 s").

What every result is (the traps)
    * |beta_k|^2 is the IN-IN expectation <in|N_out(k)|in>: the mean number of particles in mode k after the
      background has switched off (a complex field: equally many antiparticles in -k, pairs = particles; a
      real field: pairs = particles/2 after summing modes). It is NOT an in-out amplitude; the in-out
      (vacuum-persistence) probability of mode k is 1/|alpha_k|^2 (bosons) or 1 - n_k (fermions, per spin).
    * Per mode, not a rate and not integrated, unless a function says "per unit volume".
    * Only asymptotic in/out states have a particle meaning: nothing here reports a "number" while the
      background is on (transient vacuum polarisation).

PART A. High-precision single-mode Bogoliubov solvers (mpmath, 30-240 digits)
---------------------------------------------------------------------------
    Boson:   u'' + omega(t)^2 u = 0, u -> e^{-i w_in t}/sqrt(2 w_in) at t0;
             at t1: beta = sqrt(w/2) e^{-i w t1} (u - i u'/w), alpha = sqrt(w/2) e^{+i w t1} (u + i u'/w), w = w_out.
    Fermion: i dc/dt = (p(t) sigma_z + eps_perp sigma_x) c (spinor QED in a homogeneous E(t) along z, one spin
             state, p = k_par - e A(t), dp/dt = eE); start in the negative-energy adiabatic state at t0,
             n = |<positive-energy adiabatic state at t1|c(t1)>|^2 (Landau-Zener form; qp Part B).
    Integrator: qp's 4th-order Magnus scheme (two Gauss points, exact 2x2 exponential), here in mpmath.
    It is exact where omega is constant, and its truncation error is a smooth function of t, so the error
    of the extracted beta is itself exponentially small: RELATIVE, not absolute (measured: 2e-10 relative
    at 2.6e-44 with 2000 steps). The floor is therefore roundoff, 10^-dps, not 1e-16.
    Error estimate (returned, never assumed):
        precision doubling  ||beta(dps)| - |beta(2 dps)||, scaled by sqrt(steps) to the final step count (only
                            |beta| is checked: the phase of beta converges more slowly and is not reported);
        step halving        |beta(2N)| + (|beta(2N)| - |beta(N)|)/15 is returned (Richardson: the scheme is time-
                            symmetric, error h^4, h^6, ...), with error estimate ||beta(2N)| - |beta(N)||/15 (the
                            h^4 error of the 2N run: conservative for the extrapolated value);
        window ends         (eps_in + eps_out)/4, eps = |d omega/dt|/omega^2 at each end (boson) or |d theta/dt|/omega
                            (fermion): starting (extracting) with the zeroth-order vacuum where eps != 0 seeds
                            (misreads) |beta| by ~eps/4.
    dps doubles from 30 until the precision change is below rtol/16 (to 240); steps double from
    omega_max (t1 - t0)/0.8 until the step estimate is below rtol/2 (to max_steps); default rtol 1e-5 on |beta|
    (2e-5 on |beta|^2). The result is flagged resolved=False when the total relative error of |beta|^2
    exceeds flag_rel (strict=True raises ValueError instead).
    Cost: pure-Python mpmath, about 0.1-0.2 ms per step; a mode with omega_max (t1 - t0) ~ 2000 takes ~1-2 s.
    Not for m tau >> 1e4 (realistic laser pulses): use Part B there.
    Closed forms (mpmath, any precision) used as references:
      * tanh model omega^2 = k^2 + m^2 (A + B tanh rho t) (Bernard & Duncan 1977; Birrell & Davies sec. 3.4):
            |beta|^2 = sinh^2(pi w_-/rho) / (sinh(pi w_in/rho) sinh(pi w_out/rho)),  w_- = (w_out - w_in)/2;
      * Sauter pulse E0 sech^2(t/tau): Gavrilov & Gitman 1996 eqs. 42 (spinor, per spin) and 43 (scalar);
      * Poeschl-Teller dip omega^2 = w0^2 - V0 sech^2(rho t) (any real V0, Lenzi et al. 2022 eqs. D11-D12):
            |beta|^2 = |r/t|^2 = cos^2(pi sqrt(1/4 - V0/rho^2)) / sinh^2(pi w0/rho)
        (cos -> cosh of sqrt(V0/rho^2 - 1/4) for V0 > rho^2/4); zero (reflectionless) when
        V0 = -rho^2 p(p+1), p = 1, 2, ... (Ahmadiniaz et al. 2022).

PART B. Phase-integral (complex-time WKB) asymptotics: Dykhne, Davis-Pechukas, Pokrovsky-Khalatnikov
-----------------------------------------------------------------------------------------------------
    For any omega(t)^2 analytic near the real axis and > 0 on it, the turning points t_c (omega(t_c)^2 = 0)
    come in complex-conjugate pairs. With the branch of omega continued from omega > 0 on the real axis
    along the vertical path from Re t_c,
        K = |int_{t_c*}^{t_c} omega dt| = 2 Im int_{Re t_c}^{t_c} omega dt,
        |beta|^2 ~ e^{-2K} = exp(-4 Im int_{t_r}^{t_c} omega dt)   (t_r real: only the vertical part is imaginary)
    (Dykhne-Davis-Pechukas P ~ exp(-2 Im Delta(t_c)), Delta = int (E+ - E-) dt = 2 int omega dt; prefactor 1
    for a simple turning point). The dominant pair is the one with the SMALLEST K, which need not be the one
    nearest the real axis (the turning points are ranked by K). Two pairs of comparable K interfere (Dumlu & Dunne 2010, eqs. 7-8):
        N ~ e^{-2K1} + e^{-2K2} +- 2 cos(2 alpha) e^{-K1-K2}    (+ scalar, - spinor),
        alpha = L - sigma(K1) - sigma(K2),  L = |Re int_{t1*}^{t2} omega dt|,
        sigma(K) = (1/2)[(K/pi)(ln(K/pi) - 1) + Arg Gamma(1/2 - i K/pi)].
    Turning points and poles of omega^2 are found by a grid scan of a box in the upper half plane plus
    complex Newton/secant refinement (mpmath.findroot); the phase integrals by Gauss-Legendre quadrature in
    s along t = t_c + (Re t_c - t_c) s^2 (smooth through the square-root zero) with the branch tracked
    node by node. Refused (ValueError): real turning points (tunnelling, not over-barrier), a pole of
    omega^2 closer to the real axis than the dominant turning point (the DDP contour is then blocked),
    a double zero, more than two pairs within e^{-13.8} of the leading one (not validated).
    Accuracy: leading exponential x prefactor, relative error O(1/K) in general (power corrections in the
    adiabaticity parameter; Sauter scalar: e^{-pi/(4 eE0 tau^2)} - 1), exponentially small for the tanh model
    and the Sauter spinor, zero for Landau-Zener (all measured in the self-test).
    Closed-form exponents used as references: Landau-Zener/Schwinger 2K = pi eps_perp^2/eE; Sauter
    2K = pi tau (w_in + w_out) - 2 pi eE0 tau^2 (Fukushima et al. 2019 eq. 30); at k = 0 this is the
    Dunne-Schubert worldline-instanton action (pi m^2/eE) 2/(1 + sqrt(1 + gamma^2)), gamma = m omega/(eE),
    for E(t) = E sech^2(omega t) (Dunne & Schubert PRD 72 (2005) 105004, eq. 38).

PART C. Second-order Born (Dyson) for homogeneous backgrounds
-------------------------------------------------------------
    Scalar vertex: omega_k(t)^2 = omega0^2 + V(t), V -> 0 at both ends (L = -(1/2) V phi^2, real field, or
    -V|phi|^2, complex; omega0^2 = k^2 + m^2). Writing u = (a e^{-i w0 t} + b e^{+i w0 t})/sqrt(2 w0):
        a' = -i (V/2w0)(a + b e^{2iw0t}),   b' = +i (V/2w0)(a e^{-2iw0t} + b),   a(-inf) = 1, b(-inf) = 0,
        b1 = (i/2w0) int V e^{-2i w0 t} dt                                   (first order, as qp Part D)
        b2 = (1/2w0)^2 int dt V(t) [e^{-2i w0 t} F(t) - G(t)],  F = int_-inf^t V,  G = int_-inf^t V e^{-2i w0 t'}
        |beta|^2 = |b1|^2 + 2 Re(b1* b2) + O(V^4)       (Born-1: O(V^2) with O(V^3) error; Born-2: O(V^3), error O(V^4)).
    Fermion (two-level) vertex: H = (k_par - eA(t)) sigma_z + eps_perp sigma_x = H0 + W, W = -eA sigma_z, A -> 0 at
    both ends; in the eigenbasis of H0 (energies +-w0, mixing angle theta0 = atan2(eps_perp, k_par)):
        W_{+-} = eA sin theta0,  W_{++} = -W_{--} = -eA cos theta0,
        c1 = -i int W_{+-} e^{2i w0 t},  c2 = -int dt [W_{++}(t) int^t W_{+-} e^{2i w0 t'} + W_{+-} e^{2i w0 t} int^t W_{--}],
        n = |c1|^2 + 2 Re(c1* c2) + O(e^4)   (per spin state).
    Quadrature: composite 16-point Gauss-Legendre with spectral (Legendre) cumulative integration inside panels.

Assumptions and validity range
    Free fields in a classical, prescribed, spatially homogeneous background (no back-reaction); adiabatic
    in AND out regions. Part A needs omega^2 as an mpmath callable (it must return an mpmath number computed
    at the working precision); Part B needs it to accept complex mpmath numbers (analytic continuation);
    Part C takes numpy callables (double precision is enough: no cancellation in the Born integrals).

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import qft_accuracy as qa
    w2, (t0, t1) = qa.tanh_model_mp(0.5, 1.0, 2.0, 1.0, 0.07)            # k, m, A, B, rho (units of m)
    r = qa.bogoliubov_boson_mp(w2, t0, t1)                               # r["beta2"] ~ 2.6097e-44, r["beta2_relerr"]
    qa.tanh_model_beta2_mp(0.5, 1.0, 2.0, 1.0, 0.07)                     # closed form
    pt = qa.phase_integral_beta2(w2, (-50.0, 50.0), 30.0)                # pt["beta2"], pt["K"], pt["turning_points"]
    om2, p, ep, (t0, t1) = qa.sauter_mp(0.0, 0.0, 1.0, 0.03, 33.0)       # k_par, k_perp, m, eE0, tau
    qa.bogoliubov_fermion_mp(p, ep, t0, t1)["n"]                          # per spin; vs qa.sauter_n_mp(..., fermion=True)
    import numpy as np
    qa.born2_scalar_mode(lambda t: 0.1*np.exp(-t**2/0.18), [1.0, 2.0], -4.0, 4.0)["beta2_born2"]

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_accuracy.py selftest
    python3 .claude/skills/conundrum/scripts/qft_accuracy.py tanh --m 1 --A 2 --B 1 --rho 0.07 --k 0.5
    python3 .claude/skills/conundrum/scripts/qft_accuracy.py sauter --E "1e17 V/m" --tau "1e-18 s"     (electron default)
    python3 .claude/skills/conundrum/scripts/qft_accuracy.py sauter --m 1 --E 0.03 --tau 33 --kperp 0.2
    python3 .claude/skills/conundrum/scripts/qft_accuracy.py born2 --m 1 --eps 0.1 0.2 --tau 0.3
    python3 .claude/skills/conundrum/scripts/qft_accuracy.py convergence     (slow: error budgets, PI vs exact below 1e-40)
"""
from __future__ import annotations

import math
import os
import sys

import mpmath as mp
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, ".claude/skills/conundrum/scripts"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import qft_production as qp  # noqa: E402  (double-precision solvers, closed forms, SI helpers)

PI = math.pi
_MPTYPES = (mp.mpf, mp.mpc)


# ---------------------------------------------------------------- small helpers
def _finite(x, name: str) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a real number") from None
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v


def _pos(x, name: str) -> float:
    v = _finite(x, name)
    if v <= 0:
        raise ValueError(f"{name} must be > 0")
    return v


def _call_real(f, t, name: str):
    """Evaluate a user mpmath callable at real t; insist on an mpmath real result (precision must follow dps)."""
    v = f(t)
    if not isinstance(v, _MPTYPES):
        raise ValueError(f"{name} must return an mpmath number computed at the working precision "
                         f"(got {type(v).__name__}); build it from mpmath functions (mp.tanh, mp.exp, ...)")
    if isinstance(v, mp.mpc):
        if abs(v.imag) > abs(v.real) * mp.mpf(10) ** (-mp.mp.dps + 5) + mp.mpf(10) ** (-mp.mp.dps):
            raise ValueError(f"{name} must be real on the real axis")
        v = v.real
    return v


def _window(t0, t1):
    t0, t1 = _finite(t0, "t0"), _finite(t1, "t1")
    if t1 <= t0:
        raise ValueError("need finite t0 < t1")
    return t0, t1


def _omega_max(f, t0: float, t1: float, n: int = 257) -> float:
    """max sqrt|f(t)| on a uniform sample (double precision is enough to size the steps)."""
    best = 0.0
    with mp.workdps(20):
        for j in range(n):
            t = mp.mpf(t0) + (mp.mpf(t1) - mp.mpf(t0)) * j / (n - 1)
            best = max(best, math.sqrt(abs(float(f(t)))))
    return best


# ---------------------------------------------------------------- Part A: Magnus kernels in mpmath
def _magnus_boson_mp(omega2, t0, t1, n: int, dps: int):
    """Propagate the real 2x2 fundamental matrix of (u, u') with n Magnus-4 steps; return (beta, alpha)."""
    with mp.workdps(dps):
        t0, t1 = mp.mpf(t0), mp.mpf(t1)
        # end frequencies at THIS precision: a 30-digit w_in would seed |beta| ~ 1e-30 by itself
        w_in, w_out = mp.sqrt(omega2(t0)), mp.sqrt(omega2(t1))
        h = (t1 - t0) / n
        s3 = mp.sqrt(3)
        g1, g2 = (1 - s3 / 3) / 2, (1 + s3 / 3) / 2
        k12, hh = s3 * h * h / 12, h * h
        sqrt, cos, sin, cosh, sinh = mp.sqrt, mp.cos, mp.sin, mp.cosh, mp.sinh
        one, zero = mp.mpf(1), mp.mpf(0)
        y00, y01, y10, y11 = one, zero, zero, one
        for j in range(n):
            t = t0 + j * h
            a1, a2 = omega2(t + g1 * h), omega2(t + g2 * h)
            # Omega = (h/2)(A1 + A2) + (sqrt3 h^2/12)[A2, A1],  A = [[0, 1], [-omega^2, 0]]  (as qp._magnus_boson)
            c = k12 * (a2 - a1)
            ab = (a1 + a2) / 2
            q2 = c * c - hh * ab
            if q2 < 0:
                x = sqrt(-q2)
                C, S = cos(x), sin(x) / x
            elif q2 > 0:
                x = sqrt(q2)
                C, S = cosh(x), sinh(x) / x
            else:
                C = S = one
            m00, m01, m10, m11 = C + S * c, S * h, -S * h * ab, C - S * c
            y00, y01, y10, y11 = (m00 * y00 + m01 * y10, m00 * y01 + m01 * y11,
                                  m10 * y00 + m11 * y10, m10 * y01 + m11 * y11)
        u0 = mp.expj(-w_in * t0) / sqrt(2 * w_in)
        v0 = -1j * w_in * u0
        u, v = y00 * u0 + y01 * v0, y10 * u0 + y11 * v0
        beta = sqrt(w_out / 2) * (u - 1j * v / w_out) * mp.expj(-w_out * t1)
        alpha = sqrt(w_out / 2) * (u + 1j * v / w_out) * mp.expj(w_out * t1)
        return +beta, +alpha


def _magnus_fermion_mp(p_of_t, eps_perp, t0, t1, n: int, dps: int):
    """Propagate the SU(2) quaternion of i dc/dt = (p sigma_z + eps sigma_x) c with n Magnus-4 steps; return
    (amplitude in the positive-energy state at t1, amplitude in the negative-energy state)."""
    with mp.workdps(dps):
        t0, t1, ep = mp.mpf(t0), mp.mpf(t1), mp.mpf(eps_perp)
        h = (t1 - t0) / n
        s3 = mp.sqrt(3)
        g1, g2 = (1 - s3 / 3) / 2, (1 + s3 / 3) / 2
        ky = s3 * h * h / 6
        bx = h * ep
        sqrt, cos, sin = mp.sqrt, mp.cos, mp.sin
        q0, q1, q2, q3 = mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(0)      # U = q0 - i (q . sigma)
        for j in range(n):
            t = t0 + j * h
            z1, z2 = p_of_t(t + g1 * h), p_of_t(t + g2 * h)
            # b = (h/2)(a1 + a2) + (sqrt3 h^2/6)(a2 x a1), a = (eps, 0, p)   (as qp._magnus_two_level)
            by = ky * ep * (z2 - z1)
            bz = h * (z1 + z2) / 2
            nb = sqrt(bx * bx + by * by + bz * bz)
            a0 = cos(nb)
            sb = sin(nb) / nb if nb != 0 else mp.mpf(1)
            a1_, a2_, a3_ = sb * bx, sb * by, sb * bz
            # (a0 - i a.s)(q0 - i q.s) = (a0 q0 - a.q) - i (a0 q + q0 a + a x q).s
            q0, q1, q2, q3 = (a0 * q0 - a1_ * q1 - a2_ * q2 - a3_ * q3,
                              a0 * q1 + q0 * a1_ + a2_ * q3 - a3_ * q2,
                              a0 * q2 + q0 * a2_ + a3_ * q1 - a1_ * q3,
                              a0 * q3 + q0 * a3_ + a1_ * q2 - a2_ * q1)
        th0 = mp.atan2(ep, p_of_t(t0))
        th1 = mp.atan2(ep, p_of_t(t1))
        c0, c1 = -sin(th0 / 2), cos(th0 / 2)                         # negative-energy adiabatic state at t0
        # U = [[q0 - i q3, -i q1 - q2], [-i q1 + q2, q0 + i q3]]
        d0 = (q0 - 1j * q3) * c0 + (-1j * q1 - q2) * c1
        d1 = (-1j * q1 + q2) * c0 + (q0 + 1j * q3) * c1
        up = cos(th1 / 2) * d0 + sin(th1 / 2) * d1
        dn = -sin(th1 / 2) * d0 + cos(th1 / 2) * d1
        return +up, +dn


def _error_controlled(run, n0: int, dps0: int, rtol: float, atol: float, max_steps: int, max_dps: int):
    """Precision doubling, then step halving with Richardson extrapolation, on |small amplitude| from run(n, dps).

    The Magnus-4 scheme is time-symmetric, so |b(h)| = |b| + c4 h^4 + c6 h^6 + ...: R = |b_2n| + (|b_2n| - |b_n|)/15
    removes h^4, and |b_2n| - |b_n||/15 (the h^4 error of b_2n) is returned as R's error estimate (conservative
    once in the asymptotic regime, which the start at omega h <= 0.8 ensures; measured ratios 16.0-16.2)."""
    def tol(x):
        return max(rtol * x, atol)
    n, dps = n0, dps0
    b_lo, _ = run(n, dps)
    while True:                                   # precision doubling at fixed steps
        b_hi, _ = run(n, 2 * dps)
        perr = abs(abs(b_hi) - abs(b_lo))         # magnitudes: only |beta|^2 is reported (the phase converges slower)
        if perr <= tol(abs(b_hi)) / 16 or 2 * dps > max_dps:
            break
        dps, b_lo = 2 * dps, b_hi
    perr_n, prec_ok = n, perr <= tol(abs(b_hi)) / 16
    a_n = abs(b_lo)                               # continue at the verified precision
    while True:                                   # step halving + Richardson
        b_2n, o_2n = run(2 * n, dps)
        a_2n = abs(b_2n)
        serr = abs(a_2n - a_n) / 15
        rich = a_2n + (a_2n - a_n) / 15
        if serr <= tol(rich) / 2 or 4 * n > max_steps:
            break
        n, a_n = 2 * n, a_2n
    perr_final = perr * math.sqrt(2 * n / perr_n)  # roundoff grows like sqrt(steps)
    return {"amp": rich, "amp_raw": a_2n, "other": o_2n, "serr": serr, "perr": perr_final, "steps": 2 * n, "dps": dps,
            "converged": prec_ok and serr <= tol(rich) / 2}


def _finish(amp, serr, perr, end_err, flag_rel, strict, what):
    with mp.workdps(30):
        delta = serr + perr + end_err
        b2 = amp ** 2
        err2 = 2 * amp * delta + delta ** 2
        relerr = float(err2 / b2) if b2 > 0 else math.inf
    resolved = relerr <= flag_rel
    if strict and not resolved:
        raise ValueError(f"{what}: estimated relative error {relerr:.3g} > flag_rel = {flag_rel:g} "
                         f"(step {float(serr):.2g}, precision {float(perr):.2g}, window ends {float(end_err):.2g} "
                         "in the amplitude): widen the window, raise max_steps/max_dps, or use the phase integral")
    return b2, err2, relerr, resolved


def bogoliubov_boson_mp(omega2, t0: float, t1: float, rtol: float = 1e-5, atol: float = 0.0, dps: int = 30,
                        steps: int = None, max_steps: int = 2 ** 15, max_dps: int = 240, flag_rel: float = 1e-3,
                        strict: bool = False) -> dict:
    """High-precision |beta_k|^2 for u'' + omega(t)^2 u = 0 between adiabatic in/out vacua (one mode, mpmath).

    omega2(t) takes an mpmath real t (1/energy) and returns omega(t)^2 (energy^2) as an mpmath number computed with
    mpmath functions at the working precision. Precision doubles from `dps` until | |beta(dps)| - |beta(2 dps)| | <=
    tol/16, then steps double from `steps` (default omega_max (t1 - t0)/0.8) until the Richardson step estimate is
    <= tol/2, tol = max(rtol |beta|, atol) (see module docstring).

    Quantity: per-mode IN-IN expectation <in|N_out(k)|in> = |beta_k|^2 (mean number of particles in mode k after
        the background has switched off; dimensionless; not a rate, not a pair count) as an mpmath number, with
        'beta2_err' (absolute error estimate of |beta|^2 from precision doubling + step halving + window ends),
        'beta2_relerr', 'resolved' (beta2_relerr <= flag_rel), 'alpha2', 'vacuum_persistence_mode' = 1/|alpha|^2
        (in-out probability that mode pair k stays empty), 'normalisation_error' = ||alpha|^2 - |beta|^2 - 1|,
        'dps', 'steps', 'eps_end'.
    Valid when: omega^2 > 0 at both ends, t1 > t0, the background is classical and prescribed; |beta|^2 down to
        about 10^(-2 max_dps + 20) (default 1e-460); the window must be wide enough that eps_end/4 << |beta|
        (otherwise the result is flagged); omega_max (t1 - t0) up to ~1e4 with the default max_steps (cost ~0.12 ms
        per step at 30 digits)."""
    t0, t1 = _window(t0, t1)
    rtol, atol = float(rtol), float(atol)
    if not (rtol > 0 or atol > 0) or rtol < 0 or atol < 0:
        raise ValueError("need rtol >= 0, atol >= 0, not both zero")
    if int(dps) < 15 or int(max_dps) < int(dps):
        raise ValueError("need 15 <= dps <= max_dps")
    with mp.workdps(max(int(dps), 30)):
        w2i, w2o = _call_real(omega2, mp.mpf(t0), "omega2"), _call_real(omega2, mp.mpf(t1), "omega2")
        if not (w2i > 0 and w2o > 0):
            raise ValueError("omega^2 must be > 0 at both window ends (no particle interpretation otherwise)")
        w_in, w_out = mp.sqrt(w2i), mp.sqrt(w2o)      # reported only; the kernel recomputes them at its precision
        eps_in = abs(mp.diff(omega2, mp.mpf(t0))) / (2 * w_in ** 3)
        eps_out = abs(mp.diff(omega2, mp.mpf(t1))) / (2 * w_out ** 3)
        eps_end = max(eps_in, eps_out)
    n0 = int(steps) if steps is not None else max(64, math.ceil(_omega_max(omega2, t0, t1) * (t1 - t0) / 0.8))
    if n0 < 2 or n0 > max_steps:
        raise ValueError(f"need 2 <= steps <= max_steps (the window needs ~{n0} steps; raise max_steps or shorten it)")

    def run(n, d):
        return _magnus_boson_mp(omega2, t0, t1, n, d)

    ec = _error_controlled(run, n0, int(dps), rtol, atol, int(max_steps), int(max_dps))
    a, d = ec["other"], ec["dps"]
    end_err = (eps_in + eps_out) / 4 * abs(a)      # zeroth-order vacuum at t0 and zeroth-order extraction at t1
    b2, err2, relerr, resolved = _finish(ec["amp"], ec["serr"], ec["perr"], end_err, flag_rel, strict, "bogoliubov_boson_mp")
    with mp.workdps(d):
        a2 = abs(a) ** 2
        norm = abs(a2 - ec["amp_raw"] ** 2 - 1)
    return {"beta2": b2, "beta2_err": err2, "beta2_relerr": relerr, "resolved": resolved, "alpha2": a2,
            "vacuum_persistence_mode": 1 / a2, "normalisation_error": norm, "step_err": ec["serr"],
            "precision_err": ec["perr"], "end_err": end_err, "eps_end": float(eps_end), "steps": ec["steps"], "dps": d,
            "converged": ec["converged"], "omega_in": w_in, "omega_out": w_out}


def bogoliubov_fermion_mp(p_of_t, eps_perp, t0: float, t1: float, rtol: float = 1e-5, atol: float = 0.0,
                          dps: int = 30, steps: int = None, max_steps: int = 2 ** 15, max_dps: int = 240,
                          flag_rel: float = 1e-3, strict: bool = False) -> dict:
    """High-precision spinor-QED occupation n_k for a homogeneous E(t) (two-level reduction, one spin, mpmath).

    p_of_t(t) returns the kinetic momentum p(t) = k_par - e A(t) along E (energy) as an mpmath number;
    eps_perp = sqrt(m^2 + k_perp^2) (energy). Error control as bogoliubov_boson_mp.

    Quantity: per-mode, per-spin-state IN-IN mean number of electrons in mode k (= positrons in -k = pairs in that
        mode) after the field has switched off, n_k = |beta_k|^2 (dimensionless, mpmath number; multiply mode sums
        by 2 for both spins), with 'n_err' (absolute error estimate), 'n_relerr', 'resolved', 'unitarity_error'
        = |n + |<-|c>|^2 - 1|, 'vacuum_persistence_mode' = 1 - n (in-out, per spin), 'dps', 'steps', 'eps_end'.
    Valid when: E(t) homogeneous along z (no magnetic field), eps_perp > 0, the field is off at both ends
        (eps_end/4 << sqrt(n), else flagged), t1 > t0; n down to about 10^(-2 max_dps + 20)."""
    t0, t1 = _window(t0, t1)
    ep = _pos(eps_perp, "eps_perp")
    if not (rtol > 0 or atol > 0) or rtol < 0 or atol < 0:
        raise ValueError("need rtol >= 0, atol >= 0, not both zero")
    if int(dps) < 15 or int(max_dps) < int(dps):
        raise ValueError("need 15 <= dps <= max_dps")
    with mp.workdps(max(int(dps), 30)):
        eps_ends = []
        for te in (mp.mpf(t0), mp.mpf(t1)):
            p = _call_real(p_of_t, te, "p_of_t")
            om = mp.sqrt(mp.mpf(ep) ** 2 + p * p)
            eps_ends.append(mp.mpf(ep) * abs(mp.diff(p_of_t, te)) / om ** 3)   # |d theta/dt|/omega
        eps_end = max(eps_ends)

    def w2(t):
        return mp.mpf(ep) ** 2 + p_of_t(t) ** 2
    n0 = int(steps) if steps is not None else max(64, math.ceil(_omega_max(w2, t0, t1) * (t1 - t0) / 0.8))
    if n0 < 2 or n0 > max_steps:
        raise ValueError(f"need 2 <= steps <= max_steps (the window needs ~{n0} steps; raise max_steps or shorten it)")

    def run(n, d):
        return _magnus_fermion_mp(p_of_t, ep, t0, t1, n, d)

    ec = _error_controlled(run, n0, int(dps), float(rtol), float(atol), int(max_steps), int(max_dps))
    end_err = sum(eps_ends) / 4
    nk, err2, relerr, resolved = _finish(ec["amp"], ec["serr"], ec["perr"], end_err, flag_rel, strict, "bogoliubov_fermion_mp")
    with mp.workdps(ec["dps"]):
        uni = abs(ec["amp_raw"] ** 2 + abs(ec["other"]) ** 2 - 1)
    return {"n": nk, "n_err": err2, "n_relerr": relerr, "resolved": resolved, "unitarity_error": uni,
            "vacuum_persistence_mode": 1 - nk, "step_err": ec["serr"], "precision_err": ec["perr"], "end_err": end_err,
            "eps_end": float(eps_end), "steps": ec["steps"], "dps": ec["dps"], "converged": ec["converged"]}


# ---------------------------------------------------------------- Part A: models and closed forms (mpmath)
def _ends_for(exponent: float, floor_ends: float = 25.0) -> float:
    """Window half-width in switching times so that e^{-2 ends} < sqrt(|beta|^2) * 1e-7, |beta|^2 ~ e^{-exponent}: the
    seeded end error eps/4 ~ 0.1 e^{-2 ends} (tanh, Sauter) is then ~1e-8 of |beta|, below the default rtol 1e-5
    (and it is part of the returned error estimate in any case)."""
    return max(floor_ends, exponent / 4.0 + 8.0)


def tanh_model_mp(k, m, A, B, rho, ends: float = None):
    """The Bernard-Duncan tanh model omega_k(t)^2 = k^2 + m^2 (A + B tanh(rho t)) as an mpmath callable.

    Quantity: (omega2, (t0, t1)): callable t -> omega_k(t)^2 (energy^2, mpmath) and a window +-ends/rho (1/energy);
        by default ends = max(25, pi min(w_in, w_out)/(2 rho) + 8), wide enough for |beta|^2 ~ exp(-2 pi w_min/rho).
    Valid when: rho > 0, m >= 0, k^2 + m^2 (A - |B|) > 0 (omega^2 > 0 everywhere)."""
    k, m, A, B, rho = _finite(k, "k"), _finite(m, "m"), _finite(A, "A"), _finite(B, "B"), _pos(rho, "rho")
    if m < 0:
        raise ValueError("m must be >= 0")
    if k * k + m * m * (A - abs(B)) <= 0:
        raise ValueError("need k^2 + m^2 (A - |B|) > 0")
    wmin = math.sqrt(k * k + m * m * (A - abs(B)))
    if ends is None:
        ends = _ends_for(2 * PI * wmin / rho)
    ends = _pos(ends, "ends")
    kk, mm, Am, Bm, rh = mp.mpf(k) ** 2, mp.mpf(m) ** 2, mp.mpf(A), mp.mpf(B), mp.mpf(rho)

    def omega2(t):
        return kk + mm * (Am + Bm * mp.tanh(rh * t))
    return omega2, (-ends / rho, ends / rho)


def tanh_model_beta2_mp(k, m, A, B, rho, dps: int = 50):
    """Exact |beta_k|^2 of the tanh model in mpmath (Birrell & Davies eq. 3.140b), at any precision.

    |beta|^2 = sinh^2(pi w_-/rho)/(sinh(pi w_in/rho) sinh(pi w_out/rho)), w_in/out = sqrt(k^2 + m^2 (A -/+ B)),
    w_- = (w_out - w_in)/2.
    Quantity: per-mode in-in mean particle number |beta_k|^2 (dimensionless, mpmath number, dps digits).
    Valid when: rho > 0, m >= 0, k^2 + m^2 (A - |B|) > 0."""
    k, m, A, B, rho = _finite(k, "k"), _finite(m, "m"), _finite(A, "A"), _finite(B, "B"), _pos(rho, "rho")
    if m < 0 or k * k + m * m * (A - abs(B)) <= 0:
        raise ValueError("need m >= 0 and k^2 + m^2 (A - |B|) > 0")
    with mp.workdps(dps):
        kk, mm, rh = mp.mpf(k) ** 2, mp.mpf(m) ** 2, mp.mpf(rho)
        wi, wo = mp.sqrt(kk + mm * (mp.mpf(A) - mp.mpf(B))), mp.sqrt(kk + mm * (mp.mpf(A) + mp.mpf(B)))
        wm = (wo - wi) / 2
        return +(mp.sinh(mp.pi * wm / rh) ** 2 / (mp.sinh(mp.pi * wi / rh) * mp.sinh(mp.pi * wo / rh)))


def sauter_ddp_exponent(k_par, k_perp, m, eE0, tau) -> float:
    """Leading exponent of Sauter-pulse pair creation per mode: 2K = pi tau (w_in + w_out) - 2 pi eE0 tau^2.

    Fukushima, Hayashi & Shigaki 2019 (arXiv:1907.12224) eq. 30 (DDP method). It is also the exponent of the exact
    Gavrilov-Gitman eq. 42 (spinor: n = e^{-2K}(1 + O(e^{-pi tau (2 eE0 tau - |w_out - w_in|)}))), and at k = 0 it
    equals dunne_schubert_exponent. (|w_out - w_in| < 2 eE0 tau always holds for eps_perp > 0.)
    Quantity: 2K (dimensionless) such that n_k ~ exp(-2K) for E(t) = E0 sech^2(t/tau) (both statistics; leading
        exponential only, prefactor 1 to relative O(1/K)).
    Valid when: eE0 > 0 (energy^2), tau > 0 (1/energy), m^2 + k_perp^2 > 0; semiclassical when 2K >> 1."""
    w_in, w_out, eE0, tau = qp._sauter_in_out(np.atleast_1d(k_par), np.atleast_1d(k_perp), _finite(m, "m"), eE0, tau)
    if float(np.min(_finite(m, "m") ** 2 + np.atleast_1d(k_perp) ** 2)) <= 0:
        raise ValueError("need m^2 + k_perp^2 > 0")
    return PI * tau * (float(w_in[0]) + float(w_out[0])) - 2 * PI * eE0 * tau * tau


def dunne_schubert_exponent(m, eE, omega) -> float:
    """Worldline-instanton action for E(t) = E sech^2(omega t): S0 = (pi m^2/eE) * 2/(1 + sqrt(1 + gamma^2)).

    Dunne & Schubert, PRD 72 (2005) 105004 (arXiv:hep-th/0507174) eq. 38 with n = 1, gamma = m omega/(eE) (eq. 29).
    Quantity: S0 (dimensionless), the exponent of the leading (k = 0) mode occupation n ~ exp(-S0) and of
        Im L_eff at leading exponential order (prefactors not included).
    Valid when: m, eE, omega > 0; semiclassical S0 >> 1 (and m >> omega for the instanton picture)."""
    m, eE, omega = _pos(m, "m"), _pos(eE, "eE"), _pos(omega, "omega")
    g = m * omega / eE
    return PI * m * m / eE * 2.0 / (1.0 + math.sqrt(1.0 + g * g))


def sauter_mp(k_par, k_perp, m, eE0, tau, ends: float = None):
    """Sauter pulse E(t) = E0 sech^2(t/tau) for one mode, as mpmath callables (gauge A_z = -E0 tau tanh(t/tau)).

    Quantity: (omega2, p_of_t, eps_perp, (t0, t1)): callables t -> omega_k(t)^2 = eps_perp^2 + p(t)^2 (energy^2) and
        t -> p(t) = k_par + eE0 tau tanh(t/tau) (energy), eps_perp = sqrt(m^2 + k_perp^2) (energy), and a window
        +-ends tau (1/energy), by default wide enough for n ~ exp(-sauter_ddp_exponent).
    Valid when: eE0 > 0 (energy^2), tau > 0 (1/energy), m^2 + k_perp^2 > 0."""
    kz, kp, m = _finite(k_par, "k_par"), _finite(k_perp, "k_perp"), _finite(m, "m")
    eE0, tau = _pos(eE0, "eE0"), _pos(tau, "tau")
    if m < 0 or m * m + kp * kp <= 0:
        raise ValueError("need m >= 0 and m^2 + k_perp^2 > 0")
    if ends is None:
        ends = _ends_for(sauter_ddp_exponent(kz, kp, m, eE0, tau))
    ends = _pos(ends, "ends")
    a, kzm, ta = mp.mpf(eE0) * mp.mpf(tau), mp.mpf(kz), mp.mpf(tau)
    ep = math.sqrt(m * m + kp * kp)
    e2 = mp.mpf(m) ** 2 + mp.mpf(kp) ** 2

    def p_of_t(t):
        return kzm + a * mp.tanh(t / ta)

    def omega2(t):
        return e2 + p_of_t(t) ** 2
    return omega2, p_of_t, ep, (-ends * tau, ends * tau)


def sauter_n_mp(k_par, k_perp, m, eE0, tau, fermion: bool, dps: int = 50):
    """Exact Sauter-pulse occupation in mpmath (Gavrilov & Gitman 1996 eqs. 42-43; Narozhny & Nikishov 1970).

    spinor (per spin): n = sinh[(pi tau/2)(2 eE0 tau + w_in - w_out)] sinh[(pi tau/2)(2 eE0 tau + w_out - w_in)]
                           / (sinh(pi tau w_in) sinh(pi tau w_out))
    scalar:            n = (cosh^2[pi sqrt((eE0 tau^2)^2 - 1/4)] + sinh^2[(pi tau/2)(w_out - w_in)])
                           / (sinh(pi tau w_in) sinh(pi tau w_out)),   w_in/out = sqrt(eps_perp^2 + (k_par -/+ eE0 tau)^2).
    Quantity: per-mode in-in mean number of particles in mode k (= antiparticles in -k = pairs in that mode;
        spinor: per spin state), dimensionless mpmath number.
    Valid when: homogeneous Sauter pulse, m^2 + k_perp^2 > 0, eE0 > 0 (energy^2), tau > 0 (1/energy)."""
    kz, kp, m = _finite(k_par, "k_par"), _finite(k_perp, "k_perp"), _finite(m, "m")
    eE0, tau = _pos(eE0, "eE0"), _pos(tau, "tau")
    if m < 0 or m * m + kp * kp <= 0:
        raise ValueError("need m >= 0 and m^2 + k_perp^2 > 0")
    with mp.workdps(dps):
        e2, a, ta = mp.mpf(m) ** 2 + mp.mpf(kp) ** 2, mp.mpf(eE0) * mp.mpf(tau), mp.mpf(tau)
        wi, wo = mp.sqrt(e2 + (mp.mpf(kz) - a) ** 2), mp.sqrt(e2 + (mp.mpf(kz) + a) ** 2)
        den = mp.sinh(mp.pi * ta * wi) * mp.sinh(mp.pi * ta * wo)
        if fermion:
            num = mp.sinh(mp.pi * ta / 2 * (2 * a + wi - wo)) * mp.sinh(mp.pi * ta / 2 * (2 * a + wo - wi))
        else:
            lam = mp.sqrt(mp.mpc((a * ta) ** 2 - mp.mpf(1) / 4))         # imaginary when eE0 tau^2 < 1/2
            num = mp.re(mp.cosh(mp.pi * lam) ** 2) + mp.sinh(mp.pi * ta / 2 * (wo - wi)) ** 2
        return +(num / den)


def poschl_teller_mp(omega0, V0, rho, ends: float = None):
    """omega(t)^2 = omega0^2 - V0 sech^2(rho t) (a dip for V0 > 0, a bump for V0 < 0) as an mpmath callable.

    Quantity: (omega2, (t0, t1)): callable t -> omega(t)^2 (energy^2, mpmath) and a window +-ends/rho (1/energy).
    Valid when: omega0 > 0, rho > 0, V0 < omega0^2 (omega^2 > 0 everywhere)."""
    w0, V0, rho = _pos(omega0, "omega0"), _finite(V0, "V0"), _pos(rho, "rho")
    if V0 >= w0 * w0:
        raise ValueError("need V0 < omega0^2 (omega^2 > 0 everywhere)")
    if ends is None:
        ends = _ends_for(2 * PI * (w0 - math.sqrt(max(V0, 0.0))) / rho)
    ends = _pos(ends, "ends")
    w02, v, rh = mp.mpf(w0) ** 2, mp.mpf(V0), mp.mpf(rho)

    def omega2(t):
        return w02 - v / mp.cosh(rh * t) ** 2
    return omega2, (-ends / rho, ends / rho)


def poschl_teller_beta2_mp(omega0, V0, rho, dps: int = 50):
    """Exact |beta|^2 for omega^2 = omega0^2 - V0 sech^2(rho t): cos^2(pi sqrt(1/4 - V0/rho^2)) / sinh^2(pi omega0/rho).

    From the Poeschl-Teller scattering amplitudes (Lenzi et al. 2022, arXiv:2212.03732, eqs. D11-D12, potential
    V0/cosh^2 = rho^2 lambda(1 - lambda)/cosh^2): |beta|^2 = |r/t|^2 = |sin(pi lambda)|^2/sinh^2(pi omega0/rho)
    (Gamma reflection formula), lambda = 1/2 + sqrt(1/4 - V0/rho^2); the time-dependent mode problem maps onto
    over-barrier scattering with |beta/alpha|^2 = |r|^2, 1/|alpha|^2 = |t|^2.
    Quantity: per-mode in-in mean particle number |beta|^2 (dimensionless, mpmath).
    Valid when: omega0 > 0, rho > 0, V0 < omega0^2."""
    w0, V0, rho = _pos(omega0, "omega0"), _finite(V0, "V0"), _pos(rho, "rho")
    if V0 >= w0 * w0:
        raise ValueError("need V0 < omega0^2")
    with mp.workdps(dps):
        s = mp.sqrt(mp.mpc(mp.mpf(1) / 4 - mp.mpf(V0) / mp.mpf(rho) ** 2))
        return +(abs(mp.cos(mp.pi * s)) ** 2 / mp.sinh(mp.pi * mp.mpf(w0) / mp.mpf(rho)) ** 2)


# ---------------------------------------------------------------- Part B: phase integral
_GL_CACHE = {}


def _gl_mp(n: int):
    """Gauss-Legendre nodes and weights on [-1, 1] at the current precision (Newton on P_n)."""
    key = (n, mp.mp.prec)
    if key not in _GL_CACHE:
        xs, ws = [], []
        for k in range(1, n + 1):
            x = mp.cos(mp.pi * (k - mp.mpf(1) / 4) / (n + mp.mpf(1) / 2))
            for _ in range(100):
                p0, p1 = mp.mpf(1), x
                for j in range(2, n + 1):
                    p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
                dp = n * (x * p1 - p0) / (x * x - 1)
                dx = p1 / dp
                x -= dx
                if abs(dx) < mp.eps * 4:
                    break
            p0, p1 = mp.mpf(1), x
            for j in range(2, n + 1):
                p0, p1 = p1, ((2 * j - 1) * x * p1 - (j - 1) * p0) / j
            dp = n * (x * p1 - p0) / (x * x - 1)
            xs.append(x)
            ws.append(2 / ((1 - x * x) * dp * dp))
        _GL_CACHE[key] = (xs, ws)
    return _GL_CACHE[key]


def _refine(f, seed, accept, center, radius, step):
    """Polish a zero of f from seed (extra starting points `step` away: mpmath's default offset is an absolute 0.25)
    and return it if accept(r); give up if the iteration leaves the disc |t - center| <= radius (a runaway iterate
    would make mpmath evaluate e.g. tanh at astronomically large arguments)."""
    def g(t):
        if not abs(t - center) <= radius:
            raise ValueError("iterate left the search region")
        return f(t)
    starts = {"secant": (seed, seed + step), "muller": (seed - step, seed, seed + 1j * step)}
    for solver in ("secant", "muller"):
        try:
            r = mp.findroot(g, starts[solver], solver=solver, tol=mp.eps ** 1.5, maxsteps=60, verify=False)
            if abs(r - center) <= radius and accept(r):
                return r
        except (ValueError, ZeroDivisionError, OverflowError):
            continue
    return None


def _scan(omega2, x_lo, x_hi, y_max, nx, ny):
    xs = [mp.mpf(x_lo) + (mp.mpf(x_hi) - mp.mpf(x_lo)) * i / (nx - 1) for i in range(nx)]
    ys = [mp.mpf(y_max) * (j + mp.mpf(1) / 2) / ny for j in range(ny)]
    vals = [[abs(omega2(mp.mpc(x, y))) for y in ys] for x in xs]
    lo, hi = [], []
    for i in range(nx):
        for j in range(ny):
            v = vals[i][j]
            nb = [vals[a][b] for a in (i - 1, i, i + 1) for b in (j - 1, j, j + 1)
                  if 0 <= a < nx and 0 <= b < ny and (a, b) != (i, j)]
            if all(v <= w for w in nb):
                lo.append(mp.mpc(xs[i], ys[j]))
            if all(v >= w for w in nb):
                hi.append(mp.mpc(xs[i], ys[j]))
    return lo, hi


def _phase_to(omega2, tc, n: int = 24, panels: int = 8):
    """int_{Re tc}^{tc} omega dt along the vertical segment, with t = tc + (Re tc - tc) s^2 (smooth at the zero)."""
    xc = mp.re(tc)
    d = mp.mpc(xc) - tc                           # = -i Im tc
    xg, wg = _gl_mp(n)
    nodes = []
    for k in range(panels):
        a, b = mp.mpf(k) / panels, mp.mpf(k + 1) / panels
        for x, w in zip(xg, wg):
            nodes.append(((a + b) / 2 + (b - a) / 2 * x, w * (b - a) / 2))
    nodes.sort(key=lambda q: -q[0])               # from s = 1 (real axis) down to s = 0 (turning point)
    prev = mp.sqrt(omega2(mp.mpc(xc)))
    total = mp.mpc(0)
    for s, w in nodes:
        om = mp.sqrt(omega2(tc + d * s * s))
        if abs(om - prev) > abs(om + prev):        # continue the branch from omega > 0 on the real axis
            om = -om
        prev = om
        total += om * (-2 * d * s) * w            # dt = 2 d s ds, integrated from s = 1 to 0
    return total


def _dd_sigma(K):
    """Dumlu-Dunne phase correction sigma(K) = (1/2)[(K/pi)(ln(K/pi) - 1) + Arg Gamma(1/2 - i K/pi)]."""
    y = K / mp.pi
    return (y * (mp.log(y) - 1) + mp.im(mp.loggamma(mp.mpf(1) / 2 - 1j * y))) / 2


def turning_points(omega2, x_range, y_max: float, grid=(64, 24), dps: int = 30) -> dict:
    """Complex turning points (zeros of omega^2) and poles of omega^2 in the box x_range x (0, y_max] of the upper half plane.

    omega2 must accept complex mpmath numbers (analytic continuation of omega(t)^2). Seeds are the local minima
    (zeros) and maxima (poles) of |omega^2| on a grid, refined with mpmath.findroot and de-duplicated.
    Quantity: dict with 'turning_points' (complex times t_c in 1/energy, sorted by K), 'K' (K = 2 Im int_{Re t_c}^{t_c}
        omega dt, dimensionless; |beta|^2 ~ exp(-2K) per isolated pair), 'poles' (complex times of poles of omega^2),
        and 'real_axis_min' (min omega^2 sampled on the real axis, energy^2).
    Valid when: omega^2 is analytic in the box except for poles, real and > 0 on the real axis inside x_range, and
        the grid resolves the box (spacing small compared with the distance between zeros/poles: refine `grid`)."""
    x_lo, x_hi = _finite(x_range[0], "x_range[0]"), _finite(x_range[1], "x_range[1]")
    y_max = _pos(y_max, "y_max")
    nx, ny = int(grid[0]), int(grid[1])
    if x_hi <= x_lo or nx < 8 or ny < 4:
        raise ValueError("need x_range[0] < x_range[1] and a grid of at least 8 x 4")
    with mp.workdps(int(dps)):
        rmin = min(_call_real(omega2, mp.mpf(x_lo) + (mp.mpf(x_hi) - mp.mpf(x_lo)) * j / 400, "omega2") for j in range(401))
        if rmin <= 0:
            raise ValueError("omega^2 <= 0 on the real axis: real turning points (tunnelling regime); the over-barrier "
                             "phase-integral formula does not apply")
        scale = max(abs(_call_real(omega2, mp.mpf(x_lo) + (mp.mpf(x_hi) - mp.mpf(x_lo)) * j / 64, "omega2"))
                    for j in range(65))                      # size of the terms in omega^2 (roundoff reference)
        center = mp.mpc((x_lo + x_hi) / 2, y_max / 2)
        radius = 2 * (x_hi - x_lo + y_max)
        step = min((x_hi - x_lo) / (nx - 1), y_max / ny) / 4
        lo, hi = _scan(omega2, x_lo, x_hi, y_max, nx, ny)
        tps, poles = [], []
        for s in lo:
            r = _refine(omega2, s, lambda z: abs(omega2(z)) <= scale * mp.mpf(10) ** (-mp.mp.dps // 3), center, radius, step)
            if r is not None and x_lo <= r.real <= x_hi and 0 < r.imag <= y_max * 1.0001 and \
                    not any(abs(r - q) < 1e-8 * (1 + abs(r)) for q in tps):
                tps.append(r)
        inv = lambda t: 1 / omega2(t)  # noqa: E731
        for s in hi:
            try:          # a pole: |omega^2| is huge there (evaluation near a pole limits the location to ~1e-11)
                r = _refine(inv, s, lambda z: abs(inv(z)) <= mp.mpf(10) ** -6 / scale, center, radius, step)
            except ZeroDivisionError:
                r = s
            if r is not None and x_lo <= r.real <= x_hi and 0 < r.imag <= y_max * 1.0001 and \
                    not any(abs(r - q) < 1e-8 * (1 + abs(r)) for q in poles):
                poles.append(r)
        Ks = [2 * mp.im(_phase_to(omega2, tc)) for tc in tps]
        order = sorted(range(len(tps)), key=lambda i: Ks[i])
        return {"turning_points": [tps[i] for i in order], "K": [Ks[i] for i in order], "poles": poles,
                "real_axis_min": rmin}


def phase_integral_beta2(omega2, x_range, y_max: float, statistics: str = "boson", grid=(64, 24), dps: int = 30,
                         window: float = 13.8) -> dict:
    """Phase-integral (complex-time WKB / Dykhne-Davis-Pechukas) |beta_k|^2 for one mode, with turning-point interference.

    One dominant pair: |beta|^2 = exp(-2K). Two pairs within `window` in K: Dumlu & Dunne 2010 eqs. 7 (scalar, +)
    and 8 (spinor, -): N = e^{-2K1} + e^{-2K2} +- 2 cos(2 alpha) e^{-K1-K2}, alpha = L - sigma(K1) - sigma(K2).
    statistics 'boson' (u'' + omega^2 u = 0) or 'fermion' (two-level i c' = (p sigma_z + eps sigma_x) c with
    omega^2 = eps^2 + p^2; per spin state).
    Quantity: per-mode IN-IN mean number |beta_k|^2 (bosons: particles in mode k; fermions: per spin state) as the
        leading exponential x prefactor (1 per simple turning-point pair, Dumlu-Dunne interference for two pairs),
        relative error O(1/K) (not estimated; exponentially small for tanh/Sauter spinor, exact for Landau-Zener);
        dict with 'beta2' (for `statistics`; 'beta2_boson' and 'beta2_fermion' give both), 'exponent' = 2 K_min, 'K' (dominant pairs), 'turning_points', 'alpha', 'L', 'sigma',
        'poles', 'subleading_K' (other turning points found), 'label'.
    Valid when: omega^2 analytic near the strip below the dominant turning points (poles allowed only farther from
        the real axis than them), real and > 0 on the real axis, simple turning points, at most two pairs within
        `window`, semiclassical (2K >> 1); the box must contain the dominant turning points."""
    if statistics not in ("boson", "fermion"):
        raise ValueError("statistics must be 'boson' or 'fermion'")
    window = _pos(window, "window")
    tp = turning_points(omega2, x_range, y_max, grid, dps)
    if not tp["turning_points"]:
        raise ValueError("no turning point found in the box: enlarge y_max / x_range or refine the grid")
    with mp.workdps(int(dps)):
        tps, Ks = tp["turning_points"], tp["K"]
        if any(K <= 0 for K in Ks):
            raise ValueError("a turning point has K <= 0: branch tracking failed (refine the box or the grid)")
        dom = [i for i in range(len(tps)) if Ks[i] <= Ks[0] + window]
        if len(dom) > 2:
            raise ValueError(f"{len(dom)} turning-point pairs within exp(-{window:g}) of the leading one: more than two "
                             "interfering pairs is not validated here; use bogoliubov_boson_mp/bogoliubov_fermion_mp")
        y_c = min(mp.im(tps[i]) for i in dom)
        for p in tp["poles"]:
            if mp.im(p) < y_c * (1 - mp.mpf(10) ** -8):
                raise ValueError(f"pole of omega^2 at {mp.nstr(p, 6)} lies closer to the real axis than the dominant turning "
                                 "point: the DDP contour is blocked (Fukushima et al. 2019); the turning-point formula "
                                 "does not apply")
        for i in dom:                              # nothing may sit on the vertical path below a dominant point
            for q in [tps[j] for j in range(len(tps)) if j != i] + tp["poles"]:
                if abs(mp.re(q) - mp.re(tps[i])) < 1e-6 * (1 + abs(tps[i])) and mp.im(q) < mp.im(tps[i]):
                    raise ValueError("another singularity lies on the vertical path to a dominant turning point")
            d = mp.diff(omega2, tps[i])
            if abs(d) < mp.mpf(10) ** (-dps // 3) * (1 + abs(omega2(mp.re(tps[i])))):
                raise ValueError("double (non-simple) turning point: prefactor 1 does not apply")
        out = {"turning_points": [tps[i] for i in dom], "K": [float(Ks[i]) for i in dom], "poles": tp["poles"],
               "subleading_K": [float(Ks[i]) for i in range(len(tps)) if i not in dom], "exponent": float(2 * Ks[0]),
               "alpha": None, "L": None, "sigma": None, "statistics": statistics}
        if len(dom) == 1:
            out["beta2"] = out["beta2_boson"] = out["beta2_fermion"] = mp.exp(-2 * Ks[0])
            out["label"] = "leading exponential x prefactor (single simple turning-point pair), relative error O(1/K)"
            return out
        i1, i2 = sorted(dom, key=lambda i: mp.re(tps[i]))
        t1, t2 = tps[i1], tps[i2]
        K1, K2 = Ks[i1], Ks[i2]
        real_part = mp.quad(lambda x: mp.sqrt(omega2(x)), mp.linspace(mp.re(t1), mp.re(t2), 9))
        L = abs(real_part + mp.re(_phase_to(omega2, t2)) - mp.re(_phase_to(omega2, t1)))
        s1, s2 = _dd_sigma(K1), _dd_sigma(K2)
        alpha = L - s1 - s2
        incoherent, cross = mp.exp(-2 * K1) + mp.exp(-2 * K2), 2 * mp.cos(2 * alpha) * mp.exp(-K1 - K2)
        out["beta2_boson"], out["beta2_fermion"] = incoherent + cross, incoherent - cross
        out["beta2"] = out["beta2_" + statistics]
        out.update({"alpha": float(alpha), "L": float(L), "sigma": (float(s1), float(s2)), "K": [float(K1), float(K2)],
                    "turning_points": [t1, t2],
                    "label": "leading exponential x prefactor with two-pair interference (Dumlu-Dunne eq. 7/8), "
                             "relative error O(1/K) of the envelope"})
        return out


# ---------------------------------------------------------------- Part C: second-order Born
_PANEL = {}


def _panel_rule(n: int = 16):
    """Gauss-Legendre nodes/weights on [-1, 1] and the cumulative-integration matrix S[i, k] = int_{-1}^{x_i} l_k."""
    if n not in _PANEL:
        from numpy.polynomial import legendre as leg
        x, w = leg.leggauss(n)
        V = leg.legvander(x, n - 1)
        C = np.empty((n, n))
        for j in range(n):
            c = np.zeros(n)
            c[j] = 1.0
            C[:, j] = leg.legval(x, leg.legint(c, lbnd=-1))
        _PANEL[n] = (x, w, C @ np.linalg.inv(V))
    return _PANEL[n]


def _time_grid(t0, t1, panels, n=16):
    x, w, S = _panel_rule(n)
    edges = np.linspace(t0, t1, panels + 1)
    h = 0.5 * (edges[1:] - edges[:-1])
    t = 0.5 * (edges[1:] + edges[:-1])[:, None] + h[:, None] * x[None, :]
    return t, h[:, None] * w[None, :], S, h


def _cumint(f, wt, S, h):
    """int_{t0}^{t_node} f for f of shape (..., panels, n) on the Gauss grid (spectrally accurate)."""
    inner = np.einsum("ik,...pk->...pi", S, f) * h[:, None]
    tot = np.sum(f * wt, axis=-1)
    return (np.cumsum(tot, axis=-1) - tot)[..., None] + inner


def _born_setup(f_of_t, w0, t0, t1, panels, name):
    t0, t1 = _window(t0, t1)
    w0 = np.atleast_1d(np.asarray(w0, dtype=float))
    if not np.all(np.isfinite(w0)) or np.any(w0 <= 0):
        raise ValueError("omega0 must be finite and > 0")
    if panels is None:
        panels = int(max(16, math.ceil(2.0 * float(w0.max()) * (t1 - t0) / 6.0)))
    if panels < 2:
        raise ValueError("need panels >= 2")
    t, wt, S, h = _time_grid(t0, t1, panels)
    f = np.asarray(f_of_t(t), dtype=float)
    if f.shape != t.shape or not np.all(np.isfinite(f)):
        raise ValueError(f"{name} must return finite values with the shape of its (array) argument")
    fmax = float(np.max(np.abs(f)))
    ends = max(abs(float(np.asarray(f_of_t(np.array([t0])), dtype=float)[0])),
               abs(float(np.asarray(f_of_t(np.array([t1])), dtype=float)[0])))
    if fmax > 0 and ends > 1e-8 * fmax:
        raise ValueError(f"{name} must switch off at both window ends (|end value|/max = {ends / fmax:.2g} > 1e-8)")
    return w0, t, wt, S, h, f


def born2_scalar_mode(V_of_t, omega0, t0: float, t1: float, panels: int = None) -> dict:
    """First- and second-order Born (Dyson) Bogoliubov coefficient for omega_k(t)^2 = omega0^2 + V(t), V -> 0 at the ends.

    V_of_t(t_array) returns V(t) (energy^2, numpy); omega0 (energy) may be an array of modes (omega0^2 = k^2 + m^2).
    Quantity: dict with per-mode complex 'b1' (O(V)) and 'b2' (O(V^2)) terms of beta_k, 'beta2_born1' = |b1|^2 (the
        in-in mean particle number in mode k to O(V^2), error O(V^3)), 'beta2_born2' = |b1|^2 + 2 Re(b1* b2) (to O(V^3),
        error O(V^4), i.e. relative O(V^2)), and 'lam' = int |V| dt/(2 omega0) (expansion parameter; the next term is
        ~lam^2 relative); dimensionless.
    Valid when: V real, V -> 0 at both ends of [t0, t1] (|V(end)| <= 1e-8 max|V|), lam < 1 (else refused; Born is
        meaningful for lam << 1), omega0 > 0; double precision: |b1| above ~1e-14 lam."""
    w0, t, wt, S, h, V = _born_setup(V_of_t, omega0, t0, t1, panels, "V_of_t")
    lam = float(np.sum(wt * np.abs(V))) / (2 * w0)
    if np.any(lam >= 1):
        raise ValueError(f"expansion parameter int|V|dt/(2 omega0) = {lam.max():.3g} >= 1: the Born series is not "
                         "applicable; use qp.bogoliubov_boson or bogoliubov_boson_mp")
    ph = np.exp(-2j * w0[:, None, None] * t[None])
    F = _cumint(V, wt, S, h)[None]
    G = _cumint(V[None] * ph, wt, S, h)
    b1 = 1j / (2 * w0) * np.sum(wt[None] * V[None] * ph, axis=(1, 2))
    b2 = 1.0 / (2 * w0) ** 2 * np.sum(wt[None] * V[None] * (ph * F - G), axis=(1, 2))
    B1 = np.abs(b1) ** 2
    return {"b1": b1, "b2": b2, "beta2_born1": B1, "beta2_born2": B1 + 2 * np.real(np.conj(b1) * b2), "lam": lam}


def born2_scalar_number_density(V_of_t, t0: float, t1: float, m: float, kmax: float, g: float = 1.0, n: int = 64,
                                kmin: float = 0.0, panels: int = None) -> dict:
    """Born-1 and Born-2 particle number per unit volume for a homogeneous scalar vertex omega_k^2 = k^2 + m^2 + V(t).

    n_X = g/(2 pi^2) int k^2 |beta_k|^2_X dk by Gauss-Legendre with n nodes (as qp.number_density_isotropic).
    Quantity: dict with 'particles_per_volume_born1' (to O(V^2), error O(V^3)) and 'particles_per_volume_born2'
        (to O(V^3), error O(V^4)): mean number of PARTICLES per unit volume (energy^3), in-in, summed over g internal
        states; for a REAL field pairs = particles/2, for a complex field particles = antiparticles = pairs.
        Also 'lam_max' (largest expansion parameter over the k nodes).
    Valid when: as born2_scalar_mode for every k in [kmin, kmax], |beta_k|^2 negligible above kmax, m >= 0, n >= 4."""
    m = _finite(m, "m")
    if m < 0:
        raise ValueError("m must be >= 0")
    kmin, kmax = _finite(kmin, "kmin"), _finite(kmax, "kmax")
    if not 0 <= kmin < kmax or int(n) < 4:
        raise ValueError("need 0 <= kmin < kmax and n >= 4")
    k, wk = qp._gauss_legendre(kmin, kmax, int(n))
    r = born2_scalar_mode(V_of_t, np.sqrt(k * k + m * m), t0, t1, panels)
    n1 = float(g / (2 * PI * PI) * np.sum(wk * k * k * r["beta2_born1"]))
    n2 = float(g / (2 * PI * PI) * np.sum(wk * k * k * r["beta2_born2"]))
    return {"particles_per_volume_born1": n1, "particles_per_volume_born2": n2, "lam_max": float(np.max(r["lam"]))}


def born2_fermion_efield_mode(eA_of_t, k_par, k_perp, m: float, t0: float, t1: float, panels: int = None) -> dict:
    """First- and second-order Born occupation for spinor QED in a homogeneous E(t) = -A'(t) with A -> 0 at both ends.

    Two-level reduction per spin: H = (k_par - eA(t)) sigma_z + eps_perp sigma_x = H0 + W, W = -eA sigma_z (module
    docstring, Part C). eA_of_t(t_array) returns eA(t) (energy, numpy); k_par may be an array of modes.
    Quantity: dict with per-mode complex 'c1', 'c2', 'n_born1' = |c1|^2 (per-spin in-in mean number of electrons in
        mode k = pairs in that mode, to O(e^2), error O(e^3)), 'n_born2' = |c1|^2 + 2 Re(c1* c2) (to O(e^3), error
        O(e^4)), and 'lam' = int |eA| dt (expansion parameter); dimensionless.
    Valid when: A -> 0 at both ends (zero net momentum transfer, int E dt = 0; else the in and out bases differ),
        lam < 1 (else refused), m^2 + k_perp^2 > 0."""
    kz = np.atleast_1d(np.asarray(k_par, dtype=float))
    m, kp = _finite(m, "m"), _finite(k_perp, "k_perp")
    if m < 0 or m * m + kp * kp <= 0:
        raise ValueError("need m >= 0 and m^2 + k_perp^2 > 0")
    ep = math.sqrt(m * m + kp * kp)
    w0 = np.sqrt(kz * kz + ep * ep)
    w0, t, wt, S, h, A = _born_setup(eA_of_t, w0, t0, t1, panels, "eA_of_t")
    lam = float(np.sum(wt * np.abs(A)))
    if lam >= 1:
        raise ValueError(f"expansion parameter int|eA|dt = {lam:.3g} >= 1: Born is not applicable; use "
                         "qp.bogoliubov_fermion_efield or bogoliubov_fermion_mp")
    th = np.arctan2(ep, kz)
    sin_t, cos_t = np.sin(th)[:, None, None], np.cos(th)[:, None, None]
    Wpm = A[None] * sin_t                                   # W_{+-} = eA sin theta0
    Wpp = -A[None] * cos_t                                  # W_{++} = -eA cos theta0 = -W_{--}
    ph = np.exp(2j * w0[:, None, None] * t[None])
    c1 = -1j * np.sum(wt[None] * Wpm * ph, axis=(1, 2))
    inner_pm = _cumint(Wpm * ph, wt, S, h)
    inner_mm = _cumint(-Wpp, wt, S, h)
    c2 = -np.sum(wt[None] * (Wpp * inner_pm + Wpm * ph * inner_mm), axis=(1, 2))
    n1 = np.abs(c1) ** 2
    return {"c1": c1, "c2": c2, "n_born1": n1, "n_born2": n1 + 2 * np.real(np.conj(c1) * c2), "lam": lam}


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, published formulas and qft_production's independent solvers. True if all pass."""
    import time
    results, start = [], time.time()

    def check(name, got, want, tol, rel=False):
        got, want = float(got), float(want)
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  [{time.time() - start:5.1f} s] {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})", flush=True)

    # ---- A. High-precision mode solvers, far below qp's floor (~1e-28).
    # A1. tanh model at rho = 0.07 (k = 0.5, m = 1, A = 2, B = 1): exact |beta|^2 = 2.6097e-44.
    #     Birrell & Davies sec. 3.4 via arXiv:2204.02786 (ACCESS: full-text), eq. 3.133 "a2(η) =A +B tanh(ρη)",
    #     eq. 3.134 "ω1≡ ∑ k2 +m2(A−B) ω2≡ ∑ k2 +m2(A +B)", eq. 3.135 "ω±≡1 2 ( ω2±ω1 )" and eq. 3.140b
    #     "|βk|2 = sinh2(πω−/ρ) sinh(πω1/ρ) sinh(πω2/ρ)" (PDF extraction drops the square roots and the fraction bars;
    #     reading: w1,2 = sqrt(k^2 + m^2 (A -/+ B)), w-+ = (w2 -+ w1)/2, |beta|^2 = sinh^2(pi w-/rho)/(sinh(pi w1/rho) sinh(pi w2/rho))).
    #     Tolerance 1e-4 relative = 5x the solver's default budget (rtol 1e-5 on |beta| -> 2e-5 on |beta|^2); the sharper
    #     statement is the second check: the solver's OWN error estimate must bound the true error.
    w2f, (t0, t1) = tanh_model_mp(0.5, 1.0, 2.0, 1.0, 0.07)
    r = bogoliubov_boson_mp(w2f, t0, t1)
    ref = tanh_model_beta2_mp(0.5, 1.0, 2.0, 1.0, 0.07)
    check(f"tanh rho=0.07: mp solver vs eq. 3.140b (exact {mp.nstr(ref, 6)}, dps {r['dps']}, steps {r['steps']})",
          r["beta2"] / ref, 1.0, 1e-4)
    check(f"   its error estimate ({r['beta2_relerr']:.1e} rel.) bounds the true error ({float(abs(r['beta2'] / ref - 1)):.1e}); resolved",
          float(abs(r["beta2"] - ref) <= r["beta2_err"] and r["resolved"]), 1.0, 0)
    check("same mode: qp's double-precision solver cannot resolve it (flagged unresolved)",
          float(not qp.bogoliubov_boson(lambda t: np.array([2.25 + np.tanh(0.07 * t)]), t0, t1)["resolved"][0]), 1.0, 0)
    #     qp's closed form (double precision, log-sinh) agrees with this mpmath closed form at 1e-44:
    check("qp.tanh_model_beta2 (double) = tanh_model_beta2_mp at rho = 0.07", float(qp.tanh_model_beta2([0.5], 1, 2, 1, 0.07)[0]),
          float(ref), 1e-10, rel=True)
    # A2. ...and smaller: k = 2, rho = 0.12 gives exp(-2 pi sqrt5/0.12) ~ 1e-51 (dps must double past 30).
    w2f, (t0, t1) = tanh_model_mp(2.0, 1.0, 2.0, 1.0, 0.12)
    r = bogoliubov_boson_mp(w2f, t0, t1)
    ref = tanh_model_beta2_mp(2.0, 1.0, 2.0, 1.0, 0.12)
    check(f"tanh k=2, rho=0.12: mp solver vs eq. 3.140b (exact {mp.nstr(ref, 6)}, dps {r['dps']}), tol as A1",
          r["beta2"] / ref, 1.0, 1e-4)
    check(f"   error estimate ({r['beta2_relerr']:.1e}) bounds the true error ({float(abs(r['beta2'] / ref - 1)):.1e})",
          float(abs(r["beta2"] - ref) <= r["beta2_err"]), 1.0, 0)
    # A3. Sauter pulse, spinor and scalar, n ~ 1e-38: Gavrilov & Gitman 1996 (arXiv:hep-th/9603152, ACCESS: full-text)
    #     eq. 42 "Np,r = sinh [ πα 2 (2eEα +ω− −ω+) ] sinh [ πα 2 (2eEα +ω+ −ω−) ] sinh(παω+) sinh(παω−)" and eq. 43
    #     "Np,r = cosh2 [ π √ (eEα 2)2 − 1 4 ] + sinh2 [ πα 2 (ω+ −ω−) ] sinh(παω+) sinh(παω−)" (alpha = tau; the
    #     fraction bars are lost in extraction: the products of sinh(pi alpha w+-) are the denominators).
    #     m = 1, eE0 = 0.025, tau = 20 (eE0 tau^2 = 10, gamma = 2), k_par = 0.1, k_perp = 0.2. Tolerance as A1.
    args = (0.1, 0.2, 1.0, 0.025, 20.0)
    om2, pf, ep, (t0, t1) = sauter_mp(*args)
    rf = bogoliubov_fermion_mp(pf, ep, t0, t1)
    nf = sauter_n_mp(*args, True)
    check(f"Sauter spinor (n = {mp.nstr(nf, 5)}): fermion mp solver vs GG eq. 42", rf["n"] / nf, 1.0, 1e-4)
    rb = bogoliubov_boson_mp(om2, t0, t1)
    ns = sauter_n_mp(*args, False)
    check(f"Sauter scalar (n = {mp.nstr(ns, 5)}): boson mp solver vs GG eq. 43", rb["beta2"] / ns, 1.0, 1e-4)
    check("   both error estimates bound the true errors",
          float(abs(rf["n"] - nf) <= rf["n_err"] and abs(rb["beta2"] - ns) <= rb["beta2_err"]), 1.0, 0)
    check("mp closed forms = qp's double-precision GG forms (spinor, scalar), rel 1e-9 (log-sinh roundoff)",
          max(abs(float(qp.sauter_n_spinor(*args)) / float(nf) - 1), abs(float(qp.sauter_n_scalar(*args)) / float(ns) - 1)),
          0.0, 1e-9)
    # A4. Poeschl-Teller omega^2 = w0^2 - V0 sech^2(rho t). Closed form from Lenzi et al. 2022 (arXiv:2212.03732, ACCESS:
    #     full-text) eq. 115 "V (x) = V0 cosh2 (αx) = α2λ(1−λ) cosh2(αx)", eq. D11 "t(k) = Γ(λ−ik)Γ(1−λ−ik) Γ(1−ik)Γ(−ik)" and
    #     eq. D12 "r(k) = Γ(ik)Γ(λ−ik)Γ(1−λ−ik) Γ(−ik)Γ(1−λ)Γ(λ)" (alpha = 1; fraction bars lost, numerators first), reduced
    #     with Gamma(z)Gamma(1-z) = pi/sin(pi z) to |r/t|^2 = cos^2(pi sqrt(1/4 - V0/rho^2))/sinh^2(pi w0/rho).
    #     (i) It vanishes for the reflectionless bumps V0 = -p(p+1) rho^2: Ahmadiniaz et al. 2022 (arXiv:2205.15946, ACCESS:
    #     full-text) eq. 30 "ω2 (p)(t) =ω2 0 + p(p + 1)ω2 0 cosh2(ω0t)" [reading: w0^2 + p(p+1) w0^2/cosh^2(w0 t)], "particle
    #     production is absent for integer values of p where the Pöschl-Teller potential becomes reflectionless".
    for p in (1, 2):
        check(f"closed form = 0 for the reflectionless p = {p} (Ahmadiniaz et al.): below 1e-40",
              float(poschl_teller_beta2_mp(1.0, -p * (p + 1), 1.0) < mp.mpf(10) ** -40), 1.0, 0)
    #     (ii) qp's double-precision solver (independent) agrees with the closed form at moderate values (dip and bump).
    pv = np.array([0.5, 0.9, -0.75, -2.0])
    rq = qp.bogoliubov_boson(lambda t: 1.0 - pv / np.cosh(0.5 * t) ** 2, -50.0, 50.0, rtol=1e-7)["beta2"]
    check("closed form vs qp.bogoliubov_boson for V0 = 0.5, 0.9, -0.75, -2 (rho = 0.5), max rel. (qp rtol 1e-7)",
          max(abs(rq[i] / float(poschl_teller_beta2_mp(1.0, v, 0.5)) - 1) for i, v in enumerate(pv)), 0.0, 1e-6)
    #     (iii) a deep dip far below qp's floor: V0 = 0.1, rho = 0.05, |beta|^2 ~ 1e-37. Tolerance as A1.
    w2f, (t0, t1) = poschl_teller_mp(1.0, 0.1, 0.05)
    ref = poschl_teller_beta2_mp(1.0, 0.1, 0.05)
    check(f"Poeschl-Teller dip V0 = 0.1, rho = 0.05: mp solver vs closed form (exact {mp.nstr(ref, 6)})",
          bogoliubov_boson_mp(w2f, t0, t1)["beta2"] / ref, 1.0, 1e-4)

    # ---- B. Phase integral.
    # B1. Landau-Zener / constant field, omega^2 = eps^2 + (eE t)^2: exact n = exp(-pi eps^2/eE) for both statistics.
    #     Kim, Lee & Yoon 2008 (arXiv:0807.2696, ACCESS: full-text), after eqs. 46 and 51: "Nk = e− π (m2+k2 ⊥ )/ (qE)";
    #     Fukushima et al. 2019 (arXiv:1907.12224, ACCESS: full-text) eq. 10 "P≃ e−2Im∆(tc)" and eq. 23 "−2Im ∆(tc) =−4Im
    #     ∫ tc 0 dt √ (pz + eEt)2 + m2 ⊥ = ... =−πm2 ⊥ eE" [reading: = -pi m_perp^2/(eE)]. Exact here, so tol 1e-12
    #     (quadrature at 30 digits; float conversion).
    eE, ep = 0.3, 1.2
    pl = phase_integral_beta2(lambda t: mp.mpf(ep) ** 2 + (mp.mpf(eE) * t) ** 2, (-10, 10), 10)
    check("Landau-Zener: phase integral = exp(-pi eps^2/eE) (KLY; Fukushima eq. 23)", pl["beta2"] / mp.exp(-mp.pi * ep * ep / eE),
          1.0, 1e-12)
    # B2. tanh model, exponent and prefactor: 2K = 2 pi w_in/rho exactly (the closed form's small-rho limit), and
    #     exact/PI - 1 = O(exp(-2 pi w_-/rho)) only (measured 2.7e-2, 4.3e-5 at rho = 0.5, 0.2); tolerance 3 x that bound.
    for rho in (0.5, 0.2, 0.07):
        w2f, _ = tanh_model_mp(0.5, 1.0, 2.0, 1.0, rho)
        pt = phase_integral_beta2(w2f, (-3 / rho, 3 / rho), 2 / rho)
        wi, wo = math.sqrt(1.25), math.sqrt(3.25)
        check(f"tanh rho = {rho}: phase-integral exponent 2K = 2 pi w_in/rho", pt["exponent"], 2 * PI * wi / rho, 1e-12, rel=True)
        check(f"tanh rho = {rho}: closed form / phase integral - 1 <= 3 exp(-2 pi w_-/rho)",
              abs(float(tanh_model_beta2_mp(0.5, 1, 2, 1, rho) / pt["beta2"]) - 1), 0.0, 3 * math.exp(-PI * (wo - wi) / rho))
    # B3. Sauter: exponent = Fukushima et al. eq. 30 "P≃ e−Am2/(eE), with A = π γm [√(m γ + pz )2 + m2 ⊥ + √(m γ− pz )2
    #     + m2 ⊥− 2m γ ]" [reading: A = pi/(gamma m) [sqrt((m/gamma + p_z)^2 + m_perp^2) + sqrt((m/gamma - p_z)^2 + m_perp^2)
    #     - 2m/gamma], i.e. A m^2/eE = pi tau (w_in + w_out) - 2 pi eE0 tau^2 = sauter_ddp_exponent]; prefactor vs GG eqs.
    #     42/43: spinor exact/PI - 1 = O(exp(-pi tau (2 eE0 tau - |w_out - w_in|))) < 1e-50 here (tol 1e-12: float conversion);
    #     scalar exact/PI = exp(-c - pi/(64 a^3) + ...), a = eE0 tau^2, c = pi/(4a) (from GG eq. 43: 2 pi (sqrt(a^2 - 1/4) - a)),
    #     so |exact/PI - exp(-c)| ~ 1.6 c^3: tol c^2.
    for kz, kp, eE0, tau in ((0.0, 0.3, 0.2, 10.0), (0.5, 0.2, 0.1, 20.0)):
        om2, _, _, _ = sauter_mp(kz, kp, 1.0, eE0, tau)
        pt = phase_integral_beta2(om2, (-3 * tau, 3 * tau), 1.6 * tau)
        check(f"Sauter k=({kz},{kp}), eE0 tau^2 = {eE0 * tau * tau:g}: 2K = Fukushima eq. 30", pt["exponent"],
              sauter_ddp_exponent(kz, kp, 1.0, eE0, tau), 1e-12, rel=True)
        check("   spinor: GG eq. 42 / phase integral = 1", sauter_n_mp(kz, kp, 1.0, eE0, tau, True) / pt["beta2"], 1.0, 1e-12)
        c = PI / (4 * eE0 * tau * tau)
        check(f"   scalar: GG eq. 43 / phase integral = exp(-pi/(4 eE0 tau^2)) = {math.exp(-c):.5f}",
              sauter_n_mp(kz, kp, 1.0, eE0, tau, False) / pt["beta2"], math.exp(-c), c * c)
    # B3'. Poeschl-Teller dip (closed form of A4, Lenzi et al.): exponent 2K = 2 pi (w0 - sqrt V0)/rho, and the prefactor is
    #     NOT 1 at finite rho: cosh^2(pi sqrt(V0/rho^2 - 1/4))/sinh^2(pi w0/rho) -> exp(-2K - c), c = pi rho/(4 sqrt V0) (the double
    #     pole of sech^2, as for the Sauter scalar), with next term O(c^3): tol c^2. w0 = 1, V0 = 0.5, rho = 0.05.
    w2f, _ = poschl_teller_mp(1.0, 0.5, 0.05)
    pt = phase_integral_beta2(w2f, (-40.0, 40.0), 34.0)
    check("Poeschl-Teller dip: phase-integral exponent 2K = 2 pi (w0 - sqrt V0)/rho", pt["exponent"],
          2 * PI * (1 - math.sqrt(0.5)) / 0.05, 1e-12, rel=True)
    c = PI * 0.05 / (4 * math.sqrt(0.5))
    check(f"   exact / phase integral = exp(-pi rho/(4 sqrt V0)) = {math.exp(-c):.5f} (relative error O(1/K))",
          poschl_teller_beta2_mp(1.0, 0.5, 0.05) / pt["beta2"], math.exp(-c), c * c)
    # B4. Dunne & Schubert 2005 (arXiv:hep-th/0507174, ACCESS: full-text) eq. 38 for E(t) = E sech2(ωt):
    #     "S0 = ... = n m2π eE ( 2 1 + √1 + γ 2 )" [reading: n (m^2 pi/eE) * 2/(1 + sqrt(1 + gamma^2))], "γ = mω eE
    #     deﬁned in (29)" [gamma = m omega/(eE)]. The k = 0 phase-integral exponent must equal it for every gamma
    #     (an identity; tol 1e-12 from quadrature).
    for gam in (0.1, 1.0, 5.0):
        eE0 = 0.2
        tau = 1.0 / (gam * eE0)                    # omega = 1/tau, gamma = m omega/eE with m = 1
        om2, _, _, _ = sauter_mp(0.0, 0.0, 1.0, eE0, tau)
        pt = phase_integral_beta2(om2, (-3 * tau, 3 * tau), 1.6 * tau)
        check(f"k = 0 phase-integral exponent = Dunne-Schubert S0 at gamma = {gam}", pt["exponent"],
              dunne_schubert_exponent(1.0, eE0, 1.0 / tau), 1e-12, rel=True)
    # B5. Two interfering pairs: alternating double Sauter pulse, p(t) = k + eE tau [tanh((t-T)/tau) - tanh((t+T)/tau)],
    #     k = eE tau (the momentum crosses zero near t = -T and t = +T). Dumlu & Dunne 2010 (arXiv:1004.2509, ACCESS:
    #     full-text) eq. 7 "Nscalar ≈ e− 2K1 + e− 2K2 + 2 cos(2α) e− K1− K2", "α = L − σ(K1) − σ(K2) L = ⏐⏐⏐⏐Re ( ∫ t3 t2
    #     Q dt ) ⏐⏐⏐⏐ σ(K) = 1 2 [ K π ( ln ( K π ) − 1 ) + Arg Γ ( 1 2 − i K π )]", eq. 8 "Nspinor ≈ e− 2K1 + e− 2K2 − 2
    #     cos(2α) e− K1− K2" ("The only change is the sign of the interference term"). Reference: qp's double-precision
    #     solvers (independent code), 4 values of T across one fringe. |exact - PI| / envelope (4 e^{-2K}): tol 5% scalar
    #     (O(1/K) prefactor, measured 2.5% at K = 14.8, cf. B3's exp(-pi/(4 eE tau^2)) = 0.98), 1.5% spinor (measured 0.6%).
    eE, tau = 0.1, 20.0
    k = eE * tau
    Ts = 3 * tau + np.arange(4) * (PI / (2 * math.sqrt(1 + k * k))) / 4
    pnp = lambda t: k + eE * tau * (np.tanh((t - Ts) / tau) - np.tanh((t + Ts) / tau))  # noqa: E731
    t0, t1 = -(Ts.max() + 20 * tau), Ts.max() + 20 * tau       # field off to e^-40; qp rtol 1e-3 << the 1.5-5% tolerances
    eb = qp.bogoliubov_boson(lambda t: 1.0 + pnp(t) ** 2, t0, t1, rtol=1e-3)["beta2"]
    ef = qp.bogoliubov_fermion_efield(pnp, np.ones_like(Ts), t0, t1, rtol=1e-3)["n"]
    dev_s, dev_f, anti = [], [], []
    for i, T in enumerate(Ts):
        Tm = mp.mpf(T)
        w2f = lambda t, Tm=Tm: 1 + (k + eE * tau * (mp.tanh((t - Tm) / tau) - mp.tanh((t + Tm) / tau))) ** 2  # noqa: E731
        ps = phase_integral_beta2(w2f, (-T - 3 * tau, T + 3 * tau), 1.6 * tau, "boson", grid=(40, 10), dps=20)
        env = 4 * math.exp(-2 * ps["K"][0])
        dev_s.append(abs(eb[i] - float(ps["beta2_boson"])) / env)
        dev_f.append(abs(ef[i] - float(ps["beta2_fermion"])) / env)
        anti.append((eb[i] - ef[i]) * math.cos(2 * ps["alpha"]))
    check(f"double Sauter, scalar: max |qp - Dumlu-Dunne eq. 7| / envelope over 4 T (K = {ps['K'][0]:.2f})", max(dev_s), 0.0, 0.05)
    check("double Sauter, spinor: max |qp - Dumlu-Dunne eq. 8| / envelope", max(dev_f), 0.0, 0.015)
    check("scalar and spinor fringes are in antiphase, as cos(2 alpha) predicts (sign of (N_sc - N_sp) cos 2alpha > 0)",
          float(all(a > 0 for a in anti)), 1.0, 0)
    # B6. Refusals: a pole of omega^2 below the turning point blocks the DDP contour (Fukushima et al. eq. 9 context:
    #     "The second assumption holds if there are no poles between the real axis and this contour"); real turning points.
    try:
        phase_integral_beta2(lambda t: 1 + 3 / (t * t + mp.mpf(1) / 4), (-5, 5), 4)
        refused = 0.0
    except ValueError:
        refused = 1.0
    check("omega^2 = 1 + 3/(t^2 + 1/4): pole at t = i/2 below the turning point t = 1.80i: refused", refused, 1.0, 0)

    # ---- C. Second-order Born.
    # C1. Exact second-order coefficient for V = eps sech^2(rho t): the Lenzi et al. closed form quoted in A4 with V0 = -eps,
    #     |beta|^2 = cos^2(pi sqrt(1/4 + x))/sinh^2(pi w0/rho), x = eps/rho^2, expands as pi^2 x^2 (1 - 2x + O(x^2))/sinh^2(pi w0/rho):
    #     Born-1 = pi^2 x^2/sinh^2 and 2 Re(b1* b2) = -2x Born-1, for every w0 (the omega0-dependence factorises).
    #     Tolerance 1e-10: the Gauss-Legendre quadrature is converged to ~1e-13.
    rho = 0.7
    for eps in (0.05, -0.05):
        w0 = np.array([0.5, 1.0, 1.7])
        rb2 = born2_scalar_mode(lambda t, eps=eps: eps / np.cosh(rho * t) ** 2, w0, -40 / rho, 40 / rho)
        x = eps / rho ** 2
        check(f"sech^2 (eps = {eps}): Born-1 = pi^2 x^2/sinh^2(pi w0/rho), max rel. over 3 w0",
              np.max(np.abs(rb2["beta2_born1"] / (PI * PI * x * x / np.sinh(PI * w0 / rho) ** 2) - 1)), 0.0, 1e-10)
        check(f"sech^2 (eps = {eps}): 2 Re(b1* b2)/Born-1 = -2 eps/rho^2 (exact second order), max rel.",
              np.max(np.abs((rb2["beta2_born2"] - rb2["beta2_born1"]) / rb2["beta2_born1"] / (-2 * x) - 1)), 0.0, 1e-10)
    # C2. Against qp's exact mode solver (independent) for a Gaussian V = eps exp(-t^2/2tau^2), tau = 0.3, m = 1 (window
    #     +-8 tau: V(end) = e^-32 max V; |V~(Omega)|^2 ~ e^{-Omega^2 tau^2} < 1e-22 beyond Omega = 24): the
    #     residual of Born-1 scales as eps and of Born-2 as eps^2 (ratio for eps doubling: 2 and 4).
    tau_ = 0.3
    fg = lambda t: np.exp(-t ** 2 / (2 * tau_ ** 2))    # noqa: E731
    kk = np.linspace(0.05, 5.0, 12)
    w0 = np.sqrt(kk * kk + 1.0)
    res1, res2 = [], []
    for eps in (0.1, 0.2):
        ex = qp.bogoliubov_boson(lambda t, eps=eps: w0 ** 2 + eps * fg(t), -8 * tau_, 8 * tau_, rtol=1e-8)["beta2"]
        rb2 = born2_scalar_mode(lambda t, eps=eps: eps * fg(t), w0, -8 * tau_, 8 * tau_)
        res1.append(np.max(np.abs(ex / rb2["beta2_born1"] - 1)))
        res2.append(np.max(np.abs(ex / rb2["beta2_born2"] - 1)))
    check(f"Gaussian V, per mode: Born-2 residual {res2[0]:.2g} is < Born-1 residual {res1[0]:.2g} / 10 at eps = 0.1",
          float(res2[0] < res1[0] / 10), 1.0, 0)
    check("   Born-1 residual ratio (eps 0.2 vs 0.1) ~ 2 (O(eps)): in [1.6, 2.4]", res1[1] / res1[0], 2.0, 0.4)
    check("   Born-2 residual ratio ~ 4 (O(eps^2)): in [3.2, 5.6]", res2[1] / res2[0], 4.4, 1.2)
    #     Number density: Born-1 part = qp.born_scalar_homogeneous (spectral form, independent code), particles.
    nb = born2_scalar_number_density(lambda t: 0.1 * fg(t), -8 * tau_, 8 * tau_, 1.0, 12.0, n=48)
    #     qp integrates over the pair energy with plain Gauss-Legendre across the sqrt threshold at 2m, which converges
    #     only like n^-3 (measured rel. error 1.6e-6, 2.5e-8, 3e-9 at n_omega = 200, 800, 1600; this module's k-space sum
    #     is converged to 1e-14 at 48 nodes): n_omega = 800 and tol 1e-7 (4x qp's quadrature error there).
    qb = qp.born_scalar_homogeneous(lambda t: 0.1 * fg(t), -8 * tau_, 8 * tau_, 1.0, 24.0, n_omega=800)["particles_per_volume"]
    check("number density Born-1 = qp.born_scalar_homogeneous particles (independent spectral form)",
          nb["particles_per_volume_born1"], qb, 1e-7, rel=True)
    # C3. Two-level (spinor QED) second order against qp's exact two-level solver: eA(t) = a exp(-t^2/2tau^2) (int E dt = 0),
    #     m = 1, k_perp = 0.3, 8 values of k_par. Residual ratios for amplitude doubling as in C2.
    kz = np.linspace(-1.5, 1.5, 8)
    res1, res2 = [], []
    for amp in (0.1, 0.2):
        eA = lambda t, amp=amp: amp * fg(t)       # noqa: E731
        rq = qp.bogoliubov_fermion_efield(lambda t: kz - eA(t), np.full_like(kz, math.sqrt(1.09)), -8 * tau_, 8 * tau_,
                                          rtol=1e-8)["n"]
        rb2 = born2_fermion_efield_mode(eA, kz, 0.3, 1.0, -8 * tau_, 8 * tau_)
        res1.append(np.max(np.abs(rq / rb2["n_born1"] - 1)))
        res2.append(np.max(np.abs(rq / rb2["n_born2"] - 1)))
    check(f"spinor QED Born-2 residual {res2[0]:.2g} < Born-1 residual {res1[0]:.2g} / 5 at eA = 0.1", float(res2[0] < res1[0] / 5),
          1.0, 0)
    check("   spinor Born-1 residual ratio ~ 2: in [1.6, 2.4]", res1[1] / res1[0], 2.0, 0.4)
    check("   spinor Born-2 residual ratio ~ 4: in [3.2, 5.6]", res2[1] / res2[0], 4.4, 1.2)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


# ---------------------------------------------------------------- convergence studies (slow)
def _convergence() -> int:
    """Error budgets of the mp solver, and the phase integral against it where no closed form exists."""
    print("A. tanh model k = 0.5, m = 1, A = 2, B = 1: mp solver error budget vs rho")
    for rho in (0.2, 0.1, 0.07, 0.05):
        w2f, (t0, t1) = tanh_model_mp(0.5, 1.0, 2.0, 1.0, rho)
        r = bogoliubov_boson_mp(w2f, t0, t1, rtol=1e-8)
        ref = tanh_model_beta2_mp(0.5, 1.0, 2.0, 1.0, rho)
        print(f"  rho={rho}: exact {mp.nstr(ref, 8)}, solver {mp.nstr(r['beta2'], 8)}, true rel. err "
              f"{float(abs(r['beta2'] / ref - 1)):.2e}, estimated {r['beta2_relerr']:.2e} (dps {r['dps']}, steps {r['steps']})")
    print("A'. fixed steps at rho = 0.07 (dps 45): relative error vs steps (4th order, exact in the tails)")
    w2f, (t0, t1) = tanh_model_mp(0.5, 1.0, 2.0, 1.0, 0.07)
    ref = tanh_model_beta2_mp(0.5, 1.0, 2.0, 1.0, 0.07)
    for n in (1000, 1500, 2000, 4000, 8000):
        b, _ = _magnus_boson_mp(w2f, t0, t1, n, 45)
        print(f"  steps {n}: rel. error {float(abs(abs(b) ** 2 / ref - 1)):.2e}")
    print("B. Poeschl-Teller dip w0 = 1, V0 = 0.5: phase integral vs exact as rho -> 0 (relative error O(rho))")
    for rho in (0.2, 0.1, 0.05, 0.025):
        w2f, _ = poschl_teller_mp(1.0, 0.5, rho)
        pt = phase_integral_beta2(w2f, (-2 / rho, 2 / rho), 1.7 / rho)
        ex = poschl_teller_beta2_mp(1.0, 0.5, rho)
        print(f"  rho={rho}: exact {mp.nstr(ex, 6)}, PI {mp.nstr(pt['beta2'], 6)}, exact/PI - 1 = {float(ex / pt['beta2'] - 1):+.3e}"
              f" (cf. exp(-pi rho/(4 sqrt V0)) - 1 = {math.exp(-PI * rho / (4 * math.sqrt(0.5))) - 1:+.3e})")
    print("B'. Two dips (no closed form), omega^2 = 1 - 0.2[sech^2(rho(t-T)) + sech^2(rho(t+T))], rho = 0.03: PI (Dumlu-Dunne"
          " eq. 7) vs mp solver, |beta|^2 ~ 1e-50")
    rho = 0.03
    for T in (150.0, 150.4, 150.8, 151.2):
        Tm, rh = mp.mpf(T), mp.mpf(rho)
        w2f = lambda t, Tm=Tm: 1 - mp.mpf(0.2) * (1 / mp.cosh(rh * (t - Tm)) ** 2 + 1 / mp.cosh(rh * (t + Tm)) ** 2)  # noqa: E731
        ends = T + 40 / rho
        r = bogoliubov_boson_mp(w2f, -ends, ends)
        pt = phase_integral_beta2(w2f, (-T - 2 / rho, T + 2 / rho), 1.7 / rho, grid=(80, 16))
        env = 4 * math.exp(-2 * pt["K"][0])
        print(f"  T={T}: exact {mp.nstr(r['beta2'], 6)} (est. rel. err {r['beta2_relerr']:.1e}), PI {mp.nstr(pt['beta2'], 6)}, "
              f"|exact - PI|/envelope = {float(abs(r['beta2'] - pt['beta2'])) / env:.3f}")
    print("C. Born residuals vs eps (Gaussian V, tau = 0.3, m = 1): Born-1 ~ eps, Born-2 ~ eps^2")
    fg = lambda t: np.exp(-t ** 2 / 0.18)          # noqa: E731
    kk = np.linspace(0.05, 5.0, 12)
    w0 = np.sqrt(kk * kk + 1)
    for eps in (0.025, 0.05, 0.1, 0.2, 0.4):
        ex = qp.bogoliubov_boson(lambda t: w0 ** 2 + eps * fg(t), -3.6, 3.6, rtol=1e-10)["beta2"]
        rb = born2_scalar_mode(lambda t: eps * fg(t), w0, -3.6, 3.6)
        print(f"  eps={eps}: max|exact/Born1 - 1| = {np.max(np.abs(ex / rb['beta2_born1'] - 1)):.3e}, "
              f"max|exact/Born2 - 1| = {np.max(np.abs(ex / rb['beta2_born2'] - 1)):.3e}")
    return 0


# ---------------------------------------------------------------- command line
def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("convergence", help="slow: mp-solver error budgets, phase integral vs exact below 1e-40, Born scaling")
    tp = sub.add_parser("tanh", help="tanh model: high-precision solver vs closed form vs phase integral vs qp (double)")
    for name in ("m", "rho", "k"):
        tp.add_argument(f"--{name}", required=True, help="energy: a number in your natural unit, or e.g. '1 eV'")
    tp.add_argument("--A", type=float, required=True)
    tp.add_argument("--B", type=float, required=True)
    sp = sub.add_parser("sauter", help="Sauter pulse E0 sech^2(t/tau), one mode: exact, phase integral, high-precision solver")
    sp.add_argument("--m", default="0.51099895 MeV", help="mass (default electron); a bare number is in your natural unit")
    sp.add_argument("--E", required=True, help="peak field: '1e17 V/m', or a bare number = eE0 in (natural unit)^2")
    sp.add_argument("--tau", required=True, help="pulse time: '1e-18 s', or a bare number in 1/(natural unit)")
    sp.add_argument("--kpar", default="0", help="canonical momentum along E (energy)")
    sp.add_argument("--kperp", default="0", help="transverse momentum (energy)")
    sp.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    bp = sub.add_parser("born2", help="Gaussian V = eps exp(-t^2/2tau^2): particles per volume at Born-1, Born-2, exact (qp)")
    bp.add_argument("--m", type=float, default=1.0, help="mass (sets the unit)")
    bp.add_argument("--eps", type=float, nargs="+", default=[0.1, 0.2], help="amplitudes of V in m^2")
    bp.add_argument("--tau", type=float, default=0.3, help="width in 1/m")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "tanh":
            m, rho, k = qp._energy(args.m), qp._energy(args.rho), qp._energy(args.k)
            w2f, (t0, t1) = tanh_model_mp(k, m, args.A, args.B, rho)
            ref = tanh_model_beta2_mp(k, m, args.A, args.B, rho)
            r = bogoliubov_boson_mp(w2f, t0, t1)
            print(f"|beta_k|^2 (mean particles in mode k, in-in): closed form {mp.nstr(ref, 12)}")
            print(f"  high-precision solver {mp.nstr(r['beta2'], 12)} +- {mp.nstr(r['beta2_err'], 2)} "
                  f"(dps {r['dps']}, steps {r['steps']}, resolved {r['resolved']})")
            pt = phase_integral_beta2(w2f, (-3 / rho, 3 / rho), 2 / rho)
            print(f"  phase integral {mp.nstr(pt['beta2'], 12)} ({pt['label']}); exponent 2K = {pt['exponent']:.10g}")
            rq = qp.bogoliubov_boson(lambda t: np.array([k * k + m * m * (args.A + args.B * np.tanh(rho * t))]), t0, t1)
            print(f"  qp double precision {rq['beta2'][0]:.6g}, floor {rq['floor'][0]:.2g}, resolved {bool(rq['resolved'][0])}")
            return 0
        if args.cmd == "born2":
            fg = lambda t: np.exp(-t ** 2 / (2 * args.tau ** 2))   # noqa: E731
            t0, t1 = -12 * args.tau, 12 * args.tau
            kmax = 12.0 * max(args.m, 1.0 / args.tau)
            for eps in args.eps:
                nb = born2_scalar_number_density(lambda t: eps * fg(t), t0, t1, args.m, kmax, n=48)
                ex = qp.number_density_isotropic(
                    lambda k: qp.bogoliubov_boson(lambda t: k * k + args.m ** 2 + eps * fg(t), t0, t1, rtol=1e-8)["beta2"],
                    kmax, n=48)
                print(f"eps = {eps}: particles per volume (real field: pairs = half) Born-1 {nb['particles_per_volume_born1']:.6g}, "
                      f"Born-2 {nb['particles_per_volume_born2']:.6g}, exact {ex:.6g} (in units of m^3; lam_max {nb['lam_max']:.3g})")
            return 0
        # sauter
        from unit_tools import Q

        def energy2(text):
            try:
                return float(text)
            except ValueError:
                return qp.eE_from_field_SI(Q(text).expect("V/m").si)

        def time_(text):
            try:
                return float(text)
            except ValueError:
                return qp.time_to_inverse_eV(Q(text).expect("time").si)
        m, eE0, tau = qp._energy(args.m), energy2(args.E), time_(args.tau)
        kz, kp = qp._energy(args.kpar), qp._energy(args.kperp)
        fermion = not args.scalar
        ex = sauter_n_mp(kz, kp, m, eE0, tau, fermion)
        om2, pf, ep, (t0, t1) = sauter_mp(kz, kp, m, eE0, tau)
        print(f"{'spinor (per spin)' if fermion else 'scalar'} QED, m = {m:.6g}, eE0 = {eE0:.6g} (m^2 units: {eE0 / m ** 2:.4g}), "
              f"tau = {tau:.6g} (m tau = {m * tau:.4g}), eE0 tau^2 = {eE0 * tau * tau:.4g}")
        print(f"exact n_k (GG eq. {'42' if fermion else '43'}, in-in, per mode): {mp.nstr(ex, 10)}")
        pt = phase_integral_beta2(om2, (-3 * tau, 3 * tau), 1.6 * tau, "fermion" if fermion else "boson")
        print(f"phase integral: {mp.nstr(pt['beta2'], 10)}, exponent 2K = {pt['exponent']:.10g} ({pt['label']})")
        if kz == 0 and kp == 0:
            print(f"Dunne-Schubert S0 (k = 0): {dunne_schubert_exponent(m, eE0, 1 / tau):.10g}")
        steps = _omega_max(om2, t0, t1) * (t1 - t0) / 0.8
        if steps <= 2e4:
            r = bogoliubov_fermion_mp(pf, ep, t0, t1) if fermion else bogoliubov_boson_mp(om2, t0, t1)
            v = r["n"] if fermion else r["beta2"]
            print(f"high-precision solver: {mp.nstr(v, 10)} (relative error {r['n_relerr' if fermion else 'beta2_relerr']:.1e})")
        else:
            print(f"high-precision solver skipped: ~{steps:.3g} steps needed (m tau too large); the phase integral is the tool here")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
